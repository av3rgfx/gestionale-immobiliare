# Plan.md — Cruscotto del progetto

*Un solo posto per capire dove siamo. Si aggiorna a ogni chiusura di sessione, insieme a `HANDOFF.md` (che racconta la singola sessione; qui c'è il quadro d'insieme). I dettagli degli sprint sono in `05_ROADMAP_SPRINT.md`; le decisioni vincolanti in `03_DECISIONI_CONSIGLIO.md`.*

**Ultimo aggiornamento:** 14/07/2026 — sessione S0: eseguito il runbook sul Mac; **S0 completato e verificato** (5/5 criteri).

## Stato in una riga

Progettazione completa e riallineata (10 consigli, 70 ADR); **Sprint S0 COMPLETATO** (ambiente dev, cartella dati, provider LLM, eval, backup tutti provati sul Mac); il vero sviluppo inizia con S1.

## PROSSIMO PASSO (l'azione esatta)

1. Sul Mac, in una **sessione nuova** di Code: frase rituale di apertura + prompt `06_PROMPT_SPRINT/S1_core_gestionale.md` per iniziare **S1 — Core gestionale** (scaffold FastAPI + SQLite WAL, prime tabelle, login 4 ruoli, audit log, CRUD soggetti/immobili con presidio APE).
2. **Prima di codificare S1:** definire con l'agenzia la **matrice permessi dei 4 ruoli**.

## Tracker sprint

| Sprint | Cosa | Stato | Prompt pronto? |
|---|---|---|---|
| Progettazione | Consigli C1–C10, ADR-01…70, architettura, roadmap | ✅ fatta | — |
| **S0 — Fondamenta** | Repo, regole, ambiente dev, astrazione LLM, eval, backup bozza | ✅ **fatto** (verificato sul Mac) | ✅ |
| S1 — Core gestionale | Login 4 ruoli, audit log, CRUD soggetti/immobili, presidio APE | ⬜ | ✅ |
| S2 — Modulo documentale | Template CdC, templatizzazione C10, Dizionario Campi | ⬜ | ✅ |
| S3 — Privacy + Backup | Consenso immutabile, backup schedulato → **da qui dati veri** | ⬜ | ✅ |
| S4 — Scadenze locazioni | Doppio trigger 3+2, reminder, ciclo chiuso | ⬜ | ✅ |
| S5 — Proprietario & Contabilità | Movimenti automatici, dashboard, AML | ⬜ | ✅ |
| S6 — JARVIS v1 | Chat read-only (solo Proprietario), HITL, eval locale | ⬜ | ✅ |
| S6-bis — Chiamata JARVIS | Canale vocale (gate: walking skeleton) | ⬜ | ❌ da scrivere prima dello sprint |
| S7 — OCR & Adempimenti | MRZ, APE, matrice adempimenti | ⬜ | ✅ |
| S-Mob — Mobile (PWA) | PWA responsive + Tailscale (pre-go-live) | ⬜ | ❌ da scrivere prima dello sprint |
| S8 — Hardening & Go-live | Consolidamento locale, go-live | ⬜ | ✅ |
| S9 — JARVIS personale *(Fase 2)* | Memoria personale | ⬜ | ❌ da scrivere prima dello sprint |
| S10 — Trigger email *(Fase 2)* | Automazioni email | ⬜ | ❌ da scrivere prima dello sprint |

## S0 — completato (verificato sul Mac, sessione 14/07)

- [x] Ambiente dev: Python 3.12.13, LibreOffice, font Liberation, `.venv` + `requirements.txt` (openai 2.45) — `bash setup/installa_mac.sh`.
- [x] Cartella dati `~/Gestionale/` con `templates/documenti/backup/logs` — `bash setup/crea_cartella_dati.sh`.
- [x] `config.toml` compilato (Google AI Studio, `gemini-2.5-flash`; chiave inserita dall'utente, file fuori da Git).
- [x] Test di connessione reale (`llm/test_connessione.py`): **risposta del modello in italiano**.
- [x] Eval suite sul **provider vero** (`evals/esegui_evals.py`): **12/12** superati; report in `evals/report_*.md`.
- [x] Backup provato su DB di prova sintetico + **ripristino** su copia usa‑e‑getta (integrità ok, dati ritrovati).
- [x] Eval suite: 12 casi (dentro 10–15); `README.md` documenta `~/Gestionale/`; `scripts/backup_db.sh` con istruzioni di ripristino; report eval fuori da Git.

**Unico punto rinviato (non bloccante):** destinazione **offsite** del backup (disco esterno / cloud cifrato) — da fissare prima di S3.

## Verifiche esterne più vicine (tabella completa in `05_ROADMAP_SPRINT.md`)

| Verifica | Entro |
|---|---|
| Matrice permessi dei 4 ruoli da definire con l'agenzia | inizio S1 |
| Test sui 5–10 modelli reali CdC + validazione legale template + gate C10 (parser) | durante S2 |
| Bozza DPIA (art. 35 GDPR) | prima di S3 |
| Validazione legale scadenze l. 431/98 | durante S4 |

## Decisioni aperte

- **Quale Mac di produzione comprare** (brief `08_VERBALI_CONSIGLI/R6_hardware_brief.md`) — serve **prima di S6** (ADR-48).
- **Verifica esistenza del modello locale** (nome esatto, pesi, benchmark) — prima di S6.
- **Walking skeleton voce** (latenza/RAM) — gate tecnico prima di costruire S6-bis (ADR-59).

## Manutenzione di questo file

A ogni chiusura di sessione: aggiorna data, stato in una riga, PROSSIMO PASSO, e spunta ciò che è stato completato. Niente storia qui dentro (quella è nei commit e in `HANDOFF.md`): questo file descrive solo **lo stato presente**.
