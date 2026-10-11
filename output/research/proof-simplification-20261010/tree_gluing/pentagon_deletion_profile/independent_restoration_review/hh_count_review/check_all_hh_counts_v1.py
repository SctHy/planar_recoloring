"""Independent230 selected-cycle count; no peer imports/HC/edge intersections."""
from pathlib import Path
from itertools import product,permutations
from collections import Counter
import hashlib,json,re,time

HERE=Path(__file__).resolve().parent
HARD={'00001','00112'}
def edge(u,v):return tuple(sorted((u,v)))
def parse(w):return tuple(map(int,w))
def text(w):return ''.join(map(str,w))
def coordinate(e):
    changed=[i for i in range(5) if e[0][i]!=e[1][i]];assert len(changed)==1
    return changed[0]
def cycle(ws):
    assert len(ws)==len(set(ws))
    out={edge(u,v) for u,v in zip(ws,ws[1:]+ws[:1])}
    for e in out:coordinate(e)
    return out
def legal(t):return {w for w in product(range(4),repeat=5) if all(w[i]!=w[(i+1)%5] and (t[i]==4 or w[i]!=t[i]) for i in range(5))}
def common_graph(V):
    out=set()
    for w in V:
        for i in range(5):
            for c in range(4):
                if c==w[i]:continue
                other=w[:i]+(c,)+w[i+1:]
                if other in V:out.add(edge(w,other))
    return out
def count(es):
    counts=Counter(map(coordinate,es));return [counts[i] for i in range(5)]

