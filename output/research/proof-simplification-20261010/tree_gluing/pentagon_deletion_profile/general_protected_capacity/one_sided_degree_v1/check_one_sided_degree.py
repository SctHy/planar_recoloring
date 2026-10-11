#!/usr/bin/env python3
"""Fixed313 interfaces, new local one-sided degree criterion only."""
from pathlib import Path
from itertools import permutations
from collections import Counter, defaultdict
import hashlib, json, platform, re, time

BASE = Path(__file__).resolve().parent
SOURCE = BASE / "phase6-source.tex"
TEXT = SOURCE.read_text()
LIVE = Path('/Users/huahua815/Downloads/planar_recoloring/planar_recoloring_hamilton_thresholds.tex').read_text()
COLOURS = '0123'
HARD = {'00001', '00112'}


def blocks(text):
    return {m.group(1):m.group(2) for m in re.finditer(r'^% BEGIN ([^\n]+)\n(.*?)^% END \1$', text, re.S|re.M)}


B, LIVE_B = blocks(TEXT), blocks(LIVE)
relevant = [name for name in B if name.startswith(('C1-', 'FHC-', 'POOL-', 'COMMON-', 'PORTS-')) or name in ('FACTOR-00000', 'INTERFACES-ALL', 'CONSTANT-INTERFACE-FAMILIES')]
assert all(B[name] == LIVE_B[name] for name in relevant)
conv = lambda t:t.split('Here is the exact normalization convention.',1)[1].split('\\begin{lemma}',1)[0]
assert conv(TEXT) == conv(LIVE)
assert 'then $\\epsilon=+1,-1$' in conv(TEXT) and 'lexicographic' in conv(TEXT)


def edge(u, v):
    return tuple(sorted((u, v)))


def edgewords(name):
    return {edge(u,v) for u,v in re.findall(r'(?<!\d)([0-3]{5})-([0-3]{5})(?!\d)',B[name])}


def words(name):
    return re.findall(r'(?<!\d)([0-3]{5})(?!\d)',B[name])


def legal(word, boundary):
    return all(word[i] != word[(i+1)%5] and (boundary[i]=='4' or word[i]!=boundary[i]) for i in range(5))


def local_neighbours(word, boundary):
    found=[]
    for i in range(5):
        forbidden = {word[i],word[(i-1)%5],word[(i+1)%5]}
        if boundary[i]!='4':forbidden.add(boundary[i])
        for colour in COLOURS:
            if colour not in forbidden:found.append(word[:i]+colour+word[i+1:])
    return sorted(found)


pools={(name.split('-')[1],int(name.split('-')[2])):edgewords(name) for name in B if name.startswith('POOL-')}
types={t for t,c in pools}
assert len(types)==22
components={}
for name in B:
    if name.startswith(('C1-','FHC-')):components[(name.split('-')[1],0)]=words(name)
constant=words('FACTOR-00000');assert len(constant)==30
components[('00000',0)],components[('00000',1)]=constant[:15],constant[15:]
K={}
for (t,c),pool in pools.items():
    if t in HARD:
        ports=edgewords('COMMON-00001' if t=='00001' else 'PORTS-00112')
        assert len(ports)==13 and len(pool)==2 and pool<=ports
        K[(t,c)]=ports-pool
    else:
        cyc=components[(t,c)]
        assert len(cyc)==len(set(cyc))
        cycle_edges={edge(cyc[i],cyc[(i+1)%len(cyc)]) for i in range(len(cyc))}
        assert pool<=cycle_edges
        K[(t,c)]=cycle_edges-pool
    assert all(legal(u,t) and legal(v,t) and sum(a!=b for a,b in zip(u,v))==1 for u,v in K[(t,c)])


def normalize(boundary):
    for start in range(5):
        for direction in (1,-1):
            for perm in permutations(COLOURS):
                candidate=''.join('4' if boundary[(start+direction*i)%5]=='4' else perm[int(boundary[(start+direction*i)%5])] for i in range(5))
                if candidate in types:return candidate,start,direction,''.join(perm)
    raise AssertionError(boundary)


def restore(word, start, direction, perm):
    out=['']*5
    for i,c in enumerate(word):out[(start+direction*i)%5]=COLOURS[perm.index(c)]
    return ''.join(out)


pattern=r'([0-4]{5}):(\d)\s+([0-4])\s+([0-3])\s+([0-4]{5}):(\d)\s+([0-3]{5})-([0-3]{5})'
existing=re.findall(pattern,B['INTERFACES-ALL'])
assert len(existing)==283
cases=[]
for t,sc,position,colour,nt,tc,u,v in existing:
    actual=t[:int(position)]+colour+t[int(position)+1:]
    assert actual!=t and t[int(position)]!='4'
    normalized,*mapping=normalize(actual)
    assert normalized==nt
    cases.append({'source':t,'source_component':int(sc),'position':int(position),'colour':colour,'actual_target':actual,'target_type':nt,'target_component':int(tc),'mapping':mapping,'origin':'existing283'})
