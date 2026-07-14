# 00 — LEGGIMI: come usare questa harness

*Guida per chi usa questo materiale. Non serve saper programmare: serve solo saper copiare e incollare.*

---

## Cos'è questa harness e perché esiste

Questo progetto (il gestionale per l'agenzia immobiliare, con l'assistente AI "JARVIS") **è già stato perso una volta**: un reset del computer ha cancellato tutto il lavoro fatto. Da quella lezione nasce questa harness.

"Harness" significa **imbragatura**: è il set di file che tieni in questa cartella, con dentro tutto ciò che serve per sviluppare il gestionale **a sessioni**, lavorando con Claude (l'AI di Anthropic) sul computer, senza mai perdere il filo.

Il sistema si regge su tre pilastri:

1. **GitHub** (un sito che conserva i tuoi file online, con la storia di ogni modifica). È la tua cassaforte anti-disastro: anche se il computer si rompe domani, il progetto è al sicuro e riparti da dove eri.
2. **Regole scritte** (il file `02`): un foglio di regole che Claude deve seguire in ogni sessione, così non si "inventa" strade complicate e non deriva.
3. **Passaggio di consegne tra sessioni** (il file `07`): ogni sessione con Claude è una giornata di lavoro. A fine giornata si scrive un riassunto; il giorno dopo si riparte da quel riassunto. Niente si perde.

Non devi capire il codice. Devi solo **seguire i rituali descritti qui**: sono loro che tengono in piedi il progetto.

---

## Gli strumenti che userai (e quando)

Lavori dentro l'app **Claude** sul Mac, usando due delle sue sezioni, più GitHub:

| Strumento | A cosa serve | Quando lo usi |
|---|---|---|
| **Code** (sezione di Claude Desktop) | L'ambiente di lavoro principale: Claude legge e scrive **direttamente i file sul Mac**, esegue i comandi al posto tuo (ti chiede il permesso), lavora sul repository. Ha i sub-agenti veri: qui funziona il consiglio llm-council completo. | **Sempre**: dalla sessione 1 a tutti gli sprint di sviluppo. |
| **Claude Design** (sezione di Claude Desktop) | Disegna i **prototipi delle schermate** (mockup interattivi) e li consegna a Code per essere implementati. | Negli sprint con interfaccia: **S2** (modulo documentale), **S6** (chat JARVIS), **S6-bis** (Chiamata), **S-Mob** (mobile) e, in Fase 2, **S9/S10** — vedi tabella Ambienti in `05_ROADMAP_SPRINT.md`. |
| **GitHub + GitHub Desktop** | La cassaforte online del progetto. | Setup una volta; poi Claude fa commit e push da Code, tu verifichi. |

> La sezione **Progetti** di Claude Desktop **non si usa** in questo progetto: Code fa tutto ciò che farebbe un Progetto, e in più lavora direttamente sui file.

---

## Mappa dei file di questa cartella

| File | A cosa serve (in una riga) |
|---|---|
| `00_LEGGIMI.md` | Questo file: la guida d'uso di tutto il sistema. |
| `01_PROMPT_MAESTRO.md` | Il primo prompt da incollare a Claude: avvia la progettazione (sessione 1). |
| `02_REGOLE_FISSE_SKILLS.md` | Le regole che Claude deve sempre rispettare + come installarle (blocco da copiare). |
| `03_DECISIONI_CONSIGLIO.md` | Le decisioni importanti già prese sul progetto e le alternative scartate (riferimento vincolante). |
| `04_ARCHITETTURA.md` | Come è fatto il sistema: tecnologie, struttura dei dati, moduli (riferimento). |
| `05_ROADMAP_SPRINT.md` | Il piano di lavoro diviso in sprint (le "tappe" del progetto) con l'ambiente da usare per ciascuno. |
| `06_PROMPT_SPRINT/` | I prompt pronti da incollare per gli sprint S0–S8 (quelli di S6-bis, S-Mob, S9 e S10 si scrivono prima del rispettivo sprint). |
| `07_HANDOFF_TEMPLATE.md` | Il modello di "riassunto di fine sessione" e le regole per salvare su GitHub. |
| `08_VERBALI_CONSIGLI/` | I verbali integrali dei 10 consigli di progettazione (C1–C10) e gli 8 brief di ricerca (R1–R8), per tracciabilità. |
| `REGOLE.md` | Le regole operative del progetto: Claude le legge e riassume all'apertura di ogni sessione. |
| `CLAUDE.md` | Il "pilota automatico": Code lo legge da solo a ogni avvio e gli ordina di rispettare `REGOLE.md`. Non va toccato. |
| `Plan.md` | Il **cruscotto del progetto**: dove siamo, stato degli sprint, prossimo passo. Si aggiorna a ogni chiusura di sessione. |
| `HANDOFF.md` | Il riassunto dell'ultima sessione di lavoro (il punto esatto di ripartenza). |
| `config.example.toml`, `requirements.txt` | Configurazione di esempio del provider AI e dipendenze Python del progetto. |
| `llm/`, `evals/`, `scripts/`, `setup/` | Il codice dello Sprint S0: astrazione provider AI, eval suite, script di backup e di setup. |
| `.claude/skills/` | Le skill installate per Claude Code (llm-council, superpowers, ponytail…). Non vanno toccate a mano. |

Leggi solo questo file `00` e il `02`. Gli altri li userai copiando e incollando, quando indicato.

---

## Istruzioni passo-passo

### Passo 1 — Crea l'account GitHub e il repository (una volta sola)

1. Vai su **github.com** e crea un account gratuito (pulsante *Sign up*). Segna da qualche parte nome utente e password.
2. Una volta entrato, clicca il pulsante verde **New** (o *New repository*).
3. Compila così:
   - **Nome del repository:** `gestionale-immobiliare`
   - **Visibilità:** seleziona **Private** (privato: solo tu lo vedi)
   - Spunta la casella **Add a README file**
4. Clicca **Create repository**. Fatto: hai creato la "cassaforte" online del progetto.

### Passo 2 — Collega GitHub al computer e carica la harness (una volta sola)

1. Scarica e installa **GitHub Desktop** dal sito **desktop.github.com** (è gratuito, esiste per Mac e Windows).
2. Aprilo e accedi con l'account GitHub creato al passo 1.
3. Clicca **Clone a repository** → scegli `gestionale-immobiliare` → come cartella di destinazione scegli ad esempio `Documenti/gestionale-immobiliare` → **Clone**.

Ora sul computer hai una cartella "gemella" di quella online: tutto ciò che metti lì dentro potrà essere salvato online.

4. **Copia dentro quella cartella tutti i file di questa harness** (tutti i file `.md`, la cartella `06_PROMPT_SPRINT` e la cartella `08_VERBALI_CONSIGLI`).
5. Apri GitHub Desktop: vedrai i file elencati come novità. In basso a sinistra scrivi come messaggio: `primo caricamento: harness del progetto`, poi clicca **Commit to main** e poi **Push origin**.

Controlla su github.com che i file ci siano. Da questo momento esiste una copia di sicurezza online.

### Passo 3 — Installa le regole (una volta sola, 5 minuti)

Le regole vivono in **due posti** (il file `02_REGOLE_FISSE_SKILLS.md`, sezione A, spiega il perché):

1. **`REGOLE.md` nel repository**: crea il file copiando il BLOCCO REGOLE dal file `02` (sezione B), salvalo nella cartella del repository, poi commit + push da GitHub Desktop.
2. **`CLAUDE.md` nel repository**: un file di una riga che dice a Claude Code di leggere `REGOLE.md` all'avvio di ogni sessione. Il testo esatto da copiare è nel file `02`, sezione A.

Verifica che entrambi i file compaiano su github.com.

### Passo 4 — Sessione 1 in Code: avvia il progetto con il Prompt Maestro

1. Apri l'app **Claude** sul computer e vai nella sezione **Code**.
2. Seleziona come **cartella di lavoro** (working directory) la cartella del repository: `Documenti/gestionale-immobiliare`. Se è la prima volta, Claude potrebbe chiederti di autorizzare l'accesso alla cartella e l'esecuzione dei comandi: autorizza (potrà sempre chiederti conferma prima di ogni comando).
3. Incolla la **frase rituale, variante 1 — prima sessione in assoluto** (file `02`, sezione C). Aspetta il riassunto delle regole in 5 righe: è la tua verifica che le ha lette.
4. Ora incolla il **Prompt Maestro**: apri il file `01_PROMPT_MAESTRO.md` e copia-incolla tutto il blocco tra `INCOLLA DA QUI` e `FINO A QUI`.
5. Da qui in poi segui le indicazioni di Claude. In Code **non devi più fare da postino**: Claude legge e scrive i file da solo e ti propone i comandi da approvare con un clic. La sessione 1 serve a gettare le fondamenta: non si scrive ancora il gestionale vero e proprio.

### Passo 5 — Le sessioni di sviluppo: un prompt di sprint per sessione

Il progetto avanza a **sprint** (tappe), elencati nel file `05_ROADMAP_SPRINT.md`. Gli sprint S0–S8 hanno un prompt pronto nella cartella `06_PROMPT_SPRINT/`; i prompt di S6-bis, S-Mob, S9 e S10 si scrivono prima di avviare il rispettivo sprint (lo stato è tracciato in `Plan.md`).

Il metodo è sempre lo stesso:

1. Apri una **sessione nuova** in Code sulla cartella del repository (mai continuare la sessione dello sprint precedente).
2. Incolla la **frase rituale di apertura** (file `02`, sezione C).
3. Incolla il **prompt dello sprint** corrispondente (dalla cartella `06_PROMPT_SPRINT/`).
4. Lavora con Claude su **quella sola task**, finché il "criterio di accettazione" (lo trovi scritto nel prompt di sprint) non è soddisfatto.
5. Finito? Esegui il **rituale di chiusura** (Passo 7) e chiudi la sessione.

> **Sprint con interfaccia (S2, S6, S6-bis, S-Mob e, in Fase 2, S9/S10) — eccezione Claude Design.** In questi sprint, prima di implementare le schermate, il prompt ti guiderà ad aprire **Claude Design** per generare il prototipo visivo, farlo validare da chi userà quelle schermate, raccogliere il feedback, e poi tornare in Code per implementarlo. Attenzione (ADR-50): per S2 validano **segretaria/agenti**; per S6 (chat JARVIS) e S6-bis (Chiamata) il validatore è il **solo Proprietario**, perché la chat è riservata a lui. Sono gli unici momenti in cui esci da Code.

### Passo 6 — Rituale di apertura di OGNI sessione (obbligatorio)

Ogni volta che apri una sessione nuova, il **primo messaggio** deve essere la frase rituale (file `02`, sezione C):

> *"Leggi REGOLE.md e riassumilo in 5 righe prima di toccare codice."*

Perché: Claude non si ricorda le sessioni precedenti. La frase rituale lo "riallinea" alle regole in pochi secondi, e il riassunto in 5 righe è la tua prova che le ha davvero lette — una verifica che puoi fare anche senza saper leggere codice. (Il file `CLAUDE.md` fa leggere le regole in automatico, ma la frase rituale resta obbligatoria: doppia sicurezza, e ti dà la verifica leggibile.)

### Passo 7 — Rituale di chiusura di OGNI sessione (obbligatorio)

Mai chiudere una sessione "e basta". Prima di chiudere:

1. Incolla il messaggio di richiesta del **Riassunto di chiusura sessione** (lo trovi pronto da copiare nel file `07_HANDOFF_TEMPLATE.md`, sezione A).
2. Claude scriverà il riassunto strutturato e **lo salverà da solo** nel repository come file `HANDOFF.md` (sei in Code: può farlo).
3. Chiedi a Claude il **commit + push** su GitHub con messaggio nel formato `sprint-N: descrizione breve` (o fallo tu da GitHub Desktop, come preferisci).
4. Verifica su github.com che il salvataggio ci sia.
5. Solo ora chiudi la sessione.

Questo riassunto è il punto di ripartenza della prossima sessione. È il pezzo che evita di perdere il lavoro come è successo la prima volta.

---

## Le regole d'oro (stampale mentalmente)

1. **Una task per sessione.** Sessione nuova = task nuova. Se durante una sessione ti viene in mente un'altra cosa da fare, segnala a Claude di annotarla nell'handoff e falla nella sessione successiva. Le sessioni lunghe e miste sono il modo più sicuro per far "derivare" Claude.
2. **Commit a ogni fine sessione, sempre.** Anche se hai fatto poco. Il push su GitHub è il tuo backup: il progetto è già stato perso una volta, la seconda non è ammessa.
3. **Mai saltare il rituale.** Apertura con la frase rituale, chiusura con l'handoff. Sempre. Anche quando hai fretta. Soprattutto quando hai fretta.
4. **Tu approvi, Claude propone.** Claude ti presenterà piani prima di scrivere codice e ti chiederà il permesso per i comandi: leggili, e approva solo se ti tornano. Se qualcosa non ti torna, dillo. Il progetto è tuo.
5. **Niente dati veri di clienti nelle sessioni di sviluppo.** Per le prove si usano solo dati inventati.

---

## Se qualcosa va storto

### Claude "deriva" (fa cose strane, complica tutto, ignora le regole)

Capita: a metà sessione Claude inizia a proporre cose non richieste o troppo complicate. Non serve ricominciare: incolla questa **frase di stop**, indicando la sezione delle regole che sta violando:

> **Stop. Rileggi la sezione 2 di REGOLE.md e rifai seguendola.**

(Sostituisci il numero con la sezione giusta: 1 = Disciplina, 2 = Semplicità, 3 = Consiglio ridotto, 4 = Design. Le trovi nel file `02`.)

Se dopo la frase di stop continua a derivare: chiudi la sessione, esegui il rituale di chiusura (l'handoff registra anche le cose andate storte) e riparti in una sessione nuova dal punto in cui eri.

### Una sessione si perde (chiusa per errore, app andata in crash)

Niente panico: se avevi fatto il rituale di chiusura dell'ultima sessione buona, non hai perso nulla di strutturale.

1. Apri una **sessione nuova** in Code sulla cartella del repository.
2. Incolla la frase rituale di apertura.
3. Poi scrivi: *"Leggi il file HANDOFF.md nel repository e riprendiamo dal PROSSIMO PASSO indicato lì."*

L'ultimo `HANDOFF.md` salvato su GitHub contiene lo stato del progetto e il passo esatto da cui ripartire.

### Il computer si rompe o viene resettato (lo scenario già vissuto)

È il motivo per cui esiste GitHub. Segui la procedura **"Ripristino dopo disastro"** nel file `07_HANDOFF_TEMPLATE.md`, sezione D: su un computer nuovo (o ripristinato) reinstalli Claude Desktop e GitHub Desktop, scarichi il repository da GitHub, apri Code sulla cartella e riparti dall'ultimo handoff. Il lavoro perso sarà al massimo quello dell'ultima sessione non salvata.

---

*Ultima raccomandazione: la costanza batte l'eroismo. Sessioni corte, rituali rispettati, salvataggi frequenti. È così che questo progetto arriva in fondo.*
