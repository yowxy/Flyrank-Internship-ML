# Prompt Ladder — "Explain this data" → a refresh queue an editor can use

Track: ML intern (FlyRank content-refresh lane). Model: same assistant for all six runs, only the prompt changed. File attached every time: `data/raw/content_refresh_anonymized.csv`. Raw run logs: `/tmp/ladder/` (prompts + full outputs); excerpts below are representative, trimmed only for length.

---

## V0 — Baseline (the embarrassing one)

**Prompt (full):**
> Explain this data

**Output (full — all 149 words of it):**
> This dataset appears to contain content performance data! Here's a general explanation: Your data has rows (observations) and columns (variables). To understand it, you should: 1. Load the data with pandas... 2. Check the shape... 3. Look at data types... 4. Check for missing values... 5. Plot distributions... 6. Compute correlations... 7. Try a model — Random Forest is a great default! ... Common pitfalls: overfitting, data leakage... Let me know which of these you'd like to explore further!

**Notes:** no goal, no audience, no file reading — a tutorial that fits any CSV on earth. This is the hole the ladder climbs out of.

---

## V1 — Layer added: clearer goal

**Prompt (full):**
> My goal: decide which pages to refresh first out of thousands of content pages. Explain this data

**Output (excerpt):**
> ...focus on: 1. **Decline signals** — pages whose recent traffic dropped vs. an earlier period... Compute a trend: compare last-30-day vs. prior-30-day impressions. 2. **Opportunity signals** — pages ranking on page 2+ with decent impressions... 3. **Effort signals** — older, thinner content is usually cheaper to refresh... Suggested approach: build a scoring rule combining decline + opportunity, sort descending, and work the list top-down...

- **What changed in the prompt:** one goal sentence, nothing else.
- **What improved in the output:** it stopped lecturing on pandas basics and started reasoning about refresh ordering — decline/opportunity/effort is a real prioritization shape, not a tutorial.
- **What still failed:** it never opened the file ("your dataset likely contains...") — every claim is hedged, zero real numbers, and it quietly assumes columns (last-30-day splits) it hasn't verified exist.
- **Next:** tell it who is reading, so it stops writing for a generic analyst.

## V2 — Layer added: defined audience

**Prompt adds:** `My reader is a content editor: non-technical, busy, skimming between meetings.`

**Output (excerpt):**
> **The short version:** Every row is one page... Your job: find the pages slipping fastest and fix those first... **What I'd do Monday morning:** pull the 50 pages with the steepest traffic drops that still get meaningful impressions, and start there. Skip anything with near-zero traffic — refreshing a page nobody visits helps nobody.

- **What changed in the prompt:** audience line only.
- **What improved in the output:** readability transformed — short sentences, a verdict up front, a Monday-morning action. An editor could skim this between meetings, which was the point.
- **What still failed:** plain words, empty calories. "50 pages," "meaningful impressions," "near-zero" are invented thresholds with no grounding in the file — it sounds decisive while knowing nothing.
- **Next:** force it to look at the actual file by pasting verified context in.

## V3 — Layer added: real context ⚠️ (the one that made it worse)

**Prompt adds:** a verified context block (30,000 rows / 32 clients; decline mix 16,262 down = 54.2%; ×100 rate scale; avg_position = 0 means no data; medians 731 impressions / 1 click / 10.8 position; missingness follows content_type; trend columns are label machinery, never features).

**Output (excerpt):**
> **Scale:** 30,000 content items across 32 clients and 44 columns — an average of 937.5 pages per client... median impressions_90d is 731 while the mean is 5,200.37 (std 16,838.02, max 517,715) — heavily right-skewed, consider log1p transforms... 1,205 rows (4.0%) have avg_position = 0... use has_-flags rather than blind fillna(0)... **Recommendation:** the editor should... [continues for 6 more paragraphs]

