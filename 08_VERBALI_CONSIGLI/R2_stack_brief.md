# BRIEF RICERCA R2 — Stack tecnico e compliance (fatti verificati con fonti)

## 1. LLM locale su Mac Mini M4
- **Runtime**: Ollama (daemon, API OpenAI-compatible nativa con supporto tools: https://ollama.com/blog/openai-compatibility — caveat: `tool_choice` non supportato), LM Studio (MLX nativo, GUI), MLX diretto. Tutti e tre espongono API OpenAI-compatible → astrazione provider gratuita.
- **Hardware**: Mac Mini M4 base 16GB, configurabile 24/32GB (https://support.apple.com/it-it/121555). **24GB = sweet spot** per modelli 27B Q4 (~17GB) + OS. Su M4 24GB: ~20–40 tok/s su 27B Q4 (stima).
- **Modelli (da riverificare al momento dell'acquisto — NOTA: un consigliere ha segnalato che "Gemma 4 26B-A4B" potrebbe non corrispondere a release note pubbliche; verificare nome esatto, pesi e benchmark prima di decidere)**:
  - Prima scelta ricerca: Gemma 4 (26B-A4B MoE o 31B dense) Q4 — miglior italiano della classe (fonte blog Google: punto di forza lingue europee), tool-calling nativo, vision, Apache 2.0.
  - Alternativa pari merito: Qwen3.6-27B Q4_K_M (~17GB, context lungo, Apache 2.0).
  - Sconsigliati: gpt-oss-20b (multilingua debole, studio arXiv 2508.12461), GLM-4.7-Flash (tool-call GGUF instabile), GLM-4.6-Air (pesi NON open, solo API).

## 2. OCR
- **GLM-OCR** (zai-org, 0.9B, 94.62 OmniDocBench, MIT, in Ollama ~2.2GB): esiste e gira su Mac M4, MA è bilingue ZH/EN — **italiano NON tra le lingue supportate ufficialmente** → BLOCCANTE per documenti italiani. Fonti: https://github.com/zai-org/GLM-OCR, https://www.buildwithmatija.com/blog/run-glm-ocr-macbook-ollama
- **PaddleOCR-VL** (0.9B): 80+ lingue incl. italiano, supporto llama.cpp/Apple Silicon (mar 2026), server MCP ufficiale, Apache 2.0. → candidato unico per il fallback OCR.
- **Surya 2**: italiano 93% benchmark interno; licenza pesi OpenRAIL-M (da far verificare al legale).
- **MRZ ICAO 9303**: parser dedicato per CIE/passaporti (checksum deterministico).
- **APE PDF nativi**: estrazione testo diretta (pdfplumber/PyMuPDF), nessun OCR.

## 3. Stack webapp
- Backend: **FastAPI** (Python). DB: **SQLite WAL** (file unico → backup semplice; regge 2–5 utenti LAN). Template: **docxtpl** (Jinja2 in Word: https://docxtpl.readthedocs.io/). Conversione/anteprima: **LibreOffice headless** (`soffice --headless --convert-to pdf`) + **PDF.js**. Font: installare Liberation (metricamente compatibili con Calibri/Cambria) per fedeltà. Dati in un'unica cartella `~/Gestionale/{db.sqlite, documenti/, templates/}` → Time Machine + backup.
- **ATTENZIONE backup (dal Consiglio C1)**: copiare la cartella con SQLite WAL live produce backup corrotti (-wal/-shm incoerenti). Serve `sqlite3 .backup` schedulato + copia offsite cifrata + test di ripristino mensile + alert.

## 4. Compliance immobiliare Italia (verificato)
- **Registrazione contratti locazione entro 30 giorni** dalla stipula/decorrenza, AdE canale RLI (https://www.agenziaentrate.gov.it).
- **Antiriciclaggio** (D.Lgs 231/2007): per gli agenti immobiliari l'adeguata verifica scatta **al conferimento dell'incarico, indipendentemente dall'importo**; conservazione documentale 10 anni; segnalazione operazioni sospette a UIF. **I 5.000€ sono il LIMITE ALL'USO DEL CONTANTE** (art. 49, come modificato da L. 197/2022), non la soglia AML. La soglia interna di 1.000€ è policy volontaria più stringente (lecita, etichettarla "policy interna"). Validare interpretazione soglie con il consulente AML dell'agenzia.
- **Art. 7 D.Lgs 286/1998**: comunicazione cessione fabbricato/ospitalità alla Questura **entro 48h** per cittadini **extracomunitari**. **Art. 12 DL 59/1978**: cessione fabbricati (48h), assorbito dalla registrazione AdE per contratti registrati. **TULPS art. 109**: comunicazione alloggiati per locazioni turistiche (24h, Alloggiati Web) — vale per **tutti gli ospiti**.
- **Deposito modelli/formulari: presso la CAMERA DI COMMERCIO** (art. 5 L. 39/89 + d.m. 452/1990, pratica REA "Sezione Formulari"), NON all'AdE. Sanzioni per mancato deposito (~€1.549) e uso di modello diverso dal depositato (~€516). Il deposito va rinnovato a ogni modifica dei modelli.
- **Locazioni 3+2 (l. 431/98)**: dal Consiglio C4 — il preavviso di 6 mesi opera alla **scadenza del triennio** (per impedire la proroga tacita del +2); alla **scadenza del biennio** il contratto cessa automaticamente e serve **nuova stipula**. DA VALIDARE con consulente legale prima della messa in produzione del modulo scadenze.

## 5. Canali notifica
- **Email SMTP**: pienamente fattibile (Brevo free 300/giorno; Gmail 500/giorno; Workspace 2.000/giorno). Serve SPF/DKIM/DMARC.
- **WhatsApp**: API ufficiale = burocrazia + costi per messaggio + fee BSP ($50–500/mese); non ufficiali = **rischio ban elevato** sul numero aziendale → MAI in produzione. SMS: ~€0,04–0,07/msg + registrazione mittente AGCOM.
- Decisione consiglio C4: email come unico canale v1.

## 6. Dev/test cloud→locale
- SDK OpenAI con `base_url` e `model` configurabili (Ollama espone `/v1`). Opzionale LiteLLM (MIT) per budget/log — ⚠️ incidente sicurezza riportato mar 2026, verificare advisory.
- MacBook Pro 2019 i5/16GB: niente MLX (Intel), modelli locali solo piccoli/lenti → sviluppo contro API cloud, **eval suite identica rieseguita sul modello locale dal secondo sprint**. MAI dati clienti reali verso API cloud: solo dati sintetici/anonimizzati.
- Human-in-the-loop obbligatorio per azioni di scrittura (DB, email, documenti ufficiali) + audit log.
