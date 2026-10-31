"""Canonical SOS evidence identity helpers, used to capture and independently validate."""
from pathlib import Path
import hashlib,re,json,sys,subprocess,datetime
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'AI_Agent_CLi').is_dir())
CHANGE=Path(__file__).resolve().parents[1].relative_to(ROOT)
R=ROOT/CHANGE
sha=lambda b:hashlib.sha256(b).hexdigest()
def norm(s): return ('\n'.join(x.rstrip(' \t') for x in s.replace('\r\n','\n').replace('\r','\n').split('\n')).rstrip('\n')+'\n').encode()
def section(s,anchor):
 lines=s.splitlines(keepends=True);indexes=[i for i,x in enumerate(lines) if x.rstrip('\n\r')==anchor]
 assert len(indexes)==1,(anchor,indexes)
 start=indexes[0];level=len(anchor)-len(anchor.lstrip('#'));end=len(lines)
 for i in range(start+1,len(lines)):
  m=re.match(r'^(#+) ',lines[i])
  if m and len(m[1])<=level: end=i;break
 return ''.join(lines[start:end])
def contracts():
 s=(R/'tasks.md').read_text()
 return [(h,section(s,h)) for h in re.findall(r'^### Task .+$',s,re.M)]
def policy(i):
 heading,task=contracts()[i-1];ids=sorted(set(re.findall(r'REQ-TEACH-\d+',task)))
 spec=(R/'specs/teaching/spec.md').read_text(); inputs=[]
 def add(kind,path,anchor,content,canon='sos-policy-input/v1'):
  inputs.append(dict(kind=kind,source_path=path.as_posix(),source_anchor=anchor,canonicalization=canon,sha256=sha(norm(content))))
 add('task_contract',CHANGE/'tasks.md',heading,re.sub(r'\[[xX ]\]','[ ]',task),'sos-task-contract/v1')
 for id in ids:
  hs=re.findall(r'^### Requirement: '+id+r' — .+$',spec,re.M);assert len(hs)==1
  add('spec_requirement',CHANGE/'specs/teaching/spec.md',hs[0],section(spec,hs[0]))
 add('design_constraint',CHANGE/'design.md','<whole-file>',(R/'design.md').read_text())
 add('design_constraint',CHANGE/'approved-amendment.md','<whole-file>',(R/'approved-amendment.md').read_text())
 add('verification_policy',CHANGE/'validation/sos-verify-policy.md','<whole-file>',(R/'validation/sos-verify-policy.md').read_text())
 inputs.sort(key=lambda x:(x['kind'],x['source_path'],x['source_anchor']))
 listing=''.join('\t'.join(x[k] for k in ['kind','source_path','source_anchor','canonicalization','sha256'])+'\n' for x in inputs)
 return ids,dict(id='sos-task-subject/v1',policy_inputs=inputs,policy_hash='sha256:'+sha(listing.encode()),paths_source='task Files plus linked course dependencies and validation tools',path_normalization='repo-relative POSIX',directory_expansion='recursive',sort='bytewise LC_ALL=C',regular_file_digest='SHA-256 of raw bytes',symlink_digest='SHA-256 of raw link-target bytes',listing_format='<sha256>  <path>\\n',subject_digest='SHA-256 of canonical listing bytes',exclusions=['tasks.md','evidence-manifest.yaml','review-report.md','generated-evidence-payloads'],invalidates_on=['constituent_path_or_digest_change','command_change','incompatible_tool_version_change','policy_change','evidence_payload_digest_change'],ttl=None)
def subject():
 paths=list((ROOT/'AI_Agent_CLi').rglob('*'))+list((ROOT/'GeminiForDesignTeaching').glob('*'))+[ROOT/x for x in ['index.html','README.md','CONTRIBUTING.md','git_index.md','md2htmlv2.py']]+list((R/'validation').glob('*.py'))+[R/'sources.md',R/'validation/filename-map.json']
 paths=sorted({p for p in paths if p.is_file()},key=lambda p:p.relative_to(ROOT).as_posix().encode())
 cs=[dict(path=p.relative_to(ROOT).as_posix(),type='regular',sha256=sha(p.read_bytes())) for p in paths]
 listing=''.join(x['sha256']+'  '+x['path']+'\n' for x in cs)
 return dict(base_commit='b53e3dec4c41d1e951c8d1c537b4bcdfbe5a9431',constituents=cs,subject_hash='sha256:'+sha(listing.encode()))
def validate(manifest):
 for c in manifest['checks']:
  assert c['subject']==subject(),c['id']+' subject mismatch'
  ids,pol=policy(int(c['task_id'].split('-')[1]));assert c['requirement_ids']==ids
  assert c['policy']==pol,c['id']+' policy mismatch'
  assert 'sha256:'+sha((ROOT/c['evidence_path']).read_bytes())==c['evidence_sha256'],c['id']+' payload mismatch'
  assert c['result']=='pass';assert c['kind'] in ['automated','representative','high-risk']
  assert c.get('tool') or c.get('actor')
 assert manifest['manual_gaps']==[]
 print('PASS: subject, anchored policy, requirement bindings and immutable payload digests match all',len(manifest['checks']),'checks')
if __name__=='__main__':
 import yaml
 validate(yaml.safe_load((R/'evidence-manifest.yaml').read_text()))
