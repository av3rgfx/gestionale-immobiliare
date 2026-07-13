"""Client LLM del progetto (ADR-05, ADR-48).

Un solo punto di accesso al modello, con provider configurabile:
- in sviluppo: API cloud (SOLO dati sintetici o anonimizzati — ADR-05)
- in produzione (da S6): Ollama locale, endpoint compatibile OpenAI

Cambiare provider = cambiare base_url/model/api_key in config.toml.
Nessun endpoint fissato nel codice.
"""
from pathlib import Path
import tomllib

RADICE = Path(__file__).resolve().parent.parent
PERCORSO_CONFIG = RADICE / "config.toml"


def carica_config():
    """Legge config.toml e restituisce la sezione [llm], controllando i campi."""
    if not PERCORSO_CONFIG.exists():
        raise SystemExit(
            "Manca config.toml nella cartella del progetto.\n"
            "Cosa fare: copia config.example.toml in config.toml e compila i valori."
        )
    with open(PERCORSO_CONFIG, "rb") as f:
        dati = tomllib.load(f)
    llm = dati.get("llm", {})
    for chiave in ("base_url", "model", "api_key"):
        if not llm.get(chiave):
            raise SystemExit(
                f"In config.toml manca il valore [llm] {chiave}.\n"
                "Cosa fare: apri config.toml e compila il campo vuoto."
            )
    return llm


def chiedi(domanda, istruzioni=None):
    """Fa una domanda al modello configurato e restituisce la risposta (testo)."""
    from openai import OpenAI  # importato qui: la modalita' prova delle eval non lo richiede

    cfg = carica_config()
    client = OpenAI(base_url=cfg["base_url"], api_key=cfg["api_key"])
    messaggi = []
    if istruzioni:
        messaggi.append({"role": "system", "content": istruzioni})
    messaggi.append({"role": "user", "content": domanda})
    risposta = client.chat.completions.create(model=cfg["model"], messages=messaggi)
    return risposta.choices[0].message.content
