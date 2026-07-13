# Verdetto del Chairman — Consiglio C9 (Modalità Chiamata JARVIS, versione mobile, Tailscale)

> **Data:** 2026-07-13 · **Metodo:** skill `llm-council` (protocollo Karpathy adattato).
> **Partecipanti:** 5 advisor paralleli con lenti diverse (Architetto pragmatico, Avvocato del diavolo, Compliance/legale, Operatività utente, Dati e sicurezza) → peer review anonima incrociata (R1–R4) → Chairman → Progettista. Advisor/Chairman/Progettista su **Fable 5**; fase di ricerca fatti su modello forte con ricerca web.
> **Posta in gioco:** valutare la richiesta di una "modalità Chiamata" vocale in tempo reale per JARVIS e di 5 tool GitHub proposti dall'utente (databasement, bklit-ui, anime.js, NVIDIA/personaplex, livekit/agents), nella cornice — decisa dall'utente — di una **versione mobile completa del gestionale usata dal telefono via Tailscale**.
> **Fonti fatti:** brief di ricerca `R5_chiamata_mobile_brief.md` (stesso consiglio).
>
> **Certificazione del meccanismo (prima convocazione in ambiente Claude Code):** superata — (1) 5 opinioni da lavori separati e paralleli; (2) peer review che cita le altre opinioni per **etichetta anonima** (R1–R4, 82 citazioni); (3) Chairman con **divergenze esplicite** dichiarate voce per voce. Il consiglio completo via skill è quindi valido in questo ambiente.
>
> **STATO: RACCOMANDAZIONE. Gli ADR-55…63 NON sono ancora scritti nel registro `03_DECISIONI_CONSIGLIO.md`: attendono l'approvazione dell'utente.** Il consiglio raccomanda, l'utente approva.

---

# VERDETTO DEL CHAIRMAN — Consiglio C9

Convergenza sostanziale dei 5 advisor su tutto l'impianto; le divergenze reali sono puntuali e vengono dichiarate voce per voce. Il consiglio RACCOMANDA, l'utente APPROVA.

---

## D1 — Modalità Chiamata

**1. Decisione raccomandata:** SÌ, ma in Fase 3 (dopo go-live, dopo S9/S10) e con ambito blindato: a voce SOLO Q&A read-only + dettatura di proposte che finiscono in coda; l'esecuzione di scritture a voce è VIETATA sempre.

**2. Motivazione:** ADR-07 impone diff a video + conferma esplicita: chi guida non può leggere un diff, quindi un "sì" vocale è per definizione approvazione cieca (vietata). La promessa onesta è "prepara la pratica a voce, approvala da fermo". La regola del Parcheggio (ADR-03) vieta di iniziare prima del go-live. Interazione half-duplex push-to-talk in v1: il barge-in è la parte più fragile dello stack e non serve al caso d'uso.

**3. Divergenze esplicite:** Nessuno dissente sull'impianto (5/5). Divergenza sulla stima di latenza: l'Avvocato del diavolo dice 2-5 s/turno (includendo i relay DERP su rete cellulare), Operatività e Sicurezza dicono 1,5-3 s. Il Chairman recepisce la posizione più prudente subordinandola alla misura, non alla stima. L'advisor Sicurezza proponeva un "barge-in semplice" in v1: respinto a favore del push-to-talk puro (posizione di Operatività e Avvocato del diavolo, meglio argomentata).

**4. Rischi accettati e mitigazioni:** (a) gap aspettative "Iron Man" → aggiornare e far rifirmare la pagina "cosa NON fa JARVIS" (latenza dichiarata, niente full-duplex, scritture solo differite) PRIMA di costruire; (b) errori ASR con rumore d'auto → read-back verbale obbligatorio dei campi chiave prima di accodare; (c) rubber-stamping della coda → divieto del pulsante "approva tutto", diff mostrato voce per voce; (d) distrazione alla guida → risposte max 2 frasi by design, nessuna interazione visiva richiesta in movimento. PRECONDIZIONE BLOCCANTE: walking skeleton di ~1 settimana che misuri latenza end-to-end su 4G reale (incluso scenario DERP) e RAM a regime con conversazione lunga; se >4 s/turno, aspettative rifirmate o rinuncia.

**5. Alternativa più semplice considerata:** non farla affatto (solo chat testuale mobile). Scartata: il valore del Q&A a mani libere è reale e realizzabile nel perimetro ADR-02/07; ma l'animazione orb viene declassata da requisito a rifinitura finale — è inutile proprio nello scenario (guida) che la motiva.

---

## D2 — Stack voce locale

**1. Decisione raccomandata:** Glue custom minimale dentro il FastAPI esistente (WebSocket dal browser del telefono), NESSUN framework di orchestrazione né secondo servizio sempre acceso; STT = whisper.cpp large-v3-turbo con Core ML/ANE (fallback whisper medium quantizzato se la RAM non regge); LLM = Ollama 27B già residente; TTS = da decidere con le orecchie: prima benchmark di `say`/AVSpeech nativo macOS (zero dipendenze), poi Piper it_IT-paola via subprocess, fallback Kokoro-82M MLX. Processi voce avviati ON-DEMAND all'apertura della Chiamata e terminati alla chiusura.

