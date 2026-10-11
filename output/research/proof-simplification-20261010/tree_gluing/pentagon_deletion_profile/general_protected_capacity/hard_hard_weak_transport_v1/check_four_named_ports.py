"""Four designated hard--hard port identities; never pairwise-K intersections."""
from itertools import permutations
from pathlib import Path
import hashlib
import json
import platform
import re

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
ROOT = BASE.parents[5]
MANIFEST_SHA = 'b5b5e4e62dd213f52174a80b5f11d7180590c909ee5c3a3d6af90593eabd2c51'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def edge(a, b):
    return tuple(sorted((a, b)))


def blocks(text):
    return dict(re.findall(r'% BEGIN ([A-Z0-9-]+)\n(.*?)% END \1', text, re.S))


def legal(v, t):
    return all(v[i] != v[(i + 1) % 5] and v[i] != t[i] for i in range(5))


def forward(v, g):
    offset, direction, p = g
    return ''.join(str(p[int(v[(offset + direction * i) % 5])]) for i in range(5))


def restore(v, g):
    offset, direction, p = g
    out = [''] * 5
    inverse = {str(p[i]): str(i) for i in range(4)}
    for i in range(5):
        out[(offset + direction * i) % 5] = inverse[v[i]]
    return ''.join(out)


def main():
    manifest_path = BASE / 'frozen-manifest-v6.json'
    assert sha(manifest_path) == MANIFEST_SHA
    manifest = json.loads(manifest_path.read_text())
    inputs = ['phase6-protected-bases-input-v1.tex', 'general-capacity-baseline-results-v1.json',
              'transport-variant-subsets-results-v4.json', 'hard-support-templates-results-v3.json',
              'residual-weak-transport-results-v6.json']
    for name in inputs:
        assert sha(BASE / name) == manifest[name]
    source_path = BASE / inputs[0]
    literal = blocks(source_path.read_text())
    main_path = ROOT / 'planar_recoloring_hamilton_thresholds.tex'
    actual_main = blocks(main_path.read_text())
    names = ['COMMON-00001', 'POOL-00001-0', 'PORTS-00112', 'POOL-00112-0']
    assert all(literal[name] == actual_main[name] for name in names)
    standard = {name.split('-')[1] for name in literal if name.startswith(('C1-', 'FHC-'))}
    standard |= {'00000', '00001', '00112'}

    def pairs(name):
        return {edge(a, b) for a, b in re.findall(r'([0-3]{5})-([0-3]{5})', literal[name])}

    bases = {'00001': pairs('COMMON-00001'), '00112': pairs('PORTS-00112')}
    pools = {t: pairs('POOL-' + t + '-0') for t in bases}
    K = {t: bases[t] - pools[t] for t in bases}
    assert all(len(K[t]) == 11 for t in K)

    def first(u):
        for offset in range(5):
            for direction in (1, -1):
                for p in permutations(range(4)):
                    g = [offset, direction, list(p)]
                    n = forward(u, g)
                    if n in standard:
                        return n, g
        raise AssertionError(u)

    old = json.loads((BASE / inputs[1]).read_text())
    groups = {(r['hard_type'], r['canonical_changed_position'], r['opposite_colour']): r
              for r in json.loads((BASE / inputs[2]).read_text())['groups']}
    prior = json.loads((BASE / inputs[4]).read_text())
    specifications = [
        ('00001', 4, 2, ('13210', '23210'), ('13120', '23120'), [0, 1, [0, 2, 1, 3]]),
        ('00001', 4, 3, ('12310', '32310'), ('13120', '23120'), [0, 1, [0, 2, 3, 1]]),
        ('00112', 0, 2, ('12023', '13023'), ('13020', '13023'), [0, -1, [2, 1, 0, 3]]),
        ('00112', 3, 2, ('13030', '13230'), ('32030', '32031'), [1, -1, [0, 2, 1, 3]])]
    records = []
    membership_queries = set()
    for t, j, q, e, f, expected_map in specifications:
        e, f = edge(*e), edge(*f)
        u = t[:j] + str(q) + t[j + 1:]
        n, g = first(u)
        assert n == t and g == expected_map
        case, = [c for c in old['cases'] if (c['source'], c['changed_position'], c['new_colour'], c['target'])
                 == (t + ':0', j, q, t + ':0')]
        assert case['normalizer'] == g
        assert all(legal(w, t) and legal(w, u) for w in e)
        assert sum(a != b for a, b in zip(*e)) == 1
        assert edge(*(forward(w, g) for w in e)) == f
        assert edge(*(restore(w, g) for w in f)) == e
        assert all(legal(w, t) for w in f)
        for role, port in [('source', e), ('target', f)]:
            assert port in bases[t] and port not in pools[t] and port in K[t]
            membership_queries.add((t, port))
        group = groups[(t + ':0', j, q)]
        failed_bound = {
            'scope': 'inherited v4 uniform relative-map-group missing-edge criterion, not an actual-pair nonintersection claim',
            'minimum_retained_counts': group['minimum_retained_counts'],
            'surviving_missing_budget': group['surviving_missing_budget'],
            'uniform_count_hit_coordinates': group['uniform_count_hit_coordinates'],
            'best_uniform_coordinate_union': group['best_uniform_coordinate_union']}
        records.append({'case': [t + ':0', j, q, t + ':0'], 'actual_target_boundary': u,
                        'first_normalizer': g, 'matches_original_case_map': True,
                        'source_port': list(e), 'target_port': list(f),
                        'source_member_outside_pool': True, 'target_member_outside_pool': True,
                        'forward_identity_and_inverse_identity': True,
                        'source_port_legal_for_both_actual_boundaries': True,
                        'inherited_capacity_boundary': failed_bound})
    new_cases = {tuple(r['case']) for r in records}
    previous_cases = {tuple(c) for c in prior['ending_union_cases']}
    remaining = {tuple(c) for c in prior['ending_remaining']}
    universe = {tuple(c['case']) for c in json.loads((BASE / inputs[3]).read_text())['hard_side_profiles_all53']}
    assert len(new_cases) == 4 and new_cases == remaining
    assert len(previous_cases) == 49 and not previous_cases & new_cases
    assert previous_cases | new_cases == universe and len(universe) == 53
    assert len(membership_queries) == 7
    result = {'status': 'PASS_FOUR_DESIGNATED_HARD_HARD_PORT_IDENTITIES', 'python': platform.python_version(),
              'source_basis_input_sha256': sha(source_path), 'bound_manifest_v6_sha256': MANIFEST_SHA,
              'input_sha256': {name: sha(BASE / name) for name in inputs},
              'actual_main_sha256_at_readback': sha(main_path), 'four_live_hard_basis_pool_blocks_exact': True,
              'records': records, 'designated_actual_interfaces': 4, 'distinct_named_standard_K_memberships': 7,
              'previous_covered_case_identities': 49, 'final_case_identity_union': 53,
              'all53_single_symbolic_classification_claimed': False,
              'mathematical_scope': 'four fixed prescribed first maps and actual hard common-port sets; prior49 routes inherited with their own scopes',
              'HC_hypothesis_used': False, 'HC_search': False, 'full_fibre_generated': False,
              'full_paired_K_intersection_enumerated': False, 'prior_producers_rerun': False,
              'main_edited': False}
    out = HERE / 'four-named-port-results.json'
    assert not out.exists(), 'preserve existing output'
    out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('records', 'input_sha256')}, indent=2))


if __name__ == '__main__':
    main()
