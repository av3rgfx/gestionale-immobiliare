# HANDOFF — Riassunto di chiusura sessione

## 1. Data e numero sessione
14/07/2026 — **Sessione di progettazione** (pre-sprint), eseguita in Claude Code (ambiente remoto, branch `claude/regole-summary-vcxi65`). Tenuti due Consigli LLM: **C9** e **C10**.

## 2. Stato attuale del progetto (una riga)
Progettazione consolidata: **70 ADR** approvati (C1–C10), architettura e roadmap aggiornate; **nessuna riga di codice ancora scritta** (Sprint S0 non iniziato). Lavoro su branch `claude/regole-summary-vcxi65`, **PR aperta verso `main`** (da fondere).

## 3. Cosa è stato fatto in questa sessione (con i file)
- **Due Consigli LLM** via skill `llm-council` (advisor/Chairman/Progettista su **Fable 5**, ricerca web con fonti; certificazione superata — C9: 82 citazioni anonime, C10: 161):
  - **C9** — modalità Chiamata vocale di JARVIS + **versione mobile** + **Tailscale** + valutazione di 5 tool GitHub (databasement, bklit-ui, anime.js, NVIDIA/personaplex, livekit/agents).
  - **C10** — **auto-tagging dei moduli importati** + **dizionario canonico** dei tag (auto-compilazione).
- Record in `08_VERBALI_CONSIGLI/`: `C9_verdetto.md`, `R7_chiamata_mobile_brief.md`, `C10_verdetto.md`, `R8_autocompilazione_brief.md`; indice `LEGGIMI_VERBALI.md` aggiornato.
- **ADR recepiti** in `03_DECISIONI_CONSIGLIO.md`: **ADR-55…63** (C9) e **ADR-64…70** (C10), indice e tabella riassuntiva aggiornati.
- `04_ARCHITETTURA.md`: deroga n.2 Tailscale; §4.8 Chiamata; §10 (mobile PWA, hardening Tailscale, stack voce, HITL a voce); §3.15 CampoCanonico (Dizionario); §5.1 templatizzazione assistita; righe stack; range ADR→70; verifiche.
- `05_ROADMAP_SPRINT.md`: sprint **S-Mob** (mobile PWA, pre-go-live), **S6-bis** (Chiamata, subito dopo S6), **S2** esteso (templatizzazione + dizionario + invariante), ambienti e verifiche esterne C9/C10.

## 4. Decisioni prese e perché (breve)
- **5 tool GitHub: nessuno adottato.** personaplex richiede GPU NVIDIA (no Apple Silicon); livekit è il migliore dei due ma è un secondo servizio sempre acceso → solo riferimento di pattern; databasement/bklit-ui incompatibili/ridondanti; anime.js non necessario (orb/waveform nativi).
- **Modalità Chiamata: sì**; a voce solo lettura + dettatura proposte in coda, **scritture mai a voce** (HITL a video, ADR-07). Promossa a **canale di primo piano subito dopo S6** (S6-bis, decisione utente), non "Fase 3".
- **Mobile = PWA responsive** sullo stesso FastAPI via **Tailscale** (trasporto, non autenticazione; login+ruoli restano); deroga dichiarata come per l'SMTP.
- **Auto-compilazione moduli: idea buona, con correzione chiave** — **l'LLM non scrive mai nel file**: rilevamento/inserimento tag **deterministici**, **invariante di non-alterazione** bloccante, **dizionario canonico** a oggetti (ruolo-binding, campi atomici), LLM solo **classificatore** da S6 e condizionale; nessun file dell'agenzia sul cloud.

## 5. Criterio di accettazione della task
**Rispettato.** La richiesta (valutare tool e idee con `/llm-council` e recepire se approvato) è stata soddisfatta: Consigli tenuti e certificati, decisioni **approvate dall'utente** e scritte negli ADR-55…70. Nessun codice (fase di progettazione).

## 6. Problemi aperti (rimandati / da verificare)
- **Correzione già applicata in questa sessione:** i due brief di ricerca erano stati creati come R5/R6 duplicando la numerazione della sessione 2 (R5_inference, R6_hardware) → **rinominati in `R7`/`R8`** e riferimenti aggiornati ovunque.
- La **bozza operativa del Progettista di C10** non è stata generata (limite di sessione temporaneo); il verdetto del Chairman è completo e autosufficiente → non bloccante.
- **Verifiche esterne da calendarizzare:** C9 → DPA Tailscale + registro trattamenti, DPIA leggera (voce+remoto+AI), licenza voce TTS, retention trascrizioni, parere art. 173 CdS; C10 → gate S2 esteso (recall/precision parser + invariante), gate S6 condizionale (LLM-assist), allineamento dizionario alle release RLI. Restano valide le verifiche preesistenti (modello LLM, l.431/98, bake-off OCR, AML, DPIA).
- **Ereditata dalla sessione 2:** decisione **quale Mac di produzione comprare** prima di S6 (brief `R6_hardware_brief.md`).
- **Walking skeleton** (RAM/latenza voce sul Mac Mini) resta gate tecnico prima di costruire la Chiamata (S6-bis).

## 7. PROSSIMO PASSO (azione esatta)
1. **Far revisionare e fondere la PR** del branch `claude/regole-summary-vcxi65` in `main` (porta in `main` la progettazione C9/C10).
2. Poi, in una **sessione nuova** di Code: frase rituale di apertura + prompt `06_PROMPT_SPRINT/S0_fondamenta.md` per avviare lo **Sprint S0 — Fondamenta** (repo/regole/ambiente dev/astrazione LLM/eval skeleton/bozza backup).
3. In parallelo, **calendarizzare** le verifiche esterne del punto 6 e la **decisione hardware**.

## 8. Comandi per riprendere (dopo il merge della PR)
```bash
cd ~/Documenti/gestionale-immobiliare
git checkout main
git pull origin main
# poi, in una sessione NUOVA di Code, la frase rituale:
#   "Leggi REGOLE.md e riassumilo in 5 righe prima di toccare codice."
# quindi incollare il prompt di 06_PROMPT_SPRINT/S0_fondamenta.md
```
