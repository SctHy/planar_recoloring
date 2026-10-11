#!/usr/bin/env python3
"""Nonbranching HC degree forcing on14explicit frozen component vertex sets."""
from pathlib import Path
import collections,hashlib,itertools,json,platform,time
HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def edge(a,b):return tuple(sorted((a,b)))
def casekey(r):return (r['source']+':'+str(r['source_component']),r['position'],int(r['colour']),r['target_type']+':'+str(r['target_component']))
def adjacency(V,E):
    a={v:set() for v in V}
    for x,y in E:a[x].add(y);a[y].add(x)
    return a
def forced_cycles(V,F):
    a=adjacency(V,F);todo={v for v in V if a[v]};out=[]
    while todo:
        start=min(todo);seen={start};queue=[start]
        while queue:
            v=queue.pop()
            for w in a[v]:
                if w not in seen:seen.add(w);queue.append(w)
        todo-=seen
        if all(len(a[v])==2 for v in seen):out.append(sorted(seen))
    return out
def closure(V,E):
    available=set(E);forced=set();steps=[]
    for step in range(1,len(E)*2+2):
        a=adjacency(V,available);bad=[v for v in V if len(a[v])<2]
        if bad:return dict(impossible=True,obstruction='available-degree-less-than2',obstruction_vertices=bad,steps=steps,forced_edges=[list(e) for e in sorted(forced)],available_edges=[list(e) for e in sorted(available)])
        forces=[]
        for v in V:
            if len(a[v])==2:
                for w in sorted(a[v]):
                    e=edge(v,w)
                    if e not in forced:forced.add(e);forces.append(dict(edge=list(e),at_vertex=v,available_neighbors=sorted(a[v])))
        f=adjacency(V,forced);bad=[v for v in V if len(f[v])>2]
        if bad:
            steps.append(dict(round=step,new_forced=forces,excluded=[]))
            return dict(impossible=True,obstruction='forced-degree-greater-than2',obstruction_vertices=[dict(state=v,forced_neighbors=sorted(f[v])) for v in bad],steps=steps,forced_edges=[list(e) for e in sorted(forced)],available_edges=[list(e) for e in sorted(available)])
        cycles=forced_cycles(V,forced);proper=[c for c in cycles if len(c)<len(V)]
        if proper:
            steps.append(dict(round=step,new_forced=forces,excluded=[]))
            return dict(impossible=True,obstruction='proper-forced-cycle',obstruction_cycles=proper,steps=steps,forced_edges=[list(e) for e in sorted(forced)],available_edges=[list(e) for e in sorted(available)])
        excludes=[]
        for v in V:
            if len(f[v])==2:
                for w in sorted(a[v]-f[v]):
                    e=edge(v,w)
                    if e in available:available.remove(e);excludes.append(dict(edge=list(e),at_vertex=v,forced_neighbors=sorted(f[v])))
        if not forces and not excludes:
            return dict(impossible=False,obstruction=None,steps=steps,forced_edges=[list(e) for e in sorted(forced)],available_edges=[list(e) for e in sorted(available)],spanning_forced_HC=any(len(c)==len(V) for c in cycles))
        steps.append(dict(round=step,new_forced=forces,excluded=excludes))
    raise AssertionError('Monotone propagation exceeded twice edge count.')
def run():
    assert platform.python_version()=='3.14.6';start=time.monotonic()
    old=json.loads((HERE/'conditional-stars-results.json').read_text());rootpath=HERE/'frozen-root-cut-results.json';root=json.loads(rootpath.read_text());assert root['source_sha256']==old['source_sha256']
    index={tuple(r['case']):r for r in root['cases']};outputs=[]
    for r in old['records']:
        if not r['eligible']:continue
        saved=index[casekey(r['row'])];assert len(saved['directions'])==1
        d=saved['directions'][0];assert d['direction']==('forward' if r['direction']=='F' else 'reverse')
        V=sorted(set().union(*(set(c) for c in d['residual_graph_components'])));assert len(V)==d['state_count']
        boundary=saved['actual_target_boundary'] if r['direction']=='F' else r['row']['source']
        assert all(all(v[i]!=v[(i+1)%5] and (boundary[i]=='4' or v[i]!=boundary[i]) for i in range(5)) for v in V)
        buckets=collections.defaultdict(list)
        for v in V:
            for j in range(5):buckets[(j,v[:j]+'.'+v[j+1:])].append(v)
        E={edge(x,y) for vs in buckets.values() for x,y in itertools.combinations(vs,2)}
        S=set(tuple(e) for e in d['safe_K_edges_deleted']);assert S==set(tuple(e) for e in r['safe_K_edges']) and S<=E
        assert len(E)==d['original_graph_edges'] and len(E-S)==d['residual_edge_count']
        out=closure(V,E-S);outputs.append(dict(case=saved['case'],direction=r['direction'],boundary=boundary,original_first_normalizer=saved['original_first_normalizer'],state_count=len(V),full_edges=len(E),safe_K_deleted=[list(e) for e in sorted(S)],conditional_closure=out))
    assert len(outputs)==14
    result=dict(status='PASS',python=platform.python_version(),root_cut_input_sha256=sha(rootpath),source_sha256=old['source_sha256'],mixed_cases=14,total_explicit_component_states=sum(r['state_count'] for r in outputs),total_explicit_component_edges=sum(r['full_edges'] for r in outputs),positive_cases=sum(r['conditional_closure']['impossible'] for r in outputs),records=outputs,elapsed_seconds=time.monotonic()-start,scope='14existingcompleteHCcomponentvertexsets,Hamming1adjacencyreconstruction,nonbranchingforceddegreeclosure;noHCsearch,nolegalstateenumeration,noold53rerun.')
    (HERE/'full-conditional-closure-results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2))
if __name__=='__main__':run()
