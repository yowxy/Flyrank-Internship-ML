# Refresh Scout — weekly content-refresh triage agent

**Every Monday, turn a 30,000-page portfolio into a top-10 refresh queue with reasons an editor can act on in 15 minutes.**

Refresh Scout is a small, scripted agent. One command fetches the live portfolio, scores every page under a transparent leakage-free rule, screens the data for prompt-injection attempts, compares its picks to the base rate, and renders a Markdown brief plus a CSV queue — as a **draft for human approval**. It cannot publish, send, or write anything outside `work/outputs/`.

- **Spec:** `work/capstone_agent_spec.md` (job, tools, guardrails, rejected alternatives)
- **Build log (what broke, what changed):** `work/refresh_scout_build_log.md`
- **Source:** `work/scripts/refresh_scout.py` (single file, no service to run)
- **Receipts:** `work/outputs/refresh_scout_receipts.json`, `refresh_brief_YYYY-MM-DD.md`, `refresh_scout_run_capture.txt`

## What it does, and for whom

- **What it does:** ranks pages by refresh worthiness using four observable signals (visibility, staleness, position opportunity, content depth), attaches a human-readable reason code and a suggested action (`refresh`, `expand_and_refresh`, `refresh_and_review_ctr`, `monitor`) to every pick, and writes a one-page brief an editor can read top-down.
- **Who acts on it:** a junior SEO analyst / content editor who can work the top of the list in a ~15-minute Monday review. It is a **review order**, not an automatic decision — every row is a candidate, and the brief is a draft until a human approves it.
- **Success it is built for:** editor accepts ≥6 of 10 picks without rework; zero picks citing an invented or label-derived metric; full run under 5 minutes on CPU at $0 cost.

## Quickstart (a stranger can follow this)

Requires Python 3.10+ and the two libraries the agent imports (pandas, numpy). The dataset ships in the repo (30,000 pseudonymized rows × 44 columns; no client names, URLs, or queries).

```bash
git clone https://github.com/yowxy/Flyrank-Internship-ML.git
cd Flyrank-Internship-ML
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 1. Frozen evals only — offline, deterministic, ~1 s, writes nothing:
python work/scripts/refresh_scout.py --eval-only

# 2. Full end-to-end run — reads the live CSV, writes brief + queue + receipt, ~2 s:
python work/scripts/refresh_scout.py --top-k 10
```

You should see `[evals] 6/6 frozen cases passed (offline)`, then `[fetch] live portfolio: 30000 rows`, then `[done] core job complete. Brief is a DRAFT for human approval.`

> `requirements.txt` installs the whole repo stack (sklearn, matplotlib, duckdb…). Refresh Scout itself only needs pandas + numpy; the rest is for the capstone pipeline.

## Usage examples

```bash
# Weekly run: top-10 queue for today, written to work/outputs/
python work/scripts/refresh_scout.py --top-k 10

# Bigger or smaller queue
python work/scripts/refresh_scout.py --top-k 25

# Scope one client segment on demand (<2 min); 32 client IDs in the snapshot
python work/scripts/refresh_scout.py --segment client_02d20bbd7e

# Point at a different snapshot, or write somewhere else (e.g. a scratch dir)
python work/scripts/refresh_scout.py --input path/to/snapshot.csv --out-dir /tmp/scout

# Gate only: run the frozen evals and exit (used by CI)
python work/scripts/refresh_scout.py --eval-only
```

**What a run produces**

| File | Committed? | What it is |
|---|---|---|
| `work/outputs/refresh_brief_<date>.md` | yes | The one-page editor brief (rank, score, reasons, observed signals, action) |
| `work/outputs/refresh_queue_<date>.csv` | no (gitignored) | Machine-readable queue for downstream tooling |
| `work/outputs/refresh_scout_receipts.json` | yes | The receipt every number in this README traces back to |
| `work/outputs/refresh_scout_run_capture.txt` | yes | Byte-unedited `script` transcript of a real run |

The brief never prints raw page IDs, URLs, queries, or client names — only truncated `content_id` and aggregated numeric signals (`impr90d`, `upd_age`, `pos`, `ctr`), per `DATA_USE.md`.

## Architecture sketch

```text
data/raw/content_refresh_anonymized.csv   (live, read-only, 30k rows)
        │
        │  Tool 1  query_portfolio(csv, segment?)      read-only load
        ▼
    working frame ─────────────────────────────────────────────────┐
        │                                                            │
        │  Tool 2  score_pages(frame)                                │
        │     visibility / freshness / position-opportunity / depth  │
        │     → refresh_score, reason_codes, suggested_action        │
        ▼                                                            │
   injection screen (untrusted text fields — flag, never follow)     │
        │                                                            │
        │  Tool 3  compare_to_baseline(frame, k)                     │
        │     base_rate_declining vs P@k on the declining label      │
        ▼                                                            │
        │  Tool 4  render_brief(queue, metrics, flags)  ◄────────────┘
        ▼
work/outputs/refresh_brief_<date>.md  +  refresh_queue_<date>.csv  +  receipt.json
```

