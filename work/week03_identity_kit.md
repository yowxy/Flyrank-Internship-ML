# Week 3 — Identity Kit (one page)

## Type

**Inter only** — 400 for body, 600 for headings. (One family, two weights: nothing on the page competes with the results. Runners-up I rejected: Source Serif 4 + Inter felt editorial, wrong for a lab notebook; Space Grotesk + Inter felt startup-loud, and loud is the designer's job, not mine.)

## Palette

| Role | Hex | Contrast on bg | Verdict |
|---|---|---|---|
| Background (warm white) | `#FAFAF7` | — | calm, prints clean |
| Text (near-black) | `#1B1F1D` | 15.9 (need ≥ 4.5) | PASS, measured in Python (`wcag` luminance math) |
| Links / accent (muted teal) | `#0E7C6B` | 4.9 (need ≥ 4.5) | PASS as text — safe for links and small labels, and for low vision / sunlight |
| The rule | | | work stays the loudest thing: screenshots and numbers carry the color, never the chrome |

Rejected: an ink-green (`#1B7A3D`) and a slate-blue (`#2F5DA3`) — both passed contrast too, but teal reads "measured instrument" while green reads "after-figure" (Dorian's lane, not mine) and blue reads default-corporate.

## Logo / favicon

`work/assets/favicon.svg` — a muted-teal rounded square holding three ascending white bars: a ranked queue, i.e. the portfolio's proof in 16 pixels. No wordmark; the claim is the wordmark.

## Style note (also pasted into the AI workspace spec)

Inter 400/600 only; `#1B1F1D` on `#FAFAF7`, links `#0E7C6B`. Mood: quiet lab notebook — generous whitespace frames each result, and no section may be louder than its numbers. Real screenshots only; nothing generated ever stands in for measured work.

## Reusable build snippet (paste atop every build chat)

> Style: Inter 400 body / 600 headings (H1 32px, H2 24px, body 17px/1.6, small labels 13px uppercase). Colors: text #1B1F1D, bg #FAFAF7, links + accent #0E7C6B only. Spacing: 64px between sections, 24px after headings. No new fonts, no new colors, no hero images — screenshots are the color.
