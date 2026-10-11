#!/usr/bin/env python3
"""Summarize frozen finite counts without new graph computation."""
from collections import Counter
from pathlib import Path
import hashlib
import json

BASE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    source = BASE / 'hh-coordinate-capacity-results-v1.json'
    data = json.loads(source.read_text())
    assert data['interface_count'] == 230
    cases = data['cases']
    grouped = {'source': {}, 'target': {}}
    for case in cases:
        for side in grouped:
            group = grouped[side].setdefault(case[side], {'total': 0, 'coarse_covered': 0, 'refined_covered': 0})
            group['total'] += 1
            group['coarse_covered'] += bool(case['coarse_hit_coordinates'])
            group['refined_covered'] += bool(case['refined_hit_coordinates'])
    modes = {}
    for mode in ('coarse', 'refined'):
        histogram = Counter()
        best_histogram = Counter()
        lower_histogram = Counter()
        scalar_profiles = set()
        best_profiles = set()
        positive_best_profiles = set()
        changed_count = 0
        best_equals_changed = 0
        for case in cases:
            bounds = case[mode + '_bounds']
            changed_count += bounds[case['changed_position']] >= 1
            histogram.update(case[mode + '_hit_coordinates'])
            best = max(range(5), key=lambda j: (bounds[j], -j))
            best_histogram[best] += 1
            lower_histogram[bounds[best]] += 1
            best_equals_changed += best == case['changed_position']
            profiles = [tuple(case[k][j] for k in ('a', 'b', 'm', 'f', 'rC', 'rD')) for j in range(5)]
            scalar_profiles.update(profiles)
            best_profiles.add(profiles[best])
            if bounds[best] >= 1:
                positive_best_profiles.add(profiles[best])
        modes[mode] = {
            'covered': sum(bool(x[mode + '_hit_coordinates']) for x in cases),
            'changed_coordinate_covered': changed_count,
            'all_positive_coordinate_histogram': dict(histogram),
            'best_coordinate_histogram_smallest_index_tie': dict(best_histogram),
            'best_coordinate_equals_changed': best_equals_changed,
            'best_bound_histogram': dict(sorted(lower_histogram.items())),
            'all_1150_scalar_profile_distinct_count': len(scalar_profiles),
            'best_230_scalar_profile_distinct_count': len(best_profiles),
            'positive_best_scalar_profile_distinct_count': len(positive_best_profiles),
            'profile_tuple_definition': ['a', 'b', 'm', 'f', 'rC', 'rD'],
        }
    remaining = [x for x in cases if not x['refined_hit_coordinates']]
    typical = data['typical_00101_to_10101']
    summary = {
        'scope': data['scope'],
        'status': 'Finite-count feasibility; no analytic general theorem or replacement of 222 witnesses claimed.',
        'input_record': {source.name: sha(source)},
        'summary_script_sha256': sha(Path(__file__)),
        'actual_source_sha256': data['source_provenance']['source_sha256'],
        'coverage': modes, 'by_source_and_target': grouped,
        'remaining_refined_uncovered_count': len(remaining),
        'remaining_refined_uncovered_cases': remaining,
        'typical': typical,
        'constant_source_HH_interfaces': data['constant_source_HH_interfaces'],
        'constant_target_HH_interfaces': data['constant_target_HH_interfaces'],
        'profile_warning': 'Equal numeric tuples are not proved symmetry or parametric families.',
        'no_additional_graph_computation': True,
    }
    out = BASE / 'hh-coordinate-capacity-summary-v1.json'
    out.write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(modes, indent=2))
    print('remaining:', [(x['source'], x['changed_position'], x['new_colour'], x['target']) for x in remaining])


if __name__ == '__main__':
    main()
