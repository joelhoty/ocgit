"""Apply the user's approved concise English filename amendment."""
from pathlib import Path
import json,re
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'AI_Agent_CLi').is_dir())
HERE=Path(__file__).resolve().parent
mapping=json.loads((HERE/'filename-map.json').read_text())
course=ROOT/'AI_Agent_CLi'
for src,dst in mapping.items():
 for suffix in ['.md','.html']:
  a=course/(src+suffix); b=course/(dst+suffix)
  if a.exists() and a!=b:
   if b.exists(): raise ValueError('Refusing overwrite '+str(b))
   a.rename(b)
paths=list(course.glob('*.html'))+list(course.glob('*.md'))+list((ROOT/'GeminiForDesignTeaching').glob('*.html'))+[ROOT/p for p in ['index.html','README.md','git_index.md','CONTRIBUTING.md']]
for p in paths:
 s=p.read_text()
 for a,b in mapping.items():
  for suffix in ['.md','.html']: s=s.replace(a+suffix,b+suffix)
 p.write_text(s)
# Order course cards to match filename sequence while preserving all card styling.
from bs4 import BeautifulSoup
p=course/'index.html';s=BeautifulSoup(p.read_text(),'html.parser');grid=s.select_one('.course-grid')
cards=list(grid.select(':scope > .course-card'))
cards.sort(key=lambda c:c.select_one('a.view-link')['href'])
for c in cards: grid.append(c.extract())
p.write_text(str(s))
print('Applied',len(mapping),'concise topic mappings and updated all course/root/legacy HTML links.')
