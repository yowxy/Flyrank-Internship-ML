# Week 9 — Plant Your Flag (launch runbook)

**Status split, stated plainly.** Everything preparable in this repo is done (below).
Three pass criteria need the owner's accounts and cannot be completed from here:
buying/pointing the domain, creating the analytics property, and minting the
personalized badge (needs your credential ID from the internship portal). This file
makes each a 10-minute task with verification commands. Nothing here is faked.

## Prepared in this repo (done, verified)

- [x] Footer badge block installed: interim mark linking to
      `https://internship.flyrank.ai/verify`, styled pill, with a `TODO(credential)`
      comment holding the exact generation steps. Swap = paste official snippet.
- [x] Analytics insertion point ready: `TODO(deploy)` comment before `</body>` with the
      exact Cloudflare beacon template; footer "No tracker" line carries a
      `NOTE(deploy)` so it gets rewritten the moment the beacon lands (footer never lies).
- [x] Share-preview tags present: `og:type/url/title/description/image` (1200×630),
      `twitter:card` (summary_large_image) + title/description/image, `canonical`.
      All four absolute URLs use the `YOUR-DOMAIN` placeholder → swapped at deploy.
- [x] `og-card.png` generated (1200×630, 45 KB, brand colors + measured claim).
      Scrapers only — visitors never download it.
- [x] Titles: `<title>Iklil — Honest ML Prototypes</title>` + matching `og:title` /
      `twitter:title`. Favicon: relative `favicon.svg`, valid, in repo root of the
      deploy folder. Deploy push line in `work/portfolio/README.md` includes `og-card.png`.

## Owner deploy steps (in order, ~30 min + DNS waiting)

**1. Domain + HTTPS (recommended path: GitHub Pages, matches `work/portfolio/README.md`).**
Push the folder to the standalone public repo, Pages on (branch `main`, root), then
Settings → Pages → Custom domain → enter your domain → Save. At your registrar:
apex → A `185.199.108.153`, `.109`, `.110`, `.111`; `www` → CNAME
`YOUR-USER.github.io`. Then tick **Enforce HTTPS** once the certificate issues
(minutes to hours — DNS is slow, not broken). Alternative: Vercel (your other site
lives there) — project Settings → Domains, A `76.76.21.21` or CNAME
`cname.vercel-dns.com`, HTTPS automatic. Either is a pass; don't run both.
Verify: `dig +short YOUR-DOMAIN` shows the records; `curl -sI https://YOUR-DOMAIN`
→ `200`; padlock in incognito + on your phone.

**2. Swap the four `YOUR-DOMAIN` placeholders** (`grep -n YOUR-DOMAIN index.html`:
canonical, `og:url`, `og:image`, `twitter:image`), push, wait 2 min.

**3. Analytics.** Cloudflare dashboard → Web Analytics → Add a site → copy token →
paste beacon at the `TODO(deploy)` slot, push. Load the live page twice, check the
dashboard shows visits, screenshot it for the portal card (Files section).

**4. Badge.** Open `https://internship-badge.netlify.app/`, enter credential ID +
first name `Iklil` + Machine Learning track + cohort, Copy, paste over the interim
mark in the footer, push. Click it on the live page: it must open YOUR verification
result — anything showing "No public credential found" means a wrong ID, fix it.

**5. Launch hygiene on the real address (phone in hand).**
Titles correct in tab + view-source; favicon in tab; share link into
LinkedIn Post Inspector + X card validator (renders card with `og-card.png`);
all nav/demo/repo links clicked; demo scored once with defaults; footer badge
visible and linking correctly; analytics dashboard showing your visits.

## Pass/revise mapping (honest)

| Criterion | State |
|---|---|
| Live on custom domain (or clean fallback) over HTTPS | Owner step 1 — repo ready |
| Analytics installed and working | Owner step 3 — slot + instructions ready |
| Share preview, favicon, titles correct on real address | Tags + assets ready; render check is owner step 5 |
| Badge in footer linking to verification page | Interim mark installed; official snippet is owner step 4 |

## Self-check

- [x] No fabricated URLs, tokens, or credential IDs anywhere in the repo
- [x] Every owner step has exact commands/pages, not "set it up somehow"
- [x] Footer makes no claim analytics doesn't already keep (`NOTE(deploy)` guard)
- [x] No private data, tokens, or client names in the deploy folder
