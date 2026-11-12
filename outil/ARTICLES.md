# Publication des articles de blog validés

Un article est mis en ligne QUE s'il remplit TOUTES ces conditions (collection `contents` de l'outil,
artifact `215e6505-5f68-4a59-8694-595b631af2eb`) :
- `channel` = `article`
- `status` = `scheduled`
- `validated_at` présent (validé par Karim ou Julien)
- `published_at` absent
- `scheduled_at` (heure de Paris) passé
- le champ `article` est rempli (`slug`, `description`, `category`, `lead`, `body`, `faq`, `links`)

Sites :
| brand_id | dépôt GitHub (accès push) | adresse de l'article |
|---|---|---|
| `jbkt` | `wnd5ww6g5b-a11y/site-jbkt` | `https://www.jbktsolutionsdigitales.fr/blog/<slug>` |
| `gloova` | `wnd5ww6g5b-a11y/gloomy-site` | `https://gloova.fr/blog/<slug>` |

Toute autre marque : ne rien publier, écrire `publish_error` = "Pas de site relié".

## Étapes, pour chaque article

1. Ajouter le dépôt du site (add_repo, accès "push"), le cloner (`git clone --depth 1`).
2. Écrire `article.json` = `{"slug", "title", "description", "category", "lead", "body", "faq", "links", "date"}`
   avec `title` = `title` du document, les autres champs pris dans `article`, et `date` = aujourd'hui (AAAA-MM-JJ, heure de Paris).
3. Dans le dossier du site : `node scripts/ajouter-article.mjs article.json`.
   - Si le script répond que l'adresse existe déjà : NE PAS forcer. Écrire `publish_error` avec le message et passer au suivant.
4. Vérifier :
   - JBKT : ouvrir `blog/<slug>.html` (titre, intro, sous-titres présents) et voir que `blog.html` contient la carte.
   - Gloova : `npm ci` puis `npm run build` doit réussir (sinon : ne pas pousser, écrire `publish_error`).
5. `git add -A`, `git commit -m "Article : <titre>"`, `git -c push.negotiate=true push origin main`.
   Vercel met le site en ligne tout seul en 1 à 3 minutes.
6. Attendre ~3 min puis vérifier que l'adresse de l'article répond 200 (`curl -sL -o /dev/null -w "%{http_code}"`).
   Si l'outil réseau refuse l'adresse, ce n'est pas une erreur de publication : le noter dans le résumé.
7. Mettre à jour `contents/<id>` (db_write `update` avec `ifVersion`) : `status` = `published`,
   `published_at` = maintenant (ISO), `published_url` = l'adresse de l'article.

En cas d'erreur : ne pas réessayer en boucle, écrire `publish_error`, laisser `status` à `scheduled`, passer au suivant.
Ne jamais modifier autre chose sur les sites que ce que fait le script.
