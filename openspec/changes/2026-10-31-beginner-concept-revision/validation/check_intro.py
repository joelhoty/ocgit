"""Check reading order, legacy anchors, program integrity, and Markdown/HTML parity."""
from pathlib import Path
import json
import re
import sys

import markdown
from bs4 import BeautifulSoup

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "AI_Agent_CLi").is_dir())
HERE = Path(__file__).resolve().parents[1]
ORDER = ["learning-route", "agent-basics", "workspace-setup", "cli-installation", "first-task", "project-rules",
         "understand-system", "session-controls", "reliable-work", "practice-summary", "python-practice",
         "troubleshooting", "appendix-installation", "appendix-antigravity", "appendix-history"]
HEADINGS = ["h1", "h2", "h3", "h4"]


def main():
    page = ROOT / "AI_Agent_CLi/00_intro.html"
    soup = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
    before = BeautifulSoup((HERE / "inputs/00_intro.before.html").read_text(encoding="utf-8"), "html.parser")
    mapping = json.loads((HERE / "anchor-map.json").read_text(encoding="utf-8"))
    errors = []
    ids = [x["id"] for x in soup.select("[id]")]
    if len(ids) != len(set(ids)):
        errors.append("duplicate ids: " + str(sorted({i for i in ids if ids.count(i) > 1})))
    if [h.get("id") for h in soup.select("h2")] != ORDER:
        errors.append("reading order mismatch: " + str([h.get("id") for h in soup.select("h2")]))
    for old, target in mapping.items():
        alias, heading = soup.find(id=old), soup.find(id=target)
        if alias is None or heading is None:
            errors.append("missing " + old)
        elif alias is not heading and alias.find_next(HEADINGS) is not heading:
            errors.append("alias not beside topic " + old)
    code = lambda s: [x.get_text() for x in s.select("pre code.language-python")]
    if code(before) != code(soup):
        errors.append("Python program changed")
    if {i.get("src") for i in before.select("img")} != {i.get("src") for i in soup.select("img")}:
        errors.append("image inventory changed")
    links = lambda s: {a["href"] for a in s.select("a[href]") if a["href"].startswith("https:")}
    if links(before) - links(soup):
        errors.append("source URLs removed: " + str(sorted(links(before) - links(soup))))
    for a in soup.select('a[href^="#"]'):
        if not soup.find(id=a["href"][1:]):
            errors.append("broken internal link " + a["href"])
    rendered = BeautifulSoup(markdown.markdown(page.with_suffix(".md").read_text(encoding="utf-8"),
                                               extensions=["fenced_code", "tables", "nl2br", "toc", "attr_list"]), "html.parser")
    heads = lambda s: [h.get_text(" ", strip=True) for h in s.select("h1,h2,h3")]
    if heads(rendered) != heads(soup):
        errors.append("Markdown/HTML heading mismatch")
    md = page.with_suffix(".md").read_text(encoding="utf-8")
    for word in ["高中生", "原稿", "編寫教材時未代替"]:
        if word in md:
            errors.append("leftover wording: " + word)
    if re.search(r"^### (\d+\.\d+|[A-C]\.\d+) (\d+\.\d+|[A-C]\.\d+) ", md, re.M):
        errors.append("double section number")
    print(json.dumps({"status": "FAIL" if errors else "PASS", "legacy_ids": len(mapping), "errors": errors}, ensure_ascii=False, indent=2))
    sys.exit(bool(errors))


if __name__ == "__main__":
    main()
