# Verbale C7 — Revisione della progettazione prima dello sviluppo

**Data:** luglio 2026 (Sprint 0, sessione Fondamenta).
**Convocazione:** richiesta dell'utente ("passa ogni dubbio progettuale tramite skill llm-council e perfeziona la progettazione"), checkpoint conforme al file `02` sezione D (modifiche agli ADR = consiglio obbligatorio).
**Protocollo:** skill `llm-council` (conversione della webapp karpathy/llm-council): 5 advisor paralleli con lenti diverse (architetto pragmatico, avvocato del diavolo, compliance/legale, operatività utente, dati/sicurezza) → peer review anonima (etichette R1–R4) → verdetto del Chairman. 11 lavori separati in totale.
**Consiglio di prova (certificazione, file 02 sez. D):** SUPERATA — (1) risposte prodotte da lavori separati e paralleli ✓; (2) peer review con citazioni per etichetta anonima ✓; (3) verdetto del Chairman con divergenze esplicite ✓. Il consiglio completo è certificato per le sessioni di sviluppo in Code.
**Agenda:** la progettazione (03/04/05) è pronta per lo sviluppo? + 6 punti aperti (P1–P6) emersi dalla verifica di coerenza incrociata della sessione Fondamenta.
**Esito recepito in:** ADR-47, ADR-48, ADR-49 nel file `03` + patch ai file `02`, `04`, `05` (commit della stessa sessione).

---

# VERBALE C7 — VERDETTO DEL CHAIRMAN
## Revisione della progettazione prima dello sviluppo

---

### 1. Decisione raccomandata

**La progettazione è pronta per lo sviluppo a condizione di una singola sessione di allineamento documentale prima di S0** (stimata: mezza–una giornata), che emetta tre nuovi ADR e patchi 04 e 05 come sotto specificato. Nessun ridisegno architetturale.

### 2. Motivazione

I cinque advisor convergono in modo raro: l'architettura è sana, i difetti sono di **coerenza tra documenti** e di **sequenza temporale dei presidi**, non di sostanza. Poiché i prompt di sprint citano 03/04/05 come fonti vincolanti, ogni contraddizione lasciata su carta diventa codice sbagliato o rinegoziazione in sessione. Correggere ora costa ore; correggere in S5 su dati reali costa settimane. Due punti (finestra GDPR, conflitto ADR-38/AML) non sono rifiniture ma esposizione legale attiva: vanno chiusi prima del primo dato reale.

### 3. Verdetto punto per punto

**P1 — Eval suite sul modello locale.** Consenso unanime dei cinque: la clausola "dal secondo sprint" di ADR-05 è materialmente inattuabile. **Decisione: nuovo ADR-48 nel file 03** che sostituisce la sola clausola temporale di ADR-05: eval su cloud da S0 (già in roadmap); **Mac Mini M4 acquistato, configurato con Ollama e disponibile prima dell'inizio di S6**; prima esecuzione della eval sul modello locale come **criterio di done di S6**; riesecuzione a S7 e S8. Criterio di kill esplicito: se l'eval locale fallisce, S7 non parte e si cambia modello, non architettura. Beneficio collaterale (colto da più advisor): il Mac Mini da S6 fornisce anche l'hardware Apple Silicon per il bake-off OCR di S7, che il MacBook 2019 Intel non copre. Atterra anche su: 04 §4.1/§4.5, 05 regola 5.

**P2 — Finestra protezione dati S3→S8.** Consenso unanime sulla chiusura a costo quasi nullo. **Decisione: modifica al file 05** — in **S3**: FileVault attivo sulla macchina che ospita `~/Gestionale/` (funzione di sistema, zero codice), verifica che l'offsite sia davvero cifrata, riga di AuditLog a ogni consultazione/download delle scansioni consensi (infrastruttura già esistente da S1); in **S7**: retention/cancellazione immagini costruita *dentro* la pipeline OCR, con vincolo esplicito "nessun documento d'identità reale entra prima di questi presidi"; in **S8**: solo hardening e verifica. **DPIA in due tempi** (l'art. 35 la richiede *prima* del trattamento): bozza prima di S3, aggiornamento prima di S7 (che copre anche la base giuridica del corpus bake-off), chiusura formale in S8. Atterra su 05 (S3, S7, S8) + nota in HANDOFF per la bozza DPIA.

