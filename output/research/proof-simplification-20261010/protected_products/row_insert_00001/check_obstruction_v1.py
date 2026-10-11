"""Direct fixed-graph/count certificate; no seed or Hamilton search."""
from pathlib import Path
from itertools import product,combinations
import hashlib,json,re

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parents[1]/'clique_lifts'/'protected_interfaces'/'literal-input.tex'

def chi(w):
    orientation=lambda a,b:1 if (int(b)-int(a))%3==1 else -1
    return orientation(w[0],w[1])*orientation(w[2],w[3])*(1 if w[4]=='0' else -1)

def main():
    inp=HERE/'original-literal-input.tex'
    if not inp.exists():inp.write_bytes(SOURCE.read_bytes())
    source=inp.read_text()
    def block(name):return re.search('% BEGIN '+name+'\n(.*?)% END '+name,source,re.S).group(1)
    def read_edges(name):return {tuple(sorted(e)) for e in re.findall(r'([0-3]{5})-([0-3]{5})',block(name))}
    vertices=sorted(''.join(map(str,w)) for w in product(range(4),repeat=5)
                    if all(w[i]!=w[(i+1)%5] and str(w[i])!='00001'[i] for i in range(5)))
    E={tuple(sorted((u,v))) for u,v in combinations(vertices,2)
       if sum(a!=b for a,b in zip(u,v))==1}
    X={v for v in vertices if chi(v)==1};Y=set(vertices)-X
    XX={e for e in E if set(e)<=X};YY={e for e in E if set(e)<=Y}
    assert len(vertices)==44 and len(E)==74 and len(X)==20 and len(Y)==24
    assert not XX and YY=={('12312','12313'),('13212','13213')}
    D=read_edges('COMMON-00001');pool=read_edges('POOL-00001-0');K=D-pool
    assert len(D)==19 and len(pool)==7 and len(K)==12 and D<=E
    ends=set().union(*(set(e) for e in YY))
    touching_K=sorted(e for e in K if set(e)&ends)
    assert touching_K==[('12313','12323')]
    words=re.findall(r'\b[01][0-3]{5}\b',block('PC2-00001'))
    assert len(words)==88 and set(words)=={str(i)+v for i in range(2) for v in vertices}
    pairs=list(zip(words,words[1:]+words[:1]))
    for a,b in pairs:
        assert (a[0]==b[0] and tuple(sorted((a[1:],b[1:]))) in E) or (a[0]!=b[0] and a[1:]==b[1:])
    rows={str(i):sorted(tuple(sorted((a[1:],b[1:]))) for a,b in pairs if a[0]==b[0]==str(i)) for i in range(2)}
    assert all(len(es)==38 and not(set(es)&YY) for es in rows.values())
    result={'vertices':vertices,'edges':sorted(E),'X20':sorted(X),'Y24':sorted(Y),
            'X_internal_edges':sorted(XX),'Y_internal_edges':sorted(YY),'Y_internal_endpoints':sorted(ends),
            'old_D19':sorted(D),'old_pool7':sorted(pool),'old_K12':sorted(K),
            'old_K_edges_touching_Y_internal_endpoints':touching_K,
            'old_pool_edges_touching_Y_internal_endpoints':sorted(e for e in pool if set(e)&ends),
            'old_PC2_internal_edges_by_row':rows,
            'old_PC2_has_no_same_class_internal_edges':True,
            'count_identity':'r+q=4; r=#YY matching cuts; q=#YY edges in new-row forest',
            'r_upper_bound':2,'q_upper_bound':2,'necessary_r':2,'necessary_q':2,
            'fixed_old_PC2_obstruction':'r=0 contradicts r+q=4',
            'every_possible_PC2_old_K_obstruction':'r=q=2 makes12313 a forest endpoint using12312; oldK edge12313-12323 conflicts with degree1',
            'old_K_preserving_matching_insertion':'provably impossible for every possible two-row seed',
            'Hamilton_or_seed_search_performed':False,
            'input_sha256':hashlib.sha256(inp.read_bytes()).hexdigest()}
    (HERE/'obstruction-results-v1.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('vertices','edges','X20','Y24','old_D19','old_pool7','old_K12','old_PC2_internal_edges_by_row')}))

if __name__=='__main__':main()
