# Refresh Scout MVP — build log (Checkpoint 1)

Author: ML Intern (FlyRank track) · Date: 2026-10-13 · Platform: scripted agent (per FL-06 spec §8)

## What was built

`work/scripts/refresh_scout.py` — one command runs the whole core job with no mid-run hand-editing:

```
python work/scripts/refresh_scout.py --top-k 10
fetch (live CSV) → score (transparent rule) → screen → compare → render brief
```

Live connection: Tool 1 reads `data/raw/content_refresh_anonymized.csv` (30,000 rows) read-only on every run.
Outputs: `work/outputs/refresh_brief_<date>.md` (committed), `refresh_queue_<date>.csv`
(gitignored by design), `refresh_scout_receipts.json` (committed receipt),
`refresh_scout_run_capture.txt` (unedited `script` transcript of the run).

## Real iteration (what broke, what changed)

1. **First eval run: 4/6.** Cases 3 and 6 failed, and the agent correctly froze (no brief written — the kill switch works).
   - *Case 3 (stable evergreen ranked 5th, above median):* root cause was a genuine design flaw, not a bad test.
     `position_opportunity_score` rewarded good positions × visibility with no staleness condition, so a
     healthy page (updated 20 days ago, position 4) floated on visibility alone. Fix: staleness-gate the
     position term (`days_since_last_update >= 90` multiplier) and require the same gate in the
     `page_one_decay_risk` reason code. Re-run: evergreen rank 5 → 7. PASS.
   - *Case 6 (leakage probe):* the brief's own guardrail footnote named the forbidden columns, tripping the
     no-citation check. Fix: reworded to "label-derived columns" (the check now guards the property that
     matters — no signal values from label-derived columns appear in picks).
2. **Pandas `UserWarning` (regex match groups in `str.contains`).** Fixed by converting the injection pattern
   to non-capturing groups. Zero warnings on the final run.
3. **Top-of-list hand review (skill step 5) found a weak pick pattern:** ranks 1–3 carried `monitor` despite
   `page_one_decay_risk` — the action map never promoted that reason. Fix: `page_one_decay_risk → refresh`.
   Also verified the `upd_age=104d` cohort on all top picks is real (8,773 rows share that value — a batch
   refresh cohort), not a join bug.
4. **Honest negative result, kept (not tuned away):** P@10 vs the declining label is **0.20 against a 0.5421
   base rate** — the transparent rule is a weak ranker of *recent decline*. Single-signal checks agree
   (visibility P@10 ≈ 0.5, staleness ≈ 0.6, deep-position ≈ 0.1): nothing in the leakage-free feature set
   separates decliners well. I deliberately did NOT add `impressions_last_30d/prev_30d` ratios to boost it —
   that ratio is the label computation (`trend_pct`), i.e. leakage. Conclusion documented in the brief:
   the rule triages *refresh worthiness* (stale + visible), and beating it on decline prediction is the
   explicit job of the ML-08 model follow-up, evaluated on the same split.

## Spec deviations (FL-06 → MVP), with reasons

| Spec item | Deviation | Why |
|---|---|---|
| 200-row eval fixture | 12-row hand-built fixture (6 probes + 6 fillers) | Hand-verifiable in minutes; each case's mechanism is inspectable. Scale to 200 synthetic rows in hardening. |
| `query_portfolio(sql)` via DuckDB | Plain pandas CSV read | DuckDB adds nothing for a single 30k-row snapshot; pandas keeps the MVP dependency-free. DuckDB returns for the warehouse phase. |
| LLM reasoner (Gemini free tier) in the loop | Cut from MVP — brief uses templated editor language | Every LLM call is a non-determinism + data-exfiltration surface; the ranking/brief pipeline is fully verifiable without it. LLM re-enters in v2 for per-pick rationales behind the frozen eval gate. |
| Reference `02_baseline_score.py` logic ported as-is | Dropped `declining_with_demand` reason (used `trend_direction`) | It consults a label-derived column — leakage by the repo's own rule. Documented, not silently kept. |
| 2-min video capture | `script` transcript (`refresh_scout_run_capture.txt`) + record command below | No display recorder in this environment; transcript is byte-unedited. Intern records the video with: `python work/scripts/refresh_scout.py --top-k 10` (≈15 s) plus a scroll through the brief. |

## Eval-criteria self-check

- [x] Core job completes end to end without mid-run hand-editing (exit 0, artifacts written by the script).
- [x] ≥1 live tool/data connection (live CSV read every run; evals also gate the run).
- [x] Matches spec or deviations documented (table above).
- [x] Real iteration shown (4/6 → 6/6 with root causes, not a clean retroactive story).
- [x] Unedited run capture (`refresh_scout_run_capture.txt`, `COMMAND_EXIT_CODE="0"` footer intact).

## Reproduce

```
python work/scripts/refresh_scout.py --eval-only   # frozen evals, offline, ~2 s
python work/scripts/refresh_scout.py --top-k 10    # full end-to-end run, ~15 s CPU
```

## Re-verification (2026-10-14, senior review)

- Fresh end-to-end run exit 0: `6/6` evals, `30000` rows fetched live, `P@10=0.20`
  vs base rate `0.5421`, brief + queue + receipts regenerated for `2026-10-14`.
  Deterministic: top-10 identical to 2026-10-13 run (same scores, same order).
- Leakage re-check: `trend_direction`/`trend_pct` occur only in guardrail
  constant, eval fixture, eval-only label derivation, and the no-citation
  assert — zero occurrences in scoring math (`visibility/freshness/position/depth` block).
- Data-safety re-check: brief contains only truncated `content_id` + aggregated
  numeric signals (`impr90d/upd_age/pos/ctr`); no URLs, queries, names, or dates invented.
- `scripts/` pristine (`git diff HEAD -- scripts/` empty); queue CSV correctly
  gitignored per `work/**/*.csv`, brief/receipts/capture committable.
- Run capture overwritten unedited via `script` (headers + `COMMAND_EXIT_CODE="0"`
  footer intact). Video substitute: intern records with
  `python work/scripts/refresh_scout.py --top-k 10` (~15 s) + brief scroll for the ~2-min raw capture.
