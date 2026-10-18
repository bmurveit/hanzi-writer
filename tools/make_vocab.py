"""
Rebuilds tools/hsk_vocab.json from complete.json in
github.com/drkameleon/complete-hsk-vocabulary (MIT license). You only need this
if that list is updated.
    python3 tools/make_vocab.py path/to/complete.json tools/hsk_vocab.json
Words with several readings: surname-only, variant and archaic readings are
skipped, and up to two real readings are kept ("háng / xíng").
"""
import json, re, sys
SKIP = re.compile(r"^(surname|variant of|old variant|unofficial variant|\(archaic\)|archaic|used in|see )", re.I)
def good(f):
    p = f["transcriptions"]["pinyin"]
    return not p[:1].isupper() and not all(SKIP.match(m) for m in f["meanings"])
d = json.load(open(sys.argv[1]))
out = {}
for e in d:
    ls = [int(l.split("-")[1]) for l in e["level"] if l.startswith("new-")]
    w = e["simplified"]
    if w in out and (not ls or (out[w]["l"] or 99) <= min(ls)): continue
    forms = [f for f in e["forms"] if good(f)] or e["forms"]   # all names (北京)? keep them
    readings, meanings = [], []
    for f in forms:
        p = f["transcriptions"]["pinyin"]
        if p.lower() in [r.lower() for r in readings]: continue
        ms = [m for m in f["meanings"] if not SKIP.match(m)] or f["meanings"]
        readings.append(p); meanings.append("; ".join(ms[:2] if not meanings else ms[:1]))
        if len(readings) == 2: break
    out[w] = {"l": min(ls) if ls else None, "f": e["frequency"],
              "p": " / ".join(readings), "m": " / ".join(meanings), "t": e["pos"]}
json.dump(out, open(sys.argv[2], "w"), ensure_ascii=False, separators=(",", ":"))
