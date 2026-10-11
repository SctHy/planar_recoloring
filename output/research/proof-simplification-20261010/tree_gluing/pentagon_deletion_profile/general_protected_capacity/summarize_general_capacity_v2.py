#!/usr/bin/env python3
"""Summarize frozen counts; no graph or cycle operations occur here."""
from collections import Counter
from pathlib import Path
import hashlib
import json

BASE = Path(__file__).resolve().parent
HARD = {'00001:0': 1, '00112:0': 2}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def key(c):
    return [c['source'], c['changed_position'], c['new_colour'], c['target']]


def summarize(cases):
    global_plain = [sum(c['plain_support_bounds']) for c in cases]
    global_refined = [sum(c['refined_support_bounds']) for c in cases]
    preferred_hits, arbitrary_hits, both_saturation_hits, either_saturation_hits = [], [], [], []
    best_profiles = Counter()
    best_plain_profiles = Counter()
    best_bounds = Counter()
    signatures = Counter()
    neither_saturated = []
    for c in cases:
        src_hard, tgt_hard = c['source'] in HARD, c['target'] in HARD
        signatures[f'source_hard={src_hard},target_hard={tgt_hard}'] += 1
        saturation = []
        preferred = []
        if src_hard:
            k = HARD[c['source']]
            assert c['x'][k] == c['m_prime'][k]
            preferred.append(c['y'][k] > 0)
            saturation.extend(c['x'][j] == c['m_prime'][j] and c['y'][j] > 0 for j in range(5))
        if tgt_hard:
            s, eps, _ = c['normalizer']
            k = (s + eps * HARD[c['target']]) % 5
            assert c['y'][k] == c['m_prime'][k]
            preferred.append(c['x'][k] > 0)
            saturation.extend(c['y'][j] == c['m_prime'][j] and c['x'][j] > 0 for j in range(5))
        preferred_hits.append(any(preferred))
        arbitrary_hits.append(any(saturation))
        both = any(c['x'][j] == c['y'][j] == c['m_prime'][j] and c['m_prime'][j] > 0 for j in range(5))
        both_saturation_hits.append(both)
        either_saturation_hits.append(any((c['x'][j] == c['m_prime'][j] and c['y'][j] > 0)
              or (c['y'][j] == c['m_prime'][j] and c['x'][j] > 0) for j in range(5)))
        j = max(range(5), key=lambda j: (c['refined_support_bounds'][j], -j))
        profile = tuple(c[f][j] for f in ('x', 'y', 'm_prime', 'f_prime', 'rK', 'rL'))
        best_profiles[profile] += 1
        best_plain_profiles[profile[:3]] += 1
        best_bounds[c['refined_support_bounds'][j]] += 1
        if not any(saturation):
            neither_saturated.append({'case': key(c), 'best_coordinate': j,
                                     'best_profile': profile,
                                     'best_plain_bound': c['plain_support_bounds'][j],
                                     'best_refined_bound': c['refined_support_bounds'][j]})
    return {
        'total': len(cases),
        'coordinate_plain_covered': sum(bool(c['plain_hit_coordinates']) for c in cases),
        'coordinate_refined_covered': sum(bool(c['refined_hit_coordinates']) for c in cases),
        'changed_coordinate_plain_covered': sum(c['changed_position'] in c['plain_hit_coordinates'] for c in cases),
        'changed_coordinate_refined_covered': sum(c['changed_position'] in c['refined_hit_coordinates'] for c in cases),
        'global_plain_covered': sum(v >= 1 for v in global_plain),
        'global_refined_covered': sum(v >= 1 for v in global_refined),
        'global_plain_range': [min(global_plain), max(global_plain)],
        'global_refined_range': [min(global_refined), max(global_refined)],
        'global_plain_uncovered_cases': [key(c) for c, v in zip(cases, global_plain) if v < 1],
        'global_refined_uncovered_cases': [key(c) for c, v in zip(cases, global_refined) if v < 1],
        'hard_preferred_saturated_coordinate_covered': sum(preferred_hits),
        'hard_some_saturated_coordinate_covered': sum(arbitrary_hits),
        'both_bases_saturate_some_coordinate_covered': sum(both_saturation_hits),
        'either_basis_saturates_some_coordinate_covered': sum(either_saturation_hits),
        'without_either_basis_saturating_any_coordinate': [key(c) for c, hit in zip(cases, either_saturation_hits) if not hit],
        'hard_preferred_uncovered_cases': [key(c) for c, hit in zip(cases, preferred_hits) if not hit],
        'without_any_hard_saturated_coordinate': neither_saturated,
        'best_refined_profile_rule': 'maximum refined bound, then smallest physical coordinate',
        'best_refined_profiles_distinct': len(best_profiles),
        'best_plain_profiles_distinct': len(best_plain_profiles),
        'best_refined_profile_histogram': [{'profile': p, 'count': n} for p, n in sorted(best_profiles.items())],
        'best_refined_bound_histogram': dict(sorted(best_bounds.items())),
        'hard_incidence_histogram': dict(sorted(signatures.items())),
    }


def main():
    record_path = BASE / 'port-support-capacity-results-v2.json'
    baseline_path = BASE / 'general-capacity-baseline-results-v1.json'
    record = json.loads(record_path.read_text())
    baseline = json.loads(baseline_path.read_text())
    assert record['interface_count'] == baseline['interface_count'] == 313
    assert record['actual_protected_edge_intersection_computed'] is False
    assert record['HC_search'] is False
    summaries = {g: summarize([c for c in record['cases'] if c['group'] == g])
                 for g in ('nonconstant-source-hard-53', 'constant-source-30')}
    assert summaries['nonconstant-source-hard-53']['total'] == 53
    assert summaries['constant-source-30']['total'] == 30
    result = {
        'status': 'FINITE_FROZEN_COUNT_SUMMARY',
        'source_provenance': record['source_provenance'],
        'input_sha256': {record_path.name: sha(record_path), baseline_path.name: sha(baseline_path)},
        'script_sha256': sha(Path(__file__)),
        'coordinate_coverage_by_group': record['coverage_by_group'],
        'whole_record_plain_coordinate_coverage': record['plain_covered'],
        'whole_record_refined_coordinate_coverage': record['refined_covered'],
        'requested_group_summaries': summaries,
        'structural_scope': 'One-sided saturation is a sufficient structural condition, not universal here. All 53 hard cases have positive coordinate capacity, but this remains selected-basis finite evidence.',
        'graph_recomputed': False, 'actual_protected_edge_intersection_computed': False,
        'HC_search': False,
    }
    output = BASE / 'general-capacity-summary-v2.json'
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({g: {k: s[k] for k in ('total', 'global_plain_covered', 'global_refined_covered',
         'hard_preferred_saturated_coordinate_covered', 'hard_some_saturated_coordinate_covered',
         'both_bases_saturate_some_coordinate_covered', 'best_refined_profiles_distinct')}
         for g, s in summaries.items()}, indent=2))
    print(output)


if __name__ == '__main__':
    main()
