# ── Stage 1: Build ──────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /app

# Instala dependencias em camada separada (cache otimizado)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ── Stage 2: Runtime (imagem final menor e mais segura) ──────────
FROM python:3.11-slim AS runtime

# Boas praticas de seguranca: usuario nao-root
RUN groupadd -r astrodome && useradd -r -g astrodome astrodome

WORKDIR /app

# Copia dependencias do stage de build
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copia o codigo-fonte
COPY src/ ./src/

# Define usuario nao-root para execucao
USER astrodome

# Variaveis de ambiente (valores reais vem do GitHub Secrets / runtime)
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    NASA_API_KEY="" \
    TELEMETRY_DB_PASSWORD="" \
    ORBITAL_API_TOKEN=""

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import src.main; print('OK')" || exit 1

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
