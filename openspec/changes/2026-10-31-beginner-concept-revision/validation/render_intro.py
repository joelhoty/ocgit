"""Render 00_intro.md into the existing page shell and keep every legacy anchor."""
from pathlib import Path
import json

import markdown
from bs4 import BeautifulSoup

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "AI_Agent_CLi").is_dir())
HERE = Path(__file__).resolve().parents[1]
MOVED = {
    "historical-inventory": "appendix-history",
    "version-history": "appendix-history",
    "historical-verification": "appendix-history",
    "historical-jev-compliance": "appendix-history",
    "historical-jev-diagrams": "appendix-history",
}
HEADINGS = ["h1", "h2", "h3", "h4"]


def legacy_targets(before):
    """Map every id in the old page to the heading that topic belongs to."""
    targets = {}
    for node in before.select("[id]"):
        if node.name == "style":
            continue
        if node.name in HEADINGS:
            targets[node["id"]] = MOVED.get(node["id"], node["id"])
        else:
            heading = node.find_next(HEADINGS)
            targets[node["id"]] = MOVED.get(heading["id"], heading["id"])
    return targets


def main():
    page = ROOT / "AI_Agent_CLi/00_intro.html"
    before = BeautifulSoup((HERE / "inputs/00_intro.before.html").read_text(encoding="utf-8"), "html.parser")
    soup = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
    new = BeautifulSoup(
        markdown.markdown(
            page.with_suffix(".md").read_text(encoding="utf-8"),
            extensions=["fenced_code", "tables", "nl2br", "toc", "attr_list"],
        ),
        "html.parser",
    )
    for code in new.select("pre code.language-mermaid"):
        diagram = new.new_tag("div", attrs={"class": "mermaid"})
        diagram.string = code.get_text()
        code.parent.replace_with(diagram)
    targets = legacy_targets(before)
    for old, target in targets.items():
        heading = new.find(id=target)
        assert heading is not None and heading.name in HEADINGS, (old, target)
        if old != target and not new.find(id=old):
            alias = new.new_tag("span", id=old, attrs={"class": "legacy-anchor", "aria-hidden": "true"})
            heading.insert_before(alias)
    toc = new.new_tag("details", attrs={"class": "course-toc"})
    summary = new.new_tag("summary")
    summary.string = "本頁章節"
    toc.append(summary)
    items = new.new_tag("ul")
    toc.append(items)
    for heading in new.select("h2"):
        item = new.new_tag("li")
        link = new.new_tag("a", href="#" + heading["id"])
        link.string = heading.get_text(" ", strip=True)
        item.append(link)
        items.append(item)
    new.h1.insert_after(toc)
    container = soup.select_one("div.container")
    assert container
    container.clear()
    for child in list(new.contents):
        container.append(child.extract())
    page.write_text(str(soup), encoding="utf-8")
    (HERE / "anchor-map.json").write_text(json.dumps(targets, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("rendered with", len(targets), "legacy ids")


if __name__ == "__main__":
    main()
