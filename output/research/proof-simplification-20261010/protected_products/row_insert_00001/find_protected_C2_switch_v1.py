"""Bounded protected rectangle-switch search on one frozen 88-state factor.

Search is restricted to A-edge x P2 squares, preserving Kstar+two reserves
in each row and both YY edges in row digit1 throughout.
"""
from pathlib import Path
from itertools import combinations
from collections import Counter
import heapq,hashlib,json,time

HERE=Path(__file__).resolve().parent
NODE_CAP=50000
TIME_CAP_SECONDS=10.0

def edge(u,v):return tuple(sorted((u,v)))

def main():
    source=HERE/'local-switch-results-v1.json';data=json.loads(source.read_text())
    old=json.loads((HERE/'obstruction-results-v1.json').read_text())
    seed=data['explicit_variants'][0]
    vertices=[r+v for r in '01' for v in old['vertices']]
    edges=sorted({edge(r+u,r+v) for r in '01' for u,v in old['edges']}|
                 {edge('0'+v,'1'+v) for v in old['vertices']})
    indexes={e:i for i,e in enumerate(edges)}
    vindex={v:i for i,v in enumerate(vertices)}
    endpoints=[tuple(vindex[v] for v in e) for e in edges]
    def bits(es):return sum(1<<indexes[edge(u,v)] for u,v in es)
    initial=bits(e for cs in seed['result_cycles'] for e in zip(cs,cs[1:]+cs[:1]))
    K={tuple(e) for e in old['old_K12']} - {('12313','12323')} | {('13120','23120')}
    usable=[tuple(e) for e in old['old_pool7'] if not set(e)&set(old['Y_internal_endpoints'])]
    squares=[]
    for u,v in old['edges']:
        h=bits((edge('0'+u,'0'+v),edge('1'+u,'1'+v)))
        vv=bits((edge('0'+u,'1'+u),edge('0'+v,'1'+v)))
        squares.append((h,vv,h|vv))
    def cycles(state):
        adjacency=[[] for _ in vertices]
        remaining=state
        while remaining:
            low=remaining&-remaining;i=low.bit_length()-1;remaining-=low
            u,v=endpoints[i];adjacency[u].append(v);adjacency[v].append(u)
        assert all(len(ns)==2 for ns in adjacency)
        unseen=set(range(len(vertices)));components=[]
        while unseen:
            start=min(unseen);prev=None;u=start;cs=[]
            while not cs or u!=start:
                cs.append(u);unseen.remove(u)
                v=next(v for v in adjacency[u] if v!=prev);prev,u=u,v
            components.append(cs)
        return components
    start=time.monotonic();visited_nodes=0;reports=[];found=None
    for R in combinations(usable,2):
        D=K|set(R)
        required=bits(edge(r+u,r+v) for r in '01' for u,v in D)|bits(edge('1'+u,'1'+v) for u,v in old['Y_internal_edges'])
        assert initial&required==required
        queue=[(len(cycles(initial)),0,0,initial)];prev={initial:None};serial=0;local_nodes=0
        while queue and visited_nodes<NODE_CAP and time.monotonic()-start<TIME_CAP_SECONDS:
            count,depth,_,state=heapq.heappop(queue);visited_nodes+=1;local_nodes+=1
            if count==1:
                sequence=[];trace=state
                while prev[trace] is not None:
                    older,which=prev[trace];sequence.append(which);trace=older
                sequence.reverse()
                cs=cycles(state)[0];literal=[vertices[i] for i in cs]
                found={'two_reserves':R,'D14':sorted(D),'C2_words':literal,
                       'rectangle_switch_indexes':sequence,'C2_edges':sorted(edges[i] for i in range(len(edges)) if state>>i&1),
                       'all14_protected_in_both_rows':True,'both_YY_edges_in_row_digit1':True}
                break
            for i,(h,vv,full) in enumerate(squares):
                present=state&full
                if present not in (h,vv) or present&required:
                    continue
                new=state^full
                if new in prev:continue
                prev[new]=(state,i);serial+=1
                comps=len(cycles(new))
                heapq.heappush(queue,(comps,depth+1,serial,new))
        reports.append({'two_reserves':R,'nodes':local_nodes,'states_seen':len(prev),
                        'status':'FOUND' if found else ('EXHAUSTED_RECTANGLE_COMPONENT' if not queue else 'UNKNOWN_LIMIT')})
        if found or visited_nodes>=NODE_CAP or time.monotonic()-start>=TIME_CAP_SECONDS:break
    result={'status':'FOUND' if found else 'UNKNOWN','certificate':found,'reserve_attempts':reports,
            'total_nodes':visited_nodes,'elapsed_seconds':time.monotonic()-start,
            'bounds':{'node_cap':NODE_CAP,'wall_time_seconds':TIME_CAP_SECONDS},
            'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
            'limitations':['Search only uses protected A-edge x P2 rectangle switches from one specified factor.',
                           'UNKNOWN or exhausted rectangle component does not imply no protected two-row seed exists.']}
    (HERE/'protected-C2-switch-results-v1.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='certificate'}))
    if found:print(json.dumps({'reserves':found['two_reserves'],'number_switches':len(found['rectangle_switch_indexes'])}))

if __name__=='__main__':main()
