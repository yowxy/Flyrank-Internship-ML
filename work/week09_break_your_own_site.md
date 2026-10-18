# Week 9 — Break Your Own Site (hardening record)

**Scope.** The FlyRank track portfolio: `work/portfolio/index.html` (single file, 19.5 KB)
+ `favicon.svg` + `og-card.png` (new). Method: (1) extracted the page's `<script>`
and drove the demo submit handler under Node v22 with a DOM stub — 10 hostile cases
(`/tmp/opencode/break_js_harness.mjs`); (2) static audit — meta/SEO, TODO markers,
id/anchor integrity, HTML well-formedness, link liveness via curl
(`/tmp/opencode/static_audit.py`). Two audit-script bugs found and corrected by hand:
`og:type` "HAVE" was a truthy-tuple artifact (page truly had zero OG tags before the
fix), and the `lang` "missing" was a split-on-first-`>` artifact (`<html lang="en">`
is line 2 — present).

**What could NOT be tested here (no live URL for this portfolio yet, no device lab):**
real-phone render, real Safari/Firefox/Chrome matrix, Lighthouse/PageSpeed score,
Google indexing ("search your own name"), and rendered share-card preview. Each is a
named launch-checklist item below, not a silent gap. (`portoku-self.vercel.app` on the
GitHub profile is a separate personal portfolio — out of scope; this record covers the
FlyRank track site only.)

## Where it broke — triage

| ID | Finding | Verdict |
|---|---|---|
| F1 | `1e309` input overflows to `Infinity`, passed validation (`isNaN(Infinity)` is false), rendered a result | **FIXED** — added `!isFinite(n)`; harness T7 now rejects with message |
| F2 | Zero social-share tags: no `og:*`, no `twitter:card`, no `canonical` | **FIXED** — full OG + Twitter block + canonical + generated `og-card.png` (1200×630, 45 KB). Absolute URLs use `YOUR-DOMAIN` placeholder → deploy-time swap (checklist item 1) |
| F3 | No `:focus-visible` style — keyboard users get thin/inconsistent focus | **FIXED** — 3px accent outline rule added |
| F4 | No `<noscript>` — with JS off the demo button silently does nothing | **FIXED** — notice added pointing at the numbered cases above |
| F5 | Case 3 copy stale: "leakage-demo not yet executed" — but `w06_validation_audit.ipynb` ran it (Oct 15) | **FIXED** — rewritten with measured numbers: leaky LogReg AUC 0.999 vs honest 0.697, top honest shuffle-delta 0.029 (`days_with_impressions`), seed 42, held-out clients |
| F6 | `<title>` and hero said "Your Name"; LinkedIn links pointed at linkedin.com homepage | **FIXED** — name "Iklil" + `linkedin.com/in/iklilnajmi` from the public GitHub profile. Email + booking URL still TODO (unknown to me) |
| F7 | No canonical URL | **FIXED** — added with `YOUR-DOMAIN` placeholder (same deploy swap) |
| L1 | No live URL → PageSpeed, search indexing, card render all unverified | Known limitation → checklist items 1–3 |
| L2 | JS disabled → demo inert by design (no backend); noscript note softens it | Known limitation (architecture, not a bug) |
| L3 | `details/summary` + SVG favicon need a modern browser (IE/ancient dead) | Known limitation, acceptable |
| L4 | Email/booking CTAs are `mailto:` placeholders until owner adds address + Cal link | Known limitation → checklist item 4 |
| L5 | No analytics snippet (needs account + domain at deploy) | Known limitation → checklist item 2 |
| L6 | Fonts need Google CDN; offline falls back to system-ui stack (graceful by design) | Known limitation, resilient default |
| L7 | Notes/Capstone sections are scaffolding until filled | Known limitation → Week 10 content |
| L8 | No real-device/browser matrix run here | Known limitation → checklist item 3 |
| L9 | `og-card.png` is generated placeholder art, not identity-kit design | Known limitation — replaceable without code changes |

