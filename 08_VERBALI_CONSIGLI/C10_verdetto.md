# Verdetto del Chairman — Consiglio C10 (Auto-tagging dei moduli + Dizionario dei tag)

> **Data:** 2026-07-14 · **Metodo:** skill `llm-council` (protocollo Karpathy adattato).
> **Partecipanti:** 5 advisor paralleli con lenti diverse (Architetto deterministic-first, Avvocato del diavolo, Compliance documentale/legale, Operatività segretaria, Dati e ontologia) → peer review anonima incrociata (R1–R4) → Chairman. Advisor e Chairman su **Fable 5**; fase di ricerca fatti su modello forte con ricerca web.
> **Posta in gioco:** valutare l'idea dell'utente di templatizzazione semi-automatica dei moduli importati (LLM/script che inserisce tag stile `{{nome_locatore}}`) e di un "dizionario" di tag anti-drift, poi l'auto-compilazione dai dati.
> **Fonti fatti:** brief di ricerca `R6_autocompilazione_brief.md` (stesso consiglio).
> **Certificazione:** superata (opinioni parallele separate; peer review con citazioni per etichetta anonima R1–R4; Chairman con divergenze esplicite).
> **Nota di esecuzione:** l'ultimo agente (bozza operativa del Progettista) non è stato generato per un limite di sessione temporaneo; il verdetto del Chairman è completo e autosufficiente (contiene ADR proposti, collocazione e gate).
>
> **STATO: RACCOMANDAZIONE. Gli ADR-64…70 NON sono ancora scritti nel registro `03`: attendono l'approvazione dell'utente.**

---

# VERDETTO DEL CHAIRMAN — Consiglio C10
## Auto-tagging dei moduli importati + Dizionario dei tag

Premessa di sintesi: i 5 advisor, da lenti diverse, sono convergenti sull'impianto e unanimi su un punto: l'idea è buona nel fine ma va corretta nell'esecuzione — **l'LLM non deve mai scrivere nel file**. La convergenza indipendente è essa stessa evidenza. Le divergenze reali (poche ma vere) sono riportate sotto, punto per punto.

---

## D1 — Idea complessiva

**1. Decisione raccomandata:** BUONA-CON-CORREZIONI (verdetto unanime 5/5).

**2. Motivazione:** Le due novità vere (templatizzazione semi-automatica del modulo importato; dizionario canonico anti-drift) sono sane e completano gli ADR a monte. Ma la formulazione originale "l'LLM analizza e riempie i campi con i tag" viola ADR-02 nella sostanza: un LLM che ri-trascrive il documento può alterare silenziosamente il testo legale e tecnicamente corrompe i run del DOCX. Correzioni vincolanti: (a) l'LLM non tocca mai il file — al più classifica; l'inserimento dei {{tag}} lo fa codice deterministico; (b) l'LLM non salva mai da solo un tag nuovo nel dizionario — propone, un umano approva; (c) il template taggato nasce BOZZA (ADR-17), passa dry-run ADR-16 esteso e ciclo ADR-18; (d) ogni tag è agganciato a un campo del modello dati canonico, altrimenti ADR-21 non può funzionare. Con queste correzioni nessun ADR è violato.

**3. Divergenze esplicite:** Nessuna sul verdetto. Sfumatura di enfasi: l'avvocato del diavolo e l'architetto ridimensionano il valore dell'LLM ("il wizard deterministico è il 90% del valore, l'LLM il 10% di comodità"), mentre l'idea originale lo metteva al centro. Il Chairman adotta il ridimensionamento: il deliverable è il wizard, l'LLM è un acceleratore opzionale.

**4. Rischi accettati e mitigazioni:** Rischio di over-engineering (volumi piccoli: decine di moduli, una tantum) → mitigazione: dimensionare su S2, condizionare S6 alle metriche (vedi D5/D6). Rischio drift residuo → governance del dizionario (D3).

