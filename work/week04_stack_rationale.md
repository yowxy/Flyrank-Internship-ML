# Week 4 — Stack Rationale (three roads, one picked)

## My four constraints (given to AI verbatim)

1. **Free only.** Student budget: hosting and tools must cost nothing, forever — not "free trial".
2. **Honest skill level.** I write Python and notebooks daily; HTML/CSS at edit-level (I can read and tweak it, not design from scratch); no React, no backend experience. Anything I ship, I must be able to fix alone at midnight.
3. **What it must do** (from `week03_content_map.md`): 3 pages — Home (claim hero + email CTA + proof teaser), Work (3 cases, each: problem / did / number / breaks + chart/table), About (4 lines + photo). Every CTA ladders to one action: an email.
4. **How work must display.** Static proof: PNG/SVG charts, ranked tables, and links OUT to the GitHub repo and executed Colab notebooks — that is where a hiring manager checks my work. Nothing has to be dynamic yet: no live demo, no comments, no CMS, no contact form (mailto does the job).

## Three options, simplest first

| | A. Static HTML + GitHub Pages | B. Static generator (Jekyll/Hugo) + Pages | C. Next.js/Vercel (or Framer/Webflow) |
|---|---|---|---|
| Build | one `index.html`, kit CSS inline | templates + markdown, build step | components / visual builder |
| Host (free) | Pages, free forever | Pages, free forever | Vercel free tier / builder free tier with limits |
| Backend? | none | none | available — and unused |
| Trade-off | hand-edit every page; fine at 3 pages, annoying past ~10 or with a blog | blog-ready, DRY templates — but a new toolchain (Ruby/Go, themes, plugins) to learn and debug | dynamic power I have no use for yet; React cliff or platform lock-in + paywalls later |

## Pressure test (front-runner A)

- **What breaks if I pick the simplest?** Past ~10 pages or a real blog, hand-editing rots. I have 3 pages and cut the blog in Week 1 — nothing breaks within this portfolio's scope, and the content (plain HTML) migrates to B later in an afternoon.
- **What would I maintain under C?** A framework or a subscription: dependency updates, build errors, or a monthly fee the moment I need a custom domain properly or exceed free limits. Maintenance I can't do alone fails my constraint #2.
- **Can I finish in two weeks?** A is already live as a skeleton; filling 3 pages from the map is days, not weeks. B costs a week of toolchain first; C costs longer.
- **Does it show my work the way it must be shown?** Best of the three: my proof is *elsewhere* (repo, notebooks) by design — reviewers click through to check numbers. An embedded widget would be a toy; links to executed notebooks are the exhibit. A needs no apology here.

## Decision (my words)

I picked **A: static HTML on GitHub Pages, separate `portfolio` repo**. The two I didn't: B, because I have no blog and refuse to pay a week of toolchain learning for templating three pages; C, because its power answers needs I explicitly don't have yet, at the price of maintenance I can't do and lock-in I don't want. Can I maintain this? Yes — I can read every line of it, fix it without docs, and host it free forever. Does it show my work well? Yes — the site frames, the repo proves, and nothing on the page is louder than the numbers. Backend: **not yet** — mailto plus GitHub links cover every action; revisited only if a live demo or form ever earns its keep.
