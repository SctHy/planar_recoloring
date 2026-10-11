"""Two specified local rewires, followed by protected rectangle switches."""
from pathlib import Path
from itertools import combinations
import heapq,hashlib,json,time

HERE=Path(__file__).resolve().parent
NODE_CAP=50000
TIME_CAP_SECONDS=10.0

def edge(u,v):return tuple(sorted((u,v)))

def main():
    inp=HERE/'protected-C2-switch-results-v1.json';oldc=json.loads(inp.read_text())['certificate']
    old=json.loads((HERE/'obstruction-results-v1.json').read_text())
    vertices=[r+v for r in '01' for v in old['vertices']]
    edges=sorted({edge(r+u,r+v) for r in '01' for u,v in old['edges']}|{edge('0'+v,'1'+v) for v in old['vertices']})
    indexes={e:i for i,e in enumerate(edges)};vindex={v:i for i,v in enumerate(vertices)}
    endpoints=[tuple(vindex[v] for v in e) for e in edges]
    def bits(es):return sum(1<<indexes[edge(u,v)] for u,v in es)
    original=bits(oldc['C2_edges']);squares=[]
    for u,v in old['edges']:
        h=bits((edge('0'+u,'0'+v),edge('1'+u,'1'+v)))
        vv=bits((edge('0'+u,'1'+u),edge('0'+v,'1'+v)))
        squares.append((h,vv,h|vv))
    def cycles(state):
        adjacency=[[] for _ in vertices];remaining=state
        while remaining:
            low=remaining&-remaining;i=low.bit_length()-1;remaining-=low;u,v=endpoints[i];adjacency[u].append(v);adjacency[v].append(u)
        assert all(len(ns)==2 for ns in adjacency)
        unseen=set(range(len(vertices)));out=[]
        while unseen:
            start=min(unseen);prev=None;u=start;cs=[]
            while not cs or u!=start:
                cs.append(u);unseen.remove(u);v=next(v for v in adjacency[u] if v!=prev);prev,u=u,v
            out.append(cs)
        return out
    start=time.monotonic();nodes=0;reports=[]
    for partner in ('23230','13232'):
        dropped=edge('13230',partner);D={tuple(e) for e in oldc['D14']}-{dropped}
        removed={edge(r+'13230',r+partner) for r in '01'}|{edge('013210','113210')}
        added={edge(r+'13210',r+'13230') for r in '01'}|{edge('0'+partner,'1'+partner)}
        cut=edge('13210','13230')
        rm,ad=bits(removed),bits(added);assert original&rm==rm and not original&ad
        initial=(original&~rm)|ad
        required=bits(edge(r+u,r+v) for r in '01' for u,v in D)|bits(edge('1'+u,'1'+v) for u,v in old['Y_internal_edges'])|bits([edge('1'+cut[0],'1'+cut[1])])
        assert initial&required==required
        queue=[(len(cycles(initial)),0,0,initial)];prev={initial:None};serial=0;local=0;answer=None
        while queue and nodes<NODE_CAP and time.monotonic()-start<TIME_CAP_SECONDS:
            count,depth,_,state=heapq.heappop(queue);nodes+=1;local+=1
            if count==1:
                moves=[];s=state
                while prev[s] is not None:before,which=prev[s];moves.append(which);s=before
                moves.reverse();words=[vertices[i] for i in cycles(state)[0]]
                answer={'dropped_second_K_edge':dropped,'D13':sorted(D),'K11':sorted(D-set(map(tuple,oldc['two_reserves']))),
                        'two_reserves':oldc['two_reserves'],'core40_cut':cut,'C2_words':words,
                        'C2_edges':sorted(edges[i] for i in range(len(edges)) if state>>i&1),
                        'first_local_change':{'removed':sorted(removed),'added':sorted(added)},
                        'rectangle_switch_indexes':moves,'rectangle_switch_base_edges':[old['edges'][i] for i in moves]}
                break
            for i,(h,vv,full) in enumerate(squares):
                present=state&full
                if present not in (h,vv) or present&required:continue
                new=state^full
                if new in prev:continue
                prev[new]=(state,i);serial+=1
                heapq.heappush(queue,(len(cycles(new)),depth+1,serial,new))
        reports.append({'partner':partner,'dropped_second_K_edge':dropped,'initial_cycle_lengths':list(map(len,cycles(initial))),
                        'status':'FOUND' if answer else 'UNKNOWN','nodes':local,'states_seen':len(prev),'certificate':answer})
        if nodes>=NODE_CAP or time.monotonic()-start>=TIME_CAP_SECONDS:break
    result={'reports':reports,'total_nodes':nodes,'elapsed_seconds':time.monotonic()-start,
            'bounds':{'node_cap':NODE_CAP,'wall_time_seconds':TIME_CAP_SECONDS},'input_sha256':hashlib.sha256(inp.read_bytes()).hexdigest(),
            'scope':'Only specified protected three-edge local changes and rectangle switches; every D13 edge in each row and all three intended row1 cuts protected.'}
    (HERE/'C2-second-patch-results-v1.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps([{k:v for k,v in r.items() if k!='certificate'} for r in reports]))

if __name__=='__main__':main()
