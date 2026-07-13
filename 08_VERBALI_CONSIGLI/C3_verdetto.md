# C3 — VERDETTO FINALE DEL CHAIRMAN (Modulo documentale: template, anteprima, privacy)

## Dove il consiglio concorda
- Il design (a)-(d) regge e lo stack (FastAPI, docxtpl, LibreOffice, PDF.js) è giusto: nessuno propone di cambiarlo.
- PDF come template compilabile: NO, unanime. Il PDF resta solo artefatto o allegato.
- Il tracciamento della versione depositata in Camera di Commercio non è un'aggiunta: è il fondamento. Executor lo quantifica ("tre colonne nel DB"), First Principles Thinker lo erige ad architettura, Expansionist lo chiama il vero prodotto, Contrarian lo denuncia come la lacuna più grave.
- Anteprima via conversione PDF: strada giusta, purché ciò che vedi sia ciò che stampi (Contrarian, First Principles Thinker).
- Firma grafometrica: no, al più fase 2 (Executor).

## Dove il consiglio è diviso
- La cascata. Executor la costruisce con un context Jinja2 condiviso ("tecnicamente banale"). Contrarian la chiama trappola: moduli condizionali (mutuo senza mutuo) generati vuoti, documenti disallineati dopo le correzioni. First Principles Thinker propone di abolirla: ogni documento è proiezione on-demand dei dati canonici, non compilato da altri documenti. Expansionist vuole potenziarla in "genera pacchetto pratica".
- Privacy: Executor difende genera→stampa→firma→scansiona come pratica reale; Expansionist vuole subito la firma OTP via link; First Principles Thinker riformula la scansione come record immutabile di consenso; Contrarian scopre il buco del rinnovo informative.
- Import .doc/.odt: Executor accetta gli artefatti della conversione; Contrarian la considera una mina compliance (file non più identico al depositato).
- Outsider: scartato da tre revisori su cinque (critica la forma, non valida). Salvo solo il rilievo sulla carta reintrodotta nel punto più delicato.

## Punti ciechi emersi
- Dry-run segnaposti: nessuno valida i template con dati finti prima del salvataggio.
- Ruoli e permessi: chi crea, modifica, approva un template depositato.
- Conservazione a norma (CAD, D.Lgs 82/2005): hash e timestamp da soli non danno valore probatorio alle scansioni.
- Dati mancanti: campo vuoto → buco silenzioso nel documento.
- Errori comprensibili per la segretaria e controllo pre-stampa.
- Rinnovo informative e coesistenza di versioni su pratiche in corso; backup e verifica d'integrità dell'archivio.

## La raccomandazione
(a) Abolisco la compilazione in cascata documento-da-documento: mi schiero con il First Principles Thinker. Se ogni documento si renderizza on-demand dagli stessi dati canonici e dalla versione di template approvata, il disallineamento non può esistere. Restano le tre categorie per la segretaria (Contratti, Moduli di pratica, Autonomi), ma "legato" diventa un'associazione predefinita con condizioni (modulo mutuo solo se la pratica prevede mutuo) e un tasto "Genera pacchetto pratica" che renderizza tutto in blocco come istanze. Correzione di un dato → rigenerazione esplicita con nuova istanza, mai modifica a vista.
(b) Anteprima = il PDF generato e archiviato come artefatto alla creazione dell'istanza, mai ri-convertito a vista. Problema font: installare font Liberation metricamente compatibili sul Mac; al salvataggio del template il dry-run segnala font mancanti e segnaposti irrisolti con messaggi in italiano semplice. Fedeltà verificata subito sui modelli reali depositati.
(c) Import .doc/.odt consentito, convertito una tantum in .docx, ma il file convertito nasce come bozza da approvare, mai come versione depositata. Ogni versione depositata: hash SHA-256, stato (bozza/depositata/ritirata), blocco modifica, approvazione con ruoli. Cambio modello → nuova versione e nuovo deposito; le pratiche in corso restano legate alla versione con cui sono nate. PDF come template: NO definitivo.
(d) Privacy: si tiene genera→stampa→firma→scansiona (è la pratica reale e costa poco), ma la scansione è un record immutabile di consenso — soggetto, data, versione del modulo, hash, timestamp — conservato a norma. Al cambio dell'informativa, i consensi pregressi sono marcati scaduti e il sistema impone la ri-firma. Dati mancanti: generazione bloccata con elenco dei campi vuoti, nessun documento con buchi. Firma OTP via link in fase 2, previa verifica eIDAS.

## La prima cosa da fare
Prima di scrivere codice, test di validazione sui 5-10 modelli reali depositati in Camera di Commercio: conversione PDF, controllo font, dry-run segnaposti con dati finti, confronto stampa/anteprima. Se passano, il design è validato; se falliscono, si correggono i template, non il motore.
