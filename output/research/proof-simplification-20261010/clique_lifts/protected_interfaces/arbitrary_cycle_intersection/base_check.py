"""Exact local set/degree/group checks. No Hamilton search is performed."""
from pathlib import Path
from itertools import product, permutations
from collections import Counter
import hashlib, json, re, sys, time

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[4] / "planar_recoloring_hamilton_thresholds.tex"
STANDARD = ("00000", "00001", "00011", "00012", "00101", "00102",
            "00112", "00121", "00123", "01012", "01023", "00004",
            "00014", "00104", "00114", "00124", "01014", "01024",
            "01104", "01124", "01204", "01234")
HARD = {"00001", "00112"}
PERMS = tuple(permutations(range(4)))


def edge(a, b):
    return tuple(sorted((a, b)))


def cycle_edges(words):
    assert len(words) == len(set(words))
    return {edge(a, b) for a, b in zip(words, words[1:] + words[:1])}


def word_tuple(w):
    return tuple(map(int, w))


def word_text(w):
    return ''.join(map(str, w))


def transform(w, g):
    s, eps, p = g
    return tuple(4 if w[(s + eps*i) % 5] == 4 else p[w[(s + eps*i) % 5]]
                 for i in range(5))


def normalize(t):
    for s in range(5):
        for eps in (1, -1):
            for p in PERMS:
                n = word_text(transform(t, (s, eps, p)))
                if n in STANDARD:
                    return n, (s, eps, p)
    raise AssertionError(t)


def restore(w, g):
    s, eps, p = g
    pinv = tuple(p.index(i) for i in range(4))
    out = [None]*5
    for j in range(5):
        out[(s + eps*j) % 5] = pinv[w[j]]
    return tuple(out)


