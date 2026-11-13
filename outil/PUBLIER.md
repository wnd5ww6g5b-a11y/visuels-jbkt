# Publication automatique des posts Instagram

Ce dépôt sert à deux choses :
1. `outil/` : le moteur qui dessine un post en image JPEG 1080 × 1350 (`rendu.html` + `rendre.py`).
2. `images/` : les images publiées. Le dépôt est public, Instagram lit l'image à son adresse
   `https://raw.githubusercontent.com/wnd5ww6g5b-a11y/visuels-jbkt/main/images/...`

## Deux travaux à chaque passage

**A. Préparer les images à l'avance** (pour que l'outil puisse publier tout de suite, sans attendre).
Un post a besoin d'une image s'il remplit TOUTES ces conditions :
- `channel` = `instagram`
- `status` = `to_validate`, ou `status` = `scheduled` avec `validated_at` présent
- `published_at` absent
- `image_url` absent ou vide (l'outil l'efface quand le titre, la phrase grise ou le fond changent)
- `scheduled_at` entre il y a 24 h et dans 21 jours

Les posts d'exemple `scheduled` sans `validated_at` n'ont pas besoin d'image.
**Un document avec `video_url` n'a JAMAIS besoin d'image** : c'est une vidéo fournie par Karim, publiée telle quelle.

**B. Publier les posts arrivés à l'heure.** Un post n'est publié QUE s'il remplit TOUTES ces conditions :
- `channel` = `instagram`
- `status` = `scheduled` (jamais `publishing` : l'outil est en train de le publier lui-même)
- `validated_at` est présent (validé par Karim ou Julien dans l'outil)
- `published_at` est absent
- `scheduled_at` (heure de Paris) est passé, et date de moins de 24 h

Base de l'outil : artifact `215e6505-5f68-4a59-8694-595b631af2eb`, collection `contents`.
Le compte Instagram de chaque marque est dans le document `config/instagram`
(`gloova`, `jbkt`, `radar` → `account_id`).

Si aucun post ne relève de A ni de B : s'arrêter tout de suite, sans rien modifier.

## Vidéos (documents avec `video_url`)

Vidéos fournies par Karim : on les publie **exactement telles quelles** (jamais réencodées, recadrées ni refaites).
Quand une vidéo remplit les conditions de B (publication à l'heure) :
1. Story : `execute_action`, connector `instagram`, action `create_story`, account = `account_id` de la marque,
   params = `{"video_url": <video_url>}`.
2. Reel : action `create_video_post`, params = `{"video_url": <video_url>, "caption": <légende finale>, "thumb_offset": 1500, "share_to_feed": true}`
   (légende finale = `caption` + ligne vide + `hashtags`, comme pour les images).
3. Mettre à jour le document : `status` = `published`, `published_at` = maintenant, `story_media_id` et `instagram_media_id` = les id renvoyés.
Si un des deux échoue : noter `publish_error` avec le message, mais garder l'id de celui qui a réussi, et ne pas republier celui-là.

## Étapes

1. Lire `config/instagram` et la collection `contents` (db_query, `channel` = `instagram`).
2. **A — pour chaque post qui a besoin d'une image :**
   1. Écrire `post.json` = `{"brand": <brand_id>, "content": <le document>}`.
   2. `python3 outil/rendre.py post.json images/AAAA/MM/<id>-<horodatage>.jpg`
      (AAAA/MM = mois de `scheduled_at`, horodatage = date et heure du rendu, ex. `20261112-1904`, pour que chaque nouvelle version ait une adresse neuve).
   3. Vérifier l'image à l'œil (Read) : titre lisible, rien de coupé.
   Puis, une seule fois pour toutes les images : `git add`, `git commit -m "Images prêtes"`, `git push origin main`.
   Attendre ~20 s, vérifier que chaque adresse raw répond 200 (curl -I), puis écrire dans chaque document
   (db_write `update` avec `ifVersion`) : `image_url` = adresse raw. Ne pas changer le `status`.
   Si le document a changé entre-temps (conflit de version) : ne rien écrire pour ce post, il sera repris au passage suivant.
3. **B — pour chaque post à publier :**
   1. Utiliser son `image_url` (déjà prêt, ou préparé à l'étape A). S'il n'y en a pas, le préparer comme en A.
   2. Windsor.ai for Social Media : `execute_action`, connector `instagram`, action `create_image_post`,
      account = `account_id` de la marque, params = `{"image_url": <adresse raw>, "caption": <légende finale>}`.
      Légende finale = `caption` + ligne vide + les `hashtags` séparés par des espaces.
      Si `hashtags` est vide ou absent : ajouter 3 ou 4 hashtags pertinents de la liste de la marque ci-dessous.
      La légende finale ne doit jamais dépasser 2 200 caractères (raccourcir les hashtags si besoin, jamais la légende).
   3. Mettre à jour le document `contents/<id>` (db_write `update` avec `ifVersion`) :
      `status` = `published`, `published_at` = maintenant (ISO), `instagram_media_id` = id renvoyé.
4. En cas d'erreur sur un post : NE PAS réessayer en boucle. Écrire `publish_error` = le message dans le document,
   laisser `status` tel quel, et passer au suivant.
5. Résumer à la fin : images préparées, posts publiés, posts en erreur.

## Hashtags de base par marque

- **gloova** : #InstitutDeBeaute #Estheticienne #EstheticienneADomicile #ProthesisteOngulaire #Onglerie #SalonDeCoiffure #Barbier #ExtensionDeCils #ReservationEnLigne #AgendaEnLigne #ProsDeLaBeaute
- **radar** (toute la France, jamais de hashtag local comme #VTCStrasbourg) : #ChauffeurVTC #VTC #VTCFrance #ChauffeurPrive #ChauffeurIndependant #AppliVTC
- **jbkt** : #Strasbourg #Alsace #GrandEst #PME #Industrie #Digitalisation #OutilMetier #RemplacerExcel #Productivite #ApplicationSurMesure
