# Demo script — 3–5 minute live run (Assignment 8.1 / FL-09)

**Record your screen + voice, no slides.** Run the real pipeline end-to-end and narrate what each step does and why. One design decision and one limitation must be explained on camera.

## Before you record (setup)
1. Fresh clone of the repo, `pip install -r requirements.txt`, `python scripts/run_all.py` once so outputs exist.
2. Have `work/notebooks/capstone.ipynb` open and ready to run top to bottom.
3. Have `docs/index.html` (deployed paper) open in a browser tab for the closing URL.
4. Record at 1080p, narrate clearly, keep to 3–5 minutes.

## Script (aim ~4 minutes)

**0:00–0:45 — The problem (the Monday scenario).**
> "30,000 pages, an editor has time to review about fifty this sprint. The question isn't whether a page is declining — it's which page to review first. I framed this as ranked binary classification: predict a per-page decline flag, sort by predicted probability, and hand the editor an ordered queue with a reason code for every page."
> *Show: the capstone notebook Section 1 / the deployed paper Introduction.*

**0:45–1:30 — Frame it honestly (label + bar + split).**
> "The label is a proxy — last-30-day impressions more than 20% below the prior 30 days. A page at −19% and −21% get different labels, so I treat every number as directional decision support, not a forecast. I fixed the bar before training: AUC ≥ 0.70 and P@200 ≥ 0.65 on held-out clients. And I split by client, not by row — pages within a client share templates and traffic, so a row split would let the model memorize client quirks and report a flattering number."
> *Show: notebook Section 3 (Methodology) + the split-honesty audit cell (random-row vs grouped).*

**1:30–2:15 — Baseline first (the design decision on camera).**
> "Design decision I want to call out: I tested the hand rule before any model. On all 30,000 rows the generous rule looks great — but recomputed on the honest 6-client holdout it collapses to AUC 0.501 / P@50 0.42. That gap between in-sample and held-out is the whole reason to hold out clients at all. Only then did I train models."
> *Show: notebook Section 3.3 baseline + w04 receipts; the collapse from 0.90 in-sample P@50 to 0.42 held-out.*

**2:15–3:00 — The model result (one chart).**
> "Same split, same metric. Logistic regression 0.696, decision tree 0.742, random forest 0.747 AUC and 0.705 P@200 — both clear the pre-registered bar. The lift comes from modeling feature interactions (sustained visibility, position, freshness), not from 'using ML' generically."
> *Show: Figure 1 `playbook_precision_at_k.svg` and Table 1. Narration: at a ~50-page sprint budget the RF surfaces ~39 truly declining pages vs ~20 at base rate.*

**3:00–3:45 — Where it breaks (the limitation on camera).**
> "Limitation I want to be explicit about on camera: 44.7% of flagged pages are false alarms, and errors concentrate in the tail — 9.3% error at top-3 vs 37–43% deeper. Plus the label is a same-window proxy, there's no causal evidence that refreshing recovers traffic, and this is a single holdout at seed 42, not a benchmark. The queue is safe to use as a review order and unsafe to use as an automatic decision."
> *Show: notebook Section 5 (Limitations) + the 'number that keeps it honest' callout in the paper.*

**3:45–4:30 — What an editor does Monday + close.**
> "Work the top of the queue first with reason codes, run the six-point human checklist before any refresh, and retrain on explicit triggers (base-rate drift, precision@50 below 0.60 for two sprints, editor reject rate above 50%). Deployed paper: [URL]. Code and notebooks: [repo URL]."
> *Show: notebook Section 6 recommendations + deployed paper URL.*

## Upload
Upload the video (YouTube unlisted is fine) and paste the link into `work/demo_video.txt` (one line) and into the showcase thread. Do not commit the video file itself to the repo.
