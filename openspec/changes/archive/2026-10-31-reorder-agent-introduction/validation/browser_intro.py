"""Fresh exhaustive old-fragment navigation without JS and representative visual checks."""
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright
from urllib.parse import quote
import json,threading
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'AI_Agent_CLi').is_dir());R=Path(__file__).resolve().parents[1];E=R/'evidence'
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}/AI_Agent_CLi/';seq=len(list(E.glob('browser-intro-*.json')))+1;results=[];errors=[]
with sync_playwright() as p:
 browser=p.chromium.launch(channel='chrome',headless=True)
 context=browser.new_context(java_script_enabled=False,viewport={'width':1280,'height':900});page=context.new_page()
 page.goto(base+'00_intro.html',wait_until='networkidle');page.evaluate("document.documentElement.style.scrollBehavior='auto'")
 for old,target in json.loads((R/'anchor-map.json').read_text()).items():
  if old=='course-navigation-style':continue
  page.goto(base+'00_intro.html#'+quote(old),wait_until='domcontentloaded');page.wait_for_timeout(30)
  old_y=page.evaluate('scrollY');node=page.locator('[id="'+old+'"]');dest=page.locator('[id="'+target+'"]')
  row={'old':old,'target':target,'alias_count':node.count(),'topic_count':dest.count(),'old_scroll':old_y,'topic':dest.inner_text() if dest.count()==1 else ''}
  page.goto(base+'00_intro.html#'+quote(target),wait_until='domcontentloaded');page.wait_for_timeout(30);row['target_scroll']=page.evaluate('scrollY')
  row['pass']=row['alias_count']==row['topic_count']==1 and abs(row['old_scroll']-row['target_scroll'])<180
  results.append(row)
  if len(results)%20==0: print('Legacy fragments checked:',len(results),flush=True)
  if not row['pass']:errors.append(row)
 context.close()
 context=browser.new_context()
 for width in [1280,390]:
  page=context.new_page();page.set_viewport_size({'width':width,'height':900})
  for name in ['index.html','00_intro.html']:
   response=page.goto(base+name,wait_until='networkidle',timeout=60000)
   if name=='00_intro.html':page.wait_for_function("Array.from(document.querySelectorAll('.mermaid')).every(e=>e.querySelector('svg'))",timeout=30000)
   row=page.evaluate('''() => ({width:innerWidth,scroll:document.documentElement.scrollWidth,brokenImages:Array.from(document.images).filter(x=>!x.complete||!x.naturalWidth).length,diagrams:document.querySelectorAll('.mermaid').length,rendered:document.querySelectorAll('.mermaid svg').length,diagramErrors:Array.from(document.querySelectorAll('.mermaid')).filter(e=>e.textContent.includes('Syntax error')).length})''')
   row.update(file=name,status=response.status);row['pass']=row['scroll']<=width+2 and not row['brokenImages'] and not row['diagramErrors'] and row['diagrams']==row['rendered'] and row['status']==200
   results.append(row)
   if not row['pass']:errors.append(row)
   page.screenshot(path=str(E/f'visual-{seq}-{width}-{Path(name).stem}.png'))
   if name=='00_intro.html':
    for anchor in ['first-task','slash-commands','study-program','appendix-installation']:
     page.locator('[id="'+anchor+'"]').scroll_into_view_if_needed();page.screenshot(path=str(E/f'visual-{seq}-{width}-{anchor}.png'))
  page.close()
 browser.close()
server.shutdown();out=E/f'browser-intro-{seq}.json';out.write_text(json.dumps({'status':'FAIL' if errors else 'PASS','results':results,'errors':errors},ensure_ascii=False,indent=2)+'\n');print(json.dumps({'status':'FAIL' if errors else 'PASS','cases':len(results),'errors':errors,'report':str(out)},ensure_ascii=False));raise SystemExit(bool(errors))
