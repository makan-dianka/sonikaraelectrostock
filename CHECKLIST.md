# Checklist de migration EC2 → VPS OVH (par client)

## Avant la migration
- [ ] Client prévenu de la fenêtre de maintenance (date/heure)
- [ ] VPS OVH prêt : MySQL, Nginx, uWSGI Emperor mode installés et fonctionnels
- [ ] User + base MySQL créés côté VPS pour ce client
- [ ] Code de l'app cloné/copié sur le VPS (`git clone` ou rsync du repo)
- [ ] venv recréé sur le VPS (`python -m venv venv && pip install -r requirements.txt`)
- [ ] `.env` de prod préparé pour le VPS (attention aux chemins absolus différents EC2 vs OVH)
- [ ] TTL DNS Cloudflare abaissé quelques heures avant (ex: 300s) pour accélérer la propagation
- [ ] Accès SSH testé entre les deux serveurs (clé SSH en place)

## Pendant la migration
- [ ] `1_export_ec2.sh` exécuté côté EC2
- [ ] Mode maintenance actif et vérifié visuellement sur le site
- [ ] `2_import_vps.sh` exécuté côté VPS
- [ ] Vhost Nginx + config uWSGI créés pour ce client sur le VPS
- [ ] Test complet via IP directe ou `/etc/hosts` local :
  - [ ] Connexion utilisateur fonctionne
  - [ ] Consultation des données (stock, ventes, factures) correcte
  - [ ] Génération PDF (devis/facture) fonctionne (WeasyPrint + fonts installées sur le VPS ?)
  - [ ] Upload de fichier fonctionne (permissions media/)
  - [ ] Emails sortants fonctionnent (SPF record vérifié)

## Bascule DNS
- [ ] Enregistrement DNS modifié chez Cloudflare (pointer vers IP du VPS)
- [ ] SSL/HTTPS actif sur le nouveau serveur (vérifier avant la bascule, pas après)
- [ ] Attendre la propagation, tester depuis un réseau externe (4G, pas le wifi du bureau qui peut avoir du cache DNS)

## Après la migration
- [ ] Site accessible normalement via le nom de domaine
- [ ] Mode maintenance désactivé
- [ ] Backup automatisé configuré sur le nouveau VPS (mysqldump vers S3, comme sur Sonikara)
- [ ] EC2 gardé actif encore 3-7 jours en secours, SANS trafic actif dessus
- [ ] Une fois confiant (après quelques jours sans souci) : arrêt/suppression de l'instance EC2

## Points de vigilance spécifiques (déjà rencontrés par le passé)
- [ ] Timezone MySQL (`mysql_tzinfo_to_sql`) si nécessaire sur le nouveau serveur
- [ ] `ALLOWED_HOSTS` correctement configuré (pas de logique inversée)
- [ ] Headers Cloudflare (`$http_cf_connecting_ip`) bien repris dans la config Nginx du VPS
- [ ] Socket uWSGI créé au bon endroit (`/run/uwsgi/`)
9