**5. Alternativa più semplice considerata:** taggare a mano i 5-10 moduli in Word senza alcun tooling. Scartata: la digitazione manuale dei tag da parte di un non tecnico è la prima fonte di run spezzati e template rotti; il wizard deterministico costa poco e produce l'audit trail che la compliance richiede.

---

## D2 — Rilevamento dei campi vuoti

**1. Decisione raccomandata:** DETERMINISTICO per il rilevamento; ibrido solo per l'etichettatura (e solo da S6).

**2. Motivazione:** Il "vuoto" è quasi sempre codificato nel markup: w:sdt con showingPlcHdr (vuoto certo), legacy FORMTEXT/w:ffData, MERGEFIELD (fldSimple e run-based), tab leader via w:tabs/@w:leader, celle tabella vuote (gestendo gridSpan/vMerge), text:placeholder/user-field per ODT; più regex sul testo di paragrafo **aggregato** (mai sul singolo run) per underscore/puntini digitati. Avvertenza tecnica confermata da più advisor: python-docx NON espone sdt/form field — serve lxml diretto su document.xml. L'argomento decisivo (l'insight più importante del consiglio, dall'avvocato del diavolo): **un campo vuoto NON rilevato è invisibile per sempre** — un "____" non taggato non è un segnaposto irrisolto per ADR-16 né un campo vuoto per ADR-21; è testo normale, passa tutti i controlli e produce un contratto con la riga bianca. Il recall del parser è quindi un requisito di SICUREZZA, non una preferenza di stile: non delegabile a un LLM non riproducibile.

**3. Divergenze esplicite:** Nessuna sul principio. Divergenza di formulazione sull'aliquota: un advisor asserisce "il deterministico fa il 95%" senza evidenza — il Chairman la declassa a ipotesi da misurare al gate S2, come chiesto dai peer reviewer.

**4. Rischi accettati e mitigazioni:** Falsi negativi da run frammentati e celle unite → ricucitura dei run, regex su testo aggregato, validazione recall al gate S2. Falsi positivi (linee decorative) che erodono la fiducia della segretaria → calibrare per alto recall ma misurare la precision; scarto con un click e **contatore di copertura con motivo dichiarato** per ogni candidato ignorato (i falsi negativi non muoiono in silenzio).

**5. Alternativa più semplice considerata:** rilevamento puro-LLM ("dai il file al modello"). Scartata: non deterministico, non riproducibile (stesso file → risultati diversi), ridondante dove il markup già dichiara il campo, e cieco proprio dove il fallimento è fatale.

---

## D3 — Il Dizionario

**1. Decisione raccomandata:** DATA DICTIONARY versionato, derivato per flattening dal modello dati canonico esistente, con **ruolo come binding e mai come prefisso**: nel template {{ locatore.nome }}, {{ conduttore.cognome }} — non nome_locatore.

**2. Motivazione:** È la correzione di livello più alto emersa dal consiglio (advisor dati/ontologia, adottata da tutti in peer review): col ruolo come binding verso una riga di Soggetto e l'attributo canonico unico, il drift {{nome_locatore}}/{{locatore_nome}} diventa **irrappresentabile per costruzione**, non solo vietato per regola; il dizionario resta piccolo (attributi + ruoli, non prodotto cartesiano) e docxtpl lo supporta nativamente. Il dizionario non nasce ex novo: seed generato dal modello dati (Soggetto, Immobile, ContrattoLocazione...), ancorato al lessico RLI per catasto e contratto (foglio, particella, subalterno, rendita_catastale, tipologia_contratto). Regola atomica dell'utente: CONFERMATA e generalizzata — nome+cognome; indirizzo scomposto (via/civico/cap/comune/provincia); date tipizzate con filtri di formato; **importo in lettere sempre derivato da filtro deterministico dal valore numerico, mai secondo campo memorizzato** (è logica di calcolo ex ADR-02, e due campi = due possibilità di discordanza). Regola dura sull'aggancio: **ogni voce ha obbligatoriamente un binding a campo canonico o una derivazione dichiarata (filtro/funzione); tag orfani vietati**, rifiutati dal lint al salvataggio del template (dry-run ADR-16), non aspettando che ADR-21 blocchi a valle. Governance: stati proposto/approvato/deprecato; nuovo tag solo via proposta → approvazione dello steward (stesso ruolo che approva i template, ADR-18) → changelog datato; deprecazione con alias di migrazione, mai cancellazione (i template depositati che usano il vecchio nome restano validi). Metadato di **obbligatorietà per-tag-per-template** (obbligatorio/opzionale/condizionale): è ciò che rende ADR-21 preciso — blocca sui campi richiesti da QUEL modulo, non su tutto il dizionario.

