# Clear Cents — ADHD Budget Planner (Vercel site)

A static website: no framework, no database, no build step on Vercel. Customer data is stored in each buyer's own browser (localStorage), so there's nothing to host except these files.

## What's in this folder

| URL on your site | What it is | Who sees it |
|---|---|---|
| `/` | Product details page (features, screenshots, FAQ) | Public — link it from Etsy |
| `/demo/` | Free live demo with sample data + "Get the full planner" banner | Public — link it from Etsy |
| `/p/cc-iaesf2gpr8/` | **The real planner for buyers** (starts empty, setup checklist) | **Buyers only** — link is in the buyer PDF |
| `/p/cc-iaesf2gpr8/start/` | Buyer welcome guide: phone install, offline download, backups | Buyers only |
| `/p/cc-iaesf2gpr8/download/clear-cents-budget-planner.html` | Single-file offline planner | Buyers only |
| `vercel.json` | Clean URLs, old `/app/` `/start/` `/download/` redirect to home, no-index + no-referrer on `/p/` | — |
| `_source/` | Editable source + `build.py` (not deployed — see `.vercelignore`) | — |

### The hidden link
- The secret part (`cc-iaesf2gpr8`) is stored in `_source/config.json` and appears in **no public page, manifest, sitemap or robots file**. Search engines are told not to index it.
- **Keep your GitHub repo PRIVATE** if you deploy from GitHub — `_source/config.json` contains the secret.
- If the link ever leaks: change the `slug` in `_source/config.json` (any random text like `cc-x8k2m9q4ze`), run `python3 _source/build.py .`, redeploy, and update the buyer PDF. Existing buyers' data is per-device, but their saved link changes — message them the new one (Etsy lets you update the file for past buyers).
- Each buyer's data lives only in their own browser, so every customer automatically has a private planner.

## Deploy to Vercel (pick one)

**A. Drag and drop (easiest)**
1. Go to vercel.com → Add New → Project → or use https://vercel.com/new and choose "Deploy without Git" / drag this whole folder in.
2. Framework preset: **Other**. Build command: *leave empty*. Output directory: *leave empty* (root).
3. Deploy. Your site will be at `https://<project-name>.vercel.app`.

**B. GitHub (best for updates)**
1. Create a new GitHub repo and upload everything in this folder (keep the folder structure).
2. On Vercel: Add New → Project → Import the repo → Framework preset **Other** → Deploy.
3. Every time you push a change, Vercel redeploys automatically.

**C. Vercel CLI**
```
npm i -g vercel
cd clear-cents-vercel
vercel --prod
```

Tip: name the project something like `clear-cents-budget-planner` so the URL reads well, or add your own domain in Vercel → Settings → Domains.

## After deploying

1. Replace the Etsy link: search all files for `https://www.etsy.com/shop/worldtradenet` and swap in your listing URL once the listing is live (it appears in `index.html` and in the demo banner inside `_source/app.js` → rebuild, or edit `demo/index.html` directly).
2. Etsy description: link `https://<your-site>/demo/` as the free demo and `https://<your-site>/` as "see all features".
3. Buyer PDF: link the hidden start guide `https://<your-site>/p/cc-iaesf2gpr8/start/` (already done in the PDF provided).

## Editing the app later

Edit files in `_source/` (`app.js`, `app.css`, `site/…`), then run:
```
python3 _source/build.py .
```
That regenerates the demo, the hidden buyer app and the pages. Bump the cache names (`cc-app-v2` → `cc-app-v3`) in `_source/build.py` when you ship an update so installed phones fetch the new version.

## Notes
- Demo and app use separate browser storage, so playing in the demo never touches a buyer's real planner.
- The offline file stores data per browser too; buyers can move data with Settings → Download backup / Restore.
- Not financial advice — the app is a personal budgeting tool.
