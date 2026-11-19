# Genspark Prompt Pack: <YYYY-MM-DD>

Paste each prompt into genspark.ai. Save the outputs to `.claude/skills/gta6-viral-clipper/data/genspark-<date>.md`, then tell Claude "ingest Genspark".

---

## P1 · Community Pulse (Super Agent, every 6–12h)
```
Research what GTA 6 / Grand Theft Auto VI players are talking about most in the last 24 hours on Reddit (r/GTA6, r/GTA, r/gaming), X/Twitter, and gaming news sites. Today is <DATE>.

Return a table of the top 15 discussion topics with: topic, one-sentence summary, where it's trending (subreddit / X hashtag / outlet), evidence link, rough engagement (upvotes, likes, comments) labeled as observed or estimated, and sentiment (hype / funny / angry / debate).

Then list the 5 topics most likely to become viral YouTube or TikTok videos in the next 48 hours, and why.

Rules: cite a link for every row. Do not include or summarize leaked or pirated material. If numbers conflict between sources, give the range.
```

## P2 · Official Rockstar Digest (Super Agent, daily)
```
Summarize every official Rockstar Games and Take-Two announcement about GTA 6 / GTA VI and GTA Online from the last 72 hours (today is <DATE>): Rockstar Newswire posts, patch notes, trailers, social posts, earnings or sales statements, and rating or review milestones.

For each: date, headline, what changed, official source link, and one "clip angle" a YouTube creator could make about it.
Only use official sources or major outlets quoting them. Flag anything unconfirmed.
```

## P3 · Streamer Moments (Super Agent, daily during launch month)
```
Find the most-clipped and most-discussed streamer moments from GTA 6 streams in the last 24 hours (today is <DATE>) across Twitch, YouTube, and Kick. Include creators like Kai Cenat, IShowSpeed, HoneyMad, Windah Basudara, Asmongold, plus any smaller streamer whose moment went viral.

For each moment: streamer, platform, what happened in one sentence, link to the clip or VOD timestamp, reported views or peak viewers (cite the source), and whether that streamer publicly allows or pays for clipping (link to their policy if found).
```

## P4 · Fact Check (Super Agent, before publishing)
```
Fact-check these claims for a GTA 6 YouTube video. For each, return TRUE / FALSE / UNVERIFIED, the best primary source, and the exact correct figure:
1. <claim>
2. <claim>
3. <claim>
```

## P5 · Script Draft (AI Chat)
```
Write a <LENGTH>-minute YouTube script for "<TITLE>". Persona: confident gaming analyst with swagger and humor. Structure: <PASTE CHAPTERS FROM CLIP BRIEF>.
Open with a 30-second cold open that teases the payoff. Short sentences, written for voiceover. Mark [B-ROLL: ...] cues and [ON-SCREEN TEXT: ...] cues. End with a comment-bait question.
Do not state any statistic I haven't provided. Use [STAT NEEDED] instead.
```

## P6 · Thumbnail Background (AI Image, free tier)
```
16:9 YouTube thumbnail background, no text: <SCENE, e.g. "neon Miami-style city at night, police helicopter spotlight on a speeding sports car, red and blue light streaks, cinematic, high contrast">. Leave the left third darker for bold text. Original artwork. No logos, no real people, no video game key art or characters.
```

## P7 · AI B-roll Sting (AI Video, costs credits, max 1–2 per video)
```
5-second cinematic establishing shot: <SCENE, e.g. "drone sweep over a tropical coastal city at golden hour, palm trees, ocean, neon signs turning on">. Smooth camera, no text, no logos, no recognizable characters. 16:9.
```
