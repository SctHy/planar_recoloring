"""Exact memoized independent-set recursion on the frozen 44-state graph."""
from pathlib import Path
from functools import lru_cache
import json, time, hashlib

HERE=Path(__file__).resolve().parent
INP=HERE.parents[1]/'protected_products/traceability_00001/graph-input.json'

def main():
    graph=json.loads(INP.read_text()); ws=graph['states']; ix={w:i for i,w in enumerate(ws)}
    adj=[0]*len(ws)
    for u,v in graph['edges']:
        a,b=ix[u],ix[v]; adj[a]|=1<<b; adj[b]|=1<<a
    full=(1<<len(ws))-1
    def components(mask):
        remaining=mask; cc=[]
        while remaining:
            reached=todo=remaining & -remaining
            while todo:
                bit=todo & -todo; todo-=bit
                fresh=adj[bit.bit_length()-1] & remaining & ~reached
                reached|=fresh; todo|=fresh
            cc.append(reached); remaining &= ~reached
        return cc
    nodes=0
    @lru_cache(maxsize=None)
    def solve(mask):
        nonlocal nodes; nodes+=1
        if not mask: return 0,0
        cc=components(mask)
        if len(cc)>1:
            count=chosen=0
            for component in cc:
                c,s=solve(component); count+=c; chosen|=s
            return count,chosen
        # An isolated vertex belongs to a maximum independent set. A leaf
        # may always replace its neighbour, so choosing it is also exact.
        pending=mask; degree=[]
        while pending:
            bit=pending & -pending; pending-=bit; v=bit.bit_length()-1
            d=(adj[v]&mask).bit_count()
            if d<=1:
                count,chosen=solve(mask & ~(bit|adj[v]))
                return count+1,chosen|bit
            degree.append((d,v))
        _,v=max(degree)
        count,chosen=solve(mask & ~(1<<v|adj[v]))
        include=(count+1,chosen|1<<v)
        exclude=solve(mask & ~(1<<v))
        return include if include[0]>=exclude[0] else exclude
    start=time.perf_counter(); alpha,chosen=solve(full); elapsed=time.perf_counter()-start
    independent=[ws[i] for i in range(len(ws)) if chosen>>i & 1]
    assert all(not(adj[i]&chosen) for i in range(len(ws)) if chosen>>i&1)
    result={'graph_input_sha256':hashlib.sha256(INP.read_bytes()).hexdigest(),
            'exact_maximum_independent_set_size':alpha,'witness':independent,
            'recursion_states':nodes,'cache':str(solve.cache_info()),
            'elapsed_seconds':elapsed,'independence_obstruction_to_HP':alpha>23-1,
            'scope':'Exact independence result; no inference of traceability when alpha <= 22.'}
    (HERE/'exact-independence-00001.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
