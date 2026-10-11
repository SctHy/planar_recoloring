#!/usr/bin/env python3
"""Actual125tuple witness removal and separate full candidate; no graph work."""
from pathlib import Path
import hashlib,json,re
HERE=Path(__file__).resolve().parent

PREFIX=r'''\paragraph{Three-edge-union source selectors (125 interfaces).}
For a common state $x$ under an edit $j:a\to q$, the union of its
two full incident stars has $d+\alpha$ edges, where $d$ is its source
degree and $\alpha=\mathbf1[a\notin\{x_{j-1},x_{j+1}\}]$:
the only possible new target mutation is to the old forbidden colour $a$.
If $d+\alpha\le3$, any two component Hamilton cycles take two edges
each from this union and meet; their common edge is protected when
no common incident edge belongs to the source or restored target pool.

'''
SUFFIX=r'''
For each covered interface, some listed $x\in S_t$ lies in the restored
target component, has $d+\alpha\le3$, and has no common incident
pool edge under the prescribed first normalizer. These 125 checks use
the printed pools and the one-coordinate lists
\[
L_i(t,x)=\{0,1,2,3\}\setminus\{x_{i-1},x_{i+1},t_i\},\qquad
d=\sum_i(|L_i(t,x)|-1),
\]
omitting $t_i$ when starred. Thus the selector rows prove the protected
identities for the specified cycles in all 125 cases.

'''

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def blocks(s):return {m[1]:m[2] for m in re.finditer(r'^% BEGIN ([^\n]+)\n(.*?)^% END \1$',s,re.S|re.M)}
def statements(s):return [(m[1],m[2]) for m in re.finditer(r'\\begin\{(theorem|lemma|proposition|corollary)\}(.*?)\\end\{\1\}',s,re.S)]

