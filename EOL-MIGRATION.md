---
produto: Migração EOL Llama→gpt-oss/Qwen
preco_sugerido_BRL: 10
pix: pix-r10.txt / qr-r10.png
modelo: openai/gpt-oss-120b
http: 200
rpd_rem: 999
tpm_rem: 7303
region: msp
usage: {"queue_time": 0.147877289, "prompt_tokens": 409, "prompt_time": 0.018250539, "completion_tokens": 750, "completion_time": 1.58812885, "total_tokens": 1159, "total_time": 1.606379389, "completion_tokens_details": {"reasoning_tokens": 94}}
fontes: https://console.groq.com/docs/deprecations · https://console.groq.com/docs/rate-limits
---

# Guia Técnico — Migração EOL: **Llama Free → gpt‑oss / Qwen (Groq Cloud)**  

> **Objetivo:** substituir os modelos Llama que serão descontinuados em 2026 pelos equivalentes disponíveis no Groq Cloud (gpt‑oss ou Qwen) com o mínimo de interrupção e mantendo a conformidade com os limites do plano Free.

---

## 1. Contexto de Descontinuação (EOL)

| Modelo Llama (Free) | Data de shutdown | Substituto recomendado (Groq) |
|----------------------|------------------|--------------------------------|
| `llama-3.1-8b-instant` | **16/08/2026** | `openai/gpt-oss-20b` |
| `llama-3.3-70b-versatile` | **16/08/2026** | `openai/gpt-oss-120b` **ou** `qwen/qwen3.6-27b` |
| `meta-llama/llama-4-scout-17b-16e-instruct` | **17/07/2026** | `openai/gpt-oss-120b` **ou** `qwen/qwen3.6-27b` |
| `qwen/qwen3-32b` | **17/07/2026** | `openai/gpt-oss-120b` |
| `meta-llama/llama-guard-4-12b` | **03/05/2026** | `openai/gpt-oss-safeguard-20b` |

> Fonte oficial: <https://console.groq.com/docs/deprecations>

Nota: `qwen/qwen3-32b` também encerra em **17/07/2026** (substituir por `openai/gpt-oss-120b`). Não usar como fallback.

---

## 2. Limites do Plano Free (Groq Cloud)

| Métrica | Valor máximo |
|---------|--------------|
| **Requests per minute (RPM)** | 30 |
| **Requests per day (RPD)** | 1 000 |
| **Tokens per minute (TPM)** | 8 000 |
| **Tokens per day (TPD)** | 200 000 |

Documentação: <https://console.groq.com/docs/rate-limits>

> **Importante:** Free ≠ coluna Developer em `/docs/models`. Free tem rate-limits próprios; Developer = PAYG (sem mensalidade fixa publicada) — só com OK Luiz.

---

## 3. Checklist de Migração

1. **Atualizar o Model ID**  
   - Substitua `llama-3.1-8b-instant` por `openai/gpt-oss-20b`.  
   - Substitua `llama-3.3-70b-versatile` por `openai/gpt-oss-120b` **ou** `qwen/qwen3.6-27b`, conforme seu perfil de custo/latência.  

2. **Verificar a disponibilidade dos novos modelos**  
   ```bash
   curl -H "Authorization: Bearer $GROQ_API_KEY" \
        https://api.g