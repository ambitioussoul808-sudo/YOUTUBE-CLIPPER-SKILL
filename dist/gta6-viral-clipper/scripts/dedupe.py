"""Shared helpers: canonical URLs, near-duplicate detection, digest rendering.

Used by pulse.py (hourly) and score_clips.py (full scout) so both report each
video/story exactly once.
"""
import re
from urllib.parse import urlparse, parse_qs

STOP = {"the", "a", "an", "of", "in", "on", "for", "to", "and", "is", "as", "at", "with",
        "gta", "6", "vi", "grand", "theft", "auto", "s", "it", "its", "after", "from", "by"}


def canonical_url(url):
    """Collapse URL variants of the same page/video into one key.

    - YouTube watch / shorts / youtu.be / embed  -> yt:<id>
    - TikTok video id                            -> tt:<id>
    - Instagram reel/post shortcode              -> ig:<code>
    - everything else: host without www/m/amp, path without /amp, trailing slash,
      query string and fragment dropped
    """
    if not url:
        return ""
    u = url.strip()
    p = urlparse(u if "://" in u else "https://" + u)
    host = p.netloc.lower()
    for pre in ("www.", "m.", "amp.", "mobile."):
        if host.startswith(pre):
            host = host[len(pre):]
    path = p.path or "/"
    if host in ("youtube.com", "youtu.be") or host.endswith(".youtube.com"):
        vid = parse_qs(p.query).get("v", [None])[0]
        if not vid:
            m = re.search(r"/(?:shorts|embed|live)/([\w-]{11})", path) or re.match(r"/([\w-]{11})", path)
            vid = m.group(1) if m else None
        if vid:
            return "yt:" + vid
    if "tiktok.com" in host:
        m = re.search(r"/video/(\d+)", path)
        if m:
            return "tt:" + m.group(1)
    if "instagram.com" in host:
        m = re.search(r"/(?:reel|p)/([\w-]+)", path)
        if m:
            return "ig:" + m.group(1)
    path = re.sub(r"/amp/?$", "/", path)
    path = re.sub(r"\.amp$", "", path)
    path = path.rstrip("/") or "/"
    return f"{host}{path}".lower()


def tokens(title):
    return {w for w in re.findall(r"[a-z0-9]+", (title or "").lower()) if w not in STOP and len(w) > 1}


def similar(a, b, threshold=0.6):
    """Jaccard similarity on meaningful title words."""
    ta, tb = tokens(a), tokens(b)
    if not ta or not tb:
        return False
    return len(ta & tb) / len(ta | tb) >= threshold


def merge_duplicates(items, title_key="title", url_key="url", use_titles=True):
    """Merge items that share a canonical URL or a near-identical title.

    use_titles=False merges only identical canonical URLs (use for videos: two
    creators covering the same topic are different videos, not duplicates).
    Keeps the first (highest-priority) item, records every extra source in
    item['also'] and the outlet count in item['sources_n'].
    """
    kept = []
    for it in items:
        cu = canonical_url(it.get(url_key))
        it["_canon"] = cu
        dup = None
        for k in kept:
            if (cu and cu == k["_canon"]) or (use_titles and similar(it.get(title_key), k.get(title_key))):
                dup = k
                break
        if dup is None:
            it.setdefault("also", [])
            it["sources_n"] = 1
            kept.append(it)
        else:
            if cu and cu != dup["_canon"] and it.get(url_key) not in dup["also"]:
                dup["also"].append(it.get(url_key))
                dup["sources_n"] += 1
    return kept


def render_digest(rows, title, score_key="virality", label_key="label", stamp=""):
    """Bullet-point digest, highest score first, top item marked USE FIRST."""
    lines = [f"### {title}{(' · ' + stamp) if stamp else ''}"]
    if not rows:
        lines.append("- Nothing new this scan (all results were duplicates of earlier finds).")
        return "\n".join(lines)
    for i, r in enumerate(rows):
        tag = "▶ **USE FIRST**" if i == 0 else f"{i + 1}."
        extra = f" (+{r['sources_n'] - 1} more outlet{'s' if r['sources_n'] > 2 else ''})" if r.get("sources_n", 1) > 1 else ""
        why = f" ({r['why']})" if r.get("why") else ""
        lines.append(f"- {tag} **{r[score_key]}/100** [{r.get(label_key, '')}] {r.get('title', '')}{extra}{why}: {r.get('url', '')}")
    return "\n".join(lines)
