# Contenu automatique pour le référencement (JBKT et Gloova)

Décision de Karim (12 novembre 2026) : l'outil écrit ET met en ligne seul, sans validation,
2 contenus par semaine et par site. Karim et Julien relisent après coup dans l'outil.
Comme rien n'est relu avant la mise en ligne, les règles de qualité ci-dessous sont strictes.

## Planning

| Jour | JBKT (jbktsolutionsdigitales.fr) | Gloova (gloova.fr) |
|---|---|---|
| Lundi | 1 article de blog | 1 article de blog |
| Jeudi | 1 page « service + zone » | 1 page « métier ou thème » |

Radar VTC : rien (pas de site web).

## Avant d'écrire

1. Lire la fiche de la marque : `outil/marques/jbkt.md` ou `outil/marques/gloova.md`.
2. Lire `outil/journal-contenu.md` (tout ce qui a déjà été publié) et la liste réelle du site :
   - JBKT : `blog/*.html`, `zones/*.html` dans le dépôt `wnd5ww6g5b-a11y/site-jbkt` ;
   - Gloova : `src/data/articles-auto.json` et les routes de `src/App.tsx` dans `wnd5ww6g5b-a11y/gloomy-site`.
3. Lire les vraies données Google de l'outil (document `seo/jbkt` ou `seo/gloova` de l'artifact
   `215e6505-5f68-4a59-8694-595b631af2eb`) s'il existe : viser en priorité une recherche entre la 5e et la 20e place.
4. Choisir un sujet qui N'A PAS encore de contenu (ni le même sujet, ni la même recherche visée).

## Règles de qualité (toutes obligatoires)

- Français, vouvoiement, phrases courtes, aucun jargon, ton de la fiche marque.
- **Rien d'inventé** : aucun chiffre, pourcentage, statistique, étude, prix, tarif, nombre de clients,
  témoignage, avis, nom de client ou projet réalisé.
- **Gloova** : ne décrire QUE des fonctions qui existent vraiment, telles qu'elles sont décrites
  sur les pages existantes du site (`src/pages/Home*.tsx`, `src/pages/seo/*.tsx`) ou dans la fiche marque.
  En cas de doute sur une fonction : ne pas en parler.
- **JBKT** : jamais de prix (« Nos tarifs sont sur devis, après une première visite. »), jamais de nom de client.
- **Infos locales (pages zone JBKT)** : seulement des faits vérifiés par une recherche web pendant le passage
  (ex. secteurs d'activité présents, zones d'activité, type de commerces), formulés simplement.
  Ne jamais dire que JBKT a des clients dans cette ville. Si rien de fiable n'est trouvé : pas de fait local,
  parler des besoins typiques des entreprises de cette taille de ville.
- **Unique** : chaque page doit avoir un vrai angle propre (besoins des entreprises de cette zone, exemples
  de métiers de la zone, déplacement ou visio). Interdit : reprendre une page existante en changeant juste le nom de la ville.
- Liens internes : seulement vers des pages qui existent (liste dans la fiche marque, articles déjà publiés).
- Longueur : article 700 à 1 000 mots ; page service/zone ou métier 500 à 800 mots.
- Titre 50 à 70 caractères avec la recherche visée ; description Google 140 à 160 caractères.
- Corps au format : `## ` sous-titres (4 à 6, formulés comme des questions que les gens se posent),
  paragraphes courts séparés par une ligne vide, listes `- ` ou `1. `, `**gras**`, liens `[texte](/page)`.
  Pas de titre principal dans le corps, pas de FAQ dans le corps (elle va dans `faq`, 3 ou 4 questions).
- Relire le texte en entier avant publication : orthographe, rien d'inventé, ton juste.

## Règles GEO : être cité par ChatGPT, Claude, Perplexity et les résumés IA de Google (toutes obligatoires)

Les assistants IA recopient des passages courts et précis. Chaque texte doit donc pouvoir être découpé
en morceaux qui se comprennent seuls.

- **Réponse d'abord** : le `lead` répond directement à la recherche visée en 2 phrases (40 à 60 mots),
  avec le nom de la marque et ce qu'elle fait. Exemple : « Un logiciel de suivi de production remplace
  le carnet papier au poste : chaque opérateur saisit sa production sur tablette… JBKT Solutions Digitales
  le conçoit sur mesure pour les ateliers d'Alsace. »
- **Chaque sous-titre `## ` est une question**, et le premier paragraphe dessous y répond en 1 ou 2 phrases
  complètes, compréhensibles sans le reste de la page (pas de « comme vu plus haut », pas de « cela » sans sujet).
- **Nommer les choses** : écrire « Gloova » ou « JBKT Solutions Digitales » plutôt que « nous » ou « l'outil »
  au moins une fois par section ; écrire le métier et la zone en toutes lettres (« les instituts de beauté de Lyon »).
- **Définitions et étapes** : quand c'est utile, une phrase « X, c'est… » et une liste numérotée d'étapes
  (`1. `), que les IA reprennent volontiers.
