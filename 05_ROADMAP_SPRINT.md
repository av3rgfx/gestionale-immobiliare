# 05 — Roadmap Sprint — Gestionale Immobiliare + JARVIS

**Stato:** approvata. **Fonte:** verdetti dei consigli C1–C6 e brief R1/R2 (`08_VERBALI_CONSIGLI/`), registro decisioni in `03_DECISIONI_CONSIGLIO.md`.

## Come si legge questa roadmap

- Gli sprint si fanno **in ordine, uno alla volta**. Ogni sprint corrisponde a un prompt in `06_PROMPT_SPRINT/` e tipicamente a più sessioni di lavoro.
- I **criteri di done** sono scritti per essere verificati da un non-sviluppatore: se non riesci a verificarli tu, lo sprint non è finito.
- La colonna "Cosa NON entra" è importante quanto quella "Cosa entra": tutto ciò che non è previsto va nel **parcheggio Fase 2**, senza eccezioni.

## Ambienti di lavoro (decisione ADR-47, ex ADR-13)

| Sprint | Ambiente |
|---|---|
| Sessione 1 + S0, S1, S3, S4, S5, S7, S8 | **Code** (sezione di Claude Desktop), sulla cartella del repository |
| S2 e S6 | **Code**, con una deviazione guidata in **Claude Design** per disegnare il prototipo delle schermate, farlo validare da chi userà il gestionale, e poi implementarlo in Code tramite handoff. Il prompt di sprint ti guida passo passo. **Attenzione (ADR-50)**: per la chat JARVIS di S6 il validatore del prototipo è il **Proprietario** (la chat è solo sua), non segretaria/agenti. |
| S9 e S10 (Fase 2, dopo il go-live) | **Code**; per le schermate nuove («Cose da ricordare», «Automazioni», coda «Da approvare») vale la stessa deviazione in **Claude Design** di S2/S6. |
| S-Mob (mobile, pre-go-live) e S11 (Chiamata JARVIS, Fase 3) | **Code**; la resa mobile responsive e la UI della modalità Chiamata seguono la stessa deviazione in **Claude Design** di S2/S6 (per la Chiamata il validatore è il **Proprietario**). Decisioni: ADR-55…63 (verbale C9). |

La sezione **Progetti** di Claude Desktop non si usa in nessuno sprint.

## Regole della roadmap (non negoziabili)

1. **Prima il gestionale senza AI.** JARVIS arriva allo sprint S6, prima in sola lettura.
2. **Backup attivo prima di qualsiasi dato vero:** bozza dello script in S0, sistema completo (schedulazione launchd + offsite + restore test + alert) in S3. Fino ad allora, solo dati finti.
3. **Mai dati reali dei clienti verso API cloud** in sviluppo: solo dati sintetici o anonimizzati.
4. **Astrazione provider LLM fin da S0** (`base_url`/`model` configurabili): il passaggio cloud → Ollama locale (S8) deve essere un cambio di configurazione.
5. **Eval suite dal S0** (su cloud). Prima esecuzione sul **modello locale** = criterio di done di **S6**, ripetuta in S7 e S8 (ADR-48); il **Mac Mini M4 con Ollama va acquistato e configurato prima dell'inizio di S6**. Se l'eval locale fallisce, S7 non parte: si cambia modello, non architettura.
6. **Verifiche esterne obbligatorie** (vedi sotto) corrono *in parallelo* agli sprint, non dopo.

### Verifiche esterne obbligatorie (fuori dal codice, da calendarizzare)

| Verifica | Da fare entro | Chi |
|---|---|---|
| Test su 5–10 modelli reali depositati in Camera di Commercio (conversione, font, dry-run, confronto stampa) | durante S2 | agenzia + Claude |
| Validazione legale delle due scadenze l. 431/98 (doppio trigger) | durante S4, prima del go-live del modulo | consulente legale |
| Validazione legale dei template da un professionista + nominare un responsabile aggiornamento normativo | durante S2 | consulente legale |
| Verifica soglie AML con il consulente antiriciclaggio dell'agenzia | durante S5 | consulente AML |
| Assemblare il corpus di 50+ documenti reali (CI, CIE, passaporti, APE di almeno 3 regioni) | prima di S7 | agenzia |
| Verifica esistenza del modello locale scelto (nome esatto, pesi, benchmark) | prima di S6 | con Claude |
| Acquisto e configurazione del Mac Mini M4 con Ollama (ADR-48) | prima di S6 | agenzia |
| DPIA ex art. 35 GDPR in due tempi: **bozza prima di S3**, aggiornamento prima di S7, chiusura formale in S8 (verbale C7) | da S3 in poi | con Claude + eventuale consulente privacy |
| Conferma retention differenziata immagini documenti (ADR-49) | durante S5 | consulente AML |
| Addendum DPIA per la memoria personale (ADR-51) | prima di S9 | con Claude + eventuale consulente privacy |
| Addendum DPIA + informativa per il trattamento email (ADR-54) | prima di S10 | con Claude + eventuale consulente privacy |
| DPA Tailscale sottoscritto + registro dei trattamenti aggiornato per i metadati del control-plane (ADR-56) | prima di S-Mob in produzione | agenzia + con Claude |
| DPIA "leggera" (art. 35) su voce + accesso remoto + AI (ADR-59/60) | prima di S11 | con Claude + eventuale consulente privacy |
| Verifica licenza della voce TTS adottata + uso server-side GPL-3.0 non distribuito (ADR-61) | prima di S11 | con Claude + eventuale legale |
| Parere art. 173 CdS / responsabilità civile per la policy d'uso alla guida (ADR-59) | prima di S11 | consulente legale |