**2. Motivazione:** Un solo utente vocale su rete privata non giustifica un media server WebRTC permanente. whisper.cpp è MIT, maturo, eccellente in italiano su Apple Silicon. Il TTS a chunk per frase abbatte la latenza percepita. XTTS v2 è escluso in modo dirimente (licenza CPML solo non commerciale, Coqui chiusa: nessuno da cui comprare licenza).

**3. Divergenze esplicite:** L'advisor Compliance proponeva come PRIMA scelta la combo nativa Apple SpeechTranscriber + AVSpeechSynthesizer: respinta come prima scelta da 4 peer review su 5 perché richiede macOS 26 in produzione e un helper Swift accanto a uno stack Python (frizione col vincolo 5). Resta valida la sua metà TTS (`say`/AVSpeech come processo) che il Chairman adotta come primo benchmark. Divergenza sul piano B: un advisor proponeva "Pipecat prima di LiveKit" come riserva pronta; il Chairman recepisce la posizione più dura: QUALSIASI framework (anche Pipecat BSD-2) ripassa dal permesso-dipendenze solo dopo fallimento documentato del glue custom.

**4. Rischi accettati e mitigazioni:** (a) budget RAM al filo (27B ~17GB + macOS 4-5GB = ~2-3GB residui, con KV-cache che cresce) → misura obbligatoria nel walking skeleton, anche con S9/bge-m3 attivo; (b) qualità TTS italiana percepita come "scadente" → demo audio al Proprietario a verbale PRIMA dell'impegno; (c) Piper attivo è GPL-3.0 (repo MIT archiviato) → uso solo come processo esterno via CLI, mai linkato; verificare la licenza della singola voce; passaggio dal permesso-dipendenze; (d) iOS interrompe l'audio del browser al blocco schermo/cambio app → progettare la riconnessione senza perdita di contesto.

**5. Alternativa più semplice considerata:** LiveKit Agents o Pipecat come framework pronti. Scartati: portano un servizio pesante sempre acceso (LiveKit) o comunque una dipendenza non necessaria per half-duplex single-user; i loro pattern HITL si copiano, non si installano.

---

## D3 — I 5 tool GitHub

### T1 — David-Crty/databasement
**1. Decisione:** SCARTARE.
**2. Motivazione:** Verificato: è una web app Laravel/PHP via Docker per gestire flotte di DB eterogenei — per un singolo SQLite locale duplica ADR-06 (sqlite3 .backup + launchd + offsite cifrato + restore test) aggiungendo un intero stack da mantenere e una nuova superficie d'attacco (pannello web, credenziali S3).
**3. Divergenze:** Nessuna, 5/5 per lo scarto.
**4. Rischi accettati:** RPO legato all'intervallo di schedulazione launchd; mitigazione futura: se servisse RPO di secondi, l'unico incremento sensato è Litestream (Apache-2.0, binario Go arm64), come ADR separato — non databasement.
**5. Alternativa più semplice:** nessun tool aggiuntivo, basta ADR-06. TENUTA: è la scelta corretta di default.

### T2 — bklit/bklit-ui
**1. Decisione:** SCARTARE.
**2. Motivazione:** Verificato: è una registry di componenti CHART per React/Next via shadcn. Doppio mismatch: il frontend è server-rendered FastAPI senza React, e sono grafici, non orb/waveform. Lo "Studio" è pure proprietario.
**3. Divergenze:** Nessuna, 5/5.
**4. Rischi accettati:** nessuno.
**5. Alternativa più semplice:** i template esistenti + checklist impeccable. Tenuta.

### T3 — juliangarnier/anime (anime.js)
**1. Decisione:** SCARTARE IN V1 (parcheggio, rivalutabile solo con permesso esplicito).
**2. Motivazione:** Libreria sana (MIT, vanilla, ~10KB) ma non necessaria: waveform live = Web Audio AnalyserNode + Canvas 2D (~50 righe, zero dipendenze); orb pulsante = CSS custom property pilotata dall'RMS dello stesso AnalyserNode. Vincolo 5: niente dipendenze senza necessità.
**3. Divergenze:** Nessuna sullo scarto in v1; sfumatura sull'eventuale rientro futuro: alcuni advisor indicano siriwave (MIT, no-dep, ma ferma al 2023) prima di anime.js se servisse l'estetica Siri esatta. Il Chairman registra l'ordine: nativo → siriwave → anime.js, sempre con permesso.
**4. Rischi accettati:** estetica meno "cinematografica" in v1; accettato — l'orb è rifinitura da fermo, non requisito.
**5. Alternativa più semplice:** nativa (AnalyserNode + Canvas + CSS). TENUTA come scelta.

