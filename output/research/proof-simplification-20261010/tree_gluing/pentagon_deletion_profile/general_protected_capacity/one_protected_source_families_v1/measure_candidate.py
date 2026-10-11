#!/usr/bin/env python3
"""Measure the full fixed-side candidate and keep original-source copies exact."""
from pathlib import Path
import hashlib,json,platform,re,shutil,subprocess
HERE=Path(__file__).resolve().parent
MAIN=Path('/Users/huahua815/Downloads/planar_recoloring/planar_recoloring_hamilton_thresholds.tex')
CONT=HERE.parents[3]/'continuation-10'
NAME='fixed-side-source-families-candidate-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run():
    assert platform.python_version()=='3.14.6'
    assert sha(MAIN)==sha(HERE/'frozen-current-main.tex')=='ecea0571029a8527630442b2242bc21ec76f67bc44b2f768b9228c5f494203a9'
    out={}
    for name in ('frozen-current-main',NAME):
        p=HERE/(name+'.pdf');info=subprocess.check_output(['pdfinfo',str(p)]).decode();txt=subprocess.check_output(['pdftotext',str(p),'-']).decode();src=(HERE/(name+'.tex')).read_text()
        out[name]=dict(pages=int(re.search(r'Pages:\s+(\d+)',info)[1]),pdf_sha256=sha(p),tex_sha256=sha(HERE/(name+'.tex')),pdf_ascii_letter_tokens=len(re.findall(r'[A-Za-z]+',txt)),pdf_whitespace_tokens=len(txt.split()),pdf_characters=len(txt),raw_tex_bytes=len(src.encode()),raw_tex_ascii_letter_tokens=len(re.findall(r'[A-Za-z]+',src)),raw_tex_whitespace_tokens=len(src.split()),source_selector_pages=[i+1 for i,page in enumerate(txt.split('\f')) if 'source selectors' in page],individual_header_pages=[i+1 for i,page in enumerate(txt.split('\f')) if 'remaining individual' in page])
        if name==NAME:
            log=(HERE/(name+'.log')).read_text();warnings=re.findall(r'(?:Overfull|Underfull|LaTeX Warning|Package \w+ Warning|undefined references)[^\n]*',log)
            assert warnings==[];out[name]['overfull_underfull_warning_matches']=warnings;(HERE/'candidate-text-v1.txt').write_text(txt)
    assert out['frozen-current-main']['pages']==42 and out[NAME]['pages']==42
    checks=json.loads((HERE/'removed236-individual-records.json').read_text())['selected_case_conditions']
    result=dict(status='PASS',python=platform.python_version(),documents=out,main_edited=False,finite_condition_counts=dict(case_directions={'F':139,'R':97},HC_side_full_incident_observations=sum(c['saved_certificate']['HC_side_degree'] for c in checks),safe_fixed_K_incident_observations=sum(c['saved_certificate']['safe_incident_count'] for c in checks),individual_endpoint_plus_selector_members_before=364,individual_endpoint_plus_selector_members_after=172),metric_definition='Literal pdfinfo counts, pdftotext ASCII[A-Za-z]+ tokens and Python whitespace split counts.',limitations=['Finite word payload is a proxy that omits degree, safe-K membership, pool exclusion and direction premises.','The new criterion keeps one protected template fixed; it does not preserve the stage9 arbitrary-both-HC counterfactual quantifier.','Original theorem statements and their specified-template state/endpoint quantifiers remain byte exact.','Independent actual236review is separate from author metrics; no main adoption is made.'])
    (HERE/'candidate-pdf-comparison-v1.json').write_text(json.dumps(result,indent=2)+'\n')
    target=CONT/'candidate-v1';shutil.copyfile(HERE/(NAME+'.pdf'),target/(NAME+'.pdf'));assert sha(target/(NAME+'.tex'))==sha(HERE/(NAME+'.tex'))
    print(json.dumps(result,indent=2))
if __name__=='__main__':run()
