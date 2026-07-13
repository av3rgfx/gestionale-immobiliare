# 04 — Architettura tecnica

**Progetto:** Gestionale Immobiliare + JARVIS — webapp locale per piccola agenzia immobiliare italiana con agente AI locale.
**Ambiente di produzione:** Mac Mini M4, rete LAN dell'agenzia (2-5 utenti).
**Ambiente di sviluppo:** sessioni nella sezione **Code** di Claude Desktop (ADR-47), repo GitHub, codice verso API cloud (dati sintetici) e poi modello locale.
**Uso di questo documento:** riferimento citato dai prompt di sprint. Ogni sprint deve dichiarare a quali sezioni si attiene; le decisioni normative sono in `03_DECISIONI_CONSIGLIO.md` (ADR-01…ADR-63).

---

## 1. Visione e principi non negoziabili

Il sistema è il **registro operativo** di una piccola agenzia immobiliare: anagrafiche, immobili, pratiche, documenti legali, scadenze, movimenti economici e adempimenti. JARVIS, l'agente AI locale, è un assistente che **capisce l'italiano e propone**, ma il sistema decide e scrive solo attraverso codice deterministico.

Principi non negoziabili (violare uno di questi = blocco dello sprint):

1. **Deterministico prima dell'AI.** Documenti legali, calcoli, scadenze e adempimenti escono da template versionati e da codice. L'LLM non è mai autore di testo legale né di logica di calcolo (ADR-02).
2. **Tutto locale.** In produzione nessun dato lascia il Mac Mini: LLM via Ollama, OCR locale, nessuna API cloud. In sviluppo, le API cloud vedono **solo dati sintetici o anonimizzati** (ADR-01, ADR-05). **Deroghe dichiarate** (le uniche): (1) l'invio delle email di notifica via **SMTP** (§6), circoscritta ai dati minimi del messaggio, con DPA col provider e copertura nell'informativa — prima di S4 (verbale C7); (2) l'**accesso remoto via Tailscale** (§10, ADR-56): il control-plane tratta metadati (nodi, topologia, chiavi, relay DERP), **mai i dati** che restano sul Mac cifrati end-to-end — con DPA e registro dei trattamenti aggiornato (verbale C9).
3. **A prova di stupido.** L'utente tipo è una segretaria non tecnica: messaggi di errore in italiano semplice, azioni guidate, nessuna configurazione manuale di file.
4. **Backup verificabile.** Un backup mai ripristinato non è un backup: snapshot schedulato + copia offsite cifrata + restore test mensile + alert (ADR-06).
5. **Human-in-the-loop con audit.** Ogni scrittura rilevante passa da un umano che vede un **diff leggibile**, conferma esplicitamente, e lascia traccia immutabile: chi, cosa, quando, con quale versione di template e di modello (ADR-07, ADR-08).
6. **Il registro operativo non è il registro tributario.** Niente contabilità fiscale: la cerniera col commercialista è un export CSV categorizzato (ADR-39).

---

## 2. Componenti e stack

Stack unico, tecnologie mature ("noiose") e installabili via `pip`/`brew` (ADR-01):

| Componente | Tecnologia | Ruolo |
|---|---|---|
| Backend | **FastAPI** (Python) | API REST, logica applicativa, job schedulati |
| Database | **SQLite in modalità WAL** | File unico, regge 2-5 utenti LAN; backup via `sqlite3 .backup` |
| Template documenti | **docxtpl** (Jinja2 dentro DOCX) | Riempimento deterministico dei modelli |
| Conversione | **LibreOffice headless** (`soffice --headless --convert-to pdf`) | DOCX → PDF identico alla stampa |
| Font | **Liberation** (metricamente compatibili con Calibri/Cambria) | Fedeltà tipografica anteprima/stampa (ADR-16) |
| Anteprima | **PDF.js** | Visualizzazione del PDF archiviato nel browser |
| LLM | **Ollama** (API OpenAI-compatible, `/v1`) | Runtime locale per JARVIS; in dev API cloud configurabili |
| OCR (residuo) | **PaddleOCR-VL** | Solo per CI senza MRZ e foto; italiano, Apache 2.0, Apple Silicon (ADR-32) |
| Estrazione testo | **PyMuPDF / pdfplumber** | APE in PDF nativi, senza OCR |
| MRZ | Parser **ICAO 9303** con checksum | CIE/passaporti, gate bloccante |
| Email | **SMTP** (provider a scelta: es. Brevo/Gmail/Workspace) | Canale unico notifiche v1 con SPF/DKIM/DMARC |
| Frontend mobile | **PWA responsive** (stessa app FastAPI server-rendered + manifest) | Uso dal telefono del Proprietario; niente app nativa (ADR-55) |
| Accesso remoto | **Tailscale** (WireGuard mesh) + `tailscale cert`/`serve` per HTTPS tailnet-only | Raggiungere il Mac da fuori senza esporlo a Internet (ADR-56/57) |
| STT (voce, Fase 3) | **whisper.cpp** large-v3-turbo (Core ML/ANE) | Ascolto locale della modalità Chiamata (ADR-61) |
| TTS (voce, Fase 3) | `say`/AVSpeech → **Piper** it_IT-paola → **Kokoro-82M** (scelta con demo audio) | Voce italiana locale; XTTS vietato (ADR-61) |
| Orchestrazione voce (Fase 3) | **Glue custom** in FastAPI (WebSocket), processi voce **on-demand** | Nessun framework né secondo servizio sempre acceso (ADR-61) |

