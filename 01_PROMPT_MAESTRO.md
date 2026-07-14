# 01 — Prompt Maestro (Sessione 1)

## A cosa serve questo file

Questo è il prompt della **prima sessione** di lavoro in **Code** (sezione di Claude Desktop): quella in cui gettiamo le fondamenta del progetto (regole, documenti di progettazione, scaffold Sprint 0). È l'unica sessione che può partire prima che `REGOLE.md` sia nel repo, perché `REGOLE.md` lo sistemiamo proprio qui. Tutte le sessioni successive useranno i prompt in `06_PROMPT_SPRINT/`.

> Prima di questo file leggi `00_LEGGIMI.md`: contiene i passaggi preliminari (account GitHub, repository, GitHub Desktop). Se non li hai ancora fatti, falli prima e poi torna qui.

## Come usarlo (5 minuti)

1. Apri l'app **Claude** e vai nella sezione **Code**.
2. Seleziona come **cartella di lavoro** la cartella del repository `gestionale-immobiliare` (creata seguendo `00_LEGGIMI.md`, Passi 1-2). Autorizza l'accesso alla cartella se richiesto.
3. Incolla la **frase rituale, variante 1 — prima sessione in assoluto** (la trovi nel file `02`, sezione C). Aspetta che Claude riassuma le regole in 5 righe: è la tua verifica che le ha lette.
4. Ora incolla **tutto** il blocco qui sotto, dalla riga `INCOLLA DA QUI` alla riga `FINO A QUI` comprese.
5. Da quel momento segui Claude **un passo alla volta**: non anticipare, non saltare.

## Regole d'oro per te (utente)

- Sei in Code: Claude legge e scrive i file da solo e ti propone i comandi da approvare con un clic. **Leggi sempre cosa sta per fare prima di approvare**: se un comando non ti è chiaro, chiedi "spiegamelo in una riga" prima di dare l'ok.
- Non approvare mai un comando che Claude non ti ha spiegato in una riga.
- Se Claude propone un'azione distruttiva (cancellare, sovrascrivere, resettare), approva solo se sei sicuro.
- Se Claude deriva (inventa funzioni, cambia argomento, complica), scrivi: `Stop. Rileggi la sezione 2 di REGOLE.md e rifai seguendola` (il numero è la sezione violata: 1 Disciplina, 2 Semplicità, 3 Consiglio ridotto, 4 Design).

---
==================  INCOLLA DA QUI  ==================

Ciao Claude. Hai già letto le regole fisse: da questa sessione sei il mio **senior software architect e lead developer** per un progetto reale che deve arrivare in produzione. Rispondi **sempre in italiano**. Io non sono uno sviluppatore professionista: guidami un passo alla volta e spiega **ogni comando in una riga** prima di chiedermi di approvarlo. Prima di ogni azione distruttiva (cancellare, sovrascrivere, resettare) chiedimi conferma esplicita. Una cosa alla volta: non passare al punto successivo finché il precedente non è fatto e verificato.

## IL PROGETTO

Sto costruendo il **gestionale di una piccola agenzia immobiliare italiana** (la mia), più un agente AI locale chiamato **JARVIS**. Il sistema sostituisce completamente il cartaceo: anagrafiche, immobili, pratiche, documenti, scadenze, privacy, contabilità operativa. Deve essere **"a prova di stupido"**: lo useranno segretaria e agenti senza competenze tecniche.

