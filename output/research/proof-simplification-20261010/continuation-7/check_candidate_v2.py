#!/usr/bin/env python3
"""Exact source preservation and frozen-proof readback; no graph search."""
from pathlib import Path
import hashlib, json, re, difflib, shutil, subprocess

WORK = Path(__file__).resolve().parent
ROOT = WORK.parents[3]
old_path = WORK / 'original/planar_recoloring_hamilton_thresholds.tex'
new_path = WORK / 'simplification-candidate-v2.tex'
old, new = old_path.read_text(), new_path.read_text()
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
def safe_proof(s):
    i = s.index('\\begin{proof}', s.index('\\begin{lemma}[Safe common edges]'))
    j = s.index('\\end{proof}', i) + len('\\end{proof}')
    return s[i:j]
def appendix(s):
    i = s.index('The fibres $B_t$, allowed colour images', s.index('\\label{app:path232-certificates}'))
    j = s.index('\\clearpage', i)
    return s[i:j]
verification = ('The $(2,3,2)$-path proof uses the three displayed cycles, twelve\n'
                'coordinate-class deletion profiles, and six counting bounds in\n'
                'Lemma~\\ref{lem:pathsafe}, replacing the common-edge witness table.\n\n')
assert new.count(verification) == 1
old_outside = old.replace(safe_proof(old), '<SAFE-PROOF>').replace(appendix(old), '<PATH-APPENDIX>')
new_outside = new.replace(safe_proof(new), '<SAFE-PROOF>').replace(appendix(new), '<PATH-APPENDIX>').replace(verification, '')
assert old_outside == new_outside
stmt = lambda s: re.findall(r'\\begin\{(theorem|lemma|proposition|corollary)\}(.*?)\\end\{\1\}', s, re.S)
assert stmt(old) == stmt(new)
old_labels = re.findall(r'\\label\{([^}]+)\}', old)
new_labels = re.findall(r'\\label\{([^}]+)\}', new)
assert new_labels == [x for x in old_labels if x != 'tab:path232-safe-edges']
assert len(new_labels) == len(set(new_labels))
assert set(re.findall(r'\\(?:ref|eqref|pageref)\{([^}]+)\}', new)) <= set(new_labels)
assert 'tab:path232-safe-edges' not in new
assert '\\tag{DP}' not in new and '\\tag{CT}' not in new
blocks = lambda s: {m.group(1):m.group(0) for m in re.finditer(r'^% BEGIN ([^\n]+)\n.*?^% END \1$', s, re.S|re.M)}
assert blocks(old) == blocks(new)
cycles = lambda s: re.search(r'\\begin\{equation\}\n\\label\{eq:path232-cycles\}.*?\\end\{equation\}',s,re.S).group(0)
assert cycles(old) == cycles(new)
proof = safe_proof(new)
assert 'In the respective cycles' in proof
assert 'respective selected cycles, not in the full fibre graphs' in appendix(new)
prior = json.loads((WORK.parent/'path232/deletion_profile/table-free-safe-proof-results-v1.json').read_text())
assert prior['verdict'] == 'PASS'
rows = re.findall(r'(aab|abc|aba)\\to (aac|acb|cab|abd|bab|cba)&(\d+)&(\d+)&(\d+)&(\d+)&(\d+)&(\d+)', proof)
expected = [(rec['family'][0], rec['family'][1], *map(str, rec['n_m_f_qcap_Rfloor_bound'])) for rec in prior['retention_families']]
assert rows == expected
compact = re.sub(r'\s+', '', proof + appendix(new))
for phrase in ('$w=c,v=c,u=c,u=b$inducerespectively$P_4,P_4,P_3\\cupP_2,2P_2$', '$v=a,u=b,w=d,u=c$inducerespectively$P_6,P_4\\cupP_3,P_3\\cupP_2,P_3\\cupP_1$', '$u=b,w=b,u=c,w=c$inducerespectively$P_3\\cup2P_2,P_5\\cupP_2,P_3\\cupP_2,P_4\\cupP_1$'):
    assert phrase in compact
for a,b,n,m,f,r,k,bound in rows:
    assert 2*int(n)-int(r)-int(m)-int(f)+int(k) == int(bound) >= 2
