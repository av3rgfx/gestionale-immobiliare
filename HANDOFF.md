# HANDOFF — Riassunto di chiusura sessione

## 1. Data e numero sessione
14/07/2026 — **Sprint S0 (Fondamenta) — chiusura dei residui SUL MAC dell'utente**, eseguita in Code sul MacBook, branch `main`. Questa è la sessione che ha eseguito il runbook macchina‑specifico lasciato in sospeso dalla sessione precedente (che girava in cloud).

## 2. Stato attuale del progetto (una riga)
**S0 COMPLETATO:** tutti e 5 i criteri di accettazione sono stati verificati sul Mac (ambiente dev installato, cartella dati creata, test AI in italiano, eval 12/12, backup + ripristino provati). Il vero sviluppo del gestionale inizia con S1.

## 3. Cosa è stato fatto in questa sessione (con i file)
- **Ambiente di sviluppo (Task 2):** eseguito `setup/installa_mac.sh` → Python **3.12.13** (via Homebrew, il Python di sistema 3.9 resta intatto), **LibreOffice** già presente, **font Liberation** installati (12 file in `~/Library/Fonts/`), virtualenv `.venv` creato con le dipendenze di `requirements.txt` (**openai 2.45.0**).
- **Cartella dati (Task 3):** eseguito `setup/crea_cartella_dati.sh` → creata `~/Gestionale/` con `templates/`, `documenti/`, `backup/`, `logs/` (il `db.sqlite` nascerà in S1).
- **Provider LLM (Task 4):** creato `config.toml` da `config.example.toml` (ignorato da Git). Compilato per **Google AI Studio** (endpoint compatibile OpenAI `https://generativelanguage.googleapis.com/v1beta/openai/`, modello `gemini-2.5-flash`); la **chiave l'ha inserita l'utente** direttamente nel file. Eseguito `llm/test_connessione.py` → il modello ha **risposto in italiano** ("Sono un modello linguistico… addestrato da Google").
- **Eval suite (Task 5):** eseguito `evals/esegui_evals.py` sul **provider vero** → **12/12 casi superati**; report in `evals/report_20260714_2115.md` (ignorato da Git perché output rigenerabile).
- **Backup (Task 6):** provato `scripts/backup_db.sh` su un **DB di prova con dati sintetici** (tabella `soggetto`, 2 righe finte) → copia consistente in `~/Gestionale/backup/db_20260714_211707.sqlite`, integrità `ok`; eseguito il **test di ripristino** (copia usa‑e‑getta in `/tmp`, `integrity_check` = ok, tabelle e dati ritrovati, copia rimossa).
- **Chiusura:** aggiornati `HANDOFF.md` (questo file) e `Plan.md` (cruscotto).

## 4. Decisioni prese e perché (breve)
- **Provider di sviluppo = Google AI Studio, modello `gemini-2.5-flash`:** scelta dell'utente; l'endpoint è OpenAI‑compatible, quindi funziona con l'astrazione a due parametri `base_url`/`model` senza toccare il codice (ADR‑48). Passare a Ollama locale (da S6) = solo cambio di `config.toml`.
- **La chiave l'ha inserita l'utente, non Claude:** per policy di sicurezza Claude non scrive chiavi API nei file; ha compilato solo `base_url`/`model` (non segreti) e guidato l'utente a incollare la chiave nel file.
- **Backup provato con DB di prova sintetico:** il `db.sqlite` reale nasce in S1 e verso il cloud/dischi non deve passare alcun dato reale (ADR‑05/ADR‑06). Il flusso `sqlite3 .backup` → `integrity_check` → riapertura è stato dimostrato per intero.
- **Destinazione offsite del backup: rinviata ("decido dopo"):** non bloccante per S0; va fissata prima di S3 (quando l'offsite diventa automatico e iniziano i dati veri).

## 5. Criterio di accettazione della task
**RISPETTATO (tutti e 5).**
1. Harness (00–08 + `06_PROMPT_SPRINT/`), `REGOLE.md`, `CLAUDE.md`→`REGOLE.md`, `HANDOFF.md`: presenti nel repo (verrà tutto su GitHub col push di chiusura). ✅
2. Test AI: risposta del modello **in italiano** nell'output. ✅
3. Eval suite: report con esito per ciascun caso (**12/12**). ✅
4. Backup: file trovato in `~/Gestionale/backup/`; ripristino su copia di prova che si riapre con i dati. ✅
5. `~/Gestionale/` esiste con la struttura prevista. ✅

## 6. Problemi aperti (rimandati / da verificare)
- **Destinazione offsite del backup** (disco esterno cifrato / cloud cifrato): da scegliere insieme **prima di S3**.
- **Sicurezza chiave API:** nella prima risposta in chat era comparsa una chiave Google; l'utente ha poi inserito nel file una chiave **diversa**. Raccomandazione: **revocare/rigenerare** in Google AI Studio la chiave comparsa in chat, per prudenza.
- **Backup di prova lasciato** in `~/Gestionale/backup/db_20260714_211707.sqlite` (solo dati sintetici): rimovibile quando si vuole; in S1 arriverà il primo backup reale.
- **Nome modello:** `gemini-2.5-flash` ha funzionato oggi; se il provider cambiasse i nomi, basta aggiornare `model` in `config.toml`.

## 7. PROSSIMO PASSO (azione esatta)
S0 è chiuso. In una **sessione nuova** di Code sul repo (dopo `git pull`), incollare la frase rituale di apertura e poi il prompt `06_PROMPT_SPRINT/S1_core_gestionale.md` per iniziare **S1 — Core gestionale**: scaffold FastAPI + SQLite in modalità WAL, prime tabelle del modello dati (`04_ARCHITETTURA.md` §3), login con i 4 ruoli, audit log immutabile, CRUD soggetti/immobili con presidio APE. **Prima di codificare S1:** definire con l'agenzia la matrice permessi dei 4 ruoli (verifica esterna più vicina, vedi `Plan.md`).

## 8. Comandi per riprendere (sul Mac)
```bash
cd ~/Documents/GitHub/gestionale-immobiliare
git pull
# poi, in una sessione NUOVA di Code, la frase rituale:
#   "Leggi REGOLE.md e riassumilo in 5 righe prima di toccare codice."
# quindi incollare il prompt: 06_PROMPT_SPRINT/S1_core_gestionale.md

# Per rilanciare al volo i test di S0 (ambiente già pronto):
./.venv/bin/python llm/test_connessione.py     # risposta del modello in italiano
./.venv/bin/python evals/esegui_evals.py        # report 12/12 in evals/report_*.md
```
