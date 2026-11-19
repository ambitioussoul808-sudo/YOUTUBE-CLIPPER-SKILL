# Stock-Footage Shorts ("bridge content")

Use these when you have **no gameplay yet**, or between captures. Real-world stock (Florida beaches, swamps, neon nights, police lights) plus text overlays copies proven GTA meme formats **without using any Rockstar footage**.

## Proven templates
| Template | Structure | Based on |
|---|---|---|
| **Last days of peace** | 0–9.7s calm (palms, waterfront) → white flash → chaos (neon car, helicopter, police lights) → CTA | TikTok pattern at 43× the creator's median |
| **13 years. One map.** | Coast → swamps → wildlife → neon nights → "How BIG is the GTA 6 map?" | "gta 6 map" search, 725K/mo, +129% |

## Recipe
1. **Find clips:** `vidiq_find_broll` (1 credit, Pexels, portrait). Prefer 720p+ results. Note the creator and page URL for credits.
2. **Download:** `videos.pexels.com` must be on the environment's allowed hosts.
3. **Edit with ffmpeg**, one segment per shot:
   - `scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920`
   - Grade: calm = warm and saturated, chaos = high-contrast night with a teal/red push, plus `unsharp`
   - Slow push-in on calm shots: `zoompan=z='min(1+0.0009*on,1.12)'`
   - A 0.2s white flash between calm and chaos
   - `drawtext` overlays (DejaVu Sans Bold, borderw 8). Keep text **above y≈1300 and out of the right 12%** (TikTok/Reels buttons)
   - Generated audio (`aevalsrc`): a pad, then a boom plus gated bass on the cut. Royalty-free by construction
4. **Export two versions:** `-YOUTUBE.mp4` (with audio) and `-TIKTOK-REELS-silent.mp4` (`-an`, for a trending sound in-app).
5. **Covers:** take them from a *clean* (un-captioned) segment frame. 2–3 big words, centered.
6. Write `samples/CREDITS.md` and a post kit from `templates/post-kit.md`.

## Rules
- **Never** use Rockstar footage, logos, key art or characters, and never imply stock is game footage. Label "real-world footage" on screen or in the caption.
- Avoid real agency insignia (police seals) and off-theme cities in shots meant to evoke Leonida.
- Don't repeat the same clip twice in one Short.
