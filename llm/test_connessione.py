"""Test di connessione al provider LLM (criterio di done di S0).

Uso, dalla cartella del progetto sul Mac:
    ./.venv/bin/python llm/test_connessione.py
"""
from provider import carica_config, chiedi

if __name__ == "__main__":
    cfg = carica_config()
    print(f"Provider: {cfg['base_url']}")
    print(f"Modello:  {cfg['model']}")
    print("Invio una domanda di prova (nessun dato reale)...")
    risposta = chiedi("Rispondi in una sola frase, in italiano: chi sei?")
    print("\nRISPOSTA DEL MODELLO:")
    print(risposta)
    print("\nConnessione OK: il provider risponde.")
