"""Validate rendered course links and migration invariants without running lesson commands."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
from bs4 import BeautifulSoup
import re, sys, json
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'AI_Agent_CLi').is_dir())
NEW=ROOT/'AI_Agent_CLi'; OLD=ROOT/'GeminiForDesignTeaching'
rename={'Gemini_CLI_Tutorial_b02.html':'AI_CLI_Tutorial_b03.html','unit05_gemini_md_customization_b01.html':'unit05_agent_instructions_b02.html','unit05_gemini_md_customization_b01.md':'unit05_agent_instructions_b02.md'}
final_names=json.loads((Path(__file__).parent/'filename-map.json').read_text())
def final_name(name):
 p=Path(name);return final_names.get(p.stem,p.stem)+p.suffix
errors=[]; counts={'html':0,'local_links':0,'redirects':0,'markdown_pairs':0}
def fail(msg): errors.append(msg)
for src in sorted(OLD.iterdir()):
 if src.suffix not in ('.html','.md'): continue
 target=NEW/final_name(rename.get(src.name,src.name))
 if not target.exists(): fail('Missing target '+str(target.relative_to(ROOT)))
for p in sorted(NEW.glob('*.html')):
 counts['html']+=1
 soup=BeautifulSoup(p.read_text(),'html.parser')
 if not soup.title or not soup.h1: fail(p.name+': missing title/h1')
 for e in soup.select('[href], [src]'):
  u=e.get('href') or e.get('src'); parts=urlsplit(u)
  if parts.scheme or parts.netloc: continue
  path=unquote(parts.path); target=(p.parent/path).resolve() if path else p
  counts['local_links']+=1
  if 'GeminiForDesignTeaching' in path: fail(p.name+': old internal link '+u)
  if not target.exists(): fail(p.name+': missing link '+u);continue
  if parts.fragment and target.suffix=='.html':
   dest=BeautifulSoup(target.read_text(),'html.parser'); anchor=unquote(parts.fragment)
   if not dest.find(id=anchor) and not dest.find('a',attrs={'name':anchor}): fail(p.name+': missing anchor '+u)
 for code in soup.select('pre'):
  if re.search(r'(?im)^\s*(?:npm install.*@google/gemini-cli|gemini(?:\s|$))',code.get_text()) and p.name!='00_intro.html': fail(p.name+': obsolete operational command')
 md=p.with_suffix('.md')
 if md.exists():
  counts['markdown_pairs']+=1
  # Render independently to compare substantive headings, excluding generated navigation.
  import markdown
  rendered=BeautifulSoup(markdown.markdown(md.read_text(),extensions=['extra','toc','sane_lists']),'html.parser')
  heads=[x.get_text(' ',strip=True) for x in rendered.select('h1,h2')]
  actual=[x.get_text(' ',strip=True) for x in soup.select('h1,h2')]
  if heads!=actual: fail(p.name+': Markdown/HTML h1-h2 mismatch')
  expected_blocks=[x.get_text().rstrip('\n') for x in rendered.select('pre code')]
  actual_blocks=[x.get_text().strip('\n') for x in soup.select('pre code,div.mermaid')]
  if [x.strip('\n') for x in expected_blocks]!=actual_blocks: fail(p.name+': Markdown/HTML fenced content mismatch')
for p in sorted(OLD.glob('*.html')):
 s=BeautifulSoup(p.read_text(),'html.parser'); target='../AI_Agent_CLi/'+final_name(rename.get(p.name,p.name))
 if not s.find('a',href=target): fail(p.name+': missing manual redirect link')
 if not s.find('meta',attrs={'http-equiv':re.compile('refresh',re.I)}): fail(p.name+': missing HTML redirect')
 counts['redirects']+=1
idx=NEW/'index.html'
if idx.exists():
 t=idx.read_text()
 if t.find('00_intro.html')<0 or t.find('00_intro.html')>t.find('01_materials.html'): fail('Intro not before unit1')
 if '00_intro.md' not in t: fail('Intro Markdown link missing')
else: fail('New index missing')
root_soup=BeautifulSoup((ROOT/'index.html').read_text(),'html.parser')
for a in root_soup.select('a[href]'):
 if a['href'].startswith('AI_Agent_CLi/') and not (ROOT/a['href']).exists(): fail('Root index: missing '+a['href'])
expected_names={final_name(rename.get(p.name,p.name)) for p in OLD.iterdir() if p.suffix in ('.md','.html')}|{'00_intro.html','00_intro.md'}
actual_names={p.name for p in NEW.iterdir() if p.suffix in ('.md','.html')}
if expected_names!=actual_names: fail('Concise filename inventory mismatch: '+str(expected_names^actual_names))
print(json.dumps({'status':'FAIL' if errors else 'PASS','counts':counts,'errors':errors},ensure_ascii=False,indent=2))
sys.exit(bool(errors))
