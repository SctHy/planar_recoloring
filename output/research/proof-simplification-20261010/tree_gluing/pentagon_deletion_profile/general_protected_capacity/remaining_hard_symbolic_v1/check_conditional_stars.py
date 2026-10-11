#!/usr/bin/env python3
"""Extract conditional hard-K-avoidance forcing from14frozen local-star sets."""
from pathlib import Path
import collections,hashlib,json,platform,re
HERE=Path(__file__).resolve().parent
PARENT=HERE.parent
MAIN=HERE.parents[6]/'planar_recoloring_hamilton_thresholds.tex'
HARD={'00001','00112'}
KEYS=('source','source_component','position','colour','target_type','target_component')
def identity(a):return tuple(a[k] for k in KEYS)
def edge(a,b):return tuple(sorted((a,b)))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run():
    assert platform.python_version()=='3.14.6'
    source=HERE/'frozen-main.tex';assert sha(source)=='b7a048389c00d075d733581bc98fbfd397765b384777e5959076264ab0dbd557'
    data_path=HERE/'frozen-symmetric-one-sided.json';assert sha(data_path)=='6d16370fa156d7d739a6d8c2bec98ec75b8dbc640cb39183db1a89cb29499876'
    a=json.loads(data_path.read_text());index={identity(r['interface']):r for r in a['records']};assert len(index)==313
    body=source.read_text().split('% BEGIN INTERFACES-ALL\n')[1].split('% END INTERFACES-ALL')[0]
    pattern=r'\b([0-4]{5}):(\d)\s+([0-4])\s+([0-3])\s+([0-4]{5}):(\d)\s+([0-3]{5})-([0-3]{5})\b'
    rows=[]
    for m in re.finditer(pattern,body):
        d=dict(source=m[1],source_component=int(m[2]),position=int(m[3]),colour=m[4],target_type=m[5],target_component=int(m[6]),old_edge=[m[7],m[8]])
        rows.append(d)
    assert len(rows)==47
    selected=[r for r in rows if r['source'] in HARD or r['target_type'] in HARD];assert len(selected)==19
    outputs=[]
    for row in selected:
        original=index[identity(row)];i=original['interface'];src_hard=i['source'] in HARD;tar_hard=i['target_type'] in HARD
        if src_hard and tar_hard:
            outputs.append(dict(row=row,interface=i,kind='hard-hard',eligible=False));continue
        direction='F' if src_hard else 'R';record=original['forward_fixed_source_K' if direction=='F' else 'reverse_fixed_restored_target_K']
        assert record['covered'] is False
        obs=record['all_local_observations'];known={o['state']:o for o in obs};assert len(known)==len(obs)<=20
        safe=set();forced=set();force_sources={};pointwise=[]
        for o in obs:
            v=o['state'];neighbors=set(o['HC_side_neighbours']);good=set(o['safe_fixed_K_neighbours']);d=o['HC_side_degree'];g=o['safe_incident_count']
            assert len(neighbors)==d and len(good)==g and good<=neighbors and d-g>=2
            safe.update(edge(v,w) for w in good)
            if d-g==2:
                for w in neighbors-good:
                    e=edge(v,w);forced.add(e);force_sources.setdefault(e,[]).append(v)
                pointwise.append(dict(state=v,full_degree=d,safe_K_degree=g,forced_neighbors=sorted(neighbors-good)))
        for u,v in safe:
            assert u in known and v in known and v in known[u]['safe_fixed_K_neighbours'] and u in known[v]['safe_fixed_K_neighbours']
        adj=collections.defaultdict(set)
        for u,v in forced:adj[u].add(v);adj[v].add(u)
        conflicts=[dict(vertex=v,forced_neighbors=sorted(ns)) for v,ns in sorted(adj.items()) if len(ns)>2]
        todo=set(adj);cycles=[]
        while todo:
            start=min(todo);seen={start};queue=[start]
            while queue:
                v=queue.pop()
                for w in adj[v]:
                    if w not in seen:seen.add(w);queue.append(w)
            todo-=seen
            if all(len(adj[v])==2 for v in seen):
                assert len(seen)<15 # Every printed HC component has at least15states.
                cycles.append(dict(vertices=sorted(seen),edges=[list(e) for e in sorted(forced) if e[0] in seen]))
        outputs.append(dict(row=row,interface=i,kind='mixed',eligible=True,direction=direction,observation_count=len(obs),safe_K_edges=[list(e) for e in sorted(safe)],conditional_forced_stars=pointwise,forced_edges=[dict(edge=list(e),forcing_states=force_sources[e]) for e in sorted(forced)],degree_conflicts=conflicts,proper_forced_cycles=cycles,conditional_impossibility=bool(conflicts or cycles)))
    mixed=[o for o in outputs if o['eligible']];assert len(mixed)==14
    result=dict(status='PASS',python=platform.python_version(),source_sha256=sha(source),saved_observation_sha256=sha(data_path),remaining_records=47,hard_related19=len(outputs),mixed14=len(mixed),hardhard5=5,observations_read=sum(o['observation_count'] for o in mixed),conditional_positive_cases=sum(o['conditional_impossibility'] for o in mixed),records=outputs,scope='Only14savedactualmixedcases;conditionalavoidsafeKforcingnotintrinsicfullgraphclosure;noHCsearchornewneighbours.')
    target=HERE/'conditional-stars-results.json';target.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2))
if __name__=='__main__':run()
