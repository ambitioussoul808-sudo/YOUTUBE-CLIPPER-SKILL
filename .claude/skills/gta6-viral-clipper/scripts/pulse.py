#!/usr/bin/env python3
"""Hourly Pulse: dedupe new GTA 6 signals, score their virality, and print a ranked digest.

Usage:
  python3 pulse.py items.json [--state data/pulse-state.json] [--log data/pulse-log.md] [--now ISO] [--json]

Default output is a bullet-point DIGEST (new findings only, highest virality first,
top item marked USE FIRST). It is also saved to data/pulse-digest-latest.md.
--json prints machine-readable JSON instead.

items.json is a list of objects gathered this hour:
  {"title": "...", "url": "...", "source": "rockstar newswire | reddit | x | streamer | news | vidiq",
   "tier": 1-4, "published_at": "ISO (optional)", "engagement": number (optional),
   "vph": number (optional, views/hour), "kind": "official | first-ever | streamer-moment |
   drama | meme | update | rumor", "notes": "..."}

Virality score (0-100):
  base by kind:   official 55, first-ever 50, streamer-moment 45, drama 40, update 40, meme 30, rumor 15
  + freshness:    +30 if <1h old, +20 if <3h, +10 if <6h, 0 if <72h, -25 if <7d, -40 older
  + engagement:   up to +15, log-scaled (10k engagement ~ +15)
  + velocity:     up to +15 from vph, log-scaled (100k vph ~ +15)
  + corroboration:+5 per extra outlet reporting the same story (max +15)
  + tier 1 bonus: +5
  Undated items are capped at 54 (LOG): freshness must be shown by a date.
Labels: GO-LIVE >= 75 (act within 60 min), WATCH 55-74, LOG < 55.

No duplicates: URL variants (amp pages, query strings, www/m., YouTube watch/shorts/youtu.be,
TikTok/IG ids) collapse to one canonical key. Near-identical titles from different outlets are
merged into one finding (counted as corroboration). Anything already reported in an earlier
scan (canonical URL or similar title) is skipped.
"""
import argparse, json, math, os, sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dedupe import canonical_url, similar, merge_duplicates, render_digest  # noqa: E402

BASE = {"official": 55, "first-ever": 50, "streamer-moment": 45, "drama": 40,
        "update": 40, "meme": 30, "rumor": 15}


def parse_dt(s):
    if not s:
        return None
    try:
        d = datetime.fromisoformat(str(s).replace("Z", "+00:00"))
        return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def virality(item, now):
    why = [item.get("kind", "meme")]
    h = BASE.get(item.get("kind", "meme"), 30)
    pub = parse_dt(item.get("published_at"))
    if pub is None:
        why.append("undated")
    else:
        age = (now - pub).total_seconds() / 3600
        h += 30 if age < 1 else 20 if age < 3 else 10 if age < 6 else 0 if age < 72 else -25 if age < 168 else -40
        why.append(f"{age:.0f}h old" if age < 72 else f"{age / 24:.0f}d old")
    e = item.get("engagement")
    if isinstance(e, (int, float)) and e > 0:
        h += min(15, 15 * math.log10(e + 1) / 4)
        why.append(f"{int(e):,} engagements")
    v = item.get("vph")
    if isinstance(v, (int, float)) and v > 0:
        h += min(15, 15 * math.log10(v + 1) / 5)
        why.append(f"{int(v):,} views/h")
    n = item.get("sources_n", 1)
    if n > 1:
        h += min(15, 5 * (n - 1))
        why.append(f"{n} outlets")
    if int(item.get("tier", 3) or 3) == 1:
        h += 5
        why.append("official-tier")
    if pub is None:
        h = min(h, 54)
    return round(max(0, min(h, 100)), 1), " · ".join(why)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    data = os.path.join(os.path.dirname(here), "data")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("items")
    ap.add_argument("--state", default=os.path.join(data, "pulse-state.json"))
    ap.add_argument("--log", default=os.path.join(data, "pulse-log.md"))
    ap.add_argument("--digest-out", default=os.path.join(data, "pulse-digest-latest.md"))
    ap.add_argument("--now")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    now = parse_dt(a.now) if a.now else datetime.now(timezone.utc)
    items = json.load(open(a.items, encoding="utf-8"))
    state = {"seen_urls": [], "seen_titles": [], "last_vidiq_scan": None}
    if os.path.exists(a.state):
        state.update(json.load(open(a.state, encoding="utf-8")))
    seen_urls = {canonical_url(u) if "/" in u or "." in u else u for u in state["seen_urls"]}
    seen_titles = list(state.get("seen_titles", []))[-800:]

    # 1) drop anything already reported in earlier scans
    fresh = []
    for it in items:
        cu = canonical_url(it.get("url"))
        if cu and cu in seen_urls:
            continue
        if any(similar(it.get("title"), t) for t in seen_titles):
            continue
        fresh.append(it)

    # 2) merge duplicates inside this batch (same video/story from several outlets)
    merged = merge_duplicates(fresh)

    # 3) score
    for it in merged:
        it["virality"], it["why"] = virality(it, now)
        it["heat"] = it["virality"]  # backward-compatible alias
        it["label"] = "GO-LIVE" if it["virality"] >= 75 else "WATCH" if it["virality"] >= 55 else "LOG"
    merged.sort(key=lambda x: x["virality"], reverse=True)

    # 4) remember everything (including merged extra outlets)
    for it in merged:
        seen_urls.add(it["_canon"])
        for extra in it.get("also", []):
            seen_urls.add(canonical_url(extra))
        if it.get("title"):
            seen_titles.append(it["title"])
    state["seen_urls"] = sorted(u for u in seen_urls if u)[-3000:]
    state["seen_titles"] = seen_titles[-800:]
    state["last_pulse"] = now.isoformat()
    os.makedirs(os.path.dirname(a.state), exist_ok=True)
    json.dump(state, open(a.state, "w", encoding="utf-8"), indent=1)

    stamp = now.strftime("%Y-%m-%d %H:%M UTC")
    digest = render_digest(merged, "GTA 6 Pulse digest", stamp=stamp)
    with open(a.log, "a", encoding="utf-8") as f:
        f.write(f"\n## Pulse {stamp}: {len(merged)} new\n")
        f.write("\n".join(digest.splitlines()[1:]) + "\n")
    with open(a.digest_out, "w", encoding="utf-8") as f:
        f.write(digest + "\n")

    for it in merged:
        it.pop("_canon", None)
    if a.json:
        print(json.dumps({"new": merged, "go_live": [i for i in merged if i["label"] == "GO-LIVE"],
                          "watch": [i for i in merged if i["label"] == "WATCH"],
                          "seen_total": len(seen_urls)}, indent=2))
    else:
        print(digest)


if __name__ == "__main__":
    main()
