#!/usr/bin/env python3
"""Build a separated fixed-side candidate from frozen masks and original tuples."""
from pathlib import Path
import hashlib,json,platform,re,shutil
HERE=Path(__file__).resolve().parent
RESEARCH=HERE.parents[3]
CONT=RESEARCH/'continuation-10'
NAME='fixed-side-source-families-candidate-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def blocks(s):return {m[1]:m[2] for m in re.finditer(r'^% BEGIN ([^\n]+)\n(.*?)^% END \1$',s,re.S|re.M)}
def statements(s):return [(m[1],m[2]) for m in re.finditer(r'\\begin\{(theorem|lemma|proposition|corollary)\}(.*?)\\end\{\1\}',s,re.S)]
PATTERN=r'\b([0-4]{5}):(\d)\s+([0-4])\s+([0-3])\s+([0-4]{5}):(\d)\s+([0-3]{5})-([0-3]{5})\b'
KEYS=('source','source_component','position','colour','target_type','target_component')
def identity(a):return tuple(a[k] for k in KEYS)
def row_identity(m):return (m[1],int(m[2]),int(m[3]),m[4],m[5],int(m[6]))
SUFFIX=r'''
For each of the 236 nonconstant-source interfaces not listed individually
below, some $x\in S_t$ belongs to both the source and restored target
components and satisfies $d-g\le1$ in one direction: fixed source $K$
against the target component, or fixed restored target $K$ against the
source component. The opposite component has its displayed Hamilton cycle.
These 236 checks use the printed protected sets and pools under the
original interface's prescribed first normalizer. For the boundary $b$
of the Hamilton-cycle side in the original coordinates, its degree is
\[
L_i(b,x)=\{0,1,2,3\}\setminus\{x_{i-1},x_{i+1},b_i\},\qquad
d=\sum_i(|L_i(b,x)|-1),
\]
omitting $b_i$ when starred. Thus the selector rows prove the protected
identities for the specified templates in all 236 cases.

'''
def run():
    assert platform.python_version()=='3.14.6'
    current=HERE/'frozen-current-main.tex';original=HERE/'frozen-283-source.tex';resultpath=HERE/'frozen-selector-results.json'
    assert sha(current)=='ecea0571029a8527630442b2242bc21ec76f67bc44b2f768b9228c5f494203a9'
    assert sha(original)=='3806a0c7f8ec374ea92e70152f939e92e35c3c76564f9e69e8c06160999bcb58'
    assert sha(resultpath)=='af2beada94b56cebc1ac100cbb751a10a7124c7d161601c897bba83f4cc5520b'
    old=current.read_text();orig=original.read_text();a=json.loads(resultpath.read_text());fams=a['all236']['families']
    assert a['status']=='PASS' and len(fams)==21 and a['all236']['covered_interfaces']==236
    ids=set();checks=[];directions={'F':0,'R':0};typecounts={};tablelines=[]
    for t,f in fams.items():
        words=f['selected_new_words'];assert len(words)==f['minimum_new_members'] and words==f['usable_words']
        tablelines.append(t+'&'+r',\ '.join(words)+r'\\')
        for c in f['coverage']:
            interface=c['interface'];v=c['selected_actual_state'];cert=c['saved_certificate'];direction=c['direction'];case=identity(interface)
            assert case not in ids and interface['source']==t and interface['origin']=='existing283' and v in words
            assert direction in directions and c['all_selected_supports']
            assert dict(state=v,direction=direction) in c['all_selected_supports']
            d=cert['HC_side_degree'];g=cert['safe_incident_count'];ns=cert['HC_side_neighbours'];safe=cert['safe_fixed_K_neighbours']
            assert d==sum(cert['HC_side_degree_terms'])==len(set(ns)) and g==len(set(safe)) and set(safe)<=set(ns)
            assert cert['protected_edge_lower_bound']==max(0,2+g-d)>=1 and d-g<=1
            assert (direction=='F' and interface['target_type'] not in ('00001','00112')) or (direction=='R' and t not in ('00001','00112'))
            assert len(interface['mapping'])==3
            ids.add(case);directions[direction]+=1;typ=(d,g);typecounts[str(typ)]=typecounts.get(str(typ),0)+1
            checks.append(c)
    assert len(ids)==236 and directions=={'F':139,'R':97}
    members=sum(len(f['selected_new_words']) for f in fams.values());distinct=set().union(*(set(f['selected_new_words']) for f in fams.values()))
    assert members==78 and len(distinct)==47
    O=blocks(orig);B=blocks(old);assert len(O)==len(B)==53 and all(O[k]==B[k] for k in B if k!='INTERFACES-ALL')
    matches=list(re.finditer(PATTERN,O['INTERFACES-ALL']));assert len(matches)==283
    removed=[m.group(0) for m in matches if row_identity(m) in ids];remaining=[m.group(0) for m in matches if row_identity(m) not in ids]
    assert len(removed)==236 and len(remaining)==47 and {row_identity(m) for m in matches if row_identity(m) in ids}==ids
    oldremaining={row_identity(m) for m in re.finditer(PATTERN,B['INTERFACES-ALL'])};assert len(oldremaining)==158
    old125={row_identity(m) for m in matches}-oldremaining;assert len(old125)==125 and old125<=ids
    assert set(identity(u['interface']) for u in a['uncovered_interfaces'])==set(row_identity(m) for m in matches)-ids
    body='\\begingroup\\scriptsize\\ttfamily\\begin{flushleft}\n'+'\n'.join(' ; '.join(remaining[i:i+2])+r'\\' for i in range(0,len(remaining),2))+'\n\\end{flushleft}\\endgroup\n'
    candidate=old.replace(B['INTERFACES-ALL'],body,1)
    previous='''For the 313 standard-source interfaces, the appendix gives 158
individual common edges, fifteen source-selector rows covering 125
cases, and six constant-source families covering 30 cases.
Endpoint membership in the specified cycles and outside their pools
proves each individual record. The selector rows use incident unions
of at most three edges with the prescribed first normalizer and pools.
The constant-source families use two normalizing directions and four
protected target edges. Inverse coordinate and colour maps give every
labelled case. This is a complete finite case proof; no finite-length
gluing experiment is used to infer a general rule.'''
    replacement='''For the 313 standard-source interfaces, the appendix gives 47
individual common edges, twenty-one source-selector rows covering 236
cases, and six constant-source families covering 30 cases.
Endpoint membership in the specified templates and outside their pools
proves each individual record. The selector rows use fixed protected
incident edges against the opposite component's full degree, with the
prescribed first normalizer and pools. The constant-source families use
two normalizing directions and four protected target edges. Inverse
coordinate and colour maps give every labelled case. This is a complete
finite case proof; no finite-length gluing experiment infers a general rule.'''
    assert candidate.count(previous)==1;candidate=candidate.replace(previous,replacement,1)
    verification='Six constant-source families cover 30 cases; fifteen source-selector rows cover 125 by three-edge incident unions, leaving 158 individual edge records.'
    revised='Six constant-source families cover 30 cases; twenty-one source-selector rows cover 236 by the fixed-side incident-degree criterion, leaving 47 individual edge records.'
    assert candidate.count(verification)==1;candidate=candidate.replace(verification,revised,1)
    start=candidate.index('\\paragraph{Three-edge-union source selectors (125 interfaces).}')
    stop=candidate.index('\\paragraph{The 158 remaining individual nonconstant-source interfaces.}',start)
    retained=old[start:old.index('\\paragraph{The 158 remaining individual nonconstant-source interfaces.}',start)]
    (HERE/'retained-stage9-three-edge-union.tex').write_text(retained)
    table=r'\[\begin{array}{c|l}t&S_t\\\hline'+'\n'+'\n'.join(tablelines)+'\n'+r'\end{array}\]'+'\n'
    (HERE/'source-selector-table.tex').write_text(table)
    fragment=(HERE/'fixed-side-local-proof.tex').read_text()+'\n'+table+'\n'+SUFFIX
    candidate=candidate[:start]+fragment+candidate[stop:]
    candidate=candidate.replace('\\paragraph{The 158 remaining individual nonconstant-source interfaces.}','\\paragraph{The 47 remaining individual nonconstant-source interfaces.}',1)
    C=blocks(candidate);assert len(C)==53 and all(B[k]==C[k] for k in B if k!='INTERFACES-ALL')
    assert len(re.findall(PATTERN,C['INTERFACES-ALL']))==47
    S=statements(old);assert len(S)==41 and statements(candidate)==S
    normalization=lambda z:z.split('Here is the exact normalization convention.',1)[1].split('\\begin{lemma}',1)[0]
    assert normalization(old)==normalization(candidate)
    path=HERE/(NAME+'.tex');path.write_text(candidate);(HERE/'source-family-fragment-v1.tex').write_text(fragment)
    (HERE/'removed236-individual-records.json').write_text(json.dumps(dict(removed_count=236,records=removed,retained_count=47,retained_records=remaining,selected_case_conditions=checks,total_interfaces=313,old125_contained=True),indent=2)+'\n')
    out=dict(status='PASS',python=platform.python_version(),source_sha256=sha(current),original_283_source_sha256=sha(original),mask_result_sha256=sha(resultpath),candidate_sha256=sha(path),other52marked_blocks_byte_exact=True,all41theorem_statements_byte_exact=True,normalizer_paragraph_byte_exact=True,individual_records_before=158,original_individual_records=283,individual_records_after=47,source_selector_cases=236,source_selector_rows=21,constant_six_family_cases=30,total_interfaces=313,selected_direction_counts=directions,selected_certificate_types=typecounts,printed_source_selector_members=members,distinct_source_selector_words=len(distinct),individual_endpoint_plus_printed_selector_words_before=364,individual_endpoint_plus_printed_selector_words_after=172,individual_endpoint_plus_distinct_selector_words_after=141,raw_tex_bytes_before=len(old.encode()),raw_tex_bytes_after=len(candidate.encode()),raw_tex_ascii_letter_tokens_before=len(re.findall(r'[A-Za-z]+',old)),raw_tex_ascii_letter_tokens_after=len(re.findall(r'[A-Za-z]+',candidate)),raw_tex_whitespace_tokens_before=len(old.split()),raw_tex_whitespace_tokens_after=len(candidate.split()),all_tex_five_digit_tokens_before=len(re.findall(r'\b[0-4]{5}\b',old)),all_tex_five_digit_tokens_after=len(re.findall(r'\b[0-4]{5}\b',candidate)),no_main_edit=True,no_new_numbered_lemma=True,no_font_spacing_or_pagebreak_changes=True,retained_stage9_stronger_proof=True)
    (HERE/'candidate-structure-results-v1.json').write_text(json.dumps(out,indent=2)+'\n')
    target=CONT/'candidate-v1';target.mkdir(exist_ok=True);shutil.copyfile(path,target/path.name)
    print(json.dumps(out,indent=2))
if __name__=='__main__':run()
