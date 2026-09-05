---
produto: streaming SSE Groq Free
preco_BRL: 20
fontes: console.groq.com/docs/rate-limits, console.groq.com/docs/models
---

# Groq Free-tier: streaming SSE sem estourar TPM

Guia prático para `POST /openai/v1/chat/completions` com `"stream": true` no plano Free.

## O que muda com stream

- Continua sendo **1 request** (conta no RPM/RPD).
- Os **tokens** (prompt + completion) continuam no **TPM** / TPD.
- A resposta vem em eventos SSE: linhas `data: {json}` e termina com `data: [DONE]`.

Leia os limites Free oficiais em [rate-limits](https://console.groq.com/docs/rate-limits) (tabela Free Plan / freeRows) e os modelos em [models](https://console.groq.com/docs/models). **Não invente números** — use a tabela + headers da sua org.

## Headers úteis (sempre presentes)

| Header | Significado (docs) |
|--------|--------------------|
| `x-ratelimit-remaining-requests` | RPD restante |
| `x-ratelimit-remaining-tokens` | TPM restante |
| `x-ratelimit-reset-tokens` | quando o TPM recarrega |
| `retry-after` | só em **429** |

## Mini fluxo (Python stdlib)

1. `HTTPSConnection` + `User-Agent: groq-python/1.0` (evita WAF 403).
2. Body JSON com `stream: true`, `max_tokens` baixo, prompt curto.
3. Ler linha a linha; ignorar vazias; se começa com `data: `, parsear JSON (exceto `[DONE]`).
4. Concatenar `choices[0].delta.content` (quando existir). Em `openai/gpt-oss-*` o stream pode vir em `delta.reasoning` antes do content — para demo use `qwen/qwen3.6-27b`.
5. Em **429**: dormir `retry-after` (ou reset de tokens) e **não** martelar.

Script pronto: `stream_chat.py` (key só via env `GROQ_API_KEY`).

## Boas práticas Free

- Preferir modelos chat listados no Free Plan Limits (ex.: `qwen/qwen3.6-27b`, `openai/gpt-oss-20b`) — confirme em rate-limits/models.
- Se OTPM/TPM apertar, baixe `max_tokens` e espere o reset; upgrade pago **só com autorização**.
- Pare a fila se RPD usado ≥ ~80% (regra operacional deste kit).

## CTA

Landing PIX (R$10 tip / R$20 kit / R$50+): https://ziuluiziul.github.io/groq-round1-offer/  
Repo: https://github.com/Ziuluiziul/groq-round1-offer