def main():
    started = time.perf_counter()
    frozen = HERE / "literal-input.tex"
    if not frozen.exists():
        src = SOURCE.read_text()
        blocks = re.findall(r"% BEGIN ([A-Z0-9-]+)\n(.*?)% END \1", src, re.S)
        frozen.write_text(''.join(f'% BEGIN {name}\n{body}% END {name}\n'
                                  for name, body in blocks))
        (HERE / "source-provenance.json").write_text(json.dumps({
            "source_path": str(SOURCE),
            "source_sha256": hashlib.sha256(src.encode()).hexdigest(),
            "frozen_sha256": hashlib.sha256(frozen.read_bytes()).hexdigest()
        }, indent=2)+'\n')
    text = frozen.read_text()
    blocks = dict(re.findall(r"% BEGIN ([A-Z0-9-]+)\n(.*?)% END \1", text, re.S))
    def words(name, width=5):
        return [word_tuple(w) for w in re.findall(rf'\b[0-3]{{{width}}}\b', blocks[name])]
    def edges(name):
        return {edge(word_tuple(a), word_tuple(b))
                for a,b in re.findall(r'\b([0-3]{5})-([0-3]{5})\b', blocks[name])}

    states, adj, raw_edges = {}, {}, {}
    cycles, retained, pools = {}, {}, {}
    constant = words("FACTOR-00000")
    assert len(constant) == 30
    for t in STANDARD:
        all_states = {w for w in product(range(4), repeat=5)
                      if all(w[i] != w[(i+1)%5] for i in range(5))
                      and all(t[i] == '4' or w[i] != int(t[i]) for i in range(5))}
        components = [set(constant[:15]), set(constant[15:])] if t == '00000' else [all_states]
        if t == '00000':
            assert set.union(*components) == all_states and not components[0] & components[1]
        for index, vs in enumerate(components):
            key = f'{t}:{index}'
            states[key] = vs
            aa = {w: set() for w in vs}
            for w in vs:
                for i in range(5):
                    for c in range(4):
                        if c == w[i]: continue
                        z = w[:i]+(c,)+w[i+1:]
                        if z in vs: aa[w].add(z)
            adj[key] = aa
            es = {edge(w,z) for w in vs for z in aa[w]}
            raw_edges[key] = es
            if t == '00000':
                ee = cycle_edges(constant[index*15:(index+1)*15])
            elif t in HARD:
                ee = edges('COMMON-00001' if t == '00001' else 'PORTS-00112')
                seednames = ('PC2-00001', 'PC3-00001') if t == '00001' else ('C2-00112', 'C3-00112')
                for name, rows in zip(seednames, (2,3)):
                    ww = words(name, 6)
                    se = cycle_edges(ww)
                    assert len(ww) == rows*len(vs)
                    assert set(ww) == {(row,)+w for row in range(rows) for w in vs}
                    assert all(sum(a[i]!=b[i] for i in range(6)) == 1
                               and (a[0]==b[0] or abs(a[0]-b[0])==1)
                               for a,b in se)
                    for row in range(rows):
                        internal = {edge(a[1:], b[1:]) for a,b in se if a[0] == b[0] == row}
                        assert ee <= internal
            else:
                ww = words(('FHC-' if '4' in t else 'C1-')+t)
                assert set(ww) == vs
                ee = cycle_edges(ww)
                cycles[key] = ee
            pp = edges(f'POOL-{t}-{index}')
            assert len(pp) == (7 if t in HARD else 8)
            assert pp <= ee <= es
            pools[key] = pp
            retained[key] = ee - pp
            seen = {next(iter(vs))}
            todo = list(seen)
            while todo:
                u=todo.pop()
                for z in aa[u] - seen: seen.add(z); todo.append(z)
            assert seen == vs

    records = re.findall(r'([0-4]{5}:[01])\s+([0-4])\s+([0-3])\s+([0-4]{5}:[01])\s+([0-3]{5})-([0-3]{5})', blocks['INTERFACES-ALL'])
    assert len(records) == 313
    details=[]
    for source, pos_s, new_s, target, a_s, b_s in records:
        pos, new = int(pos_s), int(new_s)
        oldt = word_tuple(source.split(':')[0])
        assert oldt[pos] not in (new,4)
        changed = oldt[:pos]+(new,)+oldt[pos+1:]
        nt, mapping = normalize(changed)
        assert nt == target.split(':')[0]
        target_states = {restore(w,mapping) for w in states[target]}
        target_edges = {edge(restore(a,mapping), restore(b,mapping)) for a,b in raw_edges[target]}
        target_k = {edge(restore(a,mapping), restore(b,mapping)) for a,b in retained[target]}
        target_pool = {edge(restore(a,mapping), restore(b,mapping)) for a,b in pools[target]}
        target_degree = {restore(w,mapping):len(z) for w,z in adj[target].items()}
        common_states = states[source] & target_states
        common_edges = raw_edges[source] & target_edges
        common_k = retained[source] & target_k
        witness = edge(word_tuple(a_s), word_tuple(b_s))
        assert witness in common_k and common_states
        low_states = {w for w in common_states if len(adj[source][w]) <= 2 and target_degree[w] <= 2}
        low_edges = {e for e in common_edges if set(e) & low_states}
        low_retained = low_edges & common_k
        is_hh = source[:5] not in HARD and target[:5] not in HARD
        exact_two = {w for w in common_states if len(adj[source][w]) == target_degree[w] == 2}
        hh_forced = {e for e in common_edges if set(e) & exact_two} if is_hh else set()
        hh_protected_forced = hh_forced & common_k
        # The forcing endpoints need not be the same on the two sides.
        broader_hh_forced = {e for e in common_edges
                            if any(len(adj[source][w]) == 2 for w in e)
                            and any(target_degree[w] == 2 for w in e)} if is_hh else set()
        details.append({
            'source':source,'position':pos,'new_excluded':new,'target':target,
            'normalization':{'shift':mapping[0],'orientation':mapping[1],'permutation':mapping[2]},
            'common_states':len(common_states),'common_edges':len(common_edges),'common_K':len(common_k),
            'dual_low_states':len(low_states),'dual_low_edges':len(low_edges),
            'dual_low_retained_edges':len(low_retained),'both_Hamilton_components':is_hh,
            'forced_HH_edges':len(hh_forced),'protected_forced_HH_edges':len(hh_protected_forced),
            'broader_forced_HH_edges':len(broader_hh_forced),
            'broader_protected_forced_HH_edges':len(broader_hh_forced & common_k),
            'low_edges_lost_to_source_pool':len(low_edges & pools[source]),
            'low_edges_lost_to_target_pool':len(low_edges & target_pool),
            'first_low_state':word_text(min(low_states)) if low_states else None,
            'first_dual_low_edge':[word_text(w) for w in min(low_edges)] if low_edges else None,
            'first_dual_low_retained_edge':[word_text(w) for w in min(low_retained)] if low_retained else None,
            'witness':[a_s,b_s]
        })

    # Boundary/component/K stabilizers; preserving boundary alone is insufficient.
    stabilizers={}
    for source, vs in states.items():
        t=word_tuple(source[:5])
        boundary_group=[]
        state_group=[]
        k_group=[]
        for s in range(5):
            for eps in (1,-1):
                for p in PERMS:
                    g=(s,eps,p)
                    if transform(t,g) != t: continue
                    boundary_group.append(g)
                    if {transform(w,g) for w in vs} != vs: continue
                    state_group.append(g)
                    if {edge(transform(a,g),transform(b,g)) for a,b in retained[source]} == retained[source]:
                        k_group.append(g)
        source_records=[d for d in details if d['source']==source]
        orbit_representatives=set()
        for d in source_records:
            parameter_orbit=[]
            for s,eps,p in k_group:
                np=(eps*(d['position']-s))%5
                parameter_orbit.append((np,p[d['new_excluded']]))
            orbit_representatives.add(min(parameter_orbit))
        stabilizers[source]={
            'boundary_order':len(boundary_group),'component_order':len(state_group),
            'K_order':len(k_group),'K_elements':k_group,
            'interface_records':len(source_records),
            'parameter_orbits_ignoring_target_K':len(orbit_representatives)
        }

    summary={
        'evidence':'exact-check of fixed local objects; no universal extension inferred',
        'input_sha256':hashlib.sha256(frozen.read_bytes()).hexdigest(),
        'component_types':len(states),'interface_records':len(details),
        'dual_low_state_interfaces':sum(bool(d['dual_low_states']) for d in details),
        'dual_low_edge_interfaces':sum(bool(d['dual_low_edges']) for d in details),
        'dual_low_retained_interfaces':sum(bool(d['dual_low_retained_edges']) for d in details),
        'HH_interfaces':sum(d['both_Hamilton_components'] for d in details),
        'HH_forced_interfaces':sum(bool(d['forced_HH_edges']) for d in details),
        'HH_protected_forced_interfaces':sum(bool(d['protected_forced_HH_edges']) for d in details),
        'HH_broader_forced_interfaces':sum(bool(d['broader_forced_HH_edges']) for d in details),
        'HH_broader_protected_forced_interfaces':sum(bool(d['broader_protected_forced_HH_edges']) for d in details),
        'nontrivial_K_stabilizers':{k:v['K_order'] for k,v in stabilizers.items() if v['K_order']>1},
        'parameter_orbits_ignoring_target_K':sum(v['parameter_orbits_ignoring_target_K'] for v in stabilizers.values()),
        'full_interface_orbits_under_source_K_stabilizer':len(details) if all(v['K_order']==1 for v in stabilizers.values()) else 'not-computed',
        'first_no_dual_low_edge':next((d for d in details if not d['dual_low_edges']),None),
        'first_HH_no_forced_edge':next((d for d in details if d['both_Hamilton_components'] and not d['forced_HH_edges']),None),
        'first_HH_pool_loss':next((d for d in details if d['forced_HH_edges'] and not d['protected_forced_HH_edges']),None),
        'first_HH_no_broader_forced_edge':next((d for d in details if d['both_Hamilton_components'] and not d['broader_forced_HH_edges']),None),
        'by_source':{key:{
            'interfaces':sum(d['source']==key for d in details),
            'dual_low_edges':sum(d['source']==key and bool(d['dual_low_edges']) for d in details),
            'dual_low_retained':sum(d['source']==key and bool(d['dual_low_retained_edges']) for d in details)
        } for key in states},
        'elapsed_seconds':time.perf_counter()-started
    }
    (HERE/'results.json').write_text(json.dumps({'summary':summary,'interfaces':details,'stabilizers':stabilizers},indent=2)+'\n')
    print(json.dumps(summary))


if __name__=='__main__': main()
