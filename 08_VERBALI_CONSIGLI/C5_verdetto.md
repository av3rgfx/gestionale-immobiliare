# C5 — VERDETTO FINALE DEL CHAIRMAN (OCR, estrazione dati, Art. 7 e APE)

## Dove il consiglio concorda
Cinque su cinque bocciano GLM-OCR: Executor lo scarta "oggi stesso", Outsider e First Principles Thinker lo considerano un dibattito già chiuso, Expansionist lo chiama cul-de-sac, Contrarian aggiunge che OmniDocBench misura il dominio sbagliato. Unanimità sull'architettura deterministic-first: APE nativi → estrazione testo diretta (PyMuPDF/pdfplumber), niente OCR; CIE/passaporti → parser MRZ ICAO 9303 con checksum; OCR relegato al residuo (CI cartacee senza MRZ, documenti fotografati). Tutti concordano che il trigger "nazionalità straniera" è sbagliato e va sostituito da regole distinte per i tre adempimenti. TULPS 109 vale per tutti gli ospiti, indipendentemente dalla nazionalità.

## Dove il consiglio è diviso
Form di conferma: Contrarian demolisce il form precompilato come "teatro di sicurezza" (automation bias); Executor lo difende con campi gialli e nessun autosave. Statistica del test: Executor vuole 20 documenti e due giorni; Contrarian ribatte che 20 documenti sono rumore. Visione: Expansionist propone una piattaforma dati a 12 mesi (scoring energetico, aggancio AML): la review privacy la boccia come riuso oltre lo scopo (art. 5(1)(b) GDPR).

## Punti ciechi emersi
1. Codice fiscale come cross-check gratuito: ricalcolabile da nome/cognome/nascita con check digit proprio — validazione incrociata deterministica ignorata da tutti.
2. Autenticità APE: parsare un PDF falso è peggio che non parsarlo — verifica su registro regionale/SIAPE.
3. Mito "MRZ zero ML": leggere l'MRZ richiede comunque detection/OCR; solo il checksum è deterministico.
4. Soglie di accettazione e audit trail: nessuno quantifica l'errore per campo né propone di loggare le correzioni degli agenti come metrica di accuracy.
5. GDPR concreto: informativa, base giuridica, retention immagini, distinzione dati estratti vs immagine.
6. Nazionalità mancante e pratiche multi-soggetto: un flag anagrafico vuoto produce falsi negativi invisibili.

## La raccomandazione
1. Motore OCR — GLM-OCR: NO, definitivo. Pipeline finale: (i) APE nativi → testo diretto; (ii) CIE/passaporti → MRZ + checksum come gate bloccante; (iii) OCR solo per CI senza MRZ e foto, con PaddleOCR-VL candidato unico (italiano, Apache 2.0, Apple Silicon). Test su almeno 50 documenti reali. Criterio di kill: errore >2% su campi anagrafici → fallback al vision LLM principale, decisione chiusa senza terzo round.
2. Form anti-automation bias: niente "Conferma" cieca. Split-screen estratto/immagine, conferma campo-per-campo, salvataggio bloccato se checksum MRZ o cross-check CF falliscono, highlight solo sui campi a bassa confidenza, log di ogni correzione. La frizione è il feature, non il bug.
3. Matrice adempimenti con etichette parlanti: il sistema risolve internamente tipo pratica × categoria soggetto × registrazione e mostra compiti, non articoli: "Comunicazione Questura entro 48h — ospiti extra-UE" (art. 7 D.Lgs 286/98); "Comunicazione Alloggiati Web entro 24h — locazione turistica, tutti gli ospiti" (TULPS 109); art. 12 DL 59/78 gestito in silenzio come assorbito dalla registrazione AdE, con tooltip. Se la nazionalità manca, il sistema chiede: mai skip silenzioso. Bocciato il riuso dati senza nuova base giuridica.
4. Parsing APE robusto: whitelist dei layout regionali, regex per campo con validazione di dominio (classe A4–G, EPgl,nren numerico plausibile); layout non riconosciuto → coda di revisione umana, mai mapping silenzioso. Verifica autenticità su registro regionale/SIAPE dove disponibile.
5. Codice fiscale: ricalcolo deterministico da dati estratti + check digit; mismatch → blocco e revisione. Costo zero, valore alto.
6. Presidi GDPR: DPIA ex art. 35 prima del go-live; informativa e base giuridica per le scansioni; cancellazione immagini dopo estrazione (o retention breve e motivata); cifratura, accessi loggati, audit trail correzioni. Il processing locale su M4 è l'argomento privacy-by-design: usarlo.

## La prima cosa da fare
Assemblare il corpus di 50+ documenti reali (CI, CIE, passaporti, APE di almeno 3 regioni) e lanciare il bake-off PaddleOCR-VL + parser MRZ con checksum e criterio di kill al 2%. In parallelo, congelare la matrice adempimenti con le etichette parlanti.
