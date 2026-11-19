---
name: gta6-viral-clipper
description: Viral clip strategy engine for GTA 6 / Grand Theft Auto VI and Rockstar Games content. Use when the user asks to scout GTA 6 trends, find viral or epic GTA 6 moments, track Rockstar news, plan GTA 6 clips/shorts/reels, build a GTA content calendar, write hooks/titles/thumbnails for GTA videos, or "run a GTA sprint" / "clip scout" / "launch-day scan". Covers official Rockstar signals, streamer/creator moments, community memes, and vidIQ outlier data.
---

# GTA 6 Viral Clipper

Find the GTA 6 moments that are spreading **right now**, work out *why*, and turn them into clips, shorts and long-form ideas that ride the wave with your own angle. Ride the wave, don't re-upload it.

**Core rule: own the angle, borrow the moment.** You can use what happened (a stolen jumbo jet, an IGN score, a streamer's meltdown) as your topic. Your footage, voice, edit and take make it yours. Third-party footage is only for short commentary excerpts that pass the Rights Gate (Step 5).

## Files in this skill
| File | Use it for |
|---|---|
| `references/source-map.md` | The 4-tier source system: where to look and what each tier is good for |
| `references/clip-archetypes.md` | 12 proven GTA clip formats with hooks, lengths and examples from the live scout |
| `references/rights-and-safety.md` | The Rights Gate, Rockstar's video policy, leak rules, platform nudity/violence flags |
| `references/vidiq-playbook.md` | Which vidIQ tool to call for which question, and how to budget credits |
| `references/genspark-playbook.md` | **Tool #2.** What Genspark handles (Reddit/X/news research, scripts, AI images and B-roll) and how the handoff lane works |
| `templates/genspark-prompts.md` | Ready-to-paste Genspark prompts (pulse, official digest, streamer moments, fact check, script, image, video) |
| `templates/scout-report.md` | Output format for a scan |
| `templates/clip-brief.md` | Output format for each clip to produce |
| `scripts/score_clips.py` | Ranks signals by velocity, outlier strength, engagement and freshness. Labels each NOW / RIDE / LATE |
| `data/` | Raw scout CSVs (one per scan, dated) |

## Workflow: the 5-step Heat Loop

### 1. Intake (only ask if unclear)
- **Channel focus**: shorts-first (TikTok/Reels/Shorts), long-form YouTube, or both. Default: both.
- **Footage source**: does the user have their own GTA 6 capture? (PS5 share / Xbox capture / capture card). If not, plans lean on commentary-over-excerpt and meme formats.
- **Persona**: hype, comedy, analyst, or lore. Default: analyst-with-swagger.

### 2. Scout (all four tiers)
If you can spawn subagents, hand this step to `gta6-clip-scout` (`.claude/agents/gta6-clip-scout.md`). Otherwise run it inline.
**Two tools, two jobs:** vidIQ = numbers (YouTube, TikTok, Reels and search). Genspark = everything vidIQ can't see (Reddit, X, news, streamer drama) plus scripts and visuals. Genspark has no API or MCP connector yet, so write `genspark-prompts-<date>.md` from the template for the user to paste, then ingest their saved output from `data/genspark-<date>.md`. Use WebSearch as a fallback when no Genspark output exists.

1. **Tier 1, Official**: Rockstar Newswire, @RockstarGames, Take-Two investor news, patch notes, GTA Online announcements. *These start waves.* → Genspark P2
2. **Tier 2, Creators**: `vidiq_trending_videos` (titleQuery "GTA 6", sortBy `recentVph`, long and short), streamer coverage via web search (StreamsCharts, TwitchTracker, Kick).
3. **Tier 3, Community**: `vidiq_instagram_tiktok_outlier_search` for numbers. Genspark P1 for Reddit, X and memes, and P3 for streamer moments.
4. **Tier 4, Demand data**: `vidiq_keyword_research` mode `rising`, niche "GTA 6", period `week` (or `day` during launch).

Log every signal to `data/scout-<YYYY-MM-DD>.csv` (header in `score_clips.py`) and run:
```bash
python3 .claude/skills/gta6-viral-clipper/scripts/score_clips.py .claude/skills/gta6-viral-clipper/data/scout-<date>.csv
```
Raw vidIQ trending JSON can be passed straight in too.

### 3. Decode the heat
For each top-10 signal, record:
- **Archetype** (from `clip-archetypes.md`)
- **Moment**: the 3–10 seconds that make it work (the shock, the first-ever, the reaction face)
- **Trigger**: awe, chaos, schadenfreude, relatability, FOMO, tribal debate, or nostalgia
- **Search hook**: the rising keyword it matches (Tier 4)
- **Window**: NOW (<24h, act today) / RIDE (<72h) / LATE (pattern only)

### 4. Remix into clips
For each NOW/RIDE opportunity, write a clip brief (`templates/clip-brief.md`):
- Keep the **archetype, trigger and search hook**.
- Change the **footage** (yours), the **angle** (your take, a test, a ranking, a counter-argument) and the **packaging** (title, thumbnail, first 2 seconds).
- Make **3 variants**: a Short (≤ 45s, vertical), a long-form angle (8–15 min), and a meme/POV version that needs no gameplay.
- Titles: lead with the rising keyword ("GTA 6 map", "GTA 6 vs GTA 5", "GTA 6 reaction"). Score them with `vidiq_score_title` when credits allow.

### 5. Rights Gate + ship
Run every brief through `references/rights-and-safety.md`. Every answer must be **YES**:
1. Is the main footage ours (own gameplay, own camera, licensed, or generated)?
2. If we show anyone else's footage: is it short, credited, and *commented on*, not just replayed?
3. Does the clip add an idea the source didn't have (a ranking, a test, a counterpoint, a joke, context)?
4. Is it free of leaked, pirated, or pre-release-stolen material?
5. Does it avoid unblurred in-game nudity and extreme gore in the thumbnail and first 3 seconds (platform flags)?

Before publishing, run Genspark P4 (fact check) on every stat in the title or voiceover. Draft scripts with P5, and make thumbnail backgrounds and B-roll with P6/P7 (original art only).

Then hand off: `vidiq_generate_clips` (on the user's own long VOD), `vidiq_generate_thumbnail`, `vidiq_generate_titles`, Canva, or `vidiq_social_post_draft_create` for scheduling.

## Output standards
- Lead with the **3 highest-leverage moves for today**, then the detail.
- Every number says where it came from (vidIQ / tracker / article) and whether it's observed or estimated. **Never invent view counts.**
- Keep it modular and scannable.
- Note vidIQ credits used and credits left at the end of every scan, and which Genspark prompts were issued or ingested.
