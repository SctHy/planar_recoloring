"""Bounded exact path discovery with necessary residual cut-vertex pruning."""
from pathlib import Path
import hashlib,json,time

HERE=Path(__file__).resolve().parent
MAX_SECONDS=15.0
MAX_NODES=2_000_000

def main():
    inp=HERE/'graph-input.json';g=json.loads(inp.read_text())
    states=g['states'];index={w:i for i,w in enumerate(states)};n=len(states)
    adj=[0]*n
    for a,b in g['edges']:
        i,j=index[a],index[b];adj[i]|=1<<j;adj[j]|=1<<i
    full=(1<<n)-1;nodes=0;path=[];solution=None;dead=set()
    begin=time.perf_counter();starts=[];budget=False

    class Budget(Exception):pass

    def feasible(current,remaining):
        residual=remaining|(1<<current)
        allowed_end=remaining
        forced_end=None
        left=remaining
        while left:
            bit=left&-left;left-=bit;v=bit.bit_length()-1
            degree=(adj[v]&residual).bit_count()
            if degree==0:return False
            if degree==1:
                if forced_end is not None:return False
                forced_end=v
        # Root the residual DFS at its prescribed path endpoint. Any
        # nonroot cut vertex may have only one separated descendant part;
        # that part must contain the other path endpoint.
        disc=[-1]*n;low=[-1]*n;clock=0;valid=True
        def visit(v,parent):
            nonlocal clock,valid,allowed_end
            disc[v]=low[v]=clock;clock+=1
            subtree=1<<v;separated=[];children=0
            neighbors=adj[v]&residual
            while neighbors:
                bit=neighbors&-neighbors;neighbors-=bit;w=bit.bit_length()-1
                if disc[w]<0:
                    children+=1;child=visit(w,v);subtree|=child
                    low[v]=min(low[v],low[w])
                    if low[w]>=disc[v]:separated.append(child)
                elif w!=parent:low[v]=min(low[v],disc[w])
            if v==current:
                if children>1:valid=False
            else:
                if len(separated)>1:valid=False
                elif separated:allowed_end&=separated[0]
            return subtree
        reached=visit(current,-1)
        if reached!=residual or not valid or not allowed_end:return False
        if forced_end is not None and not (allowed_end>>forced_end&1):return False
        return forced_end

    def dfs(current,remaining):
        nonlocal nodes,solution
        nodes+=1
        if nodes>MAX_NODES or (nodes%1024==0 and time.perf_counter()-begin>MAX_SECONDS):raise Budget
        if not remaining:solution=path.copy();return True
        key=(current,remaining)
        if key in dead:return False
        condition=feasible(current,remaining)
        if condition is False:return False
        choices=adj[current]&remaining;ordered=[]
        while choices:
            bit=choices&-choices;choices-=bit;v=bit.bit_length()-1
            if v==condition and remaining!=bit:continue
            ordered.append(v)
        ordered.sort(key=lambda v:((adj[v]&remaining).bit_count(),v))
        for v in ordered:
            path.append(v)
            if dfs(v,remaining&~(1<<v)):return True
            path.pop()
        if len(dead)<200_000:dead.add(key)
        return False

    try:
        for v in sorted(range(n),key=lambda i:(-adj[i].bit_count(),i)):
            starts.append(states[v]);path[:]=[v]
            if dfs(v,full&~(1<<v)):break
    except Budget:budget=True
    literal=None if solution is None else [states[i] for i in solution]
    if literal:
        assert len(literal)==n and set(literal)==set(states)
        assert all(sum(x!=y for x,y in zip(a,b))==1 for a,b in zip(literal,literal[1:]))
    result={'boundary':'00001','status':'traceable' if literal else 'UNKNOWN',
            'Hamilton_path':literal,'nodes':nodes,'memoized_failed_states':len(dead),
            'starts_tried':starts,'budget_exhausted':budget,
            'maximum_seconds':MAX_SECONDS,'maximum_nodes':MAX_NODES,
            'elapsed_seconds':time.perf_counter()-begin,
            'graph_input_sha256':hashlib.sha256(inp.read_bytes()).hexdigest()}
    (HERE/'articulation-results-v2.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))

if __name__=='__main__':main()
