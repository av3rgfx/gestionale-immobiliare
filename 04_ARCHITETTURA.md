# 04 — Architettura tecnica

**Progetto:** Gestionale Immobiliare + JARVIS — webapp locale per piccola agenzia immobiliare italiana con agente AI locale.
**Ambiente di produzione:** Mac Mini M4, rete LAN dell'agenzia (2-5 utenti).
**Ambiente di sviluppo:** sessioni nella sezione **Code** di Claude Desktop (ADR-13), repo GitHub, codice verso API cloud (dati sintetici) e poi modello locale.
**Uso di questo documento:** riferimento citato dai prompt di sprint. Ogni sprint deve dichiarare a quali sezioni si attiene; le decisioni normative sono in `03_DECISIONI_CONSIGLIO.md` (ADR-01…ADR-46).

---

## 1. Visione e principi non negoziabili

Il sistema è il **registro operativo** di una piccola agenzia immobiliare: anagrafiche, immobili, pratiche, documenti legali, scadenze, movimenti economici e adempimenti. JARVIS, l'agente AI locale, è un assistente che **capisce l'italiano e propone**, ma il sistema decide e scrive solo attraverso codice deterministico.

Principi non negoziabili (violare uno di questi = blocco dello sprint):

1. **Deterministico prima dell'AI.** Documenti legali, calcoli, scadenze e adempimenti escono da template versionati e da codice. L'LLM non è mai autore di testo legale né di logica di calcolo (ADR-02).
2. **Tutto locale.** In produzione nessun dato lascia il Mac Mini: LLM via Ollama, OCR locale, nessuna API cloud. In sviluppo, le API cloud vedono **solo dati sintetici o anonimizzati** (ADR-01, ADR-05).
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
| Template documenti | **docxtpl** (Jinja2 dentro DOCX) | Riempimento deterministici dei modelli |
| Conversione | **LibreOffice headless** (`soffice --headless --convert-to pdf`) | DOCX → PDF identico alla stampa |
| Font | **Liberation** (metricamente compatibili con Calibri/Cambria) | Fedeltà tipografica anteprima/stampa (ADR-16) |
| Anteprima | **PDF.js** | Visualizzazione del PDF archiviato nel browser |
| LLM | **Ollama** (API OpenAI-compatible, `/v1`) | Runtime locale per JARVIS; in dev API cloud configurabili |
| OCR (residuo) | **PaddleOCR-VL** | Solo per CI senza MRZ e foto; italiano, Apache 2.0, Apple Silicon (ADR-32) |
| Estrazione testo | **PyMuPDF / pdfplumber** | APE in PDF nativi, senza OCR |
| MRZ | Parser **ICAO 9303** con checksum | CIE/passaporti, gate bloccante |
| Email | **SMTP** (provider a scelta: es. Brevo/Gmail/Workspace) | Canale unico notifiche v1 con SPF/DKIM/DMARC |

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
- **Blocco APE**: classe energetica (dominio A4–G), **EPgl,nren** (numerico plausibile), **data scadenza APE**, **path file** dell'attestato, **stato verifica autenticità** (`verificato_registro` / `da_verificare` / `non_verificabile`), layout riconosciuto in whitelist o in coda revisione (ADR-37).

### 3.3 Pratica
Contenitore operativo di una trattativa.
- Tipo pratica (vendita, locazione abitativa, locazione turistica, ecc.), stato, agente responsabile, soggetti coinvolti (ruolo per soggetto), immobili collegati.
- Flag condizionali per i moduli (es. `prevede_mutuo` → include modulo mutuo nel pacchetto — ADR-22).
- Data firma contratto (evento che genera i Movimenti — ADR-40).

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
- Include: approvazioni HITL, conferme invio email, correzioni OCR (metrica accuracy — ADR-34), consultazioni di etichette compliance (ADR-45).

---

## 4. Architettura agente JARVIS

JARVIS è un assistente in linguaggio naturale dentro al gestionale. Principio guida: **bocca e orecchie, mai mani** (ADR-02). Capisce l'italiano, interroga i dati, propone; scrive solo attraverso funzioni deterministiche e con conferma umana.

### 4.1 Astrazione provider
Un unico client LLM con due soli parametri configurabili: **`base_url`** e **`model`**.

- **Produzione**: `base_url` → Ollama locale (`/v1`, API OpenAI-compatible). Modello 27B-classe Q4 su Mac Mini M4 24GB (sweet spot: ~17GB modello + OS).
- **Sviluppo**: `base_url` → API cloud (OpenAI-compatible). **Mai dati clienti reali**: solo sintetici/anonimizzati (ADR-05).
- La stessa **eval suite italiana** gira identica su cloud e su locale, rieseguita sul modello locale **dal secondo sprint** (non alla fine).
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
- Le "skill" sono **documenti Markdown curati** (procedure operative in italiano: es. "come preparare il pacchetto pratica per una locazione turistica").
- JARVIS può **proporre** una nuova skill in MD; l'attivazione richiede **approvazione umana** e il file è versionato in **Git** (ADR-04).
- **MAI** codice auto-generato eseguito: nessuna skill può contenere né invocare codice prodotto dall'LLM. Le skill guidano il comportamento, non estendono il programma.

### 4.5 Eval suite italiana
- Dataset di test in italiano (intenti tipici dell'agenzia) costruito su **dati sintetici/anonimizzati**.
- Eseguita a ogni cambio di modello/prompt e **dal secondo sprint** anche sul modello locale: la metrica di accettazione deve reggere in produzione, non solo in dev.

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
2. **Autenticità APE**: verifica su registro regionale/SIAPE dove disponibile; `stato_verifica` nel blocco APE dell'Immobile. Parsare un PDF falso è peggio che non parsarlo (ADR-37).
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
- Documentazione di ripristino in italiano semplice (bus factor).

### 8.2 Sicurezza dati
- **Cifratura** dei dati sensibili (documenti d'identità, scansioni consensi) e della copia offsite.
- **Accessi loggati**: ogni consultazione di dati sensibili lascia traccia in AuditLog.
- **Retention immagini documento**: le immagini da cui sono stati estratti i dati sono cancellate dopo l'estrazione, oppure conservate con retention breve e motivata; distinzione netta tra **dati estratti** (restano nel DB) e **immagine** (ADR-38).
- **Login e ruoli** come da §3.10; nessun accesso anonimo.

### 8.3 GDPR
- **DPIA ex art. 35 prima del go-live** (trattamento di documenti d'identità e dati particolari).
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

**Disclaimer strutturale** (mostrato dove il sistema presenta adempimenti): *«Il gestionale segnala e ricorda adempimenti sulla base di parametri versionati; la verifica e l'esecuzione dell'adempimento restano responsabilità dell'agenzia e dei suoi consulenti. Adempimento non verificabile dal software.»*

---

## Chiusura

- Decisioni normative: `03_DECISIONI_CONSIGLIO.md` (ADR-01…ADR-46). Questo documento le applica; in caso di conflitto, **vincono gli ADR**.
- Verifiche esterne aperte (bloccanti per i moduli indicati): modello LLM (§4.1), modelli reali depositati (§5), doppio trigger l. 431/98 (§6), bake-off OCR 50+ documenti (§7), consulente AML e conservazione CAD (§9).
- Ordine di build raccomandato dal Consiglio C1: **1)** backup attivo prima dei dati veri; **2)** CRUD + audit log senza AI; **3)** un template reale (incarico) → DOCX → PDF; **4)** solo dopo, JARVIS in lettura.