**3. Divergenze esplicite:** (a) Sulla nomenclatura: un advisor aveva proposto tag piatti con prefisso e nomenclatura mista ("locatore.nome_first") — criticata in peer review come pasticciata; il Chairman impone attributi in italiano, snake_case, ruolo come binding. (b) Sulle **voci composte** nel menu ("Nome e cognome del locatore"): proposte dall'advisor UX, adottate da tutti, ma con il dissenso a verbale di un peer reviewer che il Chairman fa proprio: sono SOLO scorciatoie di UI che si **espandono in tag atomici visibili nel diff di revisione** — mai tag compositi persistiti nel template, altrimenti si reintroduce il "nominativo" dalla finestra.

**4. Rischi accettati e mitigazioni:** Drift dentro il dizionario stesso se la governance si rilassa → steward unico, changelog, lint bloccante. Vocabolario RLI che cambia con le release ufficiali → versionamento del dizionario seguendo le release.

**5. Alternativa più semplice considerata:** lista piatta di stringhe di tag (l'idea originale dell'utente). Scartata: sposta il drift un livello più su invece di eliminarlo; il binding a oggetti costa lo stesso sforzo iniziale e rende il problema irrisolvibile alla radice.

---

## D4 — Ruolo dell'LLM

**1. Decisione raccomandata:** SOLO classificatore su vocabolario CHIUSO + proponente di tag nuovi con conferma umana obbligatoria; mai in scrittura sul file, mai generatore libero di nomi.

**2. Motivazione:** L'evidenza è netta: classificazione a set chiuso con constrained decoding elimina per costruzione la classe di errore "tag inventato"; la generazione libera produce i sinonimi che il dizionario vuole impedire. Meccanica: input = candidato (etichetta adiacente + contesto locale), MAI il file intero; output = un tag dell'enum o NESSUNA_CORRISPONDENZA/DA_RIVEDERE (opzione obbligatoria); reasoning-then-constrain (campo di motivazione libero PRIMA del campo vincolato) per mitigare il constraint tax sui 27B. Garanzia ADR-02 su barriere tutte deterministiche, in ordine: (1) **per costruzione** — l'LLM emette solo coppie (posizione → tag); l'inserimento del placeholder lo fa codice Python alla posizione XML nota, tag in un singolo run; l'LLM non ha fisicamente accesso in scrittura; (2) **per verifica** — invariante primario BLOCCANTE: **diff mascherato carattere-per-carattere** (testo estratto dall'originale coi vuoti mascherati ≡ testo estratto dal template coi placeholder mascherati); qualsiasi differenza fuori dai vuoti = salvataggio RIFIUTATO, non warning; in più render di prova con dati fittizi + apertura del DOCX come rete di sicurezza secondaria; (3) **per processo** — diff visuale affiancato con semaforo per la revisione umana; il template nasce BOZZA (ADR-17) e richiede approvazione per ruolo (ADR-18). La non-alterazione del testo legale è così garantita meccanicamente, non promessa.