**Cartella dati unica** — tutto ciò che conta vive in un solo posto:

```
~/Gestionale/
├── db.sqlite            # database (WAL)
├── templates/           # versioni template DOCX + metadati deposito
├── documenti/           # artefatti PDF, scansioni consensi, allegati
├── backup/              # snapshot sqlite3 .backup (prima della copia offsite)
└── logs/                # audit log + log applicativi
```

La cartella è il perimetro del backup e della cifratura. **Mai** copiarla a caldo con il DB aperto: i file `-wal`/`-shm` sarebbero incoerenti (ADR-06).

Diagramma dei componenti:

```
┌─────────────────────────────────────────────────────────────┐
│ Browser (segretaria/agente/proprietario)                     │
│   UI FastAPI + PDF.js (anteprima)                            │
└───────────────┬─────────────────────────────────────────────┘
                │ HTTP (LAN)
┌───────────────▼─────────────────────────────────────────────┐
│ FastAPI (unico processo applicativo)                         │
│  ├─ CRUD anagrafiche/immobili/pratiche/contratti             │
│  ├─ Motore template (docxtpl) ──► LibreOffice ──► PDF        │
│  ├─ Pipeline OCR/adempimenti (MRZ, APE, PaddleOCR-VL)        │
│  ├─ Scheduler (launchd): scadenze, reminder, backup, DMS     │
│  ├─ Audit log (immutabile)                                   │
│  └─ JARVIS gateway ──► Ollama /v1 (locale) o API cloud (dev) │
└───────────────┬─────────────────────────────────────────────┘
                │
┌───────────────▼─────────────────────────────────────────────┐
│ ~/Gestionale/  (db.sqlite WAL, templates/, documenti/)       │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Modello dati

Elenco delle entità con i campi chiave. Convenzioni trasversali: ogni tabella ha `id`, `created_at`, `updated_at`; le tabelle marcate *(immutabile)* non ammettono UPDATE/DELETE applicativi (solo INSERT), in conformità ad ADR-08/ADR-20.

### 3.1 Soggetto
Persona fisica o giuridica coinvolta in una pratica (cliente, controparte, ospite).

- Dati anagrafici: tipo (persona fisica/giuridica), nome/cognome o denominazione, codice fiscale / partita IVA, data e luogo di nascita, residenza/sede, recapiti (telefono, email, PEC).
- **Nazionalità** e **categoria UE/extra-UE**: campo **calcolato dalla nazionalità** (non inserito a mano). Se la nazionalità manca, i flussi che dipendono dalla categoria **bloccano e chiedono** — mai skip silenzioso (ADR-36).
- **Stato consenso privacy**: derivato dai RecordConsenso associati: `valido` / `scaduto` (informativa cambiata → ri-firma imposta) / `mancante` (ADR-20).
- Documenti d'identità collegati (riferimento a scansione + dati estratti verificati).

### 3.2 Immobile
- Dati catastali e indirizzo, tipologia, metratura, stato (disponibile/in trattativa/locato/venduto/ritirato).
- **Sezione APE** *(gruppo di campi; rinominata da "Blocco APE" per evitare l'omonimia con la regola di blocco — verbale C7)*: classe energetica (dominio A4–G), **EPgl,nren** (numerico plausibile), **data scadenza APE**, **path file** dell'attestato, **stato verifica autenticità** (`verificato_registro` / `da_verificare` / `non_verificabile`), layout riconosciuto in whitelist o in coda revisione (ADR-37); **esenzione APE** registrabile con motivo (es. box, ruderi, categorie esenti).

### 3.3 Pratica
Contenitore operativo di una trattativa.
- Tipo pratica (vendita, locazione abitativa, locazione turistica, ecc.), stato, agente responsabile, soggetti coinvolti (ruolo per soggetto), immobili collegati.
- Flag condizionali per i moduli (es. `prevede_mutuo` → include modulo mutuo nel pacchetto — ADR-22).
- Data firma contratto (evento che genera i Movimenti — ADR-40).
- **Presidio APE**: la pratica è creabile anche senza APE, ma APE mancante/scaduta genera un **Task bloccante ben visibile** sulla pratica e **blocca la generazione dei documenti che la richiedono** (applicazione di ADR-21); l'esenzione registrata con motivo disattiva il presidio (verbale C7).

### 3.4 ContrattoLocazione
- Tipo contratto (3+2 canone concordato, transitorio, turistico…), canone, deposito, date di stipula e decorrenza.
- **Date triennio e biennio calcolate dalla proroga effettiva**, non dall'inizio contratto (ADR-25).
- **Disdetta inquilino** (data, ricevuta il) e **disdetta proprietario** (data, canale raccomandata/PEC): campi dedicati (ADR-25, ADR-26).
- Stato scenari: `attivo` / `chiusura-cessazione` / `rinnovo` (tacito o nuova stipula) / `in_trattativa` (con data di rientro) — ADR-28.
- Data **registrazione nel sistema** (T+0 dello scadenziario RLI — ADR-43) e stato registrazione AdE.

### 3.5 Template
Modello DOCX depositabile.
- Nome, categoria per la segretaria (Contratti / Moduli di pratica / Autonomi), versione, **hash SHA-256** del file.
- **Stato**: `bozza` / `depositata` / `ritirata`; **lock**: le versioni depositate sono in modifica bloccata — ogni cambio crea una nuova versione (ADR-18).
- Metadati deposito Camera di Commercio: data deposito, riferimento pratica REA, promemoria ri-deposito a ogni modifica (ADR-44).
- Esito dry-run (font mancanti, segnaposti irrisolti) e approvazione (chi, quando).

### 3.6 IstanzaDocumento
Documento generato per una pratica.
- Riferimento a **template_version_id** (la versione esatta usata — le pratiche restano legate alla versione con cui sono nate, ADR-18).
- **Dati snapshot**: copia congelata dei dati canonici al momento della generazione.
- **Artefatto PDF**: path del file archiviato alla creazione (= ciò che l'anteprima mostra, ADR-15); mai ri-convertito a vista.
- Stato: `generato` / `stampato` / `firmato` / `archiviato`; rigenerazioni successive = nuove istanze (ADR-14).

### 3.7 RecordConsenso *(immutabile)*
Scansione del modulo privacy firmato (ADR-20).
- Soggetto, **versione del modulo informativa**, data, **hash** del file, timestamp, stato (`valido` / `scaduto`), path scansione.
- Al cambio dell'informativa: marcatura massiva `scaduto` e blocco operativo fino alla ri-firma.

### 3.8 Movimento
Riga economica **auto-generata** alla firma del contratto (ADR-40, ADR-41).
- Pratica, **tipo** (provvigione, canone di gestione…), importo, data scadenza, agente.
- **Stato**: `previsto` / `fatturato` / `incassato`; acconti, storni e note di credito come stati/eventi della stessa riga (mai righe inserite a mano).
- Origine: riferimento all'evento che l'ha generato.

### 3.9 Scadenza
- Tipo **trigger 1** (fine triennio −7 mesi: scadenza legale) o **trigger 2** (fine biennio −6 mesi: nuova stipula commerciale) — ADR-24.
- Data scadenza calcolata, stato (`da_notificare` / `notificata` / `risposta_ricevuta` / `chiusa`), scenario instradato (A/B/C).
- **Reminder inviati**: contatore e date (+7/+14/+30), task operatore generato a scadenza −6 mesi (ADR-29).

### 3.10 Utente + Ruolo
- Utente: nome, credenziali, stato attivo.
- **Ruolo** con permessi: **Admin** (configurazione), **Agente** (pratiche proprie), **Segretaria** (operatività documentale), **Proprietario** (dashboard incassi in sola lettura + **margine per agente visibile solo a lui**) — ADR-42.
- I permessi sui margini sono granulari: nessun altro ruolo li vede.

### 3.11 AuditLog *(immutabile)*
- Chi (utente), cosa (entità + azione + diff dei campi chiave), quando, da quale sessione.
- **Versione del template** e **versione del modello LLM** coinvolti nell'azione (quando rilevante) — ADR-08.
- Include: approvazioni HITL, conferme invio email, correzioni OCR (metrica accuracy — ADR-34), consultazioni di etichette compliance (ADR-45), consultazioni/download delle scansioni di consensi e documenti (verbale C7), consultazioni della chat JARVIS ed esecuzioni delle automazioni (ADR-50, ADR-53).

### 3.12 Task
Compito operativo generato dal sistema, sempre visibile finché non chiuso (verbale C7).
- Tipo, riferimento (entità + id), assegnatario (utente o ruolo), data scadenza, stato (`aperto` / `completato`), esito/nota.
- Usato da: scadenze locazioni (ADR-29), adeguata verifica AML all'apertura pratica (ADR-44), riconciliazione mensile (ADR-46), verifica autenticità APE (ADR-37), presidio APE (§3.3), test di ripristino backup (ADR-06), proposte di JARVIS in coda «Da approvare» e azioni delle automazioni (ADR-50, ADR-53 — Fase 2).

### 3.13 Ricordo *(Fase 2 — S9)*
Memoria personale del Proprietario, «Cose da ricordare» (ADR-51).
- Testo dettato e confermato, categoria, **soggetto collegato** (se nomina un terzo — esercitabilità artt. 15-17 GDPR), `valid_from`/`superseded_by` per le correzioni.
- Indici: FTS5 + embedding (sqlite-vec a versione bloccata, modello `bge-m3` via Ollama).
- «Dimentica» = cancellazione fisica del testo; in AuditLog resta solo l'evento.

### 3.14 Automazione *(Fase 2 — S9)*
Regola dichiarativa del Proprietario (ADR-53).
- **Trigger / condizioni / azione con parametri, tutti da enum chiusi**; presentata come frase «QUANDO… SE… ALLORA…».
- Stato (`disattivata` / `attiva` / `in_pausa` / `autosospesa`), limite giornaliero anti-tempesta, contatori e data ultima esecuzione.
- Origine: creata da JARVIS su richiesta o «di sistema» (RLI ADR-43, scadenze ADR-24, esposte nella stessa UI, mai duplicate).

---

## 4. Architettura agente JARVIS

JARVIS è un assistente in linguaggio naturale dentro al gestionale. Principio guida: **bocca e orecchie, mai mani** (ADR-02). Capisce l'italiano, interroga i dati, propone; scrive solo attraverso funzioni deterministiche e con conferma umana.

**Accesso (ADR-50):** la chat JARVIS è riservata al **ruolo Proprietario** (permesso di ruolo, mai hardcoded sull'utente). La coda **«Da approvare»** è una schermata separata, visibile per ruolo: ogni proposta di JARVIS diventa un **Task** (§3.12) assegnato all'**unico approvatore competente per tipo di azione** (operatività documentale → Segretaria; email a clienti, dati economici, margini → Proprietario) — mai doppia firma in serie. Le consultazioni della chat (domande, tool invocati, versione modello) finiscono in AuditLog.

### 4.1 Astrazione provider
Un unico client LLM con due soli parametri configurabili: **`base_url`** e **`model`**.

- **Produzione**: `base_url` → Ollama locale (`/v1`, API OpenAI-compatible). Modello 27B-classe Q4 su Mac Mini M4 24GB (sweet spot: ~17GB modello + OS).
- **Sviluppo**: `base_url` → API cloud (OpenAI-compatible). **Mai dati clienti reali**: solo sintetici/anonimizzati (ADR-05).
- La stessa **eval suite italiana** gira identica su cloud e su locale. Prima esecuzione sul modello locale = **criterio di done di S6**, ripetuta in S7 e S8 (ADR-48); il **Mac Mini M4 con Ollama deve essere disponibile prima dell'inizio di S6**. Se l'eval locale fallisce, S7 non parte: si cambia modello, non architettura.
- ⚠️ **Verifica esterna obbligatoria**: nome, pesi e benchmark del modello scelto ("Gemma 4 26B-A4B" non corrisponde a release note pubbliche; alternativa Qwen 27B Q4). Decisione di modello subordinata a questa verifica.
- Nota tecnica: l'API OpenAI-compatible di Ollama supporta i tools ma **non** `tool_choice` — il gateway JARVIS deve gestirlo (niente dipendenze da quel parametro).

### 4.2 Tool read-only in v1
Prima versione: JARVIS **legge** il DB liberamente (anagrafiche, pratiche, scadenze, movimenti nei limiti del ruolo dell'utente che interroga) e risponde con proposte. Nessuna scrittura diretta.

### 4.3 Scritture: solo via funzioni deterministiche + HITL
Quando serve scrivere (creare una pratica, generare un documento, inviare un'email):

```
JARVIS propone → funzione deterministica valida OGNI campo
             → diff leggibile dei dati chiave all'utente
             → conferma esplicita umana
             → esecuzione + riga in AuditLog (con versione modello)
