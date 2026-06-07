# GreenHouse - DevSecOps Module 

> Ecossistema Fechado de Suporte à Vida com segurança integrada desde o código até o deploy.

---

## Sobre o Projeto

O **AstroDome** é um sistema biológico inteligente e autônomo projetado para gerenciar estufas em ambientes espaciais (Lua e Marte). Ele opera em quatro pilares: Mapeamento Orbital, Monitoramento Interno da Estufa, Inteligência Botânica por Visão Computacional e Painel de Comando para Colonos.

Este repositório contém o **Módulo de DevSecOps** integrado ao projeto, garantindo que a solução seja construída com segurança desde o início.

---

## Estrutura do Repositório

```
astrodome/
├── .github/
│   └── workflows/
│       └── astrodome-devsecops.yml   # Pipeline CI/CD com controles de segurança
├── src/
│   └── ...                           # Código-fonte dos módulos do AstroDome
├── infra/
│   └── main.tf                       # Infraestrutura como código (Terraform)
├── security/
│   └── security-policy.yaml          # Política de segurança como código
├── simulation/
│   └── SIMULACAO.md                  # Documentação da simulação DevSecOps
└── README.md
```

---

## Como o DevSecOps foi Integrado

### Pipeline CI/CD com 5 Etapas de Segurança

Cada push no repositório aciona automaticamente o pipeline abaixo:

```
[ Push/PR ]
     │
     ▼
[ 1. Scan de Segredos ]  ← Gitleaks detecta chaves de API expostas
     │
     ▼
[ 2. Análise Estática ]  ← Bandit (SAST) + Safety (dependências)
     │
     ▼
[ 3. Scan de Contêiner ] ← Trivy verifica vulnerabilidades na imagem Docker
     │
     ▼
[ 4. Validação de Infra ] ← Checkov verifica Terraform (Zero Trust, criptografia)
     │
     ▼
[ 5. Deploy Seguro ]     ← Só ocorre se TODAS as etapas anteriores passaram
```

### Controles Implementados

| Controle | Ferramenta | O que protege no AstroDome |
|----------|-----------|---------------------------|
| Gestão de Segredos | GitHub Secrets | Chaves NASA API, senhas do banco de telemetria |
| SAST | Bandit | Código Python dos módulos de IA botânica |
| Análise de Dependências | Safety | Bibliotecas OpenCV, TensorFlow, FastAPI |
| Segurança em Contêineres | Trivy | Imagem Docker dos microsserviços |
| Infraestrutura Segura | Checkov + Terraform | Recursos AWS/GCP com mínimo privilégio |

---

## Configurando os Secrets no GitHub

Para que o pipeline funcione, configure os seguintes secrets em:
`Settings > Secrets and variables > Actions`

| Secret | Descrição |
|--------|-----------|
| `NASA_API_KEY` | Chave de acesso à API de dados orbitais |
| `TELEMETRY_DB_PASSWORD` | Senha do banco de dados de telemetria |
| `ORBITAL_API_TOKEN` | Token de autenticação do serviço orbital |

> **NUNCA** coloque esses valores diretamente no código ou em arquivos YAML commitados.

---

## Executando o Scan Localmente

```bash
# Instalar ferramentas
pip install bandit safety checkov

# Scan de vulnerabilidades no código
bandit -r ./src -ll

# Verificar dependências
safety check

# Validar infraestrutura Terraform
checkov -d ./infra --framework terraform
```

---

## Simulação de Incidente

Veja a pasta [`simulation/SIMULACAO.md`](./simulation/SIMULACAO.md) para o cenário completo de:
- **Problema**: Segredo (API Key) exposto em commit
- **Controle**: Gitleaks detecta e bloqueia o pipeline
- **Ação**: Pipeline falha, desenvolvedor é notificado, segredo é removido

---

## Conexão com os ODS

| ODS | Relação |
|-----|---------|
| ODS 2 - Fome Zero | AstroDome viabiliza produção alimentar segura no espaço |
| ODS 9 - Indústria e Inovação | Pipeline DevSecOps garante infraestrutura resiliente e segura |
| ODS 17 - Parcerias | Uso de APIs abertas (NASA) com segurança e conformidade |

---

## Grupo

André de Sousa Neves 
Caio Sato Tominaga 
Eduardo Brites Coutinho 
Isabela Barcellos 
Thaís Gonçalves Leoncio 


Projeto desenvolvido para a **Global Solution 2º Semestre 2026 — FIAP**
Curso: Engenharia de Software | Disciplina: Cibersegurança
