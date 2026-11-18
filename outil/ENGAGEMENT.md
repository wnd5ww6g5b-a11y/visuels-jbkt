# Engagement Instagram : Radar VTC et JBKT (1 post + 1 reel + 2 stories par jour)

Décidé par Karim le 13/11/2026 :
- chaque marque publie **1 post et 1 reel par jour** (le reel part aussi en story) ;
- mis à jour le 14/11/2026 : en plus, **1 story du post du jour** (le visuel du post en 1080 × 1920, `outil/story.py`), soit 2 stories par jour et par marque ;
- tout est préparé **une fois par semaine, le dimanche**, pour la semaine suivante (lundi → dimanche) ;
- mis à jour le 14/11/2026 : Karim délègue le plan marketing de JBKT et Radar. Les documents sont créés **directement programmés**
  (`status` = `scheduled`, `validated_at` = maintenant, `validated_by` = `Claude (plan délégué par Karim)`).
  Karim peut toujours modifier ou refuser un contenu dans le calendrier avant l'heure prévue ;
- mis à jour le 16/11/2026 : chaque commentaire reçoit une réponse dans l'heure, automatique si elle est simple, validée par Karim si elle est délicate (voir PUBLIER.md, partie D).

Base de l'outil : artifact `215e6505-5f68-4a59-8694-595b631af2eb`, collection `contents`.

## Horaires (heure de Paris)

| Marque | Post | Reel (+ story de la même vidéo) | Story du post |
|---|---|---|---|
| radar | 07:30 | 18:30 | 21:00 |
| jbkt | 08:30 | 12:30 | 17:30 |

Si un reel est **déjà programmé** ce jour-là pour la marque (vidéo validée : `video_url` présent, `status` = `scheduled`),
on ne crée pas de nouveau reel ce jour-là : la vidéo existante est le reel du jour.

## Pourquoi ces formats

Instagram montre davantage une publication quand les gens réagissent dans la première heure (commentaires, enregistrements, partages).
Chaque publication demande donc **une action simple** : répondre OUI/NON, voter A/B, enregistrer, raconter.
On varie les formats pour ne jamais lasser, et on crée des **suites** (un post pose la question, le reel du lendemain donne la réponse).

## Semaine type

### Radar VTC (chauffeurs VTC, toute la France)

