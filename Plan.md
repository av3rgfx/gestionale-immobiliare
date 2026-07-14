# Plan.md — Cruscotto del progetto

*Un solo posto per capire dove siamo. Si aggiorna a ogni chiusura di sessione, insieme a `HANDOFF.md` (che racconta la singola sessione; qui c'è il quadro d'insieme). I dettagli degli sprint sono in `05_ROADMAP_SPRINT.md`; le decisioni vincolanti in `03_DECISIONI_CONSIGLIO.md`.*

**Ultimo aggiornamento:** 14/07/2026 — sessione di riordino della progettazione.

## Stato in una riga

Progettazione completa e riallineata (10 consigli, 70 ADR); Sprint S0 quasi finito (scaffold in `main`, restano i passi sul Mac); il vero sviluppo inizia con S1.

## PROSSIMO PASSO (l'azione esatta)

1. Far revisionare e **fondere la PR** di questo branch in `main`.
2. Sul Mac, in una **sessione nuova** di Code: frase rituale di apertura + prompt `06_PROMPT_SPRINT/S0_fondamenta.md` per **completare i residui S0** (lo scaffold esiste già: il prompt verifica e completa ciò che manca — vedi checklist sotto).
3. Chiuso S0 → sessione nuova con il prompt `06_PROMPT_SPRINT/S1_core_gestionale.md`.

## Tracker sprint

| Sprint | Cosa | Stato | Prompt pronto? |
|---|---|---|---|
| Progettazione | Consigli C1–C10, ADR-01…70, architettura, roadmap | ✅ fatta | — |
| **S0 — Fondamenta** | Repo, regole, ambiente dev, astrazione LLM, eval, backup bozza | 🔨 **quasi finito** (vedi residui) | ✅ |
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

## Residui S0 (da fare sul Mac, con il prompt S0)

- [ ] Ambiente dev: Homebrew, Python 3, LibreOffice, font Liberation, virtualenv + `requirements.txt`.
- [ ] Cartella dati `~/Gestionale/` (script `setup/crea_cartella_dati.sh`).
- [ ] `config.toml` compilato da `config.example.toml` (chiave del provider cloud di sviluppo).
- [ ] Test di connessione reale al provider (`llm/test_connessione.py`): risposta del modello visibile.
- [ ] Eval suite eseguita sul provider vero (finora solo modalità prova) e casi portati da 6 a 10–15.
- [ ] Backup provato davvero: `scripts/backup_db.sh` + ripristino su copia di prova (quando esisterà `db.sqlite`, in S1, oppure con un db di prova).

*(Fatti: repo+harness su GitHub ✅, `REGOLE.md` ✅, `CLAUDE.md` ✅, astrazione provider ✅, eval skeleton ✅, bozza backup ✅.)*

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
