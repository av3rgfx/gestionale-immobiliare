# Prompt Sprint S8 — Hardening & Go-live

> **Come usarlo:** apri una sessione **NUOVA** in **Code** (sezione di Claude Desktop) sulla cartella del repository. Incolla prima la **frase rituale di apertura** (file `02`, sezione C), aspetta il riassunto in 5 righe, poi incolla **tutto** il blocco qui sotto, da `INCOLLA DA QUI` a `FINO A QUI`. Non continuare in una sessione vecchia: una task per sessione.
> **Prerequisito:** Sprint S7 chiuso. È l'ultimo sprint prima della produzione: qui si stringono le viti, non si aggiungono funzioni.

---
==================  INCOLLA DA QUI  ==================

**RITUALE DI APERTURA (obbligatorio, prima di tutto):** leggi `REGOLE.md` nella root del repo e riassumilo in 5 righe prima di toccare codice. Poi leggi `HANDOFF.md` (riassunto dell'ultima sessione) e questi riferimenti nel repo: `04_ARCHITETTURA.md` (per questo sprint: §8 Backup e sicurezza e §4.5 Eval suite), `03_DECISIONI_CONSIGLIO.md` (registro ADR: fonte vincolante, in caso di conflitto vincono gli ADR) e `05_ROADMAP_SPRINT.md` (sezione S8). Conferma in 3 righe cosa hai capito e da che punto ripartiamo. Solo dopo inizia.

## CONTESTO

Gestionale locale per agenzia immobiliare + JARVIS, pronto per andare in produzione sul **Mac Mini M4**. Regole fisse (non negoziabili): DPIA ex art. 35 GDPR prima del go-live; immagini dei documenti cancellate dopo l'estrazione (o retention breve e motivata); dati e backup cifrati; accessi loggati; riconciliazione mensile guidata registro ↔ banca/commercialista; monitoraggio con alert (backup, disco, dead man's switch, bounce); avvio automatico con launchd; in produzione l'AI gira in locale su Ollama, dopo verifica del modello e riesecuzione della eval suite sul modello locale; documentazione utente in italiano semplice e manuale di ripristino disastro per chi erediterà il sistema. Il Mac Mini è un single point of failure: la procedura non può esserlo. Io non sono uno sviluppatore: un passo alla volta, comandi spiegati in una riga.

## OBIETTIVO DELLO SPRINT S8

Il sistema è sicuro, ripristinabile, monitorato e documentato; va in produzione sul Mac Mini M4 con l'AI locale, e chiunque potrà usarlo e ripristinarlo senza di me.

## AMBITO

**Entra:** DPIA e presidi GDPR; retention immagini e cifratura; riconciliazione mensile guidata; monitoraggio e alert; packaging con launchd e script installazione/aggiornamento; migrazione Mac Mini M4 con ripristino da backup e switch a Ollama locale; eval suite sul modello locale; documentazione utente e manuale ripristino disastro; checklist go-live.
**NON entra:** qualsiasi funzione nuova (tutto nel parcheggio Fase 2); ottimizzazioni non richieste dai test. Non previsto → parcheggio Fase 2 e mi avvisi.

## TASK ORDINATI

1. **DPIA e GDPR.** Mi guidi nella stesura della DPIA (art. 35) come documento nel repo (es. `DPIA.md`); impostiamo la retention immagini (cancellazione dopo l'estrazione, o retention breve motivata per iscritto), la cifratura dei dati sensibili e dei backup, e verifichiamo che ogni accesso ai documenti sia loggato.
2. **Riconciliazione mensile guidata.** Task guidato nell'app con checklist: confronto movimenti del gestionale ↔ estratto conto/commercialista, differenze elencate, esito registrato con data.
3. **Monitoraggio e alert.** Pannello unico con stato di: ultimo backup (esito), spazio disco, dead man's switch del cron scadenze, bounce email; alert evidente se qualcosa è rosso. Fammi simulare ognuno dei guasti.
4. **Packaging.** Avvio automatico dell'app all'accensione del Mac con launchd; script di installazione e di aggiornamento documentati; versione dell'app visibile in una schermata.
5. **Migrazione Mac Mini M4.** Installazione da zero sul Mac Mini seguendo la documentazione: ripristino dei dati **dal backup offsite** (prova reale del piano di ripristino), poi switch del provider AI a Ollama locale col modello verificato (nome esatto, pesi, benchmark già verificati in S6).
6. **Eval locale.** Riesecuzione della eval suite italiana **sul modello locale**: report archiviato nel repo accanto a quello cloud, con confronto degli esiti.
7. **Documentazione.** Guida utente in italiano semplice (le 10 operazioni quotidiane con screenshot) e **manuale di ripristino disastro** passo-passo, pensato per chi non mi conosce. Test: una persona non tecnica segue il manuale e riesce a ripristinare/ripartire senza chiedere aiuto.
8. **Checklist go-live.** Lista finale (backup verificato, restore test fatto, DPIA firmata, validazioni legali chiuse, alert provati, eval locale archiviata, documentazione testata): la spuntiamo insieme una voce alla volta.

## CRITERI DI ACCETTAZIONE (li verifico io)

- [ ] Riavvio il Mac Mini: l'app riparte da sola e faccio login senza toccare il Terminale.
- [ ] Simulo il disastro seguendo il manuale (Mac di riserva o cartella pulita): ripristino dal backup offsite e ritrovo i dati.
- [ ] La eval suite gira sul modello locale e il report è nel repo.
- [ ] Una persona non tecnica segue la guida utente e crea una pratica con documento senza chiedere aiuto.
- [ ] Completo la prima riconciliazione mensile guidata: registro e banca quadrano, o le differenze sono elencate.
- [ ] Il pannello monitoraggio mostra tutto verde; simulando un guasto vedo l'alert.
- [ ] La checklist go-live è tutta spuntata.

## ISTRUZIONI OPERATIVE PER ME (utente)

- Comandi: li esegui tu in Code; io leggo la spiegazione di una riga e approvo con un clic solo se mi è chiaro. Password Mac se richiesta: normale, invisibile mentre digito.
- Per il Mac Mini: mi guiderai passo-passo anche nel primo avvio e nella rete dell'ufficio.
- Il test della documentazione su persona non tecnica lo organizzo io (un collega): ti riporto cosa non è riuscito a fare.
- Non eseguo comandi non spiegati; azioni distruttive solo con mio "sì, procedi".
- Se derivi: "Stop. Rileggi la sezione X di REGOLE.md e rifai seguendola". Sessione lunga → chiusura e sessione nuova con questo stesso prompt.

## CHIUSURA OBBLIGATORIA

(1) Produci il riassunto di chiusura compilando il template a 8 punti del file `07_HANDOFF_TEMPLATE.md` e salvalo come `HANDOFF.md` nella root del repo, sostituendo il vecchio (prossimo passo: la manutenzione ordinaria — restore test mensile, riconciliazione mensile, controllo di conformità bisettimanale di `REGOLE.md`). (2) Checklist di conformità a `REGOLE.md` in 5 righe. (3) Commit `sprint-8: go-live` + push; mostrami l'ultimo comando git e il suo output (o i passaggi su GitHub Desktop). (4) Chiudiamo con il riepilogo finale del progetto: cosa abbiamo costruito e cosa resta nel parcheggio Fase 2.

==================  FINO A QUI  ==================
---
