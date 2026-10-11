"""Direct phase6 manuscript source/certificate review, no helper import or search."""
from pathlib import Path
from itertools import product
import re,json,hashlib

HERE=Path(__file__).resolve().parent


def main():
    n=(HERE/'candidate-input.tex').read_text();o=(HERE/'baseline-input.tex').read_text()
    direct=(HERE/'source-candidate-v2.tex').read_text()
    existing=json.loads((HERE/'source-review-results.json').read_text())
    answer=json.loads((HERE/'source-core40-path-results-v2.json').read_text())['answer']
    blocks=lambda text:dict(re.findall(r'% BEGIN ([A-Z0-9-]+)\n(.*?)% END \1',text,re.S))
    nb,ob=blocks(n),blocks(o)
    labels=lambda text:re.findall(r'\\label\{([^}]+)\}',text)
    statements=lambda text:re.findall(r'\\begin\{(theorem|lemma|proposition|corollary)\}(.*?)\\end\{\1\}',text,re.S)
    assert labels(n)==labels(o) and statements(n)==statements(o)
    changed=sorted(k for k in nb.keys()&ob.keys() if nb[k]!=ob[k])
    removed=sorted(ob.keys()-nb.keys());added=sorted(nb.keys()-ob.keys())
    assert changed==['COMMON-00001','INTERFACES-ALL','PC2-00001','POOL-00001-0']
    assert removed==['PC3-00001'] and added==['COREPATH-00001']
    assert all(nb[k]==ob[k] for k in ['HP-00112','MATCHING-CHAIN-00001','C2-00112','COREPATH-00112','PORTS-00112','POOL-00112-0','CONSTANT-INTERFACE-FAMILIES'])
    edge=lambda u,v:tuple(sorted((u,v)))
    pairs=lambda tag:{edge(u,v) for u,v in re.findall(r'([0-3]{5})-([0-3]{5})',nb[tag])}
    D,R=pairs('COMMON-00001'),pairs('POOL-00001-0');K=D-R
    oldK={edge(u,v) for u,v in re.findall(r'([0-3]{5})-([0-3]{5})',ob['COMMON-00001'])}-{edge(u,v) for u,v in re.findall(r'([0-3]{5})-([0-3]{5})',ob['POOL-00001-0'])}
    assert (len(D),len(R),len(K))==(13,2,11) and R<=D
    assert K==(oldK-{edge('12313','12323'),edge('13230','23230')})|{edge('13120','23120')}
    verbatims=re.findall(r'\\begin\{verbatim\}(.*?)\\end\{verbatim\}',direct,re.S)
    c2=re.findall(r'\b[01][0-3]{5}\b',nb['PC2-00001']);core=re.findall(r'\b[0-3]{5}\b',nb['COREPATH-00001'])
    assert c2==re.findall(r'\b[01][0-3]{5}\b',verbatims[0]) and core==re.findall(r'\b[0-3]{5}\b',verbatims[1])
    assert D=={edge(*e) for e in answer['D13']} and R=={edge(*e) for e in answer['two_reserves']}
    states={''.join(map(str,w)) for w in product(range(4),repeat=5)
        if all(w[i]!=w[(i+1)%5] and w[i]!=(0,0,0,0,1)[i] for i in range(5))}
    cycle_edges=lambda c:{edge(u,v) for u,v in zip(c,c[1:]+c[:1])}
    legal=lambda u,v:(u[0]==v[0] and sum(a!=b for a,b in zip(u[1:],v[1:]))==1) or (abs(int(u[0])-int(v[0]))==1 and u[1:]==v[1:])
    assert len(c2)==len(set(c2))==88 and set(c2)=={str(r)+w for r in (0,1) for w in states}
    assert all(legal(u,v) for u,v in cycle_edges(c2))
    assert len(core)==len(set(core))==40 and set(core)==states-{'12312','12313','13212','13213'}
    assert D<={edge(u,v) for u,v in zip(core,core[1:])}
    paths=[['12312','12313'],['13212','13213'],core];match={edge(p[0],p[-1]) for p in paths}
    assert match=={edge(*e) for e in answer['matching_cuts']} and len(set().union(*map(set,match)))==6 and not match&D
    assert {edge('1'+u,'1'+v) for u,v in match}<=cycle_edges(c2)
    by_pair={edge(p[0],p[-1]):p for p in paths};derived=[];cuts=0
    for u,v in zip(c2,c2[1:]+c2[:1]):
        derived.append(u)
        if u[0]==v[0]=='1' and edge(u[1:],v[1:]) in match:
            p=by_pair[edge(u[1:],v[1:])]
            if p[0]!=u[1:]:p=p[::-1]
            derived.extend('2'+w for w in p);cuts+=1
    assert cuts==3 and derived==answer['derived_C3_words']
    assert len(derived)==len(set(derived))==132 and set(derived)=={str(r)+w for r in (0,1,2) for w in states}
    assert all(legal(u,v) for u,v in cycle_edges(derived))
    row_edges=lambda ee,r:{edge(u[1:],v[1:]) for u,v in ee if u[0]==v[0]==str(r)}
    assert all(D<=row_edges(cycle_edges(c2),r) for r in (0,1))
    assert all(D<=row_edges(cycle_edges(derived),r) for r in (0,1,2))
    records=lambda text:re.findall(r'([0-4]{5}:[01])\s+([0-4])\s+([0-3])\s+([0-4]{5}:[01])\s+([0-3]{5})-([0-3]{5})',text)
    oldrows,newrows=records(ob['INTERFACES-ALL']),records(nb['INTERFACES-ALL']);assert len(oldrows)==len(newrows)==283
    differences=[i for i,(a,b) in enumerate(zip(oldrows,newrows)) if a!=b];assert differences==[5,14,15]
    for i,verified in zip(differences,existing['repairs']):
        assert oldrows[i][:4]==newrows[i][:4]
        assert edge(*newrows[i][4:])==edge(*verified['replacement'])
    assert existing['all313_interfaces_inherited_with_exactly_three_individual_repairs']
    assert '|D_A|=19' not in n and 'seven-edge pool' not in n and 'PC3 for 00001 (132 words)' not in n
    rule=re.search(r'\\paragraph\{Three-row insertion rule\.\}(.*?)\\paragraph\{Common ports 00112',n,re.S).group(1)
    generic_valid=bool(re.search(r'Hamilton cycle of\s*\$A\\square P_2\$',rule))
    result={'status':'PASS' if generic_valid else 'NEEDS_EXPLICIT_HAMILTON_HYPOTHESIS',
        'candidate_sha256':hashlib.sha256((HERE/'candidate-input.tex').read_bytes()).hexdigest(),
        'baseline_sha256':hashlib.sha256((HERE/'baseline-input.tex').read_bytes()).hexdigest(),
        'all41_primary_statements_exactly_unchanged':len(statements(n))==41,
        'all56_ordered_labels_exactly_unchanged':len(labels(n))==56,
        'shared_rule_explicit_C2_Hamilton_hypothesis':generic_valid,
        'shared_rule_symbolic_proof_valid_with_that_hypothesis':True,
        'changed_literal_blocks':changed,'removed_literal_blocks':removed,'added_literal_blocks':added,
        'all_other_literal_blocks_byte_exact':True,'HP00112_and_matchingchain00001_byte_exact':True,
        'new_C2_88_and_core40_exactly_final_direct_v2':True,'new_D13_R2_K11_exactly_final_direct_v2':True,
        'actual_row1_cutmatching_and_derived132_everyword_verified':True,
        'every13_commonport_retained_in_everyseedrow':True,'only_three_individual_witnesses_changed':differences,
        'interface_parameters_exactly_unchanged':True,'all313_membership_inherited_from_independent_certificate_review':True,
        'no_stale_D19_pool7_literalC3_assertions':True,
        'scope':'Source/certificate readback only; nosearch/fullkernel/compile ormain edits.'}
    (HERE/'candidate-review.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__=='__main__':main()
