#!/bin/bash
set -e

# ============================================
# RESTAURATION : DB + MEDIA depuis un backup
# Restauration par TIMESTAMP pour garantir que la DB et les media
# proviennent bien du même backup (évite un mix incohérent).
# ============================================

# --- Config ---
DB_NAME="SonikaraElectroDB"
DB_USER="sonikaraelectro"
DB_PASS="oklm"

MEDIA_DIR="/home/ubuntu/sonikaraelectroniquestock/media"      # adapte le chemin selon le projet

BACKUP_DIR="/opt/backups/ss"       # dossier local unique (db + media dedans)
S3_BUCKET="s3://sonikara-db-backups"
AWS_PROFILE="sonikara-backup"

# --- Usage ---
if [ -z "$1" ]; then
  echo "Usage: $0 <timestamp> [--from-s3]"
  echo "Exemple: $0 2026-08-03_01-00-01 --from-s3"
  echo ""
  echo "Backups locaux disponibles (timestamps) :"
  ls "$BACKUP_DIR" 2>/dev/null | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{2}-[0-9]{2}-[0-9]{2}' | sort -u || echo "  (aucun backup local)"
  exit 1
fi

TIMESTAMP="$1"
DB_FILENAME="${DB_NAME}_${TIMESTAMP}.sql.gz"
MEDIA_FILENAME="media_${TIMESTAMP}.tar.gz"

DB_LOCAL_PATH="${BACKUP_DIR}/${DB_FILENAME}"
MEDIA_LOCAL_PATH="${BACKUP_DIR}/${MEDIA_FILENAME}"

# --- Télécharger depuis S3 si demandé ---
if [ "$2" == "--from-s3" ]; then
  echo "Téléchargement depuis S3..."
  mkdir -p "$BACKUP_DIR"
  aws s3 cp "${S3_BUCKET}/db/${DB_FILENAME}" "$DB_LOCAL_PATH" --profile "$AWS_PROFILE"

  if aws s3api head-object --bucket "$(echo "$S3_BUCKET" | sed 's|s3://||')" --key "media/${MEDIA_FILENAME}" --profile "$AWS_PROFILE" &>/dev/null; then
    aws s3 cp "${S3_BUCKET}/media/${MEDIA_FILENAME}" "$MEDIA_LOCAL_PATH" --profile "$AWS_PROFILE"
  else
    echo "  -> Pas d'archive media trouvée sur S3 pour ce timestamp (backup peut-être antérieur à l'ajout des media)."
    MEDIA_LOCAL_PATH=""
  fi
fi

if [ ! -f "$DB_LOCAL_PATH" ]; then
  echo "Erreur : fichier DB introuvable ($DB_LOCAL_PATH)"
  exit 1
fi

MEDIA_AVAILABLE=false
if [ -f "$MEDIA_LOCAL_PATH" ]; then
  MEDIA_AVAILABLE=true
fi

# --- Confirmation obligatoire ---
echo "⚠️  ATTENTION : tu es sur le point d'ÉCRASER :"
echo "    - la base '${DB_NAME}' avec : $DB_LOCAL_PATH"
if [ "$MEDIA_AVAILABLE" = true ]; then
  echo "    - le dossier media '${MEDIA_DIR}' avec : $MEDIA_LOCAL_PATH"
else
  echo "    - (aucune restauration media : archive non trouvée pour ce timestamp)"
fi
read -p "Tape 'RESTORE' en majuscules pour confirmer : " CONFIRM
if [ "$CONFIRM" != "RESTORE" ]; then
  echo "Annulé."
  exit 1
fi

SAFETY_TIMESTAMP=$(date +%F_%H-%M-%S)

# --- Backup de sécurité de la DB avant restauration ---
SAFETY_DB_FILE="${BACKUP_DIR}/pre_restore_db_${SAFETY_TIMESTAMP}.sql.gz"
echo "Backup de sécurité de la DB actuelle -> $SAFETY_DB_FILE"
mysqldump --single-transaction --quick --lock-tables=false --no-tablespaces \
  -u"$DB_USER" -p"$DB_PASS" "$DB_NAME" | gzip > "$SAFETY_DB_FILE"

# --- Backup de sécurité du media actuel avant restauration ---
if [ -d "$MEDIA_DIR" ]; then
  SAFETY_MEDIA_FILE="${BACKUP_DIR}/pre_restore_media_${SAFETY_TIMESTAMP}.tar.gz"
  echo "Backup de sécurité du media actuel -> $SAFETY_MEDIA_FILE"
  tar -czf "$SAFETY_MEDIA_FILE" -C "$(dirname "$MEDIA_DIR")" "$(basename "$MEDIA_DIR")"
fi

# --- Restauration DB ---
echo "Restauration de la base de données..."
gunzip < "$DB_LOCAL_PATH" | mysql -u "$DB_USER" -p"$DB_PASS" "$DB_NAME"
echo "  -> DB restaurée."

# --- Restauration media ---
if [ "$MEDIA_AVAILABLE" = true ]; then
  echo "Restauration des fichiers media..."
  rm -rf "$MEDIA_DIR"
  mkdir -p "$(dirname "$MEDIA_DIR")"
  tar -xzf "$MEDIA_LOCAL_PATH" -C "$(dirname "$MEDIA_DIR")"
  echo "  -> Media restaurés."
fi

echo "✅ Restauration terminée."
echo "   Sauvegardes de sécurité créées avant restauration :"
echo "   - $SAFETY_DB_FILE"
[ -d "$MEDIA_DIR" ] && echo "   - $SAFETY_MEDIA_FILE"