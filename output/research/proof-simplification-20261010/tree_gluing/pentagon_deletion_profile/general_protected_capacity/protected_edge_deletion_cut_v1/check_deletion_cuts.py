"""Exact residual-only deletion/cut checks. Reuses hash-bound reviewed readers.

No Hamilton-cycle search. Negative cut tests do not imply a Hamilton cycle.
"""
from pathlib import Path
from collections import Counter
import hashlib
import json
import platform
import sys
import time
from itertools import permutations
import independent_source_reader as R
from fixed_k_source_reader import ActualSource, HARD

BASE = Path(__file__).resolve().parent

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def components(adjacency, removed=frozenset()):
    unseen = set(adjacency) - set(removed)
    answer = []
    while unseen:
        first = min(unseen)
        reached = {first}
        unseen.remove(first)
        stack = [first]
        while stack:
            for neighbor in adjacency[stack.pop()]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    reached.add(neighbor)
                    stack.append(neighbor)
        answer.append(sorted(reached))
    return sorted(answer, key=lambda part: (len(part), part))

def main():
    assert not (BASE / 'cut-results.json').exists(), 'Preserve executed results'
    manifest = json.loads((BASE / 'input-manifest.json').read_text())
    for item in manifest['files']:
        assert sha(BASE / item['path']) == item['sha256'], item['path']
    started = time.perf_counter()
    current = R.marked((BASE / 'phase10-source.tex').read_text())
    reference = R.marked((BASE / 'reference-phase9.tex').read_text())
    assert len(current) == len(reference) == 53
    assert all(current[k] == reference[k] for k in current if k != 'INTERFACES-ALL')
    prior = json.loads((BASE / 'prior-independent125-results.json').read_text())
    source = ActualSource(current, reference, prior['component_checks'])
    residual = R.interfaces(current['INTERFACES-ALL'])
    assert len(residual) == len({key for key, edge in residual}) == 47
    graph_cache = {}
    def graph(t, c):
        key = (t, c)
        if key not in graph_cache:
            V, E, P, K, hc = source.component(t, c)
            N = {word: R.neighbours(word, t) for word in V}
            assert all(neighbors <= V for neighbors in N.values())
            assert all(word in N[y] for word in V for y in N[word])
            graph_cache[key] = (V, N, P, K, hc)
        return graph_cache[key]
    cases = []
    for key, old_edge in residual:
        source_key, j, q, target_key = key
        t, sc = source_key.split(':'); target, tc = target_key.split(':')
        boundary = t[:j] + str(q) + t[j+1:]
        target_type, mapping = source.first_normalizer(boundary)
        assert target_type == target
        V, Ns, P, Ks, source_hc = graph(t, int(sc))
        targetV, targetN, targetP, targetK, target_hc = graph(target, int(tc))
        restoredV = {R.restore(word, mapping) for word in targetV}
        Nt = {R.restore(word, mapping): {R.restore(y, mapping) for y in targetN[word]} for word in targetV}
        Q = {R.edge(R.restore(a, mapping), R.restore(b, mapping)) for a, b in targetP}
        Kt = {R.edge(R.restore(a, mapping), R.restore(b, mapping)) for a, b in targetK}
        assert len(Q) == len(targetP) and len(Kt) == len(targetK) and Q.isdisjoint(Kt)
        assert all(R.is_legal(word, boundary) for word in restoredV)
        assert all(R.neighbours(word, boundary) == Nt[word] for word in restoredV)
        directions = []
        for direction, eligible, N, K, pool in [('forward', target_hc, Nt, Ks, Q), ('reverse', source_hc, Ns, Kt, P)]:
            if not eligible:
                continue
            edges = {R.edge(word, y) for word in N for y in N[word]}
            safe = (K & edges) - pool
            assert safe <= K and safe.isdisjoint(pool)
            H = {word: {y for y in neighbors if R.edge(word, y) not in safe} for word, neighbors in N.items()}
            low_degree = sorted(word for word in H if len(H[word]) <= 1)
            connected_parts = components(H)
            # Every remaining interface fails the exhaustive degree rule;
            # this independently checks that our deletion predicate agrees.
            assert not low_degree, (key, direction, low_degree)
            articulation = []
            if len(connected_parts) == 1:
                for word in sorted(H):
                    parts = components(H, {word})
                    if len(parts) > 1:
                        articulation.append({'vertex': word, 'components_after_deletion': parts})
            positive = len(connected_parts) > 1 or bool(articulation)
            directions.append({
                'direction': direction, 'whole_component_HC_side': 'restored target' if direction == 'forward' else 'standard source',
                'state_count': len(H), 'original_graph_edges': len(edges), 'safe_K_edges_deleted': sorted(safe),
                'residual_edge_count': sum(map(len, H.values())) // 2,
                'residual_minimum_degree': min(map(len, H.values())),
                'residual_degree_histogram': dict(Counter(map(len, H.values()))),
                'residual_graph_components': connected_parts,
                'articulation_witnesses': articulation,
                'positive_cut_obstruction': positive,
            })
        cases.append({'case': key, 'original_printed_edge': old_edge, 'actual_target_boundary': boundary,
            'original_first_normalizer': [mapping[0], mapping[1], list(mapping[2])],
            'source_has_printed_whole_component_HC': source_hc, 'target_has_printed_whole_component_HC': target_hc,
            'directions': directions, 'positive_cut_obstruction': any(row['positive_cut_obstruction'] for row in directions)})
    roles = Counter('HC-HC' if c['source_has_printed_whole_component_HC'] and c['target_has_printed_whole_component_HC'] else 'mixed' if c['directions'] else 'hard-hard' for c in cases)
    assert roles == {'HC-HC': 28, 'mixed': 14, 'hard-hard': 5}
    assert sum(map(lambda c: len(c['directions']), cases)) == 70
    output = {
        'status': 'EXACT_RESIDUAL_DELETION_CUT_CHECK_COMPLETE',
        'runtime': {'python': platform.python_version(), 'seconds': time.perf_counter() - started},
        'source_sha256': sha(BASE / 'phase10-source.tex'), 'script_sha256': sha(Path(__file__)),
        'residual_cases': 47, 'eligible_cases': 42, 'eligible_directions': 70,
        'case_types': dict(roles),
        'new_positive_cases': sum(c['positive_cut_obstruction'] for c in cases),
        'new_positive_directions': sum(d['positive_cut_obstruction'] for c in cases for d in c['directions']),
        'component_checks': source.component_checks,
        'cases': cases,
        'HC_search': False, 'main_modified': False,
        'scope': 'Exact70 residual directions only; reviewed reader/component premises reused. Cut success proves required local intersection. Failure only means these cuts give no certificate, not that an avoiding Hamilton cycle exists or protection fails.',
    }
    (BASE / 'cut-results.json').write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps({k: output[k] for k in ['status', 'runtime', 'eligible_cases', 'eligible_directions', 'new_positive_cases', 'new_positive_directions']}))

if __name__ == '__main__':
    main()
