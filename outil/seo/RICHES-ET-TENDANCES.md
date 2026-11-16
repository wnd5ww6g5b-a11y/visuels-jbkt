# Résultats enrichis + Tendances Google (décidé par Karim le 17/11/2026)

Tâche du lundi (après le relevé Search Console, avant le test GEO). Base de l'outil : artifact
`215e6505-5f68-4a59-8694-595b631af2eb`, documents `seo/enrichis-<marque>` et `seo/tendances-<marque>` (affichés page SEO).

## 1. Résultats enrichis (chaque lundi) — JBKT et Gloova

Google n'ouvre pas son Rich Results Test aux outils : `outil/seo/donnees_structurees.py` applique les mêmes règles
(champs obligatoires et recommandés de Google) et donne pour chaque page le lien du test officiel.

1. **JBKT** (`wnd5ww6g5b-a11y/site-jbkt`, HTML statique) : pour chaque `<loc>` de `sitemap.xml`, le fichier HTML correspondant
   (`<chemin>.html`, `<chemin>/index.html` ou `index.html` pour `/`).
2. **Gloova** (`wnd5ww6g5b-a11y/gloomy-site`, pages générées dans le navigateur) : HTML rendu avec Firecrawl
   (`firecrawl_scrape`, formats `["rawHtml"]`, `maxAge: 0`), **au plus 20 pages par lundi** pour limiter les crédits :
   d'abord les pages modifiées depuis 8 jours (`git log --since="8 days ago" --name-only`), puis les pages des
   `questions.json` du GEO, puis `/`, `/pricing`, `/gloova-prix`. Enregistrer chaque HTML dans un fichier.
3. Lancer `python3 outil/seo/donnees_structurees.py pages.json resultat.json`.
4. **Corriger** chaque `erreur` (jamais les avertissements « avis » : on n'invente jamais d'étoiles ni d'avis) :
   champ manquant ajouté dans le JSON-LD de la page, construction du site (Gloova : `npm ci` puis `npm run build`), commit, push.
   Si la construction échoue : annuler. Noter la correction dans `corrige` de la page (1 phrase).
   Une page sans données (`absent`) : ajouter un bloc adapté (BreadcrumbList, et FAQPage si la page a une vraie FAQ visible).
5. Écrire `seo/enrichis-<marque>` (db_write `set`) : `{date, resume, pages: [seulement les pages qui ne sont pas « ok »], note}`.
   `note` = « Pages vérifiées : N (… ). Seules celles à revoir sont listées. »

## 2. Tendances Google (le premier lundi du mois seulement)

Fournisseur Firecrawl `firecrawl-trends` (5 crédits par appel, 6 appels par mois), France (`geo: "FR"`) :
| Marque | interest_over_time (`time: "today 5-y"`) | related_queries (`time: "today 12-m"`) |
|---|---|---|
| gloova | bon cadeau institut, extension de cils, onglerie, institut de beauté, esthéticienne | esthéticienne |
| jbkt | création site internet, logiciel sur mesure, application mobile, site vitrine, logiciel de gestion | création site internet |
| radar | vtc, chauffeur vtc, devenir chauffeur vtc | chauffeur vtc |

Un seul appel `alexandria_library_read` avec les 6 appels dans cet ordre, résultat enregistré dans un fichier, puis :
`python3 outil/seo/tendances.py resultat.json plan.json dossier/` avec
`plan.json = {"gloova":{"courbes":[0],"associees":[3]},"jbkt":{"courbes":[1],"associees":[4]},"radar":{"courbes":[2],"associees":[5]}}`.
Relire les listes « en hausse » : retirer tout ce qui vient d'un fait divers, d'un drame ou d'un site web. Écrire `seo/tendances-<marque>`.

**Utilisation** : la tâche « Contenu SEO automatique » lit `seo/tendances-<marque>` (champ `conseil` et mois forts) pour
choisir un sujet de saison quand il colle à la marque. Radar : jamais de nom de plateforme ni de lieu dans les posts,
même si la recherche les contient.

## Règles
Rien d'inventé ; jamais de prix JBKT ; ne jamais changer l'adresse d'une page ; ne jamais ajouter d'avis ni de note.
