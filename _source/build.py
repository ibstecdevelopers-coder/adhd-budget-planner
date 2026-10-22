"""Build the Vercel deploy folder from src/.  Usage: python3 build.py <out_dir>

Public:  /            product page
         /demo/       live demo (sample data)
Private: /p/<slug>/                     buyer app            (link only in the buyer PDF)
         /p/<slug>/start/               buyer start guide
         /p/<slug>/download/...html     offline single-file planner
The secret <slug> lives in config.json and appears in NO public file.
"""
import sys, shutil, pathlib, json

SRC = pathlib.Path(__file__).parent
OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else SRC.parent / "deploy")
SLUG = json.loads((SRC / "config.json").read_text())["slug"]
PRIV = f"p/{SLUG}"

tpl = (SRC / "app.html").read_text()
css = (SRC / "app.css").read_text()
js = (SRC / "app.js").read_text().replace("</script", "<\\/script")
PWA = ('<link rel="manifest" href="manifest.webmanifest">'
       '<link rel="icon" href="/assets/icon.svg" type="image/svg+xml">'
       '<link rel="apple-touch-icon" href="/assets/icon-192.png">'
       '<meta name="apple-mobile-web-app-capable" content="yes">'
       '<meta name="mobile-web-app-capable" content="yes">'
       '<meta name="apple-mobile-web-app-title" content="Clear Cents">')
ICON = '<link rel="icon" href="data:image/svg+xml,' + (SRC / "icon.svg").read_text().replace('"', "'").replace("#", "%23").replace("\n", "") + '">'
NOINDEX = '<meta name="robots" content="noindex, nofollow"><meta name="referrer" content="no-referrer">'

def page(mode, title, robots, pwa):
    return (tpl.replace("__MODE__", mode).replace("__TITLE__", title)
               .replace("__ROBOTS__", robots).replace("__PWA__", pwa)
               .replace("__CSS__", css).replace("__JS__", js))

def manifest(name, short):
    m = json.loads((SRC / "manifest.webmanifest").read_text())
    m.update({"name": name, "short_name": short, "start_url": "./", "scope": "./", "id": "./"})
    return json.dumps(m, indent=2)

def sw(cache):
    return (SRC / "sw.js").read_text().replace("__CACHE__", cache)

OUT.mkdir(parents=True, exist_ok=True)
for old in ["app", "start", "download", "manifest.webmanifest", "sw.js"]:  # remove pre-hidden-link files
    t = OUT / old
    if t.is_dir(): shutil.rmtree(t)
    elif t.exists(): t.unlink()
if (OUT / "p").exists():
    for d in (OUT / "p").iterdir():
        if d.name != SLUG: shutil.rmtree(d)

files = {
    "demo/index.html": page("demo", "Clear Cents — Live Demo · ADHD Budget Planner", "", PWA),
    "demo/manifest.webmanifest": manifest("Clear Cents Demo", "CC Demo"),
    "demo/sw.js": sw("cc-demo-v2"),
    f"{PRIV}/index.html": page("app", "Clear Cents — ADHD Budget Planner", NOINDEX, PWA),
    f"{PRIV}/manifest.webmanifest": manifest("Clear Cents — ADHD Budget Planner", "Clear Cents"),
    f"{PRIV}/sw.js": sw("cc-app-v2"),
    f"{PRIV}/download/clear-cents-budget-planner.html": page("offline", "Clear Cents — ADHD Budget Planner (offline)", NOINDEX, ICON),
    f"{PRIV}/start/index.html": (SRC / "site" / "start" / "index.html").read_text(),
    "index.html": (SRC / "site" / "index.html").read_text(),
    "vercel.json": (SRC / "vercel.json").read_text(),
    "robots.txt": (SRC / "robots.txt").read_text(),
}
for rel, text in files.items():
    p = OUT / rel; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(text)

if (SRC / "assets").exists(): shutil.copytree(SRC / "assets", OUT / "assets", dirs_exist_ok=True)
(OUT / "assets").mkdir(exist_ok=True)
shutil.copy(SRC / "icon.svg", OUT / "assets" / "icon.svg")
# editable source kept beside the site, excluded from deploy by .vercelignore
if SRC.resolve() != (OUT / "_source").resolve():
    shutil.copytree(SRC, OUT / "_source", dirs_exist_ok=True, ignore=shutil.ignore_patterns("assets", "__pycache__"))
for name in ["README.md", ".vercelignore"]:
    if SRC.resolve() != OUT.resolve() and (SRC / name).exists(): shutil.copy(SRC / name, OUT / name)
print("built", OUT, "| buyer app: /" + PRIV + "/")
