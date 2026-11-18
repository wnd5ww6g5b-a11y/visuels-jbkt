# Bilan du lundi (décidé par Karim le 18/11/2026)

Chaque lundi vers 8 h 30, **un seul message** à Karim (notification), qu'il peut transférer à Julien.
Il résume la semaine passée (lundi → dimanche) pour les 3 marques, et donne les actions de la semaine.
Le même contenu va dans la page téléphone (`outil/MOBILE.md`, champs `chiffres.google`, `chiffres.inscriptions`,
`chiffres.top`, `actions`, `linkedin`).

## Sources

| Quoi | Où |
|---|---|
| Abonnés, portée, meilleures publications | base de l'outil (`insta/gloova`, `insta/jbkt`, `insta/radar` : `followers`, `posts`, `score`) |
| Clics et apparitions Google | base de l'outil `seo/jbkt`, `seo/gloova` (mis à jour le lundi 6 h 37 par la tâche SEO) |
| Inscriptions Gloova par source | Windsor.ai, connector `googleanalytics4` (si connecté) : sessions et conversions par `session_source` / `session_medium` / `session_campaign` sur 7 jours. Nos liens marqués : `utm_source=instagram`, `facebook`, `email`, `page-salon`, `confirmation-rdv`, `paid`. Si GA4 n'est pas connecté : l'écrire en une ligne, sans inventer. |
| Commentaires reçus et réponses | base de l'outil, collection `comments` (7 jours) |
| Ce qui est programmé | collection `contents` (7 prochains jours) |

## Le message (texte simple, lisible sur téléphone)

```
Bilan de la semaine du JJ/MM au JJ/MM

Abonnés Instagram : Gloova N (+x), JBKT N (+x), Radar VTC N (+x)
Google (28 j) : Gloova N clics / N apparitions · JBKT N clics / N apparitions
Inscriptions Gloova : N essais (Instagram x, e-mails x, pages salon x…)   ← seulement si GA4 est connecté

Ce qui a le mieux marché :
1. <marque> – <publication> : <chiffre réel>
2. …
3. …

Ce qu'on change cette semaine : 1 ou 2 phrases tirées des chiffres.

À faire (Karim / Julien) :
- …  (3 à 5 actions concrètes, les plus utiles d'abord : reels à tourner, vérifications, connexions manquantes)

LinkedIn : 2 posts prêts à copier sur la page téléphone (lien).
```

Règles : uniquement des vrais chiffres lus ; si une donnée manque, le dire ; pas de jargon ; pas de prix JBKT.

## Posts LinkedIn (JBKT)

Chaque lundi, **2 posts** pour les profils de Karim et de Julien (ou la page JBKT si LinkedIn est connecté dans Windsor :
alors on peut aussi publier sur la page, jamais sur un profil perso).
- Ton : un patron qui parle à d'autres patrons. Phrases courtes, « je » ou « on », pas de jargon, pas d'emoji en rafale.
- Sujets (alterner) : ce qu'on a construit cette semaine (démo, données fictives), une astuce Excel ou Google pour PME,
  une erreur qu'on voit souvent chez les PME, la méthode JBKT (démo gratuite, visite, maquette), un retour de terrain réel.
- 600 à 1 200 caractères, une première ligne qui accroche, une question à la fin. Au plus 3 hashtags.
- Rien d'inventé : aucun client nommé sans accord, aucun chiffre de résultat, jamais de prix.
- Les écrire dans `accueil/jour.linkedin` de la page téléphone : `[{"pour": "Karim", "texte": …}, {"pour": "Julien", "texte": …}]`.
