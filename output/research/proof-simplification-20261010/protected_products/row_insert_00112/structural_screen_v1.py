"""Exact structural screen; no Hamilton-path/cycle discovery in this version."""
from pathlib import Path
from itertools import product,combinations
from collections import Counter
import hashlib,json,re

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parents[1]/'clique_lifts'/'protected_interfaces'/'literal-input.tex'

def main():
    inp=HERE/'literal-input.tex'
    if not inp.exists():inp.write_bytes(SOURCE.read_bytes())
    text=inp.read_text()
    def block(name):return re.search('% BEGIN '+name+'\n(.*?)% END '+name,text,re.S).group(1)
    def read_edges(name):return {tuple(sorted(e)) for e in re.findall(r'([0-3]{5})-([0-3]{5})',block(name))}
    D=read_edges('PORTS-00112');pool=read_edges('POOL-00112-0');K=D-pool
    words=re.findall(r'\b[01][0-3]{5}\b',block('C2-00112'))
    vertices=sorted(''.join(map(str,x)) for x in product(range(4),repeat=5)
                    if all(x[i]!=x[(i+1)%5] and str(x[i])!='00112'[i] for i in range(5)))
    assert len(vertices)==51 and set(vertices)=={w[1:] for w in words}
    C2={tuple(sorted(e)) for e in zip(words,words[1:]+words[:1])}
    row1={tuple(sorted((a[1:],b[1:]))) for a,b in C2 if a[0]==b[0]=='1'}
    edges={tuple(sorted((a,b))) for a,b in combinations(vertices,2)
           if sum(x!=y for x,y in zip(a,b))==1}
    adj={v:{b if a==v else a for a,b in edges if v in (a,b)} for v in vertices}
    leaves={v:next(iter(ns)) for v,ns in adj.items() if len(ns)==1}
    assert leaves=={'12303':'12323','13203':'23203'}
    removed=set(leaves)|set(leaves.values());core=sorted(set(vertices)-removed)
    core_edges={e for e in edges if not set(e)&removed}
    core_adj={v:{b if a==v else a for a,b in core_edges if v in (a,b)} for v in core}
    assert len(core)==47 and len(core_edges)==94
    triangles=sorted([tuple(sorted((a,b,c))) for a,b,c in combinations(core,3)
                      if all(tuple(sorted(e)) in core_edges for e in ((a,b),(b,c),(a,c)))])
    assert triangles==[('21020','21021','21023'),('21320','21321','21323'),('23020','23021','23023')]
    reserves=[e for e in sorted(pool) if not set(e)&set(leaves.values())]
    assert len(reserves)==6 and all(sum(v in e for e in K)==0 for v in leaves.values())

    def closure(protected):
        allowed=set(core_edges);forced=set(protected);iterations=0;failure=None
        while True:
            iterations+=1;old=(len(allowed),len(forced))
            for v in core:
                f={e for e in forced if v in e};a={e for e in allowed if v in e}
                if len(f)>2:failure={'kind':'protected_degree_exceeds_two','vertex':v,'forced_incident':sorted(f)};break
                if len(a)<2:failure={'kind':'allowed_degree_below_two','vertex':v,'allowed_incident':sorted(a)};break
                if len(f)==2:allowed-=a-f
                if len(a)==2:forced|=a
            if failure:break
            if not forced<=allowed:failure={'kind':'forced_edge_deleted'};break
            left=set(core)
            while left:
                component={min(left)};front=list(component)
                while front:
                    v=front.pop()
                    for a,b in forced:
                        if v not in (a,b):continue
                        w=b if a==v else a
                        if w not in component:component.add(w);front.append(w)
                left-=component
                if len(component)<len(core) and all(sum(v in e for e in forced)==2 for v in component):
                    failure={'kind':'forced_proper_cycle','vertices':sorted(component)};break
            if failure or old==(len(allowed),len(forced)):break
        return {'structurally_feasible':failure is None,'failure':failure,
                'iterations':iterations,'allowed_edges':sorted(allowed),'forced_edges':sorted(forced)}

    screens=[]
    for R in combinations(reserves,2):
        result=closure(K|set(R))
        result['reserves']=R
        result['eligible_core_row1_cuts']=sorted((row1&set(map(tuple,result['allowed_edges'])))-(K|set(R)))
        screens.append(result)
    forced_leaf_cuts=sorted(tuple(sorted((a,b))) for a,b in leaves.items())
    candidate_e=('21201','23201')
    assert candidate_e in row1&core_edges and candidate_e not in D
    output={'boundary':'00112','input_sha256':hashlib.sha256(inp.read_bytes()).hexdigest(),
            'vertices':vertices,'edges':sorted(edges),'K':sorted(K),'pool':sorted(pool),
            'second_row_edges':sorted(row1),'original_leaf_pairs':leaves,
            'core_vertices':core,'core_edges':sorted(core_edges),
            'core_degree_distribution':dict(Counter(map(len,core_adj.values()))),
            'core_degree_two_vertices':{v:sorted(ns) for v,ns in core_adj.items() if len(ns)==2},
            'core_triangles':triangles,'leaf_compatible_reserves':reserves,
            'forced_leaf_cuts':forced_leaf_cuts,'candidate_third_cut':candidate_e,
            'reserve_pair_screens':screens,
            'feasible_pair_count':sum(r['structurally_feasible'] for r in screens),
            'claim':'necessary structural checks only; feasibility is not Hamiltonicity'}
    (HERE/'structural-results-v1.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k in ('boundary','core_degree_distribution','core_degree_two_vertices','core_triangles','feasible_pair_count','candidate_third_cut')}))
    print(json.dumps([{'reserves':s['reserves'],'feasible':s['structurally_feasible'],'failure':s['failure'],'forced_edge_count':len(s['forced_edges'])} for s in screens]))

if __name__=='__main__':main()
