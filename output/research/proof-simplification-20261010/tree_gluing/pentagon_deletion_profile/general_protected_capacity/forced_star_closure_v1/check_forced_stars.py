"""Full legal-state graph, sound degree-two propagation; no cycle-edge input."""
from pathlib import Path
from itertools import product, permutations, combinations
from collections import Counter
import hashlib
import json
import platform
import re
import time

BASE = Path(__file__).resolve().parent
SOURCE = BASE / "phase8-source.tex"
started = time.perf_counter()
src = SOURCE.read_text()
blocks = dict(re.findall(r"% BEGIN ([^\n]+)\n(.*?)% END \1", src, re.S))
standard = sorted({name.split('-')[1] for name in blocks if name.startswith('POOL-')})
hard = {'00001', '00112'}

def edge(a, b):
    return tuple(sorted((a, b)))

def neighbours(v, t):
    out = set()
    for i in range(5):
        forbidden = {v[(i-1) % 5], v[(i+1) % 5], t[i], v[i]}
        for c in '0123':
            if c not in forbidden:
                out.add(v[:i] + c + v[i+1:])
    return out

def legal(v, t):
    return all(v[i] != v[(i+1) % 5] and v[i] != t[i] for i in range(5))

def component_graph(t):
    words = {''.join(w) for w in product('0123', repeat=5) if legal(''.join(w), t)}
    graph = {v: neighbours(v, t) for v in words}
    assert all(n <= words for n in graph.values())
    reached = {min(words)}
    pending = list(reached)
    while pending:
        v = pending.pop()
        for w in graph[v] - reached:
            reached.add(w)
            pending.append(w)
    assert reached == words, (t, len(reached), len(words))
    return graph

def closure(graph):
    allowed = {v: set(ns) for v, ns in graph.items()}
    forced = {v: set() for v in graph}
    passes = 0
    while True:
        passes += 1
        force = set()
        exclude = set()
        for v in sorted(graph):
            assert len(allowed[v]) >= 2 and len(forced[v]) <= 2
            assert forced[v] <= allowed[v]
            if len(allowed[v]) == 2:
                force.update(edge(v, w) for w in allowed[v] - forced[v])
            if len(forced[v]) == 2:
                exclude.update(edge(v, w) for w in allowed[v] - forced[v])
        assert not (force & exclude), 'contradictory new implications'
        if not force and not exclude:
            break
        for v, w in force:
            assert w in allowed[v]
            forced[v].add(w)
            forced[w].add(v)
        for v, w in exclude:
            assert w not in forced[v]
            allowed[v].remove(w)
            allowed[w].remove(v)
    return allowed, forced, passes

def normalize(t):
    for s in range(5):
        for eps in (1, -1):
            for p in permutations('0123'):
                n = ''.join('4' if t[(s+eps*i)%5] == '4' else p[int(t[(s+eps*i)%5])] for i in range(5))
                if n in standard:
                    return n, s, eps, p
    raise AssertionError(('no normalizer', t))

def restore(v, m):
    _, s, eps, p = m
    out = [''] * 5
    for i, c in enumerate(v):
        out[(s+eps*i) % 5] = str(p.index(c))
    return ''.join(out)

def mapped_graph(graph, m):
    return {restore(v, m): {restore(w, m) for w in ns} for v, ns in graph.items()}

pools = {}
for name in blocks:
    if name.startswith('POOL-'):
        _, t, ci = name.split('-')
        pools[t, int(ci)] = {edge(a, b) for a, b in re.findall(r'(?<!\d)([0-3]{5})-([0-3]{5})(?!\d)', blocks[name])}

graphs = {t: component_graph(t) for t in standard if t not in hard | {'00000'}}
closures = {t: closure(g) for t, g in graphs.items()}
graph_summary = {}
for t, g in graphs.items():
    allow, forced, passes = closures[t]
    graph_summary[t] = {
        'vertices': len(g), 'full_edges': sum(map(len, g.values()))//2,
        'forced_edges': sum(map(len, forced.values()))//2,
        'excluded_edges': (sum(map(len, g.values()))-sum(map(len, allow.values())))//2,
        'passes': passes,
    }

