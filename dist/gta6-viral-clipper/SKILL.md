---
name: gta6-viral-clipper
description: End-to-end viral clip engine for GTA 6 / Grand Theft Auto VI and Rockstar Games content on YouTube, TikTok and Instagram. Use when the user asks to scout GTA 6 trends, find viral or epic GTA 6 moments, track Rockstar news, run an hourly pulse or go-live alert, write clip briefs, hooks, titles or thumbnails, create Genspark Clip Genius prompts, build stock-footage sample Shorts, or package a post kit (captions, hashtags, sounds, covers, schedule). Triggers include "run a GTA sprint", "clip scout", "launch-day scan", "hourly pulse", "clip briefs", "clip genius", "post kit", "go live first". Uses vidIQ for numbers, Genspark for research and editing, Canva for thumbnails.
---

# GTA 6 Viral Clipper

Find the GTA 6 moments spreading **right now**, work out *why*, and turn them into clips, live streams and posts that ride the wave with the user's own angle, ideally **first**.

**Core rule: own the angle, borrow the moment.** What happened (a stolen jumbo jet, a review score, a streamer's meltdown) can be the topic. The user's footage, voice, edit and take make it theirs. Third-party footage is only for short, credited commentary excerpts that pass the Rights Gate.

## Toolkit
| Tool | Job | Notes |
|---|---|---|
| **vidIQ** (MCP) | Numbers: trending velocity, outliers, rising keywords, TikTok/Reels outliers, title scores, stock B-roll, trending sounds | About 150 credits/month. Budget in `references/vidiq-playbook.md` |
| **Genspark** | Research vidIQ can't see (Reddit, X, news, streamer drama), fact checks, scripts, AI images and B-roll, and **Clip Genius** video editing | Key stored as a network secret for `www.genspark.ai` (`X-Api-Key`). CLI `@genspark/cli` needs a permission rule. Until then, use the paste-in prompt lane. See `references/genspark-playbook.md` |
| **Canva** (MCP) | Thumbnail and cover drafts (`create-design`, format "YouTube Thumbnail") | Original art only, no game logos |
| **WebSearch** | Free fallback for every research step, and the engine of the Hourly Pulse | |
| **ffmpeg** | Stock-footage Shorts, platform exports, covers | `references/stock-shorts.md` |

## Files
| File | Use it for |
|---|---|
| `references/source-map.md` | The 4-tier source system and scan cadence |
| `references/clip-archetypes.md` | 12 proven GTA clip formats, hooks and audio patterns |
| `references/rights-and-safety.md` | Rights Gate, Rockstar policy, leak rules, platform flags |
| `references/vidiq-playbook.md` | Which vidIQ call answers which question, and the credit budget |
| `references/genspark-playbook.md` | Genspark division of labor, Clip Genius rules, connection status |
| `references/hourly-pulse.md` | Hourly GO-LIVE scan protocol and the 60-minute go-live playbook |
| `references/stock-shorts.md` | Recipe for stock-footage "bridge" Shorts |
| `templates/scout-report.md` | Scan output |
| `templates/clip-brief.md` | One brief per opportunity (3 variants) |
| `templates/clip-genius-prompts.md` | One Clip Genius edit prompt per variant |
| `templates/genspark-prompts.md` | Research, fact-check, script, image and video prompts |
| `templates/post-kit.md` | Ready-to-post package for YouTube, Instagram and TikTok |
| `scripts/score_clips.py` | Ranks scout signals and labels each NOW / RIDE / LATE |
| `scripts/pulse.py` | Hourly dedupe and heat score, labels each GO-LIVE / WATCH / LOG |
| `data/` | Scout CSVs, pulse state and log, Genspark outputs |

## Modes (pick from the request)
| Request | Do |
|---|---|
| "run the GTA 6 hourly pulse" (scheduled) | **Follow `references/hourly-pulse.md` exactly.** Nothing else |
| "scan / scout / sprint" | Steps 1–3, then offer Step 4 |
| "write clip briefs" | Step 4 (+5) from the latest scout report |
| "clip genius" | Step 6a |
| "make samples / stock video" | Step 6b |
| "finish the post / post kit" | Step 7 |

## Workflow: the 7-step Heat Loop

### 1. Intake (ask only if unclear; ≤ 3 questions)
Channel focus (default: Shorts and long-form) · own footage available? (PS5/Xbox capture, capture card) · persona (default: analyst with swagger) · platforms (default: YouTube, Instagram, TikTok).

### 2. Scout (4 tiers)
Hand off to the `gta6-clip-scout` agent if subagents are available. Otherwise run inline.
1. **Tier 1, Official:** Rockstar Newswire, @RockstarGames, Take-Two, patch notes (Genspark P2 / WebSearch).
2. **Tier 2, Creators:** `vidiq_trending_videos` (titleQuery "GTA 6", `recentVph`, long and short), streamer peaks (StreamsCharts, TwitchTracker) and Genspark P3.
3. **Tier 3, Community:** `vidiq_instagram_tiktok_outlier_search` plus Genspark P1 (Reddit, X, memes).
4. **Tier 4, Demand:** `vidiq_keyword_research` mode `rising`, niche "GTA 6", period `day` (launch or trailer week) or `week`.

Log signals to `data/scout-<date>.csv` and run `python3 .claude/skills/gta6-viral-clipper/scripts/score_clips.py <csv> --now <current UTC ISO>`. **Always pass the real current time to `--now`** (check it with `date -u`). Write `scout-report-<date>.md`.

### 3. Decode the heat
For each top-10 signal: archetype · the 3–10s moment · trigger (awe, chaos, schadenfreude, relatability, FOMO, debate, nostalgia) · rising keyword · window (NOW < 24h, RIDE < 72h, LATE = pattern only).

### 4. Remix into clip briefs
Use `templates/clip-brief.md` for each NOW/RIDE opportunity. Keep the archetype, trigger and keyword. Change the footage, angle and packaging. Write **3 variants**: A Short (≤ 45s, 9:16), B long-form (8–15 min), C no-gameplay POV. Titles lead with the rising keyword. Score the lead title with `vidiq_score_title` (5 credits).

### 5. Rights Gate (all YES or it doesn't ship)
1. Main footage is ours, licensed, or generated.
2. Third-party excerpts are short (≤ 8s in Shorts, ≤ 12s in long-form), credited on screen, and commented on. The creator allows clipping.
3. Adds an idea the source lacked.
4. No leaks, piracy or exploits.
5. No nudity or extreme gore in the thumbnail or first 3s.
6. Stats in titles or voiceover are fact-checked (Genspark P4).
7. Stock footage is never passed off as game footage.

### 6. Produce
- **6a · Clip Genius:** write `clip-genius-prompts-<date>.md` from the template: one prompt per variant, with exact timings, overlay text, crop, safe zones (text out of the bottom 25% and right 12%), music style and excerpt caps. The user uploads footage and runs them.
- **6b · Stock-footage samples:** follow `references/stock-shorts.md` (vidIQ B-roll, ffmpeg edit, generated audio, credits).
- **Thumbnails:** Canva `create-design` (YouTube Thumbnail), or Genspark P6 backgrounds. Max 3 words, one face, one accent colour.
- **Own long VOD:** `vidiq_generate_clips`.

### 7. Package and post
Build `post-kit/` from `templates/post-kit.md`:
- `-YOUTUBE.mp4` (with audio) and `-TIKTOK-REELS-silent.mp4` (trending sound added in-app)
- A cover JPG from a clean frame
- A trending sound per clip from `vidiq_tiktok_trending_sound_search`, with the sync timestamp
- Title, description, tags, captions, hashtags, pinned or first comments, alt text
- Schedule: TikTok → Reels +15 min → Shorts +30 min

**Publishing:** check `vidiq_social_account_list`. Only accounts with `canPublish: true` can be drafted with `vidiq_social_post_draft_create`. Show the draft and publish only after the user approves. TikTok privacy, comment and music-confirmation settings and YouTube privacy are **the creator's choice. Ask, never fill them in.**

## Hourly Pulse and going live first
The scheduled task fires "run the GTA 6 hourly pulse" every hour. It costs 0 vidIQ credits (WebSearch, plus Genspark when connected). It sends a push notification **only on GO-LIVE**, runs a 10-credit vidIQ confirm at most once a day (only if the balance is ≥ 40), writes a one-moment brief plus Clip Genius prompt, and makes one small `pulse:` commit of its state and log every hour (the repo's stop hook requires a clean tree). Quiet hours get no alert and a one-line reply.

## Output standards
- Lead with the **3 highest-leverage moves for today**, then the detail. Keep it modular and scannable.
- Every number says where it came from (vidIQ, tracker, article) and whether it's observed, reported or estimated. **Never invent metrics.** Give ranges when sources conflict.
- End every scan with vidIQ credits used and left, Genspark prompts issued or ingested, and gaps.
- Never link to, describe in detail or use leaked or pirated material.
