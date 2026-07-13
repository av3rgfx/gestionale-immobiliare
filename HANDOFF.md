# HANDOFF — Riassunto di chiusura sessione

## 1. Data e numero sessione

13/07/2026 — **Sessione 2 (JARVIS personale: consiglio C8 + ricerche hardware/engine)**, eseguita in Claude Code (ambiente remoto, branch di lavoro `claude/regole-summary-f2y0pj`). La sessione 1 (Fondamenta) è chiusa e fusa in `main` con la PR #1.

## 2. Stato attuale del progetto (una riga)

Progettazione estesa e consolidata: JARVIS come assistente personale del Proprietario è ora normato (ADR-50…54, sprint S9/S10 dopo il go-live); resta aperta **una sola decisione: quale Mac comprare** (prima di S6), più il setup fisico sul Mac di sviluppo ereditato dalla sessione 1.

## 3. Cosa è stato fatto in questa sessione

- **PR #1 fusa in `main`** (harness, consiglio C7, skill, scaffold S0); branch di lavoro riallineato.
- **Richieste del proprietario su JARVIS** (accesso esclusivo, "secondo cervello", auto-skill, automazioni con n8n, "Graphify") passate al metodo completo: 2 brief di ricerca fattuale (**R3** memoria, **R4** automazioni) → **Consiglio C8** via skill llm-council (5 advisor → peer review anonima → chairman) → verdetto applicato integralmente con approvazione dell'utente.
- **Nuovi ADR-50…54** nel file `03` + verbale `C8_verdetto.md` + nuove sezioni **§4.6 (memoria)** e **§4.7 (automazioni)** + entità **Ricordo/Automazione** nel `04` + **sprint S9 "JARVIS personale" e S10 "Trigger email"** (Fase 2, dopo il go-live) nel `05`.
- **Domande su engine DS4 e hardware**: 2 brief di ricerca (**R5** DS4/antirez, **R6** hardware 2026 con prezzi verificati) + consiglio ridotto presentato all'utente.
- **Commit** (tutti pushati): `4eafe63` (R3/R4), `f3f2eeb` (pacchetto C8), `9226ede` (R5/R6) + questo handoff.

## 4. Decisioni prese e perché

- **ADR-50**: chat JARVIS solo per il ruolo Proprietario; coda «Da approvare» separata; **un solo approvatore competente per tipo di azione** (la doppia firma segretaria+proprietario è bocciata: rubber-stamping).
- **ADR-51**: memoria «Cose da ricordare» = tabella in SQLite + FTS5 + sqlite-vec + bge-m3 via Ollama (Graphiti/Neo4j e mem0 scartati, evidenze R3); ricordi solo da dettatura confermata (anti-avvelenamento); oblio = cancellazione fisica.
- **ADR-52**: le skill si chiamano **«Procedure»** in UI (mai "skill"); v1 solo su richiesta esplicita; approva solo il Proprietario; mai testo da contenuti esterni.
- **ADR-53**: motore automazioni **interno** a catalogo chiuso QUANDO/SE/ALLORA (n8n scartato all'unanimità, evidenze R4); dry-run, nasce disattivata, anti-tempesta, tutto in AuditLog.
- **ADR-54**: trigger email solo in S10, con difese architetturali anti prompt-injection (allowlist mittenti, Keychain, sintesi senza tool, HITL su ogni azione).
- **DS4 (antirez) verificato e NON adottato** (brief R5): esiste davvero ma è mono-modello (DeepSeek V4 Flash 284B), richiede 96–128 GB, è beta senza release, bug che blocca il Mac. **Si resta su Ollama**; in S6 usare le **quant Unsloth Dynamic 2.0** del modello scelto (stessa idea di quantizzazione, matura, zero rischio). Rivalutare DS4 tra 12+ mesi.

## 5. Criterio di accettazione della task

**Rispettato**: tutte le idee del proprietario sono passate dal consiglio (C8) come richiesto, con verdetto motivato (accolte/ridimensionate/scartate), formalizzate in ADR e roadmap, committate e pushate. Le due domande (DS4, hardware) hanno brief con fonti e raccomandazione; la scelta hardware resta volutamente all'utente.

## 6. Problemi aperti

- ⚠️ **DECISIONE APERTA — quale Mac di produzione comprare (entro l'inizio di S6, ADR-48).** Il piano scritto ("Mini M4 base 24 GB") è superato: troppo lento per il 27B (~4–5 tok/s) e tagli RAM ritirati dal listino (crisi DRAM 2026). Candidate (prezzi Italia verificati, brief R6):
  - **A** — Mini M4 Pro 24 GB, 1.929 € (RAM al pelo, niente crescita)
  - **B** — Mini M4 Pro 48 GB, ~2.400–2.600 € ⭐ raccomandata (27B/32B veloci, margine per S9/S10)
  - **C** — Studio M3 Ultra 96 GB, 6.399 € (70B+/120B; ordinare 9–10 settimane prima)
  Alla scelta: aggiornare `04` §4.1 + nota datata sotto ADR-48 (se si esce dal perimetro "Mac Mini", convocare il consiglio).
- **PR verso `main`** con il lavoro di questa sessione: aperta a fine sessione (vedi PROSSIMO PASSO) — da approvare e fondere su GitHub.
- Ereditati dalla sessione 1: **setup sul Mac di sviluppo** (comandi in §8); **provider cloud di sviluppo da scegliere** (chiave in `config.toml`, mai su Git); bozza DPIA prima di S3; conferma AML su ADR-49 in S5.
- I prompt di sprint `S9`/`S10` in `06_PROMPT_SPRINT/` si scriveranno quando la Fase 2 si avvicina.
- Nota S6: pagina «cosa NON fa JARVIS» da approvare per iscritto + validatore del prototipo chat = Proprietario (verbale C8).

## 7. PROSSIMO PASSO

1. **Fondere la PR** di questa sessione su GitHub (branch `claude/regole-summary-f2y0pj` → `main`).
2. **Decidere il Mac** (A/B/C, dati nel brief `08_VERBALI_CONSIGLI/R6_hardware_brief.md`) — serve prima di S6, ma non blocca S1–S5.
3. **Setup sul Mac di sviluppo** (comandi in §8) per chiudere davvero S0.
4. Aprire la **sessione S1** con la frase rituale + `06_PROMPT_SPRINT/S1_core_gestionale.md`.

## 8. Comandi da eseguire per riprendere (sul Mac, dalla cartella del progetto)

```bash
git pull
bash setup/installa_mac.sh
bash setup/crea_cartella_dati.sh
cp config.example.toml config.toml   # poi apri config.toml e compila i 3 valori
./.venv/bin/python llm/test_connessione.py
./.venv/bin/python evals/esegui_evals.py
bash scripts/backup_db.sh            # da provare quando esisterà il db (S1)
```