**Deliberately rejected (considered, not done):** `robots` meta + sitemap (single page, default indexable — nothing to direct); JSON-LD (no rich-result payoff for a one-pager, keeps the no-bloat promise); render-blocking-font `media=print` hack (one font, `display=swap` + preconnect + fallback stack already; complexity not earned).

## Evidence the fix-nows are fixed

- Harness after fix: **15/15 PASS**, including T7 rejecting `Infinity`, T1–T4 blocking empty/garbage/negative/whitespace, T8 double-submit byte-identical (`len 469 vs 469`), T9 injection payload never reflected (outputs use only static strings + `Number()`).
- `grep -c 'property="og:' index.html` → 7; `twitter:card` + `canonical` present; structure audit: no tag mismatches, no duplicate ids, `#work` resolves, 9 labels for 9 inputs, `role="alert"` on error.
- Links curled: repo URL 200 (×4 occurrences), fonts CSS 200. LinkedIn profile URL returns 999 to bots (bot-block, expected) — handle taken from the owner's own public GitHub profile; owner confirms at launch.
- Byte budget (speed proxy, no live URL to run Lighthouse against): HTML 19.5 KB + favicon ~0.4 KB + og-card 45 KB (only fetched by scrapers, never by visitors) + 1 font CSS + 2 woff2. Zero JS libraries, script at end of body. Estimated first paint: 4 requests. Full PageSpeed run is checklist item 3.

## Structured peer hardening review

Reviewer role: structured peer (assistant), against the Week 9 pass/revise bar.

- *Genuinely tried to break it?* Yes — 10-case hostile harness incl. empty/garbage/Infinity/double-submit/XSS, plus link-liveness and audit-script self-correction. Real edge cases, all recorded.
- *Findability/speed?* Title now carries the owner's name; description + OG/Twitter + canonical + 1200×630 card added. Live-URL-dependent proofs (search, PageSpeed, card render) are checklist items, not claims.
- *Triage honest?* 7 fixed with evidence above; 9 limitations named with owners. Nothing hidden.
- **Must-fixes (all addressed):** F1 validation hole, F2 share preview, F5 stale "pending" claim (a launched page understating its own evidence is a trust bug). No open must-fixes from this review.
- **Review verdict: PASS with launch checklist below** — the page is launch-ready pending owner deploy steps that require their accounts.

## Launch checklist (owner, in order)

1. Deploy per `work/portfolio/README.md` (push `index.html` + `favicon.svg` + `og-card.png`), point domain, confirm HTTPS. Then replace all four `YOUR-DOMAIN` placeholders with the real address.
2. Add privacy-friendly analytics (Cloudflare Web Analytics recommended — free, no banner) and screenshot it for the portal.
3. On the live address: phone check, View-Source title check, PageSpeed run, Google "Iklil FlyRank" search, share-link card preview (iMessage/X/LinkedIn), favicon visible.
4. Replace `you@example.com` (5×) with real address; replace booking mailto with Cal/Calendly link; confirm LinkedIn handle.
5. Install FlyRank graduate badge in footer (slot exists) linking to verification page.
6. Keep-building: how-to + named next piece + reminder live in `work/NEXT_CASE.md` (next case = refresh experiment; reminder = `work/next_case_reminder.ics` + screenshot). AI workspace (`ai_workspace_spec.md`) and Claude Project (`fl01_workflow_audit/claude_project_spec.md`) preserved.

## Self-check

- [x] Break-tests run, all 15 pass, evidence above (not happy-path only)
- [x] SEO/meta added; speed budget measured; live-only checks named, not faked
- [x] Fix-nows fixed in `work/portfolio/`; limitations named with owners
- [x] Hardening review recorded with verdict; no open must-fixes
- [x] No private data, tokens, or client names touched; public-profile data only (name, handle)