**3. Divergenze esplicite:** (a) Sulla forma dell'invariante: un advisor proponeva anche il confronto delle parti XML non toccate — bocciato in peer review come tecnicamente sbagliato (la ricucitura legittima dei run altera l'XML senza alterare il testo); il Chairman fissa l'invariante sul **testo estratto**, non sull'XML. (b) Un advisor proponeva "render con contesto neutro + confronto" come verifica primaria — declassata a secondaria (il render introduce normalizzazioni proprie come variabile confondente). (c) Un peer reviewer dissente sulle prescrizioni fini (enum ≤50, classificazione gerarchica, self-consistency): premature per 5-10 documenti una tantum — il Chairman le mette a verbale come **linee guida per S6**, non requisiti di progetto ora. (d) Caveat condiviso da due peer reviewer, adottato: la statistica "allucinazioni 17-88%" riguarda la generazione legale libera, non la classificazione vincolata — non va usata come evidenza per questo caso d'uso; l'argomento contro l'LLM-in-scrittura regge da solo (corruzione dei run + non verificabilità).

**4. Rischi accettati e mitigazioni:** Constraint tax sul 27B locale → reasoning-then-constrain + opzione NESSUNA_CORRISPONDENZA + revisione umana su bassa confidenza. Mappature errate ma plausibili → l'umano conferma sempre; l'LLM pre-seleziona, non decide.

**5. Alternativa più semplice considerata:** nessun LLM, mai (solo dropdown manuale). Tenuta come baseline: è esattamente il piano S2; l'LLM di S6 si aggiunge sopra la stessa UI solo se le metriche lo giustificano (D5/D6).

---

## D5 — Sequenza e privacy

**1. Decisione raccomandata:** S2 = deterministico + umano (parser + wizard + dizionario + diff + bozza), autosufficiente; LLM-assist da S6, in locale, sopra la stessa pipeline. Moduli "vuoti": **divieto cloud totale — nessun file dell'agenzia lascia il Mac**; per lo sviluppo cloud solo moduli sintetici ricreati ex novo.

**2. Motivazione:** La pipeline S2 senza LLM basta per il gate pre-codice sui 5-10 modelli reali depositati e non crea dipendenza dal modello che arriva in S6; l'LLM si innesta poi come pre-selezione del dropdown (stessa schermata, meno click, zero rework). Sul cloud: un modulo "vuoto" in astratto non contiene dati personali, ma i file reali portano metadati (autore, revisioni/track-changes, commenti), residui di compilazioni precedenti, intestazioni e know-how dei modelli depositati; e una regola con eccezioni da arbitrare caso-per-caso prima o poi viene applicata male, specie da non tecnici. Il costo della regola assoluta è quasi zero (ricreare 5-10 moduli sintetici con gli stessi pattern ____/puntini/tabelle è banale, e in S2 l'LLM non serve comunque).

**3. Divergenze esplicite:** L'avvocato del diavolo aveva aperto alla via alternativa "sanificazione verificata con checklist" per moduli reali verso il cloud. **Respinta dal Chairman** con la maggioranza (4 su 5 e tutti i peer reviewer): reintroduce il giudizio caso-per-caso che il divieto assoluto elimina; lo stesso advisor chiudeva con "nel dubbio, no". Sulla sequenza nessuna divergenza: 5/5.

**4. Rischi accettati e mitigazioni:** Si rinuncia a testare l'LLM-assist su moduli reali prima di S6 → accettato: il gate S2 valida comunque parser+wizard sui moduli reali IN LOCALE; i sintetici bastano per sviluppare l'infrastruttura cloud. Rischio che l'LLM-assist di S6 arrivi sovradimensionato → condizionato alle metriche (D6).

**5. Alternativa più semplice considerata:** aspettare S6 e fare tutto con l'LLM. Scartata: la templatizzazione serve in S2 per il gate pre-codice; e il pezzo deterministico va costruito comunque perché è la barriera ADR-02.

---

## D6 — Migliorie e alternative

