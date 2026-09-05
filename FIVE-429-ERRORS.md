---
produto: 5 erros 429/TPM Groq Free
preco_BRL: 10
gerado: qwen/qwen3.6-27b
---

<think>
Here's a thinking process:

1.  **Analyze User Input:**
   - **Language:** PT-BR (Brazilian Portuguese)
   - **Format:** Short guide, max 40 lines, Markdown
   - **Title/Topic:** «Groq Free-tier: 5 erros 429/TPM e como evitar»
   - **Content Requirements:**
     - Practical bullets
     - Cite ONLY `console.groq.com/docs/rate-limits` and `/deprecations`
     - Do NOT invent RPM (Requests Per Minute) numbers
     - Do NOT include API keys
     - End with CTA: landing `https://ziuluiziul.github.io/groq-round1-offer/` + PIX R$10 tip
   - **Constraints:** Max 40 lines total, strict formatting.

2.  **Deconstruct Requirements:**
   - Title: `# Groq Free-tier: 5 erros 429/TPM e como evitar`
   - 5 practical bullet points addressing 429 errors / TPM limits
   - Only cite the two specific URLs
   - No RPM values, no keys
   - CTA at the end with exact URL and PIX mention
   - Keep it under 40 lines
   - Language: PT-BR

3.  **Draft - Mental Refinement (PT-BR):**
   # Groq Free-tier: 5 erros 429/TPM e como evitar

   O limite de tokens por minuto (TPM) no tier gratuito é rígido. Acumulá-los gera `429 Too Many Requests`. Veja como blindar seu fluxo:

   - **Espere o cabeçalho `x-ratelimit-reset`:** Nunca tente novamente imediatamente. Leia o timestamp de retorno e aplique um `sleep` dinâmico antes da próxima chamada.
   - **Chunk its requests:** Divida prompts longos em lotes menores. Processar tudo de uma vez esgota o TPM rapidamente; batch controlável evita picos.
   - **Cache de respostas idênticas:** Implemente um-cache (Redis/local) para queries repetitivas. Menos chamadas = menos tokens consumidos = menos 429.
   - **Monitore `x-ratelimit-remaining`:** Antes de enviar, verifique o saldo restante. Se estiver abaixo de 10%, reduza a frequência ou pause a fila.
   - **Verifique modelos depreciados:** Alguns endpoints antigos foram removidos ou limitados. Acessar `/deprecations` evita chamadas a rotas que já não honram o tier gratuito.

   Regras oficiais: `console.groq.com/docs/rate-limits`

   👉 Aprenda a skalizar sem quebrar seu código: https://ziuluiziul.github.io/groq-round1-offer/
   ☕ Apoie este guia com PIX R$10: [chavereferenciais] (substitua por sua chave)

   Wait, I need to check constraints:
   - Max 40 lines? Yes, currently ~18 lines.
   - Only cite those two URLs? I cited `console.groq.com/docs/rate-limits` and mentioned `/deprecations` in the text. I should format them as links or just raw as requested. The prompt says "cita só console.groq.com/docs/rate-limits e /deprecations". I'll cite them exactly as requested.
   - No invented RPM? Checked.
   - No key? I said "substitua por sua chave" but the prompt says "Sem chave." I should remove any mention of a key placeholder. I'll just say "PIX R$10: [sua chave]" or better, just "PIX R$10: (insira sua chave)" but the prompt says "Sem chave." I'll literally just write "PIX R$10:" and leave it, or say "PIX R$10: (chave no link)". Actually, I'll just write "PIX R$10: (informada na landing)" to strictly avoid putting any key-like string. Or just "PIX R$10: [chave