```

- La validazione avviene **prima** del template/DB: campi mancanti o invalidi → rifiuto con elenco in italiano semplice (ADR-21).
- Conferma esplicita obbligatoria per email e documenti ufficiali (ADR-07, ADR-30).
- Niente "Approva" cieco: il diff mostra cosa cambierà davvero.

### 4.4 Libreria skill curata (auto-skill)
- Le "skill" sono **documenti Markdown curati** (procedure operative in italiano: es. "come preparare il pacchetto pratica per una locazione turistica"). **In UI si chiamano «Procedure»** — la parola "skill" non compare mai; le versioni Git si mostrano come «versione 3, approvata il…» (ADR-52).
- JARVIS può **proporre** una nuova Procedura in MD **solo su richiesta esplicita del Proprietario** (v1); l'attivazione richiede l'approvazione del **solo Proprietario** e il file è versionato in **Git** (ADR-04, ADR-52).
- **MAI** codice auto-generato eseguito: nessuna Procedura può contenere né invocare codice prodotto dall'LLM. Le Procedure guidano il comportamento, non estendono il programma.
- Una Procedura **non può allentare l'HITL** (a rifiutarla è il validatore, non l'LLM) e il suo testo **non può derivare da contenuti esterni** (email, documenti — regola anti-avvelenamento, ADR-52).

### 4.5 Eval suite italiana
- Dataset di test in italiano (intenti tipici dell'agenzia) costruito su **dati sintetici/anonimizzati**.
- Eseguita a ogni cambio di modello/prompt e, **da S6** (ADR-48), anche sul modello locale: la metrica di accettazione deve reggere in produzione, non solo in dev.

### 4.6 Memoria personale «Cose da ricordare» (ADR-51 — Fase 2, S9)
- Entità Ricordo (§3.13) dentro la SQLite esistente: **nessun servizio nuovo** (Graphiti/Neo4j, mem0, GraphRAG scartati — brief R3); backup e cifratura sono quelli già in essere.
- Nascita di un ricordo: **solo dettatura diretta del Proprietario + conferma esplicita** («Vuoi che ricordi: *X*?»); **mai estrazione automatica da email o documenti** (regola anti-avvelenamento).
- Recupero: ricerca ibrida (FTS5 per parole chiave + KNN semantico) iniettata nel contesto della chat; per una persona sola la scansione esaustiva è questione di millisecondi.
- UI: «Ricorda questo», «Dimentica» (cancellazione fisica), «Correggi» (nuova versione, la vecchia resta invalidata); lista sempre consultabile; categorie art. 9 GDPR rifiutate.

### 4.7 Automazioni (ADR-53, ADR-54 — Fase 2, S9/S10)
- Entità Automazione (§3.14) eseguita **dallo scheduler già esistente** (launchd + job idempotente con dead man's switch, ADR-29): mai un secondo scheduler, mai una seconda webapp (n8n scartato — brief R4).
- L'LLM **compila solo i parametri** di trigger/condizioni/azioni scelti da **enum chiusi**, validati server-side (Pydantic); mai JSON libero né codice (ADR-04).
- Ciclo di vita: proposta come frase QUANDO/SE/ALLORA (è il diff di ADR-07) → **dry-run su dati storici** («sarebbe scattata 3 volte, ecco cosa avresti ricevuto») → nasce **disattivata** → conferma esplicita → ogni esecuzione in AuditLog → pausa/elimina a un tap → **anti-tempesta** (oltre il limite giornaliero si autosospende con avviso).
- Azioni v1: *crea Task*; *notifica a destinatari fissi hardcoded*. Default: un solo digest giornaliero aggregato; notifica immediata solo per regole «urgente».
- **Trigger email (S10, ADR-54)**: IMAP polling dallo scheduler, **solo mittenti in allowlist**; credenziali solo in **Keychain** (casella dedicata o app password revocabile); la sintesi gira **senza alcun tool esposto all'LLM**; HTML→testo, link non cliccabili, banner «riassunto AI di contenuto non verificato»; retention riassunti ≤ 30 giorni; ogni azione nata da email ripassa da HITL. L'email è input non fidato ("lethal trifecta" — brief R4).

### 4.8 Modalità Chiamata (voce) — Fase 3 (ADR-59, ADR-60, ADR-61)
JARVIS parla e ascolta a mani libere (uso alla guida), ma resta **bocca e orecchie**: a voce **solo** Q&A read-only + **dettatura di proposte che finiscono in coda**; l'esecuzione di scritture a voce è **vietata** (un "sì" alla guida = approvazione cieca, ADR-07). Il gate di scrittura è **nel codice** (token di approvazione generato solo dalla UI dopo il render del diff, non forgiabile dall'LLM); niente "approva tutto". La trascrizione vocale è **input non fidato** (come le email IMAP, ADR-60): contesto mai istruzioni, loggata nell'evidence pack, **read-back verbale** dei campi chiave, nessun audio persistito, attivazione esplicita push-to-talk (mai wake word), **no autenticazione vocale** (art. 9 GDPR). Dettaglio di stack, accesso e HITL in **§10**.

---

## 5. Pipeline documentale

Fondamento: **rendering on-demand da dati canonici**, nessuna cascata documento-da-documento (ADR-14).

```
Dati canonici (Soggetto/Immobile/Pratica/Contratto)
        │  + Template (versione approvata/depositata)
        ▼
 docxtpl (Jinja2) ──► DOCX ──► LibreOffice headless ──► PDF
        │                                                  │
        ▼                                                  ▼
 validazione campi                              IstanzaDocumento:
 (generazione bloccata se mancanti)             dati snapshot + artefatto PDF archiviato
