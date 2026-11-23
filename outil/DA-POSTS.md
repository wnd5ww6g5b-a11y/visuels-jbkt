# DA des posts (validée par Karim le 23/11/2026 : « top, garde cette DA, continue à poster »)

Cette DA remplace les anciens rendus (rendre.py, texte.py, demo.py, carrousel.py, gloova_pop.py) pour **tous les nouveaux posts image** Instagram et Facebook des 3 marques. Les reels déjà prévus restent comme ils sont.

Les 3 scripts tournent depuis la racine du dépôt (polices, logos et écrans Gloova sont dans `outil/assets/`) :

```
python3 outil/gloova_post.py <post.json> <sortie.jpg>   # Gloova, sans photo
python3 outil/photo_post.py  <post.json> <sortie.jpg>   # photo + texte, 3 marques
python3 outil/mockup_post.py <post.json> <sortie.jpg>   # écrans dans des appareils, JBKT et Radar
```

Exemples JSON qui marchent, à copier : `outil/exemples-da/`. Tous les formats font 1080 × 1350.
Planches de référence : `images/nouveaux-1911-planche.jpg`, `images/gloova-epoque/`, `images/gloova-pro/`, `images/gloova-facebook/`, `images/mockups/`.

## Gloova (charte d'origine : crème #F6F2EE, rose poudré #F3E2E0, noir #1D1F20, Plus Jakarta Sans)

- `gloova_post.py`, layouts :
  - `liste` : grand titre + 3 ou 4 cartes blanches (`numeros: true` pour 1-2-3, `lettres: true` pour un sondage A-B-C, sinon coches) ; `fond` creme, rose ou noir.
  - `chiffre` : un très grand chiffre (« 24 h/24 », « 1 mois », « 9,99 € »), une phrase, un bouton.
  - `ecran` : vrai écran de l'app dans un iPhone (iphone-agenda, accueil, reservation, finances ; **pas** iphone-cliente : la fiche beauté n'est pas encore à mettre en avant) + 3 coches.
  - `prix` : les 3 formules réelles. `import` : illustration de l'import du fichier clientes.
- `photo_post.py` avec `brand: gloova`, `ton: clair`, `ia: true`, une photo de `banque/photos-ia/` (cils, comptoir, gloova-soir, gloova-cadeau, gloova-acompte) ou une nouvelle photo Higgsfield.
- Alterner : 1 liste ou sondage, 1 photo, 1 chiffre ou écran. Bouton : « Essai gratuit sur gloova.fr ».
- Fonctions citées : uniquement celles du brief (page et QR code de réservation, réservation 24 h/24, agenda, fichier clientes, rappels **par e-mail**, acompte en ligne, bons cadeaux (dès Pro+), liste d'attente, parrainage (dès Pro+), statistiques, équipe (Ultra), import des clientes). Jamais SMS, jamais caisse.
- « sans commission sur vos rendez-vous », prix TTC 9,99 / 13,99 / 15,99 €, premier mois offert avec le code INSTITUT1 (= l'essai d'un mois). Indépendantes : on pousse l'abonnement ; l'annuaire gratuit est pour les pros qui ont déjà un logiciel.

## JBKT (fond #F3F7FF ou #0B1533, Manrope 800)

- `mockup_post.py` avec des écrans de `banque/jbkt/` (sites, apps, crm, outils-metier, tableaux-de-bord) : laptop + téléphone, mention « Démo · données fictives », bouton « Démo gratuite de 30 min ».
- `photo_post.py` avec `brand: jbkt`, `ia: true`, une photo de `banque/photos-ia/` (atelier, boulangerie, bureau) : présenté comme « Exemple d'outil que nous construisons ».
- Alterner mockup et photo. Jamais de prix.

## Radar VTC (fond #111418 ou #EEF0F3, Manrope 800)

- `mockup_post.py` avec une **vraie capture** de l'app Radar (`devices[].src`, voir outil/marques/radar.md) ; les écrans redessinés en HTML ne sont plus utilisés (décision de Karim du 23/11).
- `photo_post.py` avec `brand: radar`, `ton: sombre`, `ia: true`, une photo de `banque/photos-ia/` (pluie, route, volant, cafe, support).
- Calculs toujours justes et écrits dans la légende : €/km = prix ÷ (km course + km approche) ; €/h = prix ÷ (min course + min approche) × 60. Aucune promesse de gain. Noms de plateformes et lieux : seulement tels qu'ils apparaissent sur les vraies captures de Radar, avec la mention d'indépendance (outil/marques/radar.md). Jamais une capture d'une appli de plateforme, jamais de logo.

## Photos Higgsfield

- Si l'outil Higgsfield est disponible : `generate_image_batch`, modèle `gpt_image_2_6`, format `4:5` (0,25 crédit l'image), **sans personne ni mains**, sans logo, sans texte, sans lieu reconnaissable, « large calm empty area in the top half ». Enregistrer la photo dans `banque/photos-ia/` (JPEG) pour la réutiliser.
- Sinon : réutiliser une photo de `banque/photos-ia/`, en évitant celle utilisée la semaine précédente pour la même marque.
- Chaque post photo porte « Image générée par IA » (`ia: true`).

## Facebook

Même DA, mais posts pensés pour Facebook (outil/RESEAUX.md) : image unique, texte plus long, question ou conseil à garder, vrai lien écrit en entier, pas de hashtags, jamais « lien en bio ».

## Contrôle avant de programmer

Regarder chaque image (titre lisible, rien de coupé, pas de mot seul sur une ligne : utiliser `&nbsp;`), vérifier l'adresse raw (200), puis créer le document `contents` comme d'habitude.
