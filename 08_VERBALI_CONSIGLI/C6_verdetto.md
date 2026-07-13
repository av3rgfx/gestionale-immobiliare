# Verdetto del Chairman — Consiglio C6 (Ruolo Proprietario, contabilità e compliance)

## Dove il consiglio concorda

1. **Niente contabilità fiscale nel gestionale.** First Principles Thinker, Executor, Outsider e Contrarian convergono: prima nota, IVA, fatture elettroniche e cespiti restano al commercialista. Il gestionale è il sistema di record *operativo*, il software fiscale quello *tributario*; la cerniera è un export CSV categorizzato, non una replica.
2. **I movimenti nascono dagli eventi, non dalle dita.** Provvigioni e canoni devono generarsi automaticamente alla firma del contratto: qualunque inserimento manuale uccide il dato entro tre mesi (Executor, Outsider, Contrarian).
3. **La dashboard Proprietario è una vista in lettura**: incassi per mese/anno/tipologia/agente, con margine per agente visibile solo al Proprietario. Ruolo distinto dall'Admin, ma — nota l'Outsider — va giustificato per ciò che protegge (i margini), non per titolo.
4. **Il cliente è fonte affidabile di bisogni, inaffidabile di riferimenti legali** (Outsider): il gestionale usa le diciture corrette senza esporre il dibattito giuridico.

## Dove il consiglio è diviso

**Perimetro del registro.** Contrarian: solo incassi attesi per pratica (previsto/fatturato/incassato). First Principles Thinker: entrate dentro, spese fuori. Executor: tabella unica con totali. **Expansionist dissente da tutti**: tracciare tutto come materia prima di un modulo property management e vendere la correttezza normativa come "Radar Compliance". Le peer review 2 e 5 dimostrano che vantare correttezza normativa rafforza l'affidamento del cliente e la responsabilità legale del fornitore: il marketing dell'Expansionist è bocciato, ma il suo intuito sul commercialista-canale (export pulito = venditore) viene incorporato nel design dell'export.

## Punti ciechi emersi

Nessun advisor ha coperto: (i) conservazione documentale AML **decennale** e aggiornamento periodico dell'adeguata verifica; (ii) alert **bloccante** sul contante a 5.000€; (iii) rito di **riconciliazione periodica** registro↔banca/commercialista (chi, quando, come); (iv) **audit trail** probatorio (chi vide quale etichetta, quando, quale versione della norma) e allocazione contrattuale nei ToS; (v) chi mantiene i parametri normativi nel tempo; (vi) rischio GDPR/controllo a distanza sui margini per agente; (vii) registro divergente dai libri leggibile dall'AdE come scritture extracontabili; (viii) deposito formulari CCIAA **da rinnovare a ogni modifica** dei modelli.

## La raccomandazione

Adotto l'architettura del **First Principles Thinker** con la meccanica dell'**Executor** e i presidi giuridici del **Contrarian**.

**(a) Ruolo Proprietario:** sì, distinto dall'Admin, con permesso granulare sui margini. Dashboard = solo incassi (previsto/fatturato/incassato) per periodo, tipologia e agente. Le spese restano fuori: in fase 2, import in sola lettura dal commercialista.

**(b) Registro movimentazioni — dentro:** righe auto-generate alla firma (provvigione, canone di gestione) con stato, acconti, storni e note di credito gestiti come stati della stessa riga; scadenziario RLI a T+0 dalla registrazione del contratto *nel sistema*, non dalla stipula. **Fuori:** prima nota, IVA, fatture elettroniche, cespiti, spese.

**Correzioni normative (ferme, come dati, non come scontro):** il gestionale riporta «Deposito formulari presso la Camera di Commercio» (non AdE), con promemoria a ogni modifica dei modelli; «Adeguata verifica al conferimento dell'incarico» (nessuna soglia); 5.000€ come alert bloccante sui pagamenti in contante; 1.000€ come policy interna configurabile, etichettata «policy interna», mai «obbligo di legge». Tutte le regole sono parametri versionati mantenuti dal fornitore, con disclaimer strutturale «adempimento non verificabile dal software», audit trail e clausola ToS. Conservazione documentale 10 anni nativa; riconciliazione mensile come task guidato.

**(d) Confine:** gestionale = record operativo; commercialista = record tributario; cerniera = export CSV/prima nota leggibile, allineato alle categorie del commercialista.

## La prima cosa da fare

Modellare la **tabella movimenti unica** — pratica, tipo, importo, stato, data, agente — con generazione automatica alla firma del contratto. Da quella tabella discendono dashboard, scadenziario, export e riconciliazione: senza di essa, tutto il resto è decorazione.
