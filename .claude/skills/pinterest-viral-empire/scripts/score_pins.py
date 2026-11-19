#!/usr/bin/env python3
"""Rank observed Pinterest pins by velocity and outlier strength.

Usage: python3 score_pins.py pins.csv [--top 15] [--json]

CSV header: url,creator,followers,saves,comments,age_days,format,archetype,keyword,notes
Blank numeric cells are allowed; the score uses whatever is present.

Scoring (0-100, relative within the file):
  engagement = saves + 3*comments            (comments signal deeper intent)
  velocity   = engagement / max(age_days, 1) (fresh wins rank higher)
  outlier    = engagement / max(followers, 100)  (small-account wins = format proof)
  score      = 50% velocity rank + 35% outlier rank + 15% raw engagement rank
"""
import argparse
import csv
import json
import sys


def num(v):
    try:
        return float(str(v).replace(",", "").strip())
    except (TypeError, ValueError):
        return None


def pct_rank(values):
    """Percentile rank (0-1) for each value; None stays None."""
    present = sorted(v for v in values if v is not None)
    if not present:
        return [None] * len(values)
    n = len(present)
    out = []
    for v in values:
        if v is None:
            out.append(None)
        else:
            below = sum(1 for p in present if p < v)
            equal = sum(1 for p in present if p == v)
            out.append((below + 0.5 * equal) / n)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv")
    ap.add_argument("--top", type=int, default=15)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    with open(a.csv, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        sys.exit("No rows found.")

    eng, vel, out = [], [], []
    for r in rows:
        saves, comments = num(r.get("saves")), num(r.get("comments"))
        e = None if saves is None and comments is None else (saves or 0) + 3 * (comments or 0)
        age, fol = num(r.get("age_days")), num(r.get("followers"))
        eng.append(e)
        vel.append(e / max(age, 1) if e is not None and age is not None else None)
        out.append(e / max(fol, 100) if e is not None and fol is not None else None)

    weights = (0.50, 0.35, 0.15)
    ranks = list(zip(pct_rank(vel), pct_rank(out), pct_rank(eng)))
    for r, e, v, o, rk in zip(rows, eng, vel, out, ranks):
        parts = [(w, x) for w, x in zip(weights, rk) if x is not None]
        tw = sum(w for w, _ in parts)
        r["score"] = round(100 * sum(w * x for w, x in parts) / tw, 1) if tw else 0.0
        r["engagement"] = e
        r["velocity_per_day"] = round(v, 2) if v is not None else None
        r["outlier_ratio"] = round(o, 3) if o is not None else None
        r["is_outlier"] = bool(o is not None and o >= 0.5) or r["score"] >= 80

    rows.sort(key=lambda r: r["score"], reverse=True)
    top = rows[: a.top]

    if a.json:
        print(json.dumps(top, indent=2))
        return
    print(f"{'#':>2}  {'score':>5}  {'vel/d':>7}  {'outlier':>7}  {'flag':4}  archetype / keyword / url")
    for i, r in enumerate(top, 1):
        flag = "★" if r["is_outlier"] else ""
        vel_s = "-" if r["velocity_per_day"] is None else r["velocity_per_day"]
        out_s = "-" if r["outlier_ratio"] is None else r["outlier_ratio"]
        print(f"{i:>2}  {r['score']:>5}  {vel_s:>7}  {out_s:>7}  {flag:4}  "
              f"{r.get('archetype','')} / {r.get('keyword','')} / {r.get('url','')}")


if __name__ == "__main__":
    main()
