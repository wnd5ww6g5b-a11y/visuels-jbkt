# Mise à jour mensuelle des pages (JBKT et Gloova)

Décidé par Karim le 13/11/2026 : une fois par mois, l'outil remet à jour des pages existantes, parce que les IA
(ChatGPT, Perplexity, résumés IA de Google) préfèrent un contenu récent et précis. Comme les contenus automatiques,
c'est fait **sans validation** : les règles ci-dessous sont strictes, et chaque mise à jour est visible dans l'outil.

## Combien et lesquelles

Par site, **2 pages** par mois (4 au total) :
1. d'abord une page liée à une question GEO où la marque est `absent` ou `mention`
   (document `geo/<marque>` de l'outil, et `outil/geo/priorites.md`) ;
2. ensuite la page la plus ancienne (date `<lastmod>` du plan du site) parmi : pages services, pages métier,
   pages zone, articles de blog. Jamais les pages légales, les pages de prix, ni les pages de réalisations.
Ne pas reprendre une page mise à jour dans les 3 derniers mois (voir `refreshed` dans `geo/<marque>`).

Où sont les pages :
- JBKT : dépôt `wnd5ww6g5b-a11y/site-jbkt`, fichiers `.html` (ex. `blog/*.html`, `metiers/*.html`, `zones/*.html`, pages services à la racine).
- Gloova : dépôt `wnd5ww6g5b-a11y/gloomy-site`. Pages créées par l'outil : `src/data/articles-auto.json`.
  Pages écrites à la main : `src/pages/seo/*.tsx` et `src/pages/seo/blog/*.tsx` (ne changer que du texte).

## Ce qu'on améliore (sans changer l'adresse de la page)

- Le premier paragraphe répond directement à la question principale de la page, avec le nom de la marque (règles GEO de `outil/CONTENU-AUTO.md`).
- Les sous-titres deviennent des questions quand c'est naturel ; chaque partie commence par une réponse qui se comprend seule.
- La FAQ : 3 à 5 questions telles qu'un client les taperait dans ChatGPT, réponses courtes avec le nom de la marque.
- Retirer tout chiffre, pourcentage, avis ou nom de client sans source (règle permanente). Retirer ce qui n'est plus vrai.
- Ajouter des liens vers les pages plus récentes du site quand c'est utile (seulement vers des pages qui existent).
- Garder le titre principal (h1), l'adresse, le ton et la mise en page. Pas de prix JBKT. Pas de fonction Gloova inventée.

## Date de mise à jour

- JBKT : ajouter ou mettre à jour, sous le h1, `<p class="maj">Mis à jour le <date en toutes lettres></p>`,
  et `"dateModified": "AAAA-MM-JJ"` dans les données structurées de la page (ne pas toucher `datePublished`).
- Gloova, pages de `articles-auto.json` : champ `"updated": "AAAA-MM-JJ"` (la page l'affiche et le met dans ses données).
- Gloova, pages `.tsx` : passer `dateModified="AAAA-MM-JJ"` au composant `SEOPageLayout` si la page l'utilise.

## Mettre en ligne

1. JBKT : `node scripts/sitemap.mjs && node scripts/llms.mjs` pour vérifier, puis commit et push.
2. Gloova : `npm run build` doit réussir (sinon annuler la modification), puis commit et push.
   Pour une page de `articles-auto.json`, mettre aussi à jour sa date dans `public/sitemap-pages.xml`.
3. Ajouter chaque page à `refreshed` dans `geo/<marque>` de l'outil (db_get puis db_write `update`) :
   `{"date": "AAAA-MM-JJ", "url": "<adresse complète>", "title": "<titre>"}` (garder les 24 dernières).
4. Ajouter une ligne dans `outil/journal-contenu.md` : date · marque · « mise à jour » · adresse · ce qui a changé.
5. Résumé court : les 4 pages mises à jour et ce qui a changé sur chacune.
