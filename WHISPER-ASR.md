---
produto: Groq Whisper ASR one-shot
preco_BRL: 20
gerado: qwen/qwen3.6-27b
---

<think>
Here's a thinking process:

1.  **Analyze User Input:**
   - **Language:** PT-BR (Brazilian Portuguese)
   - **Format:** Markdown
   - **Max Lines:** 45
   - **Topic:** "Groq Whisper ASR one-shot" - How to transcribe a WAV file using POST `/openai/v1/audio/transcriptions`
   - **Model:** `whisper-large-v3-turbo`
   - **Plan:** Free Plan
   - **Reference:** Cite only `console.groq.com/docs`
   - **Code:** Include minimal `curl` command
   - **Security:** `GROQ_API_KEY` must be in environment, never hardcoded
   - **Note 1:** Whisper ≠ chat RPM — validate rate-limits on the Free plan page
   - **CTA:** Landing page `https://ziuluiziul.github.io/groq-round1-offer/` PIX R$20 kit

2.  **Deconstruct Requirements:**
   - Title/Heading: # Groq Whisper ASR one-shot
   - Explain the endpoint and model
   - Provide curl command with env var for API key
   - Mention Free Plan & rate limits note
   - Cite docs
   - Add CTA
   - Keep it under 45 lines in PT-BR
   - Format in markdown

3.  **Draft Construction (Mental Refinement - PT-BR):**
   # Groq Whisper ASR one-shot

   Transcreva arquivos `.wav` via API do Groq em uma única requisição. Use o modelo `whisper-large-v3-turbo` no **Free Plan** acessando `console.groq.com/docs`.

   ```bash
   curl -X POST https://api.groq.com/openai/v1/audio/transcriptions \
     -H "Authorization: Bearer $GROQ_API_KEY" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@audio.wav" \
     -F "model=whisper-large-v3-turbo"
   ```

   **⚠️ Nota crítica:** Whisper ≠ chat RPM. Os rate-limits para ASR são desvinculados dos limites de chat. Sempre valide os valores atuais da página *Free Plan* em `console.groq.com/docs/console/free-plan`.

   A variável `GROQ_API_KEY` deve ser exportada no ambiente (`export GROQ_API_KEY="sua_chave"`). Nunca a escreva hardcoded.

   **CTA:** Quer acelerar seu setup? Acesse https://ziuluiziul.github.io/groq-round1-offer/ e garanta o kit PIX R$20.

4.  **Check Constraints:**
   - PT-BR? Yes.
   - Markdown? Yes.
   - Max 45 lines? Let's count:
     1: # Groq Whisper ASR one-shot
     2: (empty)
     3: Transcreva arquivos `.wav`...
     4: (empty)
     5: ```bash
     6: curl ...
     7: ...
     8: ...
     9: ...
     10: ```
     11: (empty)
     12: **⚠️ Nota crítica:**...
     13: (empty)
     14: A variável `GROQ_API_KEY`...
     15: (empty)
     16: **CTA:** ...
     Total: ~16 lines. Well under 45.
   - Topic: Groq Whisper ASR one-shot? Yes.
   - Endpoint: POST /openai/v1/audio/transcriptions? Yes.
   - Model: whisper-large-v3-turbo? Yes.
   - Plan: Free Plan? Yes.
   - Cite only console.groq.com/docs? Yes, referenced exactly as requested.
   - curl mínimo? Yes, standard multipart form.
   - GROQ_API_KEY no env, never hardcoded? Explicitly stated and used as `$
