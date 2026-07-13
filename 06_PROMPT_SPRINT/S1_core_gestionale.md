# Prompt Sprint S1 — Core gestionale

> **Come usarlo:** apri una sessione **NUOVA** in **Code** (sezione di Claude Desktop) sulla cartella del repository. Incolla prima la **frase rituale di apertura** (file `02`, sezione C), aspetta il riassunto in 5 righe, poi incolla **tutto** il blocco qui sotto, da `INCOLLA DA QUI` a `FINO A QUI`. Non continuare in una sessione vecchia: una task per sessione.
> **Prerequisito:** Sprint S0 chiuso (ambiente pronto, eval e backup bozza funzionanti, handoff + commit fatti). Solo dati finti: il backup completo arriva in S3.

---
==================  INCOLLA DA QUI  ==================

**RITUALE DI APERTURA (obbligatorio, prima di tutto):** leggi `REGOLE.md` nella root del repo e riassumilo in 5 righe prima di toccare codice. Poi leggi `HANDOFF.md` (riassunto dell'ultima sessione) e questi riferimenti nel repo: `04_ARCHITETTURA.md` (per questo sprint: §3, in particolare §3.1, §3.2, §3.10, §3.11), `03_DECISIONI_CONSIGLIO.md` (registro ADR: fonte vincolante, in caso di conflitto vincono gli ADR) e `05_ROADMAP_SPRINT.md` (sezione S1). Conferma in 3 righe cosa hai capito e da che punto ripartiamo. Solo dopo inizia.

## CONTESTO

Gestionale locale per piccola agenzia immobiliare italiana + agente AI locale JARVIS (che arriva solo in S6). Stack: FastAPI + SQLite (WAL) + docxtpl + LibreOffice headless + PDF.js. Decisioni architetturali già validate: non si ridiscutono. Io non sono uno sviluppatore: un passo alla volta, comandi copiabili spiegati in una riga, conferma prima di azioni distruttive. Solo dati finti in questo sprint.

## OBIETTIVO DELLO SPRINT S1

L'app esiste e si apre nel browser: login con 4 ruoli, audit log immutabile, gestione soggetti e immobili, e blocco pratiche su immobili senza APE.

## AMBITO

**Entra:** scaffold FastAPI + SQLite WAL; tabelle iniziali dal modello dati di `04_ARCHITETTURA.md` §3; login e 4 ruoli (Proprietario, Admin, Agente, Segretaria) con permessi; audit log; CRUD soggetti con validazione codice fiscale; CRUD immobili con APE e blocco pratiche senza APE; UI semplice con errori in italiano chiaro.
**NON entra:** documenti (S2), privacy (S3), scadenze (S4), movimenti (S5), AI (S6). Se emerge qualcosa di non previsto: parcheggio Fase 2 e mi avvisi.

## TASK ORDINATI

1. **Scaffold applicazione.** Crea lo scaffold FastAPI con SQLite in modalità WAL, struttura cartelle del progetto secondo `04_ARCHITETTURA.md` §2, e le tabelle iniziali dal modello dati di `04_ARCHITETTURA.md` §3 (Soggetto, Immobile, Pratica, Utente/Ruolo, AuditLog). Fammi avviare l'app e vedere la pagina iniziale nel browser.
2. **Matrice permessi.** PRIMA di codificare, proponimi la tabella permessi per i 4 ruoli (chi può creare/modificare/vedere cosa) in una tabella leggibile: la approvo io, poi la implementi.
3. **Login e ruoli.** Implementa login con i 4 ruoli e i permessi approvati. Fammi testare l'accesso con almeno due ruoli diversi.
4. **Audit log immutabile.** Ogni creazione/modifica/eliminazione registra: chi, cosa, quando, su quale record (con diff dei campi chiave). L'audit log non è modificabile dall'app. Fammi vedere le voci generate dai miei test.
5. **CRUD soggetti.** Persone fisiche e giuridiche (campi di §3.1), con validazione del codice fiscale (check digit deterministico): CF sbagliato → rifiuto con messaggio comprensibile. Se la nazionalità è richiesta da un flusso e manca, il sistema la chiede: mai skip silenzioso.
6. **CRUD immobili + blocco APE.** Immobile con dati catastali e blocco APE (campi di §3.2); la creazione di una pratica su immobile senza APE è **bloccata** con spiegazione chiara.
7. **Pulizia UI.** Liste con ricerca, form con etichette in italiano semplice, errori che dicono cosa fare, niente gergo tecnico. Applica la checklist design (sezione 4 di `REGOLE.md`) schermata per schermata.

## CRITERI DI ACCETTAZIONE (li verifico io)

- [ ] Apro l'app nel browser e faccio login come Agente e come Segretaria: i menu sono diversi.
- [ ] Inserisco un codice fiscale sbagliato: l'app lo rifiuta e mi spiega perché.
- [ ] Creo un soggetto corretto, chiudo e riapro il browser: è ancora in lista.
- [ ] Creo un immobile senza APE e provo ad aprire una pratica: l'app blocca e spiega.
- [ ] Chiedo di vedere l'audit log: ci sono le operazioni che ho fatto, con data e utente.
- [ ] Un messaggio di errore qualsiasi è in italiano comprensibile, senza codici o termini tecnici.

## ISTRUZIONI OPERATIVE PER ME (utente)

- Comandi nel Terminale (⌘+spazio → "Terminale"): incollo, invio, ti rimando tutto l'output anche se sembra errore. Password del Mac se richiesta: normale, non si vede mentre digito.
- Per avviare/fermare l'app userò i comandi che mi segni all'inizio (li tengo in un foglio a parte).
- Non eseguo comandi non spiegati in una riga; azioni distruttive solo con mio "sì, procedi".
- Se derivi: "Stop. Rileggi la sezione X di REGOLE.md e rifai seguendola". Sessione troppo lunga → chiusura e sessione nuova con questo stesso prompt.

## CHIUSURA OBBLIGATORIA

(1) Produci il riassunto di chiusura compilando il template a 8 punti del file `07_HANDOFF_TEMPLATE.md` e salvalo come `HANDOFF.md` nella root del repo, sostituendo il vecchio. (2) Checklist di conformità a `REGOLE.md` in 5 righe. (3) Commit `sprint-1: descrizione breve` + push; mostrami l'ultimo comando git e il suo output (o i passaggi su GitHub Desktop).

==================  FINO A QUI  ==================
---
