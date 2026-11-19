---
name: pinterest-viral-empire
description: Pinterest trend research and viral-content recreation for the Intentional Empire brand (EmPressEmpire / Empower8). Use when the user asks to find Pinterest trends, research what's going viral on Pinterest, analyze winning pins, "reverse-engineer" or remix viral content for their niche, build a pin pack / content calendar for Pinterest, or create branded pins in the Blue ✦ Green ✦ Gold palette. Also triggers on "pinterest sprint", "trend scout", "viral remix", "pin pack".
---

# Pinterest Viral Empire

Find what's already winning on Pinterest, work out why it works, and rebuild it for Intentional Empire with the brand's palette, voice and compliance rules.

**Core rule: copy the pattern, never the pin.** Copy the structure, hook mechanics, layout, emotional trigger and search intent. Never copy another creator's images, exact wording, characters or watermark. Every output must pass the *Transformation Test* in Step 4.

## Files in this skill

| File | Use it for |
|---|---|
| `brand.json` | Brand colors, fonts and voice settings. **The only place colors live.** Edit hex values here. |
| `references/brand-kit.md` | Voice, visual rules and niche pillars for Intentional Empire |
| `references/research-playbook.md` | Where and how to dig for trends (Pinterest Trends, Predicts, search autocomplete, outlier hunting) |
| `references/viral-pattern-library.md` | The 12 viral pin archetypes and how to remix each one |
| `references/compliance.md` | Reach-safe guardrails (disclaimer-light) for money and healing topics, plus originality rules |
| `templates/trend-brief.md` | Output format for research |
| `templates/pin-pack.md` | Output format for finished pin concepts |
| `scripts/score_pins.py` | Ranks observed pins by velocity and outlier score from a CSV |
| `scripts/render_pin.py` | Renders branded 1000×1500 text-overlay pins from a JSON spec |

## Workflow: the 5-Phase Empire Loop

### Phase 1: Intake (≤ 3 questions, only if unclear)
Confirm: **pillar** (see brand-kit.md), **goal** (saves / clicks / leads / product sales), **destination URL or offer** (lead magnet, chatbot, funnel, Substack). If the user just says "run a pinterest sprint", default to: all 5 pillars, goal = saves + outbound clicks, 10 pins.

### Phase 2: Trend Recon
Follow `references/research-playbook.md`. If you can spawn subagents, hand the recon to the `pinterest-trend-scout` agent (`.claude/agents/pinterest-trend-scout.md`). Otherwise run it inline with WebSearch / web-fetch.

Collect for each pillar:
1. **Rising search terms**: Pinterest Trends, Pinterest Predicts, autocomplete, guided-search chips.
2. **Outlier pins**: pins whose saves/engagement far exceed the creator's norm or follower count. If the user pastes pin data or screenshots, log them into a CSV and run `scripts/score_pins.py`.
3. **Seasonal timing**: Pinterest users plan 30–90 days ahead. Flag what to publish *now* to rank for the coming peak (today's date determines the window).

Write results with `templates/trend-brief.md`. Cite every source URL. Say clearly which numbers were observed and which are estimates. **Never invent metrics.**

### Phase 3: Decode the Viral DNA
For each top outlier, fill the **DNA card**:
- **Archetype**: match it to one of the 12 in `viral-pattern-library.md`
- **Hook mechanic**: curiosity gap, contrarian, number, identity call-out, before/after, or "permission slip"
- **Emotional trigger**: relief, validation, aspiration, rebellion, FOMO, or belonging
- **Search intent**: what someone typed to find it
- **Visual grammar**: layout, text-to-image ratio, font weight, color temperature
- **Save trigger**: why someone would *save* it (reference value, checklist, future self)

### Phase 4: Empire Remix
Rebuild each DNA card for Intentional Empire:
1. Keep the **archetype, hook mechanic, emotional trigger and intent**.
2. Swap the topic to an Intentional Empire pillar, and apply the voice ("defiant healing over toxic positivity", sovereign, nervous-system aware).
3. Apply the **visual system** in `brand.json` and `brand-kit.md` (blue = authority/calm, green = growth/money, gold = crown and highlight only, max 10% of the canvas).
4. Write SEO: a keyword-led title (≤ 100 chars), a 2–3 sentence description with 3–5 natural keywords, a board name and alt text.
5. Run the **Transformation Test**. Every answer must be YES:
   - Would the original creator fail to recognise their pin in ours?
   - Is all text written fresh, not paraphrased line by line?
   - Are all images ours, licensed, or generated?
   - Does it carry an Intentional Empire idea (framework, POV, story) the original didn't?
6. Run the `references/compliance.md` check on anything touching money, investing, debt, income or healing. Make the copy safe through its framing rather than adding hedges. A disclaimer only goes at the end of the description, and only for specific financial steps or crisis-level healing topics.

Output with `templates/pin-pack.md`.

### Phase 5: Produce
Pick the best route available:
- **Canva connector** (if connected): use `mcp__Canva__list-brand-kits` to find the Intentional Empire kit, then `generate-design` / `create-design-from-brand-template` with the pin copy. Size: 1000×1500.
- **Local render**: write a spec JSON and run
  `python3 .claude/skills/pinterest-viral-empire/scripts/render_pin.py spec.json --out <dir>`
  This produces branded PNG text-overlay pins for quick drafts and A/B variants.
- **Notion**: if the user runs the IntentionalEmpire Content OS, hand the pin pack to the `intentionalempire-content-os` skill to schedule it.

Always produce **3 variants per winning concept**: same idea with a different hook, a different layout and a different color dominance (blue-led, green-led, ivory-led). Pinterest rewards fresh pins.

## Output standards
- Lead with the 3 highest-leverage moves, then the detail.
- Keep sections modular and scannable, with no walls of text (decision-fatigue aware).
- Every pin concept includes: archetype, hook, on-pin text, title, description, keywords, board, CTA/destination, colorway, and its source pattern URL (for internal reference only, never published).