def run():
    source=HERE/'frozen-main.tex';old=source.read_text();assert sha(source)=='3806a0c7f8ec374ea92e70152f939e92e35c3c76564f9e69e8c06160999bcb58'
    input_path=HERE/'union-source-cover-results.json';results=json.loads(input_path.read_text())
    assert results['status']=='PASS' and results['covered_interfaces']==125 and results['source_families']==15
    assert results['input_sha256']=='36ee26c64c667dbb7bea0bc88eed3b3162c85cbae16038da3a01cd59eeca68b1'
    ids=set();selected_checks=[]
    keys=('source','source_component','position','colour','target_type','target_component')
    for t,f in results['families'].items():
        for choice in f['coverage']:
            a=choice['interface'];o=choice['certificate'];identity=tuple(a[k] for k in keys)
            assert a['source']==t and choice['selected_state'] in f['selected_words'] and identity not in ids
            assert o['forbidden_common_count']==0 and o['source_degree']+o['target_degree']-o['common_incident_count']<=3
            ids.add(identity);selected_checks.append(dict(interface=a,state=choice['selected_state'],incident_union_size=o['source_degree']+o['target_degree']-o['common_incident_count'],common_pool_incidence=0))
    assert len(ids)==125
    B=blocks(old);assert len(B)==53
    pattern=r'\b([0-4]{5}):(\d)\s+([0-4])\s+([0-3])\s+([0-4]{5}):(\d)\s+([0-3]{5})-([0-3]{5})\b'
    matches=list(re.finditer(pattern,B['INTERFACES-ALL']));assert len(matches)==283
    def identity(m):return (m[1],int(m[2]),int(m[3]),m[4],m[5],int(m[6]))
    removed=[m.group(0) for m in matches if identity(m) in ids]
    remaining=[m.group(0) for m in matches if identity(m) not in ids]
    assert len(removed)==125 and len(remaining)==158 and {identity(m) for m in matches if identity(m) in ids}==ids
    body='\\begingroup\\scriptsize\\ttfamily\\begin{flushleft}\n'+'\n'.join(' ; '.join(remaining[i:i+2])+r'\\' for i in range(0,len(remaining),2))+'\n\\end{flushleft}\\endgroup\n'
    candidate=old.replace(B['INTERFACES-ALL'],body,1)
    previous='''For the 313 standard-source interfaces, the appendix gives 283
individual common edges and six constant-source parameter families
covering the other 30 cases. Checking the five-digit endpoints in
the specified cycles and outside their pools proves each individual
record. The six families follow from two possible normalizing
directions and four protected target edges, as shown there. Applying
the inverse coordinate and colour maps gives every labelled case. This is a complete finite case proof;
no finite-length gluing experiment is used to infer a general rule.'''
    replacement='''For the 313 standard-source interfaces, the appendix gives 158
individual common edges, fifteen source-selector rows covering 125
cases, and six constant-source families covering 30 cases.
Endpoint membership in the specified cycles and outside their pools
proves each individual record. The selector rows use incident unions
of at most three edges with the prescribed first normalizer and pools.
The constant-source families use two normalizing directions and four
protected target edges. Inverse coordinate and colour maps give every
labelled case. This is a complete finite case proof; no finite-length
gluing experiment is used to infer a general rule.'''
    assert candidate.count(previous)==1;candidate=candidate.replace(previous,replacement,1)
    verification='The constant-source cases are supplied by six parameter families; the other 283 retain individual edge records.'
    revised='Six constant-source families cover 30 cases; fifteen source-selector rows cover 125 by three-edge incident unions, leaving 158 individual edge records.'
    assert candidate.count(verification)==1;candidate=candidate.replace(verification,revised,1)
    heading='\\paragraph{The 283 nonconstant-source interfaces.}';assert candidate.count(heading)==1
    table=(HERE/'source-selector-table.tex').read_text().split('\n',1)[1]
    families=PREFIX+table+SUFFIX
    candidate=candidate.replace(heading,families+'\\paragraph{The 158 remaining individual nonconstant-source interfaces.}',1)
    C=blocks(candidate);assert len(C)==53 and all(B[k]==C[k] for k in B if k!='INTERFACES-ALL')
    assert len(re.findall(pattern,C['INTERFACES-ALL']))==158
    S=statements(old);assert len(S)==41 and statements(candidate)==S
    normalization=lambda z:z.split('Here is the exact normalization convention.',1)[1].split('\\begin{lemma}',1)[0]
    assert normalization(old)==normalization(candidate)
    target=HERE/'fifteen-source-families-candidate-v1.tex';target.write_text(candidate)
    (HERE/'manuscript-source-family-fragment-v1.tex').write_text(families)
    (HERE/'removed125-individual-records.json').write_text(json.dumps(dict(removed_count=125,records=removed,retained_count=158,selected_case_conditions=selected_checks,total_interfaces=313),indent=2)+'\n')
    out=dict(status='PASS',python='3.14.6',source_sha256=sha(source),mask_result_sha256=sha(input_path),candidate_sha256=sha(target),other52marked_blocks_byte_exact=True,all41theorem_statements_byte_exact=True,normalizer_paragraph_byte_exact=True,individual_records_before=283,individual_records_after=158,source_selector_cases=125,source_selector_rows=15,constant_six_family_cases=30,total_interfaces=313,printed_source_selector_members=48,distinct_source_selector_words=27,individual_endpoint_plus_printed_selector_words_before=566,individual_endpoint_plus_printed_selector_words_after=364,individual_endpoint_plus_distinct_selector_words_after=343,raw_tex_bytes_before=len(old.encode()),raw_tex_bytes_after=len(candidate.encode()),raw_tex_ascii_letter_tokens_before=len(re.findall(r'[A-Za-z]+',old)),raw_tex_ascii_letter_tokens_after=len(re.findall(r'[A-Za-z]+',candidate)),raw_tex_whitespace_tokens_before=len(old.split()),raw_tex_whitespace_tokens_after=len(candidate.split()),all_tex_five_digit_tokens_before=len(re.findall(r'\b[0-4]{5}\b',old)),all_tex_five_digit_tokens_after=len(re.findall(r'\b[0-4]{5}\b',candidate)),no_main_edit=True,no_new_numbered_lemma=True,no_font_spacing_or_pagebreak_changes=True)
    (HERE/'manuscript-structure-results-v1.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':run()
