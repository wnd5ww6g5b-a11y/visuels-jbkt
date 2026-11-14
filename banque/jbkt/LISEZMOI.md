# Banque d'écrans JBKT

Écrans d'outils (CRM, sites, applis, outils métier, tableaux de bord) déposés par Karim,
pour montrer concrètement ce que JBKT construit dans les posts, stories et reels.

## Dossiers
- `crm/` : fiches clients, suivi des devis, relances, pipeline
- `sites/` : pages de sites vitrines, pages de réservation ou de commande
- `apps/` : écrans d'applis iPhone / iPad / Android
- `outils-metier/` : bons d'intervention, suivi de production, planning, stock
- `tableaux-de-bord/` : chiffres, graphiques, vues de pilotage

## Format des fichiers
- PNG ou JPG, au moins 1080 px de large (ordinateur) ou capture iPhone entière (téléphone).
- Nom : `<type>-<sujet>-<n>.png`, par ex. `crm-fiche-client-1.png`, `outils-metier-bon-intervention-2.png`.
- Une ligne par écran dans `ecrans.json` (créée par Claude au premier dépôt) :
  `{ "fichier", "type", "sujet", "appareil": "ordinateur|telephone|tablette", "statut": "realisation|demo", "client": null }`

## Règles
- **Aucune donnée réelle** de client ni de personne : noms, téléphones, montants et adresses doivent être fictifs.
- `statut` = `realisation` seulement pour un vrai projet livré, avec l'accord du client (jamais Cyclamen sans accord écrit).
  Sinon `demo` : le contenu dit alors « exemple d'outil que nous pouvons construire », jamais « notre client X ».
- Pas de logo ni de nom de marque tierce visible (Uber, Google…), sauf l'outil du client lui-même avec son accord.

## Comment Claude s'en sert
- Posts : l'écran posé dans un cadre ordinateur ou téléphone, titre court, ce que l'outil fait.
- Stories : un écran par story, « Ce qu'on construit : … ».
- Reels : 2 à 4 écrans enchaînés dans les téléphones animés de `outil/videos/reel.py` (`<img src="B/...">`).
