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

# Cheatsheet Free Plan Limits — GroqCloud (2026-09)

Fonte: https://console.groq.com/docs/rate-limits (aba Free Plan Limits). Limites ao nível da **organização**. Cached tokens não contam. Free ≠ coluna Developer em /docs/models.

## Chat Free (RPM / RPD / TPM / TPD)

| Model ID | RPM | RPD | TPM | TPD |
|---|---:|---:|---:|---:|
| `openai/gpt-oss-20b` | 30 | 1K | 8K | 200K |
| `openai/gpt-oss-120b` | 30 | 1K | 8K | 200K |
| `openai/gpt-oss-safeguard-20b` | 30 | 1K | 8K | 200K |
| `qwen/qwen3.6-27b` | 30 | 1K | 8K | 200K |
| `qwen/qwen3.8-27b` | 30 | 1K | 8K | 200K |

## Outros Free (só se o entregável for desse cenário)

| Model ID | RPM | RPD | TPM | TPD | ASH | ASD |
|---|---:|---:|---:|---:|---:|---:|
| `groq/compound` | 30 | 250 | 70K | — | — | — |
| `groq/compound-mini` | 30 | 250 | 70K | — | — | — |
| `whisper-large-v3` | 20 | 2K | — | — | 7.2K | 28.8K |
| `whisper-large-v3-turbo` | 20 | 2K | — | — | 7.2K | 28.8K |
| `canopylabs/orpheus-v1-english` | 10 | 100 | 1.2K | 3.6K | — | — |
| `canopylabs/orpheus-arabic-saudi` | 10 | 100 | 1.2K | 3.6K | — | — |
| `meta-llama/llama-prompt-guard-2-22m` | 30 | 14.4K | 15K | 500K | — | — |
| `meta-llama/llama-prompt-guard-2-86m` | 30 | 14.4K | 15K | 500K | — | — |

## Headers (sempre)

| Header | Significado |
|---|---|
| `x-ratelimit-remaining-requests` | RPD restante |
| `x-ratelimit-remaining-tokens` | TPM restante |
| `retry-after` | só em 429 |

## EOL (docs/deprecations)

Shutdown **16/08/2026**: `llama-3.1-8b-instant` → `openai/gpt-oss-20b`; `llama-3.3-70b-versatile` → `openai/gpt-oss-120b` ou `qwen/qwen3.6-27b`.

## Checklist

1. Key só via `GROQ_API_KEY` (env)
2. `User-Agent: groq-python/1.0` + HTTP/1.1 se WAF
3. GET `https://api.groq.com/openai/v1/models` para IDs vivos
4. Em 429: respeitar `Retry-After`; não estourar RPD/TPM
5. Developer = PAYG (sem mensalidade fixa publicada) — só com OK Luiz

Ver também: `MULTI-MODEL-FAILOVER.md` + `multi_model_chat.py`
