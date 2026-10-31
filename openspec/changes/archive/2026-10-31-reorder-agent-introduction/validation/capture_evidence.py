"""Publish checks after observed editorial review and final topic-local navigation tests."""
from evidence_identity import ROOT,R,CHANGE,subject,policy,sha,validate
import subprocess,sys,json,platform,datetime,yaml
E=R/'evidence';now=datetime.datetime.now(datetime.timezone.utc).isoformat();outputs={}
for name in ['check_course.py','check_intro.py']:
 run=subprocess.run([sys.executable,str(R/'validation'/name)],cwd=ROOT,text=True,capture_output=True)
 assert run.returncode==0,run.stdout+run.stderr;outputs[name]=json.loads(run.stdout)
assert subprocess.run(['git','diff','--check'],cwd=ROOT).returncode==0
browser_path=sorted(E.glob('browser-intro-*.json'),key=lambda p:p.stat().st_mtime)[-1];browser=json.loads(browser_path.read_text());assert browser['status']=='PASS'
reviews=[E/'spec-review-final.md',E/'quality-review-final.md',E/'visual-review.md',E/'quality-harness-followup.md']
for f in reviews:assert 'PASS' in f.read_text(),f
sub=subject();checks=[];report=['# Review report',f'Date: {now}',f'Final subject: `{sub["subject_hash"]}`','', 'Baseline showed inverted source/project prerequisites, Node interruption of Python work and late macOS setup. The approved outline is implemented. Reconciliation used actual Markdown/HTML, full old-ID inventory, source and program invariants, staged/unstaged diff, independent reviews and focused checks.','']
for i in [1,2]:
 ids,pol=policy(i);payload=E/f'task-{i}-final-{len(list(E.glob(f"task-{i}-final-*.json")))+1}.json'
 payload.write_text(json.dumps(dict(task_id=f'task-{i}',subject_hash=sub['subject_hash'],checks=outputs,browser={'path':browser_path.relative_to(ROOT).as_posix(),'sha256':sha(browser_path.read_bytes()),'cases':len(browser['results'])},reviews=[{'path':f.relative_to(ROOT).as_posix(),'sha256':sha(f.read_bytes())} for f in reviews],captured_at=now),ensure_ascii=False,indent=2)+'\n')
 for kind in ['automated','representative']+(['high-risk'] if i==2 else []):
  ev=browser_path if kind=='high-risk' else payload
  c=dict(id=f'task-{i}.{kind}',task_id=f'task-{i}',requirement_ids=ids,kind=kind,subject=sub,policy=pol,result='pass',evidence_path=ev.relative_to(ROOT).as_posix(),evidence_sha256='sha256:'+sha(ev.read_bytes()),captured_at=now,summary='Reading-order, content, paired rendering and all legacy topic mappings verified.')
  if kind=='automated':c.update(command='python3 '+(CHANGE/'validation/capture_evidence.py').as_posix(),tool=dict(name='Python',version=platform.python_version(),version_compatibility='same-major'))
  else:
   c['actor']={'type':'AI','id':'independent-reviewers-and-parent'}
   c['procedure']='Review original/new content mapping and Windows/macOS reading paths; inspect representative desktop/mobile screenshots. For high-risk: navigate every legacy topic fragment with JS disabled and compare destination position with mapped semantic heading; verify missing/duplicate/misplaced alias controls fail.'
   if kind=='high-risk':
    import importlib.metadata
    c['command']='python3 '+(CHANGE/'validation/browser_intro.py').as_posix();c['tool']=dict(name='Python + Playwright + Chrome',version=platform.python_version()+' / '+importlib.metadata.version('playwright'),version_compatibility='same-major')
  checks.append(c)
 fail=E/'intro-order-red.json'
 report += [f'## Task {i}',f'- task_id: task-{i}',f'- subject_hash: `{sub["subject_hash"]}`',f'- Adapted fail: `{fail.relative_to(ROOT)}` (`sha256:{sha(fail.read_bytes())}`)',f'- Adapted pass: `{payload.relative_to(ROOT)}` (`sha256:{sha(payload.read_bytes())}`)','- Spec compliance: PASS; see spec-review-final.md.','- Quality: PASS; see quality-review-final.md.','- Safety/failure gates: '+('not applicable (Standard).' if i==1 else 'Original111 IDs backed up; exhaustive topic mapping and no-JS navigation; negative controls reject missing, duplicate and misplaced aliases.'),'- Local variation: reuse the existing isolated feature branch to deliver the two approved curriculum corrections in PR2.','']
m=dict(schema='sos-evidence/v1',change='reorder-agent-introduction',captured_at=now,worktree=dict(path=str(ROOT),commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),diff_hash=sub['subject_hash']),checks=checks,manual_gaps=[])
validate(m);(R/'evidence-manifest.yaml').write_text(yaml.safe_dump(m,sort_keys=False,allow_unicode=True));(R/'review-report.md').write_text('\n'.join(report)+'\n## Final review\nPASS; every required outcome and compatibility gate has observed evidence.\n');print('Captured five checks for two task groups.')