def main():
    began=time.monotonic();source=HERE/'phase6-source.tex';src=source.read_text();peer_input=HERE/'peer-hh-results-v1.json';peer=json.loads(peer_input.read_text())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==peer['source_provenance']['source_sha256']
    blocks=dict(re.findall(r'% BEGIN ([A-Z0-9-]+)\n(.*?)% END \1',src,re.S))
    ordinary=set(re.findall(r'% BEGIN C1-([0-3]{5})',src))
    starred=set(re.findall(r'% BEGIN FHC-([0-4]{5})',src))
    standard=ordinary|starred|HARD|{'00000'};assert len(ordinary)==8 and len(starred)==11 and len(standard)==22
    def words(n):return [parse(w) for w in re.findall(r'\b[0-3]{5}\b',blocks[n])]
    def pool(n):return {edge(parse(u),parse(v)) for u,v in re.findall(r'([0-3]{5})-([0-3]{5})',blocks[n])}
    selected={};constant=words('FACTOR-00000');assert len(constant)==30
    for t in sorted(standard-HARD):
        ws=[constant[:15],constant[15:]] if t=='00000' else [words(('FHC-' if '4' in t else 'C1-')+t)]
        assert set.union(*(set(w) for w in ws))==legal(parse(t))
        for index,w in enumerate(ws):
            E=cycle(w);P=pool(f'POOL-{t}-{index}');assert P<=E
            assert len(P)==(5 if t=='00000' else 8)
            selected[f'{t}:{index}']=(w,E,P)
    assert len(selected)==21
    perms=tuple(permutations(range(4)))
    def normalizer(t):
        for shift in range(5):
            for eps in (1,-1):
                for p in perms:
                    n=tuple(4 if t[(shift+eps*i)%5]==4 else p[t[(shift+eps*i)%5]] for i in range(5))
                    if text(n) in standard:return text(n),(shift,eps,p)
        raise AssertionError(t)
    def restore(w,g):
        shift,eps,p=g;inverse=[p.index(i) for i in range(4)];out=[None]*5
        for i in range(5):out[(shift+eps*i)%5]=inverse[w[i]]
        return tuple(out)
    rows=[];hard_target_skips=0;empty_state_intersections=0
    for name,(source_words,C,P) in sorted(selected.items()):
        t=parse(name[:5])
        for position in range(5):
            if t[position]==4:continue
            for new in range(4):
                if new==t[position]:continue
                s=t[:position]+(new,)+t[position+1:];nt,g=normalizer(s)
                if nt in HARD:hard_target_skips+=1;continue
                for target,(target_words,_,target_pool) in sorted(selected.items()):
                    if target[:5]!=nt:continue
                    ws=[restore(w,g) for w in target_words];D=cycle(ws);Q={edge(restore(u,g),restore(v,g)) for u,v in target_pool}
                    U=set(source_words)&set(ws)
                    if not U:empty_state_intersections+=1;continue
                    H=common_graph(U);F=(P|Q)&H
                    # Each selected cycle is counted separately; no C&D edge set.
                    a=count(e for e in C if e in H);b=count(e for e in D if e in H)
                    m=count(H);f=count(F);rC=count(e for e in C if e in F);rD=count(e for e in D if e in F)
                    coarse=[a[i]+b[i]-m[i]-f[i] for i in range(5)]
                    refined=[a[i]+b[i]-m[i]-rC[i]-rD[i]+f[i] for i in range(5)]
                    assert all(refined[i]>=coarse[i] for i in range(5))
                    rows.append({'source':name,'changed_position':position,'new_colour':new,'target':target,
                                 'normalizer':[g[0],g[1],list(g[2])],'common_vertices':len(U),
                                 'a':a,'b':b,'m':m,'f':f,'rC':rC,'rD':rD,
                                 'coarse_bounds':coarse,'refined_bounds':refined,
                                 'coarse_hit_coordinates':[i for i in range(5) if coarse[i]>=1],
                                 'refined_hit_coordinates':[i for i in range(5) if refined[i]>=1]})
    key=lambda r:(r['source'],r['changed_position'],r['new_colour'],r['target'])
    own={key(r):r for r in rows};reference={key(r):r for r in peer['cases']}
    assert len(rows)==len(own)==230 and own.keys()==reference.keys()
    discrepancies=[]
    for case,r in own.items():
        if r!=reference[case]:discrepancies.append({'case':case,'own':r,'peer':reference[case]})
    assert not discrepancies
    coarse_hits=sum(bool(r['coarse_hit_coordinates']) for r in rows);refined_hits=sum(bool(r['refined_hit_coordinates']) for r in rows)
    assert (coarse_hits,refined_hits)==(216,222)==(peer['coarse_covered'],peer['refined_covered'])
    by_source={}
    for r in rows:
        group=by_source.setdefault(r['source'],{'total':0,'coarse':0,'refined':0});group['total']+=1;group['coarse']+=bool(r['coarse_hit_coordinates']);group['refined']+=bool(r['refined_hit_coordinates'])
    assert by_source==peer['coverage_by_source']
    constant_source=sum(r['source'].startswith('00000:') for r in rows);constant_target=sum(r['target'].startswith('00000:') for r in rows)
    assert constant_source==constant_target==peer['constant_source_HH_interfaces']==peer['constant_target_HH_interfaces']==0
    assert all(r['source'][:5] not in HARD and r['target'][:5] not in HARD for r in rows)
    result={'status':'PASS_BOUNDED_SUPPORTING_COUNT','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
            'peer_results_sha256':hashlib.sha256(peer_input.read_bytes()).hexdigest(),
            'selected_HH_component_count':21,'source_components_with_actual_cases':len(by_source),'interface_count':230,
            'all_six_five_coordinate_count_arrays_match':True,'all_normalizers_and_case_keys_match':True,
            'coarse_covered':coarse_hits,'refined_covered':refined_hits,'coarse_uncovered':14,'refined_uncovered':8,
            'constant_source_interfaces':constant_source,'constant_target_interfaces':constant_target,
            'hard_components_excluded_on_both_sides':True,'hard_target_transition_skips':hard_target_skips,
            'empty_restored_state_intersection_skips':empty_state_intersections,'coverage_by_source':by_source,
            'uncovered_refined_cases':[r for r in rows if not r['refined_hit_coordinates']],
            'actual_C_intersect_D_edge_set_computed':False,'Hamilton_search':False,
            'scope':'Current selected ordinary/starred HC cycles and pools only; K=C minus pool. Hard D minus pool components are excluded. Counts support230 fixed cases, not a general analytic theorem.',
            'elapsed_seconds':time.monotonic()-began,'cases':rows}
    (HERE/'review-results-v1.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('cases','coverage_by_source','uncovered_refined_cases')}))
if __name__=='__main__':main()
