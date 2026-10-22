"""Build the Vercel deploy folder from src/.  Usage: python3 build.py <out_dir>"""
import sys, shutil, pathlib

SRC = pathlib.Path(__file__).parent
OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else SRC.parent / "deploy")

tpl = (SRC / "app.html").read_text()
css = (SRC / "app.css").read_text()
js = (SRC / "app.js").read_text().replace("</script", "<\\/script")
PWA = ('<link rel="manifest" href="/manifest.webmanifest">'
       '<link rel="icon" href="/assets/icon.svg" type="image/svg+xml">'
       '<link rel="apple-touch-icon" href="/assets/icon-192.png">'
       '<meta name="apple-mobile-web-app-capable" content="yes">'
       '<meta name="mobile-web-app-capable" content="yes">'
       '<meta name="apple-mobile-web-app-title" content="Clear Cents">')
# offline single-file copy: inline SVG favicon, no manifest / service worker
ICON = '<link rel="icon" href="data:image/svg+xml,' + (SRC / "icon.svg").read_text().replace('"', "'").replace("#", "%23").replace("\n", "") + '">'

def page(mode, title, robots, pwa):
    return (tpl.replace("__MODE__", mode).replace("__TITLE__", title)
               .replace("__ROBOTS__", robots).replace("__PWA__", pwa)
               .replace("__CSS__", css).replace("__JS__", js))

NOINDEX = '<meta name="robots" content="noindex">'
builds = {
    "demo/index.html": page("demo", "Clear Cents — Live Demo · ADHD Budget Planner", "", PWA),
    "app/index.html": page("app", "Clear Cents — ADHD Budget Planner", NOINDEX, PWA),
    "download/clear-cents-budget-planner.html": page("offline", "Clear Cents — ADHD Budget Planner (offline)", NOINDEX, ICON),
}
OUT.mkdir(parents=True, exist_ok=True)
for rel, html in builds.items():
    p = OUT / rel; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(html)
for rel in ["index.html", "start/index.html"]:
    p = OUT / rel; p.parent.mkdir(parents=True, exist_ok=True); shutil.copy(SRC / "site" / rel, p)
for name in ["sw.js", "manifest.webmanifest", "vercel.json", "robots.txt"]:
    shutil.copy(SRC / name, OUT / name)
if (SRC / "assets").exists(): shutil.copytree(SRC / "assets", OUT / "assets", dirs_exist_ok=True)
(OUT / "assets").mkdir(exist_ok=True)
shutil.copy(SRC / "icon.svg", OUT / "assets" / "icon.svg")
# keep the editable source next to the site (excluded from deploy by .vercelignore)
if SRC.resolve() != (OUT / "_source").resolve(): shutil.copytree(SRC, OUT / "_source", dirs_exist_ok=True, ignore=shutil.ignore_patterns("assets", "__pycache__"))
for name in ["README.md", ".vercelignore"]:
    if SRC.resolve() != OUT.resolve() and (SRC / name).exists(): shutil.copy(SRC / name, OUT / name)
print("built", OUT)