Four single-purpose tools, each returning inspectable JSON/Markdown. Ranking math is deterministic Python (pandas/numpy) — **no LLM sits in the scoring path**, so every number is reproducible offline. The frozen evals run first on every invocation and act as a kill switch: any regression freezes the queue and writes no brief.

## Eval results (v2 — after the first review pass)

Six frozen eval cases were written **before** the build (`work/capstone_agent_spec.md` §6) and run on a hand-built 12-row fixture, offline, with a mocked LLM. Current status: **6/6 pass, 0 hallucinations.**

| # | Case | Checks | Result |
|---|---|---|---|
| 1 | Clear decliner | ranks top-3 with cited signals | PASS (rank 1) |
| 2 | Low-traffic sharp drop | recall — reaches top-10 | PASS (rank 3) |
| 3 | Stable evergreen | precision — stays below median | PASS (rank 7) |
| 4 | Ambiguous / missing `freshness` | says `monitor`, not a confident pick | PASS |
| 5 | Adversarial injection in a text field | flagged and never followed | PASS (1 flag) |
| 6 | Leakage probe | brief cites no label-derived column | PASS |

**v1 → v2 (what the evals caught).** The first eval run scored **4/6**. Case 3 failed because `position_opportunity_score` rewarded good positions with no staleness condition — a healthy evergreen floated up on visibility alone; fixed by staleness-gating that term. Case 6 failed because the brief's own guardrail footnote named the forbidden columns, tripping the no-citation check; reworded to "label-derived columns." Full root-cause write-up: `work/refresh_scout_build_log.md`.

**Honest negative result (kept, not tuned away).** On the full 30,000 rows, `P@10` against the declining label is **0.20 versus a 0.5421 base rate** (`work/outputs/refresh_scout_receipts.json`). The transparent rule is a **weak ranker of recent decline** — single-signal checks agree (visibility P@10 ≈ 0.5, staleness ≈ 0.6, deep-position ≈ 0.1). The one feature that would lift it, the 30-day impressions ratio, *is* the label (`trend_pct`) — leakage. So the agent is scoped and documented as triaging **refresh worthiness** (stale + visible + thin/weak-engagement), and beating it on decline prediction is the explicit job of the ML-08 model follow-up on the same split.

## Limitations

- **Weak decline predictor by design.** P@10 = 0.20 vs 0.5421 base rate. It orders *refresh-worthy* pages well; it does not claim to predict decline (see above).
- **No causal claim.** It ranks candidates for review. Nothing here says a refresh will recover traffic — that requires an experiment, not a ranker.
- **One frozen snapshot.** A 90-day aggregate cannot show seasonality; a page about to recover on its own can still appear.
- **No LLM reasoner in v2.** Per-pick prose is templated from observed signals; an LLM rationale is planned for v3 *behind* the frozen eval gate, to avoid adding non-determinism or a data-exfiltration surface before evals can guard it.
- **Eval fixture is 12 hand-built rows**, not a 200-row synthetic set. Each case's mechanism is inspectable by hand; scale-up is a hardening task.
- **Not scheduled.** "Weekly" is the intended cadence; the agent is invoked by hand/cron, it does not own a scheduler.
- **Schema-coupled.** It assumes the starter schema (`DATA_USE.md`, `docs/data-dictionary.md`). Schema drift triggers the kill switch (freeze + "re-validate"), not a silent wrong answer.
- **Treated as untrusted input.** All data text fields are screened for embedded instructions and flagged; the agent never follows them and never prints raw sensitive fields.

## Safety and guardrails (by construction, not by promise)

- Label-derived columns (`trend_direction`, `trend_pct`) are **never scoring features** — enforced by an in-code assertion and eval case 6.
- No network, publish, send, or overwrite tool exists in v2: the brief is a draft file for human approval. Output is limited to `work/outputs/`.
- `avg_position == 0` means "no data", never rank zero.
- Data-safety: only truncated IDs + aggregated numeric signals leave the run; no URLs, queries, client names, or secrets.

## Reproduce / verify

```bash
python work/scripts/refresh_scout.py --eval-only   # 6/6, offline, ~1 s
python work/scripts/refresh_scout.py --top-k 10    # end-to-end, ~2 s, CPU-only
```

Deterministic (seed-free; the rule is arithmetic): repeat runs produce identical top-10s. Confirm the committed receipt matches: `work/outputs/refresh_scout_receipts.json` (`rows_scored: 30000`, `base_rate_declining: 0.5421`, `precision_at_10: 0.2`, evals all `true`).

## Demo video

A 3–5 minute screen-recorded, narrated live run — including one design decision (baseline-before-model / leakage-free scoring) and one limitation (weak decline ranker, P@10 0.20) explained on camera — is scripted in `work/agent_demo_script.md`. Link goes in `work/demo_video.txt` (one line).

## Honest about AI

The agent's code, its first draft README, and the evals were built with an AI assistant. The analysis decisions are the intern's: the tool set, the guardrail list, the frozen-eval cases, the leakage rule, and the choice to keep the weak P@10 as an honest result rather than tune it away. Every number here traces to a committed receipt or the unedited run capture.
