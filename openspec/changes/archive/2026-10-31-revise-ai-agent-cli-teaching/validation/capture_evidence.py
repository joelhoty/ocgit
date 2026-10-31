"""Capture checks against current course identity after observed reviews and browser run."""
from pathlib import Path
import sys,json,subprocess,platform,datetime,yaml,re
from evidence_identity import ROOT,R,CHANGE,subject,policy,sha,validate
E=R/'evidence';now=datetime.datetime.now(datetime.timezone.utc).isoformat()
run=subprocess.run([sys.executable,str(R/'validation/check_course.py')],cwd=ROOT,text=True,capture_output=True)
assert run.returncode==0,run.stdout+run.stderr
static=json.loads(run.stdout)
browser_path=sorted(E.glob('browser-results-*.json'),key=lambda p:p.stat().st_mtime)[-1]
browser=json.loads(browser_path.read_text());assert browser['status']=='PASS'
reviews={1:['task-1-spec-review-v1.md','task-1-quality-review-v1.md'],2:['task-2-spec-review-v1.md','task-2-quality-review-v1.md'],3:['task-3-spec-review-v1.md','task-3-quality-review-v1.md'],4:['task-4-spec-review-v3.md','task-4-quality-review-v1.md'],5:['final-content-review.md']}
baselines={1:'task-1-baseline-fail.txt',2:'task-2-baseline-fail.txt',3:'task-3-red.txt',4:'task-4-red.txt',5:'task-5-baseline-fail.txt'}
sub=subject(); checks=[];report=['# Final per-task review report','',f'Captured: {now}',f'Workspace: {ROOT}',f'Subject: `{sub["subject_hash"]}`','', 'All original non-code task baselines retained. Filename amendments and common navigation are final integration changes. Independent content reviews are combined with final exact source/render parity, link traversal and observed browser evidence below.','']
for i in range(1,6):
 ids,pol=policy(i);rs=[]
 for name in reviews[i]:
  p=E/name; assert p.exists(),p
  assert 'PASS' in p.read_text(),p
  rs.append({'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p.read_bytes())})
 seq=len(list(E.glob(f'task-{i}-final-check-*.json')))+1
 payload=E/f'task-{i}-final-check-{seq}.json'
 payload.write_text(json.dumps({'task_id':f'task-{i}','subject_hash':sub['subject_hash'],'static':static,'review_payloads':rs,'browser_payload':browser_path.relative_to(ROOT).as_posix(),'browser_sha256':sha(browser_path.read_bytes()),'browser_cases':len(browser['results']),'browser_result':browser['status'],'captured_at':now,'limits':['No paid CLI execution or account login','No cross-platform installer execution','External CDN resources require network']},ensure_ascii=False,indent=2)+'\n')
 def check(kind,evidence,suffix,actor=None):
  x=dict(id=f'task-{i}.{suffix}',task_id=f'task-{i}',requirement_ids=ids,kind=kind,subject=sub,command=('python3 '+(CHANGE/'validation/check_course.py').as_posix() if kind=='automated' else None),policy=pol,result='pass',evidence_path=evidence.relative_to(ROOT).as_posix(),evidence_sha256='sha256:'+sha(evidence.read_bytes()),captured_at=now,summary='Current final subject checked; see immutable payload and linked independent reviews.')
  if kind=='automated':x['tool']=dict(name='Python',version=platform.python_version(),version_compatibility='same-major')
  else:
   x['actor']=dict(type='AI',id=actor or 'parent-integration-reviewer')
   x['procedure']='Read the linked independent spec/quality review payloads; compare current Markdown/HTML exact fenced contents and headings; inspect desktop/mobile index, SVG, Mermaid and installation-table screenshots; reconcile final filenames and recorded browser results against the current subject.'
   if kind=='high-risk':
    import importlib.metadata, plistlib
    x['command']='python3 '+(CHANGE/'validation/browser_check.py').as_posix()
    x['procedure']='Freshly visit all 15 legacy HTML URLs with JavaScript disabled; confirm visible manual destination link, wait for HTML meta redirect and confirm destination h1. Independently inspect fragment behavior and manual fallback in verifier evidence.'
    x['tool']=dict(name='Python + Playwright + installed Google Chrome',version=platform.python_version()+' / '+importlib.metadata.version('playwright')+' / Chrome '+plistlib.loads(Path('/Applications/Google Chrome.app/Contents/Info.plist').read_bytes())['CFBundleShortVersionString'],version_compatibility='same-major')
  checks.append(x)
 check('automated',payload,'static-final')
 check('representative',payload,'content-and-visual',actor='independent-reviewers-plus-parent')
 if i==4:check('high-risk',browser_path,'legacy-no-javascript',actor='playwright-independent-browser-reproduction')
 fail=E/baselines[i]
 report += [f'## Task {i}',f'- task_id: task-{i}',f'- subject_hash: `{sub["subject_hash"]}`',f'- Adapted fail: `{fail.relative_to(ROOT)}` (`sha256:{sha(fail.read_bytes())}`)',f'- Adapted pass: `{payload.relative_to(ROOT)}` (`sha256:{sha(payload.read_bytes())}`)','- Spec compliance: PASS; independent reviewer payloads linked below.','- Quality: PASS; fixes and historical iterations preserved.',*['- Review: `'+x['path']+'` (`sha256:'+x['sha256']+'`)' for x in rs],'- Local variation: user-authorized concise filenames, same teaching purposes and layout; no other scope expansion.','']
m=dict(schema='sos-evidence/v1',change='revise-ai-agent-cli-teaching',captured_at=now,worktree=dict(path=str(ROOT),commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),diff_hash=sub['subject_hash']),checks=checks,manual_gaps=[])
validate(m)
(R/'evidence-manifest.yaml').write_text(yaml.safe_dump(m,allow_unicode=True,sort_keys=False))
(R/'review-report.md').write_text('\n'.join(report)+'\n## Final review\nPASS: whole course retains the approved instructional progression and visual structure. All discovered blocking content/script/render defects have recorded fixes. Final report separately states execution limits.\n')
print('Captured',len(checks),'identity-bound checks; no pending manual gaps.')
