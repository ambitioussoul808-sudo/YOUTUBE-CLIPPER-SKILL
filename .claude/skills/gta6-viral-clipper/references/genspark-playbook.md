# Genspark Playbook: Tool #2

**vidIQ is the data source. Genspark is the research and production helper.** vidIQ tells you *what* is spreading on YouTube, TikTok and Reels, with real numbers. Genspark fills in what vidIQ can't see (Reddit, X, Discord, news, Twitch drama) and turns briefs into scripts and visual assets.

## How it connects (read this first)
As of Nov 2026, Genspark has **no confirmed public API and no MCP connector** in the Claude directory. Third-party reviews conflict on Enterprise API access. So the agent can't call Genspark directly. Instead it works as a **handoff lane**:

1. The agent writes ready-to-paste prompts to `genspark-prompts-<date>.md` (filled from `templates/genspark-prompts.md`).
2. You paste each one into Genspark (Super Agent, AI Image or AI Video) at genspark.ai.
3. You save Genspark's output (the Sparkpage link or exported text) to `data/genspark-<date>.md`.
4. The agent reads that file, logs any new signals into the scout CSV, and re-runs `score_clips.py`.

If Genspark ships an API or MCP server later, swap step 2 for a direct call. Check the Claude connector directory or the Genspark Enterprise plan page.

## Division of labor
| Job | vidIQ | Genspark | Why |
|---|---|---|---|
| YouTube trending / velocity / outliers | ✅ primary | | Real view and VPH data |
| TikTok / Reels outliers | ✅ primary | | Outlier scores against each creator's median |
| Rising search keywords | ✅ primary | | Search volume and competition |
| Title / thumbnail scoring | ✅ | | Trained on CTR |
| **Reddit / X / Discord pulse** | ❌ | ✅ primary | vidIQ doesn't cover them |
| **Rockstar news and patch-note digests** | ❌ | ✅ primary | Multi-source web research with citations |
| **Twitch/Kick streamer drama and moments** | ❌ | ✅ | Web research. Verify numbers against StreamsCharts |
| **Fact-checking claims** (map size, sales, scores) | ❌ | ✅ | Cross-checked sources |
| Long-form scripts and voiceover drafts | partial (`compose`) | ✅ | Free chat through Dec 2026 saves vidIQ credits |
| Thumbnail backgrounds / B-roll images | partial | ✅ AI Image | Free standard images through Dec 2026 |
| AI video B-roll (intro stings, transitions) | partial | ✅ AI Video (Sora/Veo/Kling) | Costs credits. Use sparingly |
| Cutting your own VOD into Shorts | ✅ `generate_clips` | | Works on your own footage |

## Credit strategy (this is the big win)
vidIQ: 150 credits a month, and a full scan costs 20. Genspark chat and standard images are reported as **free through Dec 2026**. Video, heavy agent runs and AI calls cost credits. Check your plan.
- Move **all Tier 1 and Tier 3 research** (news, Reddit, X, Twitch) to Genspark. That frees vidIQ credits for what only vidIQ does: velocity, outlier and keyword data.
- Updated launch-month cadence: **vidIQ Lean scan (10 credits) daily, plus a free Genspark pulse every 6–12h**, which comes to about 15 vidIQ scans a month instead of 7.

## Genspark guardrails (same Rights Gate applies)
- **Verify every number Genspark gives you** against a primary source before it goes in a title or voiceover. AI research tools can merge or misstate figures.
- **AI images and video must be original.** Don't prompt for Rockstar logos, official key art, real characters (Jason, Lucia), or "in the style of GTA 6 loading screens". Prompt for *vibes*: neon Miami, sunset coast, police chase. Rockstar's IP isn't yours to generate.
- **No real streamer likenesses** in AI images. Use your own face, or credited screenshots.
- Label AI-generated video where the platform requires it (YouTube's altered/synthetic content disclosure).
- Never ask Genspark to find or summarize leaked material.
