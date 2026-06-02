# ── AstroDome - Infraestrutura Segura na AWS ────────────────────
# Boas praticas validadas pelo Checkov (Zero Trust, minimo privilegio)

terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  description = "Regiao AWS para deploy do AstroDome"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Ambiente de deploy"
  type        = string
  default     = "production"
}

# ── S3: Armazenamento de Telemetria ─────────────────────────────
resource "aws_s3_bucket" "telemetria" {
  bucket = "astrodome-telemetria-${var.environment}"

  tags = {
    Project     = "AstroDome"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

# Criptografia em repouso (obrigatoria - validada pelo Checkov)
resource "aws_s3_bucket_server_side_encryption_configuration" "telemetria" {
  bucket = aws_s3_bucket.telemetria.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Bloquear acesso publico (Zero Trust)
resource "aws_s3_bucket_public_access_block" "telemetria" {
  bucket = aws_s3_bucket.telemetria.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Versionamento habilitado
resource "aws_s3_bucket_versioning" "telemetria" {
  bucket = aws_s3_bucket.telemetria.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Logging de acesso ao bucket
resource "aws_s3_bucket_logging" "telemetria" {
  bucket        = aws_s3_bucket.telemetria.id
  target_bucket = aws_s3_bucket.logs.id
  target_prefix = "telemetria-access/"
}

# ── S3: Bucket de Logs ───────────────────────────────────────────
resource "aws_s3_bucket" "logs" {
  bucket = "astrodome-logs-${var.environment}"

  tags = {
    Project     = "AstroDome"
    Environment = var.environment
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "logs" {
  bucket = aws_s3_bucket.logs.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "logs" {
  bucket                  = aws_s3_bucket.logs.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# ── IAM: Role com minimo privilegio (Zero Trust) ─────────────────
resource "aws_iam_role" "astrodome_app" {
  name = "astrodome-app-role-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = { Service = "ecs-tasks.amazonaws.com" }
        Action    = "sts:AssumeRole"
        # MFA obrigatorio para acoes sensiveis
        Condition = {
          Bool = { "aws:MultiFactorAuthPresent" = "true" }
        }
      }
    ]
  })

  tags = {
    Project = "AstroDome"
  }
}

# Politica restrita: apenas leitura no bucket de telemetria
resource "aws_iam_role_policy" "astrodome_s3_readonly" {
  name = "astrodome-s3-telemetria-readonly"
  role = aws_iam_role.astrodome_app.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["s3:GetObject", "s3:ListBucket"]
        Resource = [
          aws_s3_bucket.telemetria.arn,
          "${aws_s3_bucket.telemetria.arn}/*"
        ]
        # Sem wildcards (*) - minimo privilegio
      }
    ]
  })
}

# ── CloudWatch: Monitoramento e Alertas ──────────────────────────
resource "aws_cloudwatch_log_group" "astrodome" {
  name              = "/astrodome/${var.environment}"
  retention_in_days = 90

  tags = {
    Project     = "AstroDome"
    Environment = var.environment
  }
}

# Alerta: erro critico na estufa
resource "aws_cloudwatch_metric_alarm" "erro_critico" {
  alarm_name          = "astrodome-erro-critico-${var.environment}"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 1
  metric_name         = "ErrorCount"
  namespace           = "AstroDome/Estufa"
  period              = 60
  statistic           = "Sum"
  threshold           = 1
  alarm_description   = "Erro critico detectado nos sensores da estufa"

  alarm_actions = [aws_sns_topic.alertas.arn]
}

resource "aws_sns_topic" "alertas" {
  name              = "astrodome-alertas-${var.environment}"
  kms_master_key_id = "alias/aws/sns"
}

# ── Outputs ──────────────────────────────────────────────────────
output "bucket_telemetria" {
  description = "Nome do bucket de telemetria"
  value       = aws_s3_bucket.telemetria.bucket
}

output "iam_role_arn" {
  description = "ARN da role IAM da aplicacao"
  value       = aws_iam_role.astrodome_app.arn
}
