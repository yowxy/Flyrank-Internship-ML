# FlyRank ML Internship — Content-Refresh Ranker (capstone)

**Which pages should an editor fix first?** A decision-support ranker that scores 30,000 anonymized search pages and returns a ranked, reason-coded review queue — evaluated on held-out clients, with the failures written down.

> **Also in this repo:** **Refresh Scout**, a scripted weekly triage agent that turns the same anonymized snapshot into a top-10 editor brief (one command, frozen evals, kill switch, no LLM in the scoring path). Docs: `work/AGENT_README.md`. Demo script: `work/agent_demo_script.md`.

## What it does, and for whom

- **What it does:** frames content-refresh triage as ranked binary classification (is a page declining?), trains a transparent hand-rule baseline and a small model ladder (logistic regression, decision tree, random forest), and ships the model that clears a pre-registered bar on 6 never-seen clients.
- **For whom:** content editors who must pick ~50 pages to review per sprint out of 30,000; reviewers/employers who want to see honest ML work — baseline first, leakage checks, error analysis, and explicit limits — not a leaderboard headline.

Headline result (committed receipt `work/outputs/w05_model_receipts.json`, seed 42, client-grouped holdout):

| Approach | ROC-AUC | P@50 | P@200 |
|---|---|---|---|
| Hand-rule baseline | 0.501 | 0.42 | 0.395 |
| Logistic regression | 0.696 | 0.52 | 0.545 |
| Decision tree | 0.742 | 0.56 | 0.595 |
| **Random forest (shipped)** | **0.747** | **0.78** | **0.705** |

Test base rate 0.391 on 2,325 held-out pages (6 clients). Pre-registered bar: AUC ≥ 0.70 **and** P@200 ≥ 0.65 — cleared on both axes. The model is a queue-head tool: yield falls toward base rate as K grows, which is why several K values are reported.

## Setup (a stranger can follow, no credentials)

One-time, offline:

```bash
git clone https://github.com/yowxy/Flyrank-Internship-ML.git
cd Flyrank-Internship-ML
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

The dataset ships in the repo (`data/raw/content_refresh_anonymized.csv`, 30,000 pseudonymized pages × 44 columns). No client names, domains, URLs, titles, or queries are present; identifiers group the split only, never features. Nothing private is committed under `work/`.

## Usage

End-to-end pipeline (reproduces every number in the paper from committed receipts):

```bash
python scripts/run_all.py
```

Individual stages:

```bash
python scripts/01_prepare_features.py   # build the 60-column feature frame
python scripts/02_baseline_score.py     # hand-rule baseline + receipts
python scripts/03_train_model.py        # model ladder + receipts
python scripts/04_evaluate_and_export.py# held-out eval + charts
python scripts/05_build_pdf_report.py   # PDF of the playbook
```

Notebooks (one per week, map to paper sections): `work/notebooks/w01_…` through `work/notebooks/capstone.ipynb`. Run `capstone.ipynb` top to bottom — it recomputes the headline table from `work/outputs/*.json` and asserts all artifacts are present.

Deployed research paper: https://yowxy.github.io/Flyrank-Internship-ML/ (also in `submission/paper_url.txt`).

## Architecture sketch

```
data/raw/content_refresh_anonymized.csv
        |
        v
scripts/01_prepare_features.py  ->  60 model columns (21 numeric + 9 categorical)
        |                                 (13 label/window/ID columns banned)
        v
scripts/02_baseline_score.py    ->  hand rule: stale90 · visible500 · weak_snippet · (21 − position)
        v
scripts/03_train_model.py       ->  logreg / tree / random forest, grouped client-holdout (seed 42)
        v
scripts/04_evaluate_and_export.py->  same-split model vs baseline, AUC + P@K, charts
        v
work/outputs/*.json  +  work/figures/*.svg   ->  docs/index.html (deployed paper)
```

Split design: rows grouped by `client_id`, 6 of 32 clients held out entirely (seed 42). A random row-split flatters the model (AUC 0.757 → grouped 0.747; P@50 0.92 → 0.78); the grouped number is the one shipped. This is the load-bearing design decision.

## Evaluation results (shipped, v2)

These are the committed, re-runnable receipts — not hand-typed claims.

- `work/outputs/w05_model_receipts.json` — model ladder on the held-out split (table above).
- `work/outputs/w06_validation_receipts.json` — before/after split audit: random-row AUC 0.757 vs client-grouped AUC 0.747; gap 0.01.
- `work/outputs/w07_playbook_receipts.json` — queue action mix, monitoring triggers, value scenario (~39 of 50 reviewed pages truly declining at P@50 0.78 vs ~20 at base).
- `work/figures/playbook_precision_at_k.svg` — queue-head yield (Figure 1).
- `work/figures/playbook_archetype_rates.svg` — decline share by archetype (Figure 2).

## Limitations (stated up front, not hidden)

- The label is a **proxy**: a same-window −20% impressions bucket. −19% and −21% get different labels; nothing here predicts a future trajectory.
- **No causal evidence:** no refresh experiment was run. This claims ranking value for ordering review, not that refreshing recovers traffic.
- **Single client-holdout at seed 42:** directional, not a benchmark. A different held-out set can move the numbers.
- **Errors concentrate in the tail:** 0.447 false-alarm share on flagged pages; top-3 error 9.3% vs 37–43% deeper. The queue is human-reviewed, never automatic.
- **Overlapping windows:** 90-day aggregates contain the label's 30-day sub-windows; client-grouping contains the bleed at the boundary but not within a client.
- **Scale:** metrics come from the 30,000-page anonymized slice, not the full ~79M-row release.

## Honest about AI

I drafted this README, the notebook structure, and the paper prose with an AI assistant (Claude via opencode) — it helped with section scaffolding, chart captions, and wording. The analysis decisions are mine: the label definition, the banned-feature list and its in-code assertion, the client-grouped split, the leakage-injection test, the baseline rule, and every number traced to `work/outputs/*.json`. I checked each committed receipt against a fresh notebook run before shipping. AI wrote drafts; I verified the claims.

## Reproducibility

Seeds fixed at 42 throughout. From a fresh clone: `pip install -r requirements.txt && python scripts/run_all.py`, then open `work/notebooks/capstone.ipynb` and run all cells. Every figure and table in the deployed paper traces to a committed JSON receipt or SVG in `work/`.

## License

MIT — see LICENSE.
