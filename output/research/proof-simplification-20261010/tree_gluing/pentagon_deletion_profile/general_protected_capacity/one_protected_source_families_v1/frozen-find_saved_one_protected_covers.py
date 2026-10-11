#!/usr/bin/env python3
"""Exact word-mask DP over saved observations; no graph or normalization calls."""
from collections import Counter, defaultdict
from pathlib import Path
import hashlib
import json
import platform
import time

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
SYMMETRIC = BASE / 'one_protected_vs_hc_v2/symmetric-one-sided-results-v2.json'
UNION = BASE / 'union_star_families_v1/union-source-cover-results.json'
DIRECTIONS = [('F', 'forward_fixed_source_K'),
              ('R', 'reverse_fixed_restored_target_K')]
HARD = {'00001', '00112'}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def identity(interface):
    return tuple(interface[k] for k in ('source', 'source_component', 'position',
                                      'colour', 'target_type', 'target_component'))


def exact_cover(rows, retained=()):
    """Shortest, lexicographically first new-word set for a fixed source."""
    assert rows and len(rows) <= 15
    masks = defaultdict(int)
    direction_masks = defaultdict(lambda: {'F': 0, 'R': 0})
    by_word_case = defaultdict(list)
    for i, row in enumerate(rows):
        for direction, observation_key in DIRECTIONS:
            observation = row[observation_key]
            if observation is None:
                continue
            for certificate in observation['certificates']:
                w = certificate['state']
                masks[w] |= 1 << i
                direction_masks[w][direction] |= 1 << i
                by_word_case[w, i].append((direction, certificate))
    full = (1 << len(rows)) - 1
    assert full == sum(1 << i for i in range(len(rows)))
    retained = tuple(sorted(retained))
    precovered = 0
    for w in retained:
        precovered |= masks.get(w, 0)
    dp = {precovered: ()}
    transitions = 0
    for w, mask in sorted(masks.items()):
        if w in retained:
            continue
        updated = dict(dp)
        for oldmask, selected in dp.items():
            transitions += 1
            newmask = oldmask | mask
            new = selected + (w,)
            previous = updated.get(newmask)
            if previous is None or (len(new), new) < (len(previous), previous):
                updated[newmask] = new
        dp = updated
    selected = dp[full]
    usable = tuple(sorted(set(retained) | set(selected)))
    assert len(selected) == len(set(selected))
    coverage = []
    for i, row in enumerate(rows):
        choices = [(w, d, c) for w in usable
                   for d, c in by_word_case.get((w, i), [])]
        # Retained-word support first; then actual word and original direction.
        choices.sort(key=lambda a: (a[0] not in retained, a[0], a[1]))
        assert choices
        w, direction, certificate = choices[0]
        coverage.append({'case_bit_index': i, 'interface': row['interface'],
                         'group': row['group'], 'selected_actual_state': w,
                         'direction': direction,
                         'word_was_retained': w in retained,
                         'all_selected_supports': [{'state': a, 'direction': d}
                                                   for a, d, _ in choices],
                         'saved_certificate': certificate})
    assert sum(bool(precovered & (1 << i)) for i in range(len(rows))) == sum(
        any(masks.get(w, 0) & (1 << i) for w in retained)
        for i in range(len(rows)))
    return {'covered_cases': len(rows), 'candidate_words': len(masks),
            'candidate_masks': dict(sorted(masks.items())),
            'candidate_direction_masks': dict(sorted(direction_masks.items())),
            'retained_words': list(retained),
            'retained_precovered_cases': precovered.bit_count(),
            'minimum_new_members': len(selected), 'selected_new_words': list(selected),
            'usable_words': list(usable), 'mask_states_reached': len(dp),
            'dp_transitions': transitions, 'coverage': coverage}


def scenario(rows, retained_by_source=None):
    groups = defaultdict(list)
    for row in rows:
        groups[row['interface']['source']].append(row)
    retained_by_source = retained_by_source or {}
    families = {t: exact_cover(rs, retained_by_source.get(t, ()))
                for t, rs in sorted(groups.items())}
    members = sum(f['minimum_new_members'] for f in families.values())
    words = {w for f in families.values() for w in f['selected_new_words']}
    return {'covered_interfaces': len(rows), 'source_rows': len(families),
            'source_rows_needing_new_words': sum(bool(f['minimum_new_members'])
                                               for f in families.values()),
            'minimum_new_memberships': members, 'selected_new_distinct_words': len(words),
            'retained_precovered_cases': sum(f['retained_precovered_cases']
                                          for f in families.values()),
            'direction_assignment_counts': dict(sorted(Counter(
                c['direction'] for f in families.values() for c in f['coverage']).items())),
            'certificate_types': dict(sorted(Counter(
                f"d{c['saved_certificate']['HC_side_degree']}/g{c['saved_certificate']['safe_incident_count']}"
                for f in families.values() for c in f['coverage']).items())),
            'families': families}


