# Prompt Sprint S0 — Fondamenta

> **Come usarlo:** apri una sessione **NUOVA** in **Code** (sezione di Claude Desktop) sulla cartella del repository. Incolla prima la **frase rituale di apertura** (file `02`, sezione C), aspetta il riassunto in 5 righe, poi incolla **tutto** il blocco qui sotto, da `INCOLLA DA QUI` a `FINO A QUI`. Non continuare in una sessione vecchia: una task per sessione.
> **Prerequisito:** la sessione 1 (Prompt Maestro) è chiusa con `HANDOFF.md` e commit fatti. Se lo scaffold S0 è già stato completato nella sessione 1, questo prompt serve a **verificare e completare** ciò che manca.

---
==================  INCOLLA DA QUI  ==================

**RITUALE DI APERTURA (obbligatorio, prima di tutto):** leggi `REGOLE.md` nella root del repo e riassumilo in 5 righe prima di toccare codice. Poi leggi `HANDOFF.md` (riassunto dell'ultima sessione) e questi riferimenti nel repo: `04_ARCHITETTURA.md` (per questo sprint: §1 e §2), `03_DECISIONI_CONSIGLIO.md` (registro ADR: fonte vincolante, in caso di conflitto vincono gli ADR) e `05_ROADMAP_SPRINT.md` (sezione S0). Conferma in 3 righe cosa hai capito e da che punto ripartiamo. Solo dopo inizia.

## CONTESTO

Stiamo costruendo il gestionale locale di una piccola agenzia immobiliare italiana + l'agente AI locale JARVIS. Webapp locale: FastAPI + SQLite (WAL) + docxtpl + LibreOffice headless + PDF.js; produzione su Mac Mini M4, sviluppo su questo MacBook. Le decisioni architetturali sono già prese e validate: non si ridiscutono. Io non sono uno sviluppatore: guidami un passo alla volta: esegui tu i comandi in Code, ognuno spiegato in una riga prima della mia approvazione, conferma esplicita prima di ogni azione distruttiva. Mai dati reali dei clienti verso API cloud: solo dati sintetici.

## OBIETTIVO DELLO SPRINT S0

Il cantiere è pronto: repo, regole, ambiente di sviluppo, astrazione del provider AI, skeleton della eval suite, bozza del backup. Niente funzioni del gestionale in questo sprint.

## AMBITO

**Entra:** verifica completamento sessione 1; ambiente dev (Homebrew, Python, LibreOffice, font Liberation, virtualenv, dipendenze base); cartella dati `~/Gestionale/`; astrazione provider LLM con `base_url`/`model` configurabili + test di connessione; eval suite skeleton con casi in italiano e report; bozza script backup con `sqlite3 .backup`.
**NON entra:** CRUD, UI, template, backup schedulato (S3), modelli AI locali. Se emerge qualcosa di non previsto, lo annoti nel parcheggio Fase 2 della roadmap e mi avvisi.

## TASK ORDINATI

1. **Verifica stato sessione 1.** Controlla che nel repo ci siano i file della harness (`00`–`08` e `06_PROMPT_SPRINT/`), `REGOLE.md`, `CLAUDE.md` e `HANDOFF.md`. Se manca qualcosa, fermati e completalo con me prima di proseguire. Verifica che `CLAUDE.md` rimandi correttamente a `REGOLE.md`.
2. **Ambiente di sviluppo.** Guidami a installare/verificare: Homebrew, Python 3, LibreOffice, font Liberation. Poi virtualenv del progetto e le dipendenze di `requirements.txt` (per S0 basta l'SDK OpenAI; le altre si installano nello sprint che le usa: FastAPI/uvicorn in S1, docxtpl in S2, PyMuPDF/pdfplumber in S7 — REGOLE §2). Un comando alla volta, spiegato in una riga.
3. **Cartella dati.** Crea `~/Gestionale/` con lo script `setup/crea_cartella_dati.sh` (struttura di `04_ARCHITETTURA.md` §2: `documenti/`, `templates/`, `backup/`, `logs/`; il file `db.sqlite` nasce in S1, con la prima migrazione dello schema); documenta in `README.md` che lì vivono tutti i dati.
4. **Astrazione provider LLM.** Crea il modulo `llm/` del progetto: client SDK OpenAI con `base_url` e `model` letti da configurazione (file `.env` o config, mai nel codice), più uno script di test che fa una domanda semplice in italiano e stampa la risposta. Configuralo per il provider cloud di sviluppo.
5. **Skeleton eval suite.** Crea `evals/` con 10–15 casi di test in italiano (domande/risposte attese tipiche del gestionale, in formato semplice) e uno script che li esegue sul provider configurato e produce un report leggibile (passati/falliti per caso). Deve poter girare identico cambiando solo la configurazione del provider.
6. **Bozza backup.** Verifica/completa lo script `scripts/backup_db.sh`: usa `sqlite3 .backup` (MAI copia diretta dei file del database aperto) e controlla l'integrità della copia; in S0 la copia offsite è **manuale**, su una destinazione che scegliamo insieme (disco esterno o cloud cifrato). Aggiungi le istruzioni del test di ripristino su una copia di prova. Niente schedulazione automatica in questo sprint (arriva in S3).

## CRITERI DI ACCETTAZIONE (li verifico io)

- [ ] Su GitHub vedo il repo con i file della harness (00–08), `REGOLE.md`, `CLAUDE.md` e `HANDOFF.md`; `CLAUDE.md` rimanda a `REGOLE.md`.
- [ ] Lancio lo script di test AI: vedo una risposta del modello in italiano nell'output della sessione.
- [ ] Lancio la eval suite: vedo un report con l'esito di ogni caso di test.
- [ ] Lancio `scripts/backup_db.sh` e trovo il file di backup nella destinazione; seguendo le istruzioni, ripristino su una copia di prova e la copia si apre.
- [ ] La cartella `~/Gestionale/` esiste con la struttura prevista.

## ISTRUZIONI OPERATIVE PER ME (utente)

- Quando mi proponi un comando: leggo la tua spiegazione di una riga e approvo con un clic solo se mi è chiaro. Se non mi è chiaro, ti chiedo "spiegamelo meglio" prima di approvare.
- Se un comando chiede la password del Mac: è normale, la digito (non si vede sullo schermo).
- Non eseguo comandi che non mi hai spiegato in una riga.
- Se mi proponi qualcosa di distruttivo, ti rispondo "sì, procedi" solo se sono sicuro.
- Se derivi (inventi funzioni, complici, cambi argomento): ti scrivo "Stop. Rileggi la sezione X di REGOLE.md e rifai seguendola" (X = sezione violata: 1 Disciplina, 2 Semplicità, 3 Consiglio ridotto, 4 Design).
- Se la sessione si allunga troppo, ti chiedo la chiusura e apro una sessione nuova con questo stesso prompt.

## CHIUSURA OBBLIGATORIA

(1) Produci il riassunto di chiusura compilando il template a 8 punti del file `07_HANDOFF_TEMPLATE.md` e salvalo come `HANDOFF.md` nella root del repo, sostituendo il vecchio (ne esiste sempre uno solo). (2) Mostrami la checklist di conformità a `REGOLE.md` (5 righe: cosa rispetta, cosa no). (3) Commit con messaggio nel formato `sprint-0: descrizione breve` + push su GitHub; mostrami l'ultimo comando git e il suo output (o i passaggi fatti su GitHub Desktop).

==================  FINO A QUI  ==================
---