**P3 — Funzioni orfane.** Consenso unanime. **Decisione: modifica al file 05**: (a) audit consultazione etichette compliance → **S5**, dove le etichette nascono (una riga di AuditLog); (b) autenticità APE → **S7 come flusso manuale guidato** (task "verifica su SIAPE/registro regionale", esito in `stato_verifica`, con audit); integrazione automatica coi registri esplicitamente parcheggiata in Fase 2, correggendo la frase nel 04 §7; (c) adeguata verifica AML → **S5 come task bloccante all'apertura pratica** (spunta con operatore/data, traccia in audit, conservazione 10 anni), non dicitura: la riga attuale della roadmap declassa un obbligo del 04 e va riscritta.

**P4 — "Nessuna pratica senza APE".** Consenso sulla riformulazione: il blocco duro alla creazione produrrebbe APE fittizie o lavoro fuori sistema. **Decisione: riformulare, senza nuovo ADR** — pratica creabile senza APE; APE mancante/scaduto = compito bloccante ben visibile sulla pratica + **blocco della generazione dei documenti che lo richiedono** (applicazione diretta di ADR-21, zero codice nuovo); esenzione registrabile con motivo (box, ruderi, immobili esenti). Rinominare nel 04 il "Blocco APE" in **"Sezione APE"** per eliminare l'omonimia. Atterra su: 04 §3.3, 05 S1 (testo e criterio di done).

**P5 — Assenze nel 04.** Sì, integrare **prima di S1**, con parsimonia. **Decisione: modifica al file 04**: (a) riconciliazione mensile in §9 — mezza pagina: Movimenti `incassato` vs estratto banca/CSV commercialista, task guidato con differenze elencate ed esito in AuditLog, nessun collegamento bancario in v1; (b) informativa privacy = **un Template come gli altri** nella pipeline §5 (la `versione_modulo` di RecordConsenso è il `template_version_id`), allegato automatico via meccanismo pacchetto ADR-22 — nessun motore parallelo; (c) *dalla review*: **entità Task minima nel §3** (tipo, riferimento, assegnatario, scadenza, stato, esito) — quattro funzioni già decise la presuppongono — e **convenzione di migrazione schema** (script SQL numerati, backup automatico pre-migrazione) in §8, prima che S3 porti dati reali.

