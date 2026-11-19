# Intentional Empire: Pinterest Viral Engine ✦

A Claude Code **skill + agent** that researches Pinterest trends, decodes why pins go viral, and rebuilds those patterns for Intentional Empire in the brand's Blue ✦ Green ✦ Gold palette.

![Sample pins](.claude/skills/pinterest-viral-empire/examples-preview.png)

## What's inside
| Path | Role |
|---|---|
| `.claude/skills/pinterest-viral-empire/SKILL.md` | The 5-phase Empire Loop: Intake → Trend Recon → Decode DNA → Empire Remix → Produce |
| `.claude/agents/pinterest-trend-scout.md` | Research subagent that writes a cited trend brief |
| `.../brand.json` | **Brand colors & fonts. Edit the hex codes here.** |
| `.../references/` | Brand kit, research playbook, 12 viral archetypes, compliance guardrails |
| `.../templates/` | Trend brief + pin pack formats, example render spec |
| `.../scripts/score_pins.py` | Ranks pins by velocity and outlier score from a CSV |
| `.../scripts/render_pin.py` | Renders branded 1000×1500 pins (`--all-colorways` for A/B variants) |

## Use it
Open this repo in Claude Code and say things like:
- "Run a Pinterest sprint for Economic Sovereignty"
- "Trend scout: what's rising in healing and money mindset for January?"
- "Remix these 5 viral pins for my brand" (paste links or screenshots)

Quick render:
```bash
python3 .claude/skills/pinterest-viral-empire/scripts/render_pin.py \
  .claude/skills/pinterest-viral-empire/templates/example-spec.json --out pins --all-colorways
```

**Principle:** copy the *pattern*, never the pin. Every remix passes a Transformation Test and a financial-compliance check.