- È una **webapp locale**: gira sul Mac dell'agenzia e si usa dal browser dei computer dell'ufficio. In produzione nessun dato lascia l'ufficio.
- **Produzione:** Mac Mini M4 sempre acceso. **Sviluppo:** MacBook Pro 2019 (Intel) con Claude Desktop, in sessioni separate. In sviluppo le API AI cloud si usano **solo con dati sintetici o anonimizzati, mai con dati reali dei clienti**.
- **Repo GitHub** come unica fonte di verità: codice, regole e documenti di progettazione vivono lì. I file di riferimento del progetto (la "harness") sono già stati copiati nel repo: `00_LEGGIMI.md`, `01_PROMPT_MAESTRO.md`, `02_REGOLE_FISSE_SKILLS.md`, `03_DECISIONI_CONSIGLIO.md` (registro ADR), `04_ARCHITETTURA.md` (architettura e modello dati), `05_ROADMAP_SPRINT.md`, `06_PROMPT_SPRINT/`, `07_HANDOFF_TEMPLATE.md`, `08_VERBALI_CONSIGLI/`.
- **Ambiente di lavoro**: lavoriamo in **Code** (questa sezione), sempre su questa cartella. I prototipi di interfaccia, quando serviranno (sprint S2 e S6), li disegneremo in **Claude Design** e poi li implementeremo qui.

## DECISIONI NON NEGOZIABILI (già validate da 10 consigli tecnici, C1–C10 — si applicano, non si ridiscutono)

Il registro completo è `03_DECISIONI_CONSIGLIO.md` (ADR) e la loro applicazione tecnica è `04_ARCHITETTURA.md`: in caso di dubbio o conflitto, **vincono gli ADR**. Sintesi:

