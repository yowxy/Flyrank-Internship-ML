# Retrospective — for the person I was in Week 1

**What I set out to do.** In Week 1 I wanted to prove I could take a messy, real search dataset and ship something a content editor would actually use: an ordered answer to "which page should I fix first?" I had no clear sense of whether machine learning could beat a simple rule here, or whether the signal was strong enough to justify the complexity. My Week-1 self assumed the hard part would be picking a model and tuning hyperparameters.

**What changed.** The hard part wasn't the model — it was the framing and the honesty. I spent the most time on the things that don't show up in a leaderboard: defining a proxy label that I was willing to call a proxy, banning 13 label-derived and identity columns from the feature list with an in-code assertion, choosing a client-grouped holdout over a random row split, and testing the hand rule first. That last one changed everything. On all 30,000 rows the generous hand rule looked strong; recomputed on six never-seen clients it collapsed to AUC 0.501 / P@50 0.42. The model (random forest, AUC 0.747, P@200 0.705) only looked good because I measured it against that same honest split. I learned that the split is the product — everything else is a detail.

I also learned to lead with the failures. The 0.447 false-alarm share, the tail error rate (37–43% deep in the queue), the single-seed holdout — writing those down before a reviewer does is what makes the rest credible. What I'd show a stranger is not the AUC; it's the limitation list.

**What I'd build next.** Given more time I'd (1) add a sealed holdout evaluated once and blind, with the framing script and metrics file committed so the number is checkable rather than taken on faith; (2) run a real refresh experiment so I could speak to treatment effect instead of just ranking; and (3) make the queue production-shaped — per-client windows, retraining triggers wired to observed drift, and a human checklist embedded in the tool, not just the paper.

**Three transferable things I learned.**
1. **Baseline first, always.** A model that doesn't beat a transparent rule on the same data and metric has earned nothing. I'll start every project with the rule.
2. **The split is the product.** How you hold out data matters more than which algorithm you pick; a flattering split hides real failure modes.
3. **Write the limitations section yourself.** Stating where the work breaks is not weakness — it's the thing that makes reviewers, editors, and employers trust the parts you don't qualify.

If I handed this to my Week-1 self, I'd say: the model works, but the real skill was knowing exactly where it doesn't — and saying so out loud.
