---
produto: GPT-OSS Safeguard BYO-policy Free
preco_BRL: 20
fontes: console.groq.com/docs/content-moderation, /docs/model/openai/gpt-oss-safeguard-20b, /docs/rate-limits, /docs/models
gerado_com: docs oficiais + openai/gpt-oss-safeguard-20b smoke
---

# Groq Free-tier: content moderation com `openai/gpt-oss-safeguard-20b`

Objetivo: classificar prompts com **sua política** (bring-your-own-policy), não taxonomia fixa. Docs: [content-moderation](https://console.groq.com/docs/content-moderation).

## Por que este modelo

- Policy-following (Trust & Safety customizável)
- Substitui o EOL `meta-llama/llama-guard-4-12b` → ver [deprecations](https://console.groq.com/docs/deprecations)
- Complementa Prompt Guard 2 (`meta-llama/llama-prompt-guard-2-*`) que é pré-assado só para injection

## Free Plan (tabela oficial)

Confirme sempre em [rate-limits](https://console.groq.com/docs/rate-limits):

| ID | RPM | RPD | TPM | TPD |
|----|-----|-----|-----|-----|
| `openai/gpt-oss-safeguard-20b` | 30 | 1K | 8K | 200K |

Pare a API se **≥80% RPD** ou TPM crítico. Sem top-up.

## Padrão

1. System = política completa (DEFINITIONS / VIOLATES / SAFE / EXAMPLES)
2. User = conteúdo a classificar
3. Peça JSON: `violation`, `category`, `rationale`

Script: `safeguard_mod.py` (key só `GROQ_API_KEY`).

## CTA

https://ziuluiziul.github.io/groq-round1-offer/ — kit **R$20** (`pix-r20`) / **R$50** (`qr_2`).
