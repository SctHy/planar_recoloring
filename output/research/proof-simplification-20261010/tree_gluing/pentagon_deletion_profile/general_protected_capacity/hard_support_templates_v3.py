#!/usr/bin/env python3
"""Two fixed hard support templates plus extraction of frozen count profiles.

Only the two already frozen 20-vertex supports are reconstructed. No
opponent cycle edges, intersections, new Hamilton search or full fibres
are computed. Other-side retained counts come from the v2 record.
"""
from collections import Counter
from pathlib import Path
import hashlib
import json
import re

BASE = Path(__file__).resolve().parent
HARD = {'00001:0': ('COMMON-00001', 1), '00112:0': ('PORTS-00112', 2)}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def edge(a, b):
    return tuple(sorted((a, b)))


def coordinate(e):
    return next(j for j in range(5) if e[0][j] != e[1][j])


def counts(es):
    counter = Counter(map(coordinate, es))
    return [counter[j] for j in range(5)]


def legal(w, boundary):
    return all(w[j] != boundary[j] for j in range(5))


def transform(boundary, g):
    s, eps, perm = g
    return ''.join(str(perm[int(boundary[(s+eps*j) % 5])]) for j in range(5))


def restore(word, g):
    s, eps, perm = g
    inv = [perm.index(q) for q in range(4)]
    result = ['']*5
    for j in range(5):
        result[(s+eps*j) % 5] = str(inv[int(word[j])])
    return ''.join(result)


