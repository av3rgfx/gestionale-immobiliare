# HANDOFF — Riassunto di chiusura sessione

## 1. Data e numero sessione
14/07/2026 — **Sprint S0 (completamento residui lato‑repository)**, eseguita in Code in **ambiente remoto/cloud Linux** (non sul Mac dell'utente), branch `claude/regole-summary-krvr30`.

## 2. Stato attuale del progetto (una riga)
S0 quasi finito: tutto il lavoro **lato‑repository è completato e verificato qui**; restano solo i passi che richiedono il **Mac dell'utente e la sua chiave API** (installazioni, cartella dati reale, test AI reale, eval sul provider vero, backup reale).

## 3. Cosa è stato fatto in questa sessione (con i file)
- **Verifica sessione 1 (Task 1):** harness completa (`00`–`08` + `06_PROMPT_SPRINT/`), `REGOLE.md`, `CLAUDE.md`, `HANDOFF.md` presenti; `CLAUDE.md` rimanda correttamente a `REGOLE.md`. Nessun file mancante.
- **Eval portate da 6 a 12 casi (Task 5):** creati `evals/casi/07_ruoli.json`, `08_conferma_umana.json`, `09_backup.json`, `10_scadenza_trigger.json`, `11_determinismo.json`, `12_dati_sintetici.json` (italiano, dati sintetici, ognuno legato a un ADR). Runner verificato in modalità prova: 12/12 casi letti e report generato.
- **`README.md` ampliato (Task 3):** documenta che tutti i dati vivono in `~/Gestionale/` (con struttura), la configurazione via `config.toml` (segreti fuori da Git), l'avvio sul Mac e la procedura di backup + ripristino di prova.
- **`scripts/backup_db.sh` completato (Task 6):** aggiunte nell'output le istruzioni del **test di ripristino** su copia di prova.
- **Pulizia:** `.gitignore` ora ignora `evals/report_*.md` (sono output); rimosso il report vecchio `evals/report_20260713_1708.md` committato per errore.
- **Verifiche eseguite qui (prove reali):** `requirements.txt` installa in venv pulito (openai 2.45); tutti i `.py` compilano; `provider.py` senza `config.toml` dà l'errore guidato in italiano (nessuna chiave usata); `crea_cartella_dati.sh` crea la struttura attesa; flusso **backup → integrity_check → riapertura con dati** dimostrato con il motore SQLite (equivalente allo script).
- **Non toccati (già corretti):** `llm/provider.py`, `llm/test_connessione.py`, `evals/esegui_evals.py`, `setup/installa_mac.sh`, `setup/crea_cartella_dati.sh`, `config.example.toml`, `requirements.txt`.

## 4. Decisioni prese e perché (breve)
- **Sessione in cloud, non sul Mac:** i passi macchina‑specifici (Homebrew/LibreOffice/font, `~/Gestionale/` reale, test con chiave, eval sul provider vero, backup reale) **restano all'utente sul Mac** — la chiave API non entra mai nel cloud (ADR‑05). Segnalato all'utente e approvato prima di procedere (REGOLE §1).
- **12 casi eval (dentro il range 10–15):** sufficienti per lo skeleton, niente lavoro extra «già che ci siamo» (REGOLE §2).
- **Report eval fuori da Git:** sono output rigenerabili, non codice (REGOLE §2).
- **Nessuna riscrittura del codice già funzionante** (provider/test/runner): si tocca solo ciò che serve (REGOLE §2).
- **Destinazione offsite del backup non ancora scelta:** da decidere insieme quando si prova sul Mac (disco esterno o cloud cifrato), come chiede il prompt.

## 5. Criterio di accettazione della task
**Parzialmente rispettato.** Rispettato e verificato **tutto ciò che è lato‑repository**: harness completa e `CLAUDE.md`→`REGOLE.md`; eval con 12 casi + report; `scripts/backup_db.sh` con istruzioni di ripristino (flusso provato qui); `README` che documenta `~/Gestionale/`. **Non completabili dal cloud** (mancano il Mac e la chiave): «risposta del modello in italiano» dal test AI, «eval sul provider vero», «`~/Gestionale/` esiste» sul Mac, «backup con file nella destinazione» sul Mac. Per questi è fornito un runbook (punto 8).

## 6. Problemi aperti (rimandati / da verificare)
- **Da fare sul Mac (runbook):** ambiente dev, creazione `~/Gestionale/`, `config.toml` compilato, test di connessione reale, eval sul provider vero, backup + ripristino reale.
- **Scelta della destinazione offsite** del backup (disco esterno / cloud cifrato).
- **Nota tecnica:** il binario `sqlite3` non era installabile nel container cloud; il backup è stato provato col motore SQLite via Python (equivalente). Su macOS il binario `sqlite3` è già incluso: lo script gira così com'è.
- **Nota tecnica:** `provider.py` usa `tomllib`, disponibile da Python ≥3.11; `setup/installa_mac.sh` installa Python 3.12 → compatibile.

## 7. PROSSIMO PASSO (azione esatta)
Sul **Mac**, in una **sessione nuova** di Code sulla cartella del repository (dopo `git pull`), eseguire il runbook S0 in ordine e verificare i 5 criteri di accettazione:
1. `bash setup/installa_mac.sh`
2. `bash setup/crea_cartella_dati.sh`
3. `cp config.example.toml config.toml` → aprire `config.toml` e compilare `base_url`, `model`, `api_key` del provider cloud
4. `./.venv/bin/python llm/test_connessione.py` (deve stampare una risposta in italiano)
5. `./.venv/bin/python evals/esegui_evals.py` (deve produrre un report con l'esito dei 12 casi)
6. Backup: quando esisterà `db.sqlite` (S1) o con un DB di prova, `bash scripts/backup_db.sh` e seguire le istruzioni di ripristino stampate.
Poi chiudere S0 e passare a `06_PROMPT_SPRINT/S1_core_gestionale.md`.

## 8. Comandi per riprendere (sul Mac)
```bash
cd ~/Documenti/gestionale-immobiliare
git checkout claude/regole-summary-krvr30   # oppure main, dopo il merge della PR
git pull
# poi, in una sessione NUOVA di Code, la frase rituale:
#   "Leggi REGOLE.md e riassumilo in 5 righe prima di toccare codice."
# quindi eseguire i passi 1-6 del PROSSIMO PASSO qui sopra.
```
