"""Direct selected-pair graph/cycle/pool enumeration, with no peer imports."""
from pathlib import Path
from itertools import product,permutations,combinations
import hashlib,json,re

HERE=Path(__file__).resolve().parent

def edge(u,v):return tuple(sorted((u,v)))
def parse(w):return tuple(map(int,w))
def text(w):return ''.join(map(str,w))

def main():
    source=HERE/'phase6-source-v1.tex';raw=source.read_bytes();tex=raw.decode()
    note=HERE/'coordinate-note-v1.tex';note_text=note.read_text()
    def block(name):return re.search('% BEGIN '+name+'\n(.*?)% END '+name,tex,re.S).group(1)
    words=[parse(w) for w in re.findall(r'\b[0-3]{5}\b',block('C1-00101'))]
    pool={edge(parse(a),parse(b)) for a,b in re.findall(r'([0-3]{5})-([0-3]{5})',block('POOL-00101-0'))}
    C={edge(u,v) for u,v in zip(words,words[1:]+words[:1])}
    def legal(t):return {w for w in product(range(4),repeat=5) if all(w[i]!=w[(i+1)%5] and w[i]!=t[i] for i in range(5))}
    def graph(V):return {edge(u,v) for u,v in combinations(V,2) if sum(a!=b for a,b in zip(u,v))==1}
    t=parse('00101');s=parse('10101');Vt,Vs=legal(t),legal(s)
    assert len(words)==len(set(words))==64 and set(words)==Vt and len(pool)==8 and pool<=C<=graph(Vt)
    standard=set(re.findall(r'% BEGIN C1-([0-3]{5})',tex))|{'00000','00001','00112'}
    assert len(standard)==11
    chosen=None
    for shift in range(5):
        if chosen:break
        for direction in (1,-1):
            if chosen:break
            for p in permutations(range(4)):
                normalized=tuple(p[s[(shift+direction*i)%5]] for i in range(5))
                if text(normalized) in standard:
                    chosen=(shift,direction,p,text(normalized));break
    assert chosen==(0,-1,(1,0,2,3),'00101')
    def g(w):return tuple((1,0,2,3)[w[-j%5]] for j in range(5))
    target_words=[g(w) for w in words];target_C={edge(g(u),g(v)) for u,v in C};target_pool={edge(g(u),g(v)) for u,v in pool}
    assert set(target_words)==Vs and target_C<=graph(Vs)
    U=Vt&Vs;H=graph(U);J={e for e in H if e[0][0]!=e[1][0]}
    pairs=[(x,y) for x in (0,2,3) for y in (1,2,3) if x!=y]
    expected_J={edge((2,1,x,y,0),(3,1,x,y,0)) for x,y in pairs}
    assert len(J)==7 and J==expected_J and {edge(g(u),g(v)) for u,v in J}==J
    source_J=C&J;target_J=target_C&J;pool_J=(pool|target_pool)&J
    assert len(source_J)==len(target_J)==6 and pool_J=={edge(parse('21010'),parse('31010'))}
    listed_pairs=[tuple(map(int,p)) for p in re.findall(r'\(([0-3]),([0-3])\)',note_text)]
    assert len(listed_pairs)==5
    listed_J={edge((2,1,x,y,0),(3,1,x,y,0)) for x,y in listed_pairs}
    assert listed_J<=source_J&target_J and len(listed_J)==5
    assert {edge(g(u),g(v)) for u,v in listed_J}==listed_J
    assert {edge(g(u),g(v)) for u,v in source_J}!=source_J
    assert source_J-listed_J=={edge(parse('21310'),parse('31310'))}
    assert target_J-listed_J=={edge(parse('21030'),parse('31030'))}
    protected_source=C-pool;protected_target=target_C-target_pool
    safe=protected_source&protected_target&J
    assert len(safe)==4
    def outside_orders(ws):
        outside=set(ws)-U;starts=[i for i,w in enumerate(ws) if w in outside and ws[i-1] not in outside]
        orders=[]
        for start in starts:
            n=0
            while ws[(start+n)%len(ws)] in outside:n+=1
            orders.append(n)
        return sorted(orders)
    outside_source=outside_orders(words);outside_target=outside_orders(target_words)
    assert outside_source==outside_target==[2]*6+[6]*2
    full_F=(pool|target_pool)&H
    full_bound=2*len(U)-len(outside_source)-len(outside_target)-len(H)-len(full_F)
    assert (len(U),len(H),len(full_F),full_bound)==(40,87,3,-26)
    result={'status':'VALID_ARGUMENT_WITH_EXACT_COUNT_CORRECTION','source_sha256':hashlib.sha256(raw).hexdigest(),
            'note_v1_sha256':hashlib.sha256(note.read_bytes()).hexdigest(),
            'canonical_normalizer':{'shift':0,'direction':-1,'permutation':[1,0,2,3],'standard_type':'00101'},
            'seven_common_coordinate_edges':[[text(w) for w in e] for e in sorted(J)],
            'source_selected_edges':[[text(w) for w in e] for e in sorted(source_J)],
            'target_selected_edges':[[text(w) for w in e] for e in sorted(target_J)],
            'actual_source_and_target_J_counts':[6,6],'listed_five_subset_in_both_cycles':True,
            'listed_five_subset_g_invariant':True,'full_source_J_edge_set_g_invariant':False,
            'source_extra_edge':['21310','31310'],'target_extra_edge':['21030','31030'],
            'union_of_pools_in_J':[[text(w) for w in e] for e in sorted(pool_J)],
            'at_least_five_lower_bound':5+5-7-1,'exact_six_capacity_lower_bound':6+6-7-1,
            'actual_common_protected_J_edges':[[text(w) for w in e] for e in sorted(safe)],
            'whole_graph_bound':{'common_vertex_count':40,'common_edge_count':87,'outside_path_orders':[outside_source,outside_target],'forbidden_pool_union_count':3,'lower_bound':-26},
            'no_Hamilton_search':True,'scope':'This specified phase6 selected-cycle/pool pair only; no arbitrary-Hamilton-cycle claim.'}
    (HERE/'review-results-v1.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('seven_common_coordinate_edges','source_selected_edges','target_selected_edges','actual_common_protected_J_edges')}))

if __name__=='__main__':main()