---

## S0 — Fondamenta

**Obiettivo (una riga):** il cantiere è pronto: repo, regole, ambiente di sviluppo, astrazione AI, eval suite e bozza backup.

**Cosa entra:**
- Repo GitHub inizializzato, `REGOLE.md` scritto/approvato + `CLAUDE.md` che ci punta (doppia fonte, vedi file `02` sezione A).
- Ambiente dev sul MacBook: Homebrew, Python, LibreOffice, font Liberation, virtualenv, dipendenze base.
- Cartella dati `~/Gestionale/` con la struttura completa di `04_ARCHITETTURA.md` §2 (`db.sqlite`, `templates/`, `documenti/`, `backup/`, `logs/`).
- Astrazione provider LLM (SDK OpenAI con `base_url` e `model` da configurazione) + test di connessione al provider cloud.
- Skeleton eval suite: cartella `evals/` con primi casi di test in italiano e script che produce un report.
- Bozza script di backup con `sqlite3 .backup` + copia su destinazione offsite (manuale, non ancora schedulato).

**Cosa NON entra:** nessuna funzione del gestionale (CRUD, UI, template); nessun backup schedulato (arriva in S3); nessun modello locale.

**Criteri di done (verificabili da te):**
- [ ] Apri GitHub nel browser e vedi il repo con i file della harness (00–08 e `06_PROMPT_SPRINT/`), `REGOLE.md`, `CLAUDE.md` e `HANDOFF.md`.
- [ ] Apri `REGOLE.md` nel repo: è quello che hai approvato; `CLAUDE.md` esiste e rimanda a `REGOLE.md`.
- [ ] Lanci il comando di test connessione AI che ti dà Claude e vedi una risposta del modello.
- [ ] Lanci la eval suite e vedi un report con esito per ogni caso di test.
- [ ] Lanci lo script di backup e trovi il file di backup dove previsto; Claude ti guida a ripristinarlo su una copia di prova e la copia si apre.

**Rischi principali:** versioni incoerenti sul MacBook 2019 (Homebrew/Python); attrito iniziale che scoraggia (mitigato: un passo alla volta, niente fretta); tentazione di iniziare subito il gestionale saltando le fondamenta.

---

## S1 — Core gestionale

**Obiettivo (una riga):** l'app esiste: login con ruoli, audit log, e si gestiscono soggetti e immobili con il presidio APE sulle pratiche.

**Cosa entra:**
- Scaffold FastAPI + SQLite in modalità WAL; tabelle iniziali dal modello dati di `04_ARCHITETTURA.md` §3.
- Login con 4 ruoli: Proprietario, Admin, Agente, Segretaria (permessi differenziati).
- Audit log immutabile: chi, cosa, quando, su quale record.
- CRUD soggetti (persone fisiche e giuridiche) con validazione codice fiscale (check digit).
- CRUD immobili con dati catastali e APE associata; **presidio APE** (verbale C7): la pratica si può creare anche senza APE, ma APE mancante/scaduta = **compito bloccante ben visibile** sulla pratica + **blocco della generazione dei documenti che la richiedono** (ADR-21); esenzione registrabile con motivo.
- Convenzione **migrazioni di schema** attiva da subito: script SQL numerati nel repo + backup automatico prima di ogni migrazione (04 §8.3).
- UI semplice: liste, form, messaggi di errore in italiano chiaro.

**Cosa NON entra:** generazione documenti (S2), privacy (S3), scadenze (S4), movimenti (S5), AI (S6).

**Criteri di done:**
- [ ] Apri l'app nel browser, fai login come Agente e come Segretaria: vedi menu diversi.
- [ ] Crei un soggetto con codice fiscale sbagliato: l'app lo rifiuta con un messaggio comprensibile.
- [ ] Crei un soggetto corretto, chiudi e riapri: è ancora nella lista.
- [ ] Crei un immobile senza APE e apri una pratica: compare il compito bloccante "APE mancante" e, se provi a generare un documento che la richiede, l'app blocca e spiega perché.
- [ ] Chiedi a Claude di mostrarti l'audit log: vedi le operazioni che hai appena fatto, con data e utente.

**Rischi principali:** scope creep verso documenti/scadenze ("già che ci siamo…"); UI troppo ricca; permessi dei ruoli da definire con l'agenzia prima di codificarli.

---

## S2 — Modulo documentale

**Obiettivo (una riga):** dai dati escono documenti fedeli ai modelli depositati in Camera di Commercio, con ciclo di vita controllato dei template.

