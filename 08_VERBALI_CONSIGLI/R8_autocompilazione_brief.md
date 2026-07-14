# BRIEF RICERCA R8 — Auto-tagging moduli + dizionario canonico (fatti verificati con fonti)

> A supporto del Consiglio C10. Ricerca web del 2026-07-14. Distingue **fatti verificati** da ipotesi operative. Stack di riferimento: FastAPI + SQLite + **docxtpl** (Jinja2 in DOCX) + LibreOffice; principio deterministic-first; ADR-02 (LLM mai autore di testo legale).

## 1. Templatizzazione (da modulo grezzo a template con segnaposti)
- **docxtpl** (python-docx-template, v0.20.x, maturo): usa un `.docx` come template Jinja2 (`{{ variabile }}`, `{% for %}`, tag riga/cella/paragrafo `{%tr %}` `{%tc %}` `{%p %}`). **Limite chiave verificato:** un tag Jinja funziona solo se sta in **un unico run** dello stesso paragrafo; se Word spezza il testo in più run il tag si rompe → serve "Cancella formattazione" sul campo e tag in singolo run.
- **python-docx**: libreria di basso livello (base di docxtpl); utile per ispezione/normalizzazione dei run, non come motore di template (il find-replace naive rompe i placeholder spezzati).
- **docassemble** (open source), **HotDocs**, **Gavel/Documate**, **Afterpattern**: piattaforme di document assembly. **Fatto rilevante:** anche i migliori tool **fanno marcare le variabili da un umano** (add-in in Word, markup dichiarativo), **non** affidano la trasformazione del file a un LLM. Sono framework/SaaS: si riusa il *pattern*, non si integrano.
- **LLM per inserire i placeholder**: esistono solo come **assistenti di suggerimento**, non esiste uno standard che riscriva il DOCX in produzione. Far riscrivere l'XML del DOCX a un LLM **rompe i run e può alterare/omettere testo**. → Uso sicuro: l'LLM *propone* i campi/nomi, un umano rivede; **mai** sostituzione di testo senza diff di verifica.
- Best practice consolidata: lavorare su una **copia**; sostituire **solo** i valori variabili; **verifica per diff** del render (dati fittizi) contro l'originale.
- Fonti: pypi.org/project/docxtpl, docxtpl.readthedocs.io, github.com/elapouya/python-docx-template, docassemble docs.

## 2. Rilevamento deterministico dei campi vuoti (DOCX/ODT, senza LLM)
- **Fattibile con buona affidabilità** per tutti i costrutti a semantica esplicita nel formato: **tab leader** (puntini/underscore in `w:tabs/@w:leader`), **content control** (`w:sdt` con `w:showingPlcHdr` = vuoto certo), **legacy form field** (`FORMTEXT`/`w:ffData`), **MERGEFIELD** (`w:instrText`/`w:fldSimple`), **celle di tabella vuote** (gestendo `gridSpan`/`vMerge`); per ODT `text:placeholder`/user-field. Più **regex sul testo di paragrafo aggregato** (mai sul singolo run) per underscore/puntini digitati a mano.
- **Avvertenza verificata:** `python-docx` **non** espone sdt/form field → serve **lxml** diretto su `document.xml` (namespace OOXML). Per ODT: `odfdo`.
- Pipeline consigliata: **ibrida deterministic-first** — stadio 1 deterministico ad **alto recall** (il markup dichiara il campo), stadio 2 (solo etichettatura) eventualmente assistito.
- Fonti: python-docx.readthedocs.io (tab stops/leader), github.com/python-openxml/python-docx issues #589/#1370, learn.microsoft.com OOXML add-ins.

## 3. Vocabolario canonico e anti-drift (il "dizionario")
- Il drift dei nomi (`{{nome_locatore}}` vs `{{locatore_nome}}`) è **già risolto** dalla comunità legaltech, in modo maturo, **NON** con una lista piatta di stringhe ma con un **vocabolario controllato a oggetti**: un attore è un oggetto (`Individual`/`party`) con **attributi atomici** riutilizzabili (`name.first`, `name.last`, `address.city`…) e un campo **`role`** a valori controllati (locatore/conduttore/garante). Riferimento principale: **Document Assembly Line — Suffolk LIT Lab** su docassemble.
- Conseguenza: usare il **ruolo come binding a oggetti** (`{{ locatore.nome }}`), non come prefisso fuso (`nome_locatore`) → il drift diventa **irrappresentabile per costruzione** e il dizionario resta piccolo (attributi + ruoli, non prodotto cartesiano).
- Granularità atomica (regola dell'utente confermata e generalizzata): nome/cognome separati; indirizzo scomposto (via/civico/cap/comune/provincia); date tipizzate; **importo in lettere = filtro deterministico dal numero**, mai secondo campo. Ancoraggio al lessico **RLI** (Agenzia Entrate) per catasto/contratto (foglio, particella, subalterno, rendita, tipologia contratto).
- Fonti: assemblyline.suffolklitlab.org/docs/authoring/label_variables, docassemble.org/docs/objects, a2jauthor.org variable naming, **RLI Istruzioni (Agenzia delle Entrate)**.

## 4. Affidabilità dell'LLM (locale ~27B) per la mappatura
- **Fatto verificato (letteratura 2024-2026):** mappare un campo a un **tag esistente** (classificazione a **set chiuso**) è strutturalmente più affidabile che **generare** liberamente il tag. Il **constrained decoding / structured output** elimina per costruzione la classe di errore "tag inventato" (i token fuori dall'enum vengono azzerati al sampling).
- Pipeline consigliata: enum dei tag ammessi nel prompt; **campo di ragionamento libero PRIMA** del campo vincolato ("reasoning-then-constrain", mitiga il *constraint tax* sui modelli piccoli); opzione obbligatoria **`NESSUNA_CORRISPONDENZA`**; conferma umana sempre.
- Le statistiche "allucinazioni 17-88%" riguardano la **generazione legale libera**, **non** la classificazione vincolata: non vanno usate come prova contro questo caso d'uso (l'argomento contro l'LLM-in-scrittura regge da solo: corruzione dei run + non verificabilità).
- Fonti: getzep.com (reducing hallucinations), mbrenndoerfer.com (constrained decoding), letsdatascience.com (structured outputs), arxiv (structured output 2025-2026).

## Sintesi operativa per il Consiglio
L'idea è **buona nel fine**, da correggere nell'esecuzione: **l'LLM non scrive mai nel file** (rompe i run, altera il testo). Il deliverable centrale è un **wizard di templatizzazione deterministico** (rileva i vuoti dal markup, inserisce i `{{tag}}` via codice su una copia, verifica per diff che il testo fisso sia intatto); il **dizionario** è un vocabolario canonico a oggetti (ruolo-come-binding, attributi atomici) mappato al modello dati; l'**LLM (da S6, locale)** entra solo come **classificatore su vocabolario chiuso** che pre-seleziona il menu, con conferma umana. Nessun file dell'agenzia verso il cloud.
