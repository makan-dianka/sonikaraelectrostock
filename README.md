# Sonikara electro stock

Application web de gestion commerciale permettant de gérer plusieurs magasins, les produits, les ventes, les achats, les dépenses, les clients, les fournisseurs, les bons des commandes, les bons de livraison, les factures et les rapports d'activité.

## Technologie utilisé
- Django
- python


# Architecture



                             ┌─────────────────────────┐
                             │      Dashboard          │
                             │ KPI - Graphiques - CA  │
                             └────────────┬────────────┘
                                          │
 ─────────────────────────────────────────┼────────────────────────────────────────
                                          │
 ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────────┐
 │ MultiStore   │  │ Utilisateurs │  │ Paramètres   │  │ Notifications  │
 └──────┬───────┘  └──────┬───────┘  └────────────────┘  └────────────────┘
        │                 │
        └─────────────────┼───────────────────────────────────────────────────┐
                          │                                                   │
                          ▼                                                   ▼

                  ┌─────────────────────────────────────────────────────────────┐
                  │                    PRODUITS                                │
                  │ Catégories - Marques - Produits - Stock - Inventaire       │
                  └──────────────┬──────────────────────────────────────────────┘
                                 │
                 ┌───────────────┴────────────────┐
                 │                                │
                 ▼                                ▼

        ┌─────────────────┐              ┌──────────────────┐
        │     ACHATS      │              │      VENTES      │
        └────────┬────────┘              └─────────┬────────┘
                 │                                 │
                 ▼                                 ▼

        Ligne Achat                      Ligne Vente

                 │                                 │
                 └───────────────┬─────────────────┘
                                 │
                                 ▼

                         Mise à jour Stock

───────────────────────────────────────────────────────────────────────────────

                 ┌───────────────────────────────────────┐
                 │              DOCUMENTS                │
                 ├───────────────────────────────────────┤
                 │ Bon de commande                       │
                 │ Bon de livraison                      │
                 │ Facture PDF                           │
                 └───────────────────────────────────────┘

───────────────────────────────────────────────────────────────────────────────

        ┌────────────────┐             ┌────────────────────┐
        │    CLIENTS     │             │   FOURNISSEURS     │
        └────────────────┘             └────────────────────┘

───────────────────────────────────────────────────────────────────────────────

                 ┌──────────────────────────────────────┐
                 │            PAIEMENTS                 │
                 ├──────────────────────────────────────┤
                 │ Espèces                              │
                 │ Banque                               │
                 │ Mobile Money                         │
                 │ Chèque                               │
                 └──────────────────────────────────────┘

───────────────────────────────────────────────────────────────────────────────

         ┌────────────────────┐       ┌─────────────────────┐
         │     DÉPENSES       │       │      CRÉDITS        │
         ├────────────────────┤       ├─────────────────────┤
         │ Catégories         │       │ Crédit marchandises │
         │ Dépenses           │       │ Crédit espèces      │
         │ Historique         │       │ Remboursements      │
         └────────────────────┘       └─────────────────────┘

───────────────────────────────────────────────────────────────────────────────

                         ┌─────────────────────┐
                         │      RAPPORTS       │
                         ├─────────────────────┤
                         │ Chiffre d'affaires  │
                         │ Achats              │
                         │ Dépenses            │
                         │ Stocks              │
                         │ Bénéfices           │
                         │ Crédits             │
                         └─────────────────────┘



### Structure backend

core/
│
├── accounts/        (utilisateurs)
├── stores/          (magasins)
├── customers/       (clients)
├── suppliers/       (fournisseurs)
├── products/        (produits)
├── purchases/       (achats)
├── sales/           (ventes)
├── documents/       (bon de commande, livraison, facture)
├── payments/        (paiements)
├── expenses/        (dépenses)
├── credits/         (crédits clients et espèces)
├── dashboard/       (statistiques)
├── reports/         (rapports)
├── settings_app/    (configuration)


# Logique metier

### Fournisseur

Fournisseur
      │
      ▼
    Achat
      │
      ▼
 Mise à jour du stock
      │
      ▼
 Vente
      │
      ├──────────────► Paiement
      │                     │
      │                     ▼
      │               Espèces / Banque
      │
      ▼
 Bon de commande
      ▼
 Bon de livraison
      ▼
 Facture PDF


### Client

Client
   │
   ▼
Crédit espèces
   │
   ▼
Échéance
   │
   ▼
Paiement 1
Paiement 2
Paiement 3
   │
   ▼
Crédit soldé






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
