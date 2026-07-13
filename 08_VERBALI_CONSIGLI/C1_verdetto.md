# VERDETTO C1 — Architettura e stack tecnico (Chairman)

## Dove il consiglio concorda
- **Stack (a) convalidato.** FastAPI + SQLite (WAL) + docxtpl + LibreOffice headless è tecnologia matura e "noiosa": il First Principles Thinker lo convalida *perché* è noioso, l'Executor conferma "tutta roba matura, pip e brew".
- **Il cuore deve essere deterministico.** I documenti legali escono da template versionati riempiti da codice; l'LLM è solo "bocca e orecchie" (capisce l'intento in italiano), mai autore di testo legale (First Principles Thinker; ribadito da 3 review su 5).
- **Auto-skill come codice Python auto-generato = eresia.** 4 advisor su 5; il Contrarian dà la prova tecnica: prompt injection → esecuzione arbitraria sul server che contiene i dati dei clienti.
- **Sequenza: prima il gestionale senza AI.** CRUD + template + PDF è già "il 70% del valore" (Executor); JARVIS arriva dopo, prima in sola lettura.
- **(d) e (e) corrette ma insufficienti**: Mac Mini sempre acceso va bene come assunzione, non come piano di affidabilità; l'human-in-the-loop con utenti non tecnici rischia il rubber-stamping (Contrarian) / "teatro dell'approvazione" (Outsider).

## Dove il consiglio è diviso
- **Skill in Markdown**: l'Expansionist la chiama "moat" (JARVIS propone un .md, l'umano approva una volta, resta permanente); il Contrarian la considera deriva incontrollata. L'Executor accetta l'ibrido. Prevalgono Contrarian + Executor: MD proposto da JARVIS ma attivabile **solo** con approvazione umana e versioning Git; nessuna skill auto-attiva.
- **Visione prodotto**: l'Expansionist vuole installer, benchmark pubblicabile, scansione archivio via vision. Tutte e 5 le review lo indicano come punto cieco pericoloso: si ottimizza il go-to-market prima dell'affidabilità che ha già ucciso il progetto una volta.
- **Strategia (c)**: approvata da tutti, ma con due trappole diverse — modello forse inesistente (Contrarian) e dati reali inviati alle API cloud in fase di test (Outsider).

## Punti ciechi emersi
1. **Backup (difetto fatale, Contrarian)**: copiare la cartella con SQLite in WAL live produce backup corrotti (file -wal/-shm incoerenti); Time Machine è nello stesso edificio. Servono `sqlite3 .backup` schedulato + copia offsite cifrata + test di ripristino mensile. "Un backup mai ripristinato non è un backup."
2. **Verifica esistenza modello**: "Gemma 4 26B-A4B" non corrisponde a release note (esiste Gemma 3 27B). Verificare nome, pesi e benchmark prima di progettarci sopra.
3. **Identità, ruoli, audit log** (mancato a tutti, segnalato dalle review): login, permessi agente/segretaria, registro immutabile di chi ha approvato cosa, quando, con quale versione di template e modello. Obbligo GDPR e unica difesa dal rubber-stamping.
4. **Validazione legale dei template** da un professionista e un responsabile del loro aggiornamento normativo.
5. **Privacy in dev**: mai casi reali verso Gemini/Anthropic/OpenAI — solo dati sintetici/anonimizzati.
6. **Bus factor e monitoraggio**: alert su backup fallito e disco pieno; documentazione in italiano semplice per chi erediterà il sistema.

## La raccomandazione
**(a)** Stack approvato così com'è. **(b)** Gemma/Qwen 27B Q4 su Ollama va bene, ma solo dopo verifica di esistenza e benchmark; JARVIS legge il DB liberamente, scrive solo tramite funzioni deterministiche che validano ogni campo prima del template; auto-skill = libreria curata + proposte MD approvate da un umano, mai codice generato. **(c)** Dev cloud→locale approvato con due correzioni: eval suite rieseguita sul modello locale dal secondo sprint, non alla fine (Executor), e dataset di test anonimizzato. **(d)** Mac Mini sempre acceso + backup `sqlite3 .backup` su cron + copia offsite cifrata + restore test mensile + alert: l'hardware è single point of failure, la procedura non può esserlo. **(e)** HITL sì, ma con sostanza: audit log, diff leggibile dei dati chiave prima dell'approvazione (non un semplice "Approva"), conferma esplicita per email e documenti ufficiali.

Mi schiero con First Principles Thinker + Contrarian contro l'Expansionist: la logica legale nel template e il backup verificabile valgono più di qualsiasi moat. Dell'Expansionist tengo solo due punti da calendario, non da roadmap: documentare l'installazione e usare la vision per digitalizzare l'archivio cartaceo — dopo che la base regge.

## La prima cosa da fare
Lunedì, in quest'ordine (Executor): **1)** cron di backup `sqlite3 .backup` + copia offsite attivo *prima* di inserire dati veri; **2)** scaffold FastAPI+SQLite con CRUD anagrafiche/pratiche e audit log, senza AI; **3)** un template docxtpl reale (incarico) → DOCX → PDF via LibreOffice, per uccidere subito il rischio font/layout. Solo dopo: JARVIS in lettura sul DB.