### T4 — NVIDIA/personaplex
**1. Decisione:** SCARTARE (bocciatura netta).
**2. Motivazione:** Verificato: è un MODELLO speech-to-speech monolitico (base Moshi), non un orchestratore; richiede GPU NVIDIA + CUDA, ufficialmente NON gira su Apple Silicon (solo port community non mantenuti); non permette di collegare Ollama/whisper/Piper; un 7B in più non sta comunque in RAM accanto al 27B; pesi sotto NVIDIA Open Model License. Viola hardware, architettura, RAM e igiene di licenza.
**3. Divergenze:** Nessuna, 5/5.
**4. Rischi accettati:** rinuncia al full-duplex "Iron Man" → da scrivere nella pagina "cosa NON fa JARVIS".
**5. Alternativa più semplice:** pipeline componibile whisper.cpp + Ollama + TTS. Tenuta (è la D2).

### T5 — livekit/agents
**1. Decisione:** SCARTARE COME ADOZIONE, TENERE COME RIFERIMENTO ARCHITETTURALE.
**2. Motivazione:** Dei due proposti per la chiamata è nettamente il migliore (Apache-2.0, gira su Apple Silicon, plugin Ollama/whisper/Piper locali) — su questo la risposta al confronto chiesto dall'utente è: livekit/agents batte personaplex senza discussione. Ma impone un LiveKit media server WebRTC sempre acceso: secondo servizio pesante, RAM permanente e superficie d'attacco per UN utente vocale. I suoi pattern (approval gate, blocking HITL, turn detection) vanno copiati nel glue custom.
**3. Divergenze:** Nessuna sul verdetto; tutti e 5 riconoscono che è l'unico tecnicamente compatibile.
**4. Rischi accettati:** se il glue custom fallisse alla prova dei fatti su turn-taking, si rivaluta un framework (Pipecat prima di LiveKit) ripassando dal permesso-dipendenze.
**5. Alternativa più semplice:** glue custom (D2). Tenuta.

---

## D4 — Sicurezza Tailscale + HITL a voce