```

Regole operative:

1. **Categorie per la segretaria**: Contratti, Moduli di pratica, Autonomi. "Legato" = associazione predefinita con condizioni (es. modulo mutuo solo se `pratica.prevede_mutuo` — ADR-22).
2. **Genera pacchetto pratica**: un tasto renderizza in blocco tutte le istanze previste dalla pratica.
3. **Dry-run segnaposti** al salvataggio del template: dati finti, controllo font mancanti e segnaposti irrisolti, messaggi in italiano semplice (ADR-16).
4. **Dati mancanti → generazione bloccata** con elenco dei campi vuoti; nessun documento con buchi (ADR-21).
5. **Anteprima = PDF archiviato** alla creazione dell'istanza, mostrato via PDF.js; mai ri-convertito a vista (ADR-15).
6. **Correzione dati → rigenerazione esplicita** (nuova istanza), mai modifica a vista del PDF (ADR-14).
7. **Import `.doc`/`.odt`**: conversione una tantum in `.docx` → nasce **bozza** da approvare, mai versione depositata (ADR-17). **PDF mai come template** (ADR-19).
8. **Versioni depositate**: hash SHA-256, stato bozza/depositata/ritirata, lock, approvazione con ruoli; cambio modello → nuova versione + **ri-deposito in Camera di Commercio**; pratiche in corso ancorate alla versione di nascita (ADR-18, ADR-44).
9. **L'informativa privacy è un template come gli altri**: il modulo dell'informativa vive in questa stessa pipeline come Template versionato; la `versione del modulo` del RecordConsenso è il suo `template_version_id`, e l'allegato automatico alle pratiche usa il meccanismo del pacchetto (ADR-20, ADR-22). Nessun motore parallelo (verbale C7).

⚠️ **Gate pre-codice**: validazione su 5-10 modelli reali depositati (conversione PDF, font, dry-run, confronto stampa/anteprima). Se fallisce, si correggono i template, non il motore.

---

## 6. Pipeline notifiche (scadenze locazioni)

Canale unico v1: **email** (ADR-23). L'email raccoglie **intenzioni**, non produce effetti legali: la disdetta formale resta raccomandata AR/PEC e il messaggio lo dice esplicitamente (ADR-27).

```
job giornaliero via launchd (idempotente, con retry)
   │
   ▼
