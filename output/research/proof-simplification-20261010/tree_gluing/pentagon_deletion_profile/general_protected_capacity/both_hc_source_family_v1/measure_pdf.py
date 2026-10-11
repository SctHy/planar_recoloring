#!/usr/bin/env python3
"""Reproducible literal PDF/page/prose comparison; no mathematical rerun."""
from pathlib import Path
import hashlib,json,re,subprocess
HERE=Path(__file__).resolve().parent

def run():
    documents={}
    for name in ('frozen-main','two-source-families-candidate-v1','two-source-families-candidate-v2','two-source-families-candidate-v3'):
        p=HERE/(name+'.pdf');info=subprocess.check_output(['pdfinfo',str(p)]).decode();text=subprocess.check_output(['pdftotext',str(p),'-']).decode()
        item=dict(pages=int(re.search(r'Pages:\s+(\d+)',info)[1]),pdf_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),pdf_ascii_letter_tokens=len(re.findall(r'[A-Za-z]+',text)),pdf_whitespace_tokens=len(text.split()),pdf_characters=len(text),source_family_pages=[i+1 for i,page in enumerate(text.split('\f')) if 'Two source families' in page or 'Two ordinary-source families' in page])
        if name!='frozen-main':
            log=(HERE/(name+'.log')).read_text()
            item['overfull_underfull_warning_matches']=re.findall(r'(?:Overfull|Underfull|LaTeX Warning|Package \w+ Warning|undefined references)[^\n]*',log)
            assert item['overfull_underfull_warning_matches']==[]
        documents[name]=item
        if name.endswith('v3'):(HERE/'candidate-text-v3.txt').write_text(text)
    assert [documents[k]['pages'] for k in documents]==[42,44,43,43]
    out=dict(status='PASS',documents=documents,main_adopted=False,metric_definition='ASCII letter tokens are maximal[A-Za-z]+matches inpdftotext output; whitespace tokens use Python split. Page counts are frompdfinfo.',limits='Literal prose counts and page counts do not measure mathematical premise strength. All candidates are separate; the live main remains42pages.')
    (HERE/'candidate-pdf-comparison-final.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':run()
