#!/usr/bin/env python3
"""Contrôle des « résultats enrichis » (données structurées JSON-LD), avec les règles publiées par Google.

Google n'ouvre pas son Rich Results Test aux outils : ce script applique les mêmes champs obligatoires et
recommandés, page par page, et donne pour chaque page le lien du test officiel pour confirmer.

  python3 outil/seo/donnees_structurees.py pages.json sortie.json
pages.json : [{"url": "https://…", "html": "chemin/vers/page.html"}, …]   (HTML rendu : fichier du site ou rawHtml Firecrawl)

Sortie : {"date", "pages": [{"url", "types", "statut": ok|avertissement|erreur|absent, "erreurs": [], "avertissements": [], "test_google"}],
          "resume": {"ok", "avertissement", "erreur", "absent"}}
"""
import json, re, sys, datetime, urllib.parse

RE_LD = re.compile(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', re.S | re.I)


def blocs(html):
    out, err = [], []
    for raw in RE_LD.findall(html):
        try:
            d = json.loads(raw.strip())
        except Exception as e:
            err.append(f"JSON-LD illisible ({str(e)[:60]})")
            continue
        items = d if isinstance(d, list) else [d]
        for it in items:
            if isinstance(it, dict) and '@graph' in it:
                items += it['@graph']
        out += [i for i in items if isinstance(i, dict)]
    return out, err


def types_of(o):
    t = o.get('@type', [])
    return t if isinstance(t, list) else [t]


def has(o, *path):
    cur = o
    for p in path:
        if isinstance(cur, list):
            cur = cur[0] if cur else None
        if not isinstance(cur, dict) or p not in cur or cur[p] in ('', None, [], {}):
            return False
        cur = cur[p]
    return True


def verifier(o):
    """Renvoie (erreurs, avertissements) pour un objet, selon le type (règles Google Search Central)."""
    e, w = [], []
    T = types_of(o)
    if 'FAQPage' in T:
        q = o.get('mainEntity') or []
        q = q if isinstance(q, list) else [q]
        if not q: e.append('FAQPage sans questions (mainEntity)')
        for i, x in enumerate(q, 1):
            if not has(x, 'name'): e.append(f'FAQ question {i} : texte de la question manquant (name)')
            if not has(x, 'acceptedAnswer', 'text'): e.append(f'FAQ question {i} : réponse manquante (acceptedAnswer.text)')
    if any(t in T for t in ('Article', 'BlogPosting', 'NewsArticle')):
        if not has(o, 'headline'): e.append('Article : titre manquant (headline)')
        for f, lab in (('image', 'image'), ('datePublished', 'date de publication'), ('author', 'auteur')):
            if not has(o, f): w.append(f'Article : {lab} recommandée ({f})')
        if not has(o, 'dateModified'): w.append('Article : date de mise à jour recommandée (dateModified)')
    if 'BreadcrumbList' in T:
        L = o.get('itemListElement') or []
        if not L: e.append("Fil d'Ariane vide (itemListElement)")
        for i, x in enumerate(L, 1):
            if not has(x, 'position') or not has(x, 'name'): e.append(f"Fil d'Ariane, élément {i} : position ou nom manquant")
    if 'SoftwareApplication' in T or 'MobileApplication' in T or 'WebApplication' in T:
        if not has(o, 'name'): e.append('Application : nom manquant (name)')
        if not (has(o, 'offers', 'price') or has(o, 'offers', 'lowPrice')): e.append('Application : prix manquant (offers.price, ou lowPrice pour plusieurs formules ; 0 si gratuit)')
        if has(o, 'offers') and not has(o, 'offers', 'priceCurrency'): w.append('Application : devise recommandée (offers.priceCurrency)')
        if not has(o, 'aggregateRating') and not has(o, 'review'):
            w.append("Application : pas d'étoiles possibles sans vrais avis (aggregateRating/review) : ne jamais en inventer")
        for f in ('applicationCategory', 'operatingSystem'):
            if not has(o, f): w.append(f'Application : {f} recommandé')
    if 'Product' in T:
        if not has(o, 'name'): e.append('Produit : nom manquant')
        if not has(o, 'offers') and not has(o, 'review') and not has(o, 'aggregateRating'):
            e.append('Produit : il faut une offre (offers) ou de vrais avis')
    if any(t in T for t in ('Organization', 'ProfessionalService', 'LocalBusiness', 'BeautySalon', 'HealthAndBeautyBusiness')):
        if not has(o, 'name'): e.append('Organisation : nom manquant')
        if not has(o, 'url'): w.append('Organisation : adresse du site recommandée (url)')
        if not has(o, 'logo') and 'Organization' in T: w.append('Organisation : logo recommandé (logo)')
        if any(t in T for t in ('LocalBusiness', 'ProfessionalService', 'BeautySalon')) and not has(o, 'address'):
            w.append('Entreprise locale : adresse recommandée (address)')
    if 'Event' in T:
        for f in ('name', 'startDate', 'location'):
            if not has(o, f): e.append(f'Événement : {f} manquant')
    return e, w


def main():
    pages = json.load(open(sys.argv[1], encoding='utf-8'))
    res = []
    for p in pages:
        html = open(p['html'], encoding='utf-8', errors='ignore').read()
        objs, err = blocs(html)
        e, w = list(err), []
        for o in objs:
            a, b = verifier(o); e += a; w += b
        types = sorted({t for o in objs for t in types_of(o) if t})
        statut = 'absent' if not objs and not err else ('erreur' if e else ('avertissement' if w else 'ok'))
        res.append({'url': p['url'], 'types': types, 'statut': statut, 'erreurs': sorted(set(e)), 'avertissements': sorted(set(w)),
                    'test_google': 'https://search.google.com/test/rich-results?url=' + urllib.parse.quote(p['url'], safe='')})
    resume = {k: sum(1 for r in res if r['statut'] == k) for k in ('ok', 'avertissement', 'erreur', 'absent')}
    json.dump({'date': datetime.date.today().isoformat(), 'pages': res, 'resume': resume}, open(sys.argv[2], 'w'), ensure_ascii=False, indent=1)
    print(resume)


if __name__ == '__main__':
    main()
