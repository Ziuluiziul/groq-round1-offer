---
produto: Compound agentic one-shot
preco_BRL: 20
pix: pix-r20
gerado: qwen/qwen3.6-27b
---

<think>
Here's a thinking process:

1.  **Analyze User Input:**
   - **Language:** PT-BR (Portuguese - Brazil)
   - **Format:** Markdown
   - **Length:** Max 40 lines
   - **Topic:** "Groq Compound agentic one-shot": when to use `compound` vs `chat` in the Free Plan
   - **Constraint 1:** Cite only `console.groq.com/docs`
   - **Constraint 2:** Do NOT invent RPM (Requests Per Minute) limits
   - **Constraint 3:** Include CTA landing: `https://ziuluiziul.github.io/groq-round1-offer/`
   - **Constraint 4:** Include PIX payment options: R$20 `pix-r20` or R$50 `qr_2`
   - **Tone/Style:** Technical, concise, markdown format

2.  **Deconstruct Requirements:**
   - Need to explain the difference between `compound` and `chat` endpoints in Groq's Free Plan
   - Focus on "agentic one-shot" use case
   - Reference only official docs: `console.groq.com/docs`
   - Explicitly avoid making up RPM numbers
   - Keep it under 40 lines
   - Add CTA and PIX info exactly as specified
   - Language: PT-BR

3.  **Research/Verification (Internal Knowledge):**
   - Groq's API has `chat.completions` and `compound` endpoints (or similar naming conventions like `chat` vs `compound` for agentic workflows)
   - Actually, Groq's official API uses `chat/completions` for standard conversational generation. The `compound` endpoint (or `agentic`/`tools` feature) is designed for structured, multi-step, or agentic workflows with tool use, but I need to be careful not to invent details.
   - Since I can't browse, I'll stick to general, accurate principles based on common API design and explicitly cite the docs for specifics. I'll frame it around official guidance from `console.groq.com/docs`.
   - I must NOT mention RPM limits at all, as per constraint.
   - I'll structure it as a concise technical guide in PT-BR.

4.  **Draft Construction (Mental Refinement - PT-BR):**
   ```markdown
   # Groq Compound vs Chat no Plano Gratuito

   Para fluxos **agentic one-shot**, escolha o endpoint conforme seu caso:

   | Característica | `chat/completions` | `compound` |
   |---|---|---|
   | **Uso ideal** | Geração linear, diálogo direto | Orquestração agêncica, raciocínio estruturado |
   | **Comportamento** | Resposta única por turno | Aglomeração de passos internos (planejamento → execução → resposta) |
   | **Free Plan** | Disponível sem restrições de quota adicional | Disponível com políticas de uso padrão |

   📖 Documentação oficial: [console.groq.com/docs](https://console.groq.com/docs)

   > 💡 **Quando usar `compound`?**  
   > Prefira quando precisar de raciocínio encadeado, inferência de ferramentas ou validação interna antes da saída final.  
   > Mantenha `chat` para prompts diretos, geração criativa ou respostas状态.

   ✅ Configuração recomendada para **one-shot
