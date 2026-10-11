"""Fixed 00001 core/ear decomposition and a nontraceability cut certificate."""
from pathlib import Path
from itertools import product
import hashlib,json,re,time

HERE=Path(__file__).resolve().parent


def main():
    started=time.perf_counter()
    raw=(HERE/'graph-input.json').read_bytes(); given=json.loads(raw)
    states=set(given['states']); edge=lambda a,b:tuple(sorted((a,b)))
    edges={edge(a,b) for a,b in given['edges']}
    generated={''.join(map(str,w)) for w in product(range(4),repeat=5)
        if all(w[i]!=w[(i+1)%5] and w[i]!=(0,0,0,0,1)[i] for i in range(5))}
    generated_edges={edge(a,b) for a in generated for b in generated
                    if a<b and sum(x!=y for x,y in zip(a,b))==1}
    assert states==generated and edges==generated_edges
    assert len(states)==44 and len(edges)==74
    adj={w:{b if a==w else a for a,b in edges if w in (a,b)} for w in states}
    core={w for w in states if w[-1]=='0'}
    assert len(core)==24 and all(set(w[:4])<={'1','2','3'} for w in core)
    literal=(HERE/'literal-input.tex').read_text()
    block=re.search(r'% BEGIN FACTOR-00000\n(.*?)% END FACTOR-00000',literal,re.S).group(1)
    cc=re.findall(r'\b[0-3]{5}\b',block); assert len(cc)==30
    def sigma(w):
        sign=lambda a,b:1 if (int(b)-int(a))%3==1 else -1
        return sign(w[0],w[1])*sign(w[2],w[3])
    def chi(w): return sigma(w) if w[-1]=='0' else -sigma(w)
    ears=[]
    for i in range(2):
        cycle=cc[15*i:15*(i+1)]
        deleted=[j for j,w in enumerate(cycle) if w[-1]=='1']
        assert len(deleted)==5 and any(
            set(deleted)=={(j+r)%15 for r in range(5)} for j in range(15))
        ear={w for w in cycle if w[-1]!='1'}
        assert len(ear)==10 and ear<=states-core
        ends=sorted(w for w in ear if len(adj[w]&ear)==1)
        assert len(ends)==2 and all(len(adj[w]&ear)==2 for w in ear-set(ends))
        path=[ends[0]]
        while len(path)<10:
            nxt=(adj[path[-1]]&ear)-set(path); assert len(nxt)==1
            path.append(next(iter(nxt)))
        images=[w[:4]+'0' for w in ends]
        assert all(z in core and z in adj[w] for w,z in zip(ends,images))
        assert all(sigma(w)==1 for w in images)
        ears.append({'component':i,'deleted_five': [cycle[j] for j in deleted],
            'P10_path':path,'endpoint_core_images':images,
            'core_sign_of_both_endpoints':1,
            'chi_class_counts':{str(s):sum(chi(w)==s for w in ear) for s in (-1,1)},
            'all_matching_edges_to_core':[list(edge(w,w[:4]+'0')) for w in sorted(ear)]})
    assert core|set(ears[0]['P10_path'])|set(ears[1]['P10_path'])==states
    core_edges={e for e in edges if set(e)<=core}
    assert len(core_edges)==36 and all(sigma(a)==-sigma(b) for a,b in core_edges)
    assert sum(sigma(w)==1 for w in core)==12
    X={w for w in states if chi(w)==-1}; S=states-X
    inside_X={e for e in edges if set(e)<=X}; inside_S={e for e in edges if set(e)<=S}
    expected={edge('12312','12313'),edge('13212','13213')}
    assert len(X)==24 and len(S)==20 and inside_X==expected and not inside_S
    components=[list(e) for e in sorted(inside_X)]+[[w] for w in sorted(X-set().union(*map(set,inside_X)))]
    assert len(components)==22 and sum(map(len,components))==24
    # An explicit perfect matching proves alpha <= 22. The cut's 20 isolates
    # plus one endpoint of each remaining edge give an independent set of 22.
    matching=set()
    for w in core:
        replacement=next(c for c in '123' if c not in (w[0],w[1]))
        z=replacement+w[1:]
        matching.add(edge(w,z))
    assert len(matching)==12
    for ear in ears:
        path=ear['P10_path']
        matching|={edge(path[j],path[j+1]) for j in range(0,10,2)}
    assert len(matching)==22 and matching<=edges
    assert len(set().union(*map(set,matching)))==44
    independent=set(X)
    for a,b in inside_X: independent.remove(max(a,b))
    assert len(independent)==22 and not any(set(e)<=independent for e in edges)
    result={'boundary':'00001','vertices':44,'edges':74,
        'input_sha256':hashlib.sha256(raw).hexdigest(),
        'literal_input_sha256':hashlib.sha256((HERE/'literal-input.tex').read_bytes()).hexdigest(),
        'core':{'vertices':24,'edges':36,'bipartition_sizes':[12,12]},'ears':ears,
        'sign_definition':'sigma=orientation(positions 1,2)*orientation(positions 3,4), cyclic colors 1->2->3->1; chi=sigma if last=0, otherwise -sigma',
        'cut_certificate':{'S':sorted(S),'S_size':20,'remaining_vertices':sorted(X),
            'remaining_edges':[list(e) for e in sorted(inside_X)],
            'components':components,'component_count':22,'Hamilton_path_upper_bound':21,
            'nontraceable':True},
        'maximum_independent_set_size':22,'maximum_independent_set':sorted(independent),
        'perfect_matching':[list(e) for e in sorted(matching)],
        'elapsed_seconds':time.perf_counter()-started,
        'scope':'fixed local graph only; no Hamilton-path search'}
    (HERE/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('ears','maximum_independent_set','perfect_matching','cut_certificate')}|
          {'cut':result['cut_certificate']}))


if __name__=='__main__': main()
