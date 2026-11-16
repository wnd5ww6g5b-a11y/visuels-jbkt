# Relevé quotidien « Croissance Instagram » pour l'outil marketing.
#   python3 outil/insta/releve.py <posts.json> <abonnes.json> <ancien-dir> <sortie-dir>
# posts.json   : lignes Windsor (account_name, date, media_type, media_reach, media_saved, media_shares,
#                media_like_count, media_comments_count, media_permalink, media_caption), 30 derniers jours
# abonnes.json : [{account_name, followers_count}] du jour
# ancien-dir   : docs insta/<marque> actuels (json), pour garder l'historique des abonnés, scripts et liste 15 min
# Écrit <sortie-dir>/<marque>.json, prêt pour db_write insta/<marque>.
import json, sys, os, datetime
BR = {'gloova_beauty': 'gloova', 'jbktsolutionsdigitales': 'jbkt', 'radar_vtc': 'radar'}
posts, foll, old_dir, out = json.load(open(sys.argv[1])), json.load(open(sys.argv[2])), sys.argv[3], sys.argv[4]
today = datetime.date.today().isoformat()
os.makedirs(out, exist_ok=True)
for acc, bid in BR.items():
    old = {}
    p = os.path.join(old_dir, f'{bid}.json')
    if os.path.exists(p): old = json.load(open(p))
    rows = [r for r in posts if r['account_name'] == acc]
    ps = []
    for r in rows:
        g = lambda k: int(r.get(k) or 0)
        cap = (r.get('media_caption') or '').split('\n')[0][:90]
        reach, sv, sh, cm = g('media_reach'), g('media_saved'), g('media_shares'), g('media_comments_count')
        ps.append({'date': r['date'], 'type': r['media_type'], 'caption': cap, 'permalink': r.get('media_permalink'),
                   'reach': reach, 'saved': sv, 'shares': sh, 'likes': g('media_like_count'), 'comments': cm,
                   'score': reach + 10 * (sv + sh) + 3 * cm})
    fmt = {}
    for x in ps:
        t = 'REELS' if x['type'] in ('REELS', 'VIDEO') else x['type']
        f = fmt.setdefault(t, {'type': t, 'posts': 0, 'reach': 0, 'saved': 0, 'shares': 0})
        f['posts'] += 1; f['reach'] += x['reach']; f['saved'] += x['saved']; f['shares'] += x['shares']
    hist = [h for h in old.get('followers', []) if h['date'] != today]
    n = next((int(f['followers_count']) for f in foll if f['account_name'] == acc), None)
    if n is not None: hist.append({'date': today, 'n': n})
    doc = {'brand_id': bid, 'account': acc, 'updated_at': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S+00:00'),
           'followers': hist[-120:], 'posts': ps, 'formats': sorted(fmt.values(), key=lambda f: -f['reach'] / max(f['posts'], 1)),
           'notes': old.get('notes', [])}
    for k in ('scripts', 'engage'):
        if k in old: doc[k] = old[k]
    json.dump(doc, open(os.path.join(out, f'{bid}.json'), 'w'), ensure_ascii=False)
    print(bid, n, len(ps))
