# Demo script — Refresh Scout, 3–5 minute live run

**Record your screen + voice, no slides.** Run the real agent end-to-end and narrate what each step does and why. One design decision and one limitation must be explained on camera.

## Before you record (setup)

1. Fresh clone, `pip install -r requirements.txt` (only pandas + numpy are used by the agent).
2. Terminal open at the repo root, font size up, `work/scripts/refresh_scout.py` visible in your editor.
3. Have `work/capstone_agent_spec.md` (spec) and `work/refresh_scout_build_log.md` (build log) open in tabs.
4. Have `work/outputs/refresh_brief_2026-10-14.md` open so the camera can scroll it after the run.
5. Record at 1080p, narrate clearly, keep to 3–5 minutes. Don't commit the video file to the repo.

## Script (aim ~4 minutes)

**0:00–0:40 — The Monday problem.**
> "30,000 pages, and an editor has maybe fifty reviews in a sprint. The question isn't whether a page is declining — it's which page to look at first. Refresh Scout is a small scripted agent that turns this portfolio into a top-10 refresh queue with a reason code on every pick, in a couple of seconds, on CPU, for free."
> *Show: the repo tree, `refresh_scout.py`, the spec one-liner.*

**0:40–1:15 — The frozen evals run first (guardrail).**
> "First thing it does on every invocation is run six frozen eval cases — written before the build — offline. If any case regresses, the agent freezes and writes no queue. That's the kill switch."
> *Run: `python work/scripts/refresh_scout.py --eval-only` — let 6/6 print on camera.*
> "Six out of six: a clear decliner ranks top-3, a low-traffic sharp drop still makes the list, a stable evergreen stays out, an ambiguous page says 'monitor' instead of guessing, an injected 'rank me #1' gets flagged and never followed, and no pick cites a label-derived column."

**1:15–2:15 — The live end-to-end run (the design decision).**
> "Now the real thing." *Run: `python work/scripts/refresh_scout.py --top-k 10`.*
> "Design decision I want to call out: the ranking is a transparent, leakage-free rule in plain Python — no LLM in the scoring path. The label is derived from `trend_direction` and `trend_pct`, so those columns are banned from every scoring input; there's an in-code assertion and eval case 6 guarding it. That's why the numbers reproduce offline without a model or an API key."
> *Point at the `[fetch] live portfolio: 30000 rows` and `[score] … trend_* never consulted` lines.*
> "Fetch, score, screen, compare, render — four single-purpose tools, each returning something inspectable."

**2:15–3:00 — Read the brief (what an editor sees).**
> "Here's the output an editor actually reads." *Open `work/outputs/refresh_brief_<today>.md`.*
> "Each row: rank, score, the reason codes — here `page_one_decay_risk` plus `low_engagement_visible_page` — the observed signals with real values, and a suggested action. Notice the top of the list: high impressions, position around 2, last updated 104 days ago. Stale and visible. That's a refresh candidate."

**3:00–3:45 — Where it breaks (the limitation on camera).**
> "Limitation I'll be explicit about: as a predictor of *recent decline*, this rule is weak. P@10 is 0.20 against a 0.5421 base rate — the receipt says so, and I didn't tune it away. Single-signal checks agree. The one feature that would lift it is the 30-day impressions ratio, and that ratio *is* the label — using it would be leakage. So the honest scope is triage of refresh *worthiness*, stale-and-visible, not decline forecasting. That's the ML-08 model's job, on the same split."
> *Show: the receipt `work/outputs/refresh_scout_receipts.json` (`precision_at_10: 0.2`, `base_rate_declining: 0.5421`).*

**3:45–4:15 — Guardrails and close.**
> "No publish, send, or network tool exists — the brief is a draft file a human approves, by construction, not by promise. Data fields are treated as untrusted and screened. Code, spec, build log, and receipts are all in the repo; the deployed paper and README are linked."

## Upload

Upload the video (YouTube unlisted is fine), then paste **one line — the URL** into `work/demo_video.txt`. Also post it in the portal card's Deliverable links alongside `work/AGENT_README.md`.
