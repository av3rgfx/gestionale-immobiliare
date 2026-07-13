#!/usr/bin/env bash
# Bozza dello script di backup — Sprint 0 (ADR-06).
#
# Fa uno snapshot CONSISTENTE del database con "sqlite3 .backup"
# (MAI copiare i file del database a caldo: i file -wal/-shm sarebbero
# incoerenti e il backup corrotto) e verifica l'integrita' della copia.
#
# In S0 la copia offsite e' MANUALE; la schedulazione (launchd), la copia
# offsite cifrata automatica e gli alert arrivano in S3.
#
# Uso:
#   bash scripts/backup_db.sh                                # valori di default
#   bash scripts/backup_db.sh /percorso/db.sqlite /cartella/di/destinazione
set -euo pipefail

DB="${1:-$HOME/Gestionale/db.sqlite}"
DEST_DIR="${2:-$HOME/Gestionale/backup}"

command -v sqlite3 >/dev/null || { echo "ERRORE: il programma sqlite3 non e' installato su questo computer."; exit 1; }
[ -f "$DB" ] || { echo "ERRORE: database non trovato: $DB"; echo "Cosa fare: controlla il percorso, oppure il database nascera' in S1."; exit 1; }

mkdir -p "$DEST_DIR"
DATA="$(date +%Y%m%d_%H%M%S)"
COPIA="$DEST_DIR/db_${DATA}.sqlite"

sqlite3 "$DB" ".backup '$COPIA'"

ESITO="$(sqlite3 "$COPIA" 'PRAGMA integrity_check;')"
if [ "$ESITO" = "ok" ]; then
    echo "Backup riuscito e verificato: $COPIA"
    echo "RICORDA (S0): copia questo file a mano su una destinazione offsite cifrata, fuori dall'ufficio."
    echo "Un backup mai ripristinato non e' un backup: prova il ripristino ogni mese."
else
    echo "ATTENZIONE: backup creato ma il controllo di integrita' e' FALLITO: $ESITO"
    echo "Non fidarti di questa copia. Riprova e, se fallisce ancora, fermati e chiedi aiuto."
    exit 1
fi