1. **Stack:** FastAPI + SQLite in modalità WAL + docxtpl (template DOCX) + LibreOffice headless (conversione PDF) + PDF.js (anteprima). Font Liberation installati sul Mac. Tutti i dati in un'unica cartella `~/Gestionale/`. Niente tecnologie esotiche.
2. **Cuore deterministico:** i documenti legali escono da template versionati riempiti dal codice. L'AI è solo "bocca e orecchie" (capisce l'italiano, propone bozze), **mai** autrice di testo legale né di logica di calcolo.
3. **Prima il gestionale senza AI.** JARVIS arriva dopo, prima in sola lettura sul database.
4. **Niente auto-skill in codice:** JARVIS non genera mai codice eseguibile. Può proporre "skill" in formato Markdown, attivabili **solo** con mia approvazione esplicita e versionamento Git.
5. **Backup prima dei dati veri:** `sqlite3 .backup` schedulato (MAI copia della cartella con il database aperto: produce backup corrotti) + copia offsite cifrata + test di ripristino mensile + alert. Regola: *un backup mai ripristinato non è un backup*.
6. **Ruoli e audit log:** login con 4 ruoli (Proprietario, Admin, Agente, Segretaria), permessi per ruolo, registro **immutabile** di chi approva cosa, quando, con quale versione di template e di modello AI.
7. **Human-in-the-loop con sostanza:** ogni azione di scrittura mostra un **diff leggibile** dei dati chiave prima dell'approvazione (non un semplice pulsante "Approva"); conferma esplicita obbligatoria per email e documenti ufficiali.
8. **Modulo documentale senza cascata:** ogni documento è una proiezione on-demand dei dati canonici e della versione di template approvata. Template con ciclo di vita **bozza → depositata → ritirata**, hash SHA-256, blocco modifica sulle depositate, approvazione per ruolo. Anteprima = PDF generato e **archiviato** alla creazione del documento (ciò che vedi è ciò che stampi). Generazione **bloccata** se mancano dati, con elenco dei campi vuoti. Il PDF non è mai un template. Import `.doc`/`.odt` consentito ma convertito una tantum in `.docx` e nasce come bozza da approvare. I modelli vanno depositati presso la **Camera di Commercio**, e il deposito va rinnovato a ogni modifica.
9. **Privacy:** flusso genera → stampa → firma → scansiona. La scansione firmata è un **record immutabile di consenso** (soggetto, data, versione del modulo, hash, timestamp). Al cambio dell'informativa, i consensi pregressi sono marcati **scaduti** e il sistema impone la ri-firma.
10. **Scadenze locazioni 3+2 (doppio trigger):** T1 = fine triennio **meno 7 mesi** (il proprietario decide: disdetta con raccomandata/PEC entro 6 mesi, oppure rinnovo tacito del +2); T2 = fine biennio **meno 6 mesi** (è una **nuova stipula**, NON un preavviso: il contratto cessa e si rinegozia). Date calcolate dalla proroga effettiva. Le disdette dell'inquilino vanno registrate nel modello dati e fermano le notifiche. Tre scenari: A chiusura/cessazione, B rinnovo, C in trattativa. Ciclo chiuso obbligatorio: reminder +7/+14/+30 giorni, task operatore, cron idempotente con retry, dead man's switch sul job, dashboard "scadenze senza risposta", configurazione SPF/DKIM/DMARC e gestione bounce. L'email **raccoglie intenzioni, non produce effetti legali** (va scritto nel messaggio). Validazione legale (l. 431/98) con consulente in parallelo allo sviluppo, prima della produzione. In v1: niente parsing AI delle risposte, niente tracking aperture, niente scoring.
11. **OCR deterministic-first:** **NO GLM-OCR** (l'italiano non è supportato). APE in PDF nativo → estrazione testo diretta + whitelist dei layout + coda di revisione umana; CIE e passaporti → parser MRZ ICAO 9303 + checksum bloccante; OCR vero (PaddleOCR-VL) solo per il residuo, dopo bake-off su 50+ documenti reali con criterio di kill: errori >2% sui campi anagrafici → fallback al vision LLM principale. Cross-check codice fiscale con ricalcolo deterministico + check digit. Form anti-automation-bias: conferma campo per campo, mai un "Conferma" cieco. Matrice adempimenti con **etichette parlanti** ("Comunicazione Questura entro 48h — ospiti extra-UE"; "Comunicazione Alloggiati Web entro 24h — locazione turistica, tutti gli ospiti"); nazionalità mancante → il sistema chiede, mai skip silenzioso.
12. **Contabilità operativa, non fiscale:** il gestionale è il record operativo, il commercialista resta il record tributario. I movimenti (provvigioni, canoni di gestione) nascono **automaticamente alla firma del contratto**, con stati previsto/fatturato/incassato più acconti, storni e note di credito. Niente prima nota, IVA, fatture elettroniche, cespiti. Export CSV per il commercialista. Scadenziario RLI a T+30 dalla registrazione nel sistema. Dashboard Proprietario solo sugli incassi; il margine per agente è visibile **solo al Proprietario**. Alert **bloccante** sul contante a 5.000 €; la soglia di 1.000 € è una "policy interna" configurabile, mai etichettata come obbligo di legge. Diciture corrette ovunque: "Deposito formulari presso la Camera di Commercio", "Adeguata verifica al conferimento dell'incarico" (nessuna soglia). Conservazione documentale 10 anni. Disclaimer strutturale: "adempimento non verificabile dal software".
13. **Metodo di lavoro:** è il `REGOLE.md` a 4 sezioni (Disciplina, Semplicità, Consiglio ridotto, Design) che hai già letto all'apertura della sessione. Una task per sessione; ogni sessione si apre con il rituale e si chiude con l'handoff. Il consiglio completo (skill llm-council) gira nativamente qui in Code: usalo ai checkpoint fissi definiti nel file `02`, con advisor davvero paralleli e peer review anonima.
14. **Privacy in sviluppo:** MAI dati reali dei clienti verso API cloud — solo dati sintetici o anonimizzati.
15. **AI locale:** prima di progettare su un modello, verifica che esista davvero (nome esatto, pesi, benchmark — il nome "Gemma 4 26B-A4B" non risulta nelle release note pubbliche; alternativa pari merito Qwen 27B Q4). L'astrazione del provider (SDK OpenAI con `base_url` e `model` configurabili) c'è fin dal primo giorno, così il passaggio cloud → Ollama locale è un cambio di configurazione, non di codice. La eval suite viene rieseguita sul modello locale.

## COMPITO DI QUESTA SESSIONE (Fondamenta)

In quest'ordine, un passo alla volta, chiedendomi conferma a ogni passo:

1. **Verifica del repo GitHub.** Il repo `gestionale-immobiliare` dovrebbe già esistere sul Mac e su GitHub con i file della harness (l'ho creato seguendo `00_LEGGIMI.md`). Guidami a verificare che ci siano tutti i file (00–08, incluse le cartelle `06_PROMPT_SPRINT/` e `08_VERBALI_CONSIGLI/`) e che il push funzioni. Se manca qualcosa, completiamolo prima di proseguire.
2. **`REGOLE.md` — doppia fonte.** Se `REGOLE.md` non è ancora nel repo: scrivine la bozza partendo dal BLOCCO REGOLE approvato nel file `02_REGOLE_FISSE_SKILLS.md` (massimo 60 righe, 4 sezioni: Disciplina, Semplicità, Consiglio ridotto, Design), mostramela, io la approvo, poi commit `sprint-0: regole fisse del progetto`. Crea anche `CLAUDE.md` nella root con il contenuto indicato nel file `02` (sezione A): è il file che Code legge in automatico a ogni avvio, e rimanda a `REGOLE.md`. Se `REGOLE.md` esiste già: verifica che esista anche `CLAUDE.md` e che i due siano coerenti.
3. **Documenti di progettazione (verifica e raffinamento).** (a) `03_DECISIONI_CONSIGLIO.md` contiene il registro ADR completo dei 10 consigli (ADR-01…ADR-70): **verifica la coerenza incrociata** con `04_ARCHITETTURA.md` — ogni ADR citato nel file 04 deve trovare la sua definizione nel file 03 e viceversa; segnalami qualsiasi buco o contraddizione. (b) Rileggi `04_ARCHITETTURA.md` e `05_ROADMAP_SPRINT.md` e segnalami eventuali incongruenze o punti da raffinare: nessuna modifica senza mia approvazione. (c) Se in futuro serviranno altri documenti, li creeremo nel repo con nomi chiari.
4. **Scaffold Sprint 0** secondo la sezione S0 di `05_ROADMAP_SPRINT.md`: ambiente di sviluppo (Homebrew, Python, LibreOffice, font Liberation, virtualenv, dipendenze base), cartella dati `~/Gestionale/` con la struttura di `04_ARCHITETTURA.md` §2, astrazione provider LLM con `base_url`/`model` configurabili + test di connessione al provider cloud di sviluppo, skeleton della eval suite (cartella `evals/` con casi di test in italiano e script che produce un report), bozza dello script di backup con `sqlite3 .backup`.
5. **Chiusura obbligatoria:** produci il riassunto di chiusura compilando il template a 8 punti del file `07_HANDOFF_TEMPLATE.md` e salvalo come `HANDOFF.md` nella root del repo (ne esiste sempre uno solo: sostituisce il vecchio). Poi commit con messaggio nel formato `sprint-0: descrizione breve` e push su GitHub. Mostrami l'ultimo comando git e il suo output.

## REGOLE DI CONDOTTA DELLA SESSIONE

- Una cosa alla volta, in ordine; niente salti.
- Ogni comando in un blocco, con una riga di spiegazione in italiano semplice prima di chiedermi l'approvazione.
- Chiedi conferma prima di ogni azione distruttiva.
- Se un comando fallisce, fermati: leggi l'errore con me e proponi UNA correzione alla volta.
- Se ti chiedo qualcosa che contraddice le decisioni non negoziabili, segnalamelo invece di eseguire.
- Non inventare funzionalità: se serve qualcosa non previsto, segnalalo e lo mettiamo nel parcheggio Fase 2 della roadmap.

Inizia dal punto 1. Prima di tutto, in 5 righe, dimmi cosa hai capito del progetto e qual è il piano di questa sessione.

==================  FINO A QUI  ==================
---

## Dopo questa sessione

Quando la sessione 1 è chiusa (con `HANDOFF.md` e commit fatti), il lavoro continua con i prompt in `06_PROMPT_SPRINT/`, in ordine: `S0_fondamenta.md` (verifica e completa lo scaffold iniziato qui), poi `S1_core_gestionale.md` e così via, seguendo `05_ROADMAP_SPRINT.md`. Ogni prompt va incollato in una **sessione nuova di Code** sulla stessa cartella, dopo la frase rituale di apertura (file `02`, sezione C).
