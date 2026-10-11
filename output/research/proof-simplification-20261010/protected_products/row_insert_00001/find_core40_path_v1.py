"""Bounded protected t=1 insertion search in the fixed forty-state core."""
from pathlib import Path
from collections import Counter
import hashlib,json,time

HERE=Path(__file__).resolve().parent
NODE_CAP=1_000_000
TIME_CAP_SECONDS=10.0

def edge(u,v):return tuple(sorted((u,v)))

def main():
    c2_input=HERE/'protected-C2-switch-results-v1.json'
    c2=json.loads(c2_input.read_text())['certificate']
    old=json.loads((HERE/'obstruction-results-v1.json').read_text())
    bad=set(old['Y_internal_endpoints']);vertices=set(old['vertices'])-bad
    raw={tuple(e) for e in old['edges'] if set(e)<=vertices}
    D={tuple(e) for e in c2['D14']}
    row1={edge(u[1:],v[1:]) for u,v in c2['C2_edges'] if u[0]==v[0]=='1'}
    candidates=sorted(e for e in row1-D if set(e)<=vertices)
    start_time=time.monotonic();nodes=0;attempts=[];answer=None;budget=False
    class Budget(Exception):pass

    def degree_closure(cut):
        targets={v:1 if v in cut else 2 for v in vertices}
        available=raw-{cut};forced=set(D)
        while True:
            fdeg=Counter(v for e in forced for v in e);adeg=Counter(v for e in available for v in e)
            if any(fdeg[v]>targets[v] or adeg[v]<targets[v] for v in vertices):return None,'degree contradiction'
            adj={v:{b if a==v else a for a,b in forced if v in (a,b)} for v in vertices}
            unseen=set(vertices)
            while unseen:
                component={min(unseen)};front=list(component)
                while front:
                    u=front.pop()
                    for v in adj[u]-component:component.add(v);front.append(v)
                unseen-=component
                if len(component)>1 and all(fdeg[v]==2 for v in component):return None,'forced cycle'
                if set(cut)<=component and len(component)<len(vertices):return None,'premature forced endpoint path'
            new_available={e for e in available if e in forced or all(fdeg[v]<targets[v] for v in e)}
            new_forced=forced|{e for e in new_available if any(sum(v in z for z in new_available)==targets[v] for v in e)}
            if new_available==available and new_forced==forced:return (available,forced),'pass'
            available,forced=new_available,new_forced

    for cut in candidates:
        closure,reason=degree_closure(cut)
        if closure is None:
            attempts.append({'cut':cut,'closure':reason,'nodes':0,'found':False});continue
        allowed,F=closure;adj={v:{b if a==v else a for a,b in allowed if v in (a,b)} for v in vertices}
        fadj={v:{b if a==v else a for a,b in F if v in (a,b)} for v in vertices}
        left=set(vertices);segments=[]
        while left:
            component={min(left)};front=list(component)
            while front:
                v=front.pop()
                for w in fadj[v]-component:component.add(w);front.append(w)
            left-=component;ends=sorted(v for v in component if len(fadj[v])==1)
            if len(component)==1:path=[min(component)]
            else:
                assert len(ends)==2
                path=[ends[0]]
                while len(path)<len(component):path.append(next(iter(fadj[path[-1]]-set(path))))
            segments.append(path)
        segments.sort(key=lambda p:min(p));count=len(segments);owner={v:i for i,p in enumerate(segments) for v in p}
        START,GOAL=cut;first,last=owner[START],owner[GOAL]
        if first==last:
            assert count==1
            found=segments[first] if segments[first][0]==START else segments[first][::-1]
            answer={'cut':cut,'core40_path':found,'forced_segments':segments};break
        first_path=segments[first] if segments[first][0]==START else segments[first][::-1]
        goal_path=segments[last] if segments[last][-1]==GOAL else segments[last][::-1]
        assert first_path[0]==START and goal_path[-1]==GOAL
        options={i:[p,p[::-1]] if len(p)>1 else [p] for i,p in enumerate(segments)};options[last]=[goal_path]
        chosen=[first_path];dead=set();found=None;before=nodes

        def necessary(current,remaining):
            ids=[i for i in range(count) if remaining>>i&1]
            ports={current}|{p[0] for i in ids for p in options[i]}
            if not adj[current]&ports:return False
            for i in ids:
                p=segments[i]
                if i==last:
                    if not adj[goal_path[0]]&(ports-{goal_path[0]}):return False
                elif len(p)==1:
                    if len(adj[p[0]]&ports)<2:return False
                elif any(not adj[v]&(ports-{p[0],p[-1]}) for v in (p[0],p[-1])):return False
            return True

        def dfs(current,remaining):
            nonlocal nodes,found
            nodes+=1
            if nodes>NODE_CAP or (nodes%1024==0 and time.monotonic()-start_time>TIME_CAP_SECONDS):raise Budget
            if not remaining:
                if current==GOAL:found=[v for p in chosen for v in p];return True
                return False
            key=current,remaining
            if key in dead or not necessary(current,remaining):return False
            choices=[]
            for i in range(count):
                if not remaining>>i&1 or (i==last and remaining!=(1<<i)):continue
                for p in options[i]:
                    if p[0] in adj[current]:
                        future={q[0] for j in range(count) if j!=i and remaining>>j&1 for q in options[j]}
                        choices.append((len(adj[p[-1]]&future),i,p))
            for _,i,p in sorted(choices):
                chosen.append(p)
                if dfs(p[-1],remaining&~(1<<i)):return True
                chosen.pop()
            if len(dead)<200_000:dead.add(key)
            return False
        try:dfs(first_path[-1],((1<<count)-1)&~(1<<first))
        except Budget:budget=True
        attempts.append({'cut':cut,'closure':reason,'forced_segments':count,'nodes':nodes-before,
                         'complete_attempt':not budget,'found':found is not None})
        if found:
            answer={'cut':cut,'core40_path':found,'forced_segments':segments};break
        if budget:break

    if answer:
        path=answer['core40_path'];assert len(path)==40 and set(path)==vertices
        path_edges={edge(u,v) for u,v in zip(path,path[1:])};assert D<=path_edges<=raw
        paths={tuple(e):list(e) for e in old['Y_internal_edges']};paths[tuple(answer['cut'])]=path
        M=set(paths);assert len(set(v for e in M for v in e))==6 and M<=row1 and not M&D
        derived=[]
        for u,v in zip(c2['C2_words'],c2['C2_words'][1:]+c2['C2_words'][:1]):
            derived.append(u);key=edge(u[1:],v[1:])
            if u[0]==v[0]=='1' and key in M:
                p=paths[key];p=p if p[0]==u[1:] else p[::-1]
                assert p[0]==u[1:] and p[-1]==v[1:]
                derived.extend('2'+w for w in p)
        assert len(derived)==132 and set(derived)=={r+v for r in '012' for v in old['vertices']}
        derived_edges={edge(u,v) for u,v in zip(derived,derived[1:]+derived[:1])}
        for u,v in derived_edges:
            assert (u[0]==v[0] and edge(u[1:],v[1:]) in set(map(tuple,old['edges']))) or (abs(int(u[0])-int(v[0]))==1 and u[1:]==v[1:])
        assert all(edge(r+u,r+v) in derived_edges for r in '012' for u,v in D)
        answer.update({'D14':sorted(D),'two_reserves':c2['two_reserves'],'matching_cuts':sorted(M),
                       'derived_C3_words':derived,'all132_states_once':True,'all14_ports_in_each_row':True})
    result={'status':'FOUND' if answer else 'UNKNOWN','answer':answer,'attempts':attempts,'nodes':nodes,
            'elapsed_seconds':time.monotonic()-start_time,'budget_exhausted':budget,
            'bounds':{'node_cap':NODE_CAP,'wall_time_seconds':TIME_CAP_SECONDS},
            'input_sha256':hashlib.sha256(c2_input.read_bytes()).hexdigest(),
            'scope':'Only protected t=1 core40 Hamilton paths whose endpoint pair is a legal unprotected row1 matching cut.',
            'limitations':['UNKNOWN would not exclude insertion with more core paths, other local C2 seeds or another K patch.']}
    (HERE/'core40-path-results-v1.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='answer'}))
    if answer:print(json.dumps({k:v for k,v in answer.items() if k not in ('forced_segments','derived_C3_words')}))

if __name__=='__main__':main()
