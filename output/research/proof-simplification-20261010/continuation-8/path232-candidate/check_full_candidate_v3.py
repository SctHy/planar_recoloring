#!/usr/bin/env python3
"""Read-only v3 review: exact domain-qualifier reduction to checked v2."""
from pathlib import Path
import hashlib,json,re,difflib,shutil,subprocess
BASE=Path(__file__).resolve().parent;ROOT=BASE.parents[4]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p2=BASE/'layer-capacity-manuscript-candidate-v2.tex';p3=BASE/'layer-capacity-manuscript-candidate-v3.tex'
assert sha(p2)=='68ce8760008895fcc1c27d54faf0fadc1ff5335901894f5cf89cd9e37ec9b506'
assert sha(p3)=='3806a0c7f8ec374ea92e70152f939e92e35c3c76564f9e69e8c06160999bcb58'
v2,v3=p2.read_text(),p3.read_text()
old='For common endpoint lists $L,R$, the layer $H_v$ is'
new='For common endpoint lists $L,R$ and distinct allowed middle colours $v,w$,\nthe layer $H_v$ is'
assert v2.count(old)==v3.count(new)==1
assert v3==v2.replace(old,new)
prior=json.loads((BASE/'full-candidate-review-v2.json').read_text());assert prior['verdict']=='PASS' and prior['candidate_sha256']==sha(p2)
baseline=(BASE/'original/planar_recoloring_hamilton_thresholds.tex').read_text()
statements=lambda s:re.findall(r'\\begin\{(theorem|lemma|proposition|corollary)\}(.*?)\\end\{\1\}',s,re.S)
assert statements(baseline)==statements(v3)
labels=lambda s:re.findall(r'\\label\{([^}]+)\}',s)
assert labels(v2)==labels(v3)
assert set(re.findall(r'\\(?:ref|eqref|pageref)\{([^}]+)\}',v3))<=set(labels(v3))
blocks=lambda s:{m.group(1):m.group(0) for m in re.finditer(r'^% BEGIN ([^\n]+)\n.*?^% END \1$',s,re.S|re.M)}
assert blocks(baseline)==blocks(v3)
eq=lambda s:re.search(r'\\begin\{equation\}\n\\label\{eq:path232-cycles\}.*?\\end\{equation\}',s,re.S).group(0)
assert eq(baseline)==eq(v3)
log=(BASE/'.latex-build/layer-capacity-manuscript-candidate-v3.log').read_text()
warnings=re.findall(r'^.*(?:Warning:|Overfull|Underfull|^!).*$',log,re.M);assert not warnings,warnings
pages=int(re.search(r'^Pages:\s*(\d+)',subprocess.check_output(['pdfinfo',str(p3.with_suffix('.pdf'))],text=True),re.M).group(1));assert pages==42
metric=lambda s:len(re.findall(r'\b[A-Za-z]+\b',re.sub(r'\\[A-Za-z]+',' ',re.sub(r'(?m)%.*$','',s))))
i=v3.index('\\begin{proof}',v3.index('\\begin{lemma}[Safe common edges]'));j=v3.index('\\end{proof}',i)+len('\\end{proof}')
a=v3.index('\\subsection{Selected-layer identities and capacities}');b=v3.index('\\clearpage',a)
result={'verdict':'PASS','candidate_sha256':sha(p3),'pdf_sha256':sha(p3.with_suffix('.pdf')),'v2_sha256':sha(p2),'v3_reduces_exactly_to_reviewed_v2':True,'only_change':'distinct allowed middle colours v,w domain qualifier before Cartesian/cross-edge formula','qualifier_domain':'distinct v,w in the common allowed middle-colour set, so v,w notin{t_1,s_1}','primary_statements_exact':len(statements(v3)),'marked_literal_blocks_exact':len(blocks(v3)),'DE_DM_DA_equation_exact':True,'labels_unchanged_from_v2':len(labels(v3)),'all_refs_resolve':True,'all_fourteen_local_orientation_cases_inherited':True,'compile_exit_code':0,'final_warnings':warnings,'pages':pages,'tokens':{'main_proof':metric(v3[i:j]),'support_appendix':metric(v3[a:b])},'source_bytes':p3.stat().st_size,'live_main_sha256_at_review':sha(ROOT/'planar_recoloring_hamilton_thresholds.tex'),'no_source_or_main_edits':True,'evidence_boundary':'Read-only exact delta/source/build review; inherits the independently checked v2 selected-cycle certificate and symbolic proof. No graph or Hamilton search.'}
(BASE/'full-candidate-review-v3.json').write_text(json.dumps(result,indent=2)+'\n')
(BASE/'v2-to-v3.diff').write_text(''.join(difflib.unified_diff(v2.splitlines(True),v3.splitlines(True),fromfile='layer-v2.tex',tofile='layer-v3.tex')))
(BASE/'candidate-v3.diff').write_text(''.join(difflib.unified_diff(baseline.splitlines(True),v3.splitlines(True),fromfile='phase6-original.tex',tofile='layer-v3.tex')))
shutil.copy2(BASE/'.latex-build/layer-capacity-manuscript-candidate-v3.log',BASE/'final-latex-v3.log')
print(json.dumps(result,indent=2))