**1. Decisione raccomandata:** Difese a strati tutte obbligatorie: tailnet blindato (ACL default-deny, device approval, Tailnet Lock, MFA, key expiry, niente Funnel/exit-node/port-forwarding, bind app solo su localhost + interfaccia 100.x); Tailscale = trasporto, MAI autenticazione: login + ruoli ADR-08/ADR-50 restano obbligatori sopra la VPN; HITL a voce con gate deterministico NEL CODICE (pattern restartable-tool: token di approvazione generabile solo dalla UI dopo il render del diff, non forgiabile dall'LLM); read-only confermabile a voce con read-back, scritture SOLO coda + diff a video da fermi.

**2. Motivazione:** "Security boundaries belong in code, not in prompts": un gate nel prompt cade per persuasione o injection. La voce è un canale di input NON FIDATO come le email IMAP di S10 (errori ASR, radio, passeggeri, injection vocale): la trascrizione entra nell'evidence pack come contesto non fidato e viene loggata integralmente. Il telefono non contiene dati (client remoto): con blocco schermo forte + revoca nodo + invalidazione sessioni il rischio residuo da furto è basso.

**3. Divergenze esplicite:** Nessun dissenso sull'impianto. Divergenze di completezza sanate dal Chairman: l'advisor Operatività non chiedeva l'ADR di deroga per il control-plane Tailscale (gli altri 4 sì — adottato); l'advisor Sicurezza usava la formula ambigua "Funnel/Serve disabilitati" — chiarito: Funnel VIETATO, `tailscale serve/cert` invece è proprio il meccanismo raccomandato per l'HTTPS tailnet-only; solo Compliance portava il divieto di autenticazione vocale (art. 9 GDPR) e la procedura art. 33 — adottati integralmente.

**4. Rischi accettati e mitigazioni:** (a) control-plane Tailscale Inc. = terzo cloud che vede topologia e gestisce auth (non i dati, E2E) + relay DERP per il traffico cifrato in mobilità → deroga esplicita in ADR come per SMTP, DPA sottoscritto, registro trattamenti aggiornato, Headscale documentata come exit strategy non implementata; (b) telefono rubato → runbook scritto (revoca nodo, invalidazione sessioni, rotazione password, verifica audit) TESTATO una volta davvero, come il restore test ADR-06; (c) pressione dell'utente per "conferma a voce" → il divieto sta nel codice e in ADR firmato, non nella buona volontà; (d) rubber-stamping → no approva-tutto, poche proposte per sessione, evidence pack completo (campi estratti, diff, trascrizione, confidence); (e) audit: ogni accesso remoto loggato con utente + nodo tailnet, alert email su login da nodo nuovo, log delle proposte anche se rifiutate/scadute; niente audio persistito, solo trascrizioni con retention.

**5. Alternativa più semplice considerata:** Headscale/NetBird self-hosted per sovranità totale del control-plane. SCARTATA per ora: più manutenzione e un endpoint da esporre; per questa scala la scelta noiosa è Tailscale SaaS + Tailnet Lock, con Headscale come uscita documentata.

---

## D5 — Versione mobile

**1. Decisione raccomandata:** Web responsive + PWA installabile sulla STESSA app FastAPI server-rendered; NIENTE app nativa iOS/Android; lavoro collocato PRE-go-live come proprietà del gestionale base.

**2. Motivazione:** Un utente principale, rete privata, stack già server-rendered: un'app nativa sarebbe un secondo codebase + firma + distribuzione senza benefici, contro il vincolo 5. La PWA è anche la scelta migliore per compliance: nessun dato persistito sul telefono (service worker cache SOLO asset statici, mai dati clienti). Unica fonte design resta la checklist impeccable (una azione primaria per schermata, target touch ≥44px).

**3. Divergenze esplicite:** DIVERGENZA REALE sulla collocazione: Avvocato del diavolo e Compliance collocavano il responsive DOPO il go-live desktop; Architetto, Operatività e Sicurezza lo collocano PRE-go-live. Il Chairman decide per il PRE-go-live: la Parte A è cornice DECISA dall'utente, quindi è prodotto base; la regola del Parcheggio (ADR-03) vincola la Fase 2 di JARVIS, non il gestionale. Le peer review convergono 4/5 su questa lettura.

**4. Rischi accettati e mitigazioni:** (a) PDF.js pesante su mobile per documenti grandi → sempre affiancare il bottone "Apri/Scarica PDF" col viewer nativo del telefono; (b) upload foto documenti → `<input type=file accept=image/* capture=environment>` nativo, zero librerie, ricompressione server-side; (c) microfono: getUserMedia richiede HTTPS → certificati via `tailscale cert/serve` da fare SUBITO (prerequisito, non dettaglio), e test del mic su iOS sia in Safari sia in PWA standalone (storicamente capriccioso: se fallisce, la Chiamata si usa da tab Safari); (d) notifiche: Web Push iOS richiede PWA installata e transita da APNs (cloud Apple) → solo payload generico senza dati ("hai una proposta in attesa") oppure si resta su SMTP, canale primario; decisione a verbale.

**5. Alternativa più semplice considerata:** solo web responsive senza manifest PWA. Quasi tenuta: il manifest + icona costa pochissimo e dà avvio full-screen; service worker minimo o assente (su Tailscale l'offline non è un requisito). App nativa scartata senza appello.

---

## (a) ADR PROPOSTI

- **ADR-55 — Mobile = PWA responsive sullo stesso FastAPI.** Nessuna app nativa; HTTPS solo via tailscale cert sul tailnet; service worker cache solo asset statici, mai dati clienti offline; checklist impeccable unica fonte design anche su mobile.
- **ADR-56 — Deroga dichiarata n.2 al vincolo tutto-locale: control-plane Tailscale.** Tailscale Inc. tratta metadati (nodi, topologia, chiavi, DERP relay per traffico cifrato in mobilità), mai i dati; DPA sottoscritto, registro trattamenti aggiornato; Headscale come exit strategy documentata, non implementata.
- **ADR-57 — Hardening tailnet.** ACL default-deny (solo nodo-telefono Proprietario → porta app HTTPS del Mac), device approval, Tailnet Lock, MFA, key expiry, Funnel/exit-node/subnet-routing vietati, zero port-forwarding; app in bind solo su localhost + interfaccia 100.x; login + ruoli ADR-08/50 obbligatori sopra la VPN; audit di ogni accesso remoto con identità nodo + alert su nodo nuovo.
- **ADR-58 — Runbook telefono perso/rubato.** Procedura data-breach (valutazione art. 33 GDPR in 72h): revoca nodo Tailscale, invalidazione sessioni app, rotazione password, verifica audit; blocco schermo biometrico obbligatorio; runbook TESTATO una volta come il restore test ADR-06; sessioni mobili brevi con re-login.
- **ADR-59 — Perimetro modalità Chiamata (Fase 3).** A voce solo Q&A read-only + dettatura proposte in coda; esecuzione scritture a voce VIETATA; gate nel codice (token di approvazione non forgiabile dall'LLM); niente "approva tutto", diff voce per voce; half-duplex push-to-talk, niente barge-in in v1; risposte max 2 frasi; precondizione bloccante: walking skeleton ~1 settimana con misura latenza su 4G/DERP e RAM a regime (soglia 4 s/turno); pagina "cosa NON fa JARVIS" aggiornata e rifirmata prima di costruire.
- **ADR-60 — Canale vocale = input non fidato.** Trascrizione trattata come le email IMAP di S10 (contesto, mai istruzioni), loggata integralmente nell'evidence pack; read-back verbale dei campi chiave; nessun audio persistito, solo trascrizioni con retention definita; attivazione esplicita push-to-talk (mai ascolto continuo — tutela terzi in auto); DIVIETO di autenticazione vocale (art. 9 GDPR).
- **ADR-61 — Stack voce locale.** Glue custom in FastAPI (WebSocket), niente framework di orchestrazione né servizi voce sempre accesi (on-demand); STT whisper.cpp large-v3-turbo Core ML (fallback medium quantizzato); TTS deciso con demo audio al Proprietario nell'ordine: say/AVSpeech nativo → Piper it_IT-paola via subprocess (GPL-3.0 mai linkata, licenza voce verificata) → Kokoro-82M Apache-2.0; XTTS v2 VIETATO (CPML non commerciale).
- **ADR-62 — Notifiche mobile.** Canale primario resta l'email SMTP (deroga n.1); eventuale Web Push iOS solo con PWA installata e payload generico privo di dati (APNs = cloud Apple).
- **ADR-63 — UI voce nativa.** Orb e waveform con Web Audio AnalyserNode + Canvas 2D + CSS custom property (zero dipendenze); bklit-ui e personaplex scartati; anime.js/siriwave rivalutabili solo con permesso esplicito nuove dipendenze; l'animazione è rifinitura finale, non requisito.

## (b) Collocazione in roadmap

1. **Pre-go-live (percorso attuale):** sprint "mobile responsive + PWA" sul gestionale base (ADR-55) + setup tailscale cert/serve + hardening tailnet (ADR-57) + runbook furto (ADR-58). Le schermate nuove nascono responsive.
2. **Go-live** del gestionale senza AI, poi S6 (JARVIS testuale) come già pianificato.
3. **Fase 2 (post go-live):** S9, S10 — invariati.
4. **Fase 3:** modalità Chiamata (ADR-59/60/61/63), aperta dal walking skeleton di misura; l'orb per ultimo. Oggi si registrano solo gli ADR: zero righe di codice (ADR-03 rispettato).

## (c) Verifiche esterne obbligatorie prima della produzione

1. **DPA Tailscale** sottoscritto + aggiornamento del **Registro dei trattamenti** per i metadati del control-plane (accountability GDPR).
2. **DPIA "leggera" (art. 35 GDPR)** sulla combinazione voce + accesso remoto + AI, anche se probabilmente sotto soglia d'obbligo per 2-5 utenti.
3. **Verifica licenza della singola voce TTS** adottata (Piper it_IT-paola o altra) e conferma legale dell'uso interno server-side di software GPL-3.0 non distribuito.
4. **Definizione della retention delle trascrizioni vocali** nell'audit log, validata con il consulente privacy.
5. **Parere su art. 173 CdS / responsabilità civile** per la formulazione della policy d'uso alla guida ("il sistema non richiede mai sguardo o tocco in movimento") e sua inclusione nella pagina "cosa NON fa JARVIS" da far rifirmare al Proprietario.

Il consiglio raccomanda. La parola passa all'utente per l'approvazione degli ADR-55…63.

---

# Appendice A — Bozza di progettazione operativa (Progettista, Fable 5)

# BOZZA DI PROGETTAZIONE — Mobile, Tailscale, Modalità Chiamata JARVIS (post-Consiglio C9)

**Stato: BOZZA PRONTA PER APPROVAZIONE — nessuna riga di codice fino all'approvazione degli ADR-55…63.**

---

## 1. Sintesi in 5 righe

Il gestionale diventa anche mobile: stessa app FastAPI server-rendered, resa responsive e installabile come PWA, usata dal telefono del Proprietario tramite Tailscale (nessuna porta aperta su Internet, login e ruoli sempre obbligatori sopra la VPN).
La modalità Chiamata di JARVIS si fa, ma in Fase 3 e con perimetro blindato: a voce solo domande read-only e dettatura di proposte che finiscono in coda; ogni scrittura si approva sempre col diff a video, da fermi, mai a voce.
Lo stack voce è tutto locale sul Mac Mini: whisper.cpp per l'ascolto, TTS italiano scelto con demo audio, orchestrazione minimale dentro FastAPI, processi avviati solo a chiamata aperta.
Dei 5 tool proposti se ne adotta zero: quattro scartati, livekit/agents tenuto solo come riferimento architetturale da cui copiare i pattern.
Prima di costruire la Chiamata: walking skeleton di misura (latenza su 4G, RAM a regime) e pagina "cosa NON fa JARVIS" aggiornata e rifirmata.

---

## 2. Versione MOBILE del gestionale (decisa — Parte A)

**Approccio: web responsive + PWA installabile sulla STESSA app FastAPI. Nessuna app nativa iOS/Android.**

Perché: un utente principale, rete privata, stack già server-rendered. Un'app nativa vorrebbe dire un secondo codebase, firma Apple, distribuzione, aggiornamenti doppi — tutto contro il vincolo 5 ("stack noioso"), senza alcun beneficio per questo caso d'uso. La PWA è anche la scelta migliore per la privacy: sul telefono non resta nessun dato.

**Cosa si fa concretamente:**
- CSS responsive sui template esistenti (mobile-first sulle schermate nuove, adeguamento su quelle esistenti). Unica fonte design resta la checklist "impeccable": una sola azione primaria per schermata, target touch ≥ 44px, testo leggibile, niente gergo.
- Manifest PWA + icona per l'avvio full-screen dalla home del telefono. Service worker minimo o assente: se presente, cache SOLO degli asset statici (CSS, JS, icone), MAI dati clienti. Su Tailscale l'offline non è un requisito.
- HTTPS obbligatorio (prerequisito per PWA e microfono): certificati via `tailscale cert` + `tailscale serve`, validi solo sul tailnet. Da fare SUBITO, non è un dettaglio.

**Cosa cambia nelle schermate su telefono:**
- **PDF:** PDF.js resta, ma ogni documento ha sempre accanto il bottone "Apri/Scarica PDF" che passa al viewer nativo del telefono (PDF.js su mobile soffre con file grandi).
- **Upload foto documenti:** `<input type="file" accept="image/*" capture="environment">` nativo — apre la fotocamera senza librerie; ricompressione lato server. Zero dipendenze nuove.
- **Tabelle larghe:** scroll orizzontale nel proprio contenitore o vista a schede su schermo stretto; mai scroll orizzontale di pagina.
- **Notifiche:** canale primario resta l'email SMTP (deroga n.1 già dichiarata). Eventuale Web Push su iOS solo con PWA installata e con payload generico senza dati ("hai una proposta in attesa"), perché transita da APNs (cloud Apple). Decisione a verbale.
- **Nota microfono iOS:** getUserMedia va testato sia in Safari sia in PWA standalone (storicamente capriccioso). Se in standalone fallisce, la Chiamata si usa da tab Safari: nessun blocco.

**Roadmap: PRE-go-live.** La Parte A è cornice decisa dall'utente, quindi è prodotto base, non Fase 2 di JARVIS: la regola del Parcheggio (ADR-03) non si applica. Sprint dedicato "mobile responsive + PWA" prima del go-live; le schermate nuove nascono già responsive.

---

## 3. Accesso via Tailscale (deciso) — difese minime obbligatorie

Tailscale è il TRASPORTO, mai l'autenticazione. Tutte le difese seguenti sono obbligatorie, a strati:

1. **Tailnet blindato:** ACL default-deny — solo il nodo-telefono del Proprietario può raggiungere la porta HTTPS dell'app sul Mac Mini, nient'altro. Device approval attivo (ogni nuovo dispositivo va approvato a mano), Tailnet Lock, MFA sull'account Tailscale, key expiry attivo.
2. **Zero esposizione pubblica:** Funnel VIETATO, niente exit-node, niente subnet routing, zero port-forwarding sul router. L'app resta in bind solo su localhost + interfaccia 100.x. (`tailscale serve` invece è ammesso: è il meccanismo raccomandato per l'HTTPS tailnet-only.)
3. **Login + ruoli sopra la VPN:** essere sul tailnet NON basta: login applicativo e ruoli ADR-08/ADR-50 restano obbligatori. JARVIS solo per il ruolo Proprietario, come sempre.
4. **Telefono rubato — runbook scritto e TESTATO una volta** (come il restore test ADR-06): revoca del nodo dalla console Tailscale, invalidazione di tutte le sessioni app, rotazione password, verifica dell'audit log; valutazione data-breach art. 33 GDPR entro 72h. Il rischio residuo è basso perché il telefono non contiene dati: è solo un client. Obbligatori: blocco schermo biometrico, sessioni mobili brevi con re-login.
5. **Audit accessi remoti:** ogni accesso loggato con utente + identità del nodo tailnet; alert email al login da nodo mai visto prima.

**Impatto privacy:** il control-plane di Tailscale Inc. è un terzo servizio cloud che vede metadati (nodi, topologia, chiavi; relay DERP per il traffico, che resta cifrato end-to-end WireGuard) ma MAI i dati. Va dichiarato come **deroga n.2** al vincolo tutto-locale, come fu fatto per SMTP: ADR esplicito, DPA Tailscale sottoscritto, registro dei trattamenti aggiornato, DPIA leggera. Headscale (control-plane self-hosted) documentata come exit strategy, NON implementata: per questa scala la scelta noiosa è Tailscale SaaS + Tailnet Lock.

---

## 4. Modalità Chiamata JARVIS — cosa fa, cosa NON fa, HITL a voce

**Cosa FA (v1):**
- Q&A read-only a voce: "che appuntamenti ho domani?", "a che punto è la pratica Rossi?" — sull'elenco chiuso di funzioni di lettura (ADR-02).
- Dettatura di PROPOSTE di scrittura: JARVIS estrae i campi, fa il **read-back verbale dei campi chiave** ("ricapitolo: nuova pratica per Mario Rossi, immobile in via Verdi 12, giusto?") e alla conferma mette la proposta IN CODA. Nessun effetto sul database.
- Risposte massimo 2 frasi, by design: chi guida non deve né guardare né toccare lo schermo.
- Interazione half-duplex push-to-talk: si preme (o comando a bocca libera del telefono per premere), si parla, si ascolta. Niente barge-in in v1: è la parte più fragile e non serve al caso d'uso.

**Cosa NON fa (mai, in nessuna versione):**
- Non esegue scritture su comando vocale. Un "sì" detto guidando è un'approvazione cieca, e ADR-07 la vieta: il diff va LETTO. Il gate è NEL CODICE, non nel prompt: il token di approvazione è generabile solo dalla UI dopo il render del diff a video, non forgiabile dall'LLM ("security boundaries belong in code, not in prompts").
- Niente ascolto continuo / wake word: attivazione sempre esplicita (tutela anche dei terzi in auto).
- Niente autenticazione vocale (dato biometrico, art. 9 GDPR: vietata).
- Niente full-duplex "Iron Man": da scrivere nella pagina "cosa NON fa JARVIS", da far rifirmare PRIMA di costruire.

**HITL a voce — il flusso in due tempi:**
1. **In auto (a voce):** consulto dati + detto proposte → read-back → coda. La trascrizione integrale entra nell'evidence pack come **input NON fidato** (stesso trattamento delle email IMAP di S10: contesto, mai istruzioni). Nessun audio persistito, solo trascrizioni con retention definita.
2. **Da fermo (a video):** apro la coda sul telefono o sul desktop, vedo il diff leggibile di OGNI proposta, approvo o rifiuto una per una. VIETATO il pulsante "approva tutto". Anche le proposte rifiutate o scadute restano nell'audit log.

**Roadmap: Fase 3**, dopo go-live e dopo S9/S10 (Parcheggio ADR-03 rispettato). **Precondizione bloccante:** walking skeleton di ~1 settimana che misuri latenza end-to-end su 4G reale (incluso scenario relay DERP) e RAM a regime con conversazione lunga. Soglia: se >4 s/turno, si rifirmano le aspettative o si rinuncia. Oggi si approvano solo gli ADR: zero codice.

---

## 5. Stack voce locale (Mac Mini M4 24GB, tutto-locale)

**Orchestrazione:** glue custom minimale DENTRO il FastAPI esistente — un endpoint WebSocket: il browser del telefono manda l'audio del push-to-talk, il server risponde con audio a chunk. NESSUN framework di orchestrazione, NESSUN media server, NESSUN secondo servizio sempre acceso. I processi voce partono on-demand all'apertura della Chiamata e muoiono alla chiusura.

**Pipeline (tutto sul Mac Mini):**
- **STT:** whisper.cpp con modello large-v3-turbo via Core ML/ANE (MIT, maturo, ottimo in italiano su Apple Silicon). Fallback: whisper medium quantizzato se la RAM non regge.
- **LLM:** l'Ollama 27B già residente (nessun modello aggiuntivo).
- **TTS italiano — si decide con le orecchie**, demo audio al Proprietario a verbale, in quest'ordine: (1) `say`/AVSpeechSynthesizer nativo macOS (zero dipendenze); (2) Piper voce it_IT-paola via subprocess CLI — GPL-3.0, mai linkata, licenza della voce da verificare, passaggio dal permesso-dipendenze; (3) Kokoro-82M MLX (Apache-2.0). **XTTS v2 VIETATO** (licenza CPML non commerciale, Coqui chiusa: nessuno da cui comprare).

**Stima RAM:** 27B ≈ 17GB + macOS 4-5GB → residuo ~2-3GB. Whisper turbo ~1,5GB + TTS ~0,1-0,3GB ci stanno SOLO se on-demand e se il KV-cache del 27B è tenuto d'occhio. Misura obbligatoria nel walking skeleton, anche con S9/bge-m3 attivo.

**Stima latenza per turno:** STT 0,5-1s + LLM primo token 0,5-1,5s + TTS primo chunk 0,3-0,5s → **1,5-3s in condizioni buone, fino a 2-5s su cellulare via DERP** (stima prudente dell'Avvocato del diavolo). TTS a chunk per frase per abbattere la latenza percepita. Vale la misura, non la stima.

**Animazione voce:** nativa, zero dipendenze — waveform con Web Audio AnalyserNode + Canvas 2D (~50 righe); orb pulsante con CSS custom property pilotata dall'RMS. È rifinitura FINALE, non requisito: inutile proprio nello scenario (guida) che la motiva. Eventuale rientro futuro solo con permesso esplicito, nell'ordine: nativo → siriwave → anime.js.

**Resilienza:** iOS interrompe l'audio del browser al blocco schermo/cambio app → riconnessione WebSocket senza perdita di contesto conversazionale.

---

## 6. I 5 tool GitHub — una riga ciascuno

- **T1 databasement — SCARTARE:** web app Laravel/Docker per flotte di DB; per un singolo SQLite duplica ADR-06 aggiungendo stack e superficie d'attacco (eventuale upgrade futuro: Litestream, con ADR separato).
- **T2 bklit-ui — SCARTARE:** componenti chart per React/Next via shadcn; il frontend è FastAPI server-rendered senza React, e sono grafici, non orb.
- **T3 anime.js — SCARTARE IN V1 (parcheggio):** libreria sana ma non necessaria; waveform e orb si fanno nativi (AnalyserNode + Canvas + CSS); rivalutabile solo con permesso esplicito.
- **T4 personaplex — SCARTARE (netto):** modello speech-to-speech che richiede GPU NVIDIA/CUDA, non gira su Apple Silicon, non si collega a Ollama/whisper, non sta in RAM accanto al 27B, licenza NVIDIA restrittiva.
- **T5 livekit/agents — SCARTARE COME ADOZIONE, TENERE COME RIFERIMENTO:** dei due per la chiamata è nettamente il migliore (batte personaplex senza discussione: Apache-2.0, Apple Silicon, plugin locali), ma impone un media server sempre acceso per UN utente; i suoi pattern (approval gate, blocking HITL, turn detection) si COPIANO nel glue custom, non si installano.

---

## 7. ADR proposti (pronti per approvazione) e verifiche esterne

**ADR-55 — Mobile = PWA responsive sullo stesso FastAPI.** Nessuna app nativa. HTTPS solo via `tailscale cert/serve` sul tailnet. Service worker: cache solo asset statici, mai dati clienti offline. Checklist impeccable unica fonte design anche su mobile (una azione primaria per schermata, touch ≥ 44px). PDF sempre con bottone "Apri/Scarica" nativo accanto a PDF.js. Upload foto via input file nativo con capture, ricompressione server-side. Collocazione: sprint pre-go-live.

**ADR-56 — Deroga dichiarata n.2 al tutto-locale: control-plane Tailscale.** Tailscale Inc. tratta metadati (nodi, topologia, chiavi, relay DERP per traffico cifrato E2E), mai i dati. DPA sottoscritto, registro trattamenti aggiornato. Headscale documentata come exit strategy, non implementata.

**ADR-57 — Hardening tailnet.** ACL default-deny (solo nodo-telefono Proprietario → porta HTTPS app), device approval, Tailnet Lock, MFA, key expiry. Funnel/exit-node/subnet-routing vietati, zero port-forwarding. App in bind solo su localhost + 100.x. Login + ruoli ADR-08/50 obbligatori sopra la VPN. Audit di ogni accesso remoto con identità nodo + alert email su nodo nuovo.

**ADR-58 — Runbook telefono perso/rubato.** Revoca nodo, invalidazione sessioni, rotazione password, verifica audit; valutazione art. 33 GDPR in 72h. Blocco schermo biometrico obbligatorio, sessioni mobili brevi. Runbook TESTATO una volta davvero.

**ADR-59 — Perimetro modalità Chiamata (Fase 3).** A voce solo Q&A read-only + dettatura proposte in coda; esecuzione scritture a voce VIETATA. Gate nel codice: token di approvazione generabile solo dalla UI dopo il render del diff, non forgiabile dall'LLM. Niente "approva tutto", diff voce per voce. Half-duplex push-to-talk, niente barge-in in v1, risposte max 2 frasi. Precondizione bloccante: walking skeleton ~1 settimana con misura latenza 4G/DERP e RAM a regime, soglia 4 s/turno. Pagina "cosa NON fa JARVIS" aggiornata e rifirmata PRIMA di costruire.

**ADR-60 — Canale vocale = input non fidato.** Trascrizione trattata come le email IMAP di S10 (contesto, mai istruzioni), loggata integralmente nell'evidence pack. Read-back verbale dei campi chiave prima di accodare. Nessun audio persistito, solo trascrizioni con retention definita. Attivazione esplicita push-to-talk, mai ascolto continuo. DIVIETO di autenticazione vocale (art. 9 GDPR).

**ADR-61 — Stack voce locale.** Glue custom in FastAPI (WebSocket), niente framework né servizi voce sempre accesi (on-demand). STT whisper.cpp large-v3-turbo Core ML (fallback medium quantizzato). TTS deciso con demo audio al Proprietario nell'ordine: say/AVSpeech nativo → Piper it_IT-paola via subprocess (GPL-3.0 mai linkata, licenza voce verificata, permesso-dipendenze) → Kokoro-82M Apache-2.0. XTTS v2 VIETATO (CPML). Qualsiasi framework (anche Pipecat) solo dopo fallimento documentato del glue custom e nuovo permesso-dipendenze.

**ADR-62 — Notifiche mobile.** Canale primario resta l'email SMTP (deroga n.1). Eventuale Web Push iOS solo con PWA installata e payload generico privo di dati (APNs = cloud Apple).

**ADR-63 — UI voce nativa.** Orb e waveform con Web Audio AnalyserNode + Canvas 2D + CSS custom property, zero dipendenze. bklit-ui e personaplex scartati; anime.js/siriwave rivalutabili solo con permesso esplicito. L'animazione è rifinitura finale, non requisito.

**Roadmap complessiva:** (1) pre-go-live: sprint mobile PWA + tailscale cert/serve + hardening tailnet + runbook furto; (2) go-live senza AI, poi S6 (JARVIS testuale); (3) Fase 2: S9, S10 invariati; (4) Fase 3: modalità Chiamata, aperta dal walking skeleton, orb per ultimo.

**Verifiche esterne obbligatorie prima della produzione:**
1. DPA Tailscale sottoscritto + registro dei trattamenti aggiornato per i metadati del control-plane.
2. DPIA leggera (art. 35 GDPR) su voce + accesso remoto + AI.
3. Verifica licenza della voce TTS adottata + conferma legale dell'uso interno server-side di software GPL-3.0 non distribuito.
4. Retention delle trascrizioni vocali validata col consulente privacy.
5. Parere su art. 173 CdS / responsabilità civile per la policy d'uso alla guida ("il sistema non richiede mai sguardo o tocco in movimento"), inclusa nella pagina "cosa NON fa JARVIS" da far rifirmare.

**Fine bozza. In attesa di approvazione degli ADR-55…63 da parte dell'utente.**