# Prompt Sprint S7 — OCR & Adempimenti

> **Come usarlo:** apri una sessione **NUOVA** in **Code** (sezione di Claude Desktop) sulla cartella del repository. Incolla prima la **frase rituale di apertura** (file `02`, sezione C), aspetta il riassunto in 5 righe, poi incolla **tutto** il blocco qui sotto, da `INCOLLA DA QUI` a `FINO A QUI`. Non continuare in una sessione vecchia: una task per sessione.
> **Prerequisito:** Sprint S6 chiuso. **Materiale da preparare prima:** il corpus di **50+ documenti reali** (CI, CIE, passaporti, APE di almeno 3 regioni), raccolti con consenso o anonimizzati. Se il corpus non è pronto, la prima sessione di questo sprint serve a organizzarlo.

---
==================  INCOLLA DA QUI  ==================

**RITUALE DI APERTURA (obbligatorio, prima di tutto):** leggi `REGOLE.md` nella root del repo e riassumilo in 5 righe prima di toccare codice. Poi leggi `HANDOFF.md` (riassunto dell'ultima sessione) e questi riferimenti nel repo: `04_ARCHITETTURA.md` (per questo sprint: §7, pipeline OCR e adempimenti), `03_DECISIONI_CONSIGLIO.md` (registro ADR: fonte vincolante, in caso di conflitto vincono gli ADR) e `05_ROADMAP_SPRINT.md` (sezione S7). Conferma in 3 righe cosa hai capito e da che punto ripartiamo. Solo dopo inizia.

## CONTESTO

Gestionale locale per agenzia immobiliare + JARVIS. Regole fisse del modulo OCR (dal verdetto del consiglio C5, non negoziabili): **GLM-OCR non si usa** (l'italiano non è tra le lingue supportate); architettura **deterministic-first**: APE in PDF nativo → estrazione testo diretta (niente OCR) con whitelist dei layout e coda di revisione umana per i layout sconosciuti; CIE e passaporti → parser MRZ ICAO 9303 con **checksum bloccante**; OCR vero solo per il residuo (CI senza MRZ, foto) con PaddleOCR-VL, dopo bake-off su 50+ documenti reali con criterio di kill: errori >2% sui campi anagrafici → fallback al vision LLM principale, decisione chiusa; cross-check codice fiscale con ricalcolo deterministico + check digit; form anti-automation-bias (conferma campo per campo, mai un "Conferma" cieco); matrice adempimenti con etichette parlanti; nazionalità mancante → il sistema chiede, mai skip silenzioso. Io non sono uno sviluppatore: un passo alla volta, comandi spiegati in una riga.

## OBIETTIVO DELLO SPRINT S7

Documenti d'identità e APE entrano nel gestionale con dati verificati e confermati dall'operatore campo per campo, e ogni pratica mostra gli adempimenti dovuti in linguaggio semplice.

## AMBITO

**Entra:** parser MRZ + checksum; cross-check CF; estrazione APE da testo nativo con whitelist e coda revisione; bake-off PaddleOCR-VL con criterio di kill; form di conferma anti-automation-bias con log correzioni; matrice adempimenti con etichette parlanti.
**NON entra:** GLM-OCR (mai); riuso dei dati estratti per altri scopi (scoring energetico ecc. — bocciato); verifica automatica di autenticità APE dove il registro regionale non è accessibile (resta controllo manuale, con stato `non_verificabile`). Non previsto → parcheggio Fase 2 e mi avvisi.

## TASK ORDINATI

1. **Corpus e baseline.** Organizziamo il corpus di 50+ documenti reali (io li ho raccolti con consenso/anonimizzati) con la verità attesa per ogni campo (ground truth) in un formato semplice: sarà il metro di misura di tutto lo sprint.
2. **Parser MRZ.** Per CIE e passaporti: lettura MRZ e verifica checksum ICAO 9303 come **gate bloccante**: checksum fallito → niente salvataggio, revisione obbligatoria.
3. **Cross-check codice fiscale.** Ricalcolo deterministico del CF da nome/cognome/data e luogo di nascita + check digit; mismatch tra CF estratto e CF ricalcolato → blocco e revisione.
4. **Estrazione APE.** Da PDF nativi: estrazione testo diretta (PyMuPDF/pdfplumber), whitelist dei layout regionali noti, regex per campo con validazione di dominio (classe energetica A4–G, EPgl,nren numerico plausibile); layout non riconosciuto → coda di revisione umana, **mai** mapping silenzioso. Il blocco APE dell'Immobile registra lo stato verifica autenticità (`verificato_registro` / `da_verificare` / `non_verificabile`).
5. **Bake-off OCR.** PaddleOCR-VL sul corpus per i documenti residui (CI senza MRZ, foto). Misura errore per campo. Criterio di kill: errore >2% sui campi anagrafici → si abbandona PaddleOCR-VL e si usa il vision LLM principale come fallback. Decisione chiusa, niente terzo round. Report nel repo.
6. **Form anti-automation-bias.** Split-screen: dati estratti a sinistra, immagine del documento a destra; conferma **campo per campo**; salvataggio bloccato se checksum MRZ o check digit CF falliscono; evidenziazione solo dei campi a bassa confidenza; ogni correzione dell'operatore viene loggata (è la nostra metrica di accuracy nel tempo).
7. **Matrice adempimenti.** Il sistema risolve internamente tipo pratica × categoria soggetto × registrazione e mostra compiti in linguaggio semplice: "Comunicazione Questura entro 48h — ospiti extra-UE" (art. 7 D.Lgs 286/98); "Comunicazione Alloggiati Web entro 24h — locazione turistica, tutti gli ospiti" (TULPS 109); art. 12 DL 59/78 gestito in silenzio perché assorbito dalla registrazione AdE, con tooltip esplicativo. Se la nazionalità del soggetto manca, il sistema la chiede: mai skip silenzioso.

## CRITERI DI ACCETTAZIONE (li verifico io)

- [ ] Carico la scansione di una CIE di prova: vedo i dati estratti a fianco dell'immagine e li confermo campo per campo.
- [ ] Un codice fiscale incoerente blocca il salvataggio con spiegazione chiara.
- [ ] Carico un APE di regione in whitelist: dati compilati; un APE di layout sconosciuto va in coda revisione senza dati inventati.
- [ ] Vedo il report del bake-off: percentuale di errore per campo e decisione presa (PaddleOCR-VL tenuto oppure fallback).
- [ ] Su una pratica con ospite extra-UE compare "Comunicazione Questura entro 48h"; su una locazione turistica compare Alloggiati Web per tutti gli ospiti; se tolgo la nazionalità da un soggetto, l'app la chiede.
- [ ] Le correzioni che faccio nel form finiscono in un log consultabile.

## ISTRUZIONI OPERATIVE PER ME (utente)

- Comandi: li esegui tu in Code; io leggo la spiegazione di una riga e approvo con un clic solo se mi è chiaro. Password Mac se richiesta: normale, invisibile mentre digito.
- Il corpus documenti lo ho preparato in una cartella: ti indico il percorso quando arriviamo al task 1.
- Il bake-off può richiedere tempo: è normale, mi dici tu quando rilanciare.
- Non eseguo comandi non spiegati; azioni distruttive solo con mio "sì, procedi".
- Se derivi: "Stop. Rileggi la sezione X di REGOLE.md e rifai seguendola". Sessione lunga → chiusura e sessione nuova con questo stesso prompt.

## CHIUSURA OBBLIGATORIA

(1) Produci il riassunto di chiusura compilando il template a 8 punti del file `07_HANDOFF_TEMPLATE.md` e salvalo come `HANDOFF.md` nella root del repo, sostituendo il vecchio (inclusa la decisione del bake-off nelle decisioni). (2) Checklist di conformità a `REGOLE.md` in 5 righe. (3) Commit `sprint-7: descrizione breve` + push; mostrami l'ultimo comando git e il suo output (o i passaggi su GitHub Desktop).

==================  FINO A QUI  ==================
---