log = (WORK/'.latex-build/simplification-candidate-v2.log').read_text()
warnings = re.findall(r'^.*(?:Warning:|Overfull|Underfull|^!).*$', log,re.M)
assert not warnings, warnings
pages = lambda p: int(re.search(r'^Pages:\s*(\d+)',subprocess.check_output(['pdfinfo',str(p)],text=True),re.M).group(1))
def alpha_count(s):
    s = re.sub(r'(?m)%.*$', '', s)
    s = re.sub(r'\\[A-Za-z]+', ' ', s)
    return len(re.findall(r'\b[A-Za-z]+\b', s))
old_table_start = old.index('\\subsection{Safe common-edge witnesses}')
old_table_end = old.index('\\clearpage', old_table_start)
old_evidence = safe_proof(old) + old[old_table_start:old_table_end]
new_support = appendix(new).split('\\subsection{Selected-cycle identities}',1)[1]
new_evidence = safe_proof(new) + new_support
line = lambda s, needle: s[:s.index(needle)].count('\n')+1
result = {
    'verdict':'PASS',
    'main_unchanged_sha256':sha(ROOT/'planar_recoloring_hamilton_thresholds.tex'),
    'original_sha256':sha(old_path), 'candidate_sha256':sha(new_path),
    'original_pdf_sha256':sha(WORK/'original/planar_recoloring_hamilton_thresholds.pdf'),
    'candidate_pdf_sha256':sha(WORK/'simplification-candidate-v2.pdf'),
    'primary_statements_exact':len(stmt(new)), 'primary_statements_unchanged':True,
    'labels_before':len(old_labels), 'labels_after':len(new_labels),
    'deleted_auxiliary_label':'tab:path232-safe-edges', 'all_refs_resolve':True,
    'all_marked_literal_blocks_exact':len(blocks(new)),
    'DE_DM_DA_equation_byte_exact':True,
    'changes_confined_to_safe_proof_path_appendix_and_verification_sentence':True,
    'nine_families_all_allowed_cycles_preserved':True,
    'six_count_rows_exactly_inherit_frozen_proof':rows,
    'twelve_selected_cycle_profiles_inherit_frozen_proof':True,
    'compile':{'command':'latexmk -pdf -interaction=nonstopmode -halt-on-error simplification-candidate-v2.tex', 'exit_code':0, 'final_log_warnings_overfull_underfull':warnings},
    'page_counts':{'original':pages(WORK/'original/planar_recoloring_hamilton_thresholds.pdf'),'candidate':pages(WORK/'simplification-candidate-v2.pdf')},
    'length':{'metric':'ASCII alphabetic tokens after stripping TeX command names and comments; mathematical letters count; numerical triple words do not', 'old_proof_plus_old_conventions_orbits_table':alpha_count(old_evidence),'new_proof_plus_selected_cycle_appendix':alpha_count(new_evidence),'new_main_proof':alpha_count(safe_proof(new)),'new_supporting_appendix':alpha_count(new_support),'old_safe_proof_bytes':len(old_evidence.encode()),'new_proof_and_support_bytes':len(new_evidence.encode()),'new_main_proof_bytes':len(safe_proof(new).encode()),'new_supporting_appendix_bytes':len(new_support.encode()),'original_source_bytes':old_path.stat().st_size,'candidate_source_bytes':new_path.stat().st_size},
    'line_locations':{'safe_lemma':line(new,'\\begin{lemma}[Safe common edges]'),'safe_proof':line(new,'We first record a cycle-deletion count.'),'verification_update':line(new,verification),'unchanged_cycle_equation':line(new,'\\label{eq:path232-cycles}'),'selected_cycle_identities':line(new,'\\subsection{Selected-cycle identities}')},
    'evidence_boundary':'Exact source comparison and inherited fixed-cycle identities; analytic count reviewed separately. Compilation is not proof or formal verification. No graph or Hamilton-cycle search.'
}
assert result['main_unchanged_sha256'] == result['original_sha256'] == '7a90f79db489447b0bad3019217fd369a5cc25986288247981cbe7f3462acba3'
(WORK/'candidate-review-v2.json').write_text(json.dumps(result,indent=2)+'\n')
(WORK/'candidate-v2.diff').write_text(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='phase6-original.tex',tofile='continuation7-candidate-v2.tex')))
shutil.copy2(WORK/'.latex-build/simplification-candidate-v2.log',WORK/'latex-build-v2.log')
print(json.dumps(result,indent=2))
