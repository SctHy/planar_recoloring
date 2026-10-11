#!/usr/bin/env python3
"""Read literal page/text metrics from the final separated manuscript PDFs."""
from pathlib import Path
import hashlib,json,platform,re,subprocess
HERE=Path(__file__).resolve().parent
MAIN=Path('/Users/huahua815/Downloads/planar_recoloring/planar_recoloring_hamilton_thresholds.tex')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run():
    assert platform.python_version()=='3.14.6'
    baseline=sha(HERE/'frozen-main.tex');assert sha(MAIN)==baseline=='3806a0c7f8ec374ea92e70152f939e92e35c3c76564f9e69e8c06160999bcb58'
    out={}
    for name in ('frozen-main','fifteen-source-families-candidate-v1','fifteen-source-families-candidate-v2'):
        p=HERE/(name+'.pdf');info=subprocess.check_output(['pdfinfo',str(p)]).decode();txt=subprocess.check_output(['pdftotext',str(p),'-']).decode();src=(HERE/(name+'.tex')).read_text()
        out[name]=dict(pages=int(re.search(r'Pages:\s+(\d+)',info)[1]),pdf_sha256=sha(p),tex_sha256=sha(HERE/(name+'.tex')),pdf_ascii_letter_tokens=len(re.findall(r'[A-Za-z]+',txt)),pdf_whitespace_tokens=len(txt.split()),pdf_characters=len(txt),raw_tex_bytes=len(src.encode()),raw_tex_ascii_letter_tokens=len(re.findall(r'[A-Za-z]+',src)),raw_tex_whitespace_tokens=len(src.split()),source_selector_pages=[i+1 for i,page in enumerate(txt.split('\f')) if 'Three-edge-union source selectors' in page],individual_header_pages=[i+1 for i,page in enumerate(txt.split('\f')) if '158 remaining individual' in page])
        if name!='frozen-main':
            log=(HERE/(name+'.log')).read_text();warnings=re.findall(r'(?:Overfull|Underfull|LaTeX Warning|Package \w+ Warning|undefined references)[^\n]*',log)
            assert warnings==[];out[name]['overfull_underfull_warning_matches']=warnings
            if name.endswith('v2'):(HERE/'manuscript-text-v2.txt').write_text(txt)
    assert all(d['pages']==42 for d in out.values())
    result=dict(status='PASS',python=platform.python_version(),documents=out,main_edited=False,metric_definition='Literal pdfinfo page counts, ASCII [A-Za-z]+ letter tokens, and Python whitespace split counts from pdftotext.',limitations=['Page/prose counts do not prove mathematical correctness.','Forty-eight row members are a sum of per-row exact minima; twenty-seven distinct words are not claimed jointly minimal.','Adoption depends on separate independent actual-source review.'])
    (HERE/'manuscript-pdf-comparison-v2.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':run()
