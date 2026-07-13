# BRIEF RICERCA R1 — Verifica skill citate dall'utente (fatti verificati con fonti)

## Esiti verifica repo (tutti visitati in diretta)
1. **karpathy/llm-council** — ESISTE (22.6k★) ma NON è una skill: è una web app locale standalone che richiede OpenRouter (API a pagamento). Non imponibile come regola di progetto. Alternativa in formato skill: `tenfoldmarc/llm-council-skill` (524★, maturità bassa, formato incerto). Fonte: https://github.com/karpathy/llm-council
2. **obra/superpowers** — ESISTE (253k★, attivissimo, v6.1.1). Metodologia di sviluppo disciplinato (brainstorming → piano → TDD → review). Gira nativamente solo su **Claude Code**; su Claude Desktop va replicata come istruzioni di progetto. Fonte: https://github.com/obra/superpowers
3. **DietrichGebert/ponytail** — ESISTE (81.3k★). NON è uno strumento backend: è un **ruleset anti-overengineering generale** (semplicità, niente astrazioni premature). Ha installazione documentata anche per app desktop. Fonte: https://github.com/DietrichGebert/ponytail
4. **pbakaus/impeccable** — ESISTE (45.9k★, attivo). Skill design UI/UX, scelta legittima. Per internal tool "a prova di stupido": coppia consigliata impeccable (ramo product) + vercel web-design-guidelines (https://github.com/vercel-labs/agent-skills, 29k★); alternativa unica: ui-ux-pro-max (https://github.com/nextlevelbuilder/ui-ux-pro-max-skill, 105k★).

## Extra verificati
- **github/spec-kit** (120k★): la sua "constitution" è il meccanismo più pulito per regole fisse versionate nel repo. Fonte: https://github.com/github/spec-kit
- **bmad-code-org/BMAD-METHOD** (43k★+): più pesante, per team strutturati.

## Fatto strutturale
Le skill NON si sincronizzano tra Claude Code e Claude Desktop (fonte: docs Anthropic). Per sviluppo serio multi-sessione con queste metodologie, Claude Code è l'ambiente tecnicamente corretto; ma la struttura repo-first (regole come file nel repo) rende la migrazione un'opzione gratuita in qualsiasi momento.

## Decisione presa dal Consiglio C2 (vedi C2_verdetto.md)
REGOLE.md ≤60 righe nel repo + stesso testo nelle istruzioni di progetto Claude Desktop; 4 sezioni: disciplina (superpowers distillato), semplicità (ponytail), consiglio ridotto (template 10 righe invece del council completo), design (solo impeccable come checklist). Rituale d'apertura a ogni sessione + handoff di chiusura. No Claude Code ora, rivalutare dopo 2 settimane.
