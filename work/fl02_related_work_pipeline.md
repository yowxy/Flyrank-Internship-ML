# FL-02 — Source-Grounded Study Notes Pipeline (from audit T09)

**Pipeline picked:** T09 "related-work literature skim for the capstone" (`delegate to AI with review`).
**Why this one:** it feeds the capstone paper directly, its failure mode (invented citations) is
famous and checkable, and the audit already names the human gate: *I verify every citation
exists before it enters the paper.*

## Step diagram (4 steps, defined handoffs)

```
[1. GATHER]  human pastes title -> AI returns candidate citation (venue/year/DOI) + abstract source
      | handoff: source URL, nothing else travels forward without one
[2. SYNTHESIZE]  per paper: 2-line contribution + 1-line capstone use, quoted ONLY from the abstract/source
      | handoff: note card with source attached
[3. DRAFT]  3-sentence related-work blurb per paper + one combined paragraph
      | handoff: draft with [CITATION NEEDED: venue/DOI] flags intact
[4. REVIEW — human gate, never skipped]  citation-existence check + abstract-level limits check
      | output: committed note or REJECTED card with reason
```

**Tools (all free):** Claude Project `Related-Work Notes` (spec below) for steps 1–3;
NotebookLM (or the search snippets) as the grounding store for step 1; the human for step 4.
No custom GPT (needs a paid plan — noted and rejected).

## Project spec (paste-ready custom instructions)

> You are my related-work note-taker for a capstone on ranking web pages for content
> refresh. Rules: (1) never state a venue, year, DOI, or finding without quoting the
> source it came from; (2) every note ends with SOURCE: <url> plus one line starting
> LIMIT: saying what you did NOT read (abstract only vs full text); (3) flag anything
> you are unsure exists with [UNVERIFIED] — never smooth over it; (4) short sentences,
> no flattery. My track: 30k-row search data, decline label, hand-rule baseline P@50 0.24,
> random-forest model, client-holdout splits, leakage quarantine on trend columns.

## Per-step prompts (used verbatim)

- **S1 gather:** `Candidate citation for "<title>": venue, year, DOI, and the authoritative abstract URL. If you cannot find all four, return [UNVERIFIED] and stop.`
- **S2 synthesize:** `From the abstract at <url> only: 2 lines on the contribution, 1 line on how it touches refresh-ranking (decline labels, position bias, leakage, ranking-vs-classification, or drift). Quote the abstract for each claim. End with SOURCE: and LIMIT:.`
- **S3 draft:** `Turn the 5 note cards into five 3-sentence related-work blurbs plus one combined paragraph for a capstone. Keep every [UNVERIFIED] flag. No new claims.`
- **S4 review (human checklist):** venue+DOI confirmed on publisher page? / every finding traceable to the quoted abstract? / LIMIT lines present? / anything the draft needs that only a full read can give?

## Five real runs (executed 2026-10-11, inputs real, outputs below)

**Run 1 — position bias (touches: CTR-vs-position signal).**
Joachims, Swaminathan & Schnabel (2017), *Unbiased Learning-to-Rank with Biased Feedback*,
WSDM, DOI 10.1145/3018661.3018699. SOURCE: ACM proceedings page + author PDF (Cornell).
Contribution: click data as relevance labels is "severely biased" because presentation order
drives clicks; counterfactual IPS-weighted ERM + Propensity SVM-Rank learn unbiased rankers
from biased clicks. Capstone use: our CTR features inherit presentation bias — CTR measures
rank as much as snippet quality. LIMIT: abstract + proceedings page; robustness numbers need the PDF.
GATE: PASS (venue/DOI on ACM page).

**Run 2 — leakage (touches: leak quarantine).**
Kaufman, Rosset & Perlich (2011), *Leakage in Data Mining*, KDD pp. 556–563 (journal version
Kaufman et al., TKDD 6(4), 2012, DOI 10.1145/2382577.2382579). SOURCE: ACM pages for both versions.
Contribution: leakage = "information about the target that should not be legitimately available
to mine from"; avoided by data management plus **learn-predict separation**, detected by
withheld-window tests. Capstone use: names our contract discipline (trend columns quarantined,
outcome windows excluded). LIMIT: abstract-level; causal-graph view needs full text.
GATE: PASS with correction — my input said "KDD 2012"; the gate corrected it to KDD'11/TKDD'12.
The gate is load-bearing; this run is the proof.

