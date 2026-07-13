# Verbale C8 — JARVIS assistente personale del Proprietario

**Data:** luglio 2026 (sessione post-Fondamenta).
**Convocazione:** richiesta esplicita del proprietario ("passa tutte queste richieste e idee dalla skill llm-council per verificare se siano buone idee, se si possono migliorare o se devono essere scartate"), checkpoint conforme al file `02` sezione D (decisioni ad alta posta che toccano ADR-03/04/07).
**Protocollo:** skill `llm-council`: 5 advisor paralleli con lenti diverse (architetto pragmatico, avvocato del diavolo, compliance/legale, operatività utente, dati/sicurezza) → peer review anonima (etichette R1–R4) → verdetto del Chairman. 11 lavori separati.
**Evidenze:** brief di ricerca fattuale `R3_memoria_brief.md` (memoria personale locale) e `R4_automazioni_brief.md` (motori di automazione, pattern sicuri, prompt injection), entrambi con fonti verificate.
**Agenda:** Q1 accesso esclusivo Proprietario; Q2 "assistente completo che lavora al posto mio"; Q3 memoria/"secondo cervello"; Q4 auto-creazione "Procedure"; Q5 auto-creazione automazioni (n8n?); Q6 catalogo automazioni pre-costruite.
**Esito recepito in:** ADR-50…ADR-54 nel file `03` + nuove sezioni §4.6/§4.7 nel file `04` + sprint S9/S10 e Parcheggio nel file `05` (commit della stessa sessione).

---

# VERDETTO FINALE — Consiglio C8: JARVIS assistente personale del proprietario

## 1. Decisione raccomandata

**Accogliere il pacchetto in forma ridimensionata**: JARVIS riservato al Proprietario, memoria "noiosa" su SQLite con conferma umana, Procedure su richiesta esplicita, motore automazioni interno a catalogo chiuso — tutto in **due sprint dedicati dopo il go-live (S9, S10)**, con S6 invariato; **scartati n8n, Graphify/Graphiti e la doppia firma segretaria+proprietario**.

## 2. Motivazione (per il proprietario)

Le sue idee sono buone quasi tutte: JARVIS solo suo, il "secondo cervello", le procedure che nascono dall'uso, le automazioni. Quello che cambiamo è il *come*: niente programmi esterni da installare e mantenere (n8n, Graphify) quando il gestionale sa già fare le stesse cose in modo più semplice e sicuro; niente "fa tutto da solo con una conferma" — JARVIS prepara, lei (o la segretaria, a seconda del tipo di azione) legge una sintesi chiara e conferma con un tap. E niente di tutto questo prima che il gestionale sia in produzione: prima si consegna ciò che le fa risparmiare tempo da subito, poi l'assistente personale. Una cosa va detta con franchezza: un assistente "completo che fa tutto" non esisterà in questa forma; esisterà un assistente che fa bene un elenco crescente di cose, sotto il suo controllo.

## 3. Verdetto per domanda

