"""Exact local forced-outside capacity bounds; no selected-cycle edge input."""
from collections import Counter
from itertools import permutations
from pathlib import Path
import hashlib
import json
import platform
import re
import time

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
V1 = BASE / 'degree_aggregate_v1'
SOURCE_SHA = '7a90f79db489447b0bad3019217fd369a5cc25986288247981cbe7f3462acba3'
V1_DIGESTS = {
    'aggregate-candidate.tex': '6e33205c4e8b7f4d7cacbfbc923ae9d51375e65888bea3520c487afe099e20d9',
    'check_degree_aggregate.py': '7bd0b6db7d83fdc13bd66dfe19418c34ce061939f6130e59203afab2f2810a79',
    'aggregate-results.json': '2fdd92874b3a4970872e4a5336ec652a5ca44a36e59d3c98c600caf7a3126ef6',
    'phase6-source.tex': SOURCE_SHA,
    'verified-interface-input.json': '66108453853c98075a61713dc607fb592f1fc173b65aae3c6033a073da0e5f92',
    'root_set_functions.py': 'bbe67d8645a69e5190fb5b168756dd86736d37d0234d8bc7d552a8905543f0db'}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def edge(a, b):
    return tuple(sorted((a, b)))


def main():
    started = time.perf_counter()
    for name, expected in V1_DIGESTS.items():
        assert sha(V1 / name) == expected, name
    text = (V1 / 'phase6-source.tex').read_text()
    blocks = dict(re.findall(r'^% BEGIN ([^\n]+)\n(.*?)^% END \1$', text, re.S | re.M))
    states = {name.split('-')[1] + ':0': set(re.findall(r'\b[0-3]{5}\b', body))
              for name, body in blocks.items() if name.startswith(('C1-', 'FHC-'))}
    pools = {key: {edge(a, b) for a, b in re.findall(r'\b([0-3]{5})-([0-3]{5})\b',
                         blocks['POOL-' + key.replace(':', '-')])} for key in states}
    standard = {key[:5] for key in states} | {'00000', '00001', '00112'}
    interface_data = json.loads((V1 / 'verified-interface-input.json').read_text())
    old_data = json.loads((V1 / 'aggregate-results.json').read_text())
    old_records = {tuple(r['case']): r for r in old_data['records']}
    previous_reader = BASE / 'independent_root_review' / 'review-results.json'
    prior = json.loads(previous_reader.read_text())
    assert prior['status'] == 'PASS_BOUNDED_TWO_SCOPE_READBACK'
    assert prior['source_sha256'] == SOURCE_SHA
    assert prior['code_sha256'] == V1_DIGESTS['root_set_functions.py']
    assert prior['expected_support_sha256'] == V1_DIGESTS['verified-interface-input.json']
    node_path = BASE / 'one_sided_degree_v1' / 'independent_local_review' / 'both-hc-local-results.json'
    node_data = json.loads(node_path.read_text())
    assert node_data['status'] == 'PASS' and node_data['source_sha256'] == SOURCE_SHA
    node_covered = set()
    for r in node_data['records']:
        i = r['interface']
        key = (i['source'] + ':' + str(i['source_component']), i['position'], int(i['colour']),
               i['target_type'] + ':' + str(i['target_component']))
        if r['covered']:
            node_covered.add(key)
    assert len(node_covered) == 125
    checks = 0

    def legal(v, boundary):
        return all(v[i] != v[(i + 1) % 5] and (boundary[i] == '4' or v[i] != boundary[i])
                   for i in range(5))

    def neighbours(v, boundary):
        nonlocal checks
        assert legal(v, boundary)
        result = set()
        for i in range(5):
            for c in '0123':
                if c == v[i]:
                    continue
                checks += 1
                z = v[:i] + c + v[i + 1:]
                if legal(z, boundary):
                    result.add(z)
        return result

    def first_normalizer(boundary):
        for offset in range(5):
            for direction in (1, -1):
                for p in permutations(range(4)):
                    out = ''.join('4' if boundary[(offset + direction * i) % 5] == '4'
                                  else str(p[int(boundary[(offset + direction * i) % 5])]) for i in range(5))
                    if out in standard:
                        return out, [offset, direction, list(p)]
        raise AssertionError(boundary)

    def restore(v, mapping):
        offset, direction, p = mapping
        inverse = {str(p[i]): str(i) for i in range(4)}
        result = [''] * 5
        for i in range(5):
            result[(offset + direction * i) % 5] = inverse[v[i]]
        return ''.join(result)

    records = []
    for case in interface_data['cases']:
        if case['group'] != 'HH-230':
            continue
        source, target = case['source'], case['target']
        j, q, mapping = case['changed_position'], case['new_colour'], case['normalizer']
        source_boundary = source[:5]
        assert source_boundary[j] != '4' and source_boundary[j] != str(q)
        target_boundary = source_boundary[:j] + str(q) + source_boundary[j + 1:]
        n, canonical = first_normalizer(target_boundary)
        assert n == target[:5] and canonical == mapping
        Vs = states[source]
        Vt = {restore(v, mapping) for v in states[target]}
        U, O = Vs & Vt, Vs - Vt
        assert O == {v for v in Vs if v[j] == str(q)}
        target_pool = {edge(restore(a, mapping), restore(b, mapping)) for a, b in pools[target]}
        F = {e for e in pools[source] | target_pool if set(e) <= U}
        target_neighbours = {v: neighbours(v, target_boundary) for v in U}
        assert all(N <= Vt and len(N) >= 2 for N in target_neighbours.values())
        f = {v: sum(v in e for e in F) for v in U}
        reward = {v: 4 - len(target_neighbours[v]) - f[v] for v in U}
        S = {v for v in U if reward[v] > 0}
        assert all(len(target_neighbours[v]) <= 3 for v in S)
        outside_neighbours = {w: neighbours(w, source_boundary) for w in O}
        assert all(N <= Vs and len(N) >= 2 for N in outside_neighbours.values())
        assert all(len(N & U) <= 2 for N in outside_neighbours.values())
        J = {edge(w, z) for w in O for z in outside_neighbours[w] & O
             if len(outside_neighbours[w]) == 2 or len(outside_neighbours[z]) == 2}
        forced_degree = Counter(v for e in J for v in e)
        assert all(forced_degree[w] <= 2 for w in O)  # existing source HC guarantees consistency
        capacity = {w: 2 - forced_degree[w] for w in O}
        source_neighbours = {v: neighbours(v, source_boundary) for v in S}
        assert all(N <= Vs and len(N & O) <= 1 for N in source_neighbours.values())
        cut_counts = {w: len(outside_neighbours[w] & S) for w in O}
        cut = sum(cut_counts.values())
        assert cut == sum(len(N & O) for N in source_neighbours.values())
        # Original graph-only min(2|O|, cut) equals cut for a single boundary edit.
        assert cut <= 2 * len(O)
        cut_capacity = sum(min(cut_counts[w], capacity[w]) for w in O)
        A = sum(4 - len(target_neighbours[v]) for v in S)
        pool_inc = sum(f[v] for v in S)
        margin = A - pool_inc - cut_capacity
        optimized_original_margin = A - pool_inc - cut
        individual_margins = {v: reward[v] - len(source_neighbours[v] & O) for v in S}
        assert optimized_original_margin == sum(individual_margins.values())
        assert all(a >= 0 for a in individual_margins.values())
        # For the original, select only strictly positive node margins.
        node_positive = {v: a for v, a in individual_margins.items() if a > 0}
        bound = max(0, (margin + 1) // 2)
        optimized_original_bound = max(0, (optimized_original_margin + 1) // 2)
        key = (source, j, q, target)
        old = old_records[key]
        record = {'case': list(key), 'actual_target': target_boundary,
                  'outside_states': len(O), 'common_states': len(U),
                  'selector': sorted(S), 'selector_size': len(S),
                  'A': A, 'pool_incidences': pool_inc, 'graph_cut_edges_from_S': cut,
                  'forced_internal_outside_edges': [list(e) for e in sorted(J)],
                  'outside_capacities': {w: capacity[w] for w in sorted(O)},
                  'outside_cross_counts': {w: cut_counts[w] for w in sorted(O)},
                  'forced_outside_cut_capacity': cut_capacity, 'margin': margin, 'bound': bound,
                  'optimized_original_margin': optimized_original_margin,
                  'optimized_original_bound': optimized_original_bound,
                  'positive_node_count': len(node_positive), 'node_positive_words': node_positive,
                  'old_all_low_degree_aggregate_bound': old['aggregate_bound'],
                  'previous125_covered': key in node_covered,
                  'new_beyond125': bound > 0 and key not in node_covered,
                  'local_target_data': {v: {'d_target': len(target_neighbours[v]), 'f': f[v],
                                           'reward': reward[v], 'outside_neighbours': sorted(source_neighbours[v] & O)}
                                        for v in sorted(S)}}
        assert bool(node_positive) == (key in node_covered), key
        records.append(record)
    assert len(records) == 230
    new_covered = {tuple(r['case']) for r in records if r['bound'] > 0}
    assert node_covered <= new_covered
    for name, expected in V1_DIGESTS.items():
        assert sha(V1 / name) == expected, name
    summary = {'interfaces': len(records), 'old_all_low_degree_positive': old_data['summary']['aggregate_positive'],
               'optimized_original_positive': sum(r['optimized_original_bound'] > 0 for r in records),
               'node_positive': len(node_covered), 'forced_outside_positive': len(new_covered),
               'new_beyond125': len(new_covered - node_covered),
               'largest_forced_outside_bound': max(r['bound'] for r in records),
               'largest_optimized_original_bound': max(r['optimized_original_bound'] for r in records),
               'interfaces_with_capacity_discount': sum(r['forced_outside_cut_capacity'] < r['graph_cut_edges_from_S'] for r in records),
               'local_coordinate_mutations_tested': checks}
    result = {'status': 'PASS_EXACT_LOCAL_FORCED_OUTSIDE_CAPACITY', 'python': platform.python_version(),
              'source_sha256': SOURCE_SHA, 'v1_digests_preserved': V1_DIGESTS,
              'complete_fibre_evidence': {'path': str(previous_reader.relative_to(BASE)), 'sha256': sha(previous_reader),
                 'boundary': 'previous source-bound reader proved supplied ordinary word sets equal full legal fibres; not replayed here'},
              'node_comparison_input_sha256': sha(node_path), 'summary': summary, 'records': records,
              'new_cases_beyond125': [r['case'] for r in records if r['new_beyond125']],
              'selected_source_or_target_cycle_edges_used': False,
              'HC_search': False, 'palette_power_state_enumeration': False,
              'whole_state_graph_constructed': False, 'actual_cycle_edge_intersection': False,
              'scope': '230 fixed ordinary full-component/prescribed-pool interfaces; conditional analytic bound, not arbitrary-boundary positivity or theorem completion',
              'elapsed_seconds': time.perf_counter() - started}
    (HERE / 'forced-outside-capacity-results.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('records', 'v1_digests_preserved')}, indent=2))


if __name__ == '__main__':
    main()
