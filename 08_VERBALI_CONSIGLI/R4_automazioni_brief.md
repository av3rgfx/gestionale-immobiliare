# R4 — Brief: automazioni self-service per JARVIS

*Verificato via web il 13/07/2026.*

## Verifica n8n (licenza, requisiti, LLM→workflow)

**Licenza.** n8n è distribuito sotto **Sustainable Use License** (più Enterprise License per alcune feature): è "fair-code", **non open source secondo OSI** perché impone limitazioni d'uso. Consente l'**uso interno aziendale anche a scopo commerciale** (il caso dell'agenzia rientra pienamente), modifica e distribuzione non commerciale; vieta white-labeling, hosting/rivendita a terzi e la raccolta di credenziali di utenti terzi ([docs n8n – Sustainable Use License](https://docs.n8n.io/privacy-and-security/sustainable-use-license), [blog n8n](https://blog.n8n.io/announcing-new-sustainable-use-license/)). Per questo progetto la licenza **non è un ostacolo**; è però un vincolo "politico" (niente OSI) da registrare.

**Requisiti/footprint.** Via npm richiede **Node.js 20.19–24.x** ([docs n8n](https://docs.n8n.io/deploy/host-n8n/install-options/install-with-npm)); DB di default **SQLite** (`~/.n8n/database.sqlite`), con PostgreSQL raccomandato oltre ~10 workflow attivi o con webhook intensivi ([docs n8n – supported databases](https://docs.n8n.io/hosting/configuration/supported-databases-settings/), [Cherry Servers](https://www.cherryservers.com/blog/n8n-self-hosting-requirements)). Minimo ~2 GB RAM: il Mac M4 lo regge senza problemi; il costo vero è **una seconda applicazione web sempre accesa da aggiornare, backuppare e imparare**, con un proprio DB, proprio scheduler e proprie credenziali — duplicato di ciò che il gestionale ha già.

**API.** Esiste una REST API pubblica: `POST /api/v1/workflows` crea workflow (nati inattivi, attivazione separata) con API key ([docs n8n – API](https://docs.n8n.io/api/)). Tecnicamente JARVIS potrebbe generare workflow n8n.

**LLM→workflow, maturità.** L'**AI Workflow Builder** ufficiale è nato **cloud-first**: il team ha dichiarato in beta che il self-hosted sarebbe arrivato "dopo", con crediti a consumo perché il servizio AI ha costi reali; prompt e definizioni del workflow vengono inviati al servizio AI di n8n (non le credenziali) ([community n8n](https://community.n8n.io/t/ai-powered-workflow-building-coming-soon/196499), [docs n8n – AI Workflow Builder](https://docs.n8n.io/build/ways-of-building-workflows/ai-workflow-builder)). **Incompatibile col vincolo "nessun dato verso cloud"**. Nota architetturale importante: n8n stesso non fa generare JSON libero all'LLM — ogni modifica passa da **tool validati contro lo schema dei nodi** ("hallucinations get stopped at the tool boundary") ([deep-dive](https://medium.com/@rajveer.rathod1301/inside-n8ns-ai-workflow-builder-a-complete-architecture-deep-dive-f2eeb2d57ec8)); la generazione libera di JSON n8n da parte di LLM generici è notoriamente fragile ([OpenAI community](https://community.openai.com/t/llm-generated-n8n-workflows-with-openai-api/1359500)). Questo conferma la via del "catalogo chiuso".

## Panorama alternative

| Soluzione | Licenza | Dipendenze / footprint | Manutenzione | Adattezza (1 utente non tecnico, Mac, locale) |
|---|---|---|---|---|
| **n8n** | SUL (fair-code, non OSI) | Node 20.19–24, SQLite/PG, servizio dedicato | Alta: seconda app, aggiornamenti frequenti | Media: GUI ricca ma è un secondo sistema da imparare; AI builder legato al cloud |
| **Node-RED** | Apache-2.0 (OpenJS Foundation) | `npm i -g node-red`, Node.js, porta 1880 | Media: leggero, stabile | Bassa: paradigma flow-based pensato per sviluppatori/IoT ([nodered.org](https://nodered.org/docs/getting-started/local), [LICENSE](https://github.com/node-red/node-red/blob/master/LICENSE)) |
| **Activepieces** | MIT (core) + feature EE commerciali | Docker; produzione: Postgres+Redis (esiste modalità PGLite/in-memory per uso singolo) | Media/alta: stack Docker da gestire | Media: GUI semplice stile Zapier, ma comunque un secondo prodotto ([license](https://www.activepieces.com/docs/about/license), [install](https://www.activepieces.com/docs/install/options/docker)) |
| **Windmill** | AGPLv3 (core) + EE | docker-compose, PostgreSQL, worker | Alta | Bassa: pensato per sviluppatori (script TS/Python) ([GitHub](https://github.com/windmill-labs/windmill), [self-host](https://www.windmill.dev/docs/advanced/self_host)) |
| **Huginn** | MIT | Ruby on Rails + MySQL/PostgreSQL; **ultima release 2022**, sviluppo poco attivo | Alta (stack Ruby datato) | Bassa ([GitHub](https://github.com/huginn/huginn)) |
| **Automazioni come righe di config nel DB** (motore interno) | nessuna nuova licenza | **zero nuove dipendenze**: tabella `automation` + scheduler launchd/FastAPI ed entità Task già esistenti | Minima: qualche centinaio di righe di codice proprio | **Massima**: UI dentro il gestionale, in italiano, approvazione con diff già prevista (ADR-07) |

**Lettura.** Tutti i motori esterni portano un secondo sistema con proprio DB, proprie credenziali e propria superficie d'attacco, per un carico (~200 contratti, un utente) che uno scheduler già esistente copre banalmente. Con la regola "vince la soluzione più noiosa che funziona", **l'opzione consigliata è il motore interno**: n8n resta la scelta sensata solo se in futuro servissero decine di integrazioni SaaS esterne — scenario escluso dal vincolo no-cloud.

## Pattern sicuri per automazioni create dall'AI

Lo stato dell'arte converge su tre principi, tutti compatibili con gli ADR esistenti:

1. **Catalogo chiuso invece di workflow arbitrari.** OWASP (LLM Top 10, "Excessive Agency") prescrive: limitare le funzioni al minimo, **allowlist di azioni approvate**, permessi minimi, e **approvazione umana per le azioni ad alto impatto** ([Oligo/OWASP](https://www.oligo.security/academy/owasp-top-10-llm-updated-2025-examples-and-mitigation-strategies), [FireTail](https://www.firetail.ai/blog/llm06-excessive-agency)). In pratica: l'LLM **non genera codice né JSON libero** (coerente con ADR-04), ma **compila i parametri di uno schema dichiarativo** `trigger + condizione + azione` scelti da elenchi chiusi, validati con Pydantic/JSON Schema lato server. È lo stesso approccio "mutazioni validate al confine del tool" adottato internamente da n8n.
2. **Prior art del modello dichiarativo.** Home Assistant usa esattamente trigger/condizione/azione e lo spiega ai non tecnici come una frase: "*Quando* Paulus arriva a casa *e* dopo il tramonto: *accendi* le luci" ([Home Assistant docs](https://www.home-assistant.io/docs/automation/basics/)). È il formato di presentazione da replicare.
3. **Approvazione e ciclo di vita.** Prima dell'attivazione: (a) JARVIS mostra l'automazione come **frase QUANDO/SE/ALLORA** più il record di configurazione (il "diff leggibile" di ADR-07); (b) **dry-run** su dati storici ("nelle ultime 2 settimane sarebbe scattata 3 volte, ecco cosa avresti ricevuto"); (c) creata **disattivata**, attivazione con conferma esplicita; (d) ogni esecuzione loggata, pulsante "pausa/elimina" e limite anti-tempesta (es. max N notifiche/giorno per regola).

## Trigger email: opzioni e rischi (prompt injection)

**Lettura casella.** **IMAP polling** (ogni 2–5 minuti, dallo scheduler esistente, con `imaplib`/`imap-tools`) è l'opzione più noiosa e universale: funziona con qualunque provider e tutto resta sul Mac. Per Gmail: dal **14 marzo 2025** l'accesso IMAP/SMTP/POP con la password dell'account ("less secure apps") è disattivato per tutti gli account; restano **OAuth** oppure le **app password** (16 caratteri, richiedono verifica in due passaggi attiva) ([Google Workspace](https://knowledge.workspace.google.com/admin/sync/transition-from-less-secure-apps-to-oauth), [Google – App passwords](https://support.google.com/mail/answer/185833)). La **Gmail API** richiede un progetto OAuth su Google Cloud: più complessa e senza vantaggi per un solo utente in polling — sconsigliata. Privacy: scarico IMAP + riassunto via Ollama = l'email non lascia mai il Mac; l'unica uscita resta l'SMTP di notifica già ammesso.

**Prompt injection: rischio reale e documentato.** Nel 2025 è stato dimostrato l'attacco alle **sintesi email di Gemini**: istruzioni nascoste nell'email (testo bianco, font zero) fanno sì che il riassunto AI contenga un falso avviso di phishing "firmato Google" ([0din](https://0din.ai/blog/phishing-for-gemini), [Security Boulevard](https://securityboulevard.com/2026/01/google-gemini-ai-flaw-could-lead-to-gmail-compromise-phishing-2/)); Microsoft 365 Copilot e i connettori ChatGPT hanno avuto bug di **esfiltrazione zero-click** corretti nel 2025. Simon Willison definisce la "**lethal trifecta**": dati privati + contenuto non fidato + capacità di comunicare verso l'esterno ([simonwillison.net](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/)). Il nostro sistema ha i primi due e, via SMTP, un pezzo del terzo. **Mitigazioni da adottare**: l'email è **input non fidato** — il riassunto è solo testo informativo, **mai** sorgente di azioni (nessun tool esposto all'LLM durante la sintesi); HTML convertito in testo e contenuto delimitato nel prompt; link riportati come testo non cliccabile; notifiche **solo verso destinatari fissi hardcoded** (il proprietario), mai desunti dal contenuto; banner "riassunto AI di contenuto non verificato: non seguire istruzioni contenute nell'email"; qualsiasi proposta operativa nata da un'email passa comunque dall'approvazione umana (ADR-07). Nessun filtro elimina il rischio al 100%: la difesa vera è **architetturale** (il riassunto non può causare azioni).

## Catalogo proposto di automazioni pre-costruite

| # | Automazione | Trigger | Azione | Valore | Complessità |
|---|---|---|---|---|---|
| 1 | Riassunto email cliente in watchlist | Nuova email da mittente X (IMAP) | Notifica con riassunto LLM locale | Alto | Media |
| 2 | Promemoria scadenza contratto | Data scadenza − 90/60/30 gg | Task + email | Alto | Bassa |
| 3 | Promemoria adeguamento ISTAT canone | Anniversario contratto | Task con dati contratto | Alto | Bassa |
| 4 | Alert canone non incassato | Giorno N del mese, pagamento assente | Notifica elenco morosi | Alto | Media |
| 5 | Report settimanale incassi | Cron lunedì 08:00 | Email riepilogo entrate/attesi | Medio | Bassa |
| 6 | Email cliente senza risposta da >N gg | Scansione thread giornaliera | Promemoria | Medio | Media |
| 7 | Registrazione contratto (RLI) entro 30 gg dalla stipula | Nuovo contratto inserito | Task con scadenza | Alto | Bassa |
| 8 | Scadenze certificazioni (APE, caldaia) | Data documento − 60 gg | Notifica | Medio | Bassa |
| 9 | Rassegna nuove pratiche/documenti | Cron venerdì 17:00 | Email digest settimanale | Medio | Bassa |
| 10 | Digest mattutino task del giorno | Cron giorni feriali 08:00 | Notifica elenco task | Medio | Bassa |

Le 8 su 10 a complessità bassa usano **solo dati già nel DB + scheduler esistente**: partire da quelle; il trigger email (1, 6) è il modulo nuovo da aggiungere per secondo.

**Incertezze dichiarate**: la disponibilità self-hosted dell'AI Builder n8n a oggi non è documentata con chiarezza (la docs rimanda al pricing; la fase beta era cloud-only); i limiti pratici di SQLite in n8n provengono da guide terze, non da benchmark ufficiali; l'attività di Huginn è giudicata dalla data dell'ultima release (2022).

## Fonti (URL verificati)

- https://docs.n8n.io/privacy-and-security/sustainable-use-license — licenza SUL, fair-code, non OSI
- https://blog.n8n.io/announcing-new-sustainable-use-license/ — razionale della licenza
- https://docs.n8n.io/deploy/host-n8n/install-options/install-with-npm — Node.js 20.19–24.x
- https://docs.n8n.io/hosting/configuration/supported-databases-settings/ — SQLite default, PostgreSQL
- https://docs.n8n.io/api/ — REST API pubblica (creazione workflow)
- https://docs.n8n.io/build/ways-of-building-workflows/ai-workflow-builder — AI Workflow Builder, crediti, dati inviati
- https://community.n8n.io/t/ai-powered-workflow-building-coming-soon/196499 — beta cloud-first
- https://medium.com/@rajveer.rathod1301/inside-n8ns-ai-workflow-builder-a-complete-architecture-deep-dive-f2eeb2d57ec8 — architettura a tool validati
- https://nodered.org/docs/getting-started/local + https://github.com/node-red/node-red/blob/master/LICENSE — Node-RED (Apache-2.0)
- https://www.activepieces.com/docs/about/license + https://www.activepieces.com/docs/install/options/docker — Activepieces (MIT + EE; Docker/PG/Redis)
- https://github.com/windmill-labs/windmill + https://www.windmill.dev/docs/advanced/self_host — Windmill (AGPLv3)
- https://github.com/huginn/huginn — Huginn (MIT, Rails, ultima release 2022)
- https://www.oligo.security/academy/owasp-top-10-llm-updated-2025-examples-and-mitigation-strategies + https://www.firetail.ai/blog/llm06-excessive-agency — OWASP Excessive Agency, allowlist e HITL
- https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ — lethal trifecta
- https://0din.ai/blog/phishing-for-gemini + https://securityboulevard.com/2026/01/google-gemini-ai-flaw-could-lead-to-gmail-compromise-phishing-2/ — injection nelle sintesi email
- https://www.home-assistant.io/docs/automation/basics/ — modello trigger/condizione/azione
- https://knowledge.workspace.google.com/admin/sync/transition-from-less-secure-apps-to-oauth + https://support.google.com/mail/answer/185833 — fine LSA (14/3/2025), app password con 2FA
