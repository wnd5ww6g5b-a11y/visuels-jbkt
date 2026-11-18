# Page téléphone de l'outil (créée le 18/11/2026, demande de Karim)

L'outil complet (artifact `215e6505-5f68-4a59-8694-595b631af2eb`) est trop lourd pour l'iPhone de Karim.
Une petite page à part le résume : **artifact `81a4c9c9-9357-402e-92ec-2e86ddba3df6`**
(https://claude.ai/artifact/H1X8fxo3YXM5EQwCme27Qq). Code : ce fichier ne le contient pas, la page est publiée telle quelle ;
elle ne fait que lire **un seul document** de SA base : `accueil/jour`.

La page n'écrit rien. Ce sont les tâches programmées qui remplissent `accueil/jour`
(db_get pour la version, puis db_write « set » avec ifVersion, ou « merge » pour ne changer que quelques champs).

## Le document `accueil/jour`

```json
{
  "maj": "2026-11-18T10:05",                       // heure de Paris, AAAA-MM-JJTHH:MM
  "a_commenter": {
    "date": "2026-11-18",
    "gloova": [ {"compte", "post_url", "post_sujet", "post_date": "JJ/MM", "commentaire"} ],
    "jbkt":   [ ... ],
    "radar":  [ ... ]
  },
  "a_venir": [ {"quand": "AAAA-MM-JJTHH:MM", "marque": "gloova|jbkt|radar", "reseau": "instagram|facebook|linkedin|site", "titre"} ],
  "reponses": [ {"marque", "auteur", "texte", "reponse", "sensible": true|false, "statut": "replied|karim"} ],
  "chiffres": {
    "abonnes": {"gloova": {"n", "semaine"}, "jbkt": {...}, "radar": {...}},   // semaine = gain sur 7 jours
    "google":  {"gloova": {"clics", "apparitions"}, "jbkt": {...}},            // 28 derniers jours (bilan du lundi)
    "inscriptions": {"total", "par_source": [{"source", "n"}]},              // Google Analytics, si connecté
    "top": [ {"marque", "titre", "detail"} ]                                  // 3 meilleures publications de la semaine
  },
  "actions": [ "phrase courte", ... ],                                         // à faire par Karim / Julien
  "linkedin": [ {"pour": "Karim|Julien|page JBKT", "texte"} ]                  // posts de la semaine, prêts à copier
}
```

## Qui remplit quoi

| Tâche | Champs |
|---|---|
| Relevé Instagram (chaque matin, 9 h 41) | `maj`, `a_commenter`, `a_venir` (publications Instagram et Facebook des 3 prochains jours, **sans les stories**, contenus `scheduled` de la collection `contents` de l'outil), `reponses` (collection `comments` de l'outil, 7 derniers jours, au plus 15), `chiffres.abonnes`. Garder les autres champs (merge). |
| Bilan du lundi (8 h 23) | `chiffres.google`, `chiffres.inscriptions`, `chiffres.top`, `actions`, `linkedin`. Garder les autres champs (merge). |

Règles : rien d'inventé ; textes courts ; jamais de donnée personnelle d'une cliente Gloova ; pas de prix JBKT.