**Cosa entra:**
- **Prototipo in Claude Design (prima del codice UI):** le schermate del modulo documentale (lista template, ciclo di vita, anteprima PDF, generazione pacchetto) vengono prima disegnate in Claude Design seguendo la checklist Design di `REGOLE.md`, fatte provare a segretaria/agenti, corrette col loro feedback, e solo poi implementate in Code.
- Ciclo di vita template: bozza → depositata → ritirata; hash SHA-256; lock sulle depositate; approvazione per ruolo.
- Import `.doc`/`.odt` → conversione una tantum in `.docx` → nasce **bozza da approvare**.
- Dry-run al salvataggio: segnaposti irrisolti e font mancanti segnalati in italiano semplice, con dati finti.
- Rendering on-demand dai dati canonici (**nessuna cascata**); generazione bloccata con elenco campi mancanti.
- Tasto "Genera pacchetto pratica" con moduli condizionali (es. mutuo solo se previsto).
- Anteprima = PDF generato e archiviato alla creazione dell'istanza (PDF.js); correzione dato → rigenerazione esplicita come nuova istanza; pratiche in corso legate alla versione di nascita.
- Test di validazione sui 5–10 modelli reali depositati in CdC: conversione PDF, controllo font, confronto stampa/anteprima.

**Cosa NON entra:** firme digitali/OTP (Fase 2); conservazione a norma con valore probatorio (verifica legale esterna); PDF come template (mai).

**Criteri di done:**
- [ ] Carichi un modello Word reale dell'agenzia, lo approvi: passa a "depositata" e vedi il suo hash; provi a modificarlo: il sistema blocca.
- [ ] Generi un documento da una pratica di prova, vedi l'anteprima PDF, lo stampi: stampa e anteprima coincidono.
- [ ] Togli un dato obbligatorio dalla pratica e rigeneri: il sistema blocca ed elenca i campi mancanti.
- [ ] "Genera pacchetto pratica" produce tutti i documenti previsti, e quelli condizionali solo se servono.
- [ ] Modifichi un template: nasce una nuova versione; una pratica vecchia continua a usare la sua versione originale.

**Rischi principali:** fedeltà dei font (mitigato: Liberation + test sui modelli reali **prima** di scrivere altro codice; se fallisce, si correggono i template, non il motore); artefatti della conversione `.doc`/`.odt`; deposito CdC da rinnovare a ogni modifica (il promemoria automatico arriva in S5).

---

## S3 — Privacy + Backup

**Obiettivo (una riga):** il consenso privacy è gestito e tracciato come record immutabile, e i dati sono al sicuro con backup verificati. **Da qui in poi si possono inserire dati veri.**

**Cosa entra:**
- Informativa privacy auto-compilata dai dati del soggetto; stampa; import della scansione firmata con un click (associazione al soggetto).
- Record consenso immutabile: soggetto, data, versione del modulo, hash, timestamp.
- Cambio informativa → consensi pregressi marcati **scaduti** → ri-firma obbligatoria.
- Allegato automatico dell'informativa alle pratiche (l'informativa è un Template della pipeline documentale — 04 §5).
- Backup: script S0 su schedulazione (launchd) + copia offsite cifrata + **test di ripristino mensile guidato** + alert se il backup fallisce o il disco si riempie.
- **Presidi sui dati reali, prima che entrino** (verbale C7): FileVault attivo sulla macchina che ospita `~/Gestionale/` (verifica guidata), verifica che la copia offsite sia cifrata davvero, accessi alle scansioni dei consensi tracciati in AuditLog.
- **Bozza DPIA** (art. 35) predisposta prima dell'inserimento dei primi dati veri (la chiusura formale resta in S8).
- **Import guidato dei dati esistenti** dell'agenzia (CSV: anagrafiche, immobili, contratti in corso), con responsabile e verifica.

**Cosa NON entra:** firma OTP (Fase 2); conservazione sostitutiva con valore probatorio (verifica legale esterna).

**Criteri di done:**
- [ ] Generi l'informativa di un soggetto di prova: arriva compilata con i suoi dati.
- [ ] Carichi la scansione firmata: vedi il record consenso con data, versione e hash.
- [ ] Simuli un cambio informativa: il consenso vecchio risulta scaduto e l'app chiede la ri-firma.
- [ ] Il backup parte da solo all'ora prevista; lo vedi nella destinazione offsite.
- [ ] Fai il test di ripristino guidato: il database ripristinato su una copia si apre e contiene i dati.
- [ ] Simuli un backup fallito (Claude ti dice come): arriva l'alert.
- [ ] FileVault risulta attivo e la copia offsite è cifrata (verifica guidata).
- [ ] I contratti veri in corso sono nel sistema (import completato) **prima dell'inizio di S4**.

**Rischi principali:** scansioni caricate nel posto sbagliato (mitigato: import un-click legato al soggetto); test di ripristino saltato per pigrizia (mitigato: è un task guidato con data); copia offsite nello stesso edificio (va verificato dove "abita" la destinazione).

---

## S4 — Scadenze locazioni

**Obiettivo (una riga):** il sistema avvisa per tempo sui 3+2 con doppio trigger, invia email su conferma umana e chiude il ciclo fino alla risposta.

