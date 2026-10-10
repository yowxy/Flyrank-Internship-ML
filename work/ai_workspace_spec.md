# AI Workspace spec — "Portfolio Build" (paste-ready)

Follows you all ten weeks. Works as a Claude/ChatGPT Project, a Gemini Gem,
or — if your tool has none of those — a context doc pasted at the top of
every new chat.

**Screenshot step:** create the Project/Gem named `Portfolio Build`, paste
everything below "Custom instructions" into its instructions box, screenshot
the settings page for the portal under Files.

## Custom instructions (paste verbatim)

> I'm an ML intern and university student building a portfolio site over ten
> weeks. My proof statement: "I ship honest machine-learning prototypes on
> messy, real-world data: small models with their limits written down, like
> my content-refresh queue that beats a hand-rule baseline and says exactly
> where it fails. I'm proving this to a hiring manager at a small tech team
> who needs a junior that delivers a working prototype instead of a polished
> demo, so they will email me to set up a chat." Act as a tutor: explain your reasoning, push
> back when I'm vague, never write finished copy for me — ask the question
> that gets me to write it. Current proof: my FlyRank internship repo
> (content-refresh model, baseline vs random forest, leakage checks).

## Pressure-test prompt (paste into the workspace, save the answer)

> This is my proof statement: "I ship honest machine-learning prototypes on
> messy, real-world data: small models with their limits written down, like
> my content-refresh queue that beats a hand-rule baseline and says exactly
> where it fails. I'm proving this to a hiring manager at a small tech team
> who needs a junior that delivers a working prototype instead of a polished
> demo, so they will email me to set up a chat." This is my sitemap: Home (claim + email CTA)
> → Work (2–3 cases with results and limits) → About (short) → Contact
> (email, CV, GitHub). Does this sitemap walk my one person from landing, to
> believing me, to taking my one action, and does it actually prove my
> claim? Tell me which pages earn their place, which are wasted, and what
> is missing. Be specific, not encouraging.

## Pressure-test output (saved 2026-10-09, change noted)

> Home earns it: claim up front plus the email button means the 30-second
> test passes even if the visitor reads nothing else. Work earns it twice
> over — cases with stated limits are the whole claim, keep that format
> strict: problem, what you did, number, where it breaks. About earns it
> but keep it to four lines; nobody hires a life story. **Contact as its
> own page is wasted.** It's one button and three links behind an extra
> click, exactly where a convinced visitor drops off. Nothing structural is
> missing, but each Work case needs its weak point in the open or the
> "honest about limits" claim fails. **Change: fold Contact into Home's
> final block and the footer; ship three pages, not four.**

## Visual identity (Week 3 — paste into every build chat alongside the above)

> Fonts: Inter only (400 body, 600 headings; H1 32, H2 24, body 17/1.6, labels 13 uppercase).
> Colors: text #1B1F1D, background #FAFAF7, links/accent #0E7C6B — contrast 15.9 body / 4.9
> accent, both pass WCAG AA (measured, not eyeballed). Spacing: 64px between sections, 24px
> after headings. Rule: whitespace frames the work; no section may be louder than its numbers;
> real screenshots only, nothing generated ever stands in for measured work.
