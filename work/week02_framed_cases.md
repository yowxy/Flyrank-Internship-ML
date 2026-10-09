# Week 2 — Framed Cases (Work That Speaks for Itself)

**Voice card:** direct, warm, plain, specific, no buzzwords. Short sentences. Numbers with denominators.

> Standing instruction for my AI workspace: use this voice for everything drafted for me. If a line sounds like a generic AI bio, rewrite it the way I'd say it to a friend.

**One person, one action:** a hiring manager at a small tech team → email me to set up a chat.

---

## Case 1 — Which page should an editor fix first? (framing the refresh queue)

**The problem.** FlyRank publishes content into client sites, and pages quietly decay in search. Out of 30,000 pages across 32 clients, nobody can fix everything. The editor's real question is order: which page first? "Predict decline" is not a task until you say who acts on it.

**What I did and decided.** I framed the lane as binary classification used as a ranking queue: predict a per-page decline flag (`is_declining_label`, 1 when last-30-day impressions sit 20%+ below the prior 30 days — 16,262 of 30,000 rows, base rate 0.542), then sort pages by predicted probability. I decided the metric before training: ROC-AUC ≥ 0.70 plus precision@200 ≥ 0.65, both on held-out clients, because an editor can only work the top of the list and a within-client split would flatter us. I also wrote down the label's weak point instead of hiding it: −20% is a human line, so a page at −19% and one at −21% get different labels.

**What came of it.** A one-paragraph frame plus an executed notebook (`work/notebooks/w02_ml_task_framing.ipynb`) that states the decision, the target, the bar, and the error costs — false alarms waste editor hours, misses let traffic bleed. Where it breaks: the bar is a promise, not a result; no model is trained yet. Next time I would time-box the framing instead of rewriting the paragraph three times.

## Case 2 — The hand rule that failed (baseline before any model)

**The problem.** FlyRank already flags pages with hand-written rules, and rules are the honest baseline: if a one-line threshold orders the queue well enough, there is nothing for ML to beat.

**What I did and decided.** Before touching a model, I tested the most generous hand rule I could write — flag pages with average position worse than 20 AND untouched for 180+ days — and scored it as a queue on all 30,000 rows. I decided the rule competes on the same metric as the future model (precision, recall against the decline label), so the comparison stays fair.

**What came of it.** The rule flagged 26 pages at precision 0.538 — basically the 0.542 base rate — with recall 0.001: it caught 14 of 16,262 declines and missed the rest. Class medians overlap on every obvious cutoff (declining vs healthy median position 11.3 vs 10.0), so no single threshold separates them. That measured failure is what earns ML its place. Where it breaks: I tested one rule, not the best possible rule — a tuned multi-threshold rule could do better, and notebook 04 will build it. Next time I would test two or three rule variants instead of stopping at one.

## Case 3 — The label trap (leakage check, in progress)

**The problem.** The decline label is computed from `trend_direction`, which is computed from `trend_pct`. Any feature list that includes those columns is not predicting decline — it is rereading the answer key. That is the most common way this project silently fakes a good score.

**What I did and decided.** I wrote the quarantine into the data contract first (`work/notebooks/w03_data_contract.ipynb`): `trend_pct`, `trend_direction`, and the label itself are never features; IDs are grouping keys for client-holdout splits, never inputs. I decided the contract comes before modeling, because a leak caught after training wastes the whole run.

**What came of it.** Honestly: the contract is written, the leakage-demo notebook (`w03_feature_leakage_check.ipynb`) is still a skeleton with no executed outputs. The mechanism is documented, the demonstration is pending — I am not claiming a caught leak, only a trap named before it could bite. Where it breaks: an unwritten demo proves nothing yet. Next time I would execute the demo in the same sitting as the contract instead of splitting them across days.

---

## Bio + contact

**Bio:** I'm an ML intern and student. I build small models on messy search data and write down where they fail — my refresh queue beats a hand rule and says exactly where it breaks.

**Contact line:** Hiring for a junior who ships working prototypes instead of polished demos? Email me and I'll walk you through the repo.

---

## Before / after (generic AI line vs mine)

- **Before (generic AI):** "Results-driven ML enthusiast leveraging cutting-edge algorithms to deliver impactful, data-driven solutions."
- **After (mine):** "I build small models on messy search data and write down where they fail."

Why the edit holds: the before could describe anyone and claims nothing checkable. The after names the data (messy search), the scope (small models), and the proof (limits written down) — a stranger can open the repo and verify each word.

---

## Spots I guessed — fix before submitting

- Your three personal voice words (I used the brief's default style; swap in words you'd actually say).
- Case 3 has no executed result yet — run `w03_feature_leakage_check.ipynb` top to bottom, then replace "pending" with the measured number.
- The shortlist bar (AUC ≥ 0.70, P@200 ≥ 0.65) is mine from notebook 02 — keep it only if you stand behind it.
- Bio/contact assume the "email for a chat" action from week 1 — change if your action changed.
