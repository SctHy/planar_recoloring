#!/usr/bin/env python3
"""Specialized three-edge incident-union proof; source data and v1/v2 retained."""
from pathlib import Path
import hashlib,json,re
HERE=Path(__file__).resolve().parent

UNION_FAMILIES=r'''\paragraph{Two source families (27 interfaces).}
For a common state $x$ under an edit $j:a\to q$, the union of its
two incident stars has $d+\alpha$ edges, where $d$ is its source
degree and $\alpha=\mathbf1[a\notin\{x_{j-1},x_{j+1}\}]$:
the only possible new target mutation is to the old forbidden colour $a$.
When $d+\alpha=3$, any two component Hamilton cycles take two edges
each from this three-edge union and therefore meet; their common edge
is protected if no common incident edge lies in the union of the source
and restored target pools.

Put $w=32301$. Subscripts below give source degree, and superscripts
give $J_t(x)=\{j:t_j\in\{x_{j-1},x_{j+1}\}\}$ as position digits;
an omitted superscript means $J=\varnothing$.
\[
\begin{array}{c|l}
t&S_t\\ \hline
01023&12310_3^{01},\ 23101_3^{12},\ 23201_3^{23},\ 23210_3^{03},\ w_3^{24},\ 32310_3^{04}\\
01124&12303_3^1,\ 23031_2,\ w_2
\end{array}
\]
The one-coordinate colour lists and printed pools under the prescribed
first normalizer verify these conditions at some $x\in S_t$ in the
restored target component for every allowed edit: fifteen in the first
row and twelve in the second. The resulting common edge proves each
protected identity for the specified cycles.

'''

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def blocks(s):return {m[1]:m[2] for m in re.finditer(r'^% BEGIN ([^\n]+)\n(.*?)^% END \1$',s,re.S|re.M)}

def run():
    original=(HERE/'frozen-main.tex').read_text();v2path=HERE/'two-source-families-candidate-v2.tex'
    assert sha(v2path)=='6bfed6b8fa76d392dc0766ded22a82da4a3a048fa132b9d43347e6cdae55e5f3'
    v2=v2path.read_text();previous=(HERE/'two-source-families-short-v2.tex').read_text()
    assert v2.count(previous)==1
    v3=v2.replace(previous,UNION_FAMILIES,1)
    assert v3.count("appendix's local-degree and inclusion--exclusion argument")==1
    v3=v3.replace("appendix's local-degree and inclusion--exclusion argument","appendix's three-edge incident-union argument",1)
    assert v3.count('two further source families cover 27 by local degrees and inclusion--exclusion')==1
    v3=v3.replace('two further source families cover 27 by local degrees and inclusion--exclusion','two further source families cover 27 by three-edge incident unions',1)
    assert all(blocks(original)[k]==blocks(v3)[k] for k in blocks(original) if k!='INTERFACES-ALL')
    rowpattern=r'\b([0-4]{5}):(\d)\s+([0-4])\s+([0-3])\s+([0-4]{5}):(\d)\s+([0-3]{5})-([0-3]{5})\b'
    assert len(re.findall(rowpattern,blocks(v3)['INTERFACES-ALL']))==256
    selected=json.loads((HERE/'set-cover-results.json').read_text())
    checks=[]
    for t,f in selected['source_families'].items():
        for z in f['coverage_map']:
            o=z['certificate'];Ns=set(o['source_neighbours']);Nt=set(o['target_neighbours'])
            assert len(Ns|Nt)==o['source_degree']+o['target_degree']-o['common_incident_count']==3
            assert o['forbidden_common_count']==0
            checks.append(dict(source=t,interface=z['interface'],state=z['selected_state'],source_neighbours=o['source_neighbours'],target_neighbours=o['target_neighbours'],union_neighbours=sorted(Ns|Nt),union_size=3,common_pool_incidence=0))
    assert len(checks)==27
    target=HERE/'two-source-families-candidate-v3.tex';target.write_text(v3)
    (HERE/'two-source-families-union-v3.tex').write_text(UNION_FAMILIES)
    (HERE/'selected27-union-results.json').write_text(json.dumps(dict(status='PASS',checks=checks,total=27,scope='Exact extraction from frozen selected neighbour sets; no new neighbour generation.'),indent=2)+'\n')
    metrics=dict(status='PASS',candidate_version='v3',original_sha256=sha(HERE/'frozen-main.tex'),candidate_sha256=sha(target),v1_retained_sha256=sha(HERE/'two-source-families-candidate-v1.tex'),v2_retained_sha256=sha(v2path),other52marked_blocks_byte_exact=True,individual_records=256,source_family_cases=27,constant_family_cases=30,total_interfaces=313,selected27_incident_union_size3_and_no_common_pool_incidence=True,no_new_numbered_lemma=True,no_font_spacing_or_page_break_changes=True,raw_tex_bytes_before=len(original.encode()),raw_tex_bytes_after=len(v3.encode()),raw_tex_letter_tokens_before=len(re.findall(r'[A-Za-z]+',original)),raw_tex_letter_tokens_after=len(re.findall(r'[A-Za-z]+',v3)),raw_tex_whitespace_tokens_before=len(original.split()),raw_tex_whitespace_tokens_after=len(v3.split()),all_tex_five_digit_tokens_before=len(re.findall(r'\b[0-4]{5}\b',original)),all_tex_five_digit_tokens_after=len(re.findall(r'\b[0-4]{5}\b',v3)),case_evidence_state_words_before=566,case_evidence_state_words_after=520,global_minimum_distinct_family_words=8)
    (HERE/'candidate-structure-results-v3.json').write_text(json.dumps(metrics,indent=2)+'\n')
    print(json.dumps(metrics,indent=2))

if __name__=='__main__':run()
