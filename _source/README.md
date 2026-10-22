# Clear Cents — ADHD Budget Planner (Vercel site)

A static website: no framework, no database, no build step on Vercel. Customer data is stored in each buyer's own browser (localStorage), so there's nothing to host except these files.

## What's in this folder

| URL on your site | File | What it is |
|---|---|---|
| `/` | `index.html` | Product details page for your Etsy customers (features, screenshots, FAQ, links) |
| `/demo/` | `demo/index.html` | Free live demo, pre-filled with sample data, with a "Get the full planner" banner. Put this link in your Etsy description. |
| `/app/` | `app/index.html` | The real planner for buyers — starts empty with a setup checklist (hidden from Google) |
| `/start/` | `start/index.html` | Buyer welcome guide: app link, phone install steps, offline download, backup tips. Put this link in the PDF buyers download from Etsy. |
| `/download/…` | `download/clear-cents-budget-planner.html` | Single-file offline planner for desktop |
| — | `manifest.webmanifest`, `sw.js`, `assets/icon-*.png` | Lets buyers install the app on iPhone/Android and use it offline |
| — | `vercel.json` | Clean URLs, cache rules, download header, security headers |
| — | `_source/` | Editable source + `build.py` (not deployed — see `.vercelignore`) |

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
3. Buyer PDF: link `https://<your-site>/start/`.

## Editing the app later

Edit files in `_source/` (`app.js`, `app.css`, `site/…`), then run:
```
python3 _source/build.py .
```
That regenerates `demo/`, `app/`, `download/` and the pages. Bump `CACHE` in `_source/sw.js` (e.g. `clear-cents-v2`) when you ship an update so installed phones fetch the new version.

## Notes
- Demo and app use separate browser storage, so playing in the demo never touches a buyer's real planner.
- The offline file stores data per browser too; buyers can move data with Settings → Download backup / Restore.
- Not financial advice — the app is a personal budgeting tool.
