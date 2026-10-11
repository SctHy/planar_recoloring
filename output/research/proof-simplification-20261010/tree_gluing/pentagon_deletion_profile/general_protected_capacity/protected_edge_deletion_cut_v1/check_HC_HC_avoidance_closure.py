"""New necessary closure AFTER deleting fixed safeK, limited to28HC-HC.

This differs from the archived intrinsic graph closure; no HC search is used.
"""
from pathlib import Path
import json
import time
import platform
import hashlib
import independent_source_reader as R
from fixed_k_source_reader import ActualSource, HARD
from check_deletion_cuts import components

BASE = Path(__file__).resolve().parent

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def closure(H):
    allowed = {v: set(N) for v, N in H.items()}
    forced = {v: set() for v in H}
    trace = []
    while True:
        for v in sorted(H):
            if len(allowed[v]) < 2:
                return {'obstruction': 'allowed-degree-below-two', 'vertex': v, 'allowed': sorted(allowed[v]), 'trace': trace}
            if len(forced[v]) > 2:
                return {'obstruction': 'three-forced-edges-at-one-vertex', 'vertex': v, 'forced': sorted(forced[v]), 'trace': trace}
            assert forced[v] <= allowed[v]
        for part in components(forced):
            if len(part) > 2 and len(part) < len(H) and all(len(forced[v]) == 2 for v in part):
                return {'obstruction': 'proper-forced-cycle', 'vertices': part, 'edges': sorted({R.edge(v, w) for v in part for w in forced[v]}), 'trace': trace}
        force = set()
        exclude = set()
        reasons = []
        for v in sorted(H):
            if len(allowed[v]) == 2 and allowed[v] != forced[v]:
                new = {R.edge(v, w) for w in allowed[v] - forced[v]}
                force.update(new)
                reasons.append({'vertex': v, 'rule': 'only-two-allowed', 'edges': sorted(new)})
            if len(forced[v]) == 2 and allowed[v] != forced[v]:
                new = {R.edge(v, w) for w in allowed[v] - forced[v]}
                exclude.update(new)
                reasons.append({'vertex': v, 'rule': 'two-forced-exclude-others', 'edges': sorted(new)})
        if force & exclude:
            return {'obstruction': 'simultaneously-forced-and-excluded', 'edges': sorted(force & exclude), 'last_implications': reasons, 'trace': trace}
        if not force and not exclude:
            # A fully forced spanning cycle is an actual avoiding HC, without search.
            full_cycle = len(components(forced)) == 1 and all(len(forced[v]) == 2 for v in H)
            return {'obstruction': None, 'fully_forced_avoiding_HC': full_cycle,
                    'forced_edges': sorted({R.edge(v, w) for v in H for w in forced[v]}),
                    'allowed_edges': sorted({R.edge(v, w) for v in H for w in allowed[v]}), 'trace': trace}
        trace.append({'force': sorted(force), 'exclude': sorted(exclude), 'reasons': reasons})
        for v, w in force:
            assert w in allowed[v]
            forced[v].add(w); forced[w].add(v)
        for v, w in exclude:
            assert w not in forced[v]
            allowed[v].remove(w); allowed[w].remove(v)

