# Prompt Sprint S6 — JARVIS v1

> **Come usarlo:** apri una sessione **NUOVA** in **Code** (sezione di Claude Desktop) sulla cartella del repository. Incolla prima la **frase rituale di apertura** (file `02`, sezione C), aspetta il riassunto in 5 righe, poi incolla **tutto** il blocco qui sotto, da `INCOLLA DA QUI` a `FINO A QUI`. Non continuare in una sessione vecchia: una task per sessione.
> **Prerequisito:** Sprint S5 chiuso. Il gestionale senza AI è completo e funzionante: JARVIS si appoggia su fondamenta solide. **Prerequisito ADR-48:** il **Mac Mini M4 con Ollama** è acquistato e configurato PRIMA di iniziare questo sprint, e l'esistenza del modello locale scelto è verificata (nome esatto, pesi, benchmark): la prima esecuzione della eval suite sul modello locale è un criterio di done di S6.

---
==================  INCOLLA DA QUI  ==================

**RITUALE DI APERTURA (obbligatorio, prima di tutto):** leggi `REGOLE.md` nella root del repo e riassumilo in 5 righe prima di toccare codice. Poi leggi `HANDOFF.md` (riassunto dell'ultima sessione) e questi riferimenti nel repo: `04_ARCHITETTURA.md` (per questo sprint: §4, architettura dell'agente), `03_DECISIONI_CONSIGLIO.md` (registro ADR: fonte vincolante, in caso di conflitto vincono gli ADR) e `05_ROADMAP_SPRINT.md` (sezione S6). Conferma in 3 righe cosa hai capito e da che punto ripartiamo. Solo dopo inizia.

## CONTESTO

Gestionale locale per agenzia immobiliare, ora arriva **JARVIS**, l'agente AI locale. Regole fisse (dai consigli C1/C2, non negoziabili): l'AI è solo "bocca e orecchie, mai mani" — capisce l'italiano e propone, **mai** autrice di testo legale né di logica di calcolo; legge il DB tramite tool read-only nei limiti del ruolo di chi interroga, scrive **solo** tramite funzioni deterministiche che validano ogni campo; ogni scrittura richiede diff leggibile + conferma esplicita + audit log; le "skill" sono file Markdown che JARVIS può **proporre**, attivabili solo con mia approvazione e commit Git — nessuna skill auto-attiva, **mai codice generato**; il provider AI si cambia da configurazione (`base_url`/`model`), niente endpoint fissi nel codice; mai dati reali dei clienti verso API cloud. Io non sono uno sviluppatore: un passo alla volta, comandi spiegati in una riga.

## OBIETTIVO DELLO SPRINT S6

JARVIS risponde in italiano leggendo il gestionale, propone azioni che io approvo vedendo il diff, e impara solo skill che io approvo. La qualità è misurata con la eval suite italiana.

## AMBITO

**Entra:** prototipo schermata chat in Claude Design con validazione utenti; chat nell'app; tool read-only con elenco chiuso di funzioni; switch provider da configurazione; HITL con diff + audit; libreria skill Markdown con approvazione; eval suite italiana eseguita e archiviata.
**NON entra:** scrittura libera di JARVIS sul DB; skill auto-attive; nuove capacità oltre i tool approvati (Fase 2); modelli non verificati. Non previsto → parcheggio Fase 2 e mi avvisi.

## TASK ORDINATI

