# C4 — VERDETTO FINALE DEL CHAIRMAN (Scadenze Locazioni 3+2 canone concordato)

## Dove il consiglio concorda
1. Canale: email confermata. Abbandonare il bot WhatsApp/SMS è la scelta giusta — ban del numero aziendale con API non ufficiali, burocrazia e costi fissi con quella ufficiale. L'email è l'unica shippabile in 2-3 settimane. Bozza AI modificabile + invio su conferma umana restano il cuore della feature.
2. Ciclo chiuso obbligatorio. Tutti, tranne l'Expansionist, bocciano il fire-and-forget: senza follow-up, escalation e presidi operativi la feature è un monologo senza feedback che crea falsa sicurezza — peggio di niente.
3. Inquilino escluso dalle notifiche, ma presente nel modello dati: le disdette dell'inquilino vanno registrate, altrimenti si notificano proprietari su contratti già morti.
4. L'email raccoglie intenzioni, non produce effetti legali: la disdetta formale resta raccomandata AR/PEC — va scritto nel messaggio e nel gestionale.

## Dove il consiglio è diviso
- Il trigger (a). Il Contrarian denuncia un vizio legale: il preavviso di 6 mesi (art. 3 l. 431/98) opera alla scadenza del triennio, non del biennio, dove il contratto cessa automaticamente. Gli altri quattro accettano acriticamente la premessa. Le review giuridiche danno ragione al Contrarian.
- Lo Scenario B. Per il Contrarian è una finzione (dopo il biennio serve nuova stipula); Executor ed Expansionist lo danno per valido.
- L'ambizione. Expansionist: la feature è lead generation (pipeline 4 touchpoint, tracking, scoring). Executor: niente parsing AI ora, v1 manuale. Outsider e Contrarian: niente tracking/scoring senza consenso GDPR.

## Punti ciechi emersi
1. GDPR ignorato da tutti: parsing AI delle risposte, tracking aperture/click e scoring richiedono basi giuridiche, informative, consenso e DPA con il fornitore AI.
2. Deliverability: senza SPF/DKIM/DMARC e gestione bounce l'email fallisce in silenzio; email obsolete = trigger muto.
3. Dead man's switch: nessuno monitora il cron stesso; un job che non gira brucia finestre legali senza allarme.
4. Qualità del dato data: la fine biennio va calcolata dalla proroga effettiva, non dall'inizio contratto.
5. Aspettative del cliente: chiedeva un bot, riceve una mail — la rinuncia va motivata e venduta.

## La raccomandazione
Il design è bocciato nel punto (a) e nello Scenario B, validato nel resto. Mi schiero con il Contrarian — minoranza di uno — perché è l'unico che verifica la premessa legale e le due review giuridiche la confermano.

Correzione del modello scadenze — doppio trigger:
- Trigger 1 — fine triennio − 7 mesi: la scadenza legale vera. Decisione del proprietario: disdetta (raccomandata/PEC entro 6 mesi) oppure rinnovo tacito del +2 (scelta registrata consapevolmente).
- Trigger 2 — fine biennio − 6 mesi: nessuna disdetta necessaria, il contratto cessa. Trigger commerciale di nuova stipula: rinegoziazione, aggiornamento canone/ISTAT, registrazione RLI. Va ribattezzato "nuova stipula", non "preavviso".
- Date calcolate dalla proroga effettiva, con campi per disdetta anticipata di inquilino e proprietario. Verifica con consulente legale in parallelo alla build.

Routing a tre scenari:
- A — Chiusura/Cessazione: stop notifiche; se il "no" è del proprietario → lead vendita.
- B — Rinnovo: al triennio = tacito (registra e basta); al biennio = nuova stipula avviata.
- C — In trattativa: il "sì, ma" — canone o condizioni da rinegoziare; stato con task operatore e data di rientro.

Ciclo chiuso (non negoziabile in v1): reminder +7/+14/+30 ai non rispondenti; task operatore automatico a scadenza −6 mesi; idempotenza del cron con retry; dashboard "scadenze senza risposta"; dead man's switch sul job; SPF/DKIM/DMARC e gestione bounce.

Cosa salvare dell'Expansionist: il "no" come lead di vendita e il tracking delle aperture sono valore reale — ma in v2, subordinati a informativa e consenso GDPR, DPA con il provider AI, nessuno scoring senza base giuridica.

## La prima cosa da fare
Verifica legale delle due scadenze (consulente esterno) e, in parallelo, ridisegno del modello dati con due trigger e tre scenari. Il cron resta invariato — cambia solo ciò che conta come scadenza.
