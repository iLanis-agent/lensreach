#!/usr/bin/env python3
# Lens Reach oracle - mirrors engine.js with Fractions: every answer is a ratio of the entered numbers (the lens frames a subject in proportion to sensor over focal length), rounding is Decimal half-up.
import json, re, random
from fractions import Fraction as F
from decimal import Decimal, ROUND_HALF_UP

SW = "the sensor width must be from 1 to 60 mm with at most one decimal place"
SH = "the sensor height must be from 1 to 60 mm with at most one decimal place"
FL = "the focal length must be from 1 to 1200 mm with at most one decimal place"
D = "the distance must be from 0.1 to 1000 m with at most one decimal place"
W = "the subject width must be from 0.1 to 1000 m with at most one decimal place"
def dec(t, err, lo, hi):
    t = t.strip() if isinstance(t, str) else ""
    if not re.fullmatch(r"[0-9]{1,4}(\.[0-9])?", t) or not F(lo) <= F(t) <= F(hi): raise ValueError(err)
    return F(t)
def txt(fr, places):
    v = int((Decimal(fr.numerator) / Decimal(fr.denominator) * (10 ** places)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
    ip, fp = divmod(v, 10 ** places); fs = str(fp).zfill(places).rstrip("0")
    return f"{ip}.{fs}" if fs else str(ip)
def metres(fr):
    s = txt(fr, 2)
    return "under 0.01 m" if s == "0" else s + " m"

def equiv(sw, f):
    S = dec(sw, SW, "1", "60"); L = dec(f, FL, "1", "1200")
    return f"A {txt(L,1)} mm lens on a sensor {txt(S,1)} mm wide frames like {txt(L * 36 / S,1)} mm on a 36 mm wide full frame sensor, a crop factor of {txt(F(36) / S,2)} by width."
def cover(sw, sh, f, d):
    S = dec(sw, SW, "1", "60"); H = dec(sh, SH, "1", "60"); L = dec(f, FL, "1", "1200"); X = dec(d, D, "0.1", "1000")
    return f"At {txt(X,1)} m, a {txt(L,1)} mm lens on a {txt(S,1)} by {txt(H,1)} mm sensor covers {metres(X * S / L)} wide by {metres(X * H / L)} high."
def distance(sw, f, w):
    S = dec(sw, SW, "1", "60"); L = dec(f, FL, "1", "1200"); U = dec(w, W, "0.1", "1000")
    return f"To fit a {txt(U,1)} m wide subject across a {txt(S,1)} mm wide sensor with a {txt(L,1)} mm lens, stand {metres(U * L / S)} away."

FNS = {"equivTruth": equiv, "coverTruth": cover, "distanceTruth": distance}
def cases():
    c = []
    sws = ["1", "6.2", "13.2", "23.5", "36", "60"]; fs = ["1", "8.5", "24", "50", "200", "1200"]
    for s in sws:
        for f in fs: c.append(("equivTruth", [s, f]))
    for s, h in [("23.5", "15.6"), ("36", "24"), ("1", "1"), ("60", "60"), ("6.2", "4.6")]:
        for f in ["1", "24", "50", "1200"]:
            for d in ["0.1", "3", "10", "1000"]:
                c.append(("coverTruth", [s, h, f, d]))
    for s in ["1", "23.5", "36", "60"]:
        for f in ["1", "24", "50", "1200"]:
            for w in ["0.1", "3", "1000"]:
                c.append(("distanceTruth", [s, f, w]))
    for t in [(" 23.5 ", " 50 "), ("23.50", "50.0")]:
        c += [("equivTruth", list(t)), ("coverTruth", [t[0], " 15.6 ", t[1], " 10 "]), ("distanceTruth", [t[0], t[1], " 3 "])]
    bad = ["", "x", "0", "0.0", "0.05", "1.25", "-1", ".5", "5.", "1e2", "12345", "99999"]
    for v in bad:
        c += [("equivTruth", [v, "50"]), ("equivTruth", ["23.5", v]), ("coverTruth", ["23.5", v, "50", "10"]), ("coverTruth", ["23.5", "15.6", "50", v]),
              ("distanceTruth", ["23.5", "50", v])]
    for t in [("60.1", "50"), ("23.5", "1200.1"), ("23.5", "0.9"), ("0.9", "50")]: c.append(("equivTruth", list(t)))
    for t in [("23.5", "15.6", "50", "1000.1"), ("23.5", "60.1", "50", "10"), ("23.5", "15.6", "50", "0.09")]: c.append(("coverTruth", list(t)))
    c.append(("distanceTruth", ["23.5", "50", "1000.1"]))
    r = random.Random(713)
    for _ in range(8):
        s = f"{r.randint(1, 59)}.{r.randint(0, 9)}"; h = f"{r.randint(1, 59)}.{r.randint(0, 9)}"; f = f"{r.randint(1, 1199)}.{r.randint(0, 9)}"
        d = f"{r.randint(0, 999)}.{r.randint(0, 9)}"; d = "0.1" if d == "0.0" else d
        c += [("equivTruth", [s, f]), ("coverTruth", [s, h, f, d]), ("distanceTruth", [s, f, d])]
    return c
out = []
for fn, args in cases():
    try: exp = FNS[fn](*args)
    except ValueError as e: exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
with open("expected.json", "w") as f:
    f.write("[\n" + ",\n".join(json.dumps(o, separators=(",", ":"), ensure_ascii=False) for o in out) + "\n]\n")
print(len(out), "cases written")
