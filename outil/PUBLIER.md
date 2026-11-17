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
**Un document avec `video_url` ou `image_urls` n'a JAMAIS besoin d'image** : vidéo ou carrousel fournis par Karim, publiés tels quels.
**Un document avec `status` = `manual` n'est jamais touché** (ni image, ni publication) : c'est une story avec sticker que Karim poste à la main.

**B. Publier les posts arrivés à l'heure.** Un post n'est publié QUE s'il remplit TOUTES ces conditions :
- `channel` = `instagram`
- `status` = `scheduled` (jamais `publishing` : l'outil est en train de le publier lui-même)
- `validated_at` est présent (validé par Karim ou Julien dans l'outil)
- `published_at` est absent
- `scheduled_at` (heure de Paris) est passé, et date de moins de 24 h

Base de l'outil : artifact `215e6505-5f68-4a59-8694-595b631af2eb`, collection `contents`.
Le compte Instagram de chaque marque est dans le document `config/instagram`
(`gloova`, `jbkt`, `radar` → `account_id`).

**D. Commentaires (Gloova, Radar VTC et JBKT)** : répondre à chaque nouveau commentaire dans l'heure (automatique si simple, validation si délicat), publier les réponses validées.

Si rien ne relève de A, B ni D (ni des articles, voir ARTICLES.md) : s'arrêter tout de suite, sans rien modifier.

## Vidéos (documents avec `video_url`)

Vidéos fournies par Karim : on les publie **exactement telles quelles** (jamais réencodées, recadrées ni refaites).
Quand une vidéo remplit les conditions de B (publication à l'heure), regarder `video_formats`
(absent = `["story","reel"]`) et ne faire que les formats listés :
1. Si `story` : `execute_action`, connector `instagram`, action `create_story`, account = `account_id` de la marque,
   params = `{"video_url": <video_url>}`.
2. Si `reel` : action `create_video_post`, params = `{"video_url": <video_url>, "caption": <légende finale>, "thumb_offset": 1500, "share_to_feed": true}`
   (légende finale = `caption` + ligne vide + `hashtags`, comme pour les images).
3. Mettre à jour le document : `status` = `published`, `published_at` = maintenant, `story_media_id` et `instagram_media_id` = les id renvoyés.
Si un des deux échoue : noter `publish_error` avec le message, mais garder l'id de celui qui a réussi, et ne pas republier celui-là.

## Stories image (documents avec `format` = `story` et `image_url`)

Visuel fourni par Karim (1080 × 1920), publié tel quel, jamais redessiné. Quand il remplit les conditions de B :
`execute_action`, connector `instagram`, action `create_story`, account = `account_id` de la marque, params = `{"image_url": <image_url>}`.
Puis `status` = `published`, `published_at`, `story_media_id`. Ne jamais le publier en post (`create_image_post`).

## Carrousels (documents avec `image_urls`)

Images fournies par Karim (JPEG, dans l'ordre), publiées telles quelles. Quand un carrousel remplit les conditions de B :
`execute_action`, connector `instagram`, action `create_carousel_post`, account = `account_id` de la marque,
params = `{"image_urls": <image_urls>, "caption": <légende finale>}` (légende finale = `caption` + ligne vide + `hashtags`).
Puis `status` = `published`, `published_at`, `instagram_media_id`. En cas d'erreur : `publish_error`, pas de nouvel essai.


## Facebook (décidé par Karim le 17/11/2026, revu le soir même)

Pages Facebook (connector Windsor `facebook_organic`) : `gloova` → `1497497520105638` ; `jbkt` → `1308753372330573` ;
`radar` → `1407890339078131` (aussi dans le document `config/facebook`).

**On ne recopie plus Instagram sur Facebook** (« ce sont des réseaux différents, on ne poste pas pareil ») : seuls les
documents `channel` = `"facebook"` sont publiés sur Facebook. Ils sont écrits pour Facebook (voir `outil/RESEAUX.md`).

Pour chaque document `channel` = `"facebook"`, status `scheduled` ou `validated`, arrivé à l'heure, sans `facebook_post_id` :
1. `format` = `"image"` : action `create_photo_post`, params = `{"image_url": <image_url>, "caption": <caption>}`.
2. `format` = `"texte"` ou `"lien"` : action `create_post`, params = `{"message": <caption>}` et `"link": <link>` s'il existe.
3. account = id de la Page de la marque. Écrire `facebook_post_id`, `facebook_published_at`, status `published`.
   En cas d'erreur : `facebook_error`, status `error`, pas de nouvel essai.
4. Jamais un document Gloova en `to_validate` ; jamais de carrousel, de vidéo ni de story sur Facebook.

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
5. Facebook : publier les documents `channel` = `facebook` arrivés à l'heure (partie « Facebook » ci-dessus).
6. Résumer à la fin : images préparées, posts publiés (Instagram et Facebook), posts en erreur.

## D. Commentaires (Gloova, Radar VTC et JBKT) : réponse dans l'heure

Décidé par Karim le 16/11/2026 : pour gagner des abonnés, **chaque commentaire reçoit une réponse dans l'heure**, sur les 3 comptes.
Les réponses simples partent **tout de suite, sans validation**. Tout ce qui est délicat passe par la validation de Karim.

**Mots-clés (depuis le 16/11)** : un commentaire qui contient seulement ou surtout un mot-clé (RADAR, GLOOVA, DEMO) est déjà traité
par le serveur (lien en message privé + réponse « C'est envoyé en message privé 📩 »). Ne pas y répondre une 2e fois :
le noter `status` = `replied`, `auto` = true, `reply` = « (mot-clé : réponse automatique du serveur) ».

1. **Publier les réponses validées** : collection `comments`, documents avec `status` = `validated` et sans `error`.
   Pour chacun : Windsor.ai for Social Media, `execute_action`, connector `instagram`, action `reply_to_comment`,
   account = `account_id` de la marque, params = `{"comment_id": <id du document>, "message": <reply>}`.
   Puis `update` : `status` = `replied`, `replied_at` = maintenant. En cas d'erreur : écrire `error` = le message, ne pas réessayer.
2. **Relever les nouveaux commentaires** : `get_data`, connector `instagram`, accounts = ceux de `gloova`, `radar` et `jbkt`,
   fields = `["account_id","media_id","media_permalink","media_caption","comment_id","comment_text","comment_username","comment_timestamp","comment_parent_id"]`,
   date_preset = `last_30d` (la date est celle de la publication, pas du commentaire).
   Garder les lignes qui ont un `comment_id`, dont l'auteur n'est pas le compte lui-même (`radar_vtc`, `jbktsolutionsdigitales`, `gloova_beauty`)
   et qui n'existent pas encore dans `comments` (même id). Ignorer les commentaires de plus de 7 jours.
3. **Trier chaque nouveau commentaire** :
   - **Simple → réponse automatique tout de suite** : un vote (« A », « OUI »), un compliment, un emoji, un avis sur le sujet du post,
     une question dont la réponse est **écrite telle quelle** dans `outil/marques/<marque>.md` (ex. « c'est sur iPhone ? », « il y a un essai ? »).
     Publier avec `reply_to_comment`, puis créer `comments/<comment_id>` avec `status` = `replied`, `replied_at`, `auto` = true.
   - **Délicat → validation** : critique, plainte, problème avec l'app, question sur un prix JBKT, question sur un compte ou un paiement,
     tout ce dont la réponse n'est pas sûre. Créer le document avec la réponse proposée et `status` = `to_validate`.
   - **Spam, insulte, pub, faux comptes de gains** : `reply` = `""`, `status` = `ignored`, pas de réponse.
   Document : `{"brand_id", "media_id", "permalink", "post_title" (titre du document contents dont instagram_media_id = media_id, sinon 1re ligne de la légende),
   "username", "text", "at" (comment_timestamp), "reply", "status"}` (+ `auto`, `replied_at` si publié).
4. **Écrire la réponse** :
   - courte (1 à 2 phrases), chaleureuse, dans le ton de la marque (Radar : tutoiement entre chauffeurs ; JBKT et Gloova : vouvoiement) ;
   - **finir par une question** quand c'est naturel : une réponse qui relance fait revenir la personne et pousse le post ;
   - un vote → remercier et demander pourquoi ; un compliment → remercier et poser une question sur son activité ;
   - jamais de prix JBKT, jamais de promesse de gains, rien d'inventé ; pas de lien (le lien est en bio) ;
   - jamais 2 fois la même phrase d'affilée sur un même compte.
5. Résumer : réponses publiées automatiquement, réponses à valider.

### Concours Gloova (23 nov. → 18 déc. 2026) : réponses automatiques

Décidé par Karim : sur le post du concours (document `contents/concours-gloova-carrousel`, son `instagram_media_id`)
et sur le reel du concours (`contents/concours-gloova-reel`), les **participations** reçoivent une réponse courte
**publiée tout de suite, sans validation**. Tout le reste suit la partie D (automatique si simple, validation si délicat).
- **Participation** = un commentaire qui donne une prestation et/ou identifie un compte (@…), sans question.
  Réponse : 1 phrase, vouvoiement, chaleureuse, qui reprend la prestation citée si elle est claire, puis
  « Participation bien enregistrée, bonne chance ! ✨ » (varier un peu la formulation, jamais 2 fois la même d'affilée).
  Publier avec `reply_to_comment`, puis créer `comments/<id>` avec `status` = `replied`, `replied_at`, `auto` = true.
  Ne jamais dire qu'une participation est gagnante ou « validée » au tirage ; ne rien promettre.
- **Question** (règlement, lots, date, « je ne suis pas esthéticienne », etc.) ou **critique** : réponse proposée,
  `status` = `to_validate` (Karim valide). S'appuyer seulement sur le règlement : gloova.fr/concours.
- **Spam, insulte, compte de « tirage » ou de faux gains** : `status` = `ignored`, pas de réponse.

## Hashtags de base par marque

- **gloova** : #InstitutDeBeaute #Estheticienne #EstheticienneADomicile #ProthesisteOngulaire #Onglerie #SalonDeCoiffure #Barbier #ExtensionDeCils #ReservationEnLigne #AgendaEnLigne #ProsDeLaBeaute
- **radar** (toute la France, jamais de hashtag local comme #VTCStrasbourg) : #ChauffeurVTC #VTC #VTCFrance #ChauffeurPrive #ChauffeurIndependant #AppliVTC
- **jbkt** : #Strasbourg #Alsace #GrandEst #PME #Industrie #Digitalisation #OutilMetier #RemplacerExcel #Productivite #ApplicationSurMesure