calcolo scadenze: Trigger 1 (fine triennio −7 mesi)
                  Trigger 2 (fine biennio −6 mesi, "nuova stipula")
   │  date dalla proroga effettiva; disdette inquilino/proprietario registrate
   ▼
bozza email AI (modificabile) ──► conferma umana (HITL) ──► invio SMTP
   │                                                              │
   ▼                                                              ▼
reminder +7/+14/+30 ai non rispondenti ◄────────── tracciamento stato
   │
   ▼
routing scenari: A Chiusura/Cessazione (stop; "no" proprietario → lead vendita)
                 B Rinnovo (triennio: tacito; biennio: nuova stipula)
                 C In trattativa (task operatore + data rientro)
```

Presidi non negoziabili (ADR-29):

- **Job schedulato (launchd) idempotente con retry**: riesecuzioni non duplicano invii (il "cron" di ADR-29).
- **Dead man's switch**: un job che non gira genera **allarme** (le finestre legali bruciate in silenzio sono il fallimento della feature).
- **Task operatore automatico** a scadenza −6 mesi e **dashboard "scadenze senza risposta"**.
- **Deliverability**: SPF/DKIM/DMARC configurati + gestione bounce; email obsolete = trigger muto → verifica periodica dei recapiti.
- **Inquilino escluso** dai destinatari, ma le sue disdette sono nel modello dati (ADR-26).

v2 (subordinata a basi giuridiche GDPR, informative, consenso, DPA): tracking aperture e parsing AI delle risposte; nessuno scoring senza base giuridica.

⚠️ **Verifica esterna obbligatoria**: validazione legale del doppio trigger (l. 431/98) con consulente, in parallelo alla build, prima del go-live del modulo scadenze.

---

## 7. Pipeline OCR e adempimenti

Principio: **deterministic-first** — l'OCR è l'ultima spiaggia, non il motore (ADR-32).

```
Documento caricato
   │
   ├─ APE in PDF nativo? ──► estrazione testo diretta (PyMuPDF/pdfplumber)
   │                          └─ whitelist layout regionali + regex per campo
   │                             + validazione dominio (classe A4–G, EPgl,nren)
   │                             └─ layout sconosciuto → CODA REVISIONE UMANA
   │
   ├─ CIE / passaporto? ──► lettura MRZ ICAO 9303 + CHECKSUM (gate bloccante)
   │
   └─ Residuo (CI senza MRZ, foto) ──► PaddleOCR-VL (unico candidato)
        │
        ▼
   cross-check codice fiscale (ricalcolo + check digit) — mismatch → blocco
        │
        ▼
   form anti-automation-bias: split-screen, conferma campo-per-campo,
   highlight solo bassa confidenza, salvataggio bloccato se gate falliti,
   log di ogni correzione (metrica accuracy)
        │
        ▼
   matrice adempimenti → compiti parlanti per l'operatore
