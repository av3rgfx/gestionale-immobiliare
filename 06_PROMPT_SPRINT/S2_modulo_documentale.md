# Prompt Sprint S2 — Modulo documentale

> **Come usarlo:** apri una sessione **NUOVA** in **Code** (sezione di Claude Desktop) sulla cartella del repository. Incolla prima la **frase rituale di apertura** (file `02`, sezione C), aspetta il riassunto in 5 righe, poi incolla **tutto** il blocco qui sotto, da `INCOLLA DA QUI` a `FINO A QUI`. Non continuare in una sessione vecchia: una task per sessione.
> **Prerequisito:** Sprint S1 chiuso (app con login, ruoli, CRUD soggetti/immobili, audit log). Tieni a portata i **5–10 modelli reali** depositati in Camera di Commercio: servono subito.

---
==================  INCOLLA DA QUI  ==================

**RITUALE DI APERTURA (obbligatorio, prima di tutto):** leggi `REGOLE.md` nella root del repo e riassumilo in 5 righe prima di toccare codice. Poi leggi `HANDOFF.md` (riassunto dell'ultima sessione) e questi riferimenti nel repo: `04_ARCHITETTURA.md` (per questo sprint: §5, e §3.5–3.6 per le tabelle Template e IstanzaDocumento), `03_DECISIONI_CONSIGLIO.md` (registro ADR: fonte vincolante, in caso di conflitto vincono gli ADR) e `05_ROADMAP_SPRINT.md` (sezione S2). Conferma in 3 righe cosa hai capito e da che punto ripartiamo. Solo dopo inizia.

## CONTESTO

Gestionale locale per agenzia immobiliare + JARVIS (in S6). Stack: FastAPI + SQLite (WAL) + docxtpl + LibreOffice headless + PDF.js, font Liberation. Regole fisse del modulo documentale (da ADR-14…ADR-22, non negoziabili): nessuna cascata documento-da-documento; ogni documento è rendering on-demand dai dati canonici; template con ciclo di vita bozza/depositata/ritirata + hash SHA-256 + lock + approvazione per ruolo; anteprima = PDF archiviato alla creazione; generazione bloccata se mancano dati; PDF mai come template; import .doc/.odt → conversione una tantum in .docx → bozza da approvare; pratiche in corso legate alla versione di template con cui sono nate. Io non sono uno sviluppatore: un passo alla volta, comandi spiegati in una riga.

## OBIETTIVO DELLO SPRINT S2

Dai dati del gestionale escono documenti fedeli ai modelli depositati in Camera di Commercio, con controllo completo sulle versioni dei template.

## AMBITO

**Entra:** prototipo schermate in Claude Design con validazione utenti; test sui modelli reali; ciclo di vita template completo; import .doc/.odt; dry-run segnaposti/font; rendering on-demand con blocco dati mancanti; "Genera pacchetto pratica" con moduli condizionali; anteprima PDF archiviata con PDF.js; rigenerazione esplicita.
**NON entra:** firme digitali/OTP (Fase 2); conservazione a norma con valore probatorio (verifica legale esterna); privacy (S3). Non previsto → parcheggio Fase 2 e mi avvisi.

## TASK ORDINATI

1. **Test di validazione PRIMA del codice.** Prendo i 5–10 modelli reali depositati in Camera di Commercio. Con il tuo aiuto: conversione DOCX→PDF via LibreOffice, controllo font (Liberation installati), dry-run dei segnaposti con dati finti, confronto stampa/anteprima. Se qualcosa non torna, si correggono i template, **non** il motore. Registriamo l'esito in un documento nel repo (es. `TEST_MODELLI_REALI.md`).
2. **Prototipo schermate in Claude Design.** Mi guidi ad aprire **Claude Design** (sezione di Claude Desktop) per disegnare il prototipo delle schermate di questo modulo (lista template con stati, pagina template con approvazione/lock, generazione documento e pacchetto pratica, anteprima PDF), applicando la checklist Design di `REGOLE.md` (un'azione primaria per schermata, errori in italiano semplice, stati vuoti che guidano). Il prototipo lo faccio vedere a segretaria/agenti: raccolgo i loro commenti e te li riporto. Iteriamo il prototipo finché non lo approvo, poi mi guidi a consegnarlo qui in Code (handoff di Claude Design) e lo implementiamo. Il prototipo approvato resta salvato nel repo come riferimento visivo.
3. **Ciclo di vita template.** Tabella Template come da `04_ARCHITETTURA.md` §3.5: stati bozza → depositata → ritirata, hash SHA-256, blocco modifica sulle depositate, approvazione riservata ai ruoli che decidiamo (proponimela come tabella prima di codificarla), metadati deposito Camera di Commercio.
4. **Import .doc/.odt.** Conversione una tantum in .docx via LibreOffice; il file convertito nasce come **bozza da approvare**, mai come depositata.
5. **Dry-run al salvataggio.** Il salvataggio di un template esegue un rendering con dati finti e segnala segnaposti irrisolti e font mancanti con messaggi in italiano semplice.
6. **Rendering on-demand.** Generazione del documento dai dati canonici della pratica + versione di template depositata; se manca un dato obbligatorio: generazione bloccata con elenco dei campi vuoti. Niente compilazione a partire da altri documenti.
7. **Pacchetto pratica.** Tasto "Genera pacchetto pratica": renderizza tutti i documenti associati alla pratica come istanze, rispettando le condizioni (es. modulo mutuo solo se la pratica prevede mutuo).
8. **Anteprima e istanze.** Alla creazione dell'istanza generi il PDF e lo archivi come artefatto (tabella IstanzaDocumento, §3.6); l'anteprima (PDF.js) mostra quello, mai una riconversione a vista. Correzione di un dato → rigenerazione esplicita con nuova istanza; le pratiche vecchie restano legate alla versione di template con cui sono nate.

## CRITERI DI ACCETTAZIONE (li verifico io)

- [ ] Il test sui modelli reali è documentato nel repo: so quali modelli passano e quali no (e perché).
- [ ] Il prototipo delle schermate è stato approvato da me dopo il feedback di segretaria/agenti, ed è salvato nel repo.
- [ ] Carico un modello Word dell'agenzia, lo approvo: diventa "depositata", vedo l'hash, e se provo a modificarlo il sistema blocca.
- [ ] Genero un documento da una pratica di prova, vedo l'anteprima PDF, stampo: stampa e anteprima coincidono.
- [ ] Tolgo un dato obbligatorio e rigenero: blocco con elenco dei campi mancanti.
- [ ] "Genera pacchetto pratica" produce tutti i documenti previsti; quelli condizionali solo quando servono.
- [ ] Modifico un template: nasce una nuova versione; una pratica creata prima continua a usare la sua versione originale.

## ISTRUZIONI OPERATIVE PER ME (utente)

- Comandi: li esegui tu in Code; io leggo la spiegazione di una riga e approvo con un clic solo se mi è chiaro. Password Mac se richiesta: normale, invisibile mentre digito.
- I modelli reali li fornisco io quando me li chiedi (li ho preparati in una cartella sul Desktop).
- Non eseguo comandi non spiegati; azioni distruttive solo con mio "sì, procedi".
- Se derivi: "Stop. Rileggi la sezione X di REGOLE.md e rifai seguendola". Sessione lunga → chiusura e sessione nuova con questo stesso prompt.

## CHIUSURA OBBLIGATORIA

(1) Produci il riassunto di chiusura compilando il template a 8 punti del file `07_HANDOFF_TEMPLATE.md` e salvalo come `HANDOFF.md` nella root del repo, sostituendo il vecchio. (2) Checklist di conformità a `REGOLE.md` in 5 righe. (3) Commit `sprint-2: descrizione breve` + push; mostrami l'ultimo comando git e il suo output (o i passaggi su GitHub Desktop).

==================  FINO A QUI  ==================
---
