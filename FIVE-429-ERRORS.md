---
produto: 5 erros 429/TPM Groq Free
preco_BRL: 10
fontes: console.groq.com/docs/rate-limits, console.groq.com/docs/deprecations
---

# Groq Free-tier: 5 erros 429/TPM e como evitar

O Free Plan aplica tetos de RPM/RPD/TPM/TPD (e, em alguns casos, OTPM). Estourar qualquer um devolve **429**. Números exatos: [rate-limits](https://console.groq.com/docs/rate-limits) + headers `x-ratelimit-*` da sua org — **não invente RPM**.

1. **Ignorar `retry-after`** — em 429, espere o valor do header (segundos) antes de reenviar.
2. **Prompt/completion grande no mesmo minuto** — TPM/OTPM caem rápido; use `max_tokens` baixo e lotes.
3. **Burst de requests** — respeite RPM; serialize ou fila com jitter.
4. **Não ler `x-ratelimit-remaining-tokens`** — se estiver baixo, pause até `x-ratelimit-reset-tokens`.
5. **Chamar modelo EOL** — IDs removidos geram erro/comportamento estranho; confira [deprecations](https://console.groq.com/docs/deprecations) e a lista live `GET /openai/v1/models`.

Extra WAF: `User-Agent: groq-python/1.0` + HTTP/1.1 evita 403 que parece “API quebrada”.

CTA: https://ziuluiziul.github.io/groq-round1-offer/ — tip PIX **R$10**.
