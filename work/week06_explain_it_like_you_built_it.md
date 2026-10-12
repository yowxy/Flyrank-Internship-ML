# Explain it like you built it — Week 6

**The piece I picked:** why my Week-4 baseline rule fell apart on new clients
(from `work/notebooks/w05_model.ipynb`, Section 3).

## Why my baseline fell apart on new clients — and what that taught me

In Week 4 I built a hand-written rule for flagging pages to refresh: stale 90+
days, 500+ impressions, CTR under 0.5% while ranking on page 1–2. On the full
dataset it looked great — 9 out of the top 50 flagged pages were real declines.
I believed it.

In Week 5 I re-tested that exact rule on 6 clients it had never seen, and it
collapsed: only about 4 in 10 of its top picks were real declines, barely
better than guessing (AUC 0.501 — literally random). What I learned is that my
rule had memorised the *average* client. Its cutoffs — 0.5 CTR, 500
impressions — were tuned on rows it was then measured on, and different clients
decline at totally different rates (one at 22%, another at 62%), so fixed lines
that fit one client misfire on the next.

My Random Forest beat it on those same unseen clients (AUC 0.747, P@200 0.705
vs a 0.391 base rate) because it never trusted one frozen number — it combined
60 signals with learned weights, so when one signal shifts on a new client, the
others compensate. The lesson I keep: a model isn't good because its score is
high, it's good because its score survives meeting strangers.

*Numbers measured in `w05_model.ipynb` (seed 42, client-holdout split);
receipts in `work/outputs/w05_model_receipts.json`.*
