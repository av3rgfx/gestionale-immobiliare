---
name: llm-council
description: Convoca il Consiglio LLM — 5 advisor paralleli con lenti diverse, peer review anonima, verdetto del Chairman. Da usare per decisioni bloccanti, modifiche agli ADR, prima degli sprint pesanti (S2, S4, S6, S7) e prima del go-live, come definito in 02_REGOLE_FISSE_SKILLS.md sezione D. Non usare per decisioni di routine (per quelle basta il "consiglio ridotto" di REGOLE.md §3).
---

# LLM Council — consiglio a 5 advisor con peer review anonima

**Origine:** conversione in skill della webapp [karpathy/llm-council](https://github.com/karpathy/llm-council)
(query → più LLM in parallelo → review incrociata anonimizzata → risposta finale del Chairman).
**Adattamento per questo progetto** (vedi `03_DECISIONI_CONSIGLIO.md`, Addendum C2): gli advisor non sono
modelli diversi via OpenRouter ma **5 sub-agenti paralleli dello stesso modello con lenti di pensiero
diverse** — metodo Karpathy adattato, valido dove esistono sub-agenti reali (Claude Code).

**Nota di conformità:** questa skill è uno strumento. La fonte normativa del progetto resta `REGOLE.md`;
le decisioni vincolanti sono gli ADR in `03_DECISIONI_CONSIGLIO.md`.

## Quando convocarlo (checkpoint fissi, dal file 02 sezione D)

1. Prima di ogni sprint "pesante": S2 (documentale), S4 (scadenze), S6 (JARVIS), S7 (OCR).
2. Quando una decisione modifica un ADR: nessun ADR si riscrive senza un consiglio.
3. Quando il "consiglio ridotto" (REGOLE.md §3) scopre un rischio bloccante.
4. Prima del go-live (fine S8).
5. Quando si è indecisi tra opzioni con posta alta.

## Protocollo (3 fasi + verbale)

### Fase 1 — Prime opinioni (parallela)

Lancia **5 sub-agenti in parallelo** (tool Agent), tutti con: la decisione in gioco scritta in una riga,
il contesto completo (quali file del repo leggere, cosa è già deciso, cosa è in gioco) e la stessa domanda.
Ogni advisor ha però una **lente diversa**, dichiarata nel prompt:

- **Advisor 1 — Architetto pragmatico:** semplicità, manutenibilità, "la soluzione più noiosa che funziona".
- **Advisor 2 — Avvocato del diavolo:** modi concreti di fallire, ipotesi nascoste, costi sommersi.
- **Advisor 3 — Compliance e legale:** GDPR, norme di settore, responsabilità verso terzi.
- **Advisor 4 — Operatività utente:** segretaria/agenti non tecnici, "a prova di stupido", frizione reale.
- **Advisor 5 — Dati e sicurezza:** integrità, backup, audit, superficie d'attacco.

(Le lenti si adattano alla domanda quando serve, dichiarandolo nel verbale.)
Ogni advisor produce: analisi strutturata + **raccomandazione secca** (una riga) + rischi principali.
Gli advisor NON vedono le risposte degli altri in questa fase.

### Fase 2 — Peer review anonima (parallela)

Per ogni advisor, lancia un secondo passaggio: riceve le **4 risposte degli altri**, etichettate solo
**R1–R4 in ordine casuale, senza lente né identità** (anonimizzazione: nessun advisor deve poter
riconoscere o favorire una "fazione"). Deve: valutare ciascuna per accuratezza e profondità,
**citarle per lettera/etichetta**, indicare la migliore e la più debole con motivazione,
e dire se cambia la propria raccomandazione.

### Fase 3 — Verdetto del Chairman

Un **sub-agente finale (Chairman)** riceve: la domanda, le 5 risposte di Fase 1, le 5 review di Fase 2.
Produce il verdetto con questa struttura obbligatoria:

1. **Decisione raccomandata** (una riga).
2. **Motivazione** (breve, in italiano semplice).
3. **Divergenze esplicite**: chi dissente, su cosa e perché — mai un finto consenso unanime.
4. **Rischi accettati** e mitigazioni.
5. **Alternativa più semplice** considerata e perché è stata tenuta o scartata.

### Verbale (obbligatorio)

- Il verdetto si salva in `08_VERBALI_CONSIGLI/` (formato `CN_verdetto.md`, numerazione progressiva).
- Se la decisione **cambia o crea un ADR** → nuovo ADR in `03_DECISIONI_CONSIGLIO.md` (nuovo numero,
  mai modifica retroattiva). Se **conferma** l'esistente → nota nell'`HANDOFF.md`.
- L'approvazione finale è **sempre dell'utente**: il consiglio raccomanda, non decide.

## Certificazione (consiglio di prova — da fare una volta)

Il primo consiglio convocato in un ambiente nuovo è anche la prova che il meccanismo funziona.
Verifica che: (1) le 5 risposte arrivino da **lavori separati e paralleli**, non da un unico testo a 5 voci;
(2) la peer review citi le risposte **per etichetta anonima**; (3) il Chairman produca un verdetto con
**divergenze esplicite**. Se una condizione fallisce, il consiglio completo si tiene fuori dalle sessioni
(vedi file 02, sezione D). Annotare l'esito della prova in `HANDOFF.md`.
