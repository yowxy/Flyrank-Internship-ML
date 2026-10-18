# Next case study — how to add one (and the first one I'm adding)

## Where it goes

The portfolio lives at `work/portfolio/index.html`, in the **Work** section (`<section id="work">`). Each case is a `.case` block (problem / what I did / what came of it / where it breaks) with a "See the notebook" CTA linking to the repo. The next case is added as a new `.case` block right after the capstone case, before the "Hiring for this?" line.

## Steps to add a case (reuse the Week 2 three-beat shape)

1. **Problem.** Name the decision, who acts on it, and why data/ML helps — one paragraph, plain language, no buzzwords. (Same shape as `work/week02_framed_cases.md` Case 1–3.)
2. **What you did and decided.** Method, the metric fixed *before* training, the split, the leakage quarantine — and the decision you'd defend in an interview.
3. **What came of it.** The number (with denominator), where it breaks, and what you'd do differently next time. No claim without a committed receipt/notebook output.
4. **Add the artifact.** Execute the notebook top to bottom, commit the receipt under `work/outputs/` and any figure under `work/figures/`.
5. **Add to the site.** Paste a new `.case` block into `work/portfolio/index.html` (copy the capstone case block, swap the three beats + notebook link).
6. **Commit + push.** `git add work/portfolio/index.html work/notebooks/*.ipynb work/outputs/*.json work/figures/*.svg && git commit && git push`. The site redeploys on push (Pages).

Checklist (tick each):
- [ ] Notebook runs top to bottom, no errors
- [ ] Receipt committed in `work/outputs/*.json`
- [ ] `.case` block added to `work/portfolio/index.html`
- [ ] Commit pushed to main; Pages rebuild confirmed

## The next piece of work (named, specific)

**Refresh experiment — does refreshing a flagged page actually recover traffic?**

This directly answers the #1 limitation I already wrote down: *"No causal evidence — no refresh experiment was run. Pages that get refreshed are selected, often because they looked weak, so the data cannot say that refreshing a flagged page causes recovery."* The current capstone can only claim ranking value for ordering review; this next case tests whether the intervention works.

Concrete shape:
- Problem: editors spend sprint hours refreshing pages the queue flags; we don't know if that spend buys traffic recovery.
- What I'd do: a held-out sample of flagged pages split into "refresh now" vs "wait" (or use the existing holdout as the control pool), measure impressions delta 30 days post-refresh vs baseline, report the effect with confidence intervals and the selection-bias caveat.
- What came of it: a measured number (recovery lift, or no detectable lift) — honest either way — plus where it breaks (sample size, seasonality, can't randomize live editorial decisions).

## Reminder set

**When:** Sunday 2026-11-01, 09:00 (two weeks from 2026-10-18), repeating weekly for 12 weeks — cancel any remaining occurrences the day the case is pushed.

**The reminder itself:** `work/next_case_reminder.ics` — a real, importable calendar event titled "FlyRank: add refresh-experiment case", with this repo and this file in the description/location. It is committed, so it is reproducible evidence, not an intention.

**Set it (one click, then capture the evidence):**

1. Import `work/next_case_reminder.ics`: macOS Calendar → File → Import; Google Calendar → Settings → Import & Export; Outlook → File → Open & Export → Import an iCalendar. It lands on 2026-11-01 09:00 local and repeats weekly.
2. Open the imported event, confirm the title and date.
3. Screenshot the event (month view or the event detail showing the repeat rule) and save it as `work/fl01_workflow_audit/evidence/next_case_reminder.png`.
4. Paste that screenshot into the Week 9 portal card under **Files** next to `work/NEXT_CASE.md`.

Verify the file is valid before importing: `python -c "import pathlib,re; t=pathlib.Path('work/next_case_reminder.ics').read_text(); assert t.startswith('BEGIN:VCALENDAR') and t.rstrip().endswith('END:VCALENDAR') and 'RRULE:FREQ=WEEKLY' in t; print('ics ok')"`.

If you don't use a calendar, the fallback is the recurring note: `work/NEXT_CASE.md` is the single source of truth — open it on the first Monday of each month until the case ships.

## Build context preserved (so the next case is a short conversation)

- **Repo:** `github.com/yowxy/Flyrank-Internship-ML` (branch `main`), cloned locally.
- **Voice kit:** `work/week02_framed_cases.md` — direct, warm, plain, specific; short sentences; numbers with denominators; no generic AI bios.
- **Identity kit / CSS:** `work/portfolio/index.html` `:root` block — brand colors, Inter font, the "honest prototypes, limits written down" tone.
- **Stack:** Python 3.12, pandas, scikit-learn 1.9.x, matplotlib; `scripts/run_all.py` runs the full pipeline offline from `data/raw/content_refresh_anonymized.csv`.
- **Notebook pattern:** `work/notebooks/capstone.ipynb` — markdown thinking cell + code cell that reads committed receipts and asserts artifacts; that's the template to copy for the next notebook (`work/notebooks/w08_refresh_experiment.ipynb`).
- **Receipts pattern:** `work/outputs/w05_model_receipts.json`, `w06_validation_receipts.json`, `w07_playbook_receipts.json` — every public number traces to one committed JSON.
- **Claude Project context:** this repo, this voice, this stack, the capstone paper (`docs/index.html`), and the three-beat case shape are already in the project. Paste this file + the repo link at the start of the next session and the next case is a short conversation, not a rebuild.
