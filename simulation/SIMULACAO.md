# Simulação de Pipeline DevSecOps — AstroDome

## Cenário: Segredo Exposto e Bloqueado pelo Pipeline

---

### Contexto

Um desenvolvedor do AstroDome, ao integrar o módulo de Mapeamento Orbital,
acidentalmente commitou a chave de acesso à NASA API diretamente no código Python:

```python
# modulo_orbital.py  ← ARQUIVO PROBLEMÁTICO
import requests

NASA_API_KEY = "Xk92mPqR7nLw4vBz1tYeAoJd"  # ← SEGREDO EXPOSTO!

def buscar_dados_orbitais(planeta):
    url = f"https://api.nasa.gov/planetary/data?api_key={NASA_API_KEY}"
    return requests.get(url).json()
```

O desenvolvedor executa: `git add . && git commit -m "feat: módulo orbital" && git push`

---

### O Problema Detectado

Assim que o push chega ao GitHub, o pipeline é acionado automaticamente.

**Etapa 1 — Scan de Segredos (Gitleaks)** detecta a chave exposta:

```
┌─────────────────────────────────────────────────────┐
│  GITLEAKS DETECTION REPORT                          │
├─────────────────────────────────────────────────────┤
│  Finding:     Generic API Key                       │
│  File:        src/modulo_orbital.py                 │
│  Line:        5                                     │
│  Commit:      a3f9c12                               │
│  Author:      dev@astrodome.space                   │
│  Description: Hardcoded API key detected            │
│  Match:       NASA_API_KEY = "Xk92mPqR7nLw..."     │
├─────────────────────────────────────────────────────┤
│  [!] Leaks found: 1                                 │
│  Pipeline BLOQUEADO. Deploy cancelado.              │
└─────────────────────────────────────────────────────┘
```

**Resultado no GitHub Actions:**
```
❌ secrets-scan    FAILED  (42s)
⏭️  sast-scan      SKIPPED
⏭️  container-scan SKIPPED
⏭️  policy-check   SKIPPED
⏭️  deploy         SKIPPED
```

O deploy **não acontece**. O sistema protege a missão.

---

### A Ação Tomada

**Passo 1** — O desenvolvedor é notificado por e-mail pelo GitHub.

**Passo 2** — Remove o segredo do código e usa variável de ambiente:

```python
# modulo_orbital.py  ← VERSÃO CORRIGIDA
import requests
import os

def buscar_dados_orbitais(planeta):
    api_key = os.environ.get("NASA_API_KEY")  # ← Seguro!
    url = f"https://api.nasa.gov/planetary/data?api_key={api_key}"
    return requests.get(url).json()
```

**Passo 3** — Configura o segredo no GitHub:
`Settings > Secrets > Actions > New secret`
- Name: `NASA_API_KEY`
- Value: `Xk92mPqR7nLw4vBz1tYeAoJd`

**Passo 4** — Novo push com o código corrigido. Pipeline reexecutado:

```
✅ secrets-scan    PASSED  (38s)
✅ sast-scan       PASSED  (1m 12s)
✅ container-scan  PASSED  (2m 04s)
✅ policy-check    PASSED  (55s)
✅ deploy          PASSED  (30s)
```

**Deploy realizado com sucesso. Missão protegida.** 🚀

---

### Resumo da Simulação

| Item | Detalhe |
|------|---------|
| **Problema** | Chave da NASA API exposta em arquivo Python commitado |
| **Controle que detectou** | Gitleaks — Scan de Segredos (Etapa 1 do pipeline) |
| **Impacto evitado** | Acesso não autorizado à API orbital; comprometimento de dados de missão |
| **Ação tomada** | Pipeline bloqueado, segredo removido do código, cadastrado no GitHub Secrets |
| **Resultado** | Novo push aprovado em todas as 5 etapas; deploy liberado |