# The manuscript's six parameter families contain these30 interfaces, all hard-target.
for component in (0,1):
    for position in range(5):
        for colour in '123':
            actual='0'*position+colour+'0'*(4-position)
            normalized,*mapping=normalize(actual)
            assert normalized=='00001'
            cases.append({'source':'00000','source_component':component,'position':position,'colour':colour,'actual_target':actual,'target_type':normalized,'target_component':0,'mapping':mapping,'origin':'constant_families30'})
assert len(cases)==313
assert len({(r['source'],r['source_component'],r['position'],r['colour'],r['target_type'],r['target_component']) for r in cases})==313

tic=time.perf_counter()
records=[]
mutation_count=0
for case in cases:
    record=dict(case)
    if case['target_type'] in HARD:
        record.update({'status':'excluded-hard-target','reason':'No whole-graph target Hamilton cycle premise; no seed-row claim examined.'})
        records.append(record)
        continue
    nt,tc=case['target_type'],case['target_component']
    shift,direction,perm=case['mapping']
    restored_states={restore(w,shift,direction,perm) for w in components[(nt,tc)]}
    target_pool={edge(restore(u,shift,direction,perm),restore(v,shift,direction,perm)) for u,v in pools[(nt,tc)]}
    source_k=K[(case['source'],case['source_component'])]
    incidence=defaultdict(set)
    for u,v in source_k:
        incidence[u].add(v);incidence[v].add(u)
    candidates=sorted(set(incidence)&restored_states)
    certificates=[]
    observations=[]
    for state in candidates:
        assert legal(state,case['actual_target'])
        n=local_neighbours(state,case['actual_target'])
        mutation_count+=15
        assert set(n)<=restored_states
        safe=[w for w in n if w in incidence[state] and edge(state,w) not in target_pool]
        d,g=len(n),len(safe)
        assert d>=2 and g<=2
        bound=max(0,2+g-d)
        item={'state':state,'target_neighbours':n,'safe_source_K_neighbours':safe,'target_degree_d':d,'safe_incident_count_g':g,'protected_edge_lower_bound':bound}
        observations.append(item)
        if bound:certificates.append(item)
    baseline=any(c['target_degree_d']==2 for c in certificates)
    degree3=any(c['target_degree_d']==3 and c['safe_incident_count_g']==2 for c in certificates)
    record.update({'status':'covered' if certificates else 'not-covered','candidate_vertices_checked':len(candidates),'certificates':certificates,'all_vertex_observations':observations,'degree2_subcriterion_covered':baseline,'degree3_pair_covered':degree3,'new_beyond_degree2':degree3 and not baseline})
    records.append(record)

eligible=[r for r in records if r['status']!='excluded-hard-target']
covered=[r for r in eligible if r['status']=='covered']
new=[r for r in covered if r['new_beyond_degree2']]
summary={
    'all_interfaces':313,'excluded_hard_targets':len(records)-len(eligible),'eligible_HC_targets':len(eligible),
    'covered_interfaces':len(covered),'uncovered_eligible':len(eligible)-len(covered),
    'degree2_subcriterion_covered':sum(r['degree2_subcriterion_covered'] for r in eligible),
    'degree3_pair_covered':sum(r['degree3_pair_covered'] for r in eligible),
    'new_beyond_degree2':len(new),
    'covered_source_kind':dict(Counter('hard' if r['source'] in HARD else 'Hamilton' for r in covered)),
    'new_source_kind':dict(Counter('hard' if r['source'] in HARD else 'Hamilton' for r in new)),
    'covered_by_source':dict(sorted(Counter(r['source'] for r in covered).items())),
    'new_by_source':dict(sorted(Counter(r['source'] for r in new).items())),
    'certificate_degree_pairs':dict(Counter(f"d{c['target_degree_d']}/g{c['safe_incident_count_g']}" for r in covered for c in r['certificates'])),
    'local_mutation_alternatives_counted':mutation_count
}
result={'status':'PASS','summary':summary,'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'main_relevant_blocks_byte_equal':len(relevant),'normalizer_byte_equal':True,'python':platform.python_version(),'elapsed_seconds':time.perf_counter()-tic,'records':records,'scope':'New one-sided degree criterion only; local neighbour generation, no whole state graph, HC search, old dual-degree rerun or main edit','mathematical_rule':'Every target Hamilton cycle uses at least max(0,2+g-d) safe incident source K edges; fixed local certificates do not prove a new universal interface family.'}
(BASE/'one-sided-degree-results-v1.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'summary':summary,'seconds':result['elapsed_seconds']},indent=2))
