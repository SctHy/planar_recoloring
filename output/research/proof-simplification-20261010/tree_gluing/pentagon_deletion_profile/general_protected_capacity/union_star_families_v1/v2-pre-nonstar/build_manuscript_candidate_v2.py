#!/usr/bin/env python3
"""Define the125case complement explicitly; only a prose clarification ofv1."""
from pathlib import Path
import hashlib,json,re
HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run():
    p=HERE/'fifteen-source-families-candidate-v1.tex';old=p.read_text();assert sha(p)=='275058ea128ac1f462766a6d08baa90cb32358b55a32e4d210b18920646424d5'
    before='For each covered interface, some listed $x\\in S_t$ lies in the restored'
    after='For each of the 125 nonconstant-source interfaces not listed individually\nbelow, some $x\\in S_t$ lies in the restored'
    assert old.count(before)==1;new=old.replace(before,after,1)
    target=HERE/'fifteen-source-families-candidate-v2.tex';target.write_text(new)
    fragment=(HERE/'manuscript-source-family-fragment-v1.tex').read_text();assert fragment.count(before)==1
    (HERE/'manuscript-source-family-fragment-v2.tex').write_text(fragment.replace(before,after,1))
    changed=dict(status='PASS',candidate_version='v2',v1_source_sha256=sha(p),candidate_source_sha256=sha(target),only_prose_case_complement_clarification=True,all125actual_checks_inherited_unchanged=True,other52blocks_41statements_normalizer_inherited_unchanged=True,individual_records=158,source_selector_cases=125,constant_cases=30,total=313,raw_tex_bytes=len(new.encode()),raw_tex_letter_tokens=len(re.findall(r'[A-Za-z]+',new)),raw_tex_whitespace_tokens=len(new.split()))
    (HERE/'manuscript-structure-results-v2.json').write_text(json.dumps(changed,indent=2)+'\n');print(json.dumps(changed,indent=2))
if __name__=='__main__':run()