- **What changed in the prompt:** context block only.
- **What improved in the output:** specificity — real counts, real gotchas (×100 rates, the zero-position trap, the leakage quarantine). Nothing is invented anymore.
- **What still failed:** usability got *worse*, honestly. It handed a busy editor a statistics dump — means, stds, "937.5 pages per client" trivia — and buried the refresh decision under six paragraphs. More truth, less action. Context without a container is just a longer email nobody finishes.
- **Next:** constrain the shape of the answer so the numbers serve the decision.

## V4 — Layer added: specified output format (the biggest win)

**Prompt adds:** verdict line + exactly-3-row table (Group | Why first | How many) + one do-NOT-touch line + 150-word cap, nothing else.

**Output (full — 138 words):**
> **Verdict:** 16,262 of 30,000 pages (54%) are declining — the fix list starts there. [3-row table: declining + high impressions / declining at positions 11–20 / new pages with early traffic] **Do NOT touch:** flat/zero-traffic pages nobody visits.

- **What changed in the prompt:** format spec only.
- **What improved in the output:** everything about actionability. Same facts as V3, but the editor gets a verdict, three groups, and a skip-line in under 150 words. The format forced the model to choose instead of enumerate — choosing is the whole job.
- **What still failed:** the "How many" column went hand-wavy ("~top slice," "subset") — the word cap squeezed out the exact band counts, so precision was traded for brevity.
- **Next:** demand honesty about the guesses instead of letting brevity hide them.

## V5 — Layer added: stated assumptions + verification

**Prompt adds:** state assumptions (guessed vs proven) before answering; end with one `Verify:` line naming the check that would prove the verdict wrong.

**Output (excerpt):**
> **Assumptions:** I assume "needs attention" = declining label; I assume high-impression decliners cost the most traffic (counts proven, cost not — no revenue data). Guessed: the position 11–20 band size... **Verify:** recount trend_direction == "down" after any re-export; if it isn't ~54%, this verdict is stale.

- **What changed in the prompt:** assumptions + verification lines only.
- **What improved in the output:** a small, real gain — it flagged the unverified band count instead of smoothing over it, and the verdict is now falsifiable (recount the label). First version I'd hand to someone without a disclaimer meeting.
- **What still failed:** diminishing returns — the table itself barely moved from V4, and the extra lines push against the word cap. This layer polishes; it doesn't transform.
- **Next tried:** nothing further — the ladder stops here; remaining weakness (exact band counts) needs code execution, not more prompting.

---

## Final reusable prompt (stranger-ready)

```text
My goal: decide which [ITEMS] to [ACTION] first out of [N] candidates.
My reader is a [ROLE]: [reading context, e.g. non-technical, busy, skimming].
Explain the attached data ([FILENAME], [GRAIN, e.g. one row = one page]).

Real context from the file (I checked):
- [rows, groups, columns, time window]
- [outcome mix with counts + shares]
- [measurement gotchas: scales, sentinel values like 0 = no data, missingness pattern]
- [columns that derive the outcome and must never be inputs]

Output format (follow exactly, nothing else):
1. One-line verdict: how many items need attention, as a count and a share.
2. A table with exactly 3 rows: the top 3 groups to act on first (columns: Group | Why first | How many).
3. One "do NOT touch" line: what to skip and why.
4. Max 150 words total.

Before answering, state your assumptions (guessed vs proven by the context above).
End with one line starting "Verify:" naming the single check that would prove your verdict wrong.
```

**How to reuse:** replace every `[BRACKET]` with your track's facts; keep the one-layer-per-line discipline — if you add a line, re-run and compare before adding the next.

---

## Self-check against pass/revise

- [x] Six runs (V0 + V1–V5), each version tied to exactly one named layer (goal → audience → context → format → assumptions/verification).
- [x] Notes describe output changes ("stopped lecturing on pandas," "handed the editor a stats dump," "forced the model to choose"), not just prompt changes.
- [x] Honest failure present: V3 made usability worse (specific but unactionable); V5 logged as diminishing returns.
- [x] Final prompt is stranger-ready: all context slots are `[BRACKETED]`, no internship-specific knowledge assumed.
