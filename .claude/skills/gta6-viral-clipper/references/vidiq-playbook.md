# vidIQ Playbook

## Which tool answers which question
| Question | Tool | Key params |
|---|---|---|
| What GTA 6 videos are exploding right now? | `vidiq_trending_videos` | titleQuery "GTA 6", sortBy `recentVph`, videoFormat `long` / `short`, requireAllTitleTerms true |
| Which videos beat their channel's normal? | `vidiq_outliers` | keyword, publishedWithin `thisWeek` |
| What are people searching that's growing? | `vidiq_keyword_research` | mode `rising`, niche "GTA 6", period `day` / `week` |
| What's popping on TikTok and Reels? | `vidiq_instagram_tiktok_outlier_search` | datePostedAfter = 7 days ago |
| What exactly happened in that video? | `vidiq_video_transcript` | videoId, to find the timestamp of the moment |
| Will this title work? | `vidiq_score_title` | |
| Cut my own long VOD into Shorts | `vidiq_generate_clips` | **only on footage you own** |
| Thumbnail drafts | `vidiq_generate_thumbnail`, `vidiq_score_thumbnail` | |

## Credit budget (current plan: 150 renewable credits/month, 5 credits per call)
| Scan | Calls | Credits | Scans per month on 150 |
|---|---|---|---|
| **Full scan** (trending long, trending short, rising keywords, TikTok/IG outliers) | 4 | 20 | ~7 |
| **Lean scan** (trending short plus rising keywords) | 2 | 10 | ~15 |
| **Deep dive** (adds 2 transcripts and 1 outlier search) | +3 | +15 | |

On 150 credits a month, you can't scan every 6 hours through launch month. **Recommended:** a daily vidIQ Lean scan (10 credits), with Genspark's free research covering the hours in between. If you need more, upgrade vidIQ for launch month only.

## What vidIQ does NOT cover (fill these gaps)
| Gap | Fill with |
|---|---|
| Live Twitch/Kick viewership and top clips | StreamsCharts, TwitchTracker, the Twitch API (free `clips` endpoint) |
| Reddit / X / Discord chatter | **Genspark P1** (see `genspark-playbook.md`), WebSearch |
| Official Rockstar announcements | **Genspark P2**, Rockstar Newswire (web-fetch) |
| Actually cutting and editing video | vidIQ `generate_clips` / `edit_media` for your own footage, or CapCut / Premiere / ffmpeg |
