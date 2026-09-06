---
produto: Responses API Groq Free (beta)
preco_BRL: 20
fontes: console.groq.com/docs/responses-api, /models, /rate-limits, /deprecations
---

# Groq Free-tier: Responses API (`/v1/responses`)

Objetivo: usar o endpoint **Responses** (compat OpenAI) no Free, com `output_text` e `reasoning.effort` baixo — sem top-up.

## Chamada mínima

`POST https://api.groq.com/openai/v1/responses`

```json
{
  "model": "openai/gpt-oss-20b",
  "input": "One sentence: what is GroqCloud free-tier for?",
  "reasoning": {"effort": "low"},
  "max_output_tokens": 128
}
```

- Cliente: `base_url=https://api.groq.com/openai/v1` + `GROQ_API_KEY`.
- Resposta: leia `output_text` (atalho) ou itens `output[]` (`type=message` / `type=reasoning`).
- **Stateful ainda não**: Groq não suporta `previous_response_id` / `store` — você guarda o histórico e reenvia `input` a cada turno ([docs](https://console.groq.com/docs/responses-api)).
- Built-ins `browser_search` / `code_interpreter`: só `openai/gpt-oss-20b` e `openai/gpt-oss-120b` — gasta cota; no Free prefira demo curta.

## Modelos Free úteis

Confirme IDs vivos em [models](https://console.groq.com/docs/models) e cotas em [rate-limits](https://console.groq.com/docs/rate-limits):

- `openai/gpt-oss-20b` / `openai/gpt-oss-120b` (reasoning + tools built-in)
- `qwen/qwen3.6-27b` / `qwen/qwen3.8-27b` (texto / visão via Responses)

Llama 3.1/3.3 no Free podem sumir — [deprecations](https://console.groq.com/docs/deprecations).

## Quotas

Headers `x-ratelimit-remaining-requests` (=RPD) e `x-ratelimit-remaining-tokens` (=TPM). Se RPD usado ≥80% ou TPM crítico → **parar**. Sem spend.

Script: `responses_mini.py`.

## CTA

https://ziuluiziul.github.io/groq-round1-offer/ — kit **R$20** (`pix-r20`) / tip **R$10**.
