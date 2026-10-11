"""Bounded protected path search after contracting forced paths in the fixed 47-core."""
from pathlib import Path
import hashlib,json,re,time

HERE=Path(__file__).resolve().parent
MAX_NODES=1_000_000
MAX_SECONDS=10.0
START='21201';GOAL='23201'

def main():
    inp=HERE/'structural-results-v1.json';screen=json.loads(inp.read_text())
    core=screen['core_vertices'];oldrow=set(map(tuple,screen['second_row_edges']))
    K=set(map(tuple,screen['K']));cut=tuple(sorted((START,GOAL)))
    begin=time.perf_counter();nodes=0;attempts=[];answer=None;budget=False
    class Budget(Exception):pass
    candidates=sorted((r for r in screen['reserve_pair_screens'] if r['structurally_feasible']),
                      key=lambda r:-len(r['forced_edges']))
    for result in candidates:
        F=set(map(tuple,result['forced_edges']));allowed=set(map(tuple,result['allowed_edges']))
        assert cut in F&oldrow and cut not in K|set(map(tuple,result['reserves']))
        F.remove(cut);allowed.remove(cut)
        adj={v:{b if a==v else a for a,b in allowed if v in (a,b)} for v in core}
        fadj={v:{b if a==v else a for a,b in F if v in (a,b)} for v in core}
        left=set(core);segments=[]
        while left:
            component={min(left)};front=list(component)
            while front:
                v=front.pop()
                for w in fadj[v]-component:component.add(w);front.append(w)
            left-=component
            ends=sorted(v for v in component if len(fadj[v])==1)
            if len(component)==1:path=[min(component)]
            else:
                assert len(ends)==2
                path=[ends[0]]
                while len(path)<len(component):path.append(next(iter(fadj[path[-1]]-set(path))))
            segments.append(path)
        segments.sort(key=lambda p:min(p));count=len(segments)
        owner={v:i for i,p in enumerate(segments) for v in p}
        first,last=owner[START],owner[GOAL];assert first!=last
        start_path=segments[first] if segments[first][0]==START else segments[first][::-1]
        assert start_path[0]==START
        goal_path=segments[last] if segments[last][-1]==GOAL else segments[last][::-1]
        assert goal_path[-1]==GOAL
        options={i:[p,p[::-1]] if len(p)>1 else [p] for i,p in enumerate(segments)}
        options[last]=[goal_path]
        dead=set();chosen=[start_path];found=None;local_start=nodes

        def necessary(current,remaining):
            ids=[i for i in range(count) if remaining>>i&1]
            ports={current}
            for i in ids:
                ports|={p[0] for p in options[i]}
            if not adj[current]&ports:return False
            for i in ids:
                p=segments[i]
                if i==last:
                    if not adj[goal_path[0]]&(ports-{goal_path[0]}):return False
                elif len(p)==1:
                    if len(adj[p[0]]&ports)<2:return False
                elif any(not adj[v]&(ports-{p[0],p[-1]}) for v in (p[0],p[-1])):
                    return False
            return True

        def dfs(current,remaining):
            nonlocal nodes,found
            nodes+=1
            if nodes>MAX_NODES or (nodes%1024==0 and time.perf_counter()-begin>MAX_SECONDS):raise Budget
            if not remaining:
                if current==GOAL:found=[v for p in chosen for v in p];return True
                return False
            key=(current,remaining)
            if key in dead or not necessary(current,remaining):return False
            choices=[]
            for i in range(count):
                if not remaining>>i&1 or (i==last and remaining!=(1<<i)):continue
                for p in options[i]:
                    if p[0] in adj[current]:
                        future_ports={q[0] for j in range(count) if j!=i and remaining>>j&1 for q in options[j]}
                        choices.append((len(adj[p[-1]]&future_ports),i,p))
            choices.sort(key=lambda item:(item[0],item[1],item[2]))
            for degree,i,p in choices:
                chosen.append(p)
                if dfs(p[-1],remaining&~(1<<i)):return True
                chosen.pop()
            if len(dead)<200_000:dead.add(key)
            return False
        try:dfs(start_path[-1],((1<<count)-1)&~(1<<first))
        except Budget:budget=True
        attempts.append({'reserves':result['reserves'],'forced_segment_count':count,
                         'nodes':nodes-local_start,'memoized_failed_states':len(dead),
                         'complete_discovery_attempt':not budget,'found':found is not None})
        if found is not None:
            assert len(found)==47 and set(found)==set(core) and found[0]==START and found[-1]==GOAL
            path_edges={tuple(sorted(e)) for e in zip(found,found[1:])}
            protected=K|set(map(tuple,result['reserves']))
            assert protected<=path_edges and all(e in allowed for e in path_edges)
            answer={'reserves':result['reserves'],'core_path':found,'cut_edge':cut,
                    'protected_edges':sorted(protected),'forced_segments':segments}
            break
        if budget:break

    if answer:
        text=(HERE/'literal-input.tex').read_text()
        b=re.search('% BEGIN C2-00112\n(.*?)% END C2-00112',text,re.S).group(1)
        words=re.findall(r'\b[01][0-3]{5}\b',b)
        paths={tuple(sorted((a,z))):[a,z] for a,z in screen['original_leaf_pairs'].items()}
        paths[cut]=answer['core_path'];assert len(paths)==3
        M=set(paths);assert len({v for e in M for v in e})==6 and M<=oldrow
        derived=[]
        for a,b in zip(words,words[1:]+words[:1]):
            derived.append(a)
            key=tuple(sorted((a[1:],b[1:])))
            if a[0]==b[0]=='1' and key in M:
                p=paths[key]
                if p[0]!=a[1:]:p=p[::-1]
                assert p[0]==a[1:] and p[-1]==b[1:]
                derived.extend('2'+v for v in p)
        vertices=screen['vertices']
        assert len(derived)==153 and set(derived)=={str(i)+v for i in range(3) for v in vertices}
        derived_edges={tuple(sorted(e)) for e in zip(derived,derived[1:]+derived[:1])}
        for a,b in derived_edges:
            if a[0]==b[0]:assert sum(x!=y for x,y in zip(a[1:],b[1:]))==1
            else:assert abs(int(a[0])-int(b[0]))==1 and a[1:]==b[1:]
        for e in answer['protected_edges']:
            for row in range(3):assert tuple(str(row)+v for v in e) in derived_edges
        answer['matching_cuts']=sorted(M);answer['derived_C3']=derived
        answer['all_153_states_once']=True;answer['all_cartesian_cycle_edges_legal']=True
        answer['all_13_protected_edges_in_all_three_rows']=True
    output={'status':'found' if answer else 'UNKNOWN','answer':answer,'attempts':attempts,
            'nodes':nodes,'maximum_nodes':MAX_NODES,'maximum_seconds':MAX_SECONDS,
            'elapsed_seconds':time.perf_counter()-begin,'budget_exhausted':budget,
            'structural_input_sha256':hashlib.sha256(inp.read_bytes()).hexdigest(),
            'scope':'fixed protected 47-state core; all old K edges and two old reserves enforced throughout'}
    (HERE/'core-path-results-v1.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k!='answer'}))
    if answer:print(json.dumps({k:v for k,v in answer.items() if k not in ('derived_C3','forced_segments')}))

if __name__=='__main__':main()
