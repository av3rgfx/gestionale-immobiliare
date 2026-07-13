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