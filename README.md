# Sonikara electro stock

Application web de gestion commerciale permettant de gérer plusieurs magasins, les produits, les ventes, les achats, les dépenses, les clients, les fournisseurs, les bons des commandes, les bons de livraison, les factures et les rapports d'activité.

## Technologie utilisé
- Django
- python


## Architecture
les applications du projet

    apps
        accounts/
        stores/
        products/
        customers/
        suppliers/
        sales/
        purchases/
        payments/
        expenses/
        documents/


## installation

cloner le repo et créer un `.env` à la racine du projet

`touch .env`

ajouter ces variables d'environnement

```
SECRET_KEY=
DEBUG="True"
ENV='development'
ALLOWED_HOSTS="domaine.com,www.domaine.com"
```


ouvrir un navigateur et aller à

`http://127.0.0.1:8000/`
