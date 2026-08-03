#!/bin/bash
set -e  # Stoppe le script à la moindre erreur

# ============================================
# SCRIPT DE MIGRATION - PARTIE 1 : EXPORT (côté EC2)
# À exécuter sur le serveur EC2 source, pour un client donné
# ============================================

# ---- CONFIG À ADAPTER PAR CLIENT ----
CLIENT_NAME="sonikaraelectro"                              # nom court du client (sans espace)
DB_NAME="SonikaraElectroStockDB"                           # nom de la base MySQL
DB_USER="sonikaraelectro"                                  # user MySQL avec accès à cette base
APP_PATH="/home/ubuntu/sonikaraelectrostock"               # chemin de l'app sur EC2
MEDIA_PATH="$APP_PATH/media"                               # dossier des fichiers uploadés
VPS_USER="ubuntu"                                          # user SSH sur le VPS OVH
VPS_HOST="164.132.76.165"                                  # IP du VPS OVH
VPS_TMP_PATH="/tmp/migration_$CLIENT_NAME"                 # dossier temporaire sur le VPS
# --------------------------------------

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
EXPORT_DIR="/tmp/migration_export_${CLIENT_NAME}_${TIMESTAMP}"

echo "=== Migration $CLIENT_NAME - $TIMESTAMP ==="
mkdir -p "$EXPORT_DIR"

# --- Étape 1 : activer le mode maintenance (à adapter selon ton mécanisme sentinel-file) ---
echo "[1/5] Activation du mode maintenance..."
# /opt/backups/maintenance.sh on
echo "  -> Mode maintenance activé. Vérifie que le site affiche bien la page de maintenance avant de continuer."
read -p "Appuie sur Entrée pour continuer une fois vérifié..."

# --- Étape 2 : dump de la base de données ---
echo "[2/5] Dump de la base de données..."
mysqldump -u "$DB_USER" -poklm "$DB_NAME" \
    --single-transaction \
    --quick \
    --lock-tables=false \
    --no-tablespaces \
    > "$EXPORT_DIR/${DB_NAME}.sql"
echo "  -> Dump terminé : $EXPORT_DIR/${DB_NAME}.sql ($(du -h "$EXPORT_DIR/${DB_NAME}.sql" | cut -f1))"

# --- Étape 3 : archive des fichiers médias ---
echo "[3/5] Archive des fichiers médias..."
if [ -d "$MEDIA_PATH" ]; then
    tar -czf "$EXPORT_DIR/media.tar.gz" -C "$(dirname "$MEDIA_PATH")" "$(basename "$MEDIA_PATH")"
    echo "  -> Archive créée : $EXPORT_DIR/media.tar.gz ($(du -h "$EXPORT_DIR/media.tar.gz" | cut -f1))"
else
    echo "  -> Aucun dossier media trouvé, étape sautée."
fi

# --- Étape 4 : copie du fichier .env / settings sensibles (pour référence, à ne PAS écraser côté VPS sans vérif) ---
echo "[4/5] Copie du .env pour référence..."
if [ -f "$APP_PATH/.env" ]; then
    cp "$APP_PATH/.env" "$EXPORT_DIR/.env.reference"
fi

# --- Étape 5 : transfert vers le VPS OVH ---
echo "[5/5] Transfert vers le VPS OVH..."
ssh "$VPS_USER@$VPS_HOST" "mkdir -p $VPS_TMP_PATH"
scp -r "$EXPORT_DIR"/* "$VPS_USER@$VPS_HOST:$VPS_TMP_PATH/"

echo ""
echo "=== Export terminé ==="
echo "Fichiers transférés dans : $VPS_TMP_PATH sur $VPS_HOST"
echo "Prochaine étape : lance 2_import_vps.sh sur le VPS OVH"
echo ""
echo "IMPORTANT : le mode maintenance reste ACTIF sur EC2."
echo "Ne le désactive que si tu dois annuler la migration (rollback)."
