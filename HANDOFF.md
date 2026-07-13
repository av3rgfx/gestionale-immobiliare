# HANDOFF — Riassunto di chiusura sessione

## 1. Data e numero sessione

13/07/2026 — **Sessione 1 (Fondamenta / Sprint 0)**, eseguita in Claude Code (ambiente remoto, branch di lavoro `claude/regole-summary-f2y0pj`).

## 2. Stato attuale del progetto (una riga)

Fondamenta pronte: harness completa e coerente su GitHub, 3 nuovi ADR dal consiglio C7, skill di progetto installate, scaffold di Sprint 0 (provider LLM, eval suite, backup) scritto e collaudato — resta solo il setup fisico sul Mac.

## 3. Cosa è stato fatto in questa sessione

- **Verifica repo e harness**: aggiunto il file mancante `00_LEGGIMI.md` (fornito dall'utente); verificati 01–08, `REGOLE.md` e `CLAUDE.md` (identici alle fonti nel file `02`); push funzionante.
- **Verifica di coerenza 03/04/05** (3 agenti indipendenti + verifica): nessuna contraddizione sostanziale; corretti 8 dettagli redazionali (percorso fonti → `08_VERBALI_CONSIGLI/`, cron → launchd, struttura `~/Gestionale/` completa in S0, dicitura ambiente Code).
- **Skill installate in `.claude/skills/`** (richiesta dell'utente): `llm-council` (conversione della webapp di Karpathy in skill a sub-agenti), 14 skill di superpowers, 6 di ponytail, impeccable; con licenze e `LEGGIMI.md` (la fonte normativa resta `REGOLE.md`).
- **Consiglio C7 convocato via skill llm-council** (5 advisor paralleli → peer review anonima → chairman): verdetto applicato integralmente. Nuovi file/modifiche: `08_VERBALI_CONSIGLI/C7_verdetto.md`, ADR-47/48/49 nel file `03`, patch a `02`, `04` (eccezione SMTP, Sezione APE, presidio APE, entità Task, migrazioni schema, DPIA in due tempi, riconciliazione mensile, retention differenziata) e `05` (presidi dati in S3, import dati esistenti, task AML in S5, eval locale = done di S6, retention/APE/prova utente in S7).
- **Scaffold Sprint 0** (collaudato in sessione): `llm/provider.py` + `llm/test_connessione.py` + `config.example.toml`; `evals/` (6 casi in italiano + `esegui_evals.py`, prova 6/6 con report `evals/report_20260713_1708.md`); `scripts/backup_db.sh` (collaudato: snapshot + integrity check + ripristino di prova riusciti su db di test); `setup/installa_mac.sh` e `setup/crea_cartella_dati.sh`; `requirements.txt` (solo `openai`); `.gitignore`.
- **Commit** (tutti pushati): `4459cf4`, `fd73cf2`, `14cce14`, `f15ce13`, `47fa11c` + questo handoff.

## 4. Decisioni prese e perché

- **ADR-47** (ex "ADR-13 nuovo", rinumerato): ambiente di sviluppo = sezione Code; sanata la violazione della convenzione "nuovo numero, mai modifica retroattiva".
- **ADR-48**: eval sul modello locale da S6 (criterio di done), **Mac Mini M4 da acquistare e configurare con Ollama prima di S6**; kill: se l'eval locale fallisce, S7 non parte e si cambia modello, non architettura. Sostituisce la clausola "dal secondo sprint" di ADR-05, materialmente inattuabile.
- **ADR-49**: retention differenziata delle immagini documenti (a sola estrazione → cancellate; copie AML → 10 anni cifrate e loggate); risolve il conflitto ADR-38 ↔ conservazione AML. Da confermare col consulente AML in S5.
- **Presidio APE riformulato** (verbale C7, senza nuovo ADR): pratica creabile senza APE, ma compito bloccante visibile + blocco della generazione dei documenti che la richiedono (ADR-21); esenzioni registrabili.
- **Certificazione consiglio llm-council: SUPERATA** (lavori paralleli separati, peer review per etichetta anonima, verdetto con divergenze esplicite) — il consiglio completo è certificato per le sessioni in Code (file `02`, sez. D).
- Scaffold: SDK OpenAI con `base_url`/`model` da `config.toml` (ADR-05, vince sull'impostazione di default degli strumenti); il provider cloud di sviluppo non è ancora scelto (campi vuoti nell'esempio).

## 5. Criterio di accettazione della task

**Parzialmente rispettato** (per la parte che dipende dall'ambiente remoto: tutto fatto).
- ✅ Harness completa e coerente nel repo; `REGOLE.md`+`CLAUDE.md` verificati; push ok.
- ✅ Scaffold nel repo, committato e pushato; eval suite collaudata in modalità prova (6/6); backup collaudato con ripristino di prova.
- ⏳ Non ancora fatto (serve il Mac dell'utente): setup ambiente (`setup/installa_mac.sh`), creazione `~/Gestionale/`, `config.toml` con la chiave del provider cloud e test di connessione vero.

## 6. Problemi aperti

- **I commit sono sul branch `claude/regole-summary-f2y0pj`**, non su `main`: va aperta e approvata una pull request su GitHub per portarli su `main` (finché non si fa, la frase rituale su `main` legge i file vecchi).
- **Provider cloud di sviluppo da scegliere** (e chiave API da mettere in `config.toml` sul Mac — mai su Git).
- **Bozza DPIA da calendarizzare prima di S3**; conferma consulente AML su ADR-49 in S5; acquisto Mac Mini M4 prima di S6 (ADR-48).
- Annotazioni minori dal consiglio C7 (da trattare negli sprint indicati, non ora): trigger append-only per l'audit log → decidere in S1; canale indipendente per l'alert del dead man's switch → precisare in S4; conservazione dei consensi cartacei originali → procedura d'agenzia, non software.
- Minuzie documentali lasciate volutamente così: dettagli normativi/hardware solo nel 04 (sono parametri ex ADR-45); `REGOLE.md` senza carattere di fine riga finale (nessun effetto).

## 7. PROSSIMO PASSO

**Portare i commit su `main` e fare il setup sul Mac**: (1) aprire su GitHub la pull request del branch `claude/regole-summary-f2y0pj` verso `main` e approvarla (o chiedere a Claude di aprirla); (2) sul Mac, nella cartella del progetto: `git pull`, poi `bash setup/installa_mac.sh`, `bash setup/crea_cartella_dati.sh`, `cp config.example.toml config.toml` (compilare i 3 valori del provider scelto), `./.venv/bin/python llm/test_connessione.py` e `./.venv/bin/python evals/esegui_evals.py`. Con questo, S0 è davvero chiuso e si apre la sessione di S1 (`06_PROMPT_SPRINT/S1_core_gestionale.md`).

## 8. Comandi da eseguire per riprendere (sul Mac, dalla cartella del progetto)

```bash
git pull
bash setup/installa_mac.sh
bash setup/crea_cartella_dati.sh
cp config.example.toml config.toml   # poi apri config.toml e compila i 3 valori
./.venv/bin/python llm/test_connessione.py
./.venv/bin/python evals/esegui_evals.py
bash scripts/backup_db.sh            # da provare quando esistera' il db (S1)
```
