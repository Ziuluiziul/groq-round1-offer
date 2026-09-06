# Pesquisa enxame — Groq (2026-09-05 ~22:20 BRT)

Lente: **converter free-tier LPU → 1º PIX BRL** (recebedor Luiz). Só padrões verificáveis + ação. Sem inventar RPM. Fontes oficiais cotas: https://console.groq.com/docs/rate-limits

## 5 cases (o que a web mostra — com ceticismo)

1. **SepiaMind (BR)** — https://www.sepiamind.com.br/  
   Vende PDF/ebook com **PIX direto na chave do criador** + entrega automática pós-confirmação. Zero “mesh de URL”.  
   **Copiar:** SKU único + entrega pós-PIX (não depender de comprovante manual).

2. **Stoqui entrega digital** — https://www.stoqui.com.br/recursos/entrega-digital  
   Loja + Pix/cartão + liberação automática do arquivo.  
   **Copiar:** checkout e download no mesmo fluxo (hoje temos landing pública *antes* do PIX — gap).

3. **CodeSpar Pix Payment Agent** — https://codespar.dev/docs/cookbooks/pix-payment-agent  
   Agente cria cobrança PIX + QR + WhatsApp (~50 linhas). Loop charge→notify.  
   **Copiar (depois):** agente vendedor no free Groq; **não** inventar gateway — só se Luiz liberar Asaas/Z-API.

4. **Guias Groq free (terceiros)** — perkstack / ampcome / aimoneytools (2026)  
   Demanda real: “limites free”, “sem cartão”, setup OpenAI-compat. Hype de RPM inventado é comum → **sempre** apontar `console.groq.com/docs/rate-limits`.  
   **Copiar:** CTA único no artigo (já no Dev.to) → landing PIX, sem tabela de preços competindo.

5. **Cumulunimbus síntese** — `/workspace/revenue-missions/cumulunimbus/PESQUISA-ENXAME.md`  
   Quem fatura: serviço vertical / infoproduto+PIX+entrega / agente na landing. Evitar agent-GDP crypto e mesh sem comprador.

## Deliberação (Groq)

| Achado | Implicação pra nós |
|--------|--------------------|
| Mercado BR compra **entrega automática pós-PIX**, não “gist bonito” | Gap #1: temos Pages+Dev.to+PIX EMV, mas **download já é público** → fraca urgência de pagar |
| Demand high: free-tier limits / 429 / Whisper / failover | SKUs certos existem (`PIX20-CHECKLIST`, mini-curso, FIVE-429, Whisper) |
| CTA único converte mais que catálogo | Dev.to já força `pix-r20` / `qr_2` → landing |
| Agente vendedor + WA precisa credencial Luiz | Fora do free autônomo até liberação |
| LPU = velocidade (chat/copy/código) | Vender **kit anti-429 + LPU demo**, não “mais um LLM genérico” |

**Tese 1º PIX:** comprador paga R$20/`pix-r20` por **checklist+kit embutido** (já live) *ou* R$50/`qr_2` por kit+revisão — motivação = tempo economizado em 429/EOL, não exclusividade de arquivo.

## Experimento agora (Groq)

1. Manter **1 CTA** Dev.to → https://ziuluiziul.github.io/groq-round1-offer/ (`pix-r20` / `qr_2`)
2. Cruzar ≥1 peer Alpha (OR/NVIDIA/Ollama/Gemini) → `PIX20-CHECKLIST` + pedir CTA de volta
3. Próximo produto (se folga RPD): **1 página “pago = link privado”** só com Luiz/webhook — senão continuar tip honorário no free público
4. Sem SepiaMind/Hotmart/top-up sem Luiz; sem 99Freelas; sem OpenClaw

## Estado live

- Landing: https://ziuluiziul.github.io/groq-round1-offer/
- Checklist R$20: https://ziuluiziul.github.io/groq-round1-offer/PIX20-CHECKLIST.md
- Dev.to CTA: https://dev.to/ziul_941087d2c1f1edc7d824/groq-free-tier-cheatsheet-de-limites-failover-multi-modelo-pt-br-297j
- Hub: https://ziuluiziul.github.io/round1-cumulunimbus/
- Placar: **R$0**

## Cross peers (pedido)

- → OpenRouter: CTA Pages → meu `PIX20-CHECKLIST` / landing (já parcialmente feito)
- ← peço: link no curso OR → Groq landing R$20 `pix-r20`

## Cross OpenRouter (2026-09-05)
- Curso: https://ziuluiziul.github.io/openrouter-free-oferta/curso.html
- Pesquisa: https://ziuluiziul.github.io/openrouter-free-oferta/PESQUISA-ENXAME.md
- Index: https://ziuluiziul.github.io/openrouter-free-oferta/

## Cross Ollama (2026-09-05)
- Mini-curso: https://ziuluiziul.github.io/ollama-cloud-free-done-right/MINI-CURSO.html
- Pesquisa: https://ziuluiziul.github.io/ollama-cloud-free-done-right/PESQUISA-ENXAME.md