| Jour | Post 07:30 | Reel 18:30 |
|---|---|---|
| Lun | **Tu la prends ?** (`kind: offre`) : une offre d'exemple, « réponds OUI ou NON » | Astuce chauffeur (un piège qui coûte cher, sans promesse de gain) |
| Mar | **Astuce** (`kind: astuce`) : une liste à enregistrer (ex. ce qu'il faut compter dans son €/km) | **Le verdict** de l'offre de lundi : mêmes chiffres, le calcul €/km et €/h, « et toi, tu l'avais prise ? » |
| Mer | **A ou B** (`kind: sondage`) : une habitude de chauffeur | Une fonction de l'app (zones, historique, arrivées gare/aéroport, seuil rentable) |
| Jeu | **Tu la prends ?** (2e offre de la semaine) | Fonction de l'app, ou la vidéo déjà programmée |
| Ven | **Astuce** | **Le verdict** de l'offre de jeudi |
| Sam | **A ou B** | Astuce chauffeur |
| Dim | **Question ouverte** (`kind: standard`, titre = la question, ex. « Ta course la plus longue cette semaine ? ») | Récap : l'essai gratuit 7 jours, sans engagement |

### JBKT (patrons de TPE et de PME : artisans, commerces, restaurants, ateliers, industrie)

| Jour | Post 08:30 | Reel 12:30 |
|---|---|---|
| Lun | **Ce ou ça** (`kind: sondage`) : deux façons de faire (papier / appli, Excel / outil…) | **Avant / après** : une tâche faite à la main, puis avec un outil |
| Mar | **Astuce** (`kind: astuce`) : liste à enregistrer (site, Google, organisation) | (vidéo déjà programmée le mardi) sinon Avant / après |
| Mer | **Ce ou ça** | « 3 tâches à ne plus faire à la main » dans un métier précis |
| Jeu | **Astuce** | **Avant / après** |
| Ven | **Question ouverte** (« Quelle tâche vous prend le plus de temps chaque semaine ? ») | (réalisation déjà programmée le vendredi) |
| Sam | **Ce ou ça** | Un métier, un outil (ex. « Garage : les rendez-vous en ligne ») |
| Dim | **Astuce** | Comment on travaille : démo gratuite, visite, maquette validée, outil en place |

## Les 4 formats de post (champ `visual`)

| `visual.kind` | Champs | Ce qu'on voit |
|---|---|---|
| `offre` (Radar) | `offre` = `{prix, km, min, approche}` en texte (ex. `"14,60 €"`, `"11,2 km"`, `"24 min"`, `"7 min"`) | « Tu la prends ? » + une carte de course |
| `sondage` | `options` = 2 choix courts (5 mots max chacun) | la question + 2 cases A et B |
| `astuce` | `options` = 3 à 5 points courts (8 mots max chacun) ; titre de 50 caractères max | une liste numérotée |
| `standard` | `screen` (option) | titre + phrase grise (format habituel) |

Fond : radar `encre` (sombre) ou `gris` (clair) ; jbkt `nuit` (sombre) ou `clair`. Alterner.
`subtitle` = la phrase d'appel en bas (ex. « Réponds OUI ou NON en commentaire ») ; laisser vide pour la phrase par défaut.

Offres d'exemple Radar : des montants **plausibles et variés** (courtes, longues, approche longue…), présentés comme un exemple.
Garder `offre` dans le document : le reel « verdict » réutilise exactement les mêmes chiffres.

## Le document à créer (un par post, un par reel)

Chemin `contents/eng-<marque>-<AAAAMMJJ>-<post|reel>`. Champs :

```json
{
  "brand_id": "radar", "channel": "instagram", "status": "to_validate",
  "scheduled_at": "2026-11-16T07:30",
  "format": "Tu la prends ?",
  "title": "Tu la prends ?", "subtitle": "",
  "caption": "…", "hashtags": ["#ChauffeurVTC", "#VTC", "#VTCFrance", "#ChauffeurIndependant"],
  "visual": {"bg": "encre", "kind": "offre", "offre": {"prix": "14,60 €", "km": "11,2 km", "min": "24 min", "approche": "7 min"}},
  "checks": ["Rien d'inventé", "Appel à réagir"]
}
```
Pour un reel, en plus : `"video_url"` (adresse raw GitHub), `"video_formats": ["story", "reel"]`, `"apercus"` (sortie de `--apercus`), et `visual` = `{"bg": "encre"}`.
Mettre `"status": "scheduled"`, `"validated_at"` (maintenant, ISO) et `"validated_by": "Claude (plan délégué par Karim)"`.

**Story du post** (un document par jour et par marque) : `contents/eng-<marque>-<AAAAMMJJ>-story`, après le rendu du post :
`python3 outil/story.py images/AAAA/MM/<post>.jpg images/AAAA/MM/<id-story>.jpg`, puis
`{"brand_id", "channel": "instagram", "status": "scheduled", "scheduled_at": "<jour>T21:00" (radar) ou "T17:30" (jbkt), "title": "Story du post du jour",
"caption": "", "hashtags": [], "format": "story", "image_url": <adresse raw>, "visual": {"bg": …}, "validated_at", "validated_by"}`.
Les posts de la semaine doivent donc être rendus (`outil/rendre.py`) par cette tâche, et leur `image_url` rempli.

## Légendes

- Première ligne = la question ou l'accroche (c'est ce qu'on lit avant « plus »).
- Puis 1 à 3 phrases utiles, puis l'appel à réagir (« Réponds en commentaire », « Enregistre ce post », « Tag un collègue chauffeur »).
- Radar : tutoiement (entre chauffeurs), finir par « Essai gratuit 7 jours sur l’App Store » une fois sur deux. JBKT : vouvoiement, finir par « Démo gratuite de 30 minutes : lien en bio » une fois sur deux.
- 3 à 5 hashtags de la liste de la marque (PUBLIER.md). Radar : jamais de hashtag local.

## Étapes de la tâche du dimanche

1. `git pull`. Lire ce fichier, `outil/videos/REELS.md`, `outil/marques/radar.md`, `outil/marques/jbkt.md` et `outil/journal-engagement.md` (sujets déjà faits : ne pas les répéter avant 6 semaines).
2. Lire `contents` (db_query) : repérer les reels déjà programmés la semaine suivante pour radar et jbkt,
   et les documents `eng-…` déjà créés pour cette semaine : **ne jamais les recréer ni les écraser** (si toute la semaine existe déjà, s'arrêter et le dire).
3. Écrire les 14 posts et les reels manquants (suivre la semaine type), rendre les 14 posts (`outil/rendre.py`, vérifier à l'œil) et leurs 14 stories (`outil/story.py`).
4. Rendre chaque reel (`reel.py`, voir REELS.md) dans `videos/AAAA/MM/<id>.mp4` ; regarder des images de contrôle avant ;
   une fois tous rendus : `git add`, `git commit`, `git push`, attendre 20 s, vérifier chaque adresse raw (200).
5. Créer les documents (db_write `set`, 10 par appel au plus, attendre 2 s entre les appels).
6. Ajouter les sujets de la semaine à `outil/journal-engagement.md` (date, marque, format, sujet), commit et push.
7. Résumer : nombre de posts, reels et stories programmés, et les sujets de la semaine.


## JBKT : montrer ce qu'on construit (depuis le 15/11/2026)

Karim veut des contenus JBKT plus concrets : on voit l'outil, on comprend ce qu'il fait.
Source : la banque d'écrans `banque/jbkt/` (`ecrans.json` = les écrans, `series.json` = les textes de chaque démo).

- Rendu : `python3 outil/demo.py <demo> <dossier> --reel` donne le post (1080 × 1350), une story par écran et le reel.
  Déjà rendus dans `images/demos/` et `videos/demos/` (noms `<demo>-post.jpg`, `<demo>-story-<n>.jpg`, `<demo>-reel.mp4`).
- Semaine JBKT : **4 jours sur 7 = une démo** (post à 08:30 + reel de la démo à 12:30 + 2 stories de la démo à 17:30 et 19:30) ;
  les 3 autres jours gardent les formats d'engagement (Ce ou ça, Question, Astuce) et les vidéos déjà programmées (réalisations).
- Une démo n'est utilisée qu'une fois toutes les 6 semaines : noter la date dans `ecrans.json` (`utilise_le`).
- Légende : celle de `series.json` (`caption`, `hashtags`). Toujours « Démo réalisée avec des données fictives ».
  **Jamais** « notre client », « réalisation pour… » : ce sont des démos, pas des clients.
- Nouvelle démo déposée sans entrée dans `series.json` : l'écrire (cible, titre court sur 2 lignes, une phrase simple par écran,
  caption, hashtags, musique clair|calme|elan), rendre, vérifier les images à l'œil, puis programmer.


## JBKT : nouvelle DA et alternance (depuis le 15/11/2026, demande de Karim)

- Tous les visuels JBKT suivent la DA des démos : fond clair #F3F7FF, Manrope, logo JBKT en haut à gauche, pastille en haut à droite,
  bandeau nuit #0B1533 en bas avec l'appel à l'action et « Lien en bio ».
- Posts texte : `python3 outil/texte.py <post.json> <sortie.jpg>` (kinds : standard, sondage, astuce, fichiers, etapes ; exemples dans `images/textes/*.json`).
  Ne plus utiliser `outil/rendre.py` pour JBKT (il reste pour Radar VTC).
- **Alternance** : un jour une démo (post + reel de la démo + 2 stories de la démo), le lendemain un post texte (+ sa story via `outil/story.py`, + le reel du jour).
- Les posts texte gardés : ceux qui parlent d'un problème concret avec une phrase forte (ex. « Combien de versions de ce fichier circulent ? »).


## Croissance Instagram (depuis le 16/11/2026, demande de Karim : « + de followers »)

Constat du 16/11 : 165 abonnés Gloova, 3 Radar, 2 JBKT ; 0 enregistrement et 0 partage en 30 jours. On parlait trop de l'outil.
Instagram montre un compte à de nouvelles personnes quand ses publications sont **enregistrées, partagées et commentées**.

**Règle 70 / 30** : sur 10 publications d'une marque, 7 sont **utiles** (on les enregistre ou on les envoie à quelqu'un), 3 parlent du produit ou des démos.
- JBKT : au plus **3 démos par semaine** (remplace l'alternance un jour sur deux) ; les autres jours : astuces, carrousels utiles, questions.
- Chaque semaine, par marque : **1 carrousel utile** au moins (5 à 7 images), fait avec `python3 outil/carrousel.py <spec.json> <dossier>`
  (exemples dans `images/carrousels/*.json`). Images rangées dans `images/carrousels/`, document `contents` avec `format` = `carrousel` et `image_urls`.
  Idées : messages à copier, listes à vérifier, calculs pas à pas, erreurs à éviter. Rien d'inventé, aucun chiffre sans source.
  Sujets à faire en priorité (demande de Karim, 16/11) :
  Gloova : messages tout prêts pour relancer une cliente (fait le 17/11), **règles d'annulation à copier** ;
  JBKT : **astuces Excel et Google pour les PME** ; Radar : **calculs et seuils de rentabilité**.
  Dernière image : « Enregistre(z) ce post » + « Envoie(z)-le à … ».
- **Gloova** : depuis le 17/11/2026, Karim a délégué aussi Gloova (« valide tout automatiquement, si ça ne va pas on te dira après ») : le carrousel utile de la semaine est créé directement en `scheduled`, `validated_by` = « Claude (plan délégué par Karim) ».
- Légendes : finir par une demande simple (« Enregistre », « Envoie-le à… », une question).
- **Mot-clé en commentaire** (automatique depuis le 16/11) : quand quelqu'un écrit le mot-clé de la marque en commentaire ou en message privé,
  le serveur lui envoie le lien en message privé et répond « C'est envoyé en message privé 📩 » sous son commentaire.
  Mots-clés : **RADAR** (lien App Store), **GLOOVA** (gloova.fr), **DEMO** (démos JBKT).
  Chaque semaine, par marque, **2 publications au moins** finissent par cet appel, à la place de « lien en bio » :
  Radar « Commente RADAR et je t'envoie le lien de l'essai gratuit en privé », Gloova « Écrivez GLOOVA en commentaire et on vous envoie le lien en privé »,
  JBKT « Écrivez DEMO en commentaire pour recevoir nos démos en privé ». Le carrousel utile de la semaine en fait partie.

**Liste du jour « 10 comptes à commenter »** (champ `a_commenter` de `insta/<marque>`, rempli chaque matin par la tâche « Relevé Instagram ») :
- 10 **vrais comptes Instagram publics** de la cible, trouvés par recherche web et vérifiés (le profil existe, compte actif, pas un concurrent) :
  Gloova = esthéticiennes, instituts, ongleries, prothésistes, extensions de cils en France ;
  Radar = chauffeurs VTC indépendants en France (comptes de chauffeurs, pas de plateformes) ;
  JBKT = commerces, artisans, restaurants et PME d'Alsace (Strasbourg, Bas-Rhin, Haut-Rhin).
- Pas un compte vu dans les 14 derniers jours (`deja_vus`, garder les 140 derniers noms).
- Pour chacun : `pourquoi` (quelques mots : métier, ville si connue) et `idee` = une idée de vrai commentaire liée à son métier,
  à adapter à la publication choisie. Jamais de lien, jamais de pub, jamais de mensonge, jamais « super ! ».
- Rien d'inventé : si la recherche ne donne pas 10 comptes sûrs, en mettre moins.
- **Compte vivant obligatoire** (demande de Karim, 18/11/2026) : la dernière publication doit dater de **moins de 30 jours**.
  Vérifier avec Firecrawl / Alexandria `scrapecreators` → `instagram/user-posts` (handle, trim = true), trier par `taken_at` (les posts épinglés sont en tête).
  Compte introuvable ou sans publication depuis 30 jours : on l'écarte et on le met dans `deja_vus`.
  Pour trouver de nouveaux comptes actifs : `instagram/hashtag-posts` (date_posted = last-week) sur les hashtags de la cible.
- **Commentaire collé à la publication** : pour chaque compte, donner `post_url` (la dernière publication) et `commentaire` = un texte prêt à copier
  qui parle de CETTE publication (ce qu'elle montre ou demande), avec une vraie question. Gloova et JBKT : vouvoiement ; Radar : tutoiement.

**Onglet « Croissance Instagram » de l'outil** (documents `insta/gloova`, `insta/jbkt`, `insta/radar`) :
- rempli chaque matin par la tâche « Relevé Instagram » (abonnés du jour, portée, enregistrements, partages, formats) avec `outil/insta/releve.py` ;
- le dimanche, la tâche de programmation met à jour, pour les 3 marques :
  - `scripts` : 3 reels à tourner par Karim ou Julien (`mode` face / voix / ugc, accroche des 2 premières secondes, 3 ou 4 lignes, fin, conseil de tournage).
    UGC = seulement une vraie cliente qui est d'accord, avec ses vrais mots ; si elle est payée ou reçoit un cadeau : « collaboration commerciale ».
    Jamais de faux témoignage, jamais d'avatar présenté comme une cliente. Radar : toujours « voiture garée ».
  - `engage` : 4 ou 5 endroits où aller commenter (hashtags, types de comptes) avec 1 ou 2 idées de vrais commentaires (jamais de lien, jamais de pub).
  - `notes` : 2 à 4 phrases tirées des chiffres de la semaine (ce qui a marché, ce qu'on change).
- Pour choisir les sujets : regarder les publications avec le meilleur `score` dans `insta/<marque>` et refaire le même type de sujet.
- Quand Karim envoie une vidéo tournée : la monter (sous-titres, coupe, musique légère), la programmer en reel, et passer le script à `done` = true.

## Recycler ce qui marche (depuis le 18/11/2026, demande de Karim)

Chaque dimanche, avant de créer la semaine, regarder dans `insta/<marque>.posts` les publications publiées **il y a 3 à 6 semaines**
avec le meilleur `score` (portée + enregistrements + partages), et pour chaque marque, en reprendre **1** (2 au plus) dans un autre format :
- une image ou un post texte qui a bien marché → un reel (outil/videos) ou un carrousel utile (outil/carrousel.py) ;
- un reel qui a bien marché → un carrousel qui détaille le même conseil, ou une nouvelle accroche sur la même vidéo ;
- un carrousel qui a bien marché → un reel « en 20 secondes ».
Même idée, nouveau texte et nouvelle accroche : jamais republier le même visuel avec la même légende.
Champ du document : `recycle_de` = le `permalink` de la publication d'origine, et `format` = le nouveau format.
Les règles de chaque marque s'appliquent comme d'habitude (vérifier à nouveau prix, fonctions, calculs).
Ne pas recycler un sujet lié à une date passée (concours terminé, offre finie).

## Nouveau style des posts JBKT et Radar (depuis le 18/11/2026, validé par Karim)

Les posts image JBKT et Radar se font maintenant avec deux scripts, et plus avec les anciens visuels « carte » :
- `outil/mockup_post.py` : les écrans posés dans un ordinateur, une tablette ou un téléphone, **au format exact de l'écran**
  (ordinateur 2880 × 1800, tablette 2048 × 1536, téléphone 1179 × 2556) : jamais étirés ni coupés.
  JBKT : écrans de `banque/jbkt` (mention « Démo · données fictives »). Radar : écran dessiné en HTML au style de l'app
  (offre d'exemple, aucun nom de plateforme, aucun lieu, mention « Exemple fictif »), calculs vérifiés.
- `outil/photo_post.py` : une photo Higgsfield (gpt_image_2_6, 0,25 crédit, sans texte ni logo) + titre, logo et bouton.
Alterner une photo et un post en appareils, pour une grille propre. Exemples publiés le 18/11 : `images/mockups/`, `images/photos-posts/`.
