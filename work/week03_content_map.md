# Week 3 — Content Map & Claim (Map It & Give It a Face)

**One person, one action:** hiring manager, small tech team → email me to set up a chat.
**Site:** 3 pages (Home with contact block → Work → About). Contact folded into Home + footer per the Week-1 pressure test.

## One-line claim — 10 AI options, my pick below

1. Small models on real search data, with the failures written down.
2. I rank 30,000 decaying pages so editors fix the right one first.
3. Working ML prototypes, not polished demos — limits included.
4. I ship honest ML prototypes on messy data — limits included.
5. Machine learning with the error bars left in.
6. I beat the hand rule, then wrote down where my model breaks.
7. Honest models for messy data: measured, ranked, limits stated.
8. A junior who delivers a working prototype instead of a polished demo.
9. My refresh queue beats a rule baseline and says where it fails.
10. You need proof, not promises: every number here has a denominator.

**My pick: #1 — "Small models on real search data, with the failures written down."** (Backup: #2, the concrete proof-first option.)

## Content map

### HOME — job: pass the 30-second test (claim, one proof teaser, email CTA)

1. Hero: one-line claim + sub-line (ML intern & student, FlyRank) + **CTA: "Email me to set up a chat"** (mailto button).
2. Proof teaser: the single strongest number — random forest 0.747 AUC / 0.68 P@50 vs hand-rule baseline 0.627 / 0.24, client-holdout, base rate 0.542 (pipeline `model_report.md`, asserted in code). Visual: `assets/model_vs_baseline.png` → link to Work.
3. Three case summaries (2 lines each) → link to Work.
4. Contact block: email button + CV download + GitHub link. Same block repeated in footer on every page.

### WORK — job: the proof (lead with the strongest case)

1. **Case 2 — The hand rule that failed** (strongest: only case with measured numbers today). Sections: problem / what I did / number / where it breaks. Visual: `assets/model_vs_baseline.png`. CTA: "See the notebook" (repo link).
2. **Case 1 — Which page should an editor fix first?** (the frame: decision, target, bar). Visual: `assets/queue_top10.png` (the ranked product itself). CTA: "See the notebook".
3. **Case 3 — The label trap** (flagged IN PROGRESS until `w03_feature_leakage_check.ipynb` is executed — no claim without outputs). CTA: "See the contract".
4. Page CTA: "Hiring for this? Email me." (ladders to the one action.)

### ABOUT — job: give the claim a face, in 4 lines

Photo (optional) → 4-line bio (from Week 2) → how I work (frame → baseline → leak-check → limits) → CTA: email.

## Still need to gather (honest list — nothing here blocks the build week except stars)

- [ ] ★ Executed `w03_feature_leakage_check.ipynb` outputs (Case 3 unblocks only with these).
- [x] Model-vs-baseline numbers (RF 0.747/0.68 vs baseline 0.627/0.24 — pipeline `model_report.md`, wired into the proof teaser).
- [x] Keeper captures rendered: `assets/model_vs_baseline.png`, `assets/queue_top10.png` (IDs dropped, no private data — verified).
- [ ] Depth-2 tree printout screenshot (notebook 02) — last proof capture missing.
- [ ] CV file (PDF) for the contact block.
- [ ] Real photo (optional; a plain headshot beats any generated avatar — never generate "me").

## Images: what the portfolio needs (real vs generated)

- **Work proof = real captures only.** Charts and tables from my own executed notebooks. A generated chart would be fiction and would kill the "honest" claim on contact.
- **Connective tissue = whitespace, not images.** No hero image (Iris precedent: a clean title over whitespace beats AI-slop glass). My screenshots are the color on the page.
- **Generated (one accent, decided):** single flat divider `assets/divider_queue_motif.svg` (same bars as the favicon) — only if a page feels empty; default is whitespace. The glossy-hero trial was generated and killed (see `week03_image_set.md`).
- **Me = real photo or nothing.** No generated portrait, ever.
