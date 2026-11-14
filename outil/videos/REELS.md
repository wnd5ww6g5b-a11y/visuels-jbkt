# Fabriquer un reel (JBKT et Radar VTC)

Le style est celui des pubs Gloova, validé par Karim : le texte apparaît mot par mot, les téléphones entrent et sortent,
on passe d'un fond à l'autre, une liste se construit, et la fin montre le logo et un bouton. Durée : 16 à 19 s, en 1080 × 1920, avec musique.

## Commande

```
python3 outil/videos/reel.py fiche.json videos/AAAA/MM/<id>.mp4 --musique clair --apercus apercus.json
```
- `--musique` : `clair` (posé), `calme` (doux), `elan` (rythmé). Les 3 morceaux sont des créations originales libres de droits. Varier d'un jour à l'autre.
- `--apercus` : écrit 1 petite image (data URI) à copier dans le champ `apercus` du document, pour l'aperçu dans l'outil.
- Environ 35 s de rendu par reel. Chrome et Playwright sont déjà installés.
- Avant de rendre la vidéo complète, regarder 2 ou 3 images de contrôle :
  `python3 -c "import sys,json;sys.path.insert(0,'outil/videos');import anim;v=json.load(open('fiche.json'));print(anim.render(v,[2.0,7.0,12.0]))"`
  puis ouvrir les JPEG produits (Read) : rien de coupé, texte lisible.

## La fiche (JSON)

Voir `exemple-radar.json` et `exemple-jbkt.json`. Champs :

| Champ | Contenu |
|---|---|
| `id` | identifiant court, sans espace (ex. `radar-verdict-1611`) |
| `brand` | `radar` ou `jbkt` |
| `hook.lines` | l'accroche, 2 lignes max, `<br>` pour couper (4 à 6 mots par ligne) |
| `hook.kicker` | (option) petit texte au-dessus |
| `hook.card` | (option) `["PETIT TITRE", "texte"]` : une carte qui apparaît puis s'efface |
| `hook.note` | (option) une pastille, ex. `"Nouvelle course · 14,60 €"` |
| `hook.acc` | (option) 2e phrase en couleur, 2 lignes max |
| `phones` | 1 ou 2 téléphones : `kicker`, `title` (2 lignes max), `screen` |
| `list.title` + `list.items` | 3 points courts (4 mots max chacun) |
| `end.tagline` | phrase de fin (2 lignes max) |
| `end.button` | JBKT : `"Démo gratuite de 30 min"` · Radar : `"Essai gratuit sur l’App Store  →"` |
| `end.small` | JBKT : `"jbktsolutionsdigitales.fr"` · Radar : `"7 jours offerts · sans engagement"` |

Pour un reel d'engagement, la fin pose la question : par exemple `tagline` = `"Et toi, tu l’aurais prise ?"`,
`small` = `"Réponds en commentaire"`.

### Écrans des téléphones (`screen`)

- **Ne plus utiliser les captures réelles de Radar VTC** (`radar-offre.jpg`, `radar-historique.jpg`, `radar-zones.jpg`) :
  elles montrent des noms de plateformes et des lieux de Strasbourg. Dessiner l'écran en HTML (ci-dessous), avec des montants d'exemple et des zones « Zone A, B… ».
- Site JBKT sur mobile : `<img src="A/site-jbkt-mobile.jpg">`.
- Écran dessiné en HTML (pour une maquette d'appli JBKT, ou un calcul Radar) :
  ```html
  <div class="ui"><div class="sb">9:41</div><p class="t">Titre</p><p class="st">Sous-titre</p>
    <div class="row"><span>Ligne<small>détail</small></span><span class="chip c-g">OK</span></div>
    ...</div>
  ```
  Pastilles : `c-b` bleu, `c-g` vert, `c-o` orange, `c-v` violet. 4 à 5 lignes max.
  Formulaire : `<div class="field"><b>Libellé</b>valeur</div>` et bouton `<div class="btnp" style="background:#087BFF">Envoyer</div>`.

## Règles

- Rien d'inventé : pas de chiffre de résultat, pas d'avis, pas de nom de client.
- Radar VTC : aucune promesse de gains ; pas de logo ni de nom de plateforme (Uber, Bolt, Heetch…) ; pas de lieu précis (toute la France).
  Les montants d'une offre d'exemple sont présentés comme un exemple, et les calculs doivent être justes
  (€/km = prix ÷ km de la course ; €/h = prix ÷ (minutes de course + minutes d'approche) × 60).
- JBKT : on parle aux patrons de TPE et de PME ; pas de prix ; signature « Démo gratuite de 30 min ».
