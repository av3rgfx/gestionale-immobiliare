# 07 — Handoff tra sessioni e regole GitHub

*"Handoff" = passaggio di consegne. Ogni sessione con Claude è una giornata di lavoro; questo file spiega come chiudere la giornata lasciando tutto in ordine, così la giornata successiva riparte senza perdere nulla. Questo progetto è già stato perso una volta per mancanza di salvataggi: le regole qui sotto esistono per non ripetere quell'errore.*

---

## A. Il "Riassunto di chiusura sessione"

### Come lo ottieni

A fine di ogni sessione di lavoro in Code, **prima di chiudere la sessione**, incolla questo messaggio:

═══════════════ RICHIESTA RIASSUNTO — COPIA DA QUI ═══════════════

> La sessione è finita. Produci il RIASSUNTO DI CHIUSURA SESSIONE compilando il template qui sotto, punto per punto, in italiano semplice. Deve essere comprensibile da chi aprirà la prossima sessione senza sapere nulla di questa. Scrivi il PROSSIMO PASSO in modo operativo: la prima azione concreta da fare, non un'idea vaga.
>
> TEMPLATE DA COMPILARE:
> 1. Data e numero sessione:
> 2. Stato attuale del progetto (una riga):
> 3. Cosa è stato fatto in questa sessione (elenco, con i nomi dei file creati o modificati):
> 4. Decisioni prese e perché (elenco breve):
> 5. Criterio di accettazione della task: rispettato / parzialmente rispettato / non rispettato (e perché):
> 6. Problemi aperti (cosa non funziona, dubbi, cose rimandate):
> 7. PROSSIMO PASSO (l'azione esatta da cui ripartire nella prossima sessione):
> 8. Comandi da eseguire per riprendere (se servono, copiabili):

════════════════ RICHIESTA RIASSUNTO — COPIA FINO A QUI ════════════════

### Dove lo salvi

Claude ti risponderà con il riassunto compilato. Tu devi salvarlo nel repository come file **`HANDOFF.md`**:

1. Se Claude ti offre un file scaricabile: scaricalo e mettilo nella cartella `gestionale-immobiliare` (quella collegata a GitHub), con il nome `HANDOFF.md`, sostituendo quello vecchio.
2. Altrimenti: apri **TextEdit** (Mac) o **Blocco note** (Windows), incolli il riassunto e salvi come `HANDOFF.md` nella stessa cartella, sostituendo quello vecchio.

> **Perché si sostituisce e non si accumula?** Perché deve esistere sempre **un solo** `HANDOFF.md`: quello dell'ultima sessione. Così la prossima sessione non può confondersi leggendo un riassunto vecchio. La storia completa resta comunque salvata su GitHub (ogni commit conserva la versione precedente).

---

## B. Convenzione commit e salvataggio su GitHub

### Formato dei messaggi di commit

Ogni salvataggio ("commit") ha un messaggio nel formato:

```
sprint-N: descrizione breve di cosa è stato fatto
```

Esempi corretti:

```
sprint-0: regole fisse del progetto e primo handoff
sprint-1: anagrafica clienti completata, test ok
sprint-1: chiusura sessione 3 — handoff aggiornato
sprint-2: template incarico in Word convertito in PDF
```

Regole del formato: tutto minuscolo tranne i nomi propri, massimo ~70 caratteri, si capisce cosa è stato fatto senza aprire nulla.

### Quanto e quando salvare

- **Minimo un commit a fine sessione**, sempre, anche se hai fatto poco. Anche se la sessione è andata male: l'handoff deve dire cosa è andato male.
- Se la sessione è lunga e hai completato un pezzo importante a metà: un commit in più non guasta.
- **Il push è obbligatorio, non opzionale.** Il commit salva sul computer; il push salva su GitHub. Solo il push è il vero backup. Un lavoro salvato solo sul computer è un lavoro a rischio: è esattamente così che il progetto è stato perso la prima volta.

### Come salvare (due modi, scegline uno)

**Modo 1 — GitHub Desktop (consigliato, senza comandi):**

1. Apri GitHub Desktop: vedrai la lista dei file modificati.
2. In basso a sinistra, nel campo del messaggio, scrivi il messaggio nel formato `sprint-N: ...`.
3. Clicca **Commit to main**.
4. Clicca **Push origin**.
5. Verifica su github.com che le modifiche ci siano (aggiorna la pagina del repository).

**Modo 2 — Terminale (se preferisci i comandi):**

═══════════════ COMANDI SALVATAGGIO — COPIA DA QUI ═══════════════

```bash
cd ~/Documenti/gestionale-immobiliare
git add -A
git commit -m "sprint-1: chiusura sessione — handoff aggiornato"
git push
```

════════════════ COMANDI SALVATAGGIO — COPIA FINO A QUI ════════════════

(Sostituisci il messaggio tra virgolette con quello giusto per la sessione. Se la cartella del repository è in un percorso diverso, adatta la prima riga.)

---

## C. Checklist di chiusura sessione (6 punti)

Da seguire in ordine, a ogni fine sessione, senza eccezioni:

1. **Riassunto**: ho incollato la richiesta del Riassunto di chiusura sessione e Claude me lo ha prodotto completo (tutti gli 8 punti).
2. **Salvataggio handoff**: ho salvato il riassunto come `HANDOFF.md` nella cartella del repository, sostituendo il vecchio.
3. **Verifica accettazione**: l'handoff dice chiaramente se il criterio di accettazione della task è rispettato, parziale o no.
4. **Commit**: ho salvato con un messaggio nel formato `sprint-N: descrizione breve`.
5. **Push + verifica**: ho fatto il push e ho controllato su github.com che le modifiche siano online.
6. **Chiusura**: chiudo la sessione. La prossima task si farà in una sessione nuova di Code, con la frase rituale di apertura.

Se un punto non è fatto, la sessione non è chiusa. Sono 5 minuti: valgono l'intero progetto.

---

## D. Ripristino dopo disastro

Scenario: il computer si è rotto, è stato resettato o sostituito. Niente panico: se i rituali di chiusura sono stati rispettati, tutto il progetto è su GitHub. Procedura:

1. **Reinstalla gli strumenti** sul computer nuovo (o ripristinato): l'app **Claude Desktop** e **GitHub Desktop**.
2. **Scarica il progetto da GitHub**:
   - Con GitHub Desktop: accedi con il tuo account → **Clone a repository** → scegli `gestionale-immobiliare` → **Clone**.
   - Con il terminale:
     ```bash
     cd ~/Documenti
     git clone https://github.com/TUO-NOME-UTENTE/gestionale-immobiliare.git
     ```
     (sostituisci `TUO-NOME-UTENTE` con il tuo nome utente GitHub)
3. **Riapri il progetto in Code**: apri l'app Claude, sezione **Code**, e seleziona come cartella di lavoro la cartella del repository appena scaricata. `CLAUDE.md` e `REGOLE.md` sono già dentro il repository scaricato: le regole tornano in carico da sole. (È il momento in cui la doppia fonte ripaga il suo scopo.)
4. **Apri una sessione nuova** e incolla la frase rituale di apertura (file `02`, sezione C).
5. Come secondo messaggio incolla:

═══════════════ RIPRESA DOPO DISASTRO — COPIA DA QUI ═══════════════

> Sto riprendendo il progetto dopo un ripristino del computer. Leggi REGOLE.md e HANDOFF.md nel repository. Riassumimi in 5 righe: (1) a che punto è il progetto, (2) cosa è stato fatto per ultimo, (3) qual è il PROSSIMO PASSO esatto. Poi fammi il piano scritto per quel passo, come richiede la sezione 1 delle regole.

════════════════ RIPRESA DOPO DISASTRO — COPIA FINO A QUI ════════════════

6. **Riprendi dal PROSSIMO PASSO** indicato nell'handoff. Il lavoro perso sarà al massimo quello dell'ultima sessione non ancora salvata su GitHub.

> **La lezione del disastro, in una riga:** il computer è usa-e-ricompra; GitHub è la memoria del progetto. Ogni push è un'assicurazione pagata.