parsed = re.findall(r'([0-4]{5}):(\d) ([0-4]) ([0-3]) ([0-4]{5}):(\d) ([0-3]{5})-([0-3]{5})', blocks['INTERFACES-ALL'])
assert len(parsed) == 283
records = []
comparisons = 0
for st, sci, j, q, tt, tci, _a, _b in parsed:
    if st in hard or tt in hard or st == '00000' or tt == '00000':
        continue
    assert sci == tci == '0'
    j = int(j)
    actual = st[:j] + q + st[j+1:]
    m = normalize(actual)
    assert m[0] == tt
    ga, gb = graphs[st], mapped_graph(graphs[tt], m)
    aa, fa, _ = closures[st]
    ab, fb = (mapped_graph(x, m) for x in closures[tt][:2])
    P = pools[st, 0]
    Q = {edge(restore(a, m), restore(b, m)) for a, b in pools[tt, 0]}
    unsafe = P | Q
    common = sorted(ga.keys() & gb.keys())
    assert common
    best0 = 0
    best = 0
    witnesses = []
    for v in common:
        ncommon = ga[v] & gb[v]
        f = sum(edge(v, w) in unsafe for w in ncommon)
        local0 = max(0, 4-len(ga[v])-len(gb[v])+len(ncommon)-f)
        best0 = max(best0, local0)
        pa = [set(z) for z in combinations(sorted(aa[v]), 2) if fa[v] <= set(z)]
        pb = [set(z) for z in combinations(sorted(ab[v]), 2) if fb[v] <= set(z)]
        assert pa and pb
        local = min(sum(edge(v, w) not in unsafe for w in a & b) for a in pa for b in pb)
        comparisons += len(pa)*len(pb)
        assert local >= local0
        if local > best:
            best = local
            witnesses = [{'state': v, 'lower': local, 'base_lower': local0,
                          'source_allowed': sorted(aa[v]), 'target_allowed': sorted(ab[v]),
                          'source_forced': sorted(fa[v]), 'target_forced': sorted(fb[v]),
                          'source_pair_count': len(pa), 'target_pair_count': len(pb)}]
        elif local == best and local > 0:
            witnesses.append({'state': v, 'lower': local, 'base_lower': local0})
    records.append({'source': st, 'position': j, 'new_colour': q,
                    'target': tt, 'actual_target': actual,
                    'normalizer': [m[1], m[2], ''.join(m[3])],
                    'common_vertices': len(common), 'baseline_bound': best0,
                    'closure_bound': best, 'witnesses': witnesses})

assert len(records) == 230
baseline_covered = sum(x['baseline_bound'] > 0 for x in records)
assert baseline_covered == 125
result = {
    'status': 'PASS', 'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    'code_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'python': platform.python_version(), 'interfaces': len(records),
    'full_common_vertices': sum(x['common_vertices'] for x in records),
    'baseline_covered': baseline_covered,
    'closure_covered': sum(x['closure_bound'] > 0 for x in records),
    'newly_covered': [x for x in records if x['closure_bound'] > 0 and x['baseline_bound'] == 0],
    'improved': [x for x in records if x['closure_bound'] > x['baseline_bound']],
    'coverage_by_source': {t: {'eligible': sum(x['source']==t for x in records),
                              'baseline': sum(x['source']==t and x['baseline_bound']>0 for x in records),
                              'closure': sum(x['source']==t and x['closure_bound']>0 for x in records)} for t in graphs},
    'graph_closure': graph_summary, 'local_two_pair_comparisons': comparisons,
    'elapsed_seconds': time.perf_counter()-started, 'records': records,
    'limits': ['Graph-only sound necessity propagation, no HC existence inference or HC search.',
               'Full legal state graphs enumerated independently; selected cycle words/edges not read.',
               'Fixed first normalizers and pools; no pool equivariance assumed.',
               'Finite coverage on230 specified cases, not a uniform symbolic classification.'],
}
(BASE/'forced-star-results.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({k: result[k] for k in ('status','interfaces','full_common_vertices','baseline_covered','closure_covered','local_two_pair_comparisons','elapsed_seconds')}))
print(json.dumps({'newly_covered_count': len(result['newly_covered']), 'improved_count': len(result['improved']), 'coverage_by_source': result['coverage_by_source'], 'graph_closure': graph_summary}))
