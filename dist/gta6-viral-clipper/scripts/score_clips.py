#!/usr/bin/env python3
"""Rank GTA 6 / Rockstar content by clip-worthiness.

Usage:
  python3 score_clips.py signals.csv [--top 20] [--now 2026-11-19T12:00:00Z] [--json]
  python3 score_clips.py vidiq_trending.json        # raw vidIQ trending/outlier JSON also works

CSV header (blank numeric cells allowed):
  url,platform,creator,tier,subscribers,views,likes,comments,published_at,vph,title,notes

tier = 1 official | 2 creator | 3 community | 4 data-only

Scoring (0-100, relative within the file):
  velocity   = vph (or views / hours since publish)        -> is it moving NOW?
  outlier    = views / max(subscribers, 1000)              -> did it beat the creator's reach?
  engagement = (likes + 3*comments) / views                -> do people react, not just scroll?
  freshness  = 1 / (1 + hours/24)                          -> clip windows close fast
  score = 40% velocity + 25% outlier + 20% engagement + 15% freshness (percentile ranks)

Window label:
  NOW    (< 24h old and top-third velocity)  - clip/respond today
  RIDE   (< 72h old)                         - still worth a remix
  LATE   (older)                             - use for pattern only
"""
import argparse, csv, json, sys
from datetime import datetime, timezone


def num(v):
    try:
        return float(str(v).replace(",", "").strip())
    except (TypeError, ValueError):
        return None


def parse_dt(s):
    if not s:
        return None
    s = str(s).strip().replace("Z", "+00:00")
    try:
        d = datetime.fromisoformat(s)
        return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def pct_rank(values):
    present = sorted(v for v in values if v is not None)
    n = len(present)
    out = []
    for v in values:
        if v is None or not n:
            out.append(None)
        else:
            below = sum(1 for p in present if p < v)
            equal = sum(1 for p in present if p == v)
            out.append((below + 0.5 * equal) / n)
    return out


def load(path):
    if path.endswith(".json"):
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        vids = data.get("videos") or data.get("results") or data if isinstance(data, (dict, list)) else []
        rows = []
        for v in vids:
            vid = v.get("videoId", "")
            rows.append({
                "url": f"https://www.youtube.com/watch?v={vid}" if vid else v.get("url", ""),
                "platform": "youtube", "creator": v.get("channelTitle", ""), "tier": "2",
                "subscribers": v.get("subscriberCount"), "views": v.get("viewCount"),
                "likes": v.get("likeCount"), "comments": v.get("commentCount"),
                "published_at": v.get("videoPublishedAt"), "vph": v.get("vph"),
                "title": v.get("videoTitle", ""), "notes": "",
            })
        return rows
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path")
    ap.add_argument("--top", type=int, default=20)
    ap.add_argument("--now", help="ISO timestamp to measure age from (default: current UTC time)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    now = parse_dt(a.now) if a.now else datetime.now(timezone.utc)
    rows = load(a.path)
    if not rows:
        sys.exit("No rows found.")

    vel, outl, eng, fresh, ages = [], [], [], [], []
    for r in rows:
        views, subs = num(r.get("views")), num(r.get("subscribers"))
        likes, comments = num(r.get("likes")), num(r.get("comments"))
        pub = parse_dt(r.get("published_at"))
        hours = max((now - pub).total_seconds() / 3600, 1) if pub else None
        ages.append(hours)
        v = num(r.get("vph"))
        if v is None and views is not None and hours:
            v = views / hours
        vel.append(v)
        outl.append(views / max(subs or 0, 1000) if views is not None else None)
        eng.append(((likes or 0) + 3 * (comments or 0)) / views
                   if views and (likes is not None or comments is not None) else None)
        fresh.append(1 / (1 + hours / 24) if hours else None)

    rv, ro, re_, rf = pct_rank(vel), pct_rank(outl), pct_rank(eng), pct_rank(fresh)
    weights = (0.40, 0.25, 0.20, 0.15)
    scored = []
    for i, r in enumerate(rows):
        parts = [(rv[i], weights[0]), (ro[i], weights[1]), (re_[i], weights[2]), (rf[i], weights[3])]
        have = [(p, w) for p, w in parts if p is not None]
        score = round(100 * sum(p * w for p, w in have) / sum(w for _, w in have), 1) if have else 0.0
        h = ages[i]
        if h is not None and h < 24 and (rv[i] or 0) >= 0.67:
            window = "NOW"
        elif h is not None and h < 72:
            window = "RIDE"
        else:
            window = "LATE"
        scored.append({**r, "score": score, "window": window,
                       "vph_calc": round(vel[i]) if vel[i] else None,
                       "outlier_x": round(outl[i], 2) if outl[i] else None,
                       "engagement": round(eng[i], 4) if eng[i] else None,
                       "age_h": round(h, 1) if h else None})

    scored.sort(key=lambda x: x["score"], reverse=True)
    top = scored[: a.top]
    if a.json:
        print(json.dumps(top, indent=2, default=str))
        return
    print(f"{'#':>2}  {'score':>5}  {'win':<4}  {'age_h':>5}  {'vph':>8}  {'outl':>5}  {'eng':>6}  creator / title")
    for i, s in enumerate(top, 1):
        print(f"{i:>2}  {s['score']:>5}  {s['window']:<4}  {s['age_h'] or '-':>5}  "
              f"{s['vph_calc'] or '-':>8}  {s['outlier_x'] or '-':>5}  {s['engagement'] or '-':>6}  "
              f"{s.get('creator','')[:22]} | {s.get('title','')[:60]}")


if __name__ == "__main__":
    main()