**Run 3 — drift (touches: decline as drift).**
Gama et al. (2014), *A Survey on Concept Drift Adaptation*, ACM CSUR 46(4), DOI 10.1145/2523813.
SOURCE: ACM page + author PDF (ResearchGate upload by Bifet). Contribution: integrated view of
drift handling — explicit change detection (which also reports process dynamics) vs blind adaptation;
evaluation methodology for adaptive algorithms. Capstone use: page decline framed as drift;
their detector framing justifies monitoring refresh-queue precision over time, not once.
LIMIT: abstract-level; detector taxonomy (DDM/EDDM/ADWIN specifics) needs full text. GATE: PASS.

**Run 4 — ranking > classification (touches: queue framing).**
Burges (2010), *From RankNet to LambdaRank to LambdaMART*, MSR-TR-2010-82. SOURCE: Microsoft
Research publication page + report PDF. Contribution: self-contained derivation — RankNet
(pairwise logistic) → LambdaRank (gradients scaled by IR-metric deltas) → LambdaMART (boosted
trees on lambdas); ensemble won Yahoo! LTR Challenge Track 1. Capstone use: justifies training
a classifier but shipping its probability as a *ranking* score, evaluated by precision@K.
LIMIT: abstract-page level; gradient derivations need the PDF. GATE: PASS.

**Run 5 — forest baseline (touches: model choice).**
Liaw & Wiener (2002), *Classification and Regression by randomForest*, R News 2(3), 18–22.
SOURCE: CRAN citation page + R Journal PDF. Contribution: reference implementation of Breiman's
forests (R port of Breiman–Cutler Fortran); documents proximity/variable-importance measures.
Capstone use: method citation for our random-forest baseline and its feature-importance readout.
LIMIT: citation-page level; importance-measure details need the PDF. GATE: PASS.

**Combined draft paragraph (S3 output, flags intact):** Refresh prioritisation sits at the
crossroads of four literatures. Decline is drift: pages decay as demand and rankings shift,
the setting Gama et al. (2014) systematise, including detector-based monitoring we adopt for
queue precision over time. The queue itself is a ranking problem, not a classification one —
Burges (2010) shows why listwise/pairwise objectives beat pointwise ones, which is why our
classifier's probability ships as a rank score judged by precision@K. Our CTR features inherit
presentation bias (Joachims et al., 2017): clicks measure rank as much as snippet quality, so
CTR is tier-adjusted, never raw. And the whole pipeline is built under a leakage discipline
(Kaufman et al., 2011/2012): learn-predict separation, trend columns quarantined, outcome
windows excluded. Our forest baseline follows Liaw & Wiener (2002). [No UNVERIFIED flags;
all five citations publisher-confirmed.]

## Time accounting (honest, setup included)

- Setup (one-time): Project spec + this doc ≈ 45 min.
- Pipeline, 5 papers: gather ≈ 10 min operator time (searches return in seconds; reading
  excerpts and picking authoritative sources is the cost) + synthesize/draft ≈ 15 min → **≈25 min total**.
- Manual baseline (experienced estimate, labelled as such): careful read + verify + note ≈
  45–60 min/paper → ≈ 4–5 h for five. **Saved this batch: ≈ 4 h net of setup; every later
  batch saves ≈ 4 h against zero setup.**

## Failure points + required human review (named)

1. **Invented citations** — the classic. Caught live in Run 2 (my own "KDD 2012" wrong).
   Human must confirm venue+DOI on a publisher page; nothing enters the paper without it.
2. **Abstract-level overreach** — every run carries a LIMIT line; method claims (ULTR robustness
   numbers, ADWIN details, lambda derivations) REQUIRE the PDF before drafting. The pipeline
   produces blurbs, not evidence.
3. **Secondary-source drift** — search excerpts (ResearchGate, scholar mirrors) are pointers,
   never citations; the gate accepts ACM/DOI/publisher pages only.
4. **Scope creep into full reads** — if the draft needs a number only the PDF has, the run
   goes back to manual by design; the pipeline flags this instead of inventing it.
5. **Manual-time estimate** — unmeasured; if challenged, time one manual paper and replace the estimate.
