#!/usr/bin/env python3
"""Hourly Pulse: dedupe new GTA 6 signals, rate their heat, and flag GO-LIVE moments.

Usage:
  python3 pulse.py items.json [--state data/pulse-state.json] [--log data/pulse-log.md] [--now ISO]

items.json is a list of objects gathered this hour:
  {"title": "...", "url": "...", "source": "rockstar newswire | reddit | x | streamer | news | vidiq",
   "tier": 1-4, "published_at": "ISO (optional)", "engagement": number (optional),
   "kind": "official | first-ever | streamer-moment | drama | meme | update | rumor", "notes": "..."}

Heat (0-100):
  base by kind:  official 55, first-ever 50, streamer-moment 45, drama 40, update 40, meme 30, rumor 15
  + freshness:   +30 if <1h old, +20 if <3h, +10 if <6h, 0 if <72h, -25 if <7d, -40 older (unknown age = +10)
  + engagement:  +up to 15, log-scaled (10k engagement ~ +15)
  + tier 1 bonus +5
Labels: GO-LIVE >= 75 (act within 60 min), WATCH 55-74, LOG < 55.

Prints JSON: {"new": [...], "go_live": [...], "watch": [...], "seen_total": n}
Already-seen items (same URL or same normalised title) are skipped.
"""
import argparse, json, math, os, re, sys
from datetime import datetime, timezone

BASE = {"official": 55, "first-ever": 50, "streamer-moment": 45, "drama": 40,
        "update": 40, "meme": 30, "rumor": 15}


def norm(t):
    return re.sub(r"[^a-z0-9 ]", "", (t or "").lower()).strip()[:90]


def parse_dt(s):
    if not s:
        return None
    try:
        d = datetime.fromisoformat(str(s).replace("Z", "+00:00"))
        return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def heat(item, now):
    h = BASE.get(item.get("kind", "meme"), 30)
    pub = parse_dt(item.get("published_at"))
    if pub is None:
        h += 10
    else:
        age = (now - pub).total_seconds() / 3600
        h += 30 if age < 1 else 20 if age < 3 else 10 if age < 6 else 0 if age < 72 else -25 if age < 168 else -40
    e = item.get("engagement")
    if isinstance(e, (int, float)) and e > 0:
        h += min(15, 15 * math.log10(e + 1) / 4)
    if int(item.get("tier", 3) or 3) == 1:
        h += 5
    return round(max(0, min(h, 100)), 1)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    data = os.path.join(os.path.dirname(here), "data")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("items")
    ap.add_argument("--state", default=os.path.join(data, "pulse-state.json"))
    ap.add_argument("--log", default=os.path.join(data, "pulse-log.md"))
    ap.add_argument("--now")
    a = ap.parse_args()

    now = parse_dt(a.now) if a.now else datetime.now(timezone.utc)
    items = json.load(open(a.items, encoding="utf-8"))
    state = {"seen_urls": [], "seen_titles": [], "last_vidiq_scan": None}
    if os.path.exists(a.state):
        state.update(json.load(open(a.state, encoding="utf-8")))
    urls, titles = set(state["seen_urls"]), set(state["seen_titles"])

    new = []
    for it in items:
        u, t = (it.get("url") or "").strip(), norm(it.get("title"))
        if (u and u in urls) or (t and t in titles):
            continue
        it["heat"] = heat(it, now)
        it["label"] = "GO-LIVE" if it["heat"] >= 75 else "WATCH" if it["heat"] >= 55 else "LOG"
        new.append(it)
        if u:
            urls.add(u)
        if t:
            titles.add(t)
    new.sort(key=lambda x: x["heat"], reverse=True)

    state["seen_urls"], state["seen_titles"] = sorted(urls)[-3000:], sorted(titles)[-3000:]
    state["last_pulse"] = now.isoformat()
    os.makedirs(os.path.dirname(a.state), exist_ok=True)
    json.dump(state, open(a.state, "w", encoding="utf-8"), indent=1)

    stamp = now.strftime("%Y-%m-%d %H:%M UTC")
    with open(a.log, "a", encoding="utf-8") as f:
        f.write(f"\n## Pulse {stamp}: {len(new)} new\n")
        for it in new:
            f.write(f"- **{it['label']}** ({it['heat']}) [{it.get('kind','?')}] {it.get('title','')}: {it.get('url','')}\n")
        if not new:
            f.write("- nothing new\n")

    out = {"new": new, "go_live": [i for i in new if i["label"] == "GO-LIVE"],
           "watch": [i for i in new if i["label"] == "WATCH"], "seen_total": len(urls)}
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
