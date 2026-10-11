#!/usr/bin/env python3
"""Independent four-edge/two-map check; no all-interface or HC rerun.

Read the frozen literal bases directly. Reconstruct only the twenty-endpoint
00112 support needed to identify F. Check designated ports against the one
ordinary 00012 cycle and its pool. The v4 comparison is read, not replayed.
"""
from itertools import combinations
from pathlib import Path
import hashlib
import json
import platform
import re
import sys

BASE = Path(__file__).resolve().parent
INPUT = BASE / 'phase6-protected-bases-input-v1.tex'
EXPECTED_INPUT_SHA = '81d34d8638c0cdeebbe62c40fed700f4836696cca560199226750e909d1d6776'
MAPS = [[0, 1, [0, 1, 2, 3]], [2, -1, [0, 2, 1, 3]]]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def edge(a, b):
    return tuple(sorted((a, b)))


def apply(word, mapping):
    start, sign, perm = mapping
    return ''.join(str(perm[int(word[(start + sign*j) % 5])]) for j in range(5))


def inverse(mapping):
    start, sign, perm = mapping
    return [(-sign*start) % 5, sign, [perm.index(c) for c in range(4)]]


def map_edge(e, mapping):
    return edge(*(apply(w, mapping) for w in e))


def legal(word, boundary):
    return (all(word[j] != word[(j+1) % 5] for j in range(5))
            and all(word[j] != boundary[j] for j in range(5)))


def coordinate(e):
    changed = [j for j in range(5) if e[0][j] != e[1][j]]
    assert len(changed) == 1
    return changed[0]


