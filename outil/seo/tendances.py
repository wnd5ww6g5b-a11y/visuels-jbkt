#!/usr/bin/env python3
"""Résume les données Google Trends (Firecrawl, fournisseur firecrawl-trends) pour la page SEO de l'outil.

  python3 outil/seo/tendances.py resultat_firecrawl.json plan.json sortie_dir/
plan.json : {"gloova": {"courbes": [0], "associees": [3]}, "jbkt": {...}, "radar": {...}}
            (index des appels dans data.alexandria : interest_over_time puis related_queries)

Pour chaque marque, écrit sortie_dir/<marque>.json :
{ "date", "geo", "mots": [{"mot", "mois_forts": ["décembre", ...], "mois_faibles": [...], "evolution": "+12 %"|..., "maintenant": 0-100}],
  "en_hausse": [{"requete", "valeur"}], "populaires": [{"requete", "valeur"}], "conseil": [phrases simples] }
Rien n'est inventé : uniquement les chiffres renvoyés par Google Trends.
"""
import json, sys, os, datetime, statistics as st

MOIS = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']


def courbe(data):
    kws = data['keywords']; pts = [p for p in data['points'] if not p.get('partial')]
    out = []
    for k, kw in enumerate(kws):
        par_mois = {m: [] for m in range(12)}
        for p in pts:
            m = int(p['time'][5:7]) - 1
            par_mois[m].append(p['values'][k])
        moy = {m: (st.mean(v) if v else 0) for m, v in par_mois.items()}
        tot = st.mean(moy.values()) or 1
        fort = [MOIS[m] for m, v in sorted(moy.items(), key=lambda x: -x[1]) if v >= tot * 1.15][:3]
        faible = [MOIS[m] for m, v in sorted(moy.items(), key=lambda x: x[1]) if v <= tot * 0.85][:3]
        # évolution : 52 dernières semaines vs les 52 précédentes
        vals = [p['values'][k] for p in pts]
        evo = None
        if len(vals) >= 104 and sum(vals[-104:-52]) > 0:
            evo = round((sum(vals[-52:]) / sum(vals[-104:-52]) - 1) * 100)
        if vals and st.mean(vals) < 3:  # trop peu cherché pour en tirer une saison ou une évolution fiable
            fort, faible, evo = [], [], None
        if vals and st.mean(vals) < 8:  # évolution sur un an peu fiable pour une recherche rare
            evo = None
        out.append({'mot': kw, 'mois_forts': fort, 'mois_faibles': faible,
                    'evolution': (f'{evo:+d} %' if evo is not None else None), 'maintenant': vals[-1] if vals else 0,
                    'moyenne': round(st.mean(vals), 1) if vals else 0})
    return out


import re
BANNIS = re.compile(r'(\.(fr|com|net|org)\b|www|mort|décès|deces|accident|agression|tué|tue |viol|meurtre|drame|procès|proces|arrêt|arret|police|gendarm)', re.I)


def associees(data):
    racine = (data.get('keyword') or '').lower().split()[0] if data.get('keyword') else ''
    def lst(key):
        out = []
        for x in (data.get(key) or []):
            q = (x.get('query') or '').strip()
            # on garde seulement les recherches liées au mot de départ, sans site web ni fait divers
            if not q or BANNIS.search(q) or (racine and racine[:5] not in q.lower()):
                continue
            out.append({'requete': q, 'valeur': x.get('formatted_value') or x.get('value')})
        return out[:10]
    return lst('top'), lst('rising')


def main():
    raw = json.load(open(sys.argv[1])); plan = json.load(open(sys.argv[2])); outd = sys.argv[3]
    calls = raw['data']['alexandria']
    os.makedirs(outd, exist_ok=True)
    for marque, P in plan.items():
        mots, top, rising = [], [], []
        for i in P.get('courbes', []):
            c = calls[i]
            if c.get('data') and c['data'].get('points'): mots += courbe(c['data'])
        for i in P.get('associees', []):
            c = calls[i]
            if c.get('data'):
                d = c['data']
                if 'top' not in d and 'records' in c:  # forme alternative
                    d = d
                t, r = associees(d); top += t; rising += r
        conseil = []
        ajd = datetime.date.today().month - 1
        for m in mots:
            if m['mois_forts'] and m['moyenne'] >= 5:
                idx = [MOIS.index(x) for x in m['mois_forts']]
                prochain = min(((i - ajd) % 12, i) for i in idx)
                if prochain[0] <= 2:
                    conseil.append(f"« {m['mot']} » est très cherché en {MOIS[prochain[1]]} : publier sur ce sujet dans les prochaines semaines.")
        json.dump({'date': datetime.date.today().isoformat(), 'geo': 'France', 'periode': '5 dernières années (saisons), 12 derniers mois (requêtes)',
                   'mots': mots, 'populaires': top, 'en_hausse': rising, 'conseil': conseil[:4]},
                  open(os.path.join(outd, f'{marque}.json'), 'w'), ensure_ascii=False, indent=1)
        print(marque, len(mots), 'mots', len(top), 'populaires', len(rising), 'en hausse', conseil[:2])


if __name__ == '__main__':
    main()
