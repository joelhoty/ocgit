from pathlib import Path
import json,threading,re,subprocess
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright
root=next(p for p in Path(__file__).resolve().parents if (p/'AI_Agent_CLi').is_dir());out=Path(__file__).with_name('verify-legacy-fresh.json')
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(root)));threading.Thread(target=server.serve_forever,daemon=True).start();base='http://127.0.0.1:'+str(server.server_port)
results=[]
with sync_playwright() as p:
 browser=p.chromium.launch(channel='chrome',headless=True)
 nojs=browser.new_context(java_script_enabled=False)
 def no_refresh(route):
  response=route.fetch();body=re.sub(r'<meta http-equiv="refresh"[^>]*>','',response.text());route.fulfill(response=response,body=body)
 nojs.route('**/GeminiForDesignTeaching/*.html*',no_refresh)
 for f in sorted((root/'GeminiForDesignTeaching').glob('*.html')):
  page=nojs.new_page();page.goto(base+'/GeminiForDesignTeaching/'+f.name+'#legacy-bookmark',wait_until='domcontentloaded');link=page.locator('#new-course-link');target=link.get_attribute('href');assert link.is_visible();link.click();assert '/AI_Agent_CLi/' in page.url;assert page.locator('h1').count();results.append({'legacy':f.name,'mode':'no JavaScript and meta refresh suppressed; clicked visible manual link','target':target,'final':page.url,'pass':True});page.close()
 js=browser.new_context()
 for f in sorted((root/'GeminiForDesignTeaching').glob('*.html')):
  page=js.new_page();page.goto(base+'/GeminiForDesignTeaching/'+f.name+'#legacy-bookmark',wait_until='domcontentloaded');page.wait_for_url('**/AI_Agent_CLi/**#legacy-bookmark');assert page.locator('h1').count();results.append({'legacy':f.name,'mode':'JavaScript redirect with obsolete fragment','final':page.url,'pass':True});page.close()
 version=browser.version;browser.close()
server.shutdown()
assert not out.exists();out.write_text(json.dumps({'status':'PASS','browser_version':version,'cases':len(results),'results':results},ensure_ascii=False,indent=2));print('PASS',len(results),'fresh high-risk browser cases; Chrome',version)
