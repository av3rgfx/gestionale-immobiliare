# R5 — Brief: inference engine "DS4" (antirez) e quantizzazione dinamica

*Verificato via web il 13/07/2026.*

## Verifica del nome

**Il progetto esiste davvero.** Il proprietario ha sentito bene, con una sola imprecisione terminologica (vedi sotto).

- **Nome esatto**: `ds4` ("DwarfStar 4"), repo [github.com/antirez/ds4](https://github.com/antirez/ds4), autore Salvatore Sanfilippo (antirez). Descrizione ufficiale: *"DeepSeek 4 Flash and PRO local inference engine for Metal, CUDA and ROCm"*.
- **Rilascio**: 6–7 maggio 2026; scritto in C con dichiarata forte assistenza di GPT-5.5. Post dell'autore: ["A few words on DS4"](https://antirez.com/news/165) (metà maggio 2026). ~18.4k stelle GitHub a oggi.
- **Licenza**: MIT. Pesi quantizzati su [Hugging Face antirez/deepseek-v4-gguf](https://huggingface.co/antirez/deepseek-v4-gguf) (MIT, derivati dal rilascio ufficiale DeepSeek).
- **Release formali**: **nessuna** — la pagina releases di GitHub è vuota, niente tag né versioning.
- **Stato dichiarato dall'autore**: *"beta quality"* perché *"all this exists only for a few days"*; la componente agent è *"alpha quality"*. Non è dichiarato pronto per produzione.

## Cosa fa davvero

DS4 è un motore di inferenza **deliberatamente monomodello**: fa girare **solo DeepSeek V4 Flash** (MoE da ~284 miliardi di parametri, contesto fino a 1M token) e la variante PRO su macchine ≥512 GB. Il README è esplicito: *"intentionally narrow: not a generic GGUF runner"*. **Non può eseguire il modello classe 27B del progetto, né alcun altro modello.**

- **Quantizzazione**: non è "dinamica" in senso tecnico, ma **asimmetrica statica 2/8 bit**: solo gli esperti MoE "routed" sono quantizzati aggressivamente (up/gate a IQ2_XXS, down a Q2_K), mentre router, proiezioni, attention e shared experts restano a Q8_0. Logica: gli esperti sono la maggioranza dei parametri ma ognuno gestisce pochi token, quindi comprimerli costa poco in qualità media. Il file Q2 pesa **80.8 GB** (per Mac da 128 GB); il Q4 **153.3 GB** (≥256 GB RAM).
- **Apple Silicon/Metal**: sì, è il target primario (più CUDA/DGX Spark; ROCm mantenuto dalla community e indietro rispetto al main).
- **API OpenAI-compatible**: sì — `ds4-server` espone `/v1/chat/completions`, `/v1/messages`, `/v1/responses`. Tecnicamente compatibile con l'astrazione provider del gestionale (`base_url` + `model`).
- **Benchmark**: dell'autore, ~26.7 t/s generazione su MacBook M3 Max 128 GB, ~36 t/s su M3 Ultra. Una [recensione indipendente](https://andrew.ooo/posts/ds4-antirez-deepseek-v4-flash-local-inference-review/) conferma i numeri e nota che *"tool calling actually works"* anche a 2 bit, ma elenca limiti netti: lock-in su un solo modello, **soglia hardware minima 96 GB di RAM** (*"no path to 32GB machines"*), stabilità alpha, un bug che *"will hard-crash your machine"* compilando il path CPU su macOS, GGUF con layout proprietario. Verdetto del recensore: **"interesting alpha project, not production-ready"**.

**Incertezza dichiarata**: le recensioni indipendenti disponibili sono poche e recenti; i benchmark "indipendenti" in gran parte riproducono i numeri dell'autore.

## Contesto: come si fanno girare modelli più grandi oggi (stato dell'arte maturo)

La confusione del proprietario è comprensibile: "quantizzazione dinamica" è il nome commerciale delle **[Unsloth Dynamic 2.0 GGUF](https://unsloth.ai/docs/basics/unsloth-dynamic-2.0-ggufs)** — quantizzazione selettiva per-layer (ogni layer riceve una precisione diversa in base alla sensibilità) che DS4 di fatto reimplementa in forma estrema. Punto chiave: **le quant Unsloth Dynamic girano già su llama.cpp e Ollama**, quindi il progetto può beneficiarne **oggi, senza cambiare motore** — basta scaricare la variante Unsloth del modello 27B.

Lo stato dell'arte maturo per RAM limitata:
1. **K-quants e IQ-quants di llama.cpp** (usati da Ollama): standard de facto, anni di maturità.
2. **Unsloth Dynamic 2.0**: quant per-layer migliori a parità di dimensione, compatibili Ollama.
3. **MLX di Apple**: framework Apple per Apple Silicon, ma richiederebbe un server adattatore per l'API OpenAI.
4. **Offloading/mmap**: possibile ma lento su richieste interattive.

**La fisica non si aggira**: un modello deve stare in RAM e la velocità è dominata dalla banda di memoria. Nessun engine "crea" RAM: DS4 fa girare un 284B su 128 GB solo comprimendo a ~2 bit l'80% dei pesi, e comunque **richiede 96–128 GB minimo**. Su un Mac tipico da 32–64 GB, DS4 non fa girare *nulla*. La promessa "engine nuovo → modelli più grandi e più intelligenti" è quindi vera solo in senso stretto: *quel* modello, su *quell'*hardware. Non rende più intelligente il 27B previsto.

## Giudizio di maturità per la produzione

Criteri minimi per sostituire Ollama in un sistema no-ops gestito da non tecnici per anni:

| Criterio | DS4 oggi |
|---|---|
| Release versionate e API stabili | **No** — zero release taggate |
| Storia di manutenzione (≥12–18 mesi) | **No** — ~2 mesi di vita |
| Bus factor / community di manutentori | **Debole** — dipende da una persona (che di mestiere fa Redis) |
| Aggiornamento modelli nel tempo | **No** — un solo modello supportato, per scelta |
| Assenza di bug critici noti | **No** — crash kernel documentato sul path CPU macOS |
| Compatibilità API OpenAI | **Sì** (unico criterio superato) |

**Risposta al proprietario**: DS4 è reale, è un progetto affascinante di antirez, ma (a) è dichiaratamente beta/alpha con due mesi di vita; (b) fa girare *un solo modello* da 284B che richiede un Mac da almeno 96–128 GB di RAM — se il Mac di produzione ne ha meno, la discussione finisce qui; (c) la sua "quantizzazione asimmetrica" è una variante estrema di tecniche già disponibili in Ollama. Per la regola "vince la soluzione più noiosa che funziona": **restare su Ollama**. Se si vuole più qualità a costo zero di rischio, provare le quant Unsloth Dynamic del modello 27B su Ollama. Rivalutare DS4 fra 12+ mesi solo se avrà release stabili, manutenzione continuativa e se l'hardware verrà dimensionato di conseguenza.

## Fonti (URL verificati)

- Repo ufficiale: https://github.com/antirez/ds4 (README, licenza, stato beta/alpha; releases: nessuna)
- Blog antirez: https://antirez.com/news/165 ("A few words on DS4")
- Pesi quantizzati: https://huggingface.co/antirez/deepseek-v4-gguf (Q2 80.8 GB / Q4 153.3 GB, requisiti RAM)
- Recensione indipendente: https://andrew.ooo/posts/ds4-antirez-deepseek-v4-flash-local-inference-review/ (benchmark, 7 limiti, "not production-ready")
- Analisi: https://www.fratepietro.com/2026/dwarfstar-4-local-inference-antirez/ ; https://knightli.com/en/2026/05/11/deepseek-v4-flash-ds4-metal/ ; https://pasqualepillitteri.it/en/news/2253/ds4-antirez-deepseek-v4-flash-inference-engine
- Unsloth Dynamic 2.0: https://unsloth.ai/docs/basics/unsloth-dynamic-2.0-ggufs ; https://unsloth.ai/blog/dynamic-v2
