---
produto: Cheatsheet Free Plan Limits Groq
preco_sugerido_BRL: 10
pix: pix-r10.txt / qr-r10.png
modelo: openai/gpt-oss-20b
http: 200
rpd_rem: 999
tpm_rem: 6897
region: msp
usage: {"queue_time": 0.10983526, "prompt_tokens": 465, "prompt_time": 0.022909321, "completion_tokens": 750, "completion_time": 0.789056253, "total_tokens": 1215, "total_time": 0.811965574, "completion_tokens_details": {"reasoning_tokens": 152}}
fontes: https://console.groq.com/docs/rate-limits · https://console.groq.com/docs/deprecations
---

# Cheatsheet: Limites do Plano Free – GroqCloud (2026‑09)

> **Fonte oficial**: <https://console.groq.com/docs/rate-limits> (Free Plan Limits)

---

## 1. Visão geral dos limites

| Limite | Valor (Free) | Unidade | Observação |
|--------|--------------|---------|------------|
| **RPM** (Requests per Minute) | 30 | req/min | Aplicável a *chat* e *compound* |
| **RPD** (Requests per Day) | 1 000 | req/dia | Aplicável a *chat* e *compound* |
| **TPM** (Tokens per Minute) | 8 000 | tokens/min | Aplicável a *chat* e *compound* |
| **TPD** (Tokens per Day) | 200 000 | tokens/dia | Aplicável a *chat* e *compound* |
| **RPD (Whisper)** | 2 000 | req/dia | 20 RPM |
| **TPD (Whisper)** | 2 000 | tokens/dia | 20 RPM |
| **RPD (Orpheus TTS)** | 100 | req/dia | 10 RPM |
| **TPD (Orpheus TTS)** | 1 200 | tokens/dia | 10 RPM |
| **RPD (Compound / Compound‑Mini)** | 250 | req/dia | 30 RPM |
| **TPD (Compound / Compound‑Mini)** | 70 000 | tokens/dia | 30 RPM |

> **Nota**: Os limites são **por organização**. Se a sua conta tem múltiplos usuários, o total é compartilhado entre eles.

---

## 2. Respostas de erro e cabeçalhos

| Código | Mensagem | Cabeçalhos relevantes |
|--------|----------|-----------------------|
| **429** | Too Many Requests | `Retry-After: <segundos>` |
| **Headers** | | `x-ratelimit-remaining-requests: <RPD>`<br>`x-ratelimit-remaining-tokens: <TPM>` |

> **Dica**: Monitore esses cabeçalhos para evitar bloqueios inesperados.

---

## 3. Modelos Free (Chat)

| Modelo | RPM | RPD | TPM | TPD |
|--------|-----|-----|-----|-----|
| `openai/gpt-oss-20b` | 30 | 1 000 | 8 000 | 200 000 |
| `openai/gpt-oss-120b` | 30 | 1 000 | 8 000 | 200 000 |
| `openai/gpt-oss-safeguard