**Q1 — JARVIS solo Proprietario: BUONA IDEA** (unanimità).
Implementazione come **permesso di ruolo** (non hardcoded sull'utente, anti lock-out); i tool read-only restano comunque filtrati dal ruolo (04 §4.2). **Correzione essenziale (tensione Q1/Q2)**: riservata è la **chat**; la **coda "Da approvare" è una schermata separata, visibile per ruolo**. AuditLog esteso alle consultazioni (domande, tool invocati, versione modello — estensione naturale ADR-08); log chat con cifratura/retention di 04 §8.2. Costo sommerso reale da gestire: il prototipo Design di S6 prevede validazione con segretaria/agenti (05, riga 16) — il piano di validazione va riscritto sul proprietario. → **ADR-50**; ritocco 04 §4; nota in S6 (solo permesso + piano validazione).

**Q2 — "Lavora al posto mio": DA MIGLIORARE; il flusso a doppia firma VA RIDISEGNATO** (unanimità).
Due controllori in serie = rubber-stamping istituzionalizzato (ognuno presume che l'altro abbia letto), e la segretaria vedrebbe dati che ADR-42 le nega. Regola sostitutiva: **un solo approvatore competente per tipo di azione** — operatività documentale → segretaria; email a clienti, dati economici, margini → proprietario — sempre con diff leggibile. Veicolo: la proposta diventa un **Task** (entità esistente, 04 §3.12) assegnato all'approvatore. Perimetro: v1 = S6 com'è (lettura + proposte su elenco chiuso); estensione scrittura = Fase 2, **un tool alla volta, ciascuno con mini-ADR**. → dentro **ADR-50**; il Parcheggio resta la casa dell'estensione scrittura.

**Q3 — Memoria "secondo cervello": BUONA IDEA nella versione noiosa.**
**Opzione 1 di R3**: tabella `ricordi` in SQLite + FTS5 + sqlite-vec (versione bloccata) + bge-m3 via Ollama — dentro DB, backup e cifratura esistenti. Filtro anti-inutilità = **conferma umana** ("Vuoi che ricordi: *X*?", salva solo su tap); correzioni via `valid_from`/`superseded_by`. **GDPR**: ogni ricordo che nomina un terzo va agganciato al Soggetto in anagrafe (esercitabilità artt. 15-17); **oblio = cancellazione fisica del testo** (l'invalidazione non basta; in audit resta solo il fatto); rifiuto categorie art. 9; addendum DPIA. **Regola anti-avvelenamento (vincolante)**: i ricordi nascono **solo da dettatura diretta confermata del proprietario, mai estratti da email o documenti**. → **ADR-51**; 04 nuova §4.6; sprint S9.

**Q4 — "Procedure" auto-create: BUONA IDEA, GIÀ QUASI DECISA (ADR-04), con un ridimensionamento.**
La libreria skill Markdown è **già in S6** (05, riga 220): le Procedure su richiesta esplicita costano quasi zero. **v1: solo richiesta esplicita**; il contatore "me l'hai chiesto tre volte" **slitta** (richiede telemetria = un secondo sistema di memoria, e un 27B Q4 rischia proposte mediocri approvate per stanchezza). Approva **solo il Proprietario**; Git invisibile ("versione 3, approvata il…"). Due vincoli scritti nell'ADR: (a) una procedura **non può allentare HITL** e a rifiutarla è **il validatore**, non l'LLM; (b) **mai procedure il cui testo derivi da contenuti esterni** (stessa regola anti-avvelenamento di Q3). → **ADR-52**; la parte esplicita resta in S6.

**Q5 — Automazioni: motore INTERNO; n8n SCARTATO** (unanimità, evidenze R4).
Tabella `automazione` + **riuso** dello scheduler launchd e del job ADR-29 (dead man's switch incluso) — mai un secondo scheduler. Modello dichiarativo a **catalogo chiuso**: l'LLM compila parametri da enum fissi, validati Pydantic server-side; mai JSON libero né codice (ADR-04). Presentazione **QUANDO/SE/ALLORA** = il diff di ADR-07. Ciclo di vita non negoziabile: **dry-run su storico → nasce disattivata → conferma esplicita → ogni esecuzione in AuditLog → pausa/elimina a un tap → anti-tempesta** (max N notifiche/giorno, oltre si autosospende con avviso). Azioni v1: solo *crea Task* e *notifica a destinatari fissi hardcoded*. **Trigger email = lotto separato (S10)**: IMAP polling **solo su allowlist di mittenti** (minimizzazione), credenziali **solo in Keychain** (casella dedicata o app password revocabile), sintesi **senza alcun tool esposto all'LLM**, HTML→testo, link non cliccabili, banner "contenuto non verificato", retention riassunti ≤30 giorni; ogni azione nata da email ripassa da HITL. → **ADR-53** (motore) + **ADR-54** (trigger email); 04 nuova §4.7.

**Q6 — Catalogo pre-costruito: ADOTTARE CON POTATURA.**
Doppioni: **#7 esiste già** (scadenziario RLI, ADR-43/S5); **#2 si sovrappone ad ADR-24** (doppio trigger legale) — si riformula come estensione delle Scadenze esistenti, mai due promemoria sulle stesse date; entrambe esposte come "automazioni di sistema" nella stessa UI. **Lotto 1 (S9, solo DB)**: #10 digest mattutino, #3 ISTAT, #4 morosi, #5 report incassi, #8 certificazioni (#9 rassegna in coda, se resta tempo). **Lotto 2 (S10, email)**: #1 watchlist. **#6 tagliata** (scansione thread: costo alto, valore medio). Default: un solo digest giornaliero aggregato; notifica immediata solo per regole marcate "urgente".

## 4. Impatto sulla roadmap

- **S6 NON si tocca** (già gated da Mac Mini + eval locale, ADR-48). Vi entrano solo: permesso di ruolo per la chat (una riga) e revisione del piano di validazione del prototipo Design.
- **S9 "JARVIS personale"** (primo sprint di Fase 2, dopo il go-live S8): memoria "Cose da ricordare" + motore automazioni + lotto 1 pre-costruite + coda approvazioni. **Prerequisito: addendum DPIA** (verifica esterna calendarizzata).
- **S10 "Trigger email"**: modulo IMAP + watchlist + eventuali primi tool di scrittura aggiuntivi (dal Parcheggio, uno alla volta).
- Impatto realistico: **+6-10 settimane dopo S8, zero impatto sul percorso critico S6→S8 e sul go-live**.
- Patch: 03 (**ADR-50..54**), 04 (**§4.6, §4.7**), 05 (S9/S10 in coda, Parcheggio aggiornato).

## 5. Divergenze esplicite e risoluzione

1. **Collocazione S6b vs S9/S10**: l'advisor operatività proponeva "S6b" tra S6 e S7; gli altri quattro (e lui stesso in peer review, dove ha ritirato la proposta) la respingono perché viola la regola scritta del Parcheggio ("da non iniziare prima del go-live") e ADR-03. **Risolta: S9/S10 post go-live.**
2. **Contatore automatico "tre richieste simili"**: tre advisor lo volevano in v1, l'avvocato-diavolo mai; dopo peer review la maggioranza converge sul rinvio. **Risolta: v1 solo richiesta esplicita; il contatore si rivaluta in Fase 2 dopo la memoria, non è promesso.**
3. **ADR dedicato per le Procedure**: un advisor lo riteneva superfluo ("è già ADR-04"). **Risolta: ADR-52 serve** — fissa naming UI vincolante, approvatore unico, regola anti-allentamento HITL e anti-avvelenamento.
4. **Approvazione procedure con coinvolgimento Admin** (un advisor, se toccano flussi altrui): **respinta** — il validatore rifiuta a monte procedure che escono dal perimetro del proprietario; un solo approvatore.
5. **Riferimento della #2** (S4 vs ADR-24): **corretto in ADR-24**, come verificato da più peer review.
6. **Nome UI della memoria** (Appunti / Ricordi / Cose da ricordare): **deciso "Cose da ricordare"** — il più autoesplicativo per un utente non tecnico.

## 6. Rischi accettati e mitigazioni

| Rischio accettato | Mitigazione |
|---|---|
| Gap di aspettative ("Jarvis di Iron Man" vs 27B Q4) — rischio di abbandono dell'intero gestionale | Demo perimetrata a fine S6 + pagina "cosa NON fa JARVIS" approvata per iscritto dal proprietario |
| Trigger email = lethal trifecta residua | Difese **architetturali** (sintesi senza tool, destinatari hardcoded, allowlist mittenti), lotto separato S10, dopo un ciclo di motore senza incidenti |
| Casella email = nuovo trattamento dati + segreto di maggior valore sul Mac | Addendum DPIA e informativa **prima** di S10; Keychain; casella dedicata/app password revocabile con procedura di revoca nel manuale di ripristino; retention riassunti ≤30 giorni |
| Ricordi su terzi = shadow-database | Aggancio al Soggetto, delete fisico, lista sempre visibile, DPIA |
| Fatica da notifiche / affidamento sul silenzio | Digest unico di default; pannello "ultima esecuzione" per ogni automazione; disclaimer ADR-45 ereditato |

## 7. Naming UI (vincolante, in italiano)

- Chat: **"JARVIS"** (invariato)
- Memoria: **"Cose da ricordare"** — pulsanti **"Ricorda questo"**, **"Dimentica"**, **"Correggi"**
- Skill: **"Procedure"** (la parola "skill" non compare MAI); versioni come "versione 3, approvata il…"
- Automazioni: **"Automazioni"**, frase **"QUANDO… SE… ALLORA…"**, interruttori Attiva/Pausa, **"Prova a vuoto"** (dry-run)
- Coda: **"Da approvare"**
- Mai in UI: skill, RAG, embedding, vettori, prompt, Git, memoria AI

## 8. Cose scartate

- **n8n**: seconda webapp sempre accesa con DB/credenziali/aggiornamenti propri per un carico che launchd copre già; AI Builder cloud-only.
- **"Graphify"**: non esiste come descritto (R3); era un knowledge graph per codebase, altro prodotto.
- **Graphiti/Neo4j (e mem0)**: DB grafo da mantenere per anni + warning ufficiale sui modelli piccoli, per vantaggio marginale (J-score 68,4 vs 66,9).
- **Doppia firma segretaria→proprietario**: due controllori sono meno di uno (rubber-stamping istituzionalizzato, vietato da ADR-07).
- **"Assistente completo che fa tutto"**: non è un perimetro; il bisogno lo coprono elenco chiuso di tool + automazioni.
- **Contatore automatico ripetizioni (v1)**: richiede telemetria (un altro sistema di memoria) e produce proposte mediocri approvate per stanchezza.
- **Automazione #6 (thread senza risposta)**: costo di scansione alto per valore medio.
- **Automazione #7 e #2 come nuove automazioni**: doppioni di ADR-43 e ADR-24; si riespongono come "automazioni di sistema".
- **Codice/JSON libero generato dall'LLM**: vietato da ADR-04; solo parametri su enum chiusi validati server-side.
- **Sprint "S6b" pre go-live**: viola il Parcheggio ("da non iniziare prima del go-live") e ADR-03.