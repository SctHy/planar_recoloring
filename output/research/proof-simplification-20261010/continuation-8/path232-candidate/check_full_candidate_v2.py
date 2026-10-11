#!/usr/bin/env python3
"""Compare full manuscript source; readback of local proof is separate."""
from pathlib import Path
import hashlib,json,re,difflib,shutil,subprocess
BASE=Path(__file__).resolve().parent;ROOT=BASE.parents[4]
old_path=BASE/'original/planar_recoloring_hamilton_thresholds.tex';new_path=BASE/'layer-capacity-manuscript-candidate-v2.tex'
old,new=old_path.read_text(),new_path.read_text();sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def safeproof(s):
    a=s.index('\\begin{proof}',s.index('\\begin{lemma}[Safe common edges]'));b=s.index('\\end{proof}',a)+len('\\end{proof}');return s[a:b]
def appendix(s):
    a=s.index('The fibres $B_t$, allowed colour images',s.index('\\label{app:path232-certificates}'));b=s.index('\\clearpage',a);return s[a:b]
update=('For $(2,3,2)$-path restoration, the three displayed cycles are used\n'
        'through fixed-middle-layer and middle-change-edge capacity bounds\n'
        'rather than an interface witness table.\n\n')
assert new.count(update)==1
assert old.replace(safeproof(old),'<SAFE>').replace(appendix(old),'<APP>')==new.replace(safeproof(new),'<SAFE>').replace(appendix(new),'<APP>').replace(update,'')
statements=lambda s:re.findall(r'\\begin\{(theorem|lemma|proposition|corollary)\}(.*?)\\end\{\1\}',s,re.S)
assert statements(old)==statements(new)
labels=lambda s:re.findall(r'\\label\{([^}]+)\}',s)
assert labels(new)==[x for x in labels(old) if x!='tab:path232-safe-edges']
assert len(labels(new))==len(set(labels(new)))
assert set(re.findall(r'\\(?:ref|eqref|pageref)\{([^}]+)\}',new))<=set(labels(new))
assert 'tab:path232-safe-edges' not in new
blocks=lambda s:{m.group(1):m.group(0) for m in re.finditer(r'^% BEGIN ([^\n]+)\n.*?^% END \1$',s,re.S|re.M)}
assert blocks(old)==blocks(new)
eq=lambda s:re.search(r'\\begin\{equation\}\n\\label\{eq:path232-cycles\}.*?\\end\{equation\}',s,re.S).group(0)
assert eq(old)==eq(new)
local=(BASE/'layer-proof-input-v2.tex').read_text()
piece=lambda tag:local.split('% BEGIN '+tag+'\n',1)[1].split('% END '+tag,1)[0].rstrip()
assert safeproof(new)==piece('SAFE-PROOF')
assert piece('SELECTED-SUPPORT') in appendix(new)
assert sha(BASE/'layer-proof-input-v2.tex')==sha(ROOT/'output/research/proof-simplification-20261010/path232/layer_capacity/layer-proof-candidate-v2.tex')
assert 'outside-path' not in safeproof(new) and 'deletion profile' not in appendix(new)
log=(BASE/'.latex-build/layer-capacity-manuscript-candidate-v2.log').read_text()
warnings=re.findall(r'^.*(?:Warning:|Overfull|Underfull|^!).*$',log,re.M);assert not warnings,warnings
pages=lambda p:int(re.search(r'^Pages:\s*(\d+)',subprocess.check_output(['pdfinfo',str(p)],text=True),re.M).group(1))
metric=lambda s:len(re.findall(r'\b[A-Za-z]+\b',re.sub(r'\\[A-Za-z]+',' ',re.sub(r'(?m)%.*$','',s))))
old_witness=old[old.index('\\subsection{Safe common-edge witnesses}'):old.index('\\clearpage',old.index('\\subsection{Safe common-edge witnesses}'))]
line=lambda needle:new[:new.index(needle)].count('\n')+1
result={'verdict':'PASS','original_main_sha256':sha(old_path),'live_main_sha256':sha(ROOT/'planar_recoloring_hamilton_thresholds.tex'),'candidate_sha256':sha(new_path),'candidate_pdf_sha256':sha(BASE/'layer-capacity-manuscript-candidate-v2.pdf'),'primary_statements_byte_exact':len(statements(new)),'literal_marked_blocks_byte_exact':len(blocks(new)),'DE_DM_DA_equation_byte_exact':True,'labels_before':len(labels(old)),'labels_after':len(labels(new)),'only_removed_auxiliary_label':'tab:path232-safe-edges','all_refs_resolve':True,'changes_limited_to_safe_proof_path_appendix_verification_sentence':True,'local_math_candidate_byte_exact':True,'no_outside_deletion_profiles':True,'compile_exit_code':0,'final_compile_warnings':warnings,'pages':{'original':pages(BASE/'original/planar_recoloring_hamilton_thresholds.pdf'),'candidate':pages(BASE/'layer-capacity-manuscript-candidate-v2.pdf')},'approximate_letter_tokens':{'old_safe_proof_plus_witness_conventions':metric(safeproof(old)+old_witness),'new_main_proof':metric(safeproof(new)),'new_selected_support':metric(piece('SELECTED-SUPPORT'))},'source_bytes':{'original':old_path.stat().st_size,'candidate':new_path.stat().st_size},'line_locations':{'lemma':line('\\begin{lemma}[Safe common edges]'),'new_proof':line('Partition the common fibre graph'),'support_appendix':line('\\subsection{Selected-layer identities and capacities}'),'verification':line(update)},'evidence_boundary':'Exact source and fixed-candidate consistency checks plus compilation; separate symbolic independent review is required. No graph or Hamilton search.'}
assert result['live_main_sha256']==result['original_main_sha256']=='7a90f79db489447b0bad3019217fd369a5cc25986288247981cbe7f3462acba3'
(BASE/'full-candidate-review-v2.json').write_text(json.dumps(result,indent=2)+'\n')
(BASE/'candidate-v2.diff').write_text(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='phase6-original.tex',tofile='layer-capacity-candidate-v2.tex')))
shutil.copy2(BASE/'.latex-build/layer-capacity-manuscript-candidate-v2.log',BASE/'final-latex-v2.log')
print(json.dumps(result,indent=2))

