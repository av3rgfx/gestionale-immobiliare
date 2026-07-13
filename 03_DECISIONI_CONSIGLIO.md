# 03 — Registro delle Decisioni del Consiglio (ADR)

**Progetto:** Gestionale Immobiliare + JARVIS — webapp locale per piccola agenzia immobiliare italiana con agente AI locale (Mac Mini M4 in produzione, sviluppo su Claude Desktop, repo GitHub).
**Stato:** Approvato dal Chairman.
**Uso:** questo file è il registro delle decisioni architetturali (ADR — Architecture Decision Records). I prompt di sprint lo citano come fonte vincolante: **nessuno sprint può contraddire un ADR senza aprirne uno nuovo che lo sostituisca esplicitamente.**
**Fonti:** verdetti C1–C6 e brief di ricerca R1/R2 in `08_VERBALI_CONSIGLI/`.

> Convenzione: ogni decisione ha un identificativo **ADR-NN** con numerazione continua su tutti i consigli. Gli ADR sono normativi; le "Alternative scartate" spiegano il perché; i "Punti aperti" elencano verifiche esterne **obbligatorie prima della messa in produzione del modulo interessato**.

---

## Consiglio C1 — Architettura, stack e agente AI

**Posta in gioco:** scegliere lo stack tecnico, definire il confine tra logica deterministica e LLM, e decidere come l'agente JARVIS può agire sul sistema senza compromettere dati e documenti legali.

### Decisioni adottate

- **ADR-01 — Stack "noioso" e tutto locale.** FastAPI + SQLite (modalità WAL) + docxtpl (template DOCX con Jinja2) + LibreOffice headless (conversione PDF) + PDF.js (anteprima). Tutto gira sul Mac Mini M4 di produzione; nessun servizio cloud in produzione.
- **ADR-02 — Cuore deterministico.** I documenti legali escono da template versionati riempiti da codice. L'LLM è solo "bocca e orecchie" (capisce l'intento in italiano), **mai** autore di testo legale né di logica di calcolo.
- **ADR-03 — Sequenza di build: prima il gestionale senza AI.** CRUD + template + PDF coprono già ~il 70% del valore. JARVIS arriva dopo, prima in sola lettura sul DB.
- **ADR-04 — Auto-skill JARVIS = libreria curata, mai codice auto-generato.** JARVIS può *proporre* skill in formato Markdown; ogni skill è attivabile **solo** con approvazione umana esplicita e versionamento Git. Nessuna skill auto-attiva, nessun codice Python generato dall'LLM eseguito sul server.
- **ADR-05 — Sviluppo cloud → produzione locale.** In sviluppo si usano API cloud (provider configurabile via `base_url`/`model`) **esclusivamente con dati sintetici o anonimizzati**; in produzione Ollama locale. La eval suite italiana identica viene rieseguita sul modello locale **dal secondo sprint**, non alla fine. *(La sola clausola temporale della riesecuzione locale è sostituita da ADR-48 — consiglio C7: da S6, con Mac Mini disponibile prima.)*
- **ADR-06 — Backup verificabile.** `sqlite3 .backup` schedulato (cron) + copia offsite cifrata + test di ripristino mensile + alert su backup fallito e disco pieno. Regola: *un backup mai ripristinato non è un backup*.
- **ADR-07 — Human-in-the-loop con sostanza.** Ogni azione di scrittura rilevante mostra un **diff leggibile** dei dati chiave prima dell'approvazione (non un semplice pulsante "Approva"); conferma esplicita obbligatoria per email e documenti ufficiali.
- **ADR-08 — Identità, ruoli, audit log.** Login con ruoli, permessi per ruolo, e registro **immutabile** di chi ha approvato cosa, quando, con quale versione di template e di modello. È obbligo GDPR e unica difesa dal "rubber-stamping".

### Alternative scartate

- **Copia a caldo della cartella dati con SQLite WAL attivo** — produce backup corrotti (file `-wal`/`-shm` incoerenti).
- **Time Machine come unico backup** — stesso edificio del server: nessuna protezione da furto/incendio/disastro locale.
- **Skill come codice Python auto-generato** — prompt injection → esecuzione arbitraria sul server che contiene i dati dei clienti.
- **Skill Markdown auto-attive senza approvazione** — deriva incontrollata del comportamento dell'agente.
- **Installer, benchmark pubblicabile e scansione vision dell'archivio in roadmap iniziale** — ottimizzano il go-to-market prima dell'affidabilità; restano punti da calendario, non da roadmap.

### Punti aperti / verifiche esterne obbligatorie

- ⚠️ **Verifica esistenza modello**: "Gemma 4 26B-A4B" non corrisponde alle release note pubbliche (esiste Gemma 3 27B). Verificare nome esatto, pesi e benchmark **prima** di progettarci sopra; alternativa pari merito Qwen 27B Q4.
- ⚠️ **Validazione legale dei template** da un professionista, con un responsabile nominato per l'aggiornamento normativo nel tempo.
- **Bus factor**: documentazione di funzionamento in italiano semplice per chi erediterà il sistema.

---

## Consiglio C2 — Regole di sviluppo e "skill" su Claude Desktop

**Posta in gioco:** garantire disciplina e continuità di sviluppo in sessioni multiple su Claude Desktop, dove nessuna regola si auto-carica e l'enforcement nativo è debole.

### Decisioni adottate

