"""Bounded exact local path discovery; a found path is independently checked."""
from pathlib import Path
from itertools import product
import hashlib, json, time

HERE=Path(__file__).resolve().parent
BOUNDARY=(0,0,1,1,2)
SECONDS=10.0
NODE_LIMIT=2_000_000


def main():
    started=time.perf_counter()
    states=sorted(''.join(map(str,w)) for w in product(range(4),repeat=5)
                  if all(w[i]!=w[(i+1)%5] and w[i]!=BOUNDARY[i] for i in range(5)))
    assert len(states)==51
    adj=[sum(1<<j for j,z in enumerate(states) if sum(x!=y for x,y in zip(w,z))==1)
         for w in states]
    start=states.index('12303'); end=states.index('13203'); endbit=1<<end
    path=[start]; dead=set(); nodes=0
    class ResourceLimit(Exception): pass
    def bits(mask):
        while mask:
            b=mask & -mask; mask-=b; yield b.bit_length()-1
    def visit(cur,rem):
        nonlocal nodes
        nodes+=1
        if nodes%1024==0 and (nodes>=NODE_LIMIT or time.perf_counter()-started>SECONDS):
            raise ResourceLimit
        if rem==endbit:
            if adj[cur]&endbit: path.append(end); return True
            return False
        key=(cur,rem)
        if key in dead: return False
        avail=rem|(1<<cur)
        degrees={v:(adj[v]&avail).bit_count() for v in bits(rem)}
        if not (adj[cur]&rem) or not degrees[end] or any(
                d<2 for v,d in degrees.items() if v!=end):
            return False
        forced=[v for v in bits(adj[cur]&rem) if v!=end and degrees[v]==2]
        if len(forced)>1 or (degrees[end]==1 and adj[end]&(1<<cur)):
            return False
        reached=0; frontier=1<<cur
        while frontier:
            reached |= frontier
            expansion=0
            for v in bits(frontier): expansion |= adj[v]
            frontier=expansion & avail & ~reached
        if reached!=avail: return False
        candidates=forced if forced else sorted(bits(adj[cur]&rem&~endbit),
                         key=lambda v:((adj[v]&rem).bit_count(),states[v]))
        for v in candidates:
            path.append(v)
            if visit(v,rem&~(1<<v)): return True
            path.pop()
        dead.add(key)
        return False
    try:
        found=visit(start,((1<<len(states))-1)&~(1<<start))
        status='found' if found else 'exhausted-no-path'
    except ResourceLimit:
        found=False; status='resource-limit-unknown'
    words=[states[v] for v in path] if found else None
    if found:
        assert len(words)==51 and len(set(words))==51 and set(words)==set(states)
        assert words[0]=='12303' and words[-1]=='13203'
        # Direct word checks do not rely on the search adjacency bitsets.
        assert all(all(w[i]!=w[(i+1)%5] and int(w[i])!=BOUNDARY[i]
                       for i in range(5)) for w in words)
        assert all(sum(x!=y for x,y in zip(w,z))==1 for w,z in zip(words,words[1:]))
    result={'boundary':'00112','status':status,'path':words,'vertices':len(states),
            'nodes':nodes,'memoized_failed_states':len(dead),'time_limit_seconds':SECONDS,
            'node_limit':NODE_LIMIT,'elapsed_seconds':time.perf_counter()-started,
            'input_sha256':hashlib.sha256((HERE/'literal-input.tex').read_bytes()).hexdigest(),
            'claim':'Hamilton path exists' if found else 'UNKNOWN unless exhaustive search is independently audited'}
    (HERE/'path-results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__=='__main__': main()
