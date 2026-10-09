# FL-01 — Workflow Audit (Setup)

Internship + study week. Classification follows Mollick's intern frame:
`just me` / `delegate to AI with review` / `collaborate with AI` / `fully automate`.

## 1. Task table

| # | Task (real week) | Context | Class | Why |
|---|---|---|---|---|
| T01 | Derive graded lab-report proofs and statistical arguments (2x/week) | study | just me | Graded reasoning must be mine; AI algebra looks plausible while wrong and costs marks. |
| T02 | Final go/no-go on refresh predictions and client-facing wording (1x/week) | internship | just me | Accountability and DATA_USE safety cannot be outsourced; I sign every claim. |
| T03 | Boilerplate EDA scaffolding (describe, null-map, dtype table) (3x/week) | internship | fully automate | Deterministic pandas output; scripted once, re-run on every data drop. |
| T04 | Data-dictionary cross-check of all 44 columns (scale/gotchas) (1x/week) | internship | delegate to AI with review | Mechanical comparison AI drafts fast; I verify gotchas like trend leakage. |
| T05 | Warehouse slice aggregation in DuckDB (GROUP BY client/intent) (2x/week) | internship | delegate to AI with review | AI drafts SQL fast; I validate row counts and sums before trusting them. |
| T06 | Signal-audit plots plus trend_pct leakage demonstration (1x/week) | internship | collaborate with AI | I choose hypotheses, AI drafts charts, we iterate on the interpretation. |
| T07 | Hand-rule baseline tuning (copy of 02_baseline_score.py) (1x/week) | internship | collaborate with AI | Threshold trade-offs need my judgment; AI runs the grid and explains deltas. |
| T08 | Model training harness with client-holdout split (LogReg/RF) (1x/week) | internship | delegate to AI with review | Standard sklearn pattern; I check no client appears on both sides of the split. |
| T09 | Related-work literature skim for capstone paper section (2x/week) | study | delegate to AI with review | AI summarises fast; I verify every citation exists before it enters the paper. |
| T10 | Colab environment unblock (duckdb install, HF token via getpass) (2x/week) | internship | collaborate with AI | Pairing unblocks in minutes; I keep secrets out of cells while AI diagnoses. |
| T11 | Commit messages and capstone report copy-editing (4x/week) | internship | fully automate | Style-only transform; diff-reviewed before anything is committed. |
| T12 | Anki flashcard generation from lecture notes (3x/week) | study | fully automate | Bulk Q/A transform; I spot-check 10% and delete weak cards weekly. |
| T13 | Weekly timetable planning across internship milestones (1x/week) | study | delegate to AI with review | AI proposes the schedule; I enforce real constraints (exams, shift work). |

## 2. Three target tasks reused in FL-02..FL-04

| # | Target | Reused in | Done well means |
|---|---|---|---|
| G1 | Data-contract check on the 30k-row starter CSV | FL-02 / ML-04 | 1. Contract asserts all 44 columns present with documented dtypes.<br>2. trend_direction and trend_pct are absent from every feature list.<br>3. Run finishes in <60s and writes a committed JSON receipt. |
| G2 | Signal-audit verdict for each candidate feature | FL-03 / ML-06-07 | 1. Every candidate signal carries a keep/drop verdict with direction.<br>2. Each kept signal shows P@50 delta versus the 0.24 hand-rule baseline.<br>3. Notebook re-runs top to bottom in <5 minutes with seed 42 and 0 leakage columns. |
| G3 | Ranked refresh queue with reason codes | FL-04 / ML-07-08 | 1. Queue sorted by score desc; every row carries a human reason code.<br>2. Top-50 precision reported under client-holdout split, baseline 0.24 beaten.<br>3. Only ~3x lift claimed; no causal language without a design. |

## 3. Toolkit evidence

| Tool | Proof | Location | Status |
|---|---|---|---|
| Claude (free) | screenshot | `work/fl01_workflow_audit/evidence/claude_project.png` | pending-screenshot |
| ChatGPT (free) | screenshot | `work/fl01_workflow_audit/evidence/chatgpt_account.png` | pending-screenshot |
| Anthropic Academy — AI Fluency: Framework & Foundations | export | `work/fl01_workflow_audit/evidence/academy_module1.png` | pending-screenshot |
| Claude Project spec (paste-ready custom instructions) | receipt | `work/fl01_workflow_audit/claude_project_spec.md` | configured |

> Screenshots: open each tool, capture the account/project screen, and save
> it to the path above. The Claude Project spec is paste-ready in
> `work/fl01_workflow_audit/claude_project_spec.md`.

## 4. Self-check (mirrors `validators.py`)

- 13 tasks logged (>=10 required), 2 marked just-me (>=2 required).
- Every row carries a one-line rationale; every target criterion is measurable.
- Raw queries, client names, and secrets are never pasted into AI tools.
