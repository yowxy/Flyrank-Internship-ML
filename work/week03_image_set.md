# Week 3 — Image Set (curated, not generated-at)

Rule followed throughout: work is shown with real captures from executed code; decoration
must never be louder than a number. Charts rendered in kit colors (`#0E7C6B` / `#9AA3A0`
on `#FAFAF7`, system sans); builder script ran once from `outputs/model_results.json`
and `outputs/refresh_queue_sample.csv`, then deleted — rerun the pipeline, rerun the
numbers, never hand-edit a figure.

## Needs → image (mapped to `week03_content_map.md`)

| Page / section | Need | Image | Real / AI | Status |
|---|---|---|---|---|
| Home — proof teaser | strongest number at a glance | `assets/model_vs_baseline.png` (RF 0.747/0.68 vs baseline 0.627/0.24, base-rate line) | real capture of executed results | KEEPER |
| Work — Case 2 | the failed rule vs the model | same chart (reused, not duplicated) | real | KEEPER |
| Work — Case 1 | the product itself: a ranked queue | `assets/queue_top10.png` (top 10 of 30,000, IDs dropped) | real | KEEPER |
| Work — Cases 1–3 | feature story (what the model leans on) | `outputs/charts/top_feature_importance.svg` (pipeline output, referenced as-is) | real | KEEPER (by reference) |
| Section dividers | quiet connective tissue, if a page feels empty | `assets/divider_queue_motif.svg` (flat bars, same motif as favicon) | generated, kit-faithful | KEEPER (single accent) |
| About — the person | a face | real photo | real | PENDING — mine to supply; a plain headshot or nothing, never a generated portrait |
| Hero | nothing — whitespace does the job | — | — | deliberately empty (see rejection) |

## Where I chose real over AI (each call noted)

- **Queue table over any "dashboard" mockup.** A generated dashboard would be fiction; the table shows actual ranks, scores, and actions with denominators a reviewer can check against the repo.
- **Pipeline SVG over a restyled redraw.** I kept `top_feature_importance.svg` byte-identical — restyling a result figure risks misrepresenting it; evidence stays in the pipeline's own hand.
- **IDs dropped from the queue capture.** `content_id`/`client_id` are pseudonyms: they prove nothing on a portfolio and add noise. Rank, score, action, volume, trend is the whole story.
- **Photo: real or absent.** Nothing generated ever stands in for me, same as for my results.

## Rejection note (the graded part)

**Rejected: `assets/rejected/trial_hero_glass.png`** — a glossy teal-gradient hero with glass orbs
and the strip "AI PORTFOLIO • MACHINE LEARNING • DATA". Three concrete reasons, all checked
against the kit before killing it: (1) it violates the portfolio rule — it would be the
brightest, most memorable thing on the page, and visitors came to see the queue, not a
wallpaper; (2) it carries zero information — no number, no proof, and it could headline any
of ten thousand portfolios, which is the opposite of my checkable claim; (3) its buzzword
strip is exactly the generic-AI register my voice card bans ("Results-driven ML enthusiast…").
Kept on file under `rejected/` as the receipt. Replacement cost: nothing — a clean title
over whitespace, with the real chart below it.
