# Pinterest Trend Research Playbook

Goal: find **demand that is rising** plus **proof that a format wins**, and avoid copying what's already saturated.

## 1. Demand signals (what people are searching)
| Source | How to use | Access |
|---|---|---|
| **Pinterest Trends** (trends.pinterest.com) | Filter by region and "growing" trends; compare up to 4 terms; note the yearly peak month | Free; best with a Pinterest business login. Ask the user to paste screenshots or terms if you can't reach it. |
| **Pinterest Predicts** (yearly report) | Pinterest's own forecast of next year's trends. Search "Pinterest Predicts <year>" | Public web |
| **Search autocomplete** | Type a seed ("money mindset", "healing", "vision board") and record the suggestions | User provides, or infer from search results |
| **Guided-search chips** | The colored keyword chips under a Pinterest search = Pinterest's own keyword clusters | User screenshot |
| **Cross-platform lead indicators** | TikTok / IG Reels trends often reach Pinterest 4–8 weeks later. Use VidIQ tools (`vidiq_instagram_tiktok_outlier_search`, `vidiq_keyword_research`) if connected | Connectors |
| **Google Trends** | Confirms seasonality and rising queries | Public web |

**Seasonality rule:** Pinterest users plan ahead. Publish **45–90 days before** a peak (e.g. "vision board" peaks in Dec–Jan, so publish Oct–Nov; "back to school budget" peaks in Jul–Aug, so publish May–Jun).

## 2. Proof signals (what format is winning)
**Outlier hunting** is the most valuable technique:
1. Search each seed keyword and scan the top ~25 results.
2. Log each pin: URL, creator, follower count (if visible), saves/reactions/comments if visible, approximate age, format (static / video / idea / carousel), archetype.
3. A pin is an **outlier** when its engagement is ≥ 3× the creator's typical pin, *or* it ranks highly despite a small account. Small-account winners prove the **format** did the work, not the audience.
4. Put the rows in a CSV and run `scripts/score_pins.py` to rank them.

CSV columns (header row required):
```
url,creator,followers,saves,comments,age_days,format,archetype,keyword,notes
```
Blank numbers are allowed. The script scores whatever is present.

## 3. Saturation check
For each opportunity, rate it:
- **Blue ocean**: rising search, few high-quality pins. *Go now.*
- **Crowded but winnable**: high demand, generic pins. *Win with the Intentional Empire POV and premium design.*
- **Red ocean**: dominated by big brands with identical pins. *Skip, or go long-tail (add "for women", "after grief", "for moms", "Black women", "Aquarius").*

## 4. Niche-crossing (the Intentional Empire edge)
The viral sweet spot is the **intersection** of two territories most creators keep apart:
- money × nervous system ("budgeting when you're in survival mode")
- grief × productivity ("CEO routine for the grieving season")
- numerology × finance ("Life Path 1 money blocks")
- vision board × spreadsheet ("2027 vision board that actually has a budget")

Generate at least 5 crossings per sprint.

## 5. Report honestly
- Cite URLs for every trend and pin.
- Label every number as **observed** (seen directly), **reported** (from a source) or **estimated**.
- If a source can't be reached (Pinterest often blocks automated fetches), say so and ask the user for screenshots or exports rather than guessing.
