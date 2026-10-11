#!/usr/bin/env python3
"""Separate joint-port-support universe study for all frozen 313 cases.

Only individual K/L endpoint sets and clipped counts are used. No K/L
edge intersection, no HC search, no claim that W is the full fibre.
"""
from collections import Counter
from pathlib import Path
import hashlib
import importlib.util
import json
import re
import time

BASE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('capacity', BASE / 'general_capacity_baseline_v1.py')
cap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cap)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def endpoints(es):
    return {v for e in es for v in e}


def main():
    started = time.monotonic()
    baseline_path = BASE / 'general-capacity-baseline-results-v1.json'
    baseline = json.loads(baseline_path.read_text())
    assert baseline['interface_count'] == 313 and baseline['HH_vectors_exactly_inherited'] == 230
    frozen = BASE / 'phase6-protected-bases-input-v1.tex'
    assert sha(frozen) == baseline['source_provenance']['frozen_sha256']
    blocks = dict(re.findall(r'% BEGIN ([A-Z0-9-]+)\n(.*?)% END \1', frozen.read_text(), re.S))
    components, _ = cap.load_components(blocks)
    support_metadata = []
    for key, comp in components.items():
        K = comp['basis'] - comp['pool']
        vertices = endpoints(K)
        Hsupport = cap.raw_edges(vertices)
        support_metadata.append({'component': key, 'full_component_states': len(comp['states']),
                                 'protected_edges': len(K), 'port_endpoint_states': len(vertices),
                                 'induced_support_graph_edges': len(Hsupport),
                                 'K_coordinate_counts': cap.counts(K),
                                 'support_graph_coordinate_counts': cap.counts(Hsupport),
                                 'saturated_coordinates': [j for j, (a, b) in enumerate(zip(cap.counts(K), cap.counts(Hsupport))) if a == b and a > 0]})
        if key == '00001:0':
            assert (len(vertices), len(Hsupport), cap.counts(K), cap.counts(Hsupport)) == (20, 17, [5, 2, 0, 2, 2], [6, 2, 1, 4, 4])
        if key == '00112:0':
            assert (len(vertices), len(Hsupport), cap.counts(K), cap.counts(Hsupport)) == (20, 17, [3, 1, 3, 2, 2], [4, 3, 3, 4, 3])
    cases = []
    for original in baseline['cases']:
        source, target, g = original['source'], original['target'], original['normalizer']
        compA, compB = components[source], components[target]
        P = compA['pool']
        Q = {cap.edge(cap.restore(x, g), cap.restore(y, g)) for x, y in compB['pool']}
        K = compA['basis'] - P
        L = {cap.edge(cap.restore(x, g), cap.restore(y, g)) for x, y in compB['basis']} - Q
        VK, VL = endpoints(K), endpoints(L)
        W = VK & VL
        full_common = compA['states'] & {cap.restore(x, g) for x in compB['states']}
        assert W <= full_common
        Hprime = cap.raw_edges(W)
        Fprime = (P | Q) & Hprime
        x, y, m, f, rK, rL = map(cap.counts, (K & Hprime, L & Hprime, Hprime, Fprime, K & Fprime, L & Fprime))
        plain = [x[j] + y[j] - m[j] for j in range(5)]
        refined = [x[j] + y[j] - m[j] - rK[j] - rL[j] + f[j] for j in range(5)]
        assert all(refined[j] >= plain[j] for j in range(5))
        assert all(refined[j] >= original['refined_bounds'][j] for j in range(5))
        cases.append({'source': source, 'changed_position': original['changed_position'],
                      'new_colour': original['new_colour'], 'target': target,
                      'group': original['group'], 'normalizer': g,
                      'full_common_component_states': len(full_common),
                      'K_endpoint_states': len(VK), 'L_endpoint_states': len(VL),
                      'joint_port_support_states': len(W),
                      'x': x, 'y': y, 'm_prime': m, 'f_prime': f, 'rK': rK, 'rL': rL,
                      'plain_support_bounds': plain, 'refined_support_bounds': refined,
                      'plain_hit_coordinates': [j for j in range(5) if plain[j] >= 1],
                      'refined_hit_coordinates': [j for j in range(5) if refined[j] >= 1],
                      'baseline_refined_bounds': original['refined_bounds'],
                      'baseline_covered': bool(original['refined_hit_coordinates'])})
    coverage = {}
    for group in ('HH-230', 'nonconstant-source-hard-53', 'constant-source-30'):
        subset = [x for x in cases if x['group'] == group]
        coverage[group] = {'total': len(subset)}
        for mode in ('plain', 'refined'):
            field = mode + '_hit_coordinates'
            covered = sum(bool(x[field]) for x in subset)
            coverage[group][mode + '_covered'] = covered
            coverage[group][mode + '_uncovered'] = len(subset) - covered
            coverage[group][mode + '_changed_coordinate_covered'] = sum(x['changed_position'] in x[field] for x in subset)
        coverage[group]['new_refined_covered_over_baseline'] = sum(bool(x['refined_hit_coordinates']) and not x['baseline_covered'] for x in subset)
    result = {
        'status': 'FINITE_JOINT_PORT_SUPPORT_COUNT',
        'scope': 'All original 313 cases on W=V(K) intersect V(L), an edge-candidate support universe, not the full fibre.',
        'proof_boundary': 'The support-capacity and monotonicity inequalities are proved separately; coverage remains finite selected-basis evidence.',
        'source_provenance': baseline['source_provenance'],
        'baseline_record': {baseline_path.name: sha(baseline_path)},
        'script_sha256': sha(Path(__file__)),
        'basis_reader_dependency_sha256': sha(BASE / 'general_capacity_baseline_v1.py'),
        'lemma_sha256': sha(BASE / 'port_support_capacity_lemma_v2.tex'),
        'component_support_metadata': support_metadata,
        'coverage_by_group': coverage,
        'interface_count': len(cases),
        'plain_covered': sum(bool(x['plain_hit_coordinates']) for x in cases),
        'refined_covered': sum(bool(x['refined_hit_coordinates']) for x in cases),
        'new_refined_covered_over_baseline': sum(bool(x['refined_hit_coordinates']) and not x['baseline_covered'] for x in cases),
        'all_coordinate_refined_bounds_monotone': True,
        'cases': cases, 'actual_protected_edge_intersection_computed': False,
        'HC_search': False, 'full_fibre_coverage_claimed_for_W': False,
        'elapsed_seconds': time.monotonic() - started,
    }
    output = BASE / 'port-support-capacity-results-v2.json'
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'interface_count': len(cases), 'coverage': coverage,
                      'elapsed_seconds': result['elapsed_seconds']}, indent=2))
    print('results:', output)


if __name__ == '__main__':
    main()
