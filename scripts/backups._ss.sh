#!/bin/bash
set -e

# ============================================
# BACKUP QUOTIDIEN : DB + MEDIA -> S3
# ============================================

# --- Config ---
DB_NAME="SonikaraElectroDB"
DB_USER="sonikaraelectro"
DB_PASS="oklm"

MEDIA_DIR="/home/ubuntu/sonikaraelectroniquestock/media"       # adapte le chemin selon le projet

BACKUP_DIR="/opt/backups/ss"                                   # dossier local unique (db + media dedans)
S3_BUCKET="s3://sonikara-db-backups"
AWS_PROFILE="sonikara-backup"

RETENTION_DAYS=7

DATE=$(date +%F_%H-%M-%S)
DB_FILENAME="${DB_NAME}_${DATE}.sql.gz"
MEDIA_FILENAME="media_${DATE}.tar.gz"

mkdir -p "$BACKUP_DIR"

# --- 1. Dump DB + compression ---
echo "[1/4] Dump de la base de données..."
mysqldump --single-transaction --quick --lock-tables=false --no-tablespaces \
  -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" | gzip > "${BACKUP_DIR}/${DB_FILENAME}"
echo "  -> ${DB_FILENAME} ($(du -h "${BACKUP_DIR}/${DB_FILENAME}" | cut -f1))"

# --- 2. Archive des médias ---
echo "[2/4] Archive des fichiers médias..."
if [ -d "$MEDIA_DIR" ]; then
    tar -czf "${BACKUP_DIR}/${MEDIA_FILENAME}" -C "$(dirname "$MEDIA_DIR")" "$(basename "$MEDIA_DIR")"
    echo "  -> ${MEDIA_FILENAME} ($(du -h "${BACKUP_DIR}/${MEDIA_FILENAME}" | cut -f1))"
else
    echo "  -> ATTENTION : dossier media introuvable ($MEDIA_DIR), étape sautée."
    MEDIA_FILENAME=""
fi

# --- 3. Upload S3 ---
echo "[3/4] Upload vers S3..."
aws s3 cp "${BACKUP_DIR}/${DB_FILENAME}" "${S3_BUCKET}/db/${DB_FILENAME}" --profile "$AWS_PROFILE"

if [ -n "$MEDIA_FILENAME" ]; then
    aws s3 cp "${BACKUP_DIR}/${MEDIA_FILENAME}" "${S3_BUCKET}/media/${MEDIA_FILENAME}" --profile "$AWS_PROFILE"
fi

# --- 4. Nettoyage local (garde les X derniers jours) ---
echo "[4/4] Nettoyage local (rétention ${RETENTION_DAYS}j)..."
find "$BACKUP_DIR" -name "*.sql.gz" -mtime +${RETENTION_DAYS} -delete
find "$BACKUP_DIR" -name "media_*.tar.gz" -mtime +${RETENTION_DAYS} -delete

# --- Nettoyage S3 (optionnel, une lifecycle rule côté S3 est recommandée plutôt que ceci) ---

echo "Backup terminé : ${DB_FILENAME}${MEDIA_FILENAME:+ + $MEDIA_FILENAME}"