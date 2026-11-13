# Engagement Instagram : Radar VTC et JBKT (1 post + 1 reel par jour)

Décidé par Karim le 13/11/2026 :
- chaque marque publie **1 post et 1 reel par jour** ;
- tout est préparé **une fois par semaine, le dimanche**, pour la semaine suivante (lundi → dimanche) ;
- Karim valide le lot dans l'outil (page « À valider », bouton « Tout valider ») : rien ne part sans validation ;
- les réponses aux commentaires sont proposées par l'outil et **validées par Karim** (voir PUBLIER.md, partie D).

Base de l'outil : artifact `215e6505-5f68-4a59-8694-595b631af2eb`, collection `contents`.

## Horaires (heure de Paris)

| Marque | Post | Reel (+ story de la même vidéo) |
|---|---|---|
| radar | 07:30 | 18:30 |
| jbkt | 08:30 | 12:30 |

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
Ne jamais mettre `validated_at` : c'est Karim qui valide.

## Légendes

- Première ligne = la question ou l'accroche (c'est ce qu'on lit avant « plus »).
- Puis 1 à 3 phrases utiles, puis l'appel à réagir (« Réponds en commentaire », « Enregistre ce post », « Tag un collègue chauffeur »).
- Radar : tutoiement (entre chauffeurs), finir par « Essai gratuit 7 jours sur l’App Store » une fois sur deux. JBKT : vouvoiement, finir par « Démo gratuite de 30 minutes : lien en bio » une fois sur deux.
- 3 à 5 hashtags de la liste de la marque (PUBLIER.md). Radar : jamais de hashtag local.

## Étapes de la tâche du dimanche

1. `git pull`. Lire ce fichier, `outil/videos/REELS.md`, `outil/marques/radar.md`, `outil/marques/jbkt.md` et `outil/journal-engagement.md` (sujets déjà faits : ne pas les répéter avant 6 semaines).
2. Lire `contents` (db_query) : repérer les reels déjà programmés la semaine suivante pour radar et jbkt.
3. Écrire les 14 posts et les reels manquants (suivre la semaine type).
4. Rendre chaque reel (`reel.py`, voir REELS.md) dans `videos/AAAA/MM/<id>.mp4` ; regarder des images de contrôle avant ;
   une fois tous rendus : `git add`, `git commit`, `git push`, attendre 20 s, vérifier chaque adresse raw (200).
5. Créer les documents (db_write `set`, 10 par appel au plus, attendre 2 s entre les appels).
6. Ajouter les sujets de la semaine à `outil/journal-engagement.md` (date, marque, format, sujet), commit et push.
7. Résumer : nombre de posts et de reels préparés, à valider dans l'outil.
