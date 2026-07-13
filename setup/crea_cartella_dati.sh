#!/usr/bin/env bash
# Crea la cartella dati ~/Gestionale/ con la struttura di 04_ARCHITETTURA.md par. 2.
# (Il file db.sqlite nascera' in S1, con la prima migrazione dello schema.)
#
# Uso:  bash setup/crea_cartella_dati.sh
set -euo pipefail

BASE="${1:-$HOME/Gestionale}"
mkdir -p "$BASE/templates" "$BASE/documenti" "$BASE/backup" "$BASE/logs"

echo "Struttura creata in $BASE:"
ls -la "$BASE"
