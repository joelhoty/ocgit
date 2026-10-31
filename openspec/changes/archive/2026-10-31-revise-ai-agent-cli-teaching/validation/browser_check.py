"""Render all pages; exercise old entry points with JavaScript disabled."""
from pathlib import Path
import json, threading
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'AI_Agent_CLi').is_dir()); E=Path(__file__).resolve().parents[1]/'evidence'
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args): pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
base='http://127.0.0.1:'+str(server.server_port)
results=[]; failures=[]
with sync_playwright() as p:
 browser=p.chromium.launch(channel='chrome',headless=True)
 context=browser.new_context(viewport={'width':1280,'height':900})
 for width in [1280,390]:
  page=context.new_page();page.set_viewport_size({'width':width,'height':900})
  for f in sorted((ROOT/'AI_Agent_CLi').glob('*.html')):
   errors=[]
   handler=lambda err:errors.append(str(err))
   page.on('pageerror',handler)
   response=page.goto(base+'/AI_Agent_CLi/'+f.name,wait_until='networkidle',timeout=60000)
   # Mermaid CDN may need additional layout time; wait only when diagrams exist.
   if page.locator('.mermaid').count():
    try: page.wait_for_function("Array.from(document.querySelectorAll('.mermaid')).every(e=>e.querySelector('svg'))",timeout=20000)
    except Exception: pass
   data=page.evaluate('''() => ({title:document.title,width:innerWidth,scroll:document.documentElement.scrollWidth,diagrams:document.querySelectorAll('.mermaid').length,rendered:document.querySelectorAll('.mermaid svg').length,brokenImages:Array.from(document.images).filter(i=>!i.complete||!i.naturalWidth).map(i=>i.src),diagramErrors:Array.from(document.querySelectorAll('.mermaid')).filter(e=>e.textContent.includes('Syntax error')).length})''')
   data.update(file=f.name,status=response.status,errors=errors)
   if data['scroll']>width+2 or data['brokenImages'] or data['diagramErrors'] or data['diagrams']!=data['rendered'] or response.status!=200: failures.append(data)
   results.append(data)
   if f.name in ['index.html','00_intro.html','08_environment.html','05_instructions.html','06_lesson_plans.html']:
    page.screenshot(path=str(E/f'visual-{width}-{f.stem}.png'),full_page=False)
   page.remove_listener('pageerror',handler)
  page.close()
 # Fresh exhaustive compatibility failure-path verification.
 nojs=browser.new_context(java_script_enabled=False)
 for f in sorted((ROOT/'GeminiForDesignTeaching').glob('*.html')):
  page=nojs.new_page(); page.goto(base+'/GeminiForDesignTeaching/'+f.name+'#legacy-bookmark',wait_until='domcontentloaded')
  link=page.locator('#new-course-link'); target=link.get_attribute('href') if link.count() else None
  if not target: failures.append({'legacy':f.name,'failure':'manual link missing'})
  else:
   page.wait_for_url('**/AI_Agent_CLi/**',timeout=15000)
   if not page.locator('h1').count(): failures.append({'legacy':f.name,'failure':'destination missing heading'})
  results.append({'legacy':f.name,'javascript':False,'manual_target':target,'destination':page.url})
  page.close()
 browser.close()
server.shutdown()
report={'status':'FAIL' if failures else 'PASS','results':results,'failures':failures}
name='browser-results-'+str(len(list(E.glob('browser-results-*.json')))+1)+'.json'
(E/name).write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps({'report':name,'status':report['status'],'cases':len(results),'failures':failures},ensure_ascii=False,indent=2))
raise SystemExit(bool(failures))
