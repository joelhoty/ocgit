"""Check approved reading order and complete, topic-local legacy anchor mapping."""
from pathlib import Path
from bs4 import BeautifulSoup
import json,sys,copy
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'AI_Agent_CLi').is_dir());R=Path(__file__).resolve().parents[1]
BEFORE=json.loads((R/'evidence/intro-before-reorder.json').read_text())
ORDER=['learning-route','agent-basics','minimal-environment','workspace-setup','cli-installation','first-task','session-controls','reliable-work','python-practice','practice-summary','appendix-installation','appendix-antigravity','appendix-history']
def validate(soup,mapping):
 errors=[];ids=[x['id'] for x in soup.select('[id]')]
 if len(ids)!=len(set(ids)):errors.append('duplicate IDs')
 if [x.get('id') for x in soup.select('h2')]!=ORDER:errors.append('main/appendix reading order mismatch')
 if set(mapping)!={x['id'] for x in BEFORE['ids']}:errors.append('missing or extra old ID mappings')
 for old,target in mapping.items():
  a=soup.find(id=old);h=soup.find(id=target)
  if a is None or h is None: errors.append('missing alias or target '+old);continue
  if old=='course-navigation-style':continue
  if h.name not in ['h1','h2','h3','h4']:errors.append('target not a topic heading '+old)
  if a is not h and a.find_next(['h1','h2','h3','h4']) is not h:errors.append('alias not beside mapped topic '+old)
 return errors
def content_checks(soup):
 before=BeautifulSoup((R/'inputs/00_intro.before.html').read_text(),'html.parser');errors=[]
 if [x.get_text() for x in before.select('pre code.language-python')]!=[x.get_text() for x in soup.select('pre code.language-python')]:errors.append('Python program changed or missing')
 if {x.get('src') for x in before.select('img')}!={x.get('src') for x in soup.select('img')}:errors.append('image inventory changed')
 original={a['href'] for a in before.select('a[href]') if a['href'].startswith('https:')}
 current={a['href'] for a in soup.select('a[href]') if a['href'].startswith('https:')}
 if original-current:errors.append('source URLs missing: '+str(sorted(original-current)))
 return errors
if __name__=='__main__':
 soup=BeautifulSoup((ROOT/'AI_Agent_CLi/00_intro.html').read_text(),'html.parser');f=R/'anchor-map.json'
 mapping=json.loads(f.read_text()) if f.exists() else {};errors=validate(soup,mapping)+content_checks(soup)
 negative={}
 if not errors:
  missing=copy.deepcopy(soup);missing.find(id='510').decompose();negative['missing_alias_rejected']=bool(validate(missing,mapping))
  duplicate=copy.deepcopy(soup);duplicate.body.append(copy.deepcopy(duplicate.find(id='510')));negative['duplicate_alias_rejected']=bool(validate(duplicate,mapping))
  wrong=copy.deepcopy(soup);a=wrong.find(id='510');a.extract();wrong.body.insert(0,a);negative['misplaced_alias_rejected']=bool(validate(wrong,mapping))
  if not all(negative.values()):errors.append('negative-control failure')
 print(json.dumps({'status':'FAIL' if errors else 'PASS','legacy_ids':len(mapping),'errors':errors,'negative_controls':negative},ensure_ascii=False,indent=2));sys.exit(bool(errors))
