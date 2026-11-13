# Test GEO de la semaine (JBKT et Gloova)

Décidé par Karim le 13/11/2026 : chaque lundi, l'outil mesure si les IA citent JBKT et Gloova sur les questions des clients,
puis oriente les contenus automatiques de la semaine vers les questions où la marque est absente.
On ne publie pas plus : on publie mieux ciblé.

Base de l'outil : artifact `215e6505-5f68-4a59-8694-595b631af2eb`, document `geo/<marque>` (marque = `jbkt` ou `gloova`).
Questions : `outil/geo/questions.json` (ne pas les changer d'une semaine à l'autre : c'est ce qui rend l'évolution lisible ;
on peut en ajouter, jamais en retirer sans l'accord de Karim).

## 1. Poser chaque question

Pour chaque question de chaque marque :
1. Lancer une recherche web (WebSearch, mode `standard`) avec la question telle qu'elle est écrite.
2. Lire les résultats comme un assistant IA qui doit répondre au client, et noter :
   - `cite` : une page du site de la marque (`site` dans questions.json) fait partie des résultats ;
     noter l'adresse de la page dans `page` ;
   - `mention` : le site n'apparaît pas, mais la marque est nommée dans un résultat d'un autre site (annuaire, comparatif, article) ;
   - `absent` : ni l'un ni l'autre.
3. `others` : les 3 à 5 entreprises, logiciels ou sites qui ressortent à la place (noms courts, ex. « Planity », « Booksy »,
   « agence X »). Ne pas mettre de sites génériques (Wikipédia, Pages Jaunes) sauf s'ils répondent vraiment.
4. Ne rien deviner : uniquement ce que montrent les résultats de la recherche.

## 2. Choisir les sujets prioritaires

Par marque, marquer `priority: true` sur **2 questions** au plus, parmi les `absent` (sinon les `mention`) :
- celles qu'un contenu du site peut vraiment couvrir sans rien inventer (pas de prix JBKT, pas de fonction Gloova qui n'existe pas) ;
- pas une question déjà choisie lors des 3 semaines précédentes (voir `outil/geo/priorites.md`), sauf si plus aucune autre n'est possible.

Écrire ensuite `outil/geo/priorites.md` (remplacer le fichier) :
```
# Priorités GEO de la semaine du <lundi>
## jbkt
1. « <question> » : absent · cités à la place : … · angle conseillé : <ce que la page doit répondre, en une phrase>
2. …
## gloova
…
## Historique
- <lundi> · jbkt : « … », « … » · gloova : « … », « … »
(garder les 8 dernières semaines)
```
Ces priorités sont lues par la tâche « Contenu SEO automatique » (outil/CONTENU-AUTO.md) le lundi et le jeudi.

## 3. Enregistrer dans l'outil

1. Lire `geo/<marque>` (db_get) pour garder `history` et `refreshed`.
2. Écrire (db_write `set`) :
```json
{
  "brand_id": "jbkt",
  "updated_at": "<maintenant, ISO>",
  "engine": "Claude avec recherche web",
  "questions": [{"q": "…", "result": "absent", "page": "…", "others": ["…"], "priority": true}],
  "history": [{"date": "AAAA-MM-JJ", "cite": 2, "mention": 1, "total": 12}],
  "notes": ["1 ou 2 phrases simples : ce qui a changé depuis la semaine dernière et ce que les contenus de la semaine vont viser."],
  "refreshed": [/* conservé tel quel */]
}
```
`history` : ajouter la ligne du jour à la fin, garder les 26 dernières.
3. Commit et push de `outil/geo/priorites.md`.
4. Résumé court : score par marque (cité ou nommé / total), et les 2 sujets prioritaires de chaque marque.
