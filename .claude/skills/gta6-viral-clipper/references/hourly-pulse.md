# Hourly Pulse: be first to the moment

**Goal:** spot a GTA 6 moment within the hour it breaks, and get your clip or live stream up before the wave peaks. The full scan (`scout-report`) tells you what's *already* hot. The pulse tells you what's *about to be* hot.

## The budget rule (why the pulse is mostly free)
vidIQ gives you 150 credits a month. Hourly vidIQ scans would use the month in about 15 hours. So:
| Layer | Runs | Cost | What it uses |
|---|---|---|---|
| **Pulse** | every hour | **0 vidIQ credits** | WebSearch (3–4 queries). Genspark Super Agent once the CLI is approved |
| **Confirm** | only when the pulse finds a GO-LIVE, **max 1 per day** | 10 credits (Lean: trending shorts + rising keywords `day`) | vidIQ |
| **Full scout** | daily or every other day, by hand | 20 credits | vidIQ + Genspark |

Guards: call `vidiq_balance` before any Confirm. **Skip the Confirm if the balance is under 40** or if `last_vidiq_scan` in `data/pulse-state.json` is under 24h old.

## Each hour: the steps
1. **Gather (free).** Run these WebSearch queries, restricted to the last few hours where possible:
   - `Rockstar Newswire GTA 6 OR "GTA Online" announcement today` (Tier 1)
   - `GTA 6 viral clip streamer today` (Tier 2)
   - `r/GTA6 trending OR "GTA 6" discovery glitch easter egg today` (Tier 3)
   - `GTA 6 patch update servers down` (Tier 1 update or drama)
   - If `www.genspark.ai` works through the CLI: run Genspark prompt P1 (community pulse) for the last 60 minutes.
2. **Write the items** to `data/pulse-items.json` (schema in `scripts/pulse.py`). Classify each by `kind`: official, first-ever, streamer-moment, drama, update, meme or rumor. **Never include leaks.** A "leak" item is skipped, not classified as a rumor.
3. **Score and dedupe:** `python3 .claude/skills/gta6-viral-clipper/scripts/pulse.py .claude/skills/gta6-viral-clipper/data/pulse-items.json`
4. **Act on the label:**
   - **GO-LIVE (≥ 75)** → send a push notification (template below). Run the Confirm scan if the guards allow, write a clip brief and Clip Genius prompt for the moment, then commit and push.
   - **WATCH (55–74)** → log it. If the same topic shows up as WATCH **2 hours in a row**, promote it to GO-LIVE.
   - **LOG** → nothing. It's already in `data/pulse-log.md`.
5. **Quiet hour** (nothing new): don't notify, don't commit. End the turn in one line.

## Push notification template (GO-LIVE only)
```
🚨 GTA 6 GO-LIVE: <moment in ≤ 8 words>
Why now: <source> · <age> · heat <score>
Make: <archetype> → <format: Short / live / long>
Hook: "<first on-screen line>"
Brief: clip-briefs/<file>.md
```

## The 60-minute Go-Live playbook (what you do when the alert hits)
| Minute | Action |
|---|---|
| 0–5 | Read the alert, then open the brief and Clip Genius prompt the agent wrote |
| 5–30 | **Recreate or react in your own game**: do the thing, find the spot, test the claim. Record it |
| 30–45 | Upload to Clip Genius → paste the prompt → export the vertical Short |
| 45–55 | Title with the trending keyword, using the "World's first / I tried / GTA 6 just ___" hook. Run the Rights Gate checks |
| 55–60 | Post a native upload to Shorts, TikTok and Reels. Optional: go live with the title "Trying the <moment> LIVE" |

**Going live first:** for official drops (a new trailer, a GTA Online update, a patch), going **live within 30 minutes** with "reacting LIVE" beats any edited video. The "gta 6 live" search term is up 317%. Pin a clip of the best 30 seconds afterwards.
