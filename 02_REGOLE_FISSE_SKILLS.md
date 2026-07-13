# 02 — Regole fisse e "skill": cosa sono, come si installano, come si usano

*Questo file contiene il cuore del sistema: le regole che Claude deve rispettare in ogni sessione di lavoro. Qui trovi il blocco pronto da copiare e le istruzioni per installarlo. Non devi capire il gergo tecnico: devi solo seguire i passaggi.*

---

## A. Dove vanno le regole: la "doppia fonte"

Lavoriamo in **Code** (sezione di Claude Desktop), che legge e scrive direttamente i file del repository. Le regole vivono in **due file nella cartella principale (root) del repository**:

1. **`REGOLE.md`** → il testo completo delle regole (il BLOCCO REGOLE della sezione B). È la fonte normativa: umana, leggibile, versionata.
2. **`CLAUDE.md`** → un file corto che Code **legge in automatico a ogni avvio di sessione** e che gli ordina di leggere e rispettare `REGOLE.md`. È il "pilota automatico": anche se tu dimenticassi la frase rituale, le regole entrano comunque in carico.

Perché due file? Perché è la rete di sicurezza: `CLAUDE.md` garantisce il caricamento automatico, la frase rituale (sezione C) garantisce la **verifica leggibile** che le regole sono state davvero lette. E perché un file nel repository lo può rileggere chiunque, in qualsiasi momento, anche senza saper leggere codice.

### Come si installano (una volta sola, all'inizio)

**File 1 — `REGOLE.md`:**