1. **Verifica modello.** Prima di progettare su un modello, verifica con me che esista davvero: nome esatto, pesi, benchmark, licenza (il nome "Gemma 4 26B-A4B" non risulta nelle release note pubbliche; alternative note: Gemma 3 27B, Qwen 27B Q4). In sviluppo si lavora col provider cloud (solo dati sintetici), ma il **Mac Mini M4 con Ollama dev'essere già configurato** (prerequisito ADR-48): la eval suite va eseguita anche sul modello locale entro la fine di questo sprint. Nota tecnica da rispettare: l'API di Ollama non supporta `tool_choice` — il gateway non deve dipendere da quel parametro.
2. **Prototipo schermata chat in Claude Design.** Mi guidi ad aprire **Claude Design** per disegnare il prototipo della schermata chat di JARVIS e del pannello approvazioni (diff prima/dopo, pulsante conferma, stato "skill in attesa"), applicando la checklist Design di `REGOLE.md`. Il validatore del prototipo sono **io, il Proprietario** — la chat è riservata al mio ruolo (ADR-50), non a segretaria/agenti: lo provo io con domande reali ("quali pratiche scadono questo mese?"), iteriamo finché non lo approvo, poi handoff a Code per l'implementazione. Prototipo approvato salvato nel repo.
3. **Chat nell'app.** Interfaccia chat semplice (una domanda, una risposta, cronologia della conversazione) integrata nel gestionale, in italiano, implementata dal prototipo approvato; visibile al **solo ruolo Proprietario** (ADR-50), mentre la coda «Da approvare» è una schermata separata con visibilità per ruolo.
4. **Tool read-only.** Elenco **chiuso** di funzioni deterministiche di lettura che JARVIS può chiamare (cerca soggetto, elenca scadenze del mese, stato pratica, movimenti di una pratica…), che rispettano i permessi del ruolo di chi interroga. Ogni funzione valida i parametri. Niente SQL libero scritto dal modello.
5. **Switch provider.** La chat usa il provider da configurazione; fammi cambiare `base_url`/`model` e verificare che tutto continua a funzionare senza toccare codice.
6. **HITL con sostanza.** Per ogni azione di scrittura che JARVIS propone (solo tramite funzioni approvate, flusso di `04_ARCHITETTURA.md` §4.3): mostrami un **diff leggibile** prima/dopo dei dati chiave, chiedi conferma esplicita, registra tutto nell'audit log (chi ha approvato, quando, quale versione di modello).
7. **Libreria skill Markdown.** JARVIS può proporre una skill come file `.md` (procedura operativa in italiano, es. "come preparare il pacchetto pratica per una locazione turistica"); la proposta resta in stato "in attesa" finché io non la approvo; all'approvazione viene committata in Git. Nessuna skill si attiva da sola. Nessuna skill può contenere né invocare codice.
8. **Eval suite italiana.** Estendi la eval suite di S0 con casi realistici del gestionale (domande tipiche dell'operatività dell'agenzia), eseguila **sia sul provider cloud sia sul modello locale** (Ollama sul Mac Mini — ADR-48), archivia i report nel repo con data e modello usato. Se l'eval locale fallisce, S7 non parte: si cambia modello, non architettura.
9. **LLM-assist alla templatizzazione (condizionale — ADR-69).** Solo se i log di S2 mostrano che lo script deterministico risolve meno dell'85–90% dei campi: aggiungi nel wizard la **pre-selezione del tag** suggerita dall'LLM (l'LLM classifica, il codice scrive — mai il contrario, e mai moduli reali sul cloud — ADR-70). Altrimenti salta questo task e annotalo nell'handoff.
10. **Demo e perimetro (verbale C8).** Prepara una **demo perimetrata** per me (Proprietario) e la pagina **«cosa NON fa JARVIS»**: la rivedo e la approvo per iscritto (mitigazione del gap di aspettative).

## CRITERI DI ACCETTAZIONE (li verifico io)

- [ ] Il prototipo della chat è stato validato e approvato da me (Proprietario, unico utente della chat — ADR-50), ed è salvato nel repo.
- [ ] Chiedo in chat "quali pratiche scadono questo mese?": la risposta corrisponde a ciò che vedo nella dashboard.
- [ ] Chiedo a JARVIS di modificare un dato: vedo il diff prima/dopo e nulla cambia finché non approvo; dopo l'approvazione trovo tutto nell'audit log.
- [ ] JARVIS propone una skill: resta "in attesa" e non ha alcun effetto finché non la approvo io.
- [ ] Cambio provider nella configurazione: la chat continua a funzionare senza modifiche al codice.
- [ ] Lancio la eval suite: report con esito per caso, archiviato nel repo.
- [ ] La eval suite gira anche **sul modello locale** (Ollama sul Mac Mini) e il report è archiviato; se fallisce, S7 non parte: si cambia modello, non architettura (ADR-48).
- [ ] Ho ricevuto la **demo perimetrata** e ho approvato **per iscritto** la pagina «cosa NON fa JARVIS» (verbale C8).
- [ ] Provo a chiedere a JARVIS qualcosa fuori dai suoi tool: risponde che non può, invece di improvvisare.

## ISTRUZIONI OPERATIVE PER ME (utente)

- Comandi: li esegui tu in Code; io leggo la spiegazione di una riga e approvo con un clic solo se mi è chiaro. Password Mac se richiesta: normale, invisibile mentre digito.
- Le domande di test per la eval le scriviamo insieme pensando al lavoro vero dell'agenzia: io porto gli esempi, tu li formalizzi.
- Non eseguo comandi non spiegati; azioni distruttive solo con mio "sì, procedi".
- Se derivi: "Stop. Rileggi la sezione X di REGOLE.md e rifai seguendola". Sessione lunga → chiusura e sessione nuova con questo stesso prompt.

## CHIUSURA OBBLIGATORIA

(1) Produci il riassunto di chiusura compilando il template a 8 punti del file `07_HANDOFF_TEMPLATE.md` e salvalo come `HANDOFF.md` nella root del repo, sostituendo il vecchio (incluso l'esito della verifica modello nelle decisioni). (2) Checklist di conformità a `REGOLE.md` in 5 righe. (3) Commit `sprint-6: descrizione breve` + push; mostrami l'ultimo comando git e il suo output (o i passaggi su GitHub Desktop).

==================  FINO A QUI  ==================
---
