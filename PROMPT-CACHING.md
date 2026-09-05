---
produto: Prompt caching Free gpt-oss
preco_BRL: 10
fontes: console.groq.com/docs/prompt-caching, /docs/rate-limits, /docs/models
gerado_com: docs oficiais + openai/gpt-oss-20b smoke
---

# Groq Free-tier: prompt caching (prefix match)

Docs: [prompt-caching](https://console.groq.com/docs/prompt-caching). Caching é **automático** nos modelos suportados — sem flag extra e sem fee.

## Modelos Free com cache

| ID |
|----|
| `openai/gpt-oss-20b` |
| `openai/gpt-oss-120b` |
| `openai/gpt-oss-safeguard-20b` |

Cotas Free chat típicas: ver [rate-limits](https://console.groq.com/docs/rate-limits) (**30 RPM / 1K RPD / 8K TPM / 200K TPD**). Tokens em cache **não contam** no rate limit (docs).

## Como maximizar hit

1. Prefixo estático primeiro: system, tools, few-shot, schema
2. Conteúdo variável por último: pergunta do user, IDs, timestamps
3. Match **exato** do prefixo; mudanças mínimas quebram o cache
4. Meça `usage.prompt_tokens_details.cached_tokens`

## Batch ≠ Free

Batch/Flex exigem upgrade Developer (docs rate-limits). No Free, use caching + scripts sync.

Script: `prompt_cache_demo.py`.

## CTA

https://ziuluiziul.github.io/groq-round1-offer/ — tip **R$10** / kit **R$20**.