1. Crea un file chiamato `REGOLE.md` dentro la cartella del repository sul computer (quella collegata a GitHub, vedi file `00`).
   - Il modo più semplice: apri **TextEdit** (Mac), incolla il BLOCCO REGOLE della sezione B (tutto, esattamente com'è), e salva il file con il nome `REGOLE.md` dentro la cartella `gestionale-immobiliare`.
2. Apri GitHub Desktop, scrivi come messaggio di commit `sprint-0: regole fisse del progetto`, fai **Commit** e poi **Push**.

**File 2 — `CLAUDE.md`:**

1. Crea un secondo file chiamato `CLAUDE.md` nella stessa cartella, con **esattamente** questo contenuto:

═══════════════ CONTENUTO DI CLAUDE.md — COPIA DA QUI ═══════════════

```markdown
# Istruzioni per Claude Code

Lavori sul progetto "Gestionale Immobiliare + JARVIS". Prima di qualsiasi altra cosa,
leggi il file REGOLE.md nella root di questo repository e rispettalo in ogni momento
della sessione. Rispondi sempre in italiano. I riferimenti vincolanti del progetto sono
03_DECISIONI_CONSIGLIO.md (registro ADR) e 04_ARCHITETTURA.md. Lo stato corrente è in
HANDOFF.md. Non eseguire azioni distruttive senza conferma esplicita dell'utente.
```

════════════════ COPIA FINO A QUI ════════════════

2. Commit + push con messaggio `sprint-0: istruzioni automatiche per Code`.

Controlla che su github.com compaiano entrambi i file. Da questo momento, ogni sessione di Code aperta su questa cartella parte con le regole già in carico.

> **Regola di manutenzione:** se in futuro le regole vengono modificate (vedi sezione E), aggiorna `REGOLE.md` con la procedura di revisione. `CLAUDE.md` non va toccato: punta a `REGOLE.md` e basta.

> **Nota sul rapporto con la sessione 1:** il Prompt Maestro (file `01`) prevede che Claude ti proponga una bozza di `REGOLE.md` durante la prima sessione. Le due procedure si integrano così: se hai già creato i due file copiando i blocchi qui sopra, in sessione 1 chiedi a Claude di verificarli e proporti miglioramenti; se preferisci partire dalla bozza di Claude, confrontala con il blocco della sezione B (che è la versione approvata in fase di progettazione) e scegli un unico testo finale. Ciò che non è negoziabile: **un solo testo delle regole, in `REGOLE.md`, con `CLAUDE.md` che ci punta**.

---

## B. IL BLOCCO REGOLE (da copiare pari pari)

Copia tutto ciò che sta tra le due linee. Sono 4 sezioni, meno di 60 righe, volutamente corte: regole lunghe non vengono seguite.

═══════════════ INIZIO BLOCCO REGOLE — COPIA DA QUI ═══════════════

```markdown
# REGOLE.md — Regole fisse del progetto "Gestionale Immobiliare + JARVIS"

Queste regole valgono in OGNI sessione. Rispondi sempre in italiano.
Se una richiesta dell'utente contraddice queste regole, segnalalo prima di procedere.

## 1. Disciplina (come si lavora)

1. Prima di scrivere codice: PIANO scritto in italiano semplice (cosa facciamo, quali file tocchiamo).
2. Insieme al piano: il CRITERIO DI ACCETTAZIONE (1-3 punti verificabili: "la task è finita quando...").
3. Si scrive codice SOLO dopo l'ok dell'utente sul piano.
4. Un cambiamento piccolo alla volta. Niente modifiche extra "già che ci siamo".
5. Dopo il codice: REVIEW breve (cosa ho fatto, file toccati, come verificare che funziona).
6. Se qualcosa non funziona dopo 2 tentativi: fermarsi, spiegare il problema, chiedere.

## 2. Semplicità (anti-overengineering)

1. Vince sempre la soluzione più noiosa che funziona.
2. Niente astrazioni premature: codice ripetuto due volte è meglio di un'astrazione sbagliata.
3. Niente funzioni "per dopo", "nel caso serva", "perché è elegante".
4. Niente nuove librerie o dipendenze senza chiedere prima il permesso all'utente.
5. Niente opzioni di configurazione per casi che non esistono ancora.
6. Prima di aggiungere qualcosa, chiediti: "posso farlo con quello che c'è già?"
7. Se si può togliere codice invece di aggiungerne, si toglie.

## 3. Consiglio ridotto (prima di ogni decisione importante)

Prima di proporre una scelta strutturale (nuova tabella, nuova libreria, nuovo servizio, cambio di approccio):

1. Scrivi la decisione in una riga.
2. Elenca 3 modi concreti in cui potrebbe fallire.
3. Proponi 1 alternativa più semplice.
4. Raccomanda quale scegliere e perché (2 righe).
5. Aspetta l'ok dell'utente prima di procedere.

Niente "consigli" recitati da una sola voce. Il consiglio completo (skill
llm-council) si convoca solo dove esistono sub-agenti reali, ai checkpoint
fissi e per le decisioni bloccanti, come definito nel file 02.

## 4. Design (interfaccia "a prova di stupido")

Checklist obbligatoria per OGNI schermata:

1. Gerarchia chiara: un solo titolo principale; in 3 secondi si capisce dove si è.
2. UNA sola azione primaria per schermata (un solo pulsante evidente).
3. Errori in italiano semplice: cosa è successo + cosa fare adesso.
4. Schermate vuote che guidano (es. "Nessun cliente ancora: premi 'Nuovo cliente'").
5. Testo leggibile: contrasto forte, dimensioni adeguate, niente grigio chiaro su bianco.
6. Niente sigle o gergo tecnico nelle etichette ("Pratica", non "record").
7. Prima di dichiarare finita una schermata: rileggi questa checklist voce per voce.
```

════════════════ FINE BLOCCO REGOLE — COPIA FINO A QUI ════════════════

### Da dove vengono queste 4 sezioni (in breve)

- **Sezione 1 — Disciplina**: è la versione essenziale della metodologia *superpowers* (lavoro disciplinato: prima il piano, poi il codice, poi la review), ridotta a 6 righe perché su Claude Desktop quella metodologia non è installabile come tale.
- **Sezione 2 — Semplicità**: sono le regole anti-complicazione del ruleset *ponytail*, che esiste proprio per impedire il difetto che ha già affondato il progetto una volta: costruire troppo, troppo presto.
- **Sezione 3 — Consiglio ridotto**: sostituisce il "consiglio di esperti" completo, che su Claude Desktop non esiste come strumento installabile. Tiene solo la parte utile: prima di una decisione importante, pensare a come potrebbe fallire.
- **Sezione 4 — Design**: è la checklist operativa della skill *impeccable*, l'unica mantenuta per intero, perché la facilità d'uso delle schermate è l'unica cosa che tu non puoi correggere da solo a occhio.

---

## C. La frase rituale di apertura sessione (da incollare a ogni sessione nuova in Code)

**Frase principale** (sessioni normali, quando `REGOLE.md` è già nel repository):

═══════════════ FRASE RITUALE — COPIA DA QUI ═══════════════

> Leggi REGOLE.md e riassumilo in 5 righe prima di toccare codice.

════════════════ FRASE RITUALE — COPIA FINO A QUI ════════════════

**Variante 1 — prima sessione in assoluto** (il repository non contiene ancora `REGOLE.md`; lo creeremo in questa sessione):

> Leggi il file 02_REGOLE_FISSE_SKILLS.md in questo repository, sezione B (BLOCCO REGOLE), e riassumilo in 5 righe prima di fare qualsiasi cosa. Quando hai finito il riassunto, dimmi che sei pronto e ti darò le istruzioni di avvio.

**Variante 2 — ripresa dopo la sessione precedente** (da usare insieme alla frase principale, come secondo messaggio):

> Leggi anche il file HANDOFF.md nel repository e dimmi in 2 righe: (1) dove eravamo rimasti, (2) qual è il prossimo passo. Poi fammi il piano scritto come richiede la sezione 1 delle regole.

**Come verificare che ha funzionato:** Claude deve rispondere con un riassunto in 5 righe che assomiglia alle 4 sezioni delle regole. Se il riassunto è vago, inventato o troppo lungo, scrivi: *"Il riassunto non torna. Rileggi REGOLE.md e rifallo."* Solo dopo un riassunto corretto si prosegue.

> Perché la frase rituale resta obbligatoria anche con `CLAUDE.md`: il caricamento automatico mette le regole "sotto gli occhi" di Claude, ma il riassunto in 5 righe è la **tua** prova che le ha davvero lette — una verifica che puoi fare senza saper leggere codice.

---

## D. Le "skill" citate: cosa è vero e come le usiamo

In fase di progettazione sono stati verificati uno per uno gli strumenti ("skill") citati come riferimento. Risultato: le **skill esistono e girano nell'app Claude**, ma nessuna si applica da sola come "regola di progetto" — l'unica forma che vincola davvero è il file di regole nel repository (`REGOLE.md`), caricato in automatico da Code tramite `CLAUDE.md`. Ecco la tabella riassuntiva:

| Nome citato | Cos'è davvero (verificato) | Come lo usiamo in questo progetto |
|---|---|---|
| `karpathy/llm-council` (22,6k★) | Il repo originale NON è una skill: è una web app locale autonoma che richiede OpenRouter (servizio a pagamento). **Però è stato convertito in una skill funzionante** (5 advisor → peer review anonima → chairman) che gira dove esistono sub-agenti paralleli — ed è quella che ha prodotto i 6 consigli di questo progetto (vedi `08_VERBALI_CONSIGLI/`). | **Doppio livello.** Decisioni di routine: il **template ridotto di 10 righe della sezione 3** (perché un consiglio completo sono ~11 agenti: troppo costoso per ogni scelta quotidiana). Decisioni pesanti: il **consiglio completo via skill**, dentro la sessione se l'ambiente ha sub-agenti reali, altrimenti fuori — ai checkpoint elencati qui sotto. |
| `obra/superpowers` (253k★, attivissimo) | Esiste, ed è una metodologia che gira nativamente su **Claude Code** — cioè proprio l'ambiente che usiamo (sezione Code di Claude Desktop). | **Distillata nella sezione 1 (Disciplina)**: piano scritto → criterio di accettazione → codice → review. |
| `DietrichGebert/ponytail` (81k★) | Esiste, ma **NON è uno strumento backend**: è un insieme di regole anti-complicazione ("anti-overengineering") valide per qualsiasi progetto. | **È la sezione 2 (Semplicità)**: niente astrazioni premature, niente feature "per dopo", vince la soluzione noiosa che funziona. |
| `pbakaus/impeccable` (46k★, attivo) | Esiste ed è una vera skill di design per interfacce. Scelta confermata come valida. | **È la sezione 4 (Design)**, l'unica mantenuta praticamente per intero, come checklist operativa per le schermate. |

**Scartate, e perché:**

| Alternativa | Perché è stata scartata |
|---|---|
| `tenfoldmarc/llm-council-skill` (524★) | Versione "in formato skill" del consiglio: maturità bassa, formato incerto. Troppo rischiosa per un progetto che deve durare. |
| `github/spec-kit` (la sua "constitution") | Buona idea (regole versionate nel repo — l'abbiamo adottata come principio), ma il meccanismo completo è burocrazia per un progetto portato avanti da una persona sola. |
| `BMAD-METHOD` | Metodo pensato per team strutturati con più persone e ruoli. Qui il team sei tu + Claude. |
| `vercel web-design-guidelines` | Buona, ma avere **due fonti di regole di design** (questa + impeccable) crea paralisi e contraddizioni. Si è scelto di tenerne una sola. |
| `ui-ux-pro-max` | Alternativa di design valutata in fase di ricerca, non scelta: impeccable copre già il bisogno (schermate semplici per strumento interno). |

**Nota onesta:** in fase di progettazione si era deciso di lavorare nella sezione Progetti di Claude Desktop, rinviando la valutazione di Claude Code. La decisione è stata poi cambiata (vedi `03_DECISIONI_CONSIGLIO.md`, ADR-13): **si lavora direttamente in Code fin dalla sessione 1** — è l'ambiente tecnicamente corretto per queste metodologie (sub-agenti veri, lavoro diretto sui file, GitHub integrato), e con le regole nel repository l'attrito in più è minimo. La sezione Progetti non si usa.

### Il consiglio completo (skill llm-council): quando convocarlo

Il consiglio completo a 5 advisor — la skill convertita da `karpathy/llm-council` — **resta uno strumento attivo del progetto**. In Code esistono i sub-agenti veri (advisor in parallelo, contesti isolati, peer review anonima): il consiglio si convoca **dentro la sessione di sviluppo**, ai checkpoint elencati qui sotto. Se mai lavorassi in un ambiente senza sub-agenti reali, il consiglio completo va tenuto fuori dalle sessioni: mai un "consiglio" recitato da una sola voce — il suo valore viene dall'indipendenza degli advisor.

**Consiglio di prova (da fare una volta, nella sessione 1):** chiedi a Claude di passare al consiglio una decisione reale ma piccola (es. la scelta del provider cloud per lo sviluppo). Verifica che: (1) le risposte dei 5 advisor arrivino come lavori separati e non come un unico testo con 5 voci; (2) la peer review citi le risposte per lettera in forma anonima; (3) il chairman produca un verdetto con divergenze esplicite. Se tutto torna, il consiglio è certificato per le sessioni di sviluppo; annota l'esito in `HANDOFF.md`.

Convocalo a questi **checkpoint fissi**:

1. **Prima di ogni sprint "pesante"** (S2 documentale, S4 scadenze, S6 JARVIS, S7 OCR): valida piano, rischi e scelte aperte dello sprint prima di scrivere codice. Un consiglio da 10 minuti qui può evitare settimane di lavoro sbagliato — è quello che ha scoperto il vizio legale del 3+2 e la bocciatura di GLM-OCR.
2. **Quando una decisione modifica un ADR** (il registro in `03_DECISIONI_CONSIGLIO.md`): nessun ADR si riscrive senza un consiglio.
3. **Quando il consiglio ridotto scopre un rischio serio**: se i "3 modi in cui può fallire" ne trovano uno bloccante, esci dalla sessione e convoca il consiglio completo.
4. **Prima del go-live (fine S8)**: consiglio finale di revisione su sicurezza, dati reali e compliance.
5. **Quando sei indeciso tra opzioni con posta alta** (es. cambio di modello locale, cambio di provider, nuova funzionalità grossa richiesta dal cliente).

Come si fa, in pratica: apri una conversazione nell'ambiente dove la skill è installata, esponi la decisione con il suo contesto (cosa stai costruendo, cosa hai già deciso, cosa è in gioco) e chiedi di passarla al consiglio. Il verdetto finisce nel repo: come nuovo ADR se cambia una decisione, o come nota nell'handoff se la conferma.

---

## E. Igiene delle sessioni e controllo di conformità

### Una task per sessione. Sessione nuova per task nuova.

- Ogni sessione con Claude tratta **una sola task** (uno sprint, un problema, una modifica).
- Finita la task: rituale di chiusura (file `07`) e sessione chiusa. La task successiva si apre in una **sessione nuova** con la frase rituale.
- Se a metà sessione spunta una seconda cosa da fare: chiedi a Claude di annotarla nell'handoff come "problema aperto / prossimo passo", non farla subito. Le sessioni lunghe e miste sono la causa principale delle "derive".

### Controllo di conformità ogni 2 settimane

Ogni due settimane, apri una sessione dedicata **solo al controllo** (nessuno sviluppo in quella sessione) e incolla questo messaggio:

═══════════════ CONTROLLO BISETTIMANALE — COPIA DA QUI ═══════════════

> Sessione di controllo di conformità. Leggi REGOLE.md e gli ultimi HANDOFF.md nel repository. Poi rispondi in italiano semplice a 4 domande:
> 1. Nelle ultime sessioni le regole sono state rispettate? Se no, quali e quando?
> 2. Qualche regola è risultata inutile, confusa o impossibile da seguire?
> 3. Manca qualche regola per problemi che si sono ripetuti?
> 4. Cosa aggiorneresti in REGOLE.md? Proponimi il testo modificato e aspetta la mia approvazione.

════════════════ CONTROLLO BISETTIMANALE — COPIA FINO A QUI ════════════════

Se emergono modifiche: **tu approvi**, poi aggiorni `REGOLE.md` nel repository (con commit `regole: revisione bisettimanale`). Le regole sono vive, ma cambiano solo con questa procedura — mai "al volo" dentro una sessione di sviluppo.
