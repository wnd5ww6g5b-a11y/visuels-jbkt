# Un réseau, une façon de publier (décidé par Karim le 17/11/2026)

> « Ce sont des réseaux sociaux différents, on ne poste pas pareil. » On ne recopie jamais un post Instagram tel quel
> sur Facebook ou TikTok. Chaque réseau a ses propres publications, écrites pour lui.

## Instagram (déjà en place)
Visuel d'abord : reels, carrousels, stories. Appel « enregistre / partage », « écris X en commentaire » (message privé
automatique), lien en bio. Voir `ENGAGEMENT.md`.

## Facebook
**Qui est là** : un public un peu plus âgé, qui lit. Pros de la beauté de 25 à 55 ans (Gloova), patrons de PME, artisans
et commerçants (JBKT), chauffeurs VTC très actifs en groupes (Radar). On y cherche des infos utiles et on discute.

**Ce qui marche** :
1. **Texte qui raconte ou qui questionne**, sans image ou avec une seule image. Les 2 premières lignes font tout
   (le reste est caché derrière « Afficher la suite ») : une situation vécue ou une vraie question.
2. **Partage d'un article du site** avec l'aperçu du lien : 3 à 5 lignes qui donnent envie, la question de l'article,
   puis le lien. Facebook laisse cliquer les liens : c'est le réseau qui ramène le plus de visites sur les sites.
3. **Une seule image** (1080 × 1350 ou 1200 × 1200), jamais un carrousel : Facebook n'en affiche que la 1re image
   avec notre outil. Un contenu en carrousel sur Instagram devient sur Facebook soit **un texte complet**
   (ex. les 5 messages écrits en entier, à copier-coller), soit **une seule image résumé**.
4. **Questions à réponse facile** (A ou B, « en un mot », « vous faites comment ? ») pour lancer les commentaires.

**À éviter** : « lien en bio », « écrivez GLOOVA en commentaire » (pas de message privé automatique ici), plus de
2 hashtags, les textes collés depuis Instagram, poster la même chose le même jour sur les deux réseaux.

**Rythme** : 3 publications par semaine et par marque, à des heures où on lit : 12 h 30 ou 19 h 30
(samedi et dimanche : 10 h ou 19 h 30). Pas de story Facebook pour l'instant.

**Vidéos** : notre outil ne peut pas publier de vidéo sur Facebook. Les reels passent par le partage automatique
Instagram vers Facebook, si Karim l'active dans les réglages de chaque compte Instagram.

**Groupes Facebook** : le plus gros levier (groupes d'esthéticiennes, de chauffeurs VTC, d'entrepreneurs d'Alsace).
Seulement Karim ou Julien, à la main, en apportant de l'aide d'abord, en respectant les règles de chaque groupe.
L'outil peut préparer des idées de réponses, jamais poster dans un groupe.

**Règles de chaque marque** : identiques à Instagram (Gloova : prix TTC, « sans commission sur vos rendez-vous »,
validation de Karim ; Radar : aucune plateforme, aucun lieu, aucune promesse de gains, calculs justes ;
JBKT : jamais de prix, démos « données fictives »).

## Documents dans l'outil (collection `contents`)
`channel` = `"facebook"`, `brand_id`, `format` = `"texte"` | `"lien"` | `"image"`, `caption` (le texte complet),
`link` (format lien, ou en plus d'un texte), `image_url` (format image), `scheduled_at`, `status`
(`scheduled` pour JBKT et Radar ; `to_validate` pour Gloova tant que Karim n'a pas validé), `validated_by`.
Publication : `outil/PUBLIER.md`, partie « Facebook ».

## TikTok (bientôt)
Vidéo verticale seulement, 7 à 20 secondes, accroche dans la 1re seconde, ton direct et spontané, sous-titres,
sons du moment quand c'est possible. On ne recopie pas les reels : on les recoupe plus court et plus « brut »,
ou on tourne exprès. Rythme visé : 1 vidéo par jour quand le compte sera branché.