def main():
    assert sha(INPUT) == EXPECTED_INPUT_SHA
    raw = INPUT.read_text()

    def block(name):
        found = re.findall(r'% BEGIN '+re.escape(name)+r'\n(.*?)% END '+re.escape(name), raw, re.S)
        assert len(found) == 1
        return found[0]

    def ports(name):
        return {edge(a,b) for a,b in re.findall(r'([0-3]{5})-([0-3]{5})', block(name))}

    hard_base = ports('PORTS-00112')
    hard_pool = ports('POOL-00112-0')
    assert hard_pool <= hard_base
    K = hard_base-hard_pool
    endpoints = {w for e in K for w in e}
    assert all(legal(w, '00112') for w in endpoints)
    J = {edge(a,b) for a,b in combinations(sorted(endpoints), 2)
         if sum(x != y for x,y in zip(a,b)) == 1}
    Ju = {e for e in J if all(legal(w, '00012') for w in e)}
    assert (len(K), len(endpoints), len(J), len(Ju)) == (11,20,17,9)
    F = {edge(a,b) for a,b in [('12320','32320'),('13230','23230'),
                              ('21301','31301'),('31201','31301')]}
    assert F == {e for e in Ju if coordinate(e) in (0,2)}
    assert len(F) == 4 and len(F & K) == 3
    words = re.findall(r'\b[0-3]{5}\b', block('C1-00012'))
    assert len(words) == len(set(words))
    ordinary = {edge(a,b) for a,b in zip(words, words[1:]+words[:1])}
    ordinary_pool = ports('POOL-00012-0')
    assert ordinary_pool <= ordinary
    L = ordinary-ordinary_pool
    assert all(legal(w, '00012') for e in ordinary for w in e)
    assert all(len([j for j in range(5) if e[0][j] != e[1][j]]) == 1 for e in ordinary)
    fixed_ports = {edge(a,b) for a,b in [('12320','32320'),('13230','23230'),('13103','13203')]}
    assert fixed_ports <= L
    common_port = edge('13230','23230')
    assert common_port in K
    checks = []
    for mapping in MAPS:
        start, sign, perm = mapping
        assert 0 <= start < 5 and sign in (-1,1) and sorted(perm) == list(range(4))
        assert apply('00012', mapping) == '00012'
        assert all(apply(apply(w,mapping),inverse(mapping)) == w for w in endpoints)
        images = {e:map_edge(e,mapping) for e in F}
        assert all(all(legal(w,'00012') for w in image) for image in images.values())
        retained = [e for e,image in images.items() if image in L]
        assert len(retained) == 2
        image = map_edge(common_port,mapping)
        assert image in ordinary and image not in ordinary_pool
        checks.append({'map':mapping, 'boundary_image':apply('00012',mapping),
                       'retained_F_edges':sorted(retained), 'F_retained_count':len(retained),
                       'common_port_image':image,'common_port_image_in_cycle':True,
                       'common_port_image_outside_pool':True})
    assert checks[0]['common_port_image'] == common_port
    assert checks[1]['common_port_image'] == edge('13103','13203')
    old = json.loads((BASE/'transport-variant-subsets-results-v4.json').read_text())
    group = next(g for g in old['groups'] if
        (g['hard_type'],g['canonical_changed_position'],g['opposite_colour']) == ('00112:0',2,0))
    assert group['incidence_count'] == 3
    assert {json.dumps(v['relative_opposite_normalizer']) for v in group['variants']} == {
        json.dumps(mapping) for mapping in MAPS}
    witness_rows = re.findall(r'([0-3]{5}:\d)\s+(\d)\s+(\d)\s+([0-3]{5}:\d)\s+([0-3]{5})-([0-3]{5})',
                              block('INTERFACES-ALL'))
    witness_lookup = {(a,int(r),int(c),b):edge(x,y) for a,r,c,b,x,y in witness_rows}
    comparisons = []
    for variant in group['variants']:
        mapping = variant['relative_opposite_normalizer']
        for case in variant['cases']:
            original = witness_lookup[tuple(case)]
            assert original == edge('12320','32320')
            hard_original = original if case[0] == '00112:0' else map_edge(original,inverse(mapping))
            new_physical = common_port if case[0] == '00112:0' else map_edge(common_port,mapping)
            comparisons.append({'case':case,'original_printed_witness':original,
                'original_witness_in_hard_coordinates':hard_original,
                'new_common_hard_coordinate_port':common_port,'new_physical_witness':new_physical})
    output = {'status':'BOUNDED_TWO_MAP_FAMILY_MEMBERSHIP_CHECK_PASSED',
        'input_sha256':{INPUT.name:sha(INPUT),
            'transport-variant-subsets-results-v4.json':sha(BASE/'transport-variant-subsets-results-v4.json')},
        'script_sha256':sha(Path(__file__)),
        'runtime':{'executable':sys.executable,'python_version':platform.python_version()},
        'hard_type':'00112:0','opposite_boundary':'00012',
        'hard_support':{'protected_edge_count':len(K),'endpoint_count':len(endpoints),
                        'edge_count':len(J),'legal_edge_count':len(Ju)},
        'F':sorted(F),'F_hard_edges':sorted(F & K),'F_hard_count':len(F & K),
        'opposite_template_ports':sorted(fixed_ports),'map_checks':checks,
        'capacity_bound':3+2-4,'weak_transport_common_hard_port':common_port,
        'two_membership_argument_passed':True,'actual_witness_comparison':comparisons,
        'original_full_paired_protected_intersection_enumerated':False,
        'all_30_group_memberships_replayed':False,'all_313_interface_replayed':False,
        'full_fibre_generated':False,'HC_search':False,
        'scope':'Only the named F/K and designated port membership for the two recorded maps. No assertion for other maps or arbitrary cycles.'}
    destination = BASE/'transport-family-check-results-v4.json'
    assert not destination.exists(), 'preserve an existing execution result'
    destination.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({'status':output['status'],'capacity_bound':output['capacity_bound'],
        'common_hard_port':common_port,'ordinary_port_images':[c['common_port_image'] for c in checks],
        'actual_interface_count':len(comparisons),'result_file':destination.name},indent=2))


if __name__ == '__main__':
    main()
