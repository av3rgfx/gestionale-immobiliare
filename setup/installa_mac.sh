#!/usr/bin/env bash
# Setup dell'ambiente di sviluppo sul Mac — Sprint 0.
# Eseguire DAL MAC, dentro la cartella del progetto:
#   bash setup/installa_mac.sh
# Lo script controlla ogni passo, non reinstalla cio' che c'e' gia', e spiega cosa fa.
set -euo pipefail

echo "== Passo 1/5: Homebrew (il gestore dei programmi) =="
if ! command -v brew >/dev/null; then
    echo "Homebrew non trovato. Installalo seguendo le istruzioni su https://brew.sh"
    echo "poi rilancia questo script."
    exit 1
fi
echo "Homebrew ok."

echo "== Passo 2/5: Python 3.12 =="
brew list python@3.12 >/dev/null 2>&1 || brew install python@3.12
echo "Python ok: $(python3.12 --version)"

echo "== Passo 3/5: LibreOffice (conversione DOCX -> PDF, ADR-01) =="
brew list --cask libreoffice >/dev/null 2>&1 || brew install --cask libreoffice
echo "LibreOffice ok."

echo "== Passo 4/5: Font Liberation (fedelta' tipografica dei documenti, ADR-16) =="
brew list --cask font-liberation >/dev/null 2>&1 || brew install --cask font-liberation
echo "Font ok."

echo "== Passo 5/5: ambiente Python del progetto (virtualenv + dipendenze) =="
cd "$(dirname "$0")/.."
if [ ! -d .venv ]; then
    python3.12 -m venv .venv
fi
./.venv/bin/pip install --quiet --upgrade pip
./.venv/bin/pip install --quiet -r requirements.txt
echo "Dipendenze installate."

echo
echo "FATTO. Prossimi passi, in ordine:"
echo "  1) bash setup/crea_cartella_dati.sh"
echo "  2) cp config.example.toml config.toml    (poi apri config.toml e compila i 3 valori)"
echo "  3) ./.venv/bin/python llm/test_connessione.py"
echo "  4) ./.venv/bin/python evals/esegui_evals.py"
