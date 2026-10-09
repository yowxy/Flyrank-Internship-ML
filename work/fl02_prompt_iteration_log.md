# FL-02 — Prompt Iteration Log: data-contract check (G1)

**Task (from FL-01 audit, target G1):** data-contract check on the 30k-row starter CSV. Done well means: (1) asserts all 44 columns present with documented dtypes, (2) `trend_direction` and `trend_pct` absent from every feature list, (3) run finishes in <60s and writes a committed JSON receipt. Model: same assistant, same attached file (`data/raw/content_refresh_anonymized.csv`) for all six runs — only the prompt changed. Full run logs: `/tmp/fl02/`.

---

## V0 — Naive one-liner

**Prompt:** `Write a data contract check for my CSV`

**Output:** a lecture on what data contracts are (Pandera, Great Expectations, dbt), a placeholder schema with `column_a`/`column_b`, and four questions back to me (columns? grain? quarantined features?).

**Note — what changed and why:** nothing improved yet; this is the floor. The output failed because the prompt contained zero task facts, so the model stalled: it taught the concept and asked me to do the specification work. Lesson: a prompt with no nouns gets a tutorial.

## V1 — Technique: role assignment

**Prompt adds:** `You are a senior data engineer who writes production validation code, not tutorials.`

**Output:** same request, now answered with authority — declarative `CONTRACT` dict at top, fail-fast `sys.exit(1)`, "industry best practice" narration. But every load-bearing list is still `[...]` / `[]` for me to fill in.

**Note:** tone and code shape changed (scaffolding an engineer would recognise), but zero output facts changed — it still knows nothing about my file. Role assignment upgrades voice and structure, not knowledge. Next weakness to attack: the model has no facts to be authoritative *about*.

## V2 — Technique: context and motivation

**Prompt adds:** the FlyRank slice facts (30k rows, 44 cols, dictionary ref), the three guarantees, the <60s + JSON receipt requirement, and the cost of a miss (a fake model ships).

**Output:** pivoted to the real problem — it named the two label-machinery columns, and made its best decision of the ladder so far: check the *feature lists* in `scripts/ml_utils.py`, not just the CSV, because "the leak lives in ml_utils.py, not in the data file." Still sketchy (`...` in the code, ad-hoc receipt).

**Note:** first version that could only be about my task — motivation ("a leaky feature once faked a score") focused it on leakage over generic schema trivia. Context supplies the nouns; role supplied the verbs. Next weakness: asserts are still vague, style still generic.

## V3 — Technique: few-shot examples

**Prompt adds:** two GOOD asserts (exact style to match) and two BAD patterns (message-less assert; CSV-only checking).

**Output:** concrete asserts in house style — `assert "trend_pct" not in feats, "LEAK: trend_pct computes the label"`, grain check on `content_id`, domain check on `avg_position` — plus its own caveat that hardcoded 30,000 will false-alarm on the next drop.

**Note:** biggest single quality jump in code content: examples calibrated strictness better than any instruction did ("name the failure mode in plain words" never appeared in my prompt — it came from imitating the GOOD examples). Few-shot taught by showing. Next weakness: one unstructured blob, caveats buried, receipt schema ad hoc.

## V4 — Technique: output structure

**Prompt adds:** exactly four sections in order (checks table → script → receipt schema → limits), stdlib+pandas only, no placeholders.

**Output:** checks table (check / what breaks / fail message), full script skeleton, receipt keys with a filled example (`elapsed_s: 1.8, verdict: PASS`), and a two-bullet limits section (no drift detection; label redefinition stays green).

**Note:** same knowledge as V3, twice the usability — structure forced completeness (the limits section admitted blind spots no earlier version volunteered) and killed placeholders. Output structure is a completeness checklist disguised as formatting. Next weakness: written in one shot, assumptions unsourced (30k ±5% guessed, column set from memory).

## V5 — Technique: step decomposition (+ final)

**Prompt adds:** four visible steps — inventory facts first, quarantine asserts second with one-clause justifications, script third, self-verify against Step 1 fourth (fix or delete anything unsourced).

**Output:** Step 4 caught two real defects and fixed them: hardcoded `len(df) == 30_000` → tolerance vs the last committed receipt; bare `shape[1] == 44` → named set-diff so the 2am reader sees WHICH column drifted.

**Note:** the only version that corrected itself — decomposition turned one guess-pass into draft-then-audit, and the audit found things I hadn't spotted either. Verified for real: I ran the generated check against the actual CSV — `PASS`, 30,000 × 44, zero leak columns in features, **0.17s** (limit: 60s). The ladder's output executes; it isn't a prettier draft.

---

## Cross-model comparison — TO RUN (not run)

I can only execute one model from here, so I did not fabricate Claude/ChatGPT outputs. Run the final prompt below once in each (free tiers suffice; attach the same CSV), then score:

| Dimension | Claude | ChatGPT | Winner + evidence |
|---|---|---|---|
| Leakage asserts (names trend_pct/trend_direction/label + why) | | | |
| Grain/domain checks (uniqueness, sentinels, scales) | | | |
| No placeholders (`...`, `[...]` = fail) | | | |
| Receipt schema exact + filled example | | | |
| Honest limits section (admits blind spots) | | | |
| Runs first try (paste into repo, `time python3 check.py ...`) | | | |

What to look for (be specific, never "both were fine"): which model hardcodes the row count vs tolerancing it; which one checks the feature lists vs only the CSV; which fail messages a tired editor could act on at 2am. Paste the winning output's diff into this section before submitting.

## Final reusable template (stranger-ready)

```text
You are a senior [ROLE] who writes production [ARTIFACT], not tutorials.

Context and motivation: [what system this is, scale/grain/window, column count + dictionary ref].
This [ARTIFACT] exists for one reason: [the failure it must prevent + cost of a miss].
It must guarantee (1) [guarantee], (2) [guarantee], (3) [guarantee].
Constraints: runs in [TIME], writes [RECEIPT/OUTPUT], stack limited to [LIBS].

Examples of what good looks like (match this style exactly):
GOOD: [concrete example] — [why it is good, one clause]
GOOD: [concrete example] — [why it is good, one clause]
BAD: [concrete anti-pattern] — [why it fails, one clause]
BAD: [concrete anti-pattern] — [why it fails, one clause]

Output structure (exactly these sections, in order, nothing else):
## 1. [section] — [what each row/entry contains]
## 2. [section] — [constraints, e.g. no placeholders]
## 3. [section] — [schema + filled example]
## 4. Limits — two bullets max: what this does NOT catch

Work in steps and show each step's result before moving on:
Step 1 — Inventory: list the checkable facts and their source. Do not build yet.
Step 2 — [riskiest part] first, with one-clause justification each.
Step 3 — Build the full artifact.
Step 4 — Self-verify: walk the build against Step 1 and list anything unsourced — fix or delete it.
```

## Self-check

- [x] Five iterations beyond naive (V1–V5), each tied to one named technique.
- [x] Every note explains the observed output difference, not just the prompt change.
- [ ] Cross-model comparison executed — pending your two runs (scorecard above).
- [x] Final template reusable without my context (all specifics are `[BRACKETED]`).
- [x] Real FL-01 task (G1); final output verified by execution, not by reading.
- [ ] Anthropic tutorial basics chapters — background reading, complete it before submitting and note the chapter that changed your V5 thinking.
