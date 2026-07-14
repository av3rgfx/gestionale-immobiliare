# Gestionale Immobiliare + JARVIS

Webapp **locale** per una piccola agenzia immobiliare italiana, con l'agente AI locale **JARVIS**.
Stack: FastAPI + SQLite (modalità WAL) + docxtpl + LibreOffice headless + PDF.js (ADR‑01).
Produzione sul Mac Mini M4; sviluppo su MacBook. Lo sprint in corso è in `Plan.md`.

> **Regole di progetto:** `REGOLE.md` (fonte normativa) e `CLAUDE.md` (caricato in automatico da Code).
> **Decisioni vincolanti:** `03_DECISIONI_CONSIGLIO.md` (ADR). **Architettura:** `04_ARCHITETTURA.md`.

## Dove vivono i dati: `~/Gestionale/`

**Tutti i dati del gestionale stanno in un'unica cartella nella tua Home: `~/Gestionale/`** — non
dentro il repository. Questa cartella è il perimetro del backup e della cifratura (04 §2, ADR‑06).

```
~/Gestionale/
├── db.sqlite      # il database (nasce in S1, con la prima migrazione dello schema)
├── templates/     # modelli DOCX depositati + metadati
├── documenti/     # PDF generati, scansioni consensi, allegati
├── backup/        # copie di sicurezza fatte con «sqlite3 .backup»
└── logs/          # audit log e log applicativi
```

La crei **una volta sola** con:

```
bash setup/crea_cartella_dati.sh
```

⚠️ **Mai** copiare questa cartella «a caldo» mentre il database è aperto: i file `-wal`/`-shm`
sarebbero incoerenti e il backup corrotto. Per copiare il database si usa **sempre** `sqlite3 .backup`
(vedi sotto).

## Configurazione (i segreti restano fuori dal repository)

Gli indirizzi del provider AI e la tua chiave stanno in `config.toml`, che **non finisce mai su Git**
(è in `.gitignore`). Lo crei copiando l'esempio e compilando i tre valori:

```
cp config.example.toml config.toml
```

In sviluppo, verso le API cloud passano **solo dati sintetici o anonimizzati**, mai dati reali dei
clienti (ADR‑05).

## Primo avvio sul Mac (Sprint 0)

Script guidato: `setup/installa_mac.sh` (Homebrew, Python, LibreOffice, font Liberation, virtualenv +
dipendenze). I passi completi sono nel prompt `06_PROMPT_SPRINT/S0_fondamenta.md`.

## Backup e ripristino di prova

**Fare un backup** (copia consistente e verificata in `~/Gestionale/backup/`):

```
bash scripts/backup_db.sh
```

In S0 la copia **offsite** (su disco esterno o cloud cifrato) è **manuale**; la schedulazione
automatica arriva in S3.

**Ripristino di prova** — *un backup mai ripristinato non è un backup* (ADR‑06). Almeno una volta
(e ogni mese in produzione) verifica che una copia si riapra davvero:

```
# 1) copia l'ultimo backup come database di PROVA (non tocca l'originale)
cp ~/Gestionale/backup/db_AAAAMMGG_HHMMSS.sqlite /tmp/prova_ripristino.sqlite

# 2) controlla che sia integro e che si apra (deve stampare: ok)
sqlite3 /tmp/prova_ripristino.sqlite 'PRAGMA integrity_check;'
sqlite3 /tmp/prova_ripristino.sqlite '.tables'

# 3) se è «ok», il backup è valido: cancella la copia di prova
rm /tmp/prova_ripristino.sqlite
```