- **Un comparatif honnête** quand le sujet s'y prête (ex. « papier ou tablette », « site vitrine ou appli ») :
  une liste « avantages / limites » pour chaque option, sans dénigrer de concurrent par son nom.
- **FAQ** : questions telles qu'un client les taperait dans ChatGPT (« Combien de temps pour… ? »,
  « Est-ce que… ? »), réponses de 1 à 3 phrases qui contiennent le nom de la marque. Jamais de prix JBKT.
- **Faits datés et vérifiables seulement** : si un fait extérieur est utilisé (règle, obligation légale…),
  il vient d'une recherche web faite pendant le passage, et la source officielle est mise en lien.
  Sinon, pas de fait extérieur.
- Après publication, `llms.txt` et `llms-full.txt` se régénèrent seuls à la mise en ligne, et la nouvelle page
  est signalée à Bing (IndexNow) : rien à faire en plus.

## JBKT — pages « service + zone » (jeudi)

Services (page principale à mettre dans `service_path`) :
- Création de sites internet → `/creation-site-internet-strasbourg`
- Application sur mesure → `/creation-application-sur-mesure`
- Logiciel métier sur mesure → `/logiciel-metier-sur-mesure`
- Logiciel de suivi de production → `/logiciel-suivi-de-production`

Zones couvertes (décision de Karim) : Strasbourg et l'Eurométropole, tout le Bas-Rhin, le Haut-Rhin,
et toute la France à distance (visio). Sur place en Alsace, en visio ailleurs.

Ordre conseillé (une combinaison service + zone par semaine, en alternant les services) :
Eurométropole de Strasbourg (Schiltigheim, Illkirch-Graffenstaden, Bischheim, Lingolsheim) ; Haguenau ;
Colmar ; Mulhouse ; Sélestat ; Saverne ; Molsheim ; Obernai ; Brumath ; Bischwiller ; Erstein ;
Saint-Louis ; Wissembourg ; Guebwiller ; puis « France (à distance) » pour chaque service.
Choisir le service le plus pertinent pour la zone (ex. suivi de production pour un bassin industriel,
site internet pour une ville commerçante), en s'appuyant sur ce que la recherche web a vérifié.

Fichier `page.json` puis, dans le dépôt site-jbkt : `node scripts/ajouter-page.mjs page.json`
(champs : slug, title, description, service, service_path, zone, lead, body, faq, links).
Adresse : `https://www.jbktsolutionsdigitales.fr/zones/<slug>`.

## Gloova — pages « métier ou thème » (jeudi)

Thème propre à Gloova : les métiers de la beauté et ce que l'agenda change pour eux. Exemples, dans l'ordre :
onglerie / prothésiste ongulaire ; barbier ; salon de coiffure ; extension de cils ; esthéticienne à domicile ;
institut de massage ; épilation ; maquilleuse ; brow bar (sourcils) ;
puis thèmes : rappels de rendez-vous, fiche cliente, page de réservation à mettre en bio Instagram,
fermetures et congés, cartes cadeaux (seulement si la fonction existe sur le site).
Adresse courte et claire, ex. `agenda-en-ligne-onglerie`, `logiciel-rendez-vous-barbier`.
Ne pas reprendre une adresse qui existe déjà (le script refuse).

Fichier `article.json` avec `"type": "page"`, puis dans le dépôt gloomy-site :
`node scripts/ajouter-article.mjs article.json`. Adresse : `https://gloova.fr/<slug>`.

## Articles (lundi, les deux sites)

Comme `outil/ARTICLES.md` : JBKT → `node scripts/ajouter-article.mjs article.json` (dépôt site-jbkt),
Gloova → même commande sans `type` (dépôt gloomy-site). Catégories : voir la fiche marque.

## Publication

1. Écrire le JSON, lancer le script, vérifier le fichier créé.
   Gloova : `npm ci` puis `npm run build` doit réussir, sinon ne rien pousser.
2. `git add -A`, `git commit -m "<Article|Page> : <titre>"`, `git -c push.negotiate=true push origin main`.
3. Attendre ~3 min et vérifier que l'adresse répond 200.
4. Enregistrer dans l'outil (db_write `set`) un document `contents/auto-<AAAAMMJJ>-<marque>` :
   `{brand_id, channel: "article", status: "published", scheduled_at: maintenant (AAAA-MM-JJTHH:MM, heure de Paris),
   published_at: maintenant ISO, title, caption: description, visual: {bg: "nuit"}, seo_target, target_page,
   checks: ["Publié automatiquement", "Article" ou "Page service + zone" ou "Page métier"],
   article: {slug, description, category (ou le service), lead, body, faq, links}, published_url, validated_by: "Auto"}`.
5. Ajouter une ligne dans `outil/journal-contenu.md` : date, marque, type, titre, recherche visée, adresse. Commit et push.
6. En cas d'erreur : ne rien forcer, ne pas réessayer en boucle, le dire dans le résumé.