**1. Decisione raccomandata:** Adottare, in ordine di priorità: (1) **wizard di marcatura assistita** come deliverable centrale di S2 (candidati evidenziati, menu a tendina in italiano raggruppato per categoria, semaforo mappati/da-rivedere/ignorati, anteprima PDF con dati finti riconoscibili); (2) **memoria delle etichette** (etichetta_normalizzata → tag confermato, zero LLM, già in S2): il quick-win col miglior rapporto valore/costo del consiglio; (3) **lint del dizionario nel dry-run ADR-16** (placeholder fuori catalogo = errore in italiano semplice) + estensione con l'invariante di testo; (4) **golden test in CI per ogni versione template** (render con contesto campione, diff del testo fisso, apertura DOCX, nessun segnaposto irrisolto), agganciato all'hash ADR-18; (5) **flag automatico "richiede ri-deposito CCIAA"** quando il diff tocca il testo fisso + **audit trail di templatizzazione** per versione (originale+hash, candidati con evidenza XML, mappa campo→tag, report diff, approvatore); (6) **catalogo di filtri Jinja approvati e testati** per le ricomposizioni (nome_completo, indirizzo_su_una_riga, in_lettere, data_it); (7) **misurare prima di automatizzare**: loggare in S2 la quota di candidati risolti dal matching deterministico etichetta→alias; se ≥85-90%, l'LLM-assist di S6 si limita al residuo o si rinvia.

**2. Motivazione:** Ogni voce ha un proponente identificato nel consiglio e ha superato la peer review; insieme, spostano il baricentro dal "magico" (LLM) al "noioso che funziona" (parser + UI + test + audit), coerente col principio deterministic-first del progetto.

**3. Divergenze esplicite:** (a) Voci composte nel menu: adottate con la restrizione di D3 (solo UI, espansione atomica visibile). (b) Add-in dentro Word stile Afterpattern: proposto come possibile riferimento UX, **scartato** su parere dell'advisor operatività (fragile, manutenzione, fuori dal gestionale) — la schermata web nel gestionale è coerente con FastAPI+PDF.js. (c) docassemble/SaaS di document assembly: bocciati da tutti come componenti; se ne riusa solo il pattern. (d) La soglia 85-90% è un'ipotesi asserita, non misurata: vale come criterio di decisione, non come previsione.

**4. Rischi accettati e mitigazioni:** La memoria delle etichette con fuzzy matching può produrre pre-match sbagliati silenziosi → mitigazione: l'umano conferma sempre, e il pre-match è visivamente distinto dalla conferma. L'apprendimento via alias richiede comunque approvazione per non reintrodurre drift.

**5. Alternativa più semplice considerata:** nessun wizard — solo il parser che stampa la lista dei vuoti e tagging manuale in Word. Scartata: rimette in mano a un non tecnico l'inserimento dei tag nel file (run spezzati, template rotti) e perde l'audit trail.

---

## (a) ADR PROPOSTI (numerazione da ADR-64)