```

Regole operative:

1. **GLM-OCR escluso** (italiano non supportato — ADR-31). Bake-off obbligatorio su **50+ documenti reali** (CI, CIE, passaporti, APE di ≥3 regioni): errore >2% su campi anagrafici → fallback al vision LLM principale; decisione chiusa (ADR-33).
2. **Autenticità APE**: in v1 è un **flusso manuale guidato** — Task "verifica su SIAPE/registro regionale" con esito registrato in `stato_verifica` (sezione APE dell'Immobile) e traccia in AuditLog; l'integrazione automatica coi registri è parcheggiata in Fase 2 (ADR-37, verbale C7). Parsare un PDF falso è peggio che non parsarlo.
3. **Codice fiscale** ricalcolato deterministicamente dai dati estratti + check digit: costo zero, validazione incrociata sempre attiva (ADR-35).
4. **Matrice adempimenti con etichette parlanti**: il sistema risolve *tipo pratica × categoria soggetto × registrazione* e mostra compiti, non articoli (ADR-36):
   - «Comunicazione Questura entro 48h — ospiti extra-UE» (art. 7 D.Lgs 286/98)
   - «Comunicazione Alloggiati Web entro 24h — locazione turistica, tutti gli ospiti» (TULPS 109)
   - Art. 12 DL 59/78 gestito in silenzio (assorbito dalla registrazione AdE), con tooltip.
   - **Nazionalità mancante → il sistema chiede**: mai skip silenzioso.
5. **Form anti-automation-bias**: la frizione è il feature, non il bug (ADR-34).

---

## 8. Backup e sicurezza

### 8.1 Backup (ADR-06)
```
job notturno (launchd): sqlite3 .backup → ~/Gestionale/backup/db_YYYYMMDD.sqlite
                    │ (snapshot consistente, MAI copia a caldo di -wal/-shm)
                    ▼
          copia offsite CIFRATA (fuori dall'edificio)
                    │
                    ▼
   restore test MENSILE su copia di prova + alert se fallisce
   alert anche su: backup non eseguito, disco quasi pieno
```
- L'hardware (Mac Mini) è single point of failure: la **procedura** non può esserlo.
- **Rotazione dei backup** (es. 30 snapshot giornalieri + 12 mensili) e `PRAGMA integrity_check` sulla copia a ogni snapshot (verbale C7).
- Documentazione di ripristino in italiano semplice (bus factor).

### 8.2 Sicurezza dati
- **Cifratura** dei dati sensibili (documenti d'identità, scansioni consensi) e della copia offsite.
- **Accessi loggati**: ogni consultazione di dati sensibili lascia traccia in AuditLog.
- **Retention immagini documento — differenziata per finalità** (ADR-49): le immagini a soli fini di estrazione sono cancellate dopo l'estrazione (ADR-38); le copie richieste dall'adeguata verifica antiriciclaggio sono conservate **10 anni, cifrate e ad accesso loggato** (ADR-46); distinzione netta tra **dati estratti** (restano nel DB) e **immagine**.
- **Login e ruoli** come da §3.10; nessun accesso anonimo.

### 8.3 Migrazioni di schema (verbale C7)
- Modifiche allo schema SQLite solo tramite **script SQL numerati e versionati nel repo** (es. `migrazioni/001_....sql`), applicati in ordine.
- Ogni migrazione esegue **prima un backup automatico** (`sqlite3 .backup`); nessuna modifica manuale allo schema in produzione.
- Convenzione attiva da S1 e obbligatoria da S3 (dati reali nel sistema).

### 8.4 GDPR
- **DPIA ex art. 35 in due tempi**: bozza **prima di S3** (l'art. 35 la richiede *prima* del trattamento, non del go-live), aggiornamento prima di S7 (copre anche la base giuridica del corpus del bake-off OCR), chiusura formale in S8 (verbale C7).
- Informativa e base giuridica specifiche per le scansioni; il processing locale su M4 è l'argomento privacy-by-design e va usato (ADR-38).
- **Conservazione documentale 10 anni** per i documenti AML e di gestione (ADR-46).
- Niente riuso dei dati OCR per finalità ulteriori senza nuova base giuridica (art. 5(1)(b) GDPR).

---

## 9. Matrice compliance

Tutte le regole compliance sono **parametri versionati** mantenuti dal fornitore, con **disclaimer strutturale** «adempimento non verificabile dal software», audit trail (chi vide quale etichetta, quando, quale versione della norma) e clausola nei ToS (ADR-45). Il cliente è fonte affidabile di bisogni, inaffidabile di riferimenti legali: il gestionale usa le diciture corrette senza esporre il dibattito giuridico.

| Adempimento | Regola applicata | Implementazione nel gestionale | Fonte/verifica |
|---|---|---|---|
| **Registrazione locazioni (RLI)** | Entro **30 giorni** dalla stipula/decorrenza, canale RLI AdE | Scadenziario con T+0 = registrazione del contratto **nel sistema** (ADR-43) | AdE — ⚠️ verifica consulente |
| **Deposito formulari** | Presso la **Camera di Commercio** (art. 5 L. 39/89 + d.m. 452/1990), **non** AdE; **ri-deposito a ogni modifica** dei modelli; sanzioni per mancato deposito (~€1.549) e uso modello diverso (~€516) | Stato `depositata` + metadati REA + promemoria automatico a ogni modifica (ADR-18, ADR-44) | ⚠️ verifica consulente |
| **Antiriciclaggio — adeguata verifica** | Al **conferimento dell'incarico**, **indipendentemente dall'importo**; conservazione 10 anni; SOS a UIF | Task obbligatorio apertura pratica + retention 10 anni nativa (ADR-44, ADR-46) | D.Lgs 231/2007 — ⚠️ consulente AML |
| **Contante 5.000€** | **Limite legale all'uso del contante** (art. 49, mod. L. 197/2022) — **non** soglia AML | **Alert bloccante** sui pagamenti in contante ≥5.000€ | ⚠️ consulente AML |
| **Soglia 1.000€** | **Policy interna volontaria** più stringente (lecita) | Soglia **configurabile**, etichetta UI «policy interna», mai «obbligo di legge» | ADR-44 |
| **Art. 7 D.Lgs 286/98** | Comunicazione Questura **entro 48h** per cittadini **extra-UE** | Etichetta parlante dalla matrice; blocco se nazionalità mancante (ADR-36) | ⚠️ revisione legale matrice |
| **Art. 12 DL 59/78** | Cessione fabbricati 48h, **assorbito** dalla registrazione AdE per contratti registrati | Gestito in silenzio con tooltip | ⚠️ revisione legale matrice |
| **TULPS art. 109** | Alloggiati Web **entro 24h** per locazioni turistiche — **tutti gli ospiti** | Etichetta parlante, indipendente dalla nazionalità | ⚠️ revisione legale matrice |
| **Locazioni 3+2 (l. 431/98)** | Preavviso 6 mesi a **fine triennio**; a **fine biennio** il contratto cessa → nuova stipula | Doppio trigger (ADR-24) | ⚠️ **consulente legale prima del go-live** |
| **Conservazione documentale** | **10 anni** (AML e gestione); valore probatorio scansioni sotto CAD (D.Lgs 82/2005) | Retention nativa 10 anni; ⚠️ hash+timestamp da soli **non** danno valore probatorio → verifica conservativa | ⚠️ verifica legale/conservativa |

**Riconciliazione mensile** (ADR-46, verbale C7): Task guidato mensile che confronta i Movimenti in stato `incassato` con l'estratto conto bancario / CSV del commercialista; le differenze sono **elencate una per una** e l'esito (quadra / differenze motivate) è registrato in AuditLog. Nessun collegamento bancario automatico in v1.

**Disclaimer strutturale** (mostrato dove il sistema presenta adempimenti): *«Il gestionale segnala e ricorda adempimenti sulla base di parametri versionati; la verifica e l'esecuzione dell'adempimento restano responsabilità dell'agenzia e dei suoi consulenti. Adempimento non verificabile dal software.»*

---

## 10. Mobile, accesso remoto e modalità Chiamata (Consiglio C9)

Il gestionale si usa anche dal **telefono del Proprietario, ovunque**, tramite Tailscale. Il dato resta sul Mac Mini: il telefono è un **client remoto** su rete privata cifrata.

### 10.1 Versione mobile = PWA responsive (ADR-55)
Stessa app FastAPI server-rendered, resa **responsive** (mobile-first sulle schermate nuove) + **manifest PWA** installabile; **nessuna app nativa**. Unica fonte design: checklist impeccable (una azione primaria per schermata, touch ≥44px). Service worker: cache **solo asset statici**, mai dati clienti offline. Accorgimenti mobile: PDF con bottone "Apri/Scarica" nativo accanto a PDF.js; upload foto documenti con `<input type=file accept=image/* capture=environment>` + ricompressione server-side; tabelle larghe in scroll orizzontale nel proprio contenitore (mai scroll di pagina). **Prerequisito tecnico:** HTTPS via `tailscale cert`/`tailscale serve` (necessario per PWA e microfono) — da fare **subito**.

### 10.2 Accesso remoto via Tailscale (ADR-56, ADR-57)
Tailscale (WireGuard mesh) è il **trasporto, mai l'autenticazione**. Difese obbligatorie a strati: ACL **default-deny** (solo il nodo-telefono del Proprietario → porta HTTPS dell'app), device approval, Tailnet Lock, MFA, key expiry; **Funnel/exit-node/subnet-routing vietati, zero port-forwarding**; app in bind solo su `localhost` + `100.x`. **Login + ruoli (ADR-08, ADR-50) restano obbligatori sopra la VPN.** Ogni accesso remoto in AuditLog con identità del nodo + alert su nodo nuovo. Deroga n.2 al tutto-locale dichiarata in §1 (ADR-56): DPA + registro trattamenti; Headscale come exit strategy documentata, non implementata. **Runbook telefono perso/rubato** (ADR-58): revoca nodo, invalidazione sessioni, rotazione password, verifica audit, valutazione art. 33 GDPR in 72h — **testato una volta** come il restore test.

### 10.3 Stack voce locale (ADR-61) — Fase 3
```
Telefono (browser/PWA): push-to-talk mic ──WebSocket(Tailscale)──► FastAPI
        │                                                              │
        │ audio a chunk ◄── TTS ◄── Ollama 27B (residente) ◄── whisper.cpp (STT)
        ▼
   riproduzione                     [tutti i processi voce sul Mac, ON-DEMAND]
```
Glue custom **dentro** FastAPI (endpoint WebSocket), **nessun framework** né media server sempre acceso; STT **whisper.cpp** large-v3-turbo Core ML (fallback medium quantizzato); LLM **Ollama 27B già residente**; TTS scelto con **demo audio** (`say`/AVSpeech → Piper `it_IT-paola` via subprocess GPL-3.0 mai linkata → Kokoro-82M Apache-2.0; **XTTS vietato**). Stima RAM: 27B ~17GB + macOS ~4-5GB → residuo ~2-3GB: whisper turbo (~1,5GB) + TTS ci stanno **solo** on-demand e tenendo d'occhio il KV-cache — **misura obbligatoria nel walking skeleton**, anche con S9/bge-m3 attivo. Stima latenza 1,5-3 s/turno (fino a 2-5 s su cellulare via DERP): vale la **misura**, non la stima; soglia di kill 4 s/turno (ADR-59). Animazione orb/waveform **nativa** (Web Audio AnalyserNode + Canvas 2D + CSS), zero dipendenze (ADR-63); è rifinitura finale.

### 10.4 HITL a voce — flusso in due tempi (ADR-59, ADR-60)
1. **In auto (a voce):** consulto dati read-only + detto proposte → **read-back verbale** dei campi chiave → la proposta va **in coda** (nessun effetto sul DB). Trascrizione = input non fidato, loggata; nessun audio persistito.
2. **Da fermo (a video):** apro la coda «Da approvare» (telefono o desktop), vedo il **diff leggibile** di ogni proposta, approvo/rifiuto **una per una**. Vietato "approva tutto"; anche le proposte rifiutate/scadute restano in AuditLog.

⚠️ **Verifiche esterne (C9)** prima della produzione: DPA Tailscale + registro trattamenti; DPIA leggera (voce+remoto+AI); licenza voce TTS + uso server-side GPL-3.0; retention trascrizioni vocali; parere art. 173 CdS per la policy d'uso alla guida (nella pagina "cosa NON fa JARVIS", rifirmata).

---

## Chiusura

- Decisioni normative: `03_DECISIONI_CONSIGLIO.md` (ADR-01…ADR-63). Questo documento le applica; in caso di conflitto, **vincono gli ADR**.
- Verifiche esterne aperte (bloccanti per i moduli indicati): modello LLM (§4.1), modelli reali depositati (§5), doppio trigger l. 431/98 (§6), bake-off OCR 50+ documenti (§7), consulente AML e conservazione CAD (§9), bozza DPIA prima di S3 (§8.4); **e, dal Consiglio C9 (§10):** DPA Tailscale + registro trattamenti, DPIA leggera voce+remoto+AI, licenza voce TTS, retention trascrizioni, parere art. 173 CdS. Il **vision LLM di fallback** (ADR-33) si sceglie all'esito del bake-off di S7 con mini-ADR — vincolo: **deve girare in locale** (verbale C7).
- Ordine di build raccomandato dal Consiglio C1: **1)** backup attivo prima dei dati veri; **2)** CRUD + audit log senza AI; **3)** un template reale (incarico) → DOCX → PDF; **4)** solo dopo, JARVIS in lettura.
