# VERDETTO FINALE C2 — Chairman

> **⚠️ Nota di aggiornamento (errata, luglio 2026).** Questo verdetto si basava su due premesse risultate errate o superate: (1) "su Claude Desktop le skill installabili non esistono" — le skill girano su Web, Desktop e Claude Code; (2) "il consiglio completo è teatro di auto-consenso intra-modello perché Desktop non lancia advisor indipendenti" — i sub-agenti esistono in Claude Code e nell'app Claude Code Desktop, e la skill llm-council convertita dall'utente dichiara esplicitamente di funzionare con sub-agenti dello stesso modello e lenti di pensiero diverse (design valido per il metodo di Karpathy adattato). Le **decisioni operative del verdetto restano valide** (REGOLE.md, doppia fonte, rituali, handoff): cambia solo la collocazione del consiglio completo, che può essere convocato **dentro** le sessioni dove esistono sub-agenti reali. Regola operativa aggiornata nel file `02_REGOLE_FISSE_SKILLS.md` e addendum in `03_DECISIONI_CONSIGLIO.md` (sezione C2).

## Dove il consiglio concorda

1. **Su Claude Desktop le "skill" installabili non esistono**: niente enforcement nativo, niente CLAUDE.md auto-caricato. L'unica forma eseguibile è un file di regole versionato nel repo (Contrarian, First Principles Thinker, Executor; l'Outsider aggiunge il requisito decisivo: verificabile da chi non legge codice).
2. **Quattro metodologie integrali = overengineering del processo**. Il Contrarian coglie l'ironia: imporre ponytail (l'anti-overengineering) tramite uno stack a 4 framework contraddice ponytail stesso. Il First Principles Thinker formalizza: "applicate ponytail a ponytail".
3. **Impeccable sopravvive** in tutte le prescrizioni serie (Contrarian in forma ridotta, First Principles ed Executor intera): è l'unica che copre un gap che l'utente non può colmare da solo.
4. **L'enforcement che sopravvive alle sessioni è un rituale d'apertura fisso**, incollato dall'utente a ogni sessione (Contrarian, First Principles, Executor).
5. **spec-kit constitution e BMAD sono burocrazia** per un team di uno (Executor esplicito, gli altri impliciti).

## Dove il consiglio è diviso

- **Il council**: teatro di auto-consenso intra-modello (Contrarian) vs escalation esterna cross-modello via OpenRouter (Expansionist) vs template ridotto di 10 righe (First Principles, Executor).
- **Quante regole**: due (Contrarian), una (Outsider), tre sezioni in una pagina (First Principles), quattro sezioni ≤60 righe (Executor), cinque o più (Expansionist).
- **Enforcement**: eseguibile — test e CI (First Principles) vs rituale verbale (Contrarian, Executor) vs verifica senza leggere codice (Outsider).
- **Claude Code**: ambiente irrilevante se il file vive nel repo (First Principles) vs rinvio pragmatico di 2 settimane (Executor) vs opzione gratuita resa tale dal repo-first (Expansionist).

## Punti ciechi emersi

L'**Expansionist è il punto cieco collettivo**, segnalato da tutti e cinque i revisori: celebra l'upside, aggiunge scope (council a pagamento, "tre asset", template pubblicabile) — esattamente il pattern che ha già ucciso il progetto una volta — e non risponde mai alla domanda "come garantire il rispetto". Mancato a tutti, secondo le review: (a) **l'handoff tra sessioni** — riassunto di chiusura + commit di checkpoint — vero punto di rottura del multi-sessione; (b) l'igiene di sessione (una task per chat); (c) il protocollo di recupero quando Claude deriva a metà sessione; (d) chi scrive materialmente il file regole (Claude bozza, utente approva); (e) un controllo di conformità a 1-2 settimane.

## La raccomandazione

Adotto la diagnosi del **First Principles Thinker** con l'eseguibilità dell'**Executor**, e taglio il council come il **Contrarian**. Concretamente:

1. **Un file REGOLE.md nella root del repo, massimo 60 righe**, quattro sezioni: (a) *Disciplina* — prima piano scritto, poi criterio di accettazione, poi codice, poi review (superpowers distillato in 6 righe); (b) *Semplicità* — 6-8 regole ponytail (niente astrazioni premature, niente feature "per dopo"); (c) *Consiglio ridotto* — prima di ogni decisione architetturale, elencare 3 modi in cui fallisce e 1 alternativa più semplice: niente roleplay a 5 advisor; il council esterno via OpenRouter resta opzionale, solo per decisioni bloccanti; (d) *Design* — solo impeccable come checklist operativa, senza la coppia vercel (due fonti = paralisi: ha ragione l'Executor).
2. **Doppia fonte**: lo stesso testo incollato nelle istruzioni di progetto Desktop — se una deriva, l'altra regge. Il file è scritto da Claude nella prima sessione e approvato dall'utente.
3. **Claude Code: no, ora.** L'attrito ucciderebbe il progetto. Ma la struttura repo-first rende la migrazione gratuita: rivalutare dopo 2 settimane, se le regole reggono.
4. **Enforcement sessione per sessione**: frase d'apertura fissa — *"Leggi REGOLE.md e riassumilo in 5 righe prima di toccare codice"*. Il riassunto è la verifica che un non-sviluppatore può fare senza leggere codice (requisito dell'Outsider). A fine task, Claude produce una checklist di conformità leggibile. Se deriva a metà sessione: *"Stop. Rileggi la sezione X e rifai"*. Una task per chat, chat nuova per task nuova.
5. **Handoff**: rituale di chiusura obbligatorio — riassunto (stato, decisioni prese, prossimo passo) + commit di checkpoint; la sessione successiva apre leggendo REGOLE.md e l'ultimo riassunto. Dopo 2 settimane: controllo di conformità e revisione versionata del file.

Scartati: llm-council-skill (formato sbagliato, 524★), spec-kit constitution, BMAD, vercel web-design-guidelines. E va presa sul serio la domanda del Contrarian: l'agente AI dentro il gestionale serve davvero *ora*, o è proprio l'overengineering che ponytail esiste per impedire?

## La prima cosa da fare

Nella prossima sessione: incollare la frase d'apertura, far scrivere a Claude la bozza di REGOLE.md (≤60 righe, le 4 sezioni sopra), approvarla, committarla nel repo e incollarla identica nelle istruzioni di progetto. Tutto il resto parte da lì.
