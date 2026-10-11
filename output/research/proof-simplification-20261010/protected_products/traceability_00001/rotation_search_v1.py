"""Bounded endpoint-rotation path discovery; no nonexistence inference."""
from pathlib import Path
import json, random, time, hashlib

HERE=Path(__file__).resolve().parent
MAX_STEPS=1_000_000
MAX_SECONDS=10.0
RANDOM_SEED=20261010

def main():
    inp=HERE/'graph-input.json'
    graph=json.loads(inp.read_text())
    states=graph['states']; index={w:i for i,w in enumerate(states)}
    adj=[set() for w in states]
    for a,b in graph['edges']:
        i,j=index[a],index[b];adj[i].add(j);adj[j].add(i)
    rng=random.Random(RANDOM_SEED)
    begin=time.perf_counter();steps=0;best=[];found=None
    while steps<MAX_STEPS and time.perf_counter()-begin<MAX_SECONDS:
        path=[rng.randrange(len(states))]
        rotations_without_growth=0
        for inner in range(1000):
            steps+=1
            if len(path)>len(best):best=path.copy()
            if len(path)==len(states):found=path.copy();break
            visited=set(path)
            options=list(adj[path[-1]]-visited)
            if options:
                rng.shuffle(options)
                options.sort(key=lambda v:len(adj[v]-visited))
                path.append(options[0]);rotations_without_growth=0
            else:
                possible=[i for i in range(len(path)-2) if path[i] in adj[path[-1]]]
                if not possible:break
                i=rng.choice(possible)
                path=path[:i+1]+path[:i:-1]
                rotations_without_growth+=1
                if rotations_without_growth>10*len(states):break
            # Both endpoint choices are legitimate; alternating them avoids
            # retaining an unnecessarily fixed first endpoint.
            if rng.randrange(2):path.reverse()
        if found:break
    literal=None if found is None else [states[i] for i in found]
    if literal is not None:
        assert len(literal)==len(states) and set(literal)==set(states)
        assert all(sum(x!=y for x,y in zip(a,b))==1 for a,b in zip(literal,literal[1:]))
    result={'boundary':'00001','status':'traceable' if literal else 'UNKNOWN',
            'Hamilton_path':literal,'best_length':len(best),
            'best_path':[states[i] for i in best],
            'search':{'maximum_steps':MAX_STEPS,'maximum_seconds':MAX_SECONDS,
                      'steps':steps,'random_seed':RANDOM_SEED,
                      'elapsed_seconds':time.perf_counter()-begin},
            'graph_input_sha256':hashlib.sha256(inp.read_bytes()).hexdigest()}
    (HERE/'rotation-results-v1.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))

if __name__=='__main__':main()
