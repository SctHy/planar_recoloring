"""Read the phase5 candidate directly; no path search or interface replay."""
from pathlib import Path
from itertools import product
import hashlib,json,re,shutil

HERE=Path(__file__).resolve().parent
BASE=HERE.parent


def main():
    source=HERE/'candidate-input.tex'
    original=HERE/'baseline-input.tex'
    new=source.read_text();old=original.read_text()
    digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    assert digest(source)=='85e08613026474c11a5b5a804361070e1a68ca7857ad93f5cc8386bf4549d6f6'
    def blocks(text):
        return dict(re.findall(r'% BEGIN ([A-Z0-9-]+)\n(.*?)% END \1',text,re.S))
    nb,ob=blocks(new),blocks(old)
    changed=sorted(k for k in ob.keys()&nb.keys() if ob[k]!=nb[k])
    removed=sorted(ob.keys()-nb.keys());added=sorted(nb.keys()-ob.keys())
    assert changed==['POOL-00112-0','PORTS-00112']
    assert removed==['C3-00112'] and added==['COREPATH-00112']
    assert nb['C2-00112']==ob['C2-00112']
    assert re.findall(r'\\label\{([^}]+)\}',new)==re.findall(r'\\label\{([^}]+)\}',old)
    def statements(text):
        return re.findall(r'\\begin\{(theorem|lemma|proposition|corollary)\}(.*?)\\end\{\1\}',text,re.S)
    assert statements(new)==statements(old)
    edge=lambda a,b:tuple(sorted((a,b)))
    pairs=lambda block:{edge(a,b) for a,b in re.findall(r'([0-3]{5})-([0-3]{5})',block)}
    oldD,oldpool=pairs(ob['PORTS-00112']),pairs(ob['POOL-00112-0'])
    D,pool=pairs(nb['PORTS-00112']),pairs(nb['POOL-00112-0'])
    assert len(oldD)==18 and len(oldpool)==7 and len(oldD-oldpool)==11
    assert len(D)==13 and len(pool)==2 and pool<=D
    assert D-pool==oldD-oldpool
    states={''.join(map(str,w)) for w in product(range(4),repeat=5)
        if all(w[i]!=w[(i+1)%5] and w[i]!=(0,0,1,1,2)[i] for i in range(5))}
    assert len(states)==51
    core=re.findall(r'\b[0-3]{5}\b',nb['COREPATH-00112'])
    removed_states={'12303','12323','13203','23203'}
    assert len(core)==len(set(core))==47 and set(core)==states-removed_states
    assert (core[0],core[-1])==('21201','23201')
    assert all(sum(a!=b for a,b in zip(u,v))==1 for u,v in zip(core,core[1:]))
    assert D<={edge(u,v) for u,v in zip(core,core[1:])}
    c2=re.findall(r'\b[01][0-3]{5}\b',nb['C2-00112'])
    assert len(c2)==len(set(c2))==102
    assert set(c2)=={str(r)+w for r in (0,1) for w in states}
    e2={edge(u,v) for u,v in zip(c2,c2[1:]+c2[:1])}
    def legal(u,v):
        return (u[0]==v[0] and sum(a!=b for a,b in zip(u[1:],v[1:]))==1) or (
            abs(int(u[0])-int(v[0]))==1 and u[1:]==v[1:])
    assert all(legal(u,v) for u,v in e2)
    row_edges=lambda ee,r:{edge(u[1:],v[1:]) for u,v in ee if u[0]==v[0]==str(r)}
    assert all(D<=row_edges(e2,r) for r in (0,1))
    paths=[['12303','12323'],['13203','23203'],core]
    match={edge(p[0],p[-1]) for p in paths}
    assert len(match)==3 and len(set().union(*map(set,match)))==6
    assert {edge('1'+u,'1'+v) for u,v in match}<=e2 and not match&D
    substitutions={edge(p[0],p[-1]):p for p in paths}
    c3=[];cuts=0
    for u,v in zip(c2,c2[1:]+c2[:1]):
        c3.append(u)
        if u[0]==v[0]=='1' and edge(u[1:],v[1:]) in match:
            p=substitutions[edge(u[1:],v[1:])]
            if p[0]!=u[1:]:p=p[::-1]
            assert (p[0],p[-1])==(u[1:],v[1:])
            c3.extend('2'+w for w in p);cuts+=1
    assert cuts==3 and len(c3)==len(set(c3))==153
    assert set(c3)=={str(r)+w for r in (0,1,2) for w in states}
    e3={edge(u,v) for u,v in zip(c3,c3[1:]+c3[:1])}
    assert all(legal(u,v) for u,v in e3)
    assert all(D<=row_edges(e3,r) for r in (0,1,2))
    assert '|D_A|=18' not in new
    assert 'C3 for 00112 (153 words)' not in new
    assert 'Common ports 00112 (18 edges)' not in new
    result={'status':'PASS','candidate_sha256':digest(source),'baseline_sha256':digest(original),
        'all_theorem_lemma_proposition_corollary_statements_exactly_unchanged':True,
        'ordered_labels_exactly_unchanged':True,'changed_literal_blocks':changed,
        'removed_literal_blocks':removed,'added_literal_blocks':added,
        'all_other_literal_blocks_byte_exact':True,'C2_00112_block_byte_exact':True,
        'D_00112_count':13,'pool_00112_count':2,'K_00112_count':11,
        'K_00112_exactly_old_K':True,'core_path_states':47,'derived_cycle_states':153,
        'derived_C3_all_states_exactly_once':True,'derived_C3_all_edges_legal':True,
        'derived_C3_all_13_ports_in_all_3_rows':True,'no_stale_D18_pool7_oldC3_assertions':True,
        'adjacent_pair_symbolic_review':'PASS: unchanged/equal-list and unchanged/unequal-list cases, equal-to-unequal transition, and three-distinct-excluded-colour transition are exhaustive. The latter cycles each use4 of6 common edges. Every path-order splice retains one of at least2 common edges.',
        'mathematical_review':'PASS: new-row paths are internally disjoint and have exactly the original cut-edge endpoints, so three edge subdivisions produce one cycle. The existing protected product needs exactly two distinct alternating reserves and K is unchanged; all interface assertions therefore retain their old protected sets.',
        'limitations':['Exact source and fixed-certificate review only; no full interface kernel replay or Hamilton search','Candidate is reviewed, not independently compiled by this reviewer','No manuscript edits']}
    (HERE/'candidate-review.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__=='__main__':main()
