"""Add course navigation and preserve legacy anchors after content rendering."""
from pathlib import Path
from bs4 import BeautifulSoup
import html, re, json
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'AI_Agent_CLi').is_dir())
NEW=ROOT/'AI_Agent_CLi'; OLD=ROOT/'GeminiForDesignTeaching'
RENAME={'Gemini_CLI_Tutorial_b02.html':'AI_CLI_Tutorial_b03.html','unit05_gemini_md_customization_b01.html':'unit05_agent_instructions_b02.html'}
ORDER=['AI_working_env_b05.html','unit01_first_ai_material_b02.html','unit02_ai_image_generation_b02.html','unit03_notebooklm_b02.html','unit04_local_ai_setup_b02.html','unit04_supplement_additions.html','unit05_agent_instructions_b02.html','unit06_practical_lesson_plan_b02.html','unit06_supplement_additions.html']
STYLE='''<style id="course-navigation-style">
html{scroll-behavior:smooth}body{box-sizing:border-box}img{max-width:100%;height:auto}pre{max-width:100%;overflow-x:auto}table{display:block;max-width:100%;overflow-x:auto}td,th{min-width:7em}.course-nav{display:flex;flex-wrap:wrap;gap:.65em;align-items:center;padding:1em 0;margin:1em 0;border-bottom:1px solid #3e3e3e;font-size:.95rem}.course-nav a{color:#66b3ff}.course-nav span{color:#aaa}.course-toc{margin:1.5em 0;padding:1em;background:#222831;border-radius:8px}.course-toc a{overflow-wrap:anywhere}h1,h2,h3,p,li{overflow-wrap:break-word}.mermaid svg{max-width:100%;height:auto}@media(max-width:600px){body{padding:14px!important}h1{font-size:1.65em}pre code{padding:1em}.course-nav{line-height:1.8}}
</style>'''
for p in NEW.glob('*.html'):
 text=p.read_text();soup=BeautifulSoup(text,'html.parser')
 if not soup.body: raise ValueError(p)
 # Restore Mermaid source as text so <br/> is syntax, never a DOM child.
 md=p.with_suffix('.md')
 if md.exists():
  blocks=[]; fence=None; lang=None; buf=[]
  for line in md.read_text().splitlines():
   if fence is None:
    m=re.match(r'^(`{3,}|~{3,})(.*)$',line)
    if m: fence=m[1];lang=m[2].strip();buf=[]
   elif re.fullmatch(re.escape(fence[0])+r'{'+str(len(fence))+r',}\s*',line):
    if lang=='mermaid': blocks.append('\n'.join(buf)+'\n')
    fence=None
   else: buf.append(line)
  nodes=soup.select('.mermaid')
  if len(nodes)!=len(blocks): raise ValueError('Mermaid count mismatch: '+p.name)
  for node,source in zip(nodes,blocks): node.clear();node.append(source)
 # Preserve substantive old anchors, even when heading text changed.
 old_name=next((k for k,v in RENAME.items() if v==p.name),p.name); orig=OLD/old_name
 existing={x.get('id') for x in soup.select('[id]')}
 if orig.exists():
  legacy=BeautifulSoup(orig.read_text(),'html.parser')
  for h in legacy.select('[id]'):
   anchor=h.get('id')
   if anchor and anchor not in existing:
    alias=soup.new_tag('span',id=anchor);alias['class']='legacy-anchor';soup.body.insert(0,alias);existing.add(anchor)
 # Stable headings for table of contents; existing anchors kept.
 for i,h in enumerate(soup.select('h2'),1):
  if not h.get('id'): h['id']='section-'+str(i)
 if p.name!='index_content.html':
  for oldnav in soup.select('.course-nav,.course-toc'): oldnav.decompose()
  nav='<nav class="course-nav" aria-label="課程導覽"><a href="index_content.html">課程目錄</a>'
  if p.name in ORDER:
   i=ORDER.index(p.name)
   if i: nav+=f'<a href="{ORDER[i-1]}">← 上一章</a>'
   if i+1<len(ORDER): nav+=f'<a href="{ORDER[i+1]}">下一章 →</a>'
  else: nav+='<a href="AI_working_env_b05.html">前導章</a>'
  if p.with_suffix('.md').exists(): nav+=f'<a href="{p.with_suffix(".md").name}">Markdown 原文</a>'
  nav+='<span>雙 CLI 教材 · 2026-10-31</span></nav>'
  soup.body.insert(0,BeautifulSoup(nav,'html.parser'))
  heads=soup.select('h2')
  if heads:
   toc='<details class="course-toc"><summary>本頁章節</summary><ul>'+''.join(f'<li><a href="#{html.escape(h["id"],quote=True)}">{html.escape(h.get_text(" ",strip=True))}</a></li>' for h in heads)+'</ul></details>'
   soup.h1.insert_after(BeautifulSoup(toc,'html.parser'))
  soup.body.append(BeautifulSoup(nav,'html.parser'))
 if soup.select_one('#course-navigation-style'): soup.select_one('#course-navigation-style').decompose()
 soup.head.append(BeautifulSoup(STYLE,'html.parser'))
 p.write_text(str(soup))
# Only replace old pages once all destinations exist.
for p in OLD.glob('*.html'):
 dest=NEW/RENAME.get(p.name,p.name)
 if not dest.exists(): raise ValueError('Missing redirect target: '+str(dest))
for p in OLD.glob('*.html'):
 dest='../AI_Agent_CLi/'+RENAME.get(p.name,p.name)
 p.write_text(f'''<!doctype html>
<html lang="zh-TW"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>教材已移至 AI Agent CLI</title><meta http-equiv="refresh" content="2;url={dest}"><style>body{{font:1.1rem/1.8 system-ui;background:#20242a;color:#eee;max-width:50em;margin:10vh auto;padding:1.5em}}a{{color:#72b7ff}}</style></head><body><h1>教材已改版</h1><p>本章已更新為 Codex CLI／Claude Code 教材。</p><p><a id="new-course-link" href="{dest}">前往新版對應章節 →</a></p><p>若原書籤的小節已更名，請使用新版「本頁章節」尋找內容。</p><script>const target={json.dumps(dest)};document.getElementById('new-course-link').href=target+location.hash;location.replace(target+location.hash);</script></body></html>''')
print('Navigation and legacy redirects generated for',len(list(NEW.glob('*.html'))),'new pages.')