- **ADR-09 — Un file `REGOLE.md` nella root del repo, massimo 60 righe**, in quattro sezioni: (a) *Disciplina* — prima piano scritto, poi criterio di accettazione, poi codice, poi review; (b) *Semplicità* — 6-8 regole anti-overengineering (niente astrazioni premature, niente feature "per dopo"); (c) *Consiglio ridotto* — prima di ogni decisione architetturale elencare 3 modi in cui fallisce e 1 alternativa più semplice; (d) *Design* — solo la checklist impeccable, unica fonte design.
- **ADR-10 — Doppia fonte.** Le regole vivono in due file nel repository: `REGOLE.md` (testo completo, fonte normativa) e `CLAUDE.md` (file corto che Code legge in automatico a ogni avvio e che ordina di rispettare `REGOLE.md`). Caricamento automatico + verifica leggibile con la frase rituale. *(Aggiornato luglio 2026: la forma originale prevedeva le istruzioni di progetto della sezione Progetti, abbandonata con l'ADR-47, ex "ADR-13 nuovo".)*
- **ADR-11 — Rituale d'apertura e chiusura di sessione.** Apertura fissa: *"Leggi REGOLE.md e riassumilo in 5 righe prima di toccare codice"* (verifica eseguibile anche da chi non legge codice). Chiusura: checklist di conformità leggibile. Una task per chat; se Claude deriva: *"Stop. Rileggi la sezione X e rifai"*.
- **ADR-12 — Handoff obbligatorio tra sessioni.** Rituale di chiusura: riassunto (stato, decisioni prese, prossimo passo) + commit di checkpoint; la sessione successiva apre leggendo `REGOLE.md` e l'ultimo riassunto. Controllo di conformità e revisione versionata del file dopo 2 settimane.
- ~~**ADR-13 — Claude Code: non ora.** L'attrito ucciderebbe il progetto; la struttura repo-first rende la migrazione gratuita. Rivalutare dopo 2 settimane, se le regole reggono.~~ **SOSTITUITO — la decisione sostitutiva è ADR-47 (consiglio C7, luglio 2026).**
- *(Nota di registro: la decisione sostitutiva era stata inizialmente annotata qui come "ADR-13 (nuovo)", riusando il numero. Il consiglio C7 l'ha rinumerata in **ADR-47** per rispettare la convenzione del registro — nuovo numero, mai modifica retroattiva. Il testo integrale è in ADR-47, consiglio C7.)*

### Alternative scartate

- **`llm-council-skill` (repo tenfoldmarc)** — formato incerto e maturità bassa (524★); superata dalla conversione in skill fatta dall'utente, che è quella in uso.
- **`spec-kit` constitution e `BMAD-METHOD`** — burocrazia di processo per un team di una persona.
- **Doppia fonte design (impeccable + vercel web-design-guidelines)** — due fonti = paralisi; resta solo impeccable come checklist operativa.
- **Council completo per ogni micro-decisione di sessione** — ~11 agenti per decisione paralizzerebbe lo sviluppo; resta ai checkpoint e per le decisioni bloccanti.

### Addendum (luglio 2026) — correzione di due premesse

Due premesse del consiglio C2 sono risultate errate o superate e vengono corrette qui, senza riscrivere gli ADR (che restano validi perché non dipendono da esse):

1. ~~"Su Claude Desktop le skill installabili non esistono"~~ → le skill girano su Web, Desktop e Claude Code.
2. ~~"Il consiglio completo è auto-consenso intra-modello perché Desktop non lancia advisor indipendenti"~~ → i sub-agenti esistono in Claude Code e nell'app Claude Code Desktop; la skill llm-council convertita dall'utente funziona per design con sub-agenti dello stesso modello e lenti di pensiero diverse (metodo Karpathy adattato, valido).

**Conseguenza operativa (integra ADR-09 sezione c):** il consiglio completo via skill llm-council può essere convocato **dentro le sessioni** in qualsiasi ambiente con sub-agenti reali — ai checkpoint fissi e per le decisioni bloccanti elencati nel file `02_REGOLE_FISSE_SKILLS.md`. Il "consiglio ridotto" di ADR-09 resta per le decisioni di routine, per motivi di costo (un consiglio completo sono ~11 agenti). Prerequisito: un **consiglio di prova** su Claude Desktop per verificare che gli advisor siano agenti davvero separati (paralleli, contesti isolati, peer review anonima) e non una simulazione a voce singola; se la prova fallisce, il consiglio completo si tiene fuori dalle sessioni.

### Punti aperti / verifiche esterne obbligatorie

- **Paternità del file**: la bozza di `REGOLE.md` la scrive Claude nella prima sessione, l'utente la approva e la committa; ogni modifica successiva è una revisione versionata.
- **Controllo di conformità a 1-2 settimane** da calendarizzare (chi lo fa, quando).
- ~~**Rivalutazione Claude Code** alla scadenza delle 2 settimane.~~ **Chiuso**: si lavora in Code fin dalla sessione 1 (ADR-47). Resta solo il controllo di conformità bisettimanale, che include la verifica che l'ambiente scelto regga.

---

## Consiglio C3 — Modulo documentale: template, anteprima, privacy

**Posta in gioco:** come generare documenti legali fedeli ai modelli depositati in Camera di Commercio, come garantire che l'anteprima sia ciò che si stampa, e come gestire consenso privacy e versioni dei modelli.

### Decisioni adottate

- **ADR-14 — Nessuna compilazione in cascata documento-da-documento.** Ogni documento è una **proiezione on-demand dei dati canonici** e della versione di template approvata: il disallineamento tra documenti non può esistere. Correzione di un dato → rigenerazione esplicita con nuova istanza, mai modifica a vista.
- **ADR-15 — Anteprima = PDF archiviato.** L'anteprima mostra il PDF generato e archiviato come artefatto alla creazione dell'istanza, mai ri-convertito a vista: *ciò che vedi è ciò che stampi*.
- **ADR-16 — Fedeltà tipografica.** Font Liberation (metricamente compatibili con Calibri/Cambria) installati sul Mac. Al salvataggio del template, **dry-run** che segnala font mancanti e segnaposti irrisolti con messaggi in italiano semplice.
- **ADR-17 — Import `.doc`/`.odt` consentito, con riserva.** Il file viene convertito una tantum in `.docx` e **nasce come bozza da approvare**, mai come versione depositata (la conversione non garantisce identità col modello depositato).
- **ADR-18 — Tracciamento della versione depositata in Camera di Commercio.** Ogni versione di template ha: hash SHA-256, stato (bozza / depositata / ritirata), blocco modifica (lock) e approvazione con ruoli. Cambio modello → nuova versione e **nuovo deposito**; le pratiche in corso restano legate alla versione con cui sono nate.
- **ADR-19 — PDF come template: NO definitivo.** Il PDF resta solo artefatto finale o allegato.
- **ADR-20 — Privacy: genera → stampa → firma → scansiona.** È la pratica reale e costa poco; la scansione è un **record immutabile di consenso** (soggetto, data, versione del modulo, hash, timestamp) conservato a norma. Al cambio dell'informativa, i consensi pregressi sono marcati **scaduti** e il sistema impone la ri-firma.
- **ADR-21 — Dati mancanti = generazione bloccata.** Nessun documento con buchi: il sistema elenca i campi vuoti e blocca la generazione finché non sono compilati.
- **ADR-22 — Pacchetto pratica.** Tasto "Genera pacchetto pratica" che renderizza in blocco tutte le istanze previste; i moduli condizionali hanno associazioni predefinite con condizioni (es. modulo mutuo solo se la pratica prevede mutuo).

### Alternative scartate

- **Compilazione in cascata tra documenti** — moduli condizionali generati vuoti e documenti disallineati dopo le correzioni.
- **PDF compilabile come template** — bocciato all'unanimità: nessuna garanzia di fedeltà e versionabilità.
- **Firma grafometrica** — rinviata, al più fase 2.
- **Firma OTP via link** — fase 2, subordinata a verifica eIDAS.
- **File convertito da `.doc`/`.odt` usato come versione depositata** — mina compliance: non è identico al modello depositato.

### Punti aperti / verifiche esterne obbligatorie

- ⚠️ **Test di validazione PRIMA del codice** su 5-10 modelli reali depositati in Camera di Commercio: conversione PDF, controllo font, dry-run segnaposti con dati finti, confronto stampa/anteprima. Se falliscono si correggono i template, non il motore.
- ⚠️ **Conservazione a norma (CAD, D.Lgs 82/2005)**: hash e timestamp da soli **non** danno valore probatorio alle scansioni — verifica legale/conservativa obbligatoria.
- **Ruoli e permessi** su creazione/modifica/approvazione dei template depositati (coperto da ADR-08 e ADR-18, da configurare con l'agenzia).

---

## Consiglio C4 — Scadenze locazioni 3+2 (canone concordato)

**Posta in gioco:** costruire il sistema di notifiche per le scadenze dei contratti 3+2 a canone concordato, scegliendo canale, trigger temporali e ciclo di follow-up, senza incorrere in vizi legali né creare falsa sicurezza.

### Decisioni adottate

- **ADR-23 — Canale unico v1: email.** Il bot WhatsApp/SMS è abbandonato: API non ufficiali = rischio ban del numero aziendale; API ufficiale = burocrazia e costi fissi. L'email è l'unico canale shippabile in 2-3 settimane. Restano il cuore della feature: bozza AI modificabile + invio su conferma umana.
- **ADR-24 — Doppio trigger (correzione legale).** Il trigger unico "preavviso 7 mesi" è legalmente viziato. Il modello corretto è:
  - **Trigger 1 — fine triennio − 7 mesi**: la scadenza legale vera. Il proprietario decide: disdetta (raccomandata AR/PEC entro i 6 mesi di preavviso, art. 3 l. 431/98) oppure rinnovo tacito del +2 (scelta registrata consapevolmente).
  - **Trigger 2 — fine biennio − 6 mesi**: nessuna disdetta necessaria, il contratto **cessa automaticamente**; è un trigger commerciale di **nuova stipula** (rinegoziazione, aggiornamento canone/ISTAT, registrazione RLI). Ribattezzato "nuova stipula", non "preavviso".
- **ADR-25 — Date calcolate dalla proroga effettiva**, non dall'inizio contratto; campi dedicati per disdetta anticipata di inquilino e proprietario.
- **ADR-26 — Inquilino fuori dalle notifiche, dentro al modello dati.** Le disdette dell'inquilino vanno registrate, altrimenti si notificano proprietari su contratti già morti.
- **ADR-27 — L'email raccoglie intenzioni, non produce effetti legali.** La disdetta formale resta raccomandata AR/PEC: va scritto nel messaggio e nel gestionale.
- **ADR-28 — Routing a tre scenari.** A — Chiusura/Cessazione (stop notifiche; se il "no" è del proprietario → lead vendita). B — Rinnovo (al triennio = tacito, registra e basta; al biennio = nuova stipula avviata). C — In trattativa ("sì, ma": stato con task operatore e data di rientro).
- **ADR-29 — Ciclo chiuso obbligatorio (non negoziabile in v1).** Reminder +7/+14/+30 ai non rispondenti; task operatore automatico a scadenza −6 mesi; cron idempotente con retry; dashboard "scadenze senza risposta"; dead man's switch sul job; SPF/DKIM/DMARC e gestione bounce.
- **ADR-30 — HITL sulle email.** Ogni email è una bozza AI modificabile inviata solo su conferma umana esplicita (coerente con ADR-07).

### Alternative scartate

- **Trigger unico "preavviso 7 mesi"** — vizio legale: il preavviso di 6 mesi (art. 3 l. 431/98) opera alla scadenza del triennio, non del biennio.
- **Scenario B come "proroga" del biennio** — finzione: dopo il biennio serve una nuova stipula.
- **Bot WhatsApp** — ban del numero aziendale con API non ufficiali; burocrazia + costi fissi con quella ufficiale.
- **SMS** — costo per messaggio + registrazione mittente AGCOM.
- **Fire-and-forget (invio senza follow-up)** — monologo senza feedback che crea falsa sicurezza: peggio di niente.
- **Tracking aperture/click, scoring e parsing AI delle risposte in v1** — richiedono basi giuridiche GDPR, informative, consenso e DPA con il fornitore AI; rinviati a v2.

### Punti aperti / verifiche esterne obbligatorie

- ⚠️ **Verifica legale delle due scadenze con consulente esterno** (l. 431/98), in parallelo alla build e prima della messa in produzione del modulo scadenze.
- **Comunicazione al cliente**: chiedeva un bot, riceve una mail — la rinuncia va motivata e presentata.
- **Qualità del dato**: email obsolete = trigger muto; va prevista la verifica periodica dei recapiti.

---

## Consiglio C5 — OCR, estrazione dati, Art. 7/APE, GDPR

**Posta in gioco:** come estrarre dati da documenti d'identità e attestati APE in modo affidabile, come attivare gli adempimenti di polizia (art. 7, art. 12, TULPS 109) senza falsi negativi, e come trattare le scansioni in conformità GDPR.

### Decisioni adottate

- **ADR-31 — GLM-OCR scartato, definitivamente.** È bilingue ZH/EN: l'italiano non è tra le lingue supportate ufficialmente, e OmniDocBench misura il dominio sbagliato per documenti italiani.
- **ADR-32 — Pipeline deterministic-first.** (i) APE in PDF nativi → estrazione testo diretta (PyMuPDF/pdfplumber), **niente OCR**; (ii) CIE/passaporti → parser MRZ ICAO 9303 con **checksum come gate bloccante**; (iii) OCR solo per il residuo (CI cartacee senza MRZ, documenti fotografati) con **PaddleOCR-VL candidato unico** (italiano supportato, Apache 2.0, Apple Silicon). Precisazione: leggere l'MRZ richiede comunque detection/OCR — solo il checksum è deterministico.
- **ADR-33 — Criterio di kill misurabile.** Bake-off su **almeno 50 documenti reali** (CI, CIE, passaporti, APE di almeno 3 regioni): errore >2% sui campi anagrafici → fallback al vision LLM principale. Decisione chiusa senza terzo round.
- **ADR-34 — Form anti-automation-bias.** Niente "Conferma" cieca: split-screen estratto/immagine, conferma **campo-per-campo**, salvataggio bloccato se checksum MRZ o cross-check codice fiscale falliscono, highlight solo sui campi a bassa confidenza, log di ogni correzione (metrica di accuracy). La frizione è il feature, non il bug.
- **ADR-35 — Codice fiscale come cross-check gratuito.** Ricalcolo deterministico da nome/cognome/nascita con check digit proprio; mismatch → blocco e revisione. Costo zero, valore alto.
- **ADR-36 — Matrice adempimenti con etichette parlanti.** Il sistema risolve internamente *tipo pratica × categoria soggetto × registrazione* e mostra **compiti, non articoli**: "Comunicazione Questura entro 48h — ospiti extra-UE" (art. 7 D.Lgs 286/98); "Comunicazione Alloggiati Web entro 24h — locazione turistica, tutti gli ospiti" (TULPS 109); art. 12 DL 59/78 gestito in silenzio come assorbito dalla registrazione AdE, con tooltip. Se la nazionalità manca, il sistema **chiede**: mai skip silenzioso.
- **ADR-37 — Parsing APE robusto.** Whitelist dei layout regionali, regex per campo con validazione di dominio (classe A4–G, EPgl,nren numerico plausibile); layout non riconosciuto → **coda di revisione umana**, mai mapping silenzioso. Verifica autenticità su registro regionale/SIAPE dove disponibile (parsare un PDF falso è peggio che non parsarlo).
- **ADR-38 — Presidi GDPR sulle scansioni.** DPIA ex art. 35 prima del go-live; informativa e base giuridica per le scansioni; cancellazione delle immagini dopo l'estrazione (o retention breve e motivata); cifratura, accessi loggati, audit trail delle correzioni. Il processing locale su M4 è l'argomento privacy-by-design: usarlo.

### Alternative scartate

- **GLM-OCR** — italiano non supportato ufficialmente (bloccante).
- **Trigger unico "nazionalità straniera"** — sbagliato: regole distinte per i tre adempimenti; TULPS 109 vale per **tutti** gli ospiti, indipendentemente dalla nazionalità.
- **Form precompilato con conferma unica** — teatro di sicurezza: favorisce l'automation bias.
- **Piattaforma dati a 12 mesi (scoring energetico, aggancio AML su dati OCR)** — riuso oltre lo scopo di raccolta, vietato dall'art. 5(1)(b) GDPR senza nuova base giuridica.
- **Surya 2 come candidato principale** — licenza pesi OpenRAIL-M da far verificare al legale; resta eventualmente secondario.

### Punti aperti / verifiche esterne obbligatorie

- ⚠️ **Test A/B (bake-off) PaddleOCR-VL + parser MRZ su 50+ documenti reali** (CI, CIE, passaporti, APE di ≥3 regioni) con criterio di kill al 2% — da fare prima di integrare l'OCR.
- **Verifica legale della licenza Surya 2** (OpenRAIL-M) solo se mai riconsiderato.
- **Congelamento della matrice adempimenti** con le etichette parlanti (con revisione del consulente legale).

---

## Consiglio C6 — Ruolo Proprietario, movimenti economici e compliance

**Posta in gioco:** definire il ruolo Proprietario e i suoi permessi, il perimetro del registro dei movimenti economici, e le diciture compliance corrette (registrazione RLI, deposito formulari, antiriciclaggio) senza esporre l'agenzia a responsabilità indebite.

### Decisioni adottate

- **ADR-39 — Niente contabilità fiscale nel gestionale.** Prima nota, IVA, fatture elettroniche e cespiti restano al commercialista. Il gestionale è il sistema di record **operativo**, il software fiscale quello **tributario**; la cerniera è un **export CSV categorizzato** allineato alle categorie del commercialista.
- **ADR-40 — I movimenti nascono dagli eventi, non dalle dita.** Provvigioni e canoni di gestione si generano **automaticamente alla firma del contratto**, con stato (previsto/fatturato/incassato); acconti, storni e note di credito sono stati della stessa riga. Nessun inserimento manuale: qualunque inserimento manuale uccide il dato entro tre mesi.
- **ADR-41 — Tabella movimenti unica.** Campi chiave: pratica, tipo, importo, stato, data, agente. Da questa tabella discendono dashboard, scadenziario, export e riconciliazione: senza di essa tutto il resto è decorazione.
- **ADR-42 — Ruolo Proprietario distinto da Admin**, con permesso granulare sui margini. Dashboard = vista in sola lettura degli **incassi** (previsto/fatturato/incassato) per mese/anno/tipologia/agente; il **margine per agente è visibile solo al Proprietario**. Il ruolo è giustificato da ciò che protegge (i margini), non dal titolo. Le spese restano fuori: in fase 2, import in sola lettura dal commercialista.
- **ADR-43 — Scadenziario RLI.** La registrazione va fatta entro 30 giorni dalla stipula/decorrenza; lo scadenziario del gestionale parte da **T+0 = registrazione del contratto nel sistema**, non dalla stipula (leva operativa sotto il controllo dell'agenzia).
- **ADR-44 — Diciture compliance corrette.** Il gestionale riporta «Deposito formulari presso la Camera di Commercio» (**non** AdE), con promemoria a ogni modifica dei modelli; «Adeguata verifica al conferimento dell'incarico» (**nessuna soglia** di importo); **5.000€** come alert **bloccante** sui pagamenti in contante (limite legale all'uso del contante, art. 49 D.Lgs 231/2007 come modificato da L. 197/2022 — *non* la soglia AML); **1.000€** come **policy interna configurabile**, etichettata «policy interna», mai «obbligo di legge».
- **ADR-45 — Regole compliance come parametri versionati** mantenuti dal fornitore, con **disclaimer strutturale** «adempimento non verificabile dal software», audit trail (chi vide quale etichetta, quando, quale versione della norma) e clausola dedicata nei ToS.
- **ADR-46 — Conservazione documentale 10 anni nativa** (AML e gestione) e **riconciliazione mensile** registro↔banca/commercialista come task guidato (chi, quando, come).

### Alternative scartate

- **Contabilità fiscale nel gestionale** — duplica il commercialista e ne assume la responsabilità tributaria.
- **Inserimento manuale dei movimenti** — degrada il dato entro tre mesi.
- **Perimetro "tutto dentro" (entrate e spese) in v1** — le spese arrivano in fase 2 come import in sola lettura dal commercialista.
- **Marketing "Radar Compliance" / vendere la correttezza normativa come prodotto** — rafforza l'affidamento del cliente e la responsabilità legale del fornitore; bocciato dalle review.
- **Dicitura "modelli brevettati AdE"** — doppiamente errata: i formulari si **depositano** (non si brevettano) presso la **Camera di Commercio** (non l'AdE), e il deposito va rinnovato a ogni modifica.

### Punti aperti / verifiche esterne obbligatorie

- ⚠️ **Validazione soglie AML con il consulente antiriciclaggio dell'agenzia** (adeguata verifica all'incarico senza soglia; 5.000€ come limite contante; policy interna 1.000€).
- **Aggiornamento periodico dell'adeguata verifica** (scadenze di rinnovo da modellare).
- **Rischio GDPR / controllo a distanza** sulla visibilità dei margini per agente — da valutare con consulente privacy/lavoro.
- **Registro divergente dai libri**: può essere letto dall'AdE come scritture extracontabili — coerenza con il commercialista.

---

## Consiglio C7 — Revisione della progettazione prima dello sviluppo (Sprint 0)

**Posta in gioco:** chiudere i punti aperti emersi dalla verifica di coerenza incrociata tra 03/04/05 prima di scrivere codice, e sanare le anomalie del registro. Verbale integrale: `08_VERBALI_CONSIGLI/C7_verdetto.md`.

### Decisioni adottate

- **ADR-47 — Ambiente di sviluppo: Code fin dalla sessione 1** *(sostituisce ADR-13; è l'ex "ADR-13 nuovo", rinumerato)*. Si lavora nella sezione **Code** di Claude Desktop (Claude Code integrato: sub-agenti veri, lettura/scrittura diretta sui file, GitHub integrato) su tutti gli sprint; la sezione **Progetti non si usa**. Le regole vivono in `REGOLE.md` + `CLAUDE.md` nel repo (doppia fonte, vedi ADR-10). **Claude Design** si usa solo nei punti UI degli sprint **S2 e S6**: prototipo delle schermate → validazione con segretaria/agenti → handoff a Code per l'implementazione. Motivo del cambio: chiarito che Code dispone dei sub-agenti reali (consiglio llm-council nativo) e che l'attrito è minimo con le regole nel repo; Code elimina il copia-incolla manuale di comandi, che era il rischio operativo principale per un utente non sviluppatore.
- **ADR-48 — Eval sul modello locale: da S6, con Mac Mini disponibile prima** *(sostituisce la sola clausola temporale di ADR-05)*. La eval suite gira su cloud da S0. Il **Mac Mini M4 va acquistato e configurato con Ollama prima dell'inizio di S6** (vincolo esplicito: senza Mac disponibile, S6 non si chiude). La **prima esecuzione della eval sul modello locale è criterio di done di S6**, ripetuta in S7 e S8. Criterio di kill: se l'eval locale fallisce, S7 non parte e **si cambia modello, non architettura**. Beneficio collaterale: il Mac M4 da S6 fornisce anche l'hardware Apple Silicon per il bake-off OCR di S7 (il MacBook 2019 Intel non lo è).
- **ADR-49 — Retention differenziata delle immagini dei documenti** *(precisa il rapporto tra ADR-38 e ADR-46)*. Le immagini acquisite a soli fini di estrazione dati si cancellano dopo l'estrazione (ADR-38); le copie dei documenti richieste dall'adeguata verifica antiriciclaggio si conservano **10 anni, cifrate e ad accesso loggato** (ADR-46). La pipeline OCR di S7 nasce con questa distinzione incorporata. ⚠️ Da confermare con il consulente AML (verifica già prevista in S5).

### Alternative scartate

- **"Interpretare" ADR-05 senza correggerlo** (eval su cloud = adempimento) — lascerebbe la scoperta del modello locale a S8, il rischio che ADR-05 voleva evitare.
- **Lasciare i presidi sui dati reali in S8** — non un rischio ma una non-conformità in corso d'opera; la chiusura costa quasi zero (FileVault + log accessi).
- **Blocco duro "nessuna pratica senza APE"** — produrrebbe APE fittizie o lavoro fuori sistema; sostituito da compito bloccante visibile + blocco della generazione documenti (applicazione di ADR-21, vedi verbale C7 P4).
- **Sola nota di anomalia su ADR-13 riusato** — un registro che viola la propria convenzione perde autorevolezza dove serve di più.

### Punti aperti / verifiche esterne obbligatorie

- ⚠️ **Bozza DPIA (art. 35) prima di S3** (aggiornamento prima di S7, chiusura formale in S8): l'art. 35 la richiede *prima* del trattamento.
- ⚠️ **Conferma consulente AML su ADR-49** (retention differenziata) durante S5.
- **Acquisto Mac Mini M4** da calendarizzare in tempo per l'inizio di S6 (ADR-48).

---

## Consiglio C8 — JARVIS assistente personale del Proprietario

**Posta in gioco:** le richieste del proprietario su JARVIS (accesso esclusivo, "secondo cervello", auto-creazione di skill e automazioni, n8n/"Graphify") senza violare ADR-02/03/04/07 né il vincolo tutto-locale. Evidenze: brief `R3_memoria_brief.md` e `R4_automazioni_brief.md`. Verbale integrale: `08_VERBALI_CONSIGLI/C8_verdetto.md`.

### Decisioni adottate

- **ADR-50 — JARVIS riservato al Proprietario; un solo approvatore competente per azione.** La **chat** JARVIS è accessibile al solo ruolo Proprietario (**permesso di ruolo**, mai hardcoded sull'utente — anti lock-out); la coda **«Da approvare»** è una schermata separata, visibile per ruolo. Ogni proposta di JARVIS diventa un **Task** assegnato all'**unico approvatore competente per tipo di azione** (operatività documentale → Segretaria; email a clienti, dati economici, margini → Proprietario), sempre con diff leggibile (ADR-07). La **doppia firma in serie è vietata**: due controllori sono meno di uno (rubber-stamping istituzionalizzato). AuditLog esteso alle consultazioni della chat (domande, tool invocati, versione modello — estensione di ADR-08); log chat sotto cifratura/retention di 04 §8.2. Perimetro v1 = S6 invariato (lettura + proposte su elenco chiuso); estensione scrittura = Fase 2, **un tool alla volta, ciascuno con mini-ADR**.
- **ADR-51 — Memoria personale «Cose da ricordare» (versione noiosa).** Tabella `ricordi` in SQLite + FTS5 + sqlite-vec (versione bloccata) + embedding `bge-m3` via Ollama — dentro DB, backup e cifratura esistenti; nessun servizio nuovo (Graphiti/Neo4j, mem0, GraphRAG scartati — evidenze R3). I ricordi nascono **solo da dettatura diretta confermata del Proprietario** («Vuoi che ricordi: X?»), **mai estratti da email o documenti** (regola anti-avvelenamento). Correzioni via `valid_from`/`superseded_by`; **oblio = cancellazione fisica del testo** (in audit resta solo l'evento); ricordi che nominano terzi agganciati al Soggetto in anagrafe (artt. 15-17 GDPR); categorie art. 9 rifiutate; addendum DPIA prima dello sprint. Si costruisce in **S9**.
- **ADR-52 — «Procedure» solo su richiesta esplicita (conferma e precisa ADR-04).** In UI la parola "skill" **non compare mai**: si chiamano **«Procedure»**, versionate in Git in modo invisibile («versione 3, approvata il…»). v1: creazione **solo su richiesta esplicita** del Proprietario, che è anche l'**unico approvatore**; il contatore "richiesta ripetuta N volte" slitta a Fase 2 (richiede telemetria; rischio proposte mediocri approvate per stanchezza) e non è promesso. Vincoli: (a) una procedura **non può allentare HITL** — a rifiutarla è il validatore, non l'LLM; (b) **mai procedure il cui testo derivi da contenuti esterni** (stessa regola anti-avvelenamento di ADR-51).
- **ADR-53 — Motore automazioni interno a catalogo chiuso (n8n scartato).** Tabella `automazione` + **riuso** dello scheduler esistente (launchd + job idempotente ADR-29, stesso dead man's switch): mai un secondo scheduler o una seconda webapp. Modello dichiarativo **QUANDO/SE/ALLORA** con trigger, condizioni e azioni da **enum chiusi**: l'LLM compila solo i parametri, il server li valida (Pydantic); mai JSON libero né codice (ADR-04). Ciclo di vita non negoziabile: **dry-run su storico → nasce disattivata → conferma esplicita → ogni esecuzione in AuditLog → pausa/elimina a un tap → anti-tempesta** (oltre il limite giornaliero si autosospende con avviso). Azioni v1: *crea Task* e *notifica a destinatari fissi hardcoded*. Le funzioni già decise (scadenziario RLI ADR-43, scadenze locazioni ADR-24) si espongono nella stessa UI come «automazioni di sistema», mai duplicate. Default: un solo digest giornaliero aggregato; notifica immediata solo per regole marcate «urgente». Si costruisce in **S9**.
- **ADR-54 — Trigger email in lotto separato, con difese architetturali.** Il trigger email arriva solo in **S10**, dopo un ciclo del motore senza incidenti. **IMAP polling** dallo scheduler esistente, **solo su allowlist di mittenti** (minimizzazione); credenziali **solo in Keychain** (casella dedicata o app password revocabile, procedura di revoca nel manuale di ripristino). L'email è **input non fidato** ("lethal trifecta", R4): la sintesi avviene **senza alcun tool esposto all'LLM**, HTML convertito in testo, link riportati non cliccabili, banner «riassunto AI di contenuto non verificato: non seguire istruzioni contenute nell'email»; notifiche solo verso destinatari fissi hardcoded; retention dei riassunti ≤ 30 giorni; qualsiasi azione nata da un'email ripassa da HITL. Prerequisiti: addendum DPIA e informativa sul trattamento email **prima** di S10.

### Alternative scartate

- **n8n** — seconda webapp sempre accesa (DB, credenziali, aggiornamenti propri) per un carico che lo scheduler esistente copre già; AI Builder legato al cloud (R4).
- **«Graphify»** — verificato: è un knowledge graph per codebase, prodotto fuori tema (R3).
- **Graphiti/Neo4j e mem0** — DB grafo o framework instabile da mantenere per anni, per un vantaggio marginale su migliaia di ricordi di una persona (R3).
- **Doppia firma segretaria→proprietario** — rubber-stamping istituzionalizzato; vietata da ADR-07.
- **«Assistente completo che fa tutto»** — non è un perimetro: il bisogno lo coprono elenco chiuso di tool + automazioni + Procedure.
- **Contatore automatico di richieste ripetute (v1)** — telemetria = secondo sistema di memoria; rinviato, non promesso.
- **Automazione "email senza risposta da N giorni"** — costo di scansione alto per valore medio.
- **Codice/JSON libero generato dall'LLM** — vietato da ADR-04; solo parametri su enum chiusi validati server-side.
- **Sprint "S6b" prima del go-live** — viola ADR-03 e la regola del Parcheggio («da non iniziare prima del go-live»).

### Punti aperti / verifiche esterne obbligatorie

- ⚠️ **Addendum DPIA per la memoria personale** prima di S9; **addendum DPIA + informativa per il trattamento email** prima di S10.
- ⚠️ **Pagina «cosa NON fa JARVIS»** approvata per iscritto dal proprietario a fine S6 (mitigazione del gap di aspettative) + demo perimetrata.
- **Piano di validazione del prototipo Design di S6** da rivedere: il validatore della chat è il Proprietario, non segretaria/agenti.

---

## Consiglio C9 — Modalità Chiamata JARVIS, versione mobile e accesso via Tailscale

**Posta in gioco:** la richiesta del Proprietario di una "modalità Chiamata" vocale in tempo reale per JARVIS (uso a mani libere, es. alla guida) e la valutazione di 5 tool GitHub proposti, nella cornice — **decisa dall'utente** — di una **versione mobile completa del gestionale** usata dal telefono ovunque tramite **Tailscale**. Evidenze: brief `R5_chiamata_mobile_brief.md`. Verbale integrale (con certificazione del meccanismo del consiglio e bozza di progettazione di Fable 5 in appendice): `08_VERBALI_CONSIGLI/C9_verdetto.md`.

### Decisioni adottate

- **ADR-55 — Mobile = PWA responsive sullo stesso FastAPI (pre-go-live).** Nessuna app nativa iOS/Android: un secondo codebase senza benefici per un utente principale su rete privata. Web responsive + manifest PWA installabile sulla stessa app server-rendered; HTTPS solo via `tailscale cert`/`tailscale serve` sul tailnet; service worker che cachea **solo asset statici, mai dati clienti offline**. Unica fonte design resta la checklist impeccable anche su mobile (una sola azione primaria per schermata, target touch ≥44px). PDF sempre con bottone "Apri/Scarica" nativo accanto a PDF.js; upload foto documenti via `<input type=file accept=image/* capture=environment>` nativo con ricompressione server-side. **Collocazione: sprint dedicato pre-go-live** (la versione mobile è cornice decisa dall'utente, quindi prodotto base — la regola del Parcheggio ADR-03 vincola la Fase 2 di JARVIS, non il gestionale).
- **ADR-56 — Deroga dichiarata n.2 al vincolo tutto-locale: control-plane Tailscale.** Come per l'SMTP (deroga n.1), l'accesso remoto via Tailscale introduce un terzo che tratta **metadati** (nodi, topologia, chiavi, relay DERP per il traffico che resta cifrato end-to-end WireGuard) ma **mai i dati**. Richiede: DPA Tailscale sottoscritto, aggiornamento del registro dei trattamenti, Headscale documentata come exit strategy **non** implementata.
- **ADR-57 — Hardening del tailnet.** ACL **default-deny** (solo il nodo-telefono del Proprietario raggiunge la porta HTTPS dell'app sul Mac Mini), device approval, Tailnet Lock, MFA sull'account Tailscale, key expiry; **Funnel/exit-node/subnet-routing vietati, zero port-forwarding**; app in bind solo su `localhost` + interfaccia `100.x`. **Tailscale è trasporto, mai autenticazione:** login applicativo e ruoli (ADR-08, ADR-50) restano obbligatori sopra la VPN. Ogni accesso remoto in AuditLog con identità del nodo tailnet + alert email al login da nodo mai visto.
- **ADR-58 — Runbook telefono perso/rubato.** Procedura scritta e **testata una volta davvero** (come il restore test ADR-06): revoca del nodo Tailscale, invalidazione di tutte le sessioni app, rotazione password, verifica dell'audit; valutazione data-breach **art. 33 GDPR entro 72h**. Obbligatori: blocco schermo biometrico sul telefono, sessioni mobili brevi con re-login. Rischio residuo basso perché il telefono non contiene dati (è solo un client).
- **ADR-59 — Perimetro della modalità Chiamata (Fase 3).** A voce **solo** Q&A read-only + **dettatura di proposte che finiscono in coda**; l'esecuzione di scritture a voce è **vietata sempre** (un "sì" alla guida è approvazione cieca, vietata da ADR-07). Gate **nel codice**: il token di approvazione è generabile solo dalla UI dopo il render del diff a video, **non forgiabile dall'LLM**. Niente pulsante "approva tutto", diff mostrato voce per voce. Interazione **half-duplex push-to-talk**, niente barge-in in v1; risposte max 2 frasi by design. **Precondizione bloccante:** walking skeleton (~1 settimana) che misuri latenza end-to-end su 4G reale (incluso relay DERP) e RAM a regime con conversazione lunga — soglia **4 s/turno**, altrimenti aspettative rifirmate o rinuncia. Pagina "cosa NON fa JARVIS" aggiornata e **rifirmata prima di costruire**.
- **ADR-60 — Il canale vocale è input NON fidato.** La trascrizione è trattata come le email IMAP di S10 (**contesto, mai istruzioni**), loggata integralmente nell'evidence pack; **read-back verbale** dei campi chiave prima di accodare una proposta; **nessun audio persistito**, solo trascrizioni con retention definita; attivazione sempre esplicita push-to-talk (**mai ascolto continuo/wake word** — tutela dei terzi in auto); **divieto di autenticazione vocale** (dato biometrico, art. 9 GDPR).
- **ADR-61 — Stack voce locale "noioso".** Glue custom minimale **dentro** FastAPI (un endpoint WebSocket), **nessun framework di orchestrazione né secondo servizio sempre acceso**; processi voce avviati **on-demand** all'apertura della Chiamata e terminati alla chiusura. STT = **whisper.cpp** large-v3-turbo con Core ML/ANE (fallback whisper medium quantizzato); LLM = **Ollama 27B già residente**; TTS = deciso con **demo audio al Proprietario** nell'ordine: `say`/AVSpeech nativo → **Piper** `it_IT-paola` via subprocess (GPL-3.0 **mai linkata**, licenza della voce da verificare) → **Kokoro-82M** (Apache-2.0). **XTTS v2 VIETATO** (licenza CPML non commerciale). Qualsiasi framework (anche Pipecat/LiveKit) solo dopo fallimento documentato del glue custom e nuovo permesso-dipendenze.
- **ADR-62 — Notifiche mobile.** Canale primario resta l'**email SMTP** (deroga n.1). Eventuale **Web Push su iOS** solo con PWA installata e **payload generico privo di dati** ("hai una proposta in attesa"), perché transita da APNs (cloud Apple).
- **ADR-63 — UI voce nativa, zero dipendenze.** Orb "Jarvis che parla" e waveform della voce in ingresso con **Web Audio AnalyserNode + Canvas 2D + CSS custom property** (~50 righe). `bklit-ui` e `personaplex` scartati; `anime.js`/`siriwave` rivalutabili solo con permesso esplicito nuove dipendenze; l'animazione è **rifinitura finale, non requisito** (è inutile proprio nello scenario — la guida — che la motiva).

### Alternative scartate

- **NVIDIA/personaplex** — modello speech-to-speech monolitico (base Moshi) che richiede GPU NVIDIA/CUDA, non gira su Apple Silicon (solo port community non mantenuti), non collega Ollama/whisper/Piper, non sta in RAM accanto al 27B; pesi sotto NVIDIA Open Model License. Viola hardware, architettura, RAM e igiene di licenza.
- **livekit/agents come adozione** — dei due proposti è il migliore (Apache-2.0, Apple Silicon, plugin locali: **batte personaplex senza discussione**), ma impone un media server WebRTC **sempre acceso** per un solo utente vocale. Tenuto **solo come riferimento architetturale**: i pattern (approval gate, blocking HITL, turn detection) si copiano nel glue custom.
- **David-Crty/databasement** — web app Laravel/Docker per flotte di DB eterogenei: per un singolo SQLite locale duplica ADR-06 e aggiunge una superficie d'attacco. (Per RPO di secondi l'unico incremento sensato sarebbe **Litestream**, Apache-2.0, con ADR separato — non databasement.)
- **bklit-ui** — registry di componenti *chart* per React/Next via shadcn: doppio mismatch (frontend server-rendered senza React; sono grafici, non orb/waveform).
- **anime.js in v1** — libreria sana (MIT, ~10KB) ma non necessaria: waveform/orb si fanno nativi.
- **XTTS v2 / Coqui** — licenza CPML non commerciale, azienda chiusa: nessuno da cui acquistare licenza.
- **App nativa iOS/Android** — secondo codebase + firma + distribuzione senza benefici per il caso d'uso; contro il vincolo di semplicità.
- **Scritture eseguite a voce / conferma vocale delle scritture** — approvazione cieca, vietata da ADR-07; il gate sta nel codice, non nella buona volontà.
- **Full-duplex "Iron Man" / ascolto continuo / wake word** — fragilità tecnica non necessaria + rischio privacy sui terzi; da scrivere nella pagina "cosa NON fa JARVIS".
- **Headscale/NetBird self-hosted** — più manutenzione e un endpoint da esporre; per questa scala la scelta noiosa è Tailscale SaaS + Tailnet Lock, con Headscale come uscita documentata.

### Punti aperti / verifiche esterne obbligatorie

- ⚠️ **DPA Tailscale** sottoscritto + aggiornamento del **registro dei trattamenti** per i metadati del control-plane (accountability GDPR) — prima dell'accesso remoto in produzione.
- ⚠️ **DPIA "leggera" (art. 35 GDPR)** sulla combinazione voce + accesso remoto + AI (probabilmente sotto soglia d'obbligo per 2-5 utenti, ma da istruire).
- ⚠️ **Verifica licenza della singola voce TTS** adottata (es. Piper `it_IT-paola`) e conferma legale dell'uso interno server-side di software GPL-3.0 non distribuito.
- **Retention delle trascrizioni vocali** nell'audit log, validata con il consulente privacy.
- ⚠️ **Parere su art. 173 CdS / responsabilità civile** per la policy d'uso alla guida ("il sistema non richiede mai sguardo o tocco in movimento"), inclusa nella pagina "cosa NON fa JARVIS" da far rifirmare al Proprietario.
- **Walking skeleton di misura** (latenza 4G/DERP, RAM a regime) come gate tecnico prima di costruire la Chiamata (ADR-59).

---

## Tabella riassuntiva — Richiesta originale del cliente → decisione finale

| # | Richiesta originale del cliente | Decisione finale | ADR |
|---|--------------------------------|------------------|-----|
| 1 | **Anteprima documenti** | L'anteprima mostra il **PDF generato e archiviato come artefatto** alla creazione dell'istanza, mai ri-convertito a vista: ciò che vedi è ciò che stampi. | ADR-15 |
| 2 | **Import doc/docx/odt/pdf** | `.doc`/`.odt` convertiti una tantum in `.docx` e **nati come bozza da approvare**, mai come versione depositata; il **PDF non è mai un template** (solo artefatto o allegato). | ADR-17, ADR-19 |
| 3 | **Bot scadenze WhatsApp** | **Abbandonato**: l'unico canale v1 è l'**email** (bozza AI modificabile + invio su conferma umana). WhatsApp non ufficiale = rischio ban; ufficiale = costi e burocrazia. | ADR-23, ADR-30 |
| 4 | **Trigger 7 mesi** | **Doppio trigger corretto legalmente**: Trigger 1 = fine **triennio** −7 mesi (disdetta o rinnovo tacito); Trigger 2 = fine **biennio** −6 mesi (**nuova stipula**, non preavviso). Date dalla proroga effettiva. Da validare col consulente legale. | ADR-24, ADR-25 |
| 5 | **GLM-OCR** | **Scartato definitivamente** (italiano non supportato). Pipeline deterministic-first: testo nativo per APE, MRZ+checksum per CIE/passaporti, **PaddleOCR-VL solo per il residuo**, con bake-off su 50+ documenti e kill al 2%. | ADR-31, ADR-32, ADR-33 |
| 6 | **Ruolo Proprietario** | **Sì, distinto da Admin**, con permesso granulare sui margini: dashboard in sola lettura sugli incassi; margine per agente visibile solo al Proprietario. | ADR-42 |
| 7 | **Registrazione 30 giorni** | Scadenziario RLI a **T+0 = registrazione del contratto nel sistema** (non dalla stipula), con scadenza legale di 30 giorni dalla stipula/decorrenza. | ADR-43 |
| 8 | **Modelli "brevettati AdE"** | Dicitura corretta: **deposito formulari presso la Camera di Commercio** (non brevetto, non AdE), con **promemoria di ri-deposito a ogni modifica** dei modelli e tracciamento versione depositata (hash, stato, lock). | ADR-18, ADR-44 |
| 9 | **AML 5000/1000** | **5.000€** = alert **bloccante** sul contante (limite legale all'uso del contante, non soglia AML); **1.000€** = **policy interna configurabile**, etichettata «policy interna». Adeguata verifica **all'incarico, senza soglia**. Da validare col consulente AML. | ADR-44 |
| 10 | **Privacy auto-compilata** | Nessuna raccolta automatica del consenso: flusso **genera → stampa → firma → scansiona**; la scansione è **record immutabile di consenso** (soggetto, versione modulo, data, hash); cambio informativa → consensi scaduti e **ri-firma obbligatoria**. | ADR-20 |
| 11 | **API cloud in sviluppo** | Sì in sviluppo con **soli dati sintetici/anonimizzati** (provider configurabile via `base_url`/`model`); produzione su **Ollama locale**; eval suite rieseguita sul modello locale **da S6** (prima esecuzione = criterio di done di S6). | ADR-05, ADR-48 |
| 12 | **Auto-skill JARVIS** | **Libreria curata**: JARVIS propone skill in Markdown, attivabili **solo con approvazione umana + versioning Git**; **mai** codice auto-generato eseguito sul server. | ADR-04 |
| 13 | **Versione mobile** | **PWA responsive** sulla stessa app FastAPI (niente app nativa), usata dal telefono via **Tailscale**; sprint dedicato **pre-go-live**. | ADR-55, ADR-56, ADR-57 |
| 14 | **JARVIS "come Iron Man" (chiamata vocale)** | **Modalità Chiamata in Fase 3**: a voce solo Q&A read-only + dettatura di proposte in coda; **scritture mai a voce** (HITL a video); stack voce **tutto locale** (whisper.cpp + Ollama 27B + TTS italiano), on-demand. | ADR-59, ADR-60, ADR-61 |
| 15 | **Tool GitHub proposti** | **Nessuno adottato**: databasement, bklit-ui, personaplex e anime.js (v1) scartati; livekit/agents solo come **riferimento di pattern**; UI voce **nativa**. | ADR-63 |

---

## Indice ADR

| Intervallo | Consiglio | Tema |
|-----------|-----------|------|
| ADR-01 … ADR-08 | C1 | Stack, determinismo, JARVIS, backup, HITL, identità/audit |
| ADR-09 … ADR-13 | C2 | Regole di sviluppo su Claude Desktop, rituali di sessione, handoff |
| ADR-14 … ADR-22 | C3 | Rendering on-demand, anteprima PDF, versioni depositate, privacy |
| ADR-23 … ADR-30 | C4 | Canale email, doppio trigger, ciclo chiuso, routing scenari |
| ADR-31 … ADR-38 | C5 | OCR deterministic-first, MRZ, matrice adempimenti, GDPR |
| ADR-39 … ADR-46 | C6 | Movimenti automatici, ruolo Proprietario, diciture compliance, retention |
| ADR-47 … ADR-49 | C7 | Ambiente di sviluppo (Code), eval locale da S6 con Mac Mini, retention differenziata immagini |
| ADR-50 … ADR-54 | C8 | JARVIS solo Proprietario, memoria «Cose da ricordare», Procedure, automazioni interne, trigger email |
| ADR-55 … ADR-63 | C9 | Mobile PWA, deroga/hardening Tailscale, runbook furto, modalità Chiamata JARVIS, voce = input non fidato, stack voce locale, notifiche, UI voce nativa |

**Prossima modifica a questo registro:** solo tramite nuovo ADR (nuovo numero, mai modifica retroattiva) con motivazione e, se richiesto dai Punti aperti, esito della verifica esterna allegato.
