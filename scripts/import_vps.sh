#!/bin/bash
set -e

# ============================================
# SCRIPT DE MIGRATION - PARTIE 2 : IMPORT (côté VPS OVH)
# À exécuter sur le VPS OVH destination, après 1_export_ec2.sh
# ============================================

# ---- CONFIG À ADAPTER PAR CLIENT ----
CLIENT_NAME="sonikaraelectro"
DB_NAME="sonikaraslectroDB"
DB_USER="sonikaraelectro"
DB_PASSWORD="oklm"                                               # mot de passe MySQL pour ce user (créé au préalable)
APP_PATH="/home/ubuntu/sonikaraelectrostock"                     # chemin cible de l'app sur le VPS
MEDIA_PATH="$APP_PATH/media"
VPS_TMP_PATH="/tmp/migration_$CLIENT_NAME"
VENV_PATH="/home/ubuntu/.venv"
# --------------------------------------

echo "=== Import $CLIENT_NAME sur VPS OVH ==="

# --- Étape 0 : vérifications préalables ---
if [ ! -d "$VPS_TMP_PATH" ]; then
    echo "ERREUR : dossier $VPS_TMP_PATH introuvable. As-tu lancé 1_export_ec2.sh ?"
    exit 1
fi

SQL_FILE=$(find "$VPS_TMP_PATH" -name "*.sql" | head -n 1)
if [ -z "$SQL_FILE" ]; then
    echo "ERREUR : aucun fichier .sql trouvé dans $VPS_TMP_PATH"
    exit 1
fi

# --- Étape 1 : créer la base et le user MySQL si pas déjà fait ---
echo "[1/6] Vérification de la base MySQL..."
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS $DB_NAME CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
mysql -u root -p -e "CREATE USER IF NOT EXISTS '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASSWORD';"
mysql -u root -p -e "GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'localhost'; FLUSH PRIVILEGES;"

# --- Étape 2 : import du dump ---
echo "[2/6] Import du dump SQL ($SQL_FILE)..."
mysql -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" < "$SQL_FILE"
echo "  -> Import terminé."

# --- Étape 3 : restauration des médias ---
echo "[3/6] Restauration des fichiers médias..."
MEDIA_ARCHIVE=$(find "$VPS_TMP_PATH" -name "media.tar.gz" | head -n 1)
if [ -n "$MEDIA_ARCHIVE" ]; then
    mkdir -p "$(dirname "$MEDIA_PATH")"
    tar -xzf "$MEDIA_ARCHIVE" -C "$(dirname "$MEDIA_PATH")"
    echo "  -> Médias restaurés dans $MEDIA_PATH"
else
    echo "  -> Pas d'archive média trouvée, étape sautée."
fi

# --- Étape 4 : rappel .env ---
echo "[4/6] Vérification du .env..."
if [ -f "$VPS_TMP_PATH/.env.reference" ]; then
    echo "  -> Un .env.reference a été transféré depuis EC2 : $VPS_TMP_PATH/.env.reference"
    echo "  -> NE PAS l'écraser aveuglément : vérifie les valeurs (DB_HOST, ALLOWED_HOSTS, chemins) avant de l'utiliser sur le VPS."
fi
read -p "As-tu bien configuré le .env de production sur le VPS ? (Entrée pour continuer)"

# --- Étape 5 : migrations Django + collectstatic ---
echo "[5/6] Application des migrations Django et collecte des statics..."
cd "$APP_PATH"
source "$VENV_PATH/bin/activate"
python manage.py migrate --check || echo "  -> Attention : des migrations semblent en attente, vérifie avant de continuer."
python manage.py collectstatic --noinput

# --- Étape 6 : vérification des permissions fichiers ---
echo "[6/6] Vérification des permissions..."
chown -R ubuntu:www-data "$MEDIA_PATH" 2>/dev/null || echo "  -> Ajuste manuellement les permissions si besoin (user uWSGI)."

echo ""
echo "=== Import terminé ==="
echo "Prochaines étapes manuelles :"
echo "  1. Configure le vhost Nginx + uWSGI pour ce client sur le VPS (si pas déjà fait)"
echo "  2. Teste l'app via /etc/hosts local ou IP directe AVANT de toucher au DNS"
echo "  3. Une fois validé : bascule le DNS chez Cloudflare"
echo "  4. Garde EC2 actif quelques jours en rollback de secours"
echo "  5. Désactive le mode maintenance côté EC2 seulement en cas de rollback"