def main():
    assert not (BASE / 'HC-HC-avoidance-closure-results.json').exists(), 'Preserve executed results'
    manifest = json.loads((BASE / 'input-manifest.json').read_text())
    for item in manifest['files']:
        assert sha(BASE / item['path']) == item['sha256']
    start = time.perf_counter()
    current = R.marked((BASE / 'phase10-source.tex').read_text())
    ref = R.marked((BASE / 'reference-phase9.tex').read_text())
    prior = json.loads((BASE / 'prior-independent125-results.json').read_text())
    source = ActualSource(current, ref, prior['component_checks'])
    rows = [(key, edge) for key, edge in R.interfaces(current['INTERFACES-ALL']) if key[0][:5] not in HARD and key[3][:5] not in HARD]
    assert len(rows) == 28
    results = []
    for key, old_edge in rows:
        sk, j, q, tk = key
        t, sc = sk.split(':'); target, tc = tk.split(':')
        boundary = t[:j] + str(q) + t[j+1:]
        normalized, mapping = source.first_normalizer(boundary)
        assert normalized == target
        V, E, P, Ks, shc = source.component(t, int(sc))
        targetV, targetE, targetP, targetK, thc = source.component(target, int(tc))
        assert shc and thc
        Ns = {v: R.neighbours(v, t) for v in V}
        targetN = {v: R.neighbours(v, target) for v in targetV}
        Nt = {R.restore(v, mapping): {R.restore(w, mapping) for w in targetN[v]} for v in targetV}
        Q = {R.edge(R.restore(a, mapping), R.restore(b, mapping)) for a, b in targetP}
        Kt = {R.edge(R.restore(a, mapping), R.restore(b, mapping)) for a, b in targetK}
        directions = []
        for direction, N, K, pool in [('forward', Nt, Ks, Q), ('reverse', Ns, Kt, P)]:
            assert all(ns <= set(N) for ns in N.values())
            edges = {R.edge(v, w) for v in N for w in N[v]}
            safe = (K & edges) - pool
            H = {v: {w for w in N[v] if R.edge(v, w) not in safe} for v in N}
            assert min(map(len, H.values())) >= 2
            answer = closure(H)
            answer['direction'] = direction
            answer['safe_K_edges_deleted'] = sorted(safe)
            answer['state_count'] = len(H)
            if answer['obstruction'] is None and answer['fully_forced_avoiding_HC']:
                forced_edges = {tuple(e) for e in answer['forced_edges']}
                answer['avoiding_HC_contains_HC_side_pool'] = pool <= forced_edges
            directions.append(answer)
        results.append({'case': key, 'original_printed_edge': old_edge,
            'first_normalizer': [mapping[0], mapping[1], list(mapping[2])], 'directions': directions,
            'positive_avoidance_obstruction': any(d['obstruction'] is not None for d in directions)})
    positive = [r for r in results if r['positive_avoidance_obstruction']]
    cuts = json.loads((BASE / 'cut-results.json').read_text())
    cut_keys = {tuple(c['case']) for c in cuts['cases'] if c['positive_cut_obstruction']}
    closure_keys = {tuple(c['case']) for c in positive}
    output = {'status': 'EXACT_28_HC_HC_AVOIDANCE_CLOSURE_COMPLETE',
        'runtime': {'python': platform.python_version(), 'seconds': time.perf_counter() - start},
        'source_sha256': sha(BASE / 'phase10-source.tex'), 'script_sha256': sha(Path(__file__)),
        'cases_checked': 28, 'directions_checked': 56,
        'positive_cases': len(positive), 'cut_positive_cases': len(cut_keys),
        'additional_positive_beyond_cut_cases': sorted(closure_keys-cut_keys),
        'avoiding_fully_forced_HC_directions': sum(d['obstruction'] is None and d['fully_forced_avoiding_HC'] for c in results for d in c['directions']),
        'cases': results, 'HC_search': False, 'main_modified': False,
        'scope': 'Necessary-HC closure ongraph AFTER safeK deletion,not the old intrinsic closure. Obstructions prove avoiding HC impossible; non-obstruction proves nothing unless a fullyforced spanningcycle is actually exhibited. Finite results remain unadopted pending independent proof/shortness review.'}
    (BASE / 'HC-HC-avoidance-closure-results.json').write_text(json.dumps(output, indent=2)+'\n')
    print(json.dumps({k: output[k] for k in ['status', 'runtime', 'cases_checked', 'directions_checked', 'positive_cases', 'cut_positive_cases', 'additional_positive_beyond_cut_cases', 'avoiding_fully_forced_HC_directions']}))

if __name__ == '__main__':
    main()
