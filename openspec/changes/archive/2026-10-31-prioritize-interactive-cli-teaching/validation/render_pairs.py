"""Render edited Markdown into the existing page shell, retaining design and anchors."""
from pathlib import Path
from bs4 import BeautifulSoup
import markdown
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'AI_Agent_CLi').is_dir())
for name in ['00_intro','04_workspace','04a_workflows','06_lesson_plans','06a_assessment','05_instructions']:
    md=ROOT/'AI_Agent_CLi'/f'{name}.md'; page=md.with_suffix('.html')
    soup=BeautifulSoup(page.read_text(),'html.parser')
    container=soup.select_one('div.container'); assert container is not None,name
    old_ids={x['id'] for x in container.select('[id]')}
    new=BeautifulSoup(markdown.markdown(md.read_text(),extensions=['fenced_code','tables','nl2br','toc']),'html.parser')
    for node in new.select('pre code.language-mermaid'):
        diagram=new.new_tag('div',attrs={'class':'mermaid'}); diagram.string=node.get_text();node.parent.replace_with(diagram)
    toc=new.new_tag('details',attrs={'class':'course-toc'}); summary=new.new_tag('summary');summary.string='本頁章節';toc.append(summary);ul=new.new_tag('ul');toc.append(ul)
    for h in new.select('h2'):
        li=new.new_tag('li');a=new.new_tag('a',href='#'+h['id']);a.string=h.get_text(' ',strip=True);li.append(a);ul.append(li)
    new.h1.insert_after(toc)
    new_ids={x['id'] for x in new.select('[id]')}
    container.clear()
    for anchor in sorted(old_ids-new_ids):container.append(soup.new_tag('span',id=anchor,attrs={'class':'legacy-anchor'}))
    for child in list(new.contents): container.append(child.extract())
    page.write_text(str(soup))
    print(page.relative_to(ROOT))
