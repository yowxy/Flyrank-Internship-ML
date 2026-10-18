# Build-in-public: the content-refresh queue that beat a hand rule — and where it breaks

**The decision.** I tested the hand-rule baseline before any model — and it failed on the data that mattered. On all 30,000 pages the rule looked strong, but recomputed on six never-seen clients it collapsed to AUC 0.501 / P@50 0.42. That gap between "looks great in-sample" and "holds out on unseen clients" is why I split by client, not by row, and why the random forest result (AUC 0.747 / P@200 0.705) only means anything relative to that same honest split. The split is the product; the model is a detail.

**The limitation.** Forty-four point seven percent of pages the model flags are not actually declining, and errors concentrate in the tail of the queue. The label is a same-window proxy (−19% vs −21% get different labels), there's no causal evidence that refreshing recovers traffic, and this is a single holdout at one seed — directional, not a benchmark. The queue is safe to use as a review order and unsafe to use as an automatic decision.

**The ship.** A ranked, reason-coded content-refresh queue on 30,000 anonymized FlyRank search pages, evaluated on held-out clients, with the receipts committed. Deployed paper and code: github.com/yowxy/Flyrank-Internship-ML.
