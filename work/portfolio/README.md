# Portfolio — "empty but live" (Week 4)

Source of truth for the portfolio site. Deploy = push this folder's contents to a
standalone public repo with Pages on (keeps the ML repo's CI and data concerns separate).

## Go live (5 minutes, one time)

1. Create a new **public** repo on GitHub (e.g. `portfolio`), empty (no README tick).
2. Push this folder as its root:
   ```bash
   cd work/portfolio
   git init -b main && git add index.html favicon.svg && git commit -m "feat: empty but live"
   git remote add origin git@github.com:YOUR-USER/portfolio.git && git push -u origin main
   ```
3. On github.com: repo **Settings → Pages → Deploy from branch → main → /(root) → Save**.
4. Wait ~1 minute, open `https://YOUR-USER.github.io/portfolio/` — **on your phone**, not just your laptop. Screenshot it for the portal card under Files.

## After it is live

- Replace the three `TODO(you)` placeholders (name, email ×2).
- Next week this blank fills with the content map (`../week03_content_map.md`); the kit
  (`../week03_identity_kit.md`) is already baked into the CSS :root block above.
