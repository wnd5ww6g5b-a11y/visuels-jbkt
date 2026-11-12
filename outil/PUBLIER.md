# Publication automatique des posts Instagram

Ce dépôt sert à deux choses :
1. `outil/` : le moteur qui dessine un post en image JPEG 1080 × 1350 (`rendu.html` + `rendre.py`).
2. `images/` : les images publiées. Le dépôt est public, Instagram lit l'image à son adresse
   `https://raw.githubusercontent.com/wnd5ww6g5b-a11y/visuels-jbkt/main/images/...`

## Règles de publication (à respecter strictement)

Un post n'est publié QUE s'il remplit TOUTES ces conditions, lues dans la base de l'outil
(artifact `215e6505-5f68-4a59-8694-595b631af2eb`, collection `contents`) :
- `channel` = `instagram`
- `status` = `scheduled`
- `validated_at` est présent (validé par Karim ou Julien dans l'outil)
- `published_at` est absent
- `scheduled_at` (heure de Paris) est passé, et date de moins de 24 h

Les posts d'exemple n'ont pas de `validated_at` : ils ne sont jamais publiés.

Le compte Instagram de chaque marque est dans le document `config/instagram`
(`gloova`, `jbkt`, `radar` → `account_id`).

## Étapes

1. Lire `config/instagram` et la collection `contents` (db_query, `channel` = `instagram`, `status` = `scheduled`).
2. Garder seulement les posts qui remplissent les règles ci-dessus.
3. Pour chaque post :
   1. Écrire `post.json` = `{"brand": <brand_id>, "content": <le document>}`.
   2. `python3 outil/rendre.py post.json images/AAAA/MM/<id>.jpg` (Pillow et Google Chrome nécessaires).
   3. Vérifier l'image à l'œil (Read) : titre lisible, rien de coupé.
   4. `git add`, `git commit -m "Post <id>"`, `git push origin main`.
   5. Attendre ~20 s, puis vérifier que l'adresse raw répond (curl -I, code 200).
   6. Windsor.ai for Social Media : `execute_action`, connector `instagram`, action `create_image_post`,
      account = `account_id` de la marque, params = `{"image_url": <adresse raw>, "caption": <légende finale>}`.
      Légende finale = `caption` + ligne vide + les `hashtags` séparés par des espaces.
      Si `hashtags` est vide ou absent : ajouter 3 ou 4 hashtags pertinents de la liste de la marque ci-dessous.
      La légende finale ne doit jamais dépasser 2 200 caractères (raccourcir les hashtags si besoin, jamais la légende).
   7. Mettre à jour le document `contents/<id>` (db_write `update` avec `ifVersion`) :
      `status` = `published`, `published_at` = maintenant (ISO), `image_url` = adresse raw.
4. En cas d'erreur sur un post : NE PAS réessayer en boucle. Écrire `publish_error` = le message dans le document,
   laisser `status` à `scheduled`, et passer au suivant.
5. Résumer à la fin : posts publiés, posts en erreur.

## Hashtags de base par marque

- **gloova** : #InstitutDeBeaute #Estheticienne #EstheticienneADomicile #ProthesisteOngulaire #Onglerie #SalonDeCoiffure #Barbier #ExtensionDeCils #ReservationEnLigne #AgendaEnLigne #ProsDeLaBeaute
- **radar** : #ChauffeurVTC #VTC #VTCStrasbourg #Strasbourg #Alsace #ChauffeurPrive #VTCFrance #ChauffeurIndependant
- **jbkt** : #Strasbourg #Alsace #GrandEst #PME #Industrie #Digitalisation #OutilMetier #RemplacerExcel #Productivite #ApplicationSurMesure
