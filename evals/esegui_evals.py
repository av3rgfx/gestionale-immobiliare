"""Eval suite del progetto — skeleton di Sprint 0 (ADR-05, ADR-48).

Esegue i casi di test in italiano contenuti in evals/casi/ contro il modello
configurato in config.toml e produce un report leggibile con l'esito per caso.

Uso, dalla cartella del progetto:
    ./.venv/bin/python evals/esegui_evals.py           # con il modello vero
    python3 evals/esegui_evals.py --prova              # modalita' prova, senza modello

La modalita' --prova collauda solo il meccanismo (lettura dei casi, verifica
delle parole attese, scrittura del report): simula le risposte e NON misura
nessun modello. Il report lo dichiara in testa.

Criterio di esito per caso: la risposta contiene almeno la meta' (arrotondata
per eccesso) delle parole attese, senza distinguere maiuscole/minuscole.
"""
import json
import math
import sys
from datetime import datetime
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
CARTELLA_CASI = RADICE / "evals" / "casi"
CARTELLA_REPORT = RADICE / "evals"


def carica_casi():
    casi = []
    for percorso in sorted(CARTELLA_CASI.glob("*.json")):
        with open(percorso, encoding="utf-8") as f:
            casi.append(json.load(f))
    if not casi:
        raise SystemExit(f"Nessun caso di test trovato in {CARTELLA_CASI}")
    return casi


def verifica(risposta, parole_attese):
    trovate = [p for p in parole_attese if p.lower() in risposta.lower()]
    soglia = math.ceil(len(parole_attese) / 2)
    return len(trovate) >= soglia, trovate


def main():
    prova = "--prova" in sys.argv
    casi = carica_casi()

    if prova:
        descrizione_modello = "MODALITA' PROVA (risposte simulate, nessun modello interrogato)"

        def rispondi(caso):
            return "Risposta simulata per collaudo: " + " ".join(caso["parole_attese"])
    else:
        sys.path.insert(0, str(RADICE))
        from llm.provider import carica_config, chiedi

        cfg = carica_config()
        descrizione_modello = f"{cfg['model']} via {cfg['base_url']}"

        def rispondi(caso):
            return chiedi(caso["domanda"])

    righe = []
    superati = 0
    for caso in casi:
        try:
            risposta = rispondi(caso)
        except Exception as errore:  # un caso fallito non ferma la suite
            righe.append((caso["id"], "ERRORE", [], str(errore)))
            continue
        ok, trovate = verifica(risposta, caso["parole_attese"])
        if ok:
            superati += 1
        righe.append((caso["id"], "SUPERATO" if ok else "NON SUPERATO", trovate, risposta))

    adesso = datetime.now()
    percorso_report = CARTELLA_REPORT / f"report_{adesso.strftime('%Y%m%d_%H%M')}.md"
    with open(percorso_report, "w", encoding="utf-8") as f:
        f.write("# Report eval suite\n\n")
        f.write(f"- **Data:** {adesso.strftime('%d/%m/%Y %H:%M')}\n")
        f.write(f"- **Modello:** {descrizione_modello}\n")
        f.write(f"- **Esito complessivo:** {superati}/{len(casi)} casi superati\n\n")
        for id_caso, esito, trovate, risposta in righe:
            f.write(f"## Caso: {id_caso} — {esito}\n\n")
            f.write(f"- Parole attese trovate: {', '.join(trovate) if trovate else 'nessuna'}\n")
            testo = risposta.replace("\n", " ").strip()
            if len(testo) > 300:
                testo = testo[:300] + " [...]"
            f.write(f"- Risposta: {testo}\n\n")

    print(f"Eval suite completata: {superati}/{len(casi)} casi superati.")
    print(f"Report salvato in: {percorso_report}")
    if prova:
        print("ATTENZIONE: modalita' prova — il risultato non misura nessun modello.")


if __name__ == "__main__":
    main()
