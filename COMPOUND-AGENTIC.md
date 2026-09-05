---
produto: Compound agentic one-shot Free
preco_BRL: 20
fontes: console.groq.com/docs/compound, /docs/rate-limits, /docs/models
gerado_com: docs oficiais + groq/compound-mini smoke
---

# Groq Free-tier: Compound vs chat (agentic one-shot)

Docs: [compound](https://console.groq.com/docs/compound). Compound roda **web search + code execution** no servidor — você não implementa tools custom (ainda não suportado).

## Quando usar o quê

| Caso | Modelo |
|------|--------|
| Pergunta com fato ao vivo / cálculo server-side | `groq/compound` ou `groq/compound-mini` |
| Diálogo linear / tools **locais** (seu código) | chat + [tool-use](https://console.groq.com/docs/tool-use) |
| 1 tool call / menor latência (~3×) | `groq/compound-mini` |
| Vários tool calls no mesmo request | `groq/compound` |

Mesmo endpoint: `POST /openai/v1/chat/completions` com `model` Compound. Inspecione `executed_tools` e `usage_breakdown`.

## Free Plan (tabela oficial)

| ID | RPM | RPD | TPM |
|----|-----|-----|-----|
| `groq/compound` | 30 | 250 | 70K |
| `groq/compound-mini` | 30 | 250 | 70K |

Fonte: [rate-limits](https://console.groq.com/docs/rate-limits). RPD Compound é **menor** que chat 1K — não misture tetos. ≥80% RPD → parar.

Script: `compound_mini.py`. HIPAA: Compound **não** é Covered Cloud Service (docs).

## CTA

https://ziuluiziul.github.io/groq-round1-offer/ — kit **R$20** (`pix-r20`).
