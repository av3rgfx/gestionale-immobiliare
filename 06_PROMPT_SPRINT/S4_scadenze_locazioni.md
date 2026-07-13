# Prompt Sprint S4 — Scadenze locazioni

> **Come usarlo:** apri una sessione **NUOVA** in **Code** (sezione di Claude Desktop) sulla cartella del repository. Incolla prima la **frase rituale di apertura** (file `02`, sezione C), aspetta il riassunto in 5 righe, poi incolla **tutto** il blocco qui sotto, da `INCOLLA DA QUI` a `FINO A QUI`. Non continuare in una sessione vecchia: una task per sessione.
> **Prerequisito:** Sprint S3 chiuso. **Azione tua fuori dal computer:** contatta il consulente legale per la validazione delle due scadenze (l. 431/98): il modulo non va in produzione senza il suo via libera. Lo sviluppo procede in parallelo.

---
==================  INCOLLA DA QUI  ==================

**RITUALE DI APERTURA (obbligatorio, prima di tutto):** leggi `REGOLE.md` nella root del repo e riassumilo in 5 righe prima di toccare codice. Poi leggi `HANDOFF.md` (riassunto dell'ultima sessione) e questi riferimenti nel repo: `04_ARCHITETTURA.md` (per questo sprint: §6, e §3.4/§3.9 per le tabelle ContrattoLocazione e Scadenza), `03_DECISIONI_CONSIGLIO.md` (registro ADR: fonte vincolante, in caso di conflitto vincono gli ADR) e `05_ROADMAP_SPRINT.md` (sezione S4). Conferma in 3 righe cosa hai capito e da che punto ripartiamo. Solo dopo inizia.

## CONTESTO

Gestionale locale per agenzia immobiliare + JARVIS (S6). Stack: FastAPI + SQLite (WAL). Regole fisse del modulo scadenze (dal verdetto del consiglio C4, non negoziabili): doppio trigger — T1 fine triennio **meno 7 mesi** (decisione del proprietario: disdetta con raccomandata/PEC entro 6 mesi oppure rinnovo tacito +2), T2 fine biennio **meno 6 mesi** ("nuova stipula", NON preavviso: il contratto cessa e si rinegozia); date calcolate dalla **proroga effettiva**; le disdette dell'inquilino vanno registrate e fermano le notifiche; l'email raccoglie intenzioni, **non produce effetti legali** (va scritto nel messaggio); ciclo chiuso obbligatorio (reminder +7/+14/+30, task operatore, dashboard senza risposta, dead man's switch); SPF/DKIM/DMARC e gestione bounce; in v1 niente parsing AI delle risposte, niente tracking aperture, niente scoring. Validazione legale in parallelo prima della produzione. Io non sono uno sviluppatore: un passo alla volta, comandi spiegati in una riga.

## OBIETTIVO DELLO SPRINT S4

Il sistema calcola le scadenze 3+2 col doppio trigger, invia email ai proprietari solo su mia conferma, e porta il ciclo fino alla risposta registrata con routing A/B/C.

## AMBITO

**Entra:** modello dati doppio trigger con disdette inquilino; cron idempotente con retry e dead man's switch; bozze email AI modificabili con invio su conferma; SMTP con SPF/DKIM/DMARC e bounce; reminder e task operatore; dashboard "senza risposta"; routing scenari A/B/C.
**NON entra:** parsing AI delle risposte (Fase 2); tracking aperture e scoring (Fase 2, solo con GDPR a posto); WhatsApp/SMS (Fase 2); produzione senza validazione legale. Non previsto → parcheggio Fase 2 e mi avvisi.

## TASK ORDINATI

1. **Modello dati.** Tabelle ContrattoLocazione e Scadenza come da `04_ARCHITETTURA.md` §3.4/§3.9: date triennio e biennio calcolate dalla **proroga effettiva**; trigger T1 = fine triennio −7 mesi, T2 = fine biennio −6 mesi; campi disdetta anticipata di inquilino e proprietario. La disdetta inquilino registrata **ferma** le notifiche al proprietario.
2. **Cron idempotente + dead man's switch.** Job schedulato che crea le scadenze dovute senza duplicarle (idempotenza), con retry in caso di errore; un controllo che verifica che il job sia girato: se non gira, alert evidente (dead man's switch). Fammi simulare il cron fermo.
3. **Bozze email AI.** Per ogni scadenza, bozza generata dal provider LLM configurato (in sviluppo: provider cloud, ma **solo con dati sintetici/di test**, mai dati reali dei clienti). La bozza è modificabile nell'app e parte **solo dopo la mia conferma esplicita**. Il testo include la dicitura: questa email raccoglie intenzioni; la disdetta formale resta raccomandata AR/PEC.
4. **SMTP serio.** Configurazione SMTP con SPF/DKIM/DMARC (mi guidi nella configurazione del dominio dell'agenzia) e gestione dei bounce: email non valida → il contatto viene segnalato "da aggiornare".
5. **Ciclo chiuso.** Reminder automatici +7/+14/+30 giorni ai non rispondenti; task operatore automatico a scadenza −6 mesi; dashboard "scadenze senza risposta".
6. **Routing scenari.** Registro la risposta: **A** chiusura/cessazione (se il "no" è del proprietario → segna come lead vendita), **B** rinnovo (al triennio: tacito, registra e basta; al biennio: nuova stipula avviata con task), **C** in trattativa (task operatore + data di rientro). Stop notifiche una volta instradato.

## CRITERI DI ACCETTAZIONE (li verifico io)

- [ ] Creo un contratto di prova con date tali da far scattare T1: la scadenza compare in dashboard con il giorno giusto (controllo il calcolo con te).
- [ ] La bozza email arriva, la modifico, e solo dopo il mio "invia" parte davvero; nel testo c'è la dicitura su raccomandata/PEC.
- [ ] Registro la risposta "in trattativa": il contratto passa allo scenario C con task e data di rientro, e i reminder si fermano.
- [ ] Registro una disdetta inquilino: le notifiche a quel proprietario si fermano.
- [ ] Simulo il cron fermo: il dead man's switch genera l'alert.
- [ ] Invio a un indirizzo finto: il bounce viene registrato e il contatto segnalato da aggiornare.
- [ ] Ti confermo che la richiesta di validazione legale è partita (la faccio io, fuori dal computer).

## ISTRUZIONI OPERATIVE PER ME (utente)

- Comandi: li esegui tu in Code; io leggo la spiegazione di una riga e approvo con un clic solo se mi è chiaro. Password Mac se richiesta: normale, invisibile mentre digito.
- Per SPF/DKIM/DMARC mi guiderai nel pannello del provider del dominio dell'agenzia: ti incollo ciò che vedo.
- Nei test delle email uso solo indirizzi miei o finti, mai clienti veri.
- Non eseguo comandi non spiegati; azioni distruttive solo con mio "sì, procedi".
- Se derivi: "Stop. Rileggi la sezione X di REGOLE.md e rifai seguendola". Sessione lunga → chiusura e sessione nuova con questo stesso prompt.

## CHIUSURA OBBLIGATORIA

(1) Produci il riassunto di chiusura compilando il template a 8 punti del file `07_HANDOFF_TEMPLATE.md` e salvalo come `HANDOFF.md` nella root del repo, sostituendo il vecchio (incluso lo stato della validazione legale nei problemi aperti). (2) Checklist di conformità a `REGOLE.md` in 5 righe. (3) Commit `sprint-4: descrizione breve` + push; mostrami l'ultimo comando git e il suo output (o i passaggi su GitHub Desktop).

==================  FINO A QUI  ==================
---
