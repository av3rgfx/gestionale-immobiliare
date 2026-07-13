# Skill del progetto — provenienza e regole d'uso

Questa cartella contiene le skill installate nel progetto (caricate in automatico da Claude Code).

**Regola d'oro:** le skill sono **strumenti**, non regole. La fonte normativa del progetto resta
`REGOLE.md` nella root (che le distilla nelle sue 4 sezioni, come deciso dal consiglio C2);
in caso di conflitto tra una skill e `REGOLE.md`, vince `REGOLE.md`.

| Skill | Provenienza | Uso nel progetto |
|---|---|---|
| `llm-council` | Conversione in skill di [karpathy/llm-council](https://github.com/karpathy/llm-council) (webapp) | Decisioni bloccanti, modifiche ADR, checkpoint pre-sprint pesanti (file 02, sez. D) |
| `brainstorming`, `writing-plans`, `executing-plans`, `test-driven-development`, `systematic-debugging`, `subagent-driven-development`, `dispatching-parallel-agents`, `requesting-code-review`, `receiving-code-review`, `verification-before-completion`, `finishing-a-development-branch`, `using-git-worktrees`, `using-superpowers`, `writing-skills` | [obra/superpowers](https://github.com/obra/superpowers) | Metodo di sviluppo (è l'origine di REGOLE.md §1 Disciplina) |
| `ponytail`, `ponytail-review`, `ponytail-audit`, `ponytail-debt`, `ponytail-gain`, `ponytail-help` | [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | Anti-overengineering (è l'origine di REGOLE.md §2 Semplicità) |
| `impeccable` | [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | Design del frontend negli sprint S2 e S6 (è l'origine di REGOLE.md §4 Design) |

Le licenze dei progetti importati sono in `LICENZE/`.
Installate nello Sprint 0; aggiornarle significa ricopiarle dai repo di origine con un commit dedicato.