**Cosa entra:**
- Modello dati a **doppio trigger**: T1 fine triennio −7 mesi (disdetta vs rinnovo tacito), T2 fine biennio −6 mesi ("nuova stipula"); date dalla **proroga effettiva**; campi disdetta anticipata di inquilino e proprietario; disdetta inquilino registrata → stop notifiche.
- Cron idempotente con retry + **dead man's switch** (alert se il job non gira).
- Bozze email generate dall'AI tramite provider configurato (in dev: cloud, solo dati sintetici nei test), **modificabili, invio solo su conferma umana**.
- SMTP con SPF/DKIM/DMARC + gestione bounce (email non valida → contatto segnalato da aggiornare).
- Ciclo chiuso: reminder +7/+14/+30 ai non rispondenti; task operatore automatico a scadenza −6 mesi; dashboard "scadenze senza risposta".
- Routing tre scenari: **A** chiusura/cessazione (il "no" del proprietario diventa lead vendita), **B** rinnovo (al triennio: tacito, registra e basta; al biennio: nuova stipula avviata), **C** in trattativa (task operatore + data di rientro).
- Dicitura obbligatoria nel messaggio e nel gestionale: l'email raccoglie intenzioni, la disdetta formale resta raccomandata AR/PEC.

**Cosa NON entra:** parsing AI delle risposte (Fase 2); tracking aperture e scoring (Fase 2, subordinati a GDPR); WhatsApp/SMS (Fase 2); messa in produzione del modulo senza la validazione legale l. 431/98.

**Criteri di done:**
- [ ] Crei un contratto di prova con date tali da far scattare T1: la scadenza compare in dashboard con il giorno giusto.
- [ ] La bozza email arriva, la modifichi, e solo dopo il tuo "invia" parte davvero.
- [ ] Registri la risposta "in trattativa": il contratto passa allo scenario C con task e data di rientro.
- [ ] Registri una disdetta inquilino: le notifiche a quel proprietario si fermano.
- [ ] Claude simula il job schedulato fermo: il dead man's switch genera l'alert.
- [ ] Mandi un'email a un indirizzo finto: il bounce viene registrato e il contatto segnalato.

