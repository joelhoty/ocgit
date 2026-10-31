"""Capture observed editorial checks and independent reviews with SOS identities."""
from evidence_identity import ROOT,R,CHANGE,subject,policy,sha,validate
from pathlib import Path
import datetime,sys,subprocess,json,yaml,platform,re
E=R/'evidence';now=datetime.datetime.now(datetime.timezone.utc).isoformat()
run=subprocess.run([sys.executable,str(R/'validation/check_course.py')],capture_output=True,text=True,cwd=ROOT)
assert run.returncode==0,run.stdout+run.stderr
bad=[]
for f in (ROOT/'AI_Agent_CLi').glob('*'):
 if f.suffix in ['.md','.html']:
  for n,line in enumerate(f.read_text().splitlines(),1):
   if re.search(r'(?:codex|claude)(?: exec| -p| +["\u201c]| +&quot;)',line):bad.append(f'{f.name}:{n}')
assert not bad,bad
assert subprocess.run(['git','diff','--check'],cwd=ROOT).returncode==0
browser_path=sorted(E.glob('browser-results-*.json'),key=lambda p:p.stat().st_mtime)[-1]
browser=json.loads(browser_path.read_text());assert browser['status']=='PASS'
reviews=[E/'spec-review-v2.md',E/'quality-review-v1.md',E/'visual-review.md',E/'spec-policy-review.md']
for f in reviews:assert 'PASS' in f.read_text(),f
sub=subject();checks=[];report=['# Review report',f'Date: {now}',f'Final subject: `{sub["subject_hash"]}`','', 'Both Standard tasks reconciled from baseline: existing course static checks passed, but old command-plus-prompt examples failed the approved interaction criteria. Task 2 includes chapter 05 corrections discovered by whole-course review. No paid CLI/model task execution was needed for this editorial change.','']
for i in [1,2]:
 ids,pol=policy(i)
 payload=E/f'task-{i}-final-{len(list(E.glob(f"task-{i}-final-*.json")))+1}.json'
 payload.write_text(json.dumps(dict(task_id=f'task-{i}',subject_hash=sub['subject_hash'],static=json.loads(run.stdout),command_prompt_matches=bad,browser={'path':browser_path.relative_to(ROOT).as_posix(),'sha256':sha(browser_path.read_bytes()),'cases':len(browser['results'])},reviews=[{'path':f.relative_to(ROOT).as_posix(),'sha256':sha(f.read_bytes())} for f in reviews],captured_at=now),ensure_ascii=False,indent=2)+'\n')
 for kind in ['automated','representative']:
  c=dict(id=f'task-{i}.{kind}',task_id=f'task-{i}',requirement_ids=ids,kind=kind,subject=sub,policy=pol,result='pass',evidence_path=payload.relative_to(ROOT).as_posix(),evidence_sha256='sha256:'+sha(payload.read_bytes()),captured_at=now,summary='Final source/render invariants, interaction scan, independent reviews and browser checks.')
  if kind=='automated':
   c['command']='python3 '+(CHANGE/'validation/capture_evidence.py').as_posix();c['tool']=dict(name='Python',version=platform.python_version(),version_compatibility='same-major')
  else:
   c['actor']={'type':'AI','id':'independent-spec-and-quality-reviewers-plus-parent-visual'};c['procedure']='Inspect complete changed instructional examples and representative desktop/mobile screenshots: intro slash table, long workflow and assessment; verify sources, parity, input location, session progression, batch failure handling. See linked immutable review records.'
  checks.append(c)
 fail=E/'baseline-interaction.txt'
 report += [f'## Task {i}',f'- task_id: task-{i}',f'- subject_hash: `{sub["subject_hash"]}`',f'- Adapted fail: `{fail.relative_to(ROOT)}` (`sha256:{sha(fail.read_bytes())}`)',f'- Adapted pass: `{payload.relative_to(ROOT)}` (`sha256:{sha(payload.read_bytes())}`)','- Spec compliance: PASS (spec-review-v2.md); chapter05 remnants and transient rendering mismatch corrected.','- Quality: PASS (quality-review-v1.md).','- Local variation: chapter05 paths added under approved whole-course consistency provision.','']
m=dict(schema='sos-evidence/v1',change='prioritize-interactive-cli-teaching',captured_at=now,worktree=dict(path=str(ROOT),commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),diff_hash=sub['subject_hash']),checks=checks,manual_gaps=[])
validate(m);(R/'evidence-manifest.yaml').write_text(yaml.safe_dump(m,sort_keys=False,allow_unicode=True));(R/'review-report.md').write_text('\n'.join(report)+'\n## Final review\nPASS: all requirements and both task outcomes covered; execution limits remain explicit.\n')
print('Captured four checks for two Standard tasks.')
