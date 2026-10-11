"""Strictly descending bounded two-opt experiment on one frozen interface."""
from pathlib import Path
from itertools import product,combinations
import json,re,hashlib

HERE=Path(__file__).resolve().parent


def main():
    old=json.loads((HERE/'switch-results.json').read_text())
    cycles=[old['answer']['alternate_cycle'],old['answer']['unchanged_cycle']]
    text=(HERE/'literal-input.tex').read_text()
    blocks=dict(re.findall(r'% BEGIN ([A-Z0-9-]+)\n(.*?)% END \1',text,re.S))
    edge=lambda u,v:tuple(sorted((u,v)))
    edges=lambda c:{edge(u,v) for u,v in zip(c,c[1:]+c[:1])}
    legal=lambda u,v:sum(a!=b for a,b in zip(u,v))==1
    states=[];graph_edges=[];forced=[]
    for boundary in ('00101','10101'):
        vs={''.join(map(str,w)) for w in product(range(4),repeat=5)
            if all(w[i]!=w[(i+1)%5] and w[i]!=int(boundary[i]) for i in range(5))}
        es={edge(u,v) for u,v in combinations(vs,2) if legal(u,v)}
        adj={u:{v for e in es if u in e for v in e if v!=u} for u in vs}
        states.append(vs);graph_edges.append(es)
        forced.append({e for e in es if any(len(adj[u])==2 for u in e)})
    pool0={edge(u,v) for u,v in re.findall(r'([0-3]{5})-([0-3]{5})',blocks['POOL-00101-0'])}
    swap='1023'
    restore=lambda w:''.join(swap[int(w[(-i)%5])] for i in range(5))
    pools=[pool0,{edge(restore(u),restore(v)) for u,v in pool0}]
    def validate(c,side):
        assert len(c)==len(set(c))==64 and set(c)==states[side]
        assert edges(c)<=graph_edges[side] and pools[side]<=edges(c)
    for side,c in enumerate(cycles):validate(c,side)
    start_common=edges(cycles[0])&edges(cycles[1]);assert len(start_common)==8
    common_forced=forced[0]&forced[1]
    common_pool=pools[0]&pools[1]
    floor=common_forced|common_pool
    assert floor<=start_common
    steps=[];checks=0;valid=0
    while True:
        current=edges(cycles[0])&edges(cycles[1])
        best=None;best_count=len(current)
        for side,c in enumerate(cycles):
            other_edges=edges(cycles[1-side]);n=len(c)
            for i in range(n):
                for j in range(i+2,n):
                    if i==0 and j==n-1:continue
                    checks+=1
                    a,b=c[i],c[(i+1)%n];u,v=c[j],c[(j+1)%n]
                    if edge(a,b) in pools[side] or edge(u,v) in pools[side]:continue
                    if not legal(a,u) or not legal(b,v):continue
                    alternate=c[:i+1]+c[i+1:j+1][::-1]+c[j+1:]
                    valid+=1
                    new_common=edges(alternate)&other_edges
                    if len(new_common)<best_count:
                        best_count=len(new_common)
                        best=(side,i,j,alternate,{edge(a,b),edge(u,v)},{edge(a,u),edge(b,v)})
        if best is None:break
        side,i,j,alternate,removed,added=best;validate(alternate,side)
        steps.append({'side':side,'cut_indices':[i,j],'raw_before':len(current),'raw_after':best_count,
            'removed_edges':[list(e) for e in sorted(removed)],'added_edges':[list(e) for e in sorted(added)]})
        cycles[side]=alternate
        assert len(steps)<=8
        if best_count==len(floor):break
    final=edges(cycles[0])&edges(cycles[1])
    protected=(edges(cycles[0])-pools[0])&(edges(cycles[1])-pools[1])
    result={'status':'complete','fixed_interface':'00101->10101','start_raw_common':8,
        'accepted_steps':steps,'edge_pair_checks':checks,'legal_pool_preserving_switches':valid,
        'forced_edge_counts':[len(s) for s in forced],
        'common_forced_edges':[list(e) for e in sorted(common_forced)],
        'common_fixed_pool_edges':[list(e) for e in sorted(common_pool)],
        'unavoidable_raw_floor_from_forced_and_pools':len(floor),
        'final_raw_common':len(final),'final_common_edges':[list(e) for e in sorted(final)],
        'final_common_K_count':len(protected),'final_common_K_edges':[list(e) for e in sorted(protected)],
        'both_old_pool8_retained':True,'cycles':cycles,
        'stopping_reason':'reached forced/pool floor' if len(final)==len(floor) else 'no strictly descending pool-preserving single switch',
        'scope':'One fixed interface, strictly descending single-switch experiment only; no full kernel or arbitrary Hamilton search.',
        'input_sha256':hashlib.sha256((HERE/'literal-input.tex').read_bytes()).hexdigest(),
        'v1_sha256':hashlib.sha256((HERE/'switch-results.json').read_bytes()).hexdigest()}
    (HERE/'greedy-results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='cycles'}))


if __name__=='__main__':main()
