#!/usr/bin/env python3
"""Actual PDF/page/text/log comparison of the separated125-selector candidate."""
from pathlib import Path
import hashlib,json,re,subprocess
HERE=Path(__file__).resolve().parent
def run():
    out={}
    for name in ('frozen-main','fifteen-source-families-candidate-v1'):
        p=HERE/(name+'.pdf');info=subprocess.check_output(['pdfinfo',str(p)]).decode();txt=subprocess.check_output(['pdftotext',str(p),'-']).decode()
        out[name]=dict(pages=int(re.search(r'Pages:\s+(\d+)',info)[1]),pdf_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),pdf_ascii_letter_tokens=len(re.findall(r'[A-Za-z]+',txt)),pdf_whitespace_tokens=len(txt.split()),pdf_characters=len(txt),source_selector_pages=[i+1 for i,page in enumerate(txt.split('\f')) if 'Three-edge-union source selectors' in page],individual_header_pages=[i+1 for i,page in enumerate(txt.split('\f')) if '158 remaining individual' in page])
        if name!='frozen-main':
            log=(HERE/(name+'.log')).read_text();warnings=re.findall(r'(?:Overfull|Underfull|LaTeX Warning|Package \w+ Warning|undefined references)[^\n]*',log)
            assert warnings==[];out[name]['overfull_underfull_warning_matches']=warnings
            (HERE/'manuscript-text-v1.txt').write_text(txt)
    assert out['frozen-main']['pages']==out['fifteen-source-families-candidate-v1']['pages']==42
    result=dict(status='PASS',documents=out,main_edited=False,metric_definition='Literalpdfinfo page counts and ASCII[A-Za-z]+letter tokens / Python whitespace split counts frompdftotext.',limitations=['Page/prose counts do not prove mathematical correctness.','Adoption depends on separate independent actual-source review.'])
    (HERE/'manuscript-pdf-comparison-v1.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':run()