**Rischi principali:** il vizio legale sul trigger (mitigato: validazione l. 431/98 **in parallelo**, il modulo non va in produzione senza via libera); deliverability (SPF/DKIM/DMARC non opzionali); date sbagliate in anagrafica (fine biennio dalla proroga effettiva, non dall'inizio contratto).

---

## S5 — Proprietario & Contabilità operativa

**Obiettivo (una riga):** alla firma nascono da soli i movimenti; il Proprietario vede gli incassi; il commercialista riceve un CSV pulito.

**Cosa entra:**
- Tabella movimenti unica (pratica, tipo, importo, stato, data, agente) con **generazione automatica alla firma** (provvigione, canone di gestione).
- Stati previsto/fatturato/incassato; acconti, storni e note di credito come stati della stessa riga.
- Dashboard Proprietario: incassi per mese/anno/tipologia/agente; margine per agente visibile **solo al Proprietario**.
- Export CSV categorizzato per il commercialista (allineato alle sue categorie: va concordato con lui).
- Scadenziario RLI a T+30 dalla registrazione del contratto **nel sistema**.
- Alert **bloccante** su pagamento in contante ≥ 5.000 €; soglia 1.000 € configurabile etichettata "policy interna".
- Promemoria deposito/ri-deposito formulari Camera di Commercio a ogni modifica dei modelli; disclaimer "adempimento non verificabile dal software"; conservazione 10 anni.
- **Adeguata verifica AML come task bloccante all'apertura pratica** (verbale C7): spunta con operatore e data, traccia in audit, conservazione 10 anni — non una semplice dicitura. Etichetta: "Adeguata verifica al conferimento dell'incarico" (nessuna soglia).
- **Audit delle consultazioni delle etichette compliance** (ADR-45): chi vide quale etichetta, quando, con quale versione della norma.

**Cosa NON entra:** prima nota, IVA, fatture elettroniche, cespiti (restano al commercialista); spese (Fase 2: import in sola lettura); marketing "correttezza normativa garantita" (mai).

**Criteri di done:**
- [ ] Firmi (simuli) un contratto di prova: i movimenti provvigione/canone compaiono da soli con gli importi giusti.
- [ ] Registri un acconto e uno storno: lo stato della riga cambia e i totali tornano.
- [ ] Apri la dashboard come Proprietario: vedi incassi per mese e per agente, margini compresi; come Agente, i margini non ci sono.
- [ ] Esporti il CSV e lo apri in Excel/Numbers: colonne categorizzate e totali corretti.
- [ ] Registri un pagamento in contante da 5.500 €: il sistema blocca. Da 1.200 €: avvisa citando la "policy interna", non la legge.
- [ ] Apri una nuova pratica: compare il task bloccante di adeguata verifica, e finché non lo spunti la pratica lo segnala.
- [ ] Modifichi un template: compare il promemoria di ri-deposito in Camera di Commercio.

**Rischi principali:** registro che diverge dai libri del commercialista (mitigato: riconciliazione mensile guidata in S8); aspettativa "mi fa anche la contabilità" (da chiarire subito: è contabilità operativa); categorie CSV non concordate col commercialista.

---

## S6 — JARVIS v1

**Obiettivo (una riga):** JARVIS risponde in italiano leggendo il gestionale, propone azioni che l'umano approva con diff, e impara solo skill approvate.

**Cosa entra:**
- **Prototipo in Claude Design (prima del codice UI):** la schermata della chat JARVIS e del pannello approvazioni (diff prima/dopo) viene prima disegnata in Claude Design seguendo la checklist Design di `REGOLE.md`, fatta provare a segretaria/agenti, e solo poi implementata in Code.
- Chat nell'app con risposte in italiano, **riservata al ruolo Proprietario** (permesso di ruolo — ADR-50); la coda «Da approvare» è una schermata separata visibile per ruolo.
- Tool **read-only** sul DB: elenco chiuso di funzioni deterministiche (cerca soggetto, elenca scadenze, stato pratica…) con validazione di ogni campo.
- Switch provider da configurazione (cloud in dev ↔ locale), nessun endpoint fissato nel codice. **Prerequisito di sprint: Mac Mini M4 acquistato e configurato con Ollama (ADR-48)** — senza, S6 non si chiude.
- HITL con sostanza: ogni scrittura proposta mostra un **diff leggibile** dei dati chiave; conferma esplicita; tutto in audit log.
- Libreria skill Markdown: JARVIS può **proporre** skill; attivazione solo con approvazione umana + commit Git; nessuna skill auto-attiva; **mai codice generato**.
- Eval suite italiana eseguita su cloud **e sul modello locale** (prima esecuzione locale = criterio di done — ADR-48); report archiviati.

**Cosa NON entra:** scrittura libera di JARVIS sul DB (solo tramite funzioni deterministiche approvate); skill auto-attive; nuove capacità oltre i tool approvati (Fase 2: estensione scrittura).

**Criteri di done:**
- [ ] Chiedi "quali pratiche scadono questo mese?": la risposta corrisponde a ciò che vedi nella dashboard.
- [ ] Chiedi a JARVIS di modificare un dato: vedi il diff prima/dopo e nulla cambia finché non approvi; l'approvazione finisce nell'audit log.
- [ ] JARVIS propone una skill: resta "in attesa" finché non la approvi; prima dell'approvazione non ha effetto.
- [ ] Cambi provider nella configurazione e la chat continua a funzionare senza toccare codice.
- [ ] Lanci la eval suite: report con esiti per caso, archiviato nel repo.
- [ ] La eval suite gira anche **sul modello locale** (Ollama sul Mac Mini) e il report è archiviato; se fallisce, S7 non parte: si cambia modello, non architettura (ADR-48).
- [ ] Demo perimetrata al Proprietario + pagina **«cosa NON fa JARVIS»** approvata per iscritto (mitigazione del gap di aspettative — verbale C8).

**Rischi principali:** rubber-stamping ("approvo senza leggere" — mitigato: diff sostanziali, non un pulsante); tool-calling instabile su modelli locali (mitigato: verifica esistenza/benchmark del modello prima; provider cloud in dev); prompt injection (mitigato: elenco chiuso di tool, niente codice generato).

---

## S7 — OCR & Adempimenti

**Obiettivo (una riga):** documenti e APE entrano nel gestionale con estrazione verificata e adempimenti a etichette parlanti, con l'umano che conferma campo per campo.

**Cosa entra:**
- Parser MRZ ICAO 9303 con **checksum bloccante** per CIE e passaporti.
- Cross-check codice fiscale: ricalcolo deterministico da nome/cognome/nascita + check digit; mismatch → blocco e revisione.
- Estrazione APE da PDF nativi: testo diretto (PyMuPDF/pdfplumber), whitelist layout regionali, validazione di dominio (classe A4–G, valori plausibili); layout sconosciuto → **coda di revisione umana**, mai mapping silenzioso.
- Bake-off PaddleOCR-VL su **50+ documenti reali** (CI, CIE, passaporti, APE di almeno 3 regioni); criterio di kill: errore >2% sui campi anagrafici → fallback al vision LLM principale, decisione chiusa senza terzo round.
- Form anti-automation-bias: split-screen estratto/immagine, conferma **campo per campo**, salvataggio bloccato se checksum/check digit falliscono, evidenziazione solo dei campi a bassa confidenza, log di ogni correzione.
- Matrice adempimenti con etichette parlanti: "Comunicazione Questura entro 48h — ospiti extra-UE" (art. 7 D.Lgs 286/98); "Comunicazione Alloggiati Web entro 24h — locazione turistica, tutti gli ospiti" (TULPS 109); art. 12 DL 59/78 gestito in silenzio (assorbito dalla registrazione AdE) con tooltip; **nazionalità mancante → il sistema chiede, mai skip**.
- **Retention immagini costruita dentro la pipeline** (ADR-49): immagini a sola estrazione cancellate; copie AML conservate 10 anni cifrate e ad accesso loggato. **Nessun documento d'identità reale entra prima di questi presidi.**
- **Verifica autenticità APE come flusso manuale guidato**: task "verifica su SIAPE/registro regionale" con esito in `stato_verifica` e traccia in audit (integrazione automatica coi registri: Fase 2).
- **Aggiornamento DPIA** prima dello sprint (copre anche la base giuridica del corpus del bake-off).
- **Prova del form campo-per-campo con un utente reale** (segretaria/agente) prima di dichiarare chiuso lo sprint.
- Riesecuzione eval suite sul modello locale (ADR-48).

**Cosa NON entra:** GLM-OCR (mai); scoring energetico o altri riusi dei dati oltre lo scopo (bocciato, GDPR); verifica automatica autenticità APE su registri regionali dove non disponibile (resta controllo manuale).

**Criteri di done:**
- [ ] Carichi la scansione di una CIE di prova: i dati vengono estratti e tu li confermi campo per campo guardando l'immagine a fianco.
- [ ] Un codice fiscale incoerente blocca il salvataggio con spiegazione chiara.
- [ ] Carichi un APE di una regione in whitelist: i dati escono compilati; un APE di layout sconosciuto finisce in coda revisione senza dati inventati.
- [ ] Vedi il report del bake-off con la percentuale di errore e la decisione (PaddleOCR-VL tenuto o fallback).
- [ ] Su una pratica con ospite extra-UE compare il compito "Comunicazione Questura entro 48h"; su una locazione turistica compare Alloggiati Web per tutti gli ospiti; se la nazionalità manca, l'app la chiede.

**Rischi principali:** corpus di documenti reali difficile da raccogliere (privacy: solo con consenso o anonimizzati); automation bias degli operatori (la frizione del form è voluta, non va "resa comoda"); errori residui OCR su documenti fotografati male.

---

## S-Mob — Versione mobile (PWA) e accesso remoto Tailscale *(pre-go-live)*

**Obiettivo (una riga):** dal telefono del Proprietario si usa il gestionale ovunque, in sicurezza, tramite Tailscale — stessa app, resa responsive e installabile.

> **Collocazione:** dopo S7 e **prima del go-live S8** (decisione utente + Consiglio C9). Il setup HTTPS via `tailscale cert`/`serve` è **prerequisito** e va anticipato (serve anche a PWA e microfono). Riferimenti: ADR-55, ADR-56, ADR-57, ADR-58; architettura §10.

**Cosa entra:**
- **Prototipo in Claude Design (prima del codice UI):** adattamento responsive delle schermate chiave sul telefono (liste, form, dashboard, anteprima), seguendo la checklist Design di `REGOLE.md` (una azione primaria per schermata, target touch ≥44px).
- CSS responsive sui template esistenti + **manifest PWA** installabile; service worker che cachea **solo asset statici**, mai dati clienti. Nessuna app nativa.
- **HTTPS via `tailscale cert`/`serve`** (tailnet-only); app in bind solo su `localhost` + `100.x`.
- **Hardening tailnet:** ACL default-deny (solo il nodo-telefono del Proprietario → porta HTTPS), device approval, Tailnet Lock, MFA, key expiry; Funnel/exit-node/port-forwarding vietati.
- **Login + ruoli sopra la VPN** (essere sul tailnet non basta); **audit di ogni accesso remoto** con identità del nodo + alert su nodo nuovo.
- **Runbook telefono perso/rubato** scritto e **provato una volta** (revoca nodo, invalidazione sessioni, rotazione password, verifica audit; art. 33 GDPR 72h).
- Accorgimenti mobile: PDF con bottone "Apri/Scarica" nativo accanto a PDF.js; upload foto documenti con fotocamera nativa (`input file capture`) + ricompressione server-side; tabelle in scroll orizzontale nel contenitore.

**Cosa NON entra:** app nativa iOS/Android (mai); **modalità Chiamata vocale** (è S11, Fase 3); dati clienti persistiti sul telefono; Web Push (al più opzionale, payload generico — ADR-62); esposizione del Mac a Internet pubblico.

**Criteri di done (verificabili da te):**
- [ ] Dal tuo telefono connesso a Tailscale apri l'app e fai login: funziona come da desktop, leggibile a una mano.
- [ ] Da un telefono/dispositivo **non autorizzato** sul tailnet non raggiungi nulla (ACL default-deny).
- [ ] Installi l'app come icona sulla home (PWA) e si apre a schermo intero.
- [ ] Generi un documento e lo apri/scarichi dal telefono; carichi la foto di un documento dalla fotocamera.
- [ ] Provi il runbook furto: revochi il nodo dalla console Tailscale e da quel telefono non entri più; le sessioni risultano invalidate.

**Rischi principali:** dipendenza dal control-plane Tailscale (mitigato: deroga dichiarata ADR-56 + DPA + Headscale come exit documentata); PDF.js pesante su file grandi (mitigato: bottone nativo); microfono iOS capriccioso (rimandato a S11, che lo verifica); tentazione di aprire porte sul router (vietato: solo Tailscale).

---

## S8 — Hardening & Go-live

**Obiettivo (una riga):** il sistema è sicuro, ripristinabile, documentato, e va in produzione sul Mac Mini M4 con l'AI locale.

**Cosa entra:**
- **Chiusura formale della DPIA** (bozza da S3, aggiornata in S7); verifica finale di retention immagini (ADR-49), cifratura dati e backup, accessi loggati.
- **Riconciliazione mensile guidata** registro ↔ banca/commercialista (task con checklist).
- Monitoraggio e alert: backup, disco pieno, dead man's switch, bounce email.
- Packaging: avvio automatico con launchd; script di installazione/aggiornamento.
- Migrazione sul Mac Mini M4: installazione, **ripristino da backup**, consolidamento del provider Ollama locale (attivo dal S6 — ADR-48), **riesecuzione eval suite sul modello locale**.
- Documentazione utente semplice in italiano + **manuale di ripristino disastro** (per chi erediterà il sistema).
- Collaudo finale con checklist go-live.

**Cosa NON entra:** tutto il parcheggio Fase 2; ottimizzazioni non richieste dai test.

**Criteri di done:**
- [ ] Riavvii il Mac Mini: l'app riparte da sola e fai login senza toccare il Terminale.
- [ ] Simuli il disastro seguendo il manuale (Mac di riserva o cartella pulita): ripristini dal backup offsite e ritrovi i dati.
- [ ] La eval suite gira sul modello locale e il report è archiviato nel repo.
- [ ] Una persona non tecnica segue la documentazione utente e riesce a creare una pratica e generare un documento senza chiedere aiuto.
- [ ] Completi la prima riconciliazione mensile guidata: registro e banca quadrano (o le differenze sono elencate).
- [ ] La checklist go-live è tutta spuntata e firmata (DPIA compresa).

**Rischi principali:** hardware single point of failure (mitigato: backup offsite + manuale ripristino provato); modello locale diverso dalle aspettative (mitigato: eval locale prima del go-live, provider cloud resta configurabile come ripiego temporaneo solo se compatibile con la privacy — dati reali mai in cloud); documentazione scritta "da tecnico" (mitigato: test su persona non tecnica come criterio di done).

---

## S9 — JARVIS personale *(Fase 2 — dopo il go-live)*

**Obiettivo (una riga):** JARVIS diventa l'assistente personale del Proprietario: ricorda ciò che gli viene dettato ed esegue automazioni approvate.

**Prerequisiti:** go-live di S8 completato; **addendum DPIA** per la memoria personale (verifica esterna).

**Cosa entra:**
- Memoria **«Cose da ricordare»** (ADR-51): salvataggio solo su conferma («Vuoi che ricordi: X?»), ricerca ibrida, pulsanti «Ricorda questo» / «Dimentica» (cancellazione fisica) / «Correggi», aggancio ai Soggetti per i ricordi su terzi, lista sempre consultabile.
- **Motore automazioni interno** (ADR-53): entità Automazione, frase QUANDO/SE/ALLORA, prova a vuoto sullo storico, nasce disattivata, conferma esplicita, anti-tempesta, tutto in AuditLog. Azioni v1: crea Task, notifica a destinatari fissi.
- Coda **«Da approvare»** con approvatore unico per tipo di azione (ADR-50).
- **Lotto 1 di automazioni pre-costruite** (solo dati già nel DB): digest mattutino dei task, promemoria adeguamento ISTAT, alert canoni non incassati, report settimanale incassi, scadenze certificazioni (APE/caldaia); rassegna settimanale pratiche se resta tempo.

**Cosa NON entra:** trigger email (S10); estrazione automatica di ricordi da email/documenti (**mai** — ADR-51); contatore di richieste ripetute per le Procedure (Parcheggio); nuovi tool di scrittura (Parcheggio, poi S10).

**Criteri di done:**
- [ ] Detti a JARVIS un'informazione: propone «Vuoi che ricordi: X?»; dopo la conferma la ritrovi facendogli una domanda in italiano.
- [ ] «Dimentica» cancella davvero il testo del ricordo (verifica guidata sul DB).
- [ ] Chiedi un'automazione in chat: nasce spenta, vedi la frase QUANDO/SE/ALLORA e la prova a vuoto sullo storico; si attiva solo dopo la tua conferma.
- [ ] Il digest mattutino arriva con i task del giorno; una regola che supera il limite giornaliero si autosospende con avviso.
- [ ] Ogni esecuzione di automazione è nell'audit log.

**Rischi principali:** gap di aspettative "Jarvis di Iron Man" (mitigato: pagina «cosa NON fa JARVIS» firmata a fine S6); qualità dell'estrazione del modello locale (mitigato: conferma umana su ogni ricordo); fatica da notifiche (mitigato: digest unico di default).

---

## S10 — Trigger email *(Fase 2)*

**Obiettivo (una riga):** le automazioni possono reagire alle email del Proprietario, in sicurezza e senza che nulla lasci il Mac.

**Prerequisiti:** S9 in produzione **senza incidenti per almeno un ciclo**; **addendum DPIA + informativa** sul trattamento email (verifica esterna).

**Cosa entra:**
- Modulo **IMAP in polling** dallo scheduler esistente, **solo mittenti in allowlist** (ADR-54); credenziali solo in **Keychain** (casella dedicata o app password revocabile, procedura di revoca nel manuale).
- Automazione **watchlist clienti**: riassunto locale delle email dei mittenti scelti, con banner «contenuto non verificato» e link non cliccabili; retention riassunti ≤ 30 giorni.
- Eventuali **primi tool di scrittura aggiuntivi** dal Parcheggio: uno alla volta, ciascuno con mini-ADR (ADR-50).

**Cosa NON entra:** azioni automatiche derivate dal contenuto delle email (tutto ripassa da approvazione umana — ADR-54); lettura di caselle diverse da quella del Proprietario; risposta automatica alle email.

**Criteri di done:**
- [ ] Un'email da un mittente in watchlist genera la notifica col riassunto; una da mittente fuori lista non genera nulla.
- [ ] Un'email "trappola" con istruzioni nascoste (test guidato da Claude) produce solo un riassunto innocuo con il banner: nessuna azione, nessun destinatario nuovo.
- [ ] Revochi la app password seguendo la procedura del manuale: il modulo si ferma con un avviso chiaro, senza errori a cascata.

**Rischi principali:** prompt injection via email (mitigato: difese architetturali ADR-54 — la sintesi non può causare azioni); la casella email diventa il segreto di maggior valore sul Mac (mitigato: Keychain, casella dedicata, revoca provata).

---

## S11 — Modalità Chiamata JARVIS *(Fase 3)*

**Obiettivo (una riga):** JARVIS parla e ascolta a mani libere (uso alla guida), ma resta bocca e orecchie: a voce solo domande e dettatura di proposte in coda; ogni scrittura si approva col diff **a video, da fermi**.

**Prerequisiti:** go-live S8 e S-Mob in produzione; S9/S10 completati; **walking skeleton di misura superato** (latenza end-to-end su 4G reale/DERP e RAM a regime ≤ **4 s/turno**); **pagina «cosa NON fa JARVIS» aggiornata e rifirmata**; verifiche esterne C9 evase (DPIA leggera, licenza voce TTS, retention trascrizioni, parere art. 173 CdS). Riferimenti: ADR-59, ADR-60, ADR-61, ADR-63; architettura §4.8 e §10.3/10.4.

**Cosa entra:**
- **Walking skeleton (prima di tutto):** misura reale di latenza e RAM con la pipeline voce accesa; se sopra soglia, si rifirmano le aspettative o si rinuncia.
- **Prototipo in Claude Design:** schermata della Chiamata (orb, waveform, stato push-to-talk, coda proposte), validata dal **Proprietario**.
- **Stack voce locale** (ADR-61): endpoint WebSocket in FastAPI, processi **on-demand**; **whisper.cpp** (STT), **Ollama 27B** già residente, **TTS scelto con demo audio** (`say`/AVSpeech → Piper `it_IT-paola` → Kokoro). Nessun framework, nessun servizio sempre acceso.
- **Half-duplex push-to-talk**, risposte max 2 frasi; **orb/waveform nativi** (AnalyserNode + Canvas + CSS), zero dipendenze.
- **HITL a voce** (ADR-59/60): Q&A read-only + dettatura proposte con **read-back verbale** → coda «Da approvare»; **gate di scrittura nel codice** (token dalla UI dopo il diff, non forgiabile dall'LLM); niente "approva tutto". Trascrizione = **input non fidato**, loggata; **nessun audio persistito**.
- **Eval voce**: casi realistici a voce, report archiviato.

**Cosa NON entra:** esecuzione di scritture a voce (mai); barge-in / full-duplex; wake word / ascolto continuo; autenticazione vocale (art. 9 GDPR); framework di orchestrazione (LiveKit/Pipecat) — solo se il glue custom fallisce alla prova, con nuovo permesso-dipendenze; animazione "cinematografica" oltre l'orb nativo (rifinitura, non requisito).

**Criteri di done (verificabili da te):**
- [ ] In auto (o simulato) chiedi a voce "che scadenze ho questo mese?": la risposta a voce corrisponde a ciò che vedi in dashboard.
- [ ] Detti "prepara una nuova pratica per Mario Rossi…": JARVIS fa il **read-back** dei campi chiave e mette la proposta **in coda**; sul database non cambia nulla.
- [ ] Da fermo apri la coda, vedi il **diff** della proposta e la approvi/rifiuti una per una; l'esito è in audit log.
- [ ] Provi a farle **eseguire** una modifica solo a voce: risponde che l'approvazione va fatta a video, non la esegue.
- [ ] La latenza reale per turno è sotto la soglia concordata; l'orb reagisce alla voce.

**Rischi principali:** latenza su cellulare (mitigato: misura + half-duplex + risposte brevi); RAM al filo col 27B (mitigato: on-demand + misura, anche con bge-m3 di S9 attivo); gap aspettative "Iron Man" (mitigato: pagina firmata, niente full-duplex); **sicurezza stradale** (mitigato: nessuna interazione visiva richiesta in movimento, risposte brevi) — la policy d'uso alla guida è nella pagina «cosa NON fa JARVIS».

---

## Parcheggio — Fase 2 (da non iniziare prima del go-live)

Nessuno di questi punti entra negli sprint S0–S8. La Fase 2 inizia dopo il go-live con gli sprint **S9 e S10** qui sopra; tutto il resto si annota qui e basta.

- **Firma OTP via link** — subordinata a verifica eIDAS.
- **Tracking aperture email** — solo con informativa e consenso GDPR.
- **Parsing AI delle risposte** alle email di scadenza — con base giuridica e DPA col provider.
- **Import spese** in sola lettura dal commercialista.
- **WhatsApp Business** — solo valutando l'API ufficiale (costi/burocrazia); mai API non ufficiali (rischio ban).
- **Estensione scrittura JARVIS** oltre le funzioni deterministiche approvate — un tool alla volta, ciascuno con mini-ADR (ADR-50); primi candidati valutabili in S10.
- **Contatore "richiesta ripetuta N volte"** per proporre Procedure in automatico — si rivaluta dopo la memoria di S9 (ADR-52); non promesso.
- **Automazione "email cliente senza risposta da N giorni"** — tagliata dal consiglio C8 (costo alto, valore medio).
- **Scoring proprietari** — solo con base giuridica solida.
- *(punti da calendario, non da roadmap: documentazione di installazione pubblicabile; scansione vision dell'archivio cartaceo storico.)*