- **ADR-64 — Dizionario dei Campi (vocabolario canonico):** il dizionario è un data dictionary versionato in git, generato come flattening deterministico del modello dati canonico e ancorato al lessico RLI; voci con stato proposto/approvato/deprecato, steward umano, changelog datato, deprecazione con alias e mai cancellazione. Nessun placeholder può esistere fuori dal dizionario approvato.
- **ADR-65 — Ruolo come binding, granularità atomica:** nei template il ruolo (locatore, conduttore, garante...) è un binding a oggetti ({{ locatore.nome }}), mai un prefisso fuso nel nome del tag; gli attributi sono atomici (nome/cognome, indirizzo scomposto, date tipizzate, importi numerici); le ricomposizioni (nome completo, importo in lettere, indirizzo su una riga) sono esclusivamente filtri Python deterministici approvati e testati, mai campi duplicati e mai output dell'LLM.
- **ADR-66 — Aggancio obbligatorio tag→dato:** ogni voce del dizionario ha obbligatoriamente un binding a un campo del modello dati canonico o una derivazione dichiarata; i tag orfani sono rifiutati al salvataggio del template (lint nel dry-run ADR-16), non alla generazione. Metadato di obbligatorietà per-tag-per-template per rendere preciso il blocco ADR-21.
- **ADR-67 — Templatizzazione assistita deterministica:** il rilevamento dei campi vuoti è deterministico (lxml su sdt/showingPlcHdr, FORMTEXT, MERGEFIELD, tab leader, celle vuote, regex su testo aggregato; odfdo per ODT); l'inserimento dei placeholder è esclusivamente codice deterministico su copia, tag in singolo run; il wizard impone il contatore di copertura con motivo dichiarato per ogni candidato scartato.
- **ADR-68 — Invariante di non-alterazione (bloccante):** al salvataggio di un template templatizzato, il testo estratto dall'originale coi vuoti mascherati deve essere identico carattere-per-carattere al testo del template coi placeholder mascherati; diff non vuoto = salvataggio rifiutato. Render di prova con dati fittizi e verifica di integrità del DOCX come controllo secondario. Se il testo fisso differisce dal modello depositato: flag automatico "richiede ri-deposito CCIAA". Audit trail di templatizzazione (originale+hash, candidati, mappa, diff, approvatore) agganciato alla versione template.
- **ADR-69 — LLM solo classificatore su vocabolario chiuso:** l'LLM (locale, da S6) riceve solo il candidato con etichetta e contesto, mai il file; emette solo un tag dall'enum del dizionario approvato (constrained decoding, reasoning-then-constrain, opzione obbligatoria NESSUNA_CORRISPONDENZA) o una proposta di tag nuovo; ogni proposta richiede approvazione umana; l'LLM non ha mai accesso in scrittura a file o dizionario.
- **ADR-70 — Divieto cloud assoluto per i file dell'agenzia:** nessun file proveniente dall'agenzia (inclusi i moduli "vuoti": metadati, revisioni, residui, know-how dei depositati) lascia il Mac; per sviluppo e test su cloud si usano esclusivamente moduli sintetici ricreati ex novo. Nessuna eccezione né procedura di sanificazione caso-per-caso.

## (b) Collocazione in roadmap

- **S2 (modulo documentale):** parser deterministico dei vuoti; dizionario seed dal modello dati + RLI; wizard di marcatura assistita (menu in italiano, voci composte con espansione atomica, semaforo, anteprima PDF con dati finti); memoria delle etichette; lint dizionario + invariante di non-alterazione nel dry-run; audit trail e flag ri-deposito; golden test in CI; logging della quota di risoluzione deterministica. Tutto senza LLM, tutto in locale.
- **S3–S5:** nessun lavoro su questa feature oltre manutenzione dizionario (aggiunte via governance ADR-64) e raccolta metriche d'uso.
- **S6 (modello locale disponibile):** SOLO SE i log di S2 mostrano risoluzione deterministica < ~85-90%: layer LLM-assist come pre-selezione del dropdown sul residuo ambiguo, secondo ADR-69; le prescrizioni fini (enum ≤50, classificazione gerarchica, self-consistency) valgono come linee guida di implementazione in questa fase, non prima.

## (c) Verifiche esterne / gate necessari

1. **Gate pre-codice S2 (esteso):** sui 5-10 modelli reali depositati in CCIAA, oltre a conversione/font/dry-run/confronto stampa-anteprima già previsti, misurare: recall del parser sui campi vuoti (requisito di sicurezza — un campo mancato è invisibile ad ADR-16/21), precision (falsi candidati per modulo, soglia di tollerabilità per la segretaria), quota di pre-match deterministico etichetta→tag, esito dell'invariante di non-alterazione su tutti e 5-10.
2. **Test di usabilità con la segretaria** sul wizard S2: un modulo grezzo → template bozza senza assistenza tecnica, tempo e punti di frizione a verbale.
3. **Gate S6 (condizionale):** prima di costruire l'LLM-assist, verificare sui log S2 la quota residua non risolta dal deterministico; validare il classificatore 27B su un set etichettato interno (non esistono benchmark pubblici per legale italiano su questo compito) con conferma umana obbligatoria in ogni caso.
4. **Verifica periodica release RLI:** allineamento del dizionario alle release ufficiali dell'Agenzia delle Entrate (voci catastali/contrattuali), via governance ADR-64.

Il consiglio RACCOMANDA quanto sopra; l'approvazione — inclusi gli ADR-64…70 proposti — spetta all'utente.