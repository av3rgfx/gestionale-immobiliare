# Prompt Sprint S3 — Privacy + Backup

> **Come usarlo:** apri una sessione **NUOVA** in **Code** (sezione di Claude Desktop) sulla cartella del repository. Incolla prima la **frase rituale di apertura** (file `02`, sezione C), aspetta il riassunto in 5 righe, poi incolla **tutto** il blocco qui sotto, da `INCOLLA DA QUI` a `FINO A QUI`. Non continuare in una sessione vecchia: una task per sessione.
> **Prerequisito:** Sprint S2 chiuso. **Questo sprint è il cancello dei dati veri:** finché non è chiuso con tutti i criteri verificati, nel gestionale entrano solo dati finti.

---
==================  INCOLLA DA QUI  ==================

**RITUALE DI APERTURA (obbligatorio, prima di tutto):** leggi `REGOLE.md` nella root del repo e riassumilo in 5 righe prima di toccare codice. Poi leggi `HANDOFF.md` (riassunto dell'ultima sessione) e questi riferimenti nel repo: `04_ARCHITETTURA.md` (per questo sprint: §8, e §3.7 per il RecordConsenso), `03_DECISIONI_CONSIGLIO.md` (registro ADR: fonte vincolante, in caso di conflitto vincono gli ADR) e `05_ROADMAP_SPRINT.md` (sezione S3). Conferma in 3 righe cosa hai capito e da che punto ripartiamo. Solo dopo inizia.

## CONTESTO

Gestionale locale per agenzia immobiliare + JARVIS (S6). Stack: FastAPI + SQLite (WAL) + docxtpl + LibreOffice + PDF.js. Regole fisse (non negoziabili): il consenso privacy è un record immutabile (soggetto, data, versione del modulo, hash, timestamp); al cambio informativa i consensi pregressi scadono e il sistema impone la ri-firma; il backup si fa SOLO con `sqlite3 .backup` (mai copia dei file del database aperto: produce backup corrotti) + copia offsite cifrata + test di ripristino + alert. Regola d'oro: *un backup mai ripristinato non è un backup*. Io non sono uno sviluppatore: un passo alla volta, comandi spiegati in una riga.

## OBIETTIVO DELLO SPRINT S3

Il consenso privacy è generato, firmato, scansionato e tracciato come record immutabile; i dati sono protetti da backup automatici, offsite e verificati. Da qui in poi si possono inserire dati veri.

## AMBITO

**Entra:** informativa auto-compilata e stampa; import scansione firmata con un click; record consenso immutabile; scadenza consensi al cambio informativa con ri-firma obbligatoria; allegato automatico informativa alle pratiche; backup schedulato + offsite cifrato + restore test mensile guidato + alert.
**NON entra:** firma OTP (Fase 2); conservazione sostitutiva a norma con valore probatorio (verifica legale esterna, resta aperta e va segnalata nell'handoff). Non previsto → parcheggio Fase 2 e mi avvisi.

## TASK ORDINATI

1. **Informativa auto-compilata.** Template informativa privacy (gestito come template del modulo documentale, quindi con ciclo di vita depositata) compilato automaticamente con i dati del soggetto; stampa diretta dall'app.
2. **Import scansione firmata un-click.** Dalla scheda del soggetto: carico la scansione dell'informativa firmata, il sistema la associa al soggetto e archivia il file in `~/Gestionale/documenti/`.
3. **Record consenso immutabile.** Alla scansione si crea il RecordConsenso (§3.7): soggetto, data, versione del modulo informativa, hash SHA-256 del file, timestamp, stato valido/scaduto. Non modificabile dall'app; visibile dalla scheda soggetto.
4. **Cambio informativa.** Quando una nuova versione dell'informativa viene depositata, i consensi legati a versioni precedenti passano a "scaduto" e la scheda del soggetto segnala "ri-firma richiesta" finché non carico la nuova scansione.
5. **Allegato automatico.** Il pacchetto pratica include sempre l'informativa nella versione depositata corrente.
6. **Backup schedulato.** Lo script `backup.sh` (S0) viene schedulato (launchd/cron) con frequenza che decidiamo; copia offsite cifrata (decidiamo insieme la destinazione: disco esterno o cloud cifrato — deve stare fuori dall'edificio).
7. **Restore test mensile guidato.** Un task guidato nell'app (o checklist stampabile) che ogni mese mi fa ripristinare il backup su una copia di prova e registra l'esito (data, esito).
8. **Alert.** Notifica evidente se il backup fallisce o il disco si sta riempiendo; fammi simulare un fallimento per vederlo.

## CRITERI DI ACCETTAZIONE (li verifico io)

- [ ] Genero l'informativa di un soggetto di prova: arriva compilata con i suoi dati e la stampo.
- [ ] Carico la scansione firmata con un click: vedo il record consenso con data, versione e hash.
- [ ] Simulo il deposito di una nuova informativa: il consenso vecchio risulta scaduto e l'app chiede la ri-firma.
- [ ] Il backup parte da solo all'orario previsto; lo trovo nella destinazione offsite.
- [ ] Eseguo il restore test guidato: il database ripristinato si apre e contiene i dati.
- [ ] Simulo un backup fallito (come mi indichi tu): vedo l'alert.
- [ ] La destinazione offsite è fuori dall'edificio (lo confermo io).

## ISTRUZIONI OPERATIVE PER ME (utente)

- Comandi: li esegui tu in Code; io leggo la spiegazione di una riga e approvo con un clic solo se mi è chiaro. Password Mac se richiesta: normale, invisibile mentre digito.
- La destinazione offsite la decido io con il tuo consiglio (ti dirò cosa ho disponibile: disco esterno, servizio cloud…).
- Non eseguo comandi non spiegati; azioni distruttive solo con mio "sì, procedi".
- Se derivi: "Stop. Rileggi la sezione X di REGOLE.md e rifai seguendola". Sessione lunga → chiusura e sessione nuova con questo stesso prompt.

## CHIUSURA OBBLIGATORIA

(1) Produci il riassunto di chiusura compilando il template a 8 punti del file `07_HANDOFF_TEMPLATE.md` e salvalo come `HANDOFF.md` nella root del repo, sostituendo il vecchio. (2) Checklist di conformità a `REGOLE.md` in 5 righe. (3) Commit `sprint-3: descrizione breve` + push; mostrami l'ultimo comando git e il suo output (o i passaggi su GitHub Desktop). (4) Ricordami in chiusura: **da qui in poi posso inserire dati veri**, e di segnare in calendario il restore test mensile.

==================  FINO A QUI  ==================
---