**P6 — Minuzie.** **Decisioni**: (a) vision LLM fallback: non sceglierlo ora; aggiungere alla tabella verifiche esterne del 04 "scelto all'esito del bake-off S7 con mini-ADR, **vincolo: deve girare in locale**" (un fallback cloud violerebbe il principio 2 con documenti d'identità); (b) sanzioni/48h/24GB solo nel 04: **va bene così** — sono parametri versionati ex ADR-45, non decisioni; (c) refuso: correggere in "riempimento deterministico"; (d) ADR-13 riusato: **rinumerare il nuovo come ADR-47** con tombstone sul vecchio 13 barrato e aggiornamento dei rimandi in 02/04/05 (dieci minuti). Atterra su: 03 (ADR-47), 04, 02, 05.

### 4. Divergenze esplicite

1. **ADR-13: rinumerare o solo annotare.** Un advisor propone la sola nota di anomalia per non rompere i riferimenti; gli altri quattro chiedono la rinumerazione, e il dissenziente stesso ha ceduto in peer review. **Risolvo per la rinumerazione (ADR-47)**: la regola "nuovo numero, mai modifica retroattiva" è scritta nel registro stesso (riga 239) e i rimandi da aggiornare sono 2-3.
2. **P4: promuovere la regola APE ad ADR autonomo?** Un advisor lo chiede (regola normativa); gli altri la considerano applicazione di ADR-21. **Risolvo contro il nuovo ADR**: è ADR-21 applicato più un compito visibile; la decisione resta tracciata in questo verbale, che è la sede formale sufficiente.
3. **DPIA in S8 vs anticipata.** In prima battuta tre advisor su cinque la lasciavano in S8; dopo la review tutti convergono sull'anticipazione. **Risolvo per la DPIA in due tempi** (bozza pre-S3): è l'unica lettura conforme all'art. 35.
4. **"Il Mac Mini esiste già".** Affermazione di un advisor smentita dai documenti (acquisto futuro). **Risolvo trattando l'acquisto come vincolo esplicito di ADR-48**: data di disponibilità prima di S6, altrimenti S6 non si chiude.

### 5. Rischi accettati e mitigazioni

- **Cifratura solo full-disk (FileVault) fino a S8**, niente SQLCipher/cifratura applicativa prima: accettato — mitigato da FileVault + accessi loggati + DPIA anticipata che può imporre di più.
- **Verifica APE manuale in v1** (niente integrazione registri): accettato — mitigato da task guidato con esito registrato; automazione in Fase 2.
- **Anticipo dell'acquisto Mac Mini** (esborso prima del collaudo finale): accettato — è l'assicurazione contro il fallimento del progetto in S8, il punto di non ritorno più costoso.
- **SMTP cloud resta** (vedi §7): accettato come eccezione dichiarata con DPA, non eliminato.

### 6. Alternativa più semplice considerata

- **P1**: "interpretare" ADR-05 senza toccarlo (eval cloud = adempimento). Scartata: lascerebbe la scoperta del modello locale a S8, esattamente il rischio che ADR-05 voleva evitare; e il registro impone la correzione formale, non l'interpretazione.
- **P2**: lasciare tutto in S8 accettando il rischio. Scartata: non è un rischio ma una non-conformità in corso d'opera; la chiusura costa quasi zero (FileVault + una riga di log).
- **P4**: togliere semplicemente la riga da S1. Scartata a metà: si toglie il blocco duro ma si tiene il compito visibile — l'APE mancante deve restare impossibile da ignorare.
- **P6d**: sola nota di anomalia su ADR-13. Scartata: un registro che viola la propria convenzione perde autorevolezza dove serve di più.

### 7. Debolezze aggiuntive da recepire (3)

1. **Conflitto ADR-38 ↔ conservazione AML decennale** (il miglior catch del giro, verificato: 03 riga 159 vs 04 riga 340). Cancellare le immagini dei documenti d'identità post-estrazione può violare il D.Lgs 231/2007. **Azione: nuovo ADR-49 nel 03** — retention differenziata per finalità: copia AML conservata 10 anni cifrata e ad accesso loggato; immagini a sola estrazione cancellate. Punto aperto: conferma del consulente AML già previsto in S5.
2. **Contraddizione SMTP ↔ principio 2 "nessun dato lascia il Mac Mini"** (04 riga 17 vs riga 41). **Azione: modifica al 04 §1** — eccezione esplicita e circoscritta per le email di notifica, DPA col provider e copertura nell'informativa, prima di S4.
3. **Nessuno sprint prevede il caricamento dei dati esistenti** (anagrafiche, contratti in corso, template depositati): è il punto in cui i gestionali muoiono. **Azione: modifica al 05** — import CSV guidato in S3 con responsabile e criterio di done ("i contratti veri sono dentro prima di S4").

**Scartate con motivo (una riga ciascuna):** trigger SQLite append-only → dettaglio implementativo giusto, si decide in S1 senza toccare la progettazione (nota in HANDOFF); rotazione backup + `integrity_check` → due righe da aggiungere al 04 §8.1 contestualmente alle patch P5, non merita punto autonomo; dead man's switch autoreferenziale e canale alert indipendente → requisito da precisare dentro S4, nota in HANDOFF; prova utente sul form S7 → una riga da aggiungere a S7 in roadmap, costo mezza giornata; base giuridica corpus bake-off → già assorbita dall'aggiornamento DPIA pre-S7 (P2); conservazione dei consensi cartacei originali → procedura operativa d'agenzia, non software (nota in HANDOFF).

---
*Verbale C7 — pronto per il salvataggio in 08_VERBALI_CONSIGLI/ e per la traduzione in modifiche a 03 (ADR-47, ADR-48, ADR-49), 04, 05, 02 e HANDOFF.*