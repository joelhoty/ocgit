"""Render every course page in Chrome: Mermaid, overflow, console errors, no-JS anchors and redirects."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import quote
import json
import sys
import threading

from playwright.sync_api import sync_playwright

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "AI_Agent_CLi").is_dir())
HERE = Path(__file__).resolve().parents[1]
SHOTS = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "evidence"
SHOTS.mkdir(parents=True, exist_ok=True)
STUBS = {"08_environment.html": "00_intro.html", "11_literacy_practice.html": "10_literacy.html", "12_literacy_research.html": "10_literacy.html"}


class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def main():
    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(Quiet, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_port}/AI_Agent_CLi/"
    pages = sorted(p.name for p in (ROOT / "AI_Agent_CLi").glob("*.html") if p.name not in STUBS)
    errors, rows = [], []
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True)
        for width in (1280, 390):
            context = browser.new_context(viewport={"width": width, "height": 900})
            for name in pages:
                page = context.new_page()
                logs = []
                page.on("console", lambda m: logs.append(m.text) if m.type == "error" and "favicon" not in m.location.get("url", "") else None)
                page.on("pageerror", lambda e: logs.append(str(e)))
                page.goto(base + name, wait_until="networkidle")
                page.wait_for_timeout(1500)
                state = page.evaluate("""() => ({
                    diagrams: document.querySelectorAll('.mermaid').length,
                    rendered: document.querySelectorAll('.mermaid svg').length,
                    failed: [...document.querySelectorAll('.mermaid')].filter(d => /Syntax error/i.test(d.textContent)).length,
                    overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
                    broken: [...document.images].filter(i => !i.naturalWidth).length })""")
                rows.append({"page": name, "width": width, **state, "console": len(logs)})
                if state["rendered"] != state["diagrams"] or state["failed"]:
                    errors.append(f"{name}@{width}: mermaid {state}")
                if state["overflow"] > 1:
                    errors.append(f"{name}@{width}: horizontal overflow {state['overflow']}")
                if state["broken"]:
                    errors.append(f"{name}@{width}: broken image")
                if logs:
                    errors.append(f"{name}@{width}: console {logs[:2]}")
                if name in ("00_intro.html", "index.html", "10_literacy.html", "04_workspace.html"):
                    page.screenshot(path=str(SHOTS / f"{Path(name).stem}-{width}.png"))
                if name == "00_intro.html":
                    page.locator("#vscode-workbench").scroll_into_view_if_needed()
                    page.wait_for_timeout(300)
                    page.screenshot(path=str(SHOTS / f"workbench-{width}.png"))
                page.close()
            context.close()
        context = browser.new_context(java_script_enabled=False, viewport={"width": 1280, "height": 900})
        page = context.new_page()
        page.goto(base + "00_intro.html", wait_until="domcontentloaded")
        page.evaluate("document.documentElement.style.scrollBehavior = 'auto'")  # smooth scroll would still be animating
        mapping = json.loads((HERE / "anchor-map.json").read_text(encoding="utf-8"))
        checked = 0
        for old, target in mapping.items():
            page.goto(base + "00_intro.html#" + quote(old), wait_until="domcontentloaded")
            page.wait_for_timeout(15)
            gap = page.evaluate("id => { const h = document.getElementById(id); return h ? Math.abs(h.getBoundingClientRect().top) : 1e9; }", target)
            checked += 1
            limit = page.evaluate("Math.max(0, document.documentElement.scrollHeight - innerHeight - scrollY) === 0")
            if gap > 80 and not limit:
                errors.append(f"anchor {old} -> {target}: {gap:.0f}px away")
        for stub, target in STUBS.items():
            page.goto(base + stub, wait_until="domcontentloaded")
            if not page.locator(f'a[href^="{target}"]').count():
                errors.append("stub without manual link " + stub)
        context.close()
        context = browser.new_context()
        page = context.new_page()
        for stub, target in STUBS.items():
            page.goto(base + stub)
            page.wait_for_url("**/" + target + "*", timeout=8000)
        browser.close()
    print(json.dumps({"status": "FAIL" if errors else "PASS", "pages": len(pages), "anchors_no_js": checked,
                      "mermaid": sum(r["rendered"] for r in rows if r["width"] == 1280), "errors": errors}, ensure_ascii=False, indent=2))
    sys.exit(bool(errors))


if __name__ == "__main__":
    main()