def run():
    begin = time.perf_counter()
    initial_hashes = {str(p.relative_to(BASE)): sha(p) for p in (SYMMETRIC, UNION)}
    saved = json.loads(SYMMETRIC.read_text())
    union = json.loads(UNION.read_text())
    assert saved['status'] == union['status'] == 'PASS'
    assert saved['original_mapping_preserved_on_reverse'] is True
    rows = saved['records']
    assert len(rows) == 313
    assert len({identity(r['interface']) for r in rows}) == 313
    observed_counts = Counter()
    certificate_types = Counter()
    for row in rows:
        fixed_support = []
        for direction, key in DIRECTIONS:
            observation = row[key]
            hc_type = row['interface']['target_type' if direction == 'F' else 'source']
            assert (observation is None) == (hc_type in HARD)
            if observation is None:
                continue
            local = observation['all_local_observations']
            assert len(local) == observation['candidate_vertices']
            assert len({c['state'] for c in local}) == len(local)
            positive = []
            for c in local:
                d, g = c['HC_side_degree'], c['safe_incident_count']
                assert d >= 2 and 0 <= g <= 2
                assert d == sum(c['HC_side_degree_terms']) == len(c['HC_side_neighbours'])
                assert g == len(c['safe_fixed_K_neighbours'])
                assert set(c['safe_fixed_K_neighbours']) <= set(c['HC_side_neighbours'])
                assert c['protected_edge_lower_bound'] == max(0, 2+g-d)
                if c['protected_edge_lower_bound'] > 0:
                    assert d-g <= 1 and (d, g) in {(2, 1), (2, 2), (3, 2)}
                    certificate_types[d, g] += 1
                    positive.append(c)
            assert positive == observation['certificates']
            assert observation['covered'] == bool(positive)
            observed_counts[direction] += len(local)
            fixed_support.append(bool(positive))
        assert row['covered'] == any(fixed_support)
    assert dict(observed_counts) == {'F': 10706, 'R': 10808}
    nonconstant = [r for r in rows if r['interface']['source'] != '00000']
    covered = [r for r in nonconstant if r['covered']]
    assert len(nonconstant) == 283 and len(covered) == 236
    baseline = {identity(c['interface']) for f in union['families'].values()
                for c in f['coverage']}
    covered_ids = {identity(r['interface']) for r in covered}
    assert len(baseline) == 125 and baseline <= covered_ids
    extra = [r for r in covered if identity(r['interface']) not in baseline]
    assert len(extra) == 111
    retained = {t: f['selected_words'] for t, f in union['families'].items()}
    assert sum(map(len, retained.values())) == 48
    baseline_words = {w for ws in retained.values() for w in ws}
    assert len(baseline_words) == 27
    full = scenario(covered)
    additional = scenario(extra)
    kept = scenario(extra, retained)
    added_words = {w for f in kept['families'].values() for w in f['selected_new_words']}
    added_source_rows = set(kept['families']) - set(retained)
    remaining = [r for r in nonconstant if not r['covered']]
    assert len(remaining) == 47
    out = {'status': 'PASS', 'python': platform.python_version(),
           'input_sha256': initial_hashes, 'code_sha256': sha(Path(__file__)),
           'data_structure_sufficient': True,
           'all_saved_local_observations_scalar_readback': dict(observed_counts),
           'all_positive_certificate_types': {f'd{d}/g{g}': n
                                               for (d, g), n in sorted(certificate_types.items())},
           'original_first_maps_retained_without_recomputation': True,
           'current_union_baseline': {'interfaces': 125, 'source_rows': 15,
                                      'memberships': 48, 'distinct_words': 27,
                                      'remaining_individual_records': 158},
           'all236': full, 'extra111': additional,
           'extra111_with_retained_union48': kept,
           'combined_retained125_plus_extra111': {
               'covered_interfaces': 236, 'source_rows': len(set(retained) | set(kept['families'])),
               'new_source_rows': len(added_source_rows),
               'total_memberships': 48 + kept['minimum_new_memberships'],
               'total_distinct_words': len(baseline_words | added_words),
               'remaining_individual_records': 47},
           'literal_endpoint_proxy': {
               'current125_membership_proxy': 2*158+48,
               'all236_membership_proxy': 2*47+full['minimum_new_memberships'],
               'retained125_plus_extra_membership_proxy': 2*47+48+kept['minimum_new_memberships'],
               'meaning': 'Two endpoint-word occurrences per residual individual edge plus selector memberships; ignores degree, safe-membership and direction/map premises, so not proof length.'},
           'uncovered_interfaces': [{'interface': r['interface'], 'group': r['group']}
                                    for r in remaining],
           'uncovered_groups': dict(sorted(Counter(r['group'] for r in remaining).items())),
           'elapsed_seconds': time.perf_counter()-begin,
           'limits': ['Minimum is exact per original source within saved candidate-word masks, not globally minimum distinct words.',
                      'One side stays the specified fixed protected K; never an arbitrary-both-HC theorem.',
                      'Every interface retains its actual source-coordinate word, F/R direction, original mapping and component IDs.',
                      'No new neighbor, whole-state graph, normalizer, HC or K/K intersection calculation.',
                      'Counts are finite selector feasibility, not a shorter proved symbolic family or manuscript candidate.']}
    assert initial_hashes == {str(p.relative_to(BASE)): sha(p) for p in (SYMMETRIC, UNION)}
    result = HERE / 'saved-one-protected-selector-results.json'
    result.write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({k: v for k, v in out.items()
                      if k not in {'all236', 'extra111', 'extra111_with_retained_union48',
                                   'uncovered_interfaces'}}, indent=2))
    for name in ('all236', 'extra111', 'extra111_with_retained_union48'):
        value = out[name]
        print(name, json.dumps({k: v for k, v in value.items() if k != 'families'}))
        print(json.dumps({t: {k: v for k, v in f.items()
                              if k in {'covered_cases', 'minimum_new_members', 'selected_new_words',
                                       'retained_precovered_cases', 'mask_states_reached', 'dp_transitions'}}
                          for t, f in value['families'].items()}, indent=2))


if __name__ == '__main__':
    run()
