"""Render reordered intro, positioning each legacy alias at its mapped topic."""
from pathlib import Path
from bs4 import BeautifulSoup
import markdown,json
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'AI_Agent_CLi').is_dir());R=Path(__file__).resolve().parents[1]
original=BeautifulSoup((R/'inputs/00_intro.before.html').read_text(),'html.parser')
rows=json.loads((R/'section-map.json').read_text());assert len({x['old_text'] for x in rows})==len(rows)
section_map={x['old_text']:x['new_id'] for x in rows}
page=ROOT/'AI_Agent_CLi/00_intro.html';soup=BeautifulSoup(page.read_text(),'html.parser')
new=BeautifulSoup(markdown.markdown(page.with_suffix('.md').read_text(),extensions=['fenced_code','tables','nl2br','toc','attr_list']),'html.parser')
for code in new.select('pre code.language-mermaid'):
    diagram=new.new_tag('div',attrs={'class':'mermaid'});diagram.string=code.get_text();code.parent.replace_with(diagram)
anchors={}
for old in original.select('[id]'):
    oldid=old['id']
    if old.name=='style':anchors[oldid]=oldid;continue
    if oldid=='59-cli':target='first-task'
    else:
        title=old.get_text(' ',strip=True)
        assert title in section_map,('unmapped original heading',oldid,title)
        target=section_map[title]
    h=new.find(id=target);assert h and h.name in ['h1','h2','h3','h4'],(oldid,target)
    anchors[oldid]=target
    if oldid!=target:
        assert not new.find(id=oldid),('alias collision',oldid)
        alias=new.new_tag('span',id=oldid,attrs={'class':'legacy-anchor','aria-hidden':'true'});h.insert_before(alias)
toc=new.new_tag('details',attrs={'class':'course-toc'});summary=new.new_tag('summary');summary.string='本頁章節';toc.append(summary);ul=new.new_tag('ul');toc.append(ul)
for h in new.select('h2'):
    li=new.new_tag('li');a=new.new_tag('a',href='#'+h['id']);a.string=h.get_text(' ',strip=True);li.append(a);ul.append(li)
new.h1.insert_after(toc)
container=soup.select_one('div.container');assert container;container.clear()
for child in list(new.contents):container.append(child.extract())
page.write_text(str(soup));(R/'anchor-map.json').write_text(json.dumps(anchors,ensure_ascii=False,indent=2)+'\n')
print('Rendered intro with',len(anchors),'legacy anchor mappings')
