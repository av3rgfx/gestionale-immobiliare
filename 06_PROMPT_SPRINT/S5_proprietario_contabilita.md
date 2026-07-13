# Prompt Sprint S5 — Proprietario & Contabilità operativa

> **Come usarlo:** apri una sessione **NUOVA** in **Code** (sezione di Claude Desktop) sulla cartella del repository. Incolla prima la **frase rituale di apertura** (file `02`, sezione C), aspetta il riassunto in 5 righe, poi incolla **tutto** il blocco qui sotto, da `INCOLLA DA QUI` a `FINO A QUI`. Non continuare in una sessione vecchia: una task per sessione.
> **Prerequisito:** Sprint S4 chiuso. **Azione tua fuori dal computer:** chiedi al commercialista quali categorie vuole nell'export CSV, e al consulente AML la conferma dell'interpretazione delle soglie.

---
==================  INCOLLA DA QUI  ==================

**RITUALE DI APERTURA (obbligatorio, prima di tutto):** leggi `REGOLE.md` nella root del repo e riassumilo in 5 righe prima di toccare codice. Poi leggi `HANDOFF.md` (riassunto dell'ultima sessione) e questi riferimenti nel repo: `04_ARCHITETTURA.md` (per questo sprint: §3.8 Movimento e §9 Matrice compliance), `03_DECISIONI_CONSIGLIO.md` (registro ADR: fonte vincolante, in caso di conflitto vincono gli ADR) e `05_ROADMAP_SPRINT.md` (sezione S5). Conferma in 3 righe cosa hai capito e da che punto ripartiamo. Solo dopo inizia.

## CONTESTO

Gestionale locale per agenzia immobiliare + JARVIS (S6). Stack: FastAPI + SQLite (WAL). Regole fisse (dal verdetto del consiglio C6, non negoziabili): il gestionale è il record **operativo**, il commercialista resta il record **tributario** — niente prima nota, IVA, fatture elettroniche, cespiti; i movimenti nascono **automaticamente alla firma del contratto**; dashboard Proprietario solo sugli incassi, margine per agente visibile **solo al Proprietario**; alert **bloccante** sul contante a 5.000 €; la soglia 1.000 € è "policy interna" configurabile, mai presentata come obbligo di legge; diciture corrette: "Deposito formulari presso la Camera di Commercio" (da rinnovare a ogni modifica dei modelli) e "Adeguata verifica al conferimento dell'incarico" (nessuna soglia); conservazione documentale 10 anni; disclaimer strutturale "adempimento non verificabile dal software". Io non sono uno sviluppatore: un passo alla volta, comandi spiegati in una riga.

## OBIETTIVO DELLO SPRINT S5

Alla firma di un contratto i movimenti si generano da soli; il Proprietario vede gli incassi in dashboard; il commercialista riceve un export CSV pulito; gli alert di compliance sono a posto con le diciture corrette.

## AMBITO

**Entra:** tabella movimenti unica con auto-generazione alla firma; stati previsto/fatturato/incassato + acconti/storni/note di credito; dashboard Proprietario; export CSV commercialista; scadenziario RLI T+30; alert contante e policy interna; promemoria deposito Camera di Commercio; diciture e disclaimer.
**NON entra:** contabilità fiscale di qualsiasi tipo; spese (Fase 2: import in sola lettura); messaggi che promettono "correttezza normativa garantita". Non previsto → parcheggio Fase 2 e mi avvisi.

## TASK ORDINATI

1. **Tabella movimenti unica.** Come da `04_ARCHITETTURA.md` §3.8: pratica, tipo (provvigione, canone di gestione), importo, data scadenza, agente, origine (evento generatore). Generazione **automatica alla firma del contratto**: nessun inserimento manuale per i movimenti standard. Fammi firmare un contratto di prova e vedere le righe nascere.
2. **Stati e rettifiche.** Stati previsto → fatturato → incassato; acconti, storni e note di credito come stati/eventi della stessa riga (mai righe inserite a mano). Totali sempre coerenti.
3. **Dashboard Proprietario.** Incassi per mese/anno/tipologia/agente; il margine per agente è visibile **solo** al ruolo Proprietario (verifico loggando come Agente: non lo vedo).
4. **Export CSV commercialista.** Export categorizzato secondo le categorie che il commercialista mi ha indicato (te le detto io); apertura pulita in Excel/Numbers.
5. **Scadenziario RLI.** Scadenza registrazione contratto a T+30 giorni dalla registrazione **nel sistema** (T+0), visibile in dashboard/scadenziario.
6. **Alert contante e policy.** Pagamento in contante ≥ 5.000 €: **bloccante**. Soglia 1.000 €: avviso configurabile etichettato "policy interna" (mai "obbligo di legge"). Le soglie sono parametri configurabili e versionati.
7. **Compliance e diciture.** Promemoria automatico di deposito/ri-deposito formulari presso la Camera di Commercio a ogni modifica dei modelli; dicitura "Adeguata verifica al conferimento dell'incarico" nel flusso incarico; disclaimer "adempimento non verificabile dal software" dove compaiono scadenze e alert normativi (testo come da `04_ARCHITETTURA.md` §9); conservazione documentale 10 anni impostata come regola di retention.

## CRITERI DI ACCETTAZIONE (li verifico io)

- [ ] Firmo (simulo) un contratto di prova: provvigione e canone compaiono da soli con gli importi giusti.
- [ ] Registro un acconto e uno storno: lo stato della riga cambia e i totali tornano.
- [ ] Come Proprietario vedo incassi per mese e per agente, margini compresi; come Agente i margini non ci sono.
- [ ] Esporto il CSV e lo apro in Excel/Numbers: colonne categorizzate e totali corretti.
- [ ] Registro un pagamento in contante da 5.500 €: bloccato. Da 1.200 €: avviso che parla di "policy interna", non di legge.
- [ ] Modifico un template: compare il promemoria di ri-deposito in Camera di Commercio.
- [ ] In nessuna schermata leggo diciture sbagliate (es. "deposito AdE" al posto di Camera di Commercio, o la soglia 1.000 € spacciata per legge).

## ISTRUZIONI OPERATIVE PER ME (utente)

- Comandi: li esegui tu in Code; io leggo la spiegazione di una riga e approvo con un clic solo se mi è chiaro. Password Mac se richiesta: normale, invisibile mentre digito.
- Le categorie per l'export CSV me le ha date il commercialista: te le detto quando arriviamo al task 4.
- Non eseguo comandi non spiegati; azioni distruttive solo con mio "sì, procedi".
- Se derivi: "Stop. Rileggi la sezione X di REGOLE.md e rifai seguendola". Sessione lunga → chiusura e sessione nuova con questo stesso prompt.

## CHIUSURA OBBLIGATORIA

(1) Produci il riassunto di chiusura compilando il template a 8 punti del file `07_HANDOFF_TEMPLATE.md` e salvalo come `HANDOFF.md` nella root del repo, sostituendo il vecchio. (2) Checklist di conformità a `REGOLE.md` in 5 righe. (3) Commit `sprint-5: descrizione breve` + push; mostrami l'ultimo comando git e il suo output (o i passaggi su GitHub Desktop).

==================  FINO A QUI  ==================
---