def main():
    frozen = BASE / 'phase6-protected-bases-input-v1.tex'
    record_path = BASE / 'port-support-capacity-results-v2.json'
    text = frozen.read_text()
    record = json.loads(record_path.read_text())
    templates = {}
    for key, (name, k) in HARD.items():
        def read_edges(block_name):
            body = re.search('% BEGIN '+block_name+'\n(.*?)% END '+block_name, text, re.S).group(1)
            return {edge(a, b) for a, b in re.findall(r'([0-3]{5})-([0-3]{5})', body)}
        K = read_edges(name) - read_edges('POOL-'+key[:5]+'-0')
        V = {v for e in K for v in e}
        J = {edge(a, b) for a in V for b in V if sum(x != y for x, y in zip(a, b)) == 1}
        missing = J-K
        assert (len(K), len(V), len(J), len(missing)) == (11, 20, 17, 6)
        assert all(coordinate(e) != k for e in missing)
        expected_metadata = next(m for m in record['component_support_metadata'] if m['component'] == key)
        assert counts(K) == expected_metadata['K_coordinate_counts']
        assert counts(J) == expected_metadata['support_graph_coordinate_counts']
        templates[key] = {'K': K, 'V': V, 'J': J, 'missing': missing, 'preferred': k}
    summaries = {}
    all_side_profiles = []
    fixed_failures = []
    for group in ('nonconstant-source-hard-53', 'constant-source-30'):
        cases = [c for c in record['cases'] if c['group'] == group]
        per_case = []
        preferred_hit, full_support_hit, legal_support_hit = 0, 0, 0
        for c in cases:
            sides = []
            for role in ('source', 'target'):
                key = c[role]
                if key not in HARD:
                    continue
                template = templates[key]
                if role == 'source':
                    r = c['changed_position']
                    q = c['new_colour']
                    opposite_boundary = key[:r]+str(q)+key[r+1:5]
                    physical = list(range(5))
                    opposite_counts = c['y']
                    hard_counts = c['x']
                    relative_normalizer = c['normalizer']
                    opposite_component = c['target']
                else:
                    s, eps, perm = c['normalizer']
                    r = (eps*(c['changed_position']-s)) % 5
                    opposite_boundary = transform(c['source'][:5], c['normalizer'])
                    q = int(opposite_boundary[r])
                    physical = [(s+eps*j) % 5 for j in range(5)]
                    opposite_counts = c['x']
                    hard_counts = c['y']
                    relative_normalizer = [(-eps*s) % 5, eps, [perm.index(a) for a in range(4)]]
                    opposite_component = c['source']
                assert sum(a != b for a, b in zip(key[:5], opposite_boundary)) == 1
                assert key[:5][r] != str(q)
                assert transform(opposite_boundary, relative_normalizer) == opposite_component[:5]
                legal_J = {e for e in template['J'] if all(legal(v, opposite_boundary) for v in e)}
                legal_missing = template['missing'] & legal_J
                deficit = counts(legal_missing)
                full_deficit = counts(template['missing'])
                ell = [opposite_counts[j] for j in physical]
                bounds = [ell[j]-deficit[j] for j in range(5)]
                full_bounds = [ell[j]-full_deficit[j] for j in range(5)]
                k = template['preferred']
                assert hard_counts[physical[k]] == c['m_prime'][physical[k]]
                legal_preferred_ports = sum(coordinate(e) == k for e in template['K'] & legal_J)
                sides.append({'hard_role': role, 'hard_type': key, 'opposite_boundary_in_hard_coordinates': opposite_boundary,
                              'canonical_changed_position': r, 'opposite_colour': q,
                              'opposite_component': opposite_component,
                              'relative_opposite_normalizer': relative_normalizer,
                              'preferred_canonical_coordinate': k, 'preferred_physical_coordinate': physical[k],
                              'preferred_opposite_retained_ports': ell[k],
                              'preferred_legal_hard_ports': legal_preferred_ports,
                              'preferred_clipped_hard_ports': hard_counts[physical[k]],
                              'opposite_retained_counts_in_fixed_support': ell,
                              'surviving_missing_edge_budget': deficit,
                              'one_sided_legal_support_bounds': bounds,
                              'one_sided_full_support_bounds': full_bounds})
            case_key = [c['source'], c['changed_position'], c['new_colour'], c['target']]
            if group == 'nonconstant-source-hard-53':
                all_side_profiles.extend({'case': case_key, **s} for s in sides)
            preferred = any(s['preferred_opposite_retained_ports'] > 0 for s in sides)
            full = any(max(s['one_sided_full_support_bounds']) >= 1 for s in sides)
            clipped = any(max(s['one_sided_legal_support_bounds']) >= 1 for s in sides)
            preferred_hit += preferred
            full_support_hit += full
            legal_support_hit += clipped
            per_case.append({'case': case_key, 'hard_sides': sides, 'fixed_preferred_hit': preferred,
                             'one_sided_full_support_hit': full, 'one_sided_legal_support_hit': clipped})
            if group == 'nonconstant-source-hard-53' and not preferred:
                fixed_failures.append(per_case[-1])
        summaries[group] = {'total': len(cases), 'fixed_preferred_covered': preferred_hit,
                            'one_sided_full_support_covered': full_support_hit,
                            'one_sided_legal_support_covered': legal_support_hit,
                            'legal_support_uncovered': [c for c in per_case if not c['one_sided_legal_support_hit']]}
    assert summaries['nonconstant-source-hard-53']['fixed_preferred_covered'] == 32
    assert len(fixed_failures) == 21
    assert summaries['nonconstant-source-hard-53']['one_sided_legal_support_covered'] == 51
    failure_parameters = {}
    for key in HARD:
        failure_parameters[key] = sorted({(s['canonical_changed_position'], s['opposite_colour'],
                                           s['opposite_boundary_in_hard_coordinates'])
            for c in fixed_failures for s in c['hard_sides'] if s['hard_type'] == key})
    grouped_profiles = {}
    for side in all_side_profiles:
        signature = (side['hard_type'], side['canonical_changed_position'], side['opposite_colour'])
        grouped_profiles.setdefault(signature, []).append(side)
    group_summary = []
    for signature, sides in sorted(grouped_profiles.items()):
        profiles = sorted({tuple(s['opposite_retained_counts_in_fixed_support']) for s in sides})
        maps = sorted({tuple([s['relative_opposite_normalizer'][0], s['relative_opposite_normalizer'][1], *s['relative_opposite_normalizer'][2]]) for s in sides})
        group_summary.append({'hard_type': signature[0], 'canonical_changed_position': signature[1],
                              'opposite_colour': signature[2], 'incidence_count': len(sides),
                              'opposite_component_labels': sorted({s['opposite_component'] for s in sides}),
                              'retained_coordinate_profiles': profiles, 'profile_count': len(profiles),
                              'relative_opposite_normalizers': maps, 'normalizer_count': len(maps)})
    self_supports = []
    for c in summaries['nonconstant-source-hard-53']['legal_support_uncovered']:
        key, changed, colour, target = c['case']
        assert key == target
        frozen_case = next(x for x in record['cases'] if [x['source'],x['changed_position'],x['new_colour'],x['target']] == c['case'])
        g = frozen_case['normalizer']
        K, V = templates[key]['K'], templates[key]['V']
        target_V = {restore(v, g) for v in V}
        W = V & target_V
        H = {edge(a,b) for a in W for b in W if sum(x != y for x,y in zip(a,b)) == 1}
        target_K = {edge(restore(a,g),restore(b,g)) for a,b in K}
        assert len(W) == 6
        assert counts(K & H) == counts(target_K & H) == counts(H)
        assert counts(H) == frozen_case['m_prime']
        assert len(H) == (1 if key == '00001:0' else 2)
        degrees = Counter(v for e in H for v in e)
        assert sorted(degrees.values()) == ([1,1] if len(H) == 1 else [1,1,2])
        self_supports.append({'case': c['case'], 'normalizer': g, 'joint_support_vertices': sorted(W),
                              'legal_support_edges': sorted(H), 'coordinate_edge_counts': counts(H),
                              'source_retained_counts': counts(K & H), 'target_retained_counts': counts(target_K & H),
                              'support_graph_shape': 'P2 + four isolated vertices' if len(H) == 1 else 'P3 + three isolated vertices'})
    result = {'status': 'TWO_FIXED_SUPPORT_TEMPLATES_AND_FROZEN_PROFILE_EXTRACTION',
              'source_provenance': record['source_provenance'],
              'input_sha256': {frozen.name: sha(frozen), record_path.name: sha(record_path)},
              'script_sha256': sha(Path(__file__)),
              'fixed_hard_templates': {k: {'protected_edge_count': 11, 'endpoint_state_count': 20,
                  'support_edge_count': 17, 'missing_edges': sorted(t['missing']),
                  'missing_coordinate_counts': counts(t['missing']),
                  'preferred_coordinate': t['preferred'],
                  'preferred_coordinate_protected_edges': sorted(e for e in t['K'] if coordinate(e) == t['preferred'])}
                  for k, t in templates.items()},
              'coverage': summaries, 'fixed_preferred_failures_21': fixed_failures,
              'canonical_failure_parameter_sets': failure_parameters,
              'canonical_hard_boundary_groups': group_summary,
              'hard_side_profiles_all53': all_side_profiles,
              'hard_side_profile_incidence_count': len(all_side_profiles),
              'exact_fixed_support_retention_identity': 'L intersect E_j(J_t(u)) equals L intersect E_j(H[W]); each L edge already has both endpoints in V(L), so lying inside V(K_t) is exactly lying inside W.',
              'two_hard_self_supports': self_supports,
              'dynamic_saturation_scope': 'any-hard46 and any-side50 use x=m or y=m after interface-specific restriction to W, not saturation in the fixed full support graph',
              'universal_template_scope': 'If opposite retained ports exceed the surviving fixed missing-edge budget in some coordinate, a common protected edge follows. Existence of such a coordinate is finite evidence for51/53, not yet an analytic all-interface theorem.',
              'HC_search': False, 'opponent_cycle_edges_computed': False,
              'actual_protected_edge_intersection_computed': False,
              'full_fibre_graphs_recomputed': False}
    output = BASE / 'hard-support-templates-results-v3.json'
    output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'coverage': {g: {k:v for k,v in s.items() if k != 'legal_support_uncovered'}
                        for g,s in summaries.items()},
                      'fixed_preferred_failure_count': len(fixed_failures),
                      'canonical_hard_boundary_groups': len(group_summary),
                      'hard_side_incidence_count': len(all_side_profiles),
                      'profile_multiplicity_histogram': dict(Counter(s['profile_count'] for s in group_summary)),
                      'self_support_shapes': [s['support_graph_shape'] for s in self_supports]}, indent=2))


if __name__ == '__main__':
    main()
