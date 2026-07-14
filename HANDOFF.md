# HANDOFF — Riassunto di chiusura sessione

## 1. Data e numero sessione
14/07/2026 — **Sessione di riordino della progettazione** (pre-S1), eseguita in Claude Code (ambiente remoto, branch `claude/affectionate-edison-76fmij`). Eseguito un audit di coerenza dell'intera documentazione (56 agenti in parallelo, ogni segnalazione ri-verificata).

## 2. Stato attuale del progetto (una riga)
Progettazione completa e **riallineata** (C1–C10, ADR-01…70); **scaffold S0 già in `main`** (dal 13/07, PR #1) con residui da completare sul Mac; PR #3 (progettazione C9/C10) **fusa in `main`** il 14/07; il cruscotto del progetto vive ora in `Plan.md`.

## 3. Cosa è stato fatto in questa sessione (con i file)
- **Audit completo di coerenza** della progettazione: 36 incongruenze uniche confermate e corrette.
- **`CLAUDE.md` ricreato** (testo di `02` sez. A + rimando a `Plan.md`): era stato **cancellato per errore il 13/07** (commit "Delete CLAUDE.md", prevalso nel merge della PR #1) — il caricamento automatico delle regole era quindi inattivo. Il blocco prescritto in `02` sez. A è stato aggiornato in modo identico.
- **`Plan.md` creato**: cruscotto unico (stato, tracker sprint, residui S0, verifiche esterne, decisioni aperte); il rituale di chiusura in `07` ora chiede di aggiornarlo insieme all'handoff.
- **Correzioni**: `00_LEGGIMI.md` (mappa file reale, 10 consigli, prompt S0–S8, Claude Design esteso, validatore S6 = Proprietario); `01_PROMPT_MAESTRO.md` (10 consigli, ADR-01…70, file 00–08); `02` (consigli C1–C10; blocco CLAUDE.md); `03` (Fonti C1–C10; nota di superamento parziale sullo scarto "S6b" per ADR-59); `04` (nome file di backup allineato allo script); `05` (Fonte C1–C10; prompt S0–S8; regola 4 → Ollama da S6 per ADR-48; `db.sqlite` nasce in S1; parcheggio con S6-bis/S-Mob); `07` (in Code l'handoff lo salva Claude; rituale esteso a `Plan.md`).
- **Prompt di sprint allineati agli ADR**: `S0` (script `scripts/backup_db.sh`, `db.sqlite` in S1, dipendenze per sprint); `S1` (presidio APE per **ADR-21**: pratica creabile senza APE + compito bloccante + esenzione con motivo); `S2` (integrato il **Consiglio C10**: Dizionario dei Campi, templatizzazione assistita, invariante di non-alterazione, metriche di gate — ADR-64…70); `S3` (nome script backup); `S6` (prerequisito **ADR-48** Mac Mini+Ollama ed eval locale come done; validatore = **Proprietario** per **ADR-50**; demo perimetrata + pagina «cosa NON fa JARVIS» del C8; task condizionale LLM-assist **ADR-69**).

## 4. Decisioni prese e perché (breve)
- **Struttura dei file invariata** (niente rinomini/spostamenti): i rituali e i prompt citano i nomi attuali ovunque; riorganizzare avrebbe rotto la harness per pura estetica (REGOLE §2).
- **`Plan.md` come cruscotto unico**: HANDOFF racconta l'ultima sessione, Plan.md lo stato d'insieme; si aggiornano insieme a ogni chiusura.
- **Prompt di S6-bis, S-Mob, S9, S10 NON creati ora**: si scrivono prima del rispettivo sprint (niente lavoro "per dopo" — REGOLE §2); tracciato in `Plan.md`.
- **Nessun file di codice toccato**: l'audit non ha trovato incongruenze interne allo scaffold.

## 5. Criterio di accettazione della task
**Rispettato.** (1) `CLAUDE.md` esiste ed è conforme al blocco di `02` sez. A; `Plan.md` mostra stato e prossimo passo in una pagina. (2) Le frasi superate ("6 consigli", "ADR-01…ADR-46", "nessuna riga di codice", "backup.sh"…) non compaiono più (verificato con ricerca su tutto il repo). (3) I prompt S1/S2/S6 sono allineati ad ADR-21, ADR-48, ADR-50, ADR-64…70; nessun contenuto estraneo alterato.

## 6. Problemi aperti (rimandati / da verificare)
- **Residui S0** (solo sul Mac dell'utente, checklist completa in `Plan.md`): ambiente dev, `~/Gestionale/`, `config.toml`, test di connessione reale, eval sul provider vero + casi da 6 a 10–15, prova di backup/ripristino.
- **Verifiche esterne da calendarizzare** (le più vicine in `Plan.md`; tabella completa in `05`).
- **Decisione hardware** (quale Mac di produzione, brief R6) prima di S6; walking skeleton voce prima di S6-bis.

## 7. PROSSIMO PASSO (azione esatta)
1. **Far revisionare e fondere la PR** del branch `claude/affectionate-edison-76fmij` in `main`.
2. Poi, sul Mac, in una **sessione nuova** di Code: frase rituale + prompt `06_PROMPT_SPRINT/S0_fondamenta.md` per **completare i residui S0** (lo scaffold c'è già: il prompt verifica e completa).
3. Chiuso S0 → sessione nuova con `06_PROMPT_SPRINT/S1_core_gestionale.md` (**inizio del vero sviluppo**).

## 8. Comandi per riprendere (dopo il merge della PR)
```bash
cd ~/Documenti/gestionale-immobiliare
git checkout main
git pull origin main
# poi, in una sessione NUOVA di Code, la frase rituale:
#   "Leggi REGOLE.md e riassumilo in 5 righe prima di toccare codice."
# quindi incollare il prompt di 06_PROMPT_SPRINT/S0_fondamenta.md
```
