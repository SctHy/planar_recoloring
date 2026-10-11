#!/usr/bin/env python3
"""Independent literal check of the one 00123 reflection certificate only."""
from pathlib import Path
import hashlib
import json
import re

BASE = Path(__file__).resolve().parent
PROJECT = Path('/Users/huahua815/Downloads/planar_recoloring')
SOURCE = PROJECT / 'output/research/proof-simplification-20261010/continuation-6/final/planar_recoloring_hamilton_thresholds.tex'
CANDIDATE = BASE.parent / 'square-capacity-candidate-v1.tex'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def block(text, name):
    return re.search(r'% BEGIN ' + re.escape(name) + r'\n(.*?)% END ' + re.escape(name), text, re.S).group(1)


def edge(a, b):
    return tuple(sorted((a, b)))


def g(w):
    return ''.join(str(3-int(w[(-i) % 5])) for i in range(5))


def legal(w, boundary):
    return all(w[i] != boundary[i] and w[i] != w[(i+1) % 5] for i in range(5))


def main():
    text = SOURCE.read_text()
    cycle = re.findall(r'\b[0-3]{5}\b', block(text, 'C1-00123'))
    pool = {edge(a, b) for a, b in re.findall(r'([0-3]{5})-([0-3]{5})', block(text, 'POOL-00123-0'))}
    assert len(cycle) == len(set(cycle)) == 57 and len(pool) == 8
    cycle_edges = {edge(cycle[i], cycle[(i+1) % len(cycle)]) for i in range(len(cycle))}
    assert pool <= cycle_edges
    S = {'2'+x+'2'+y+'0' for x in '13' for y in '13'}
    T = {'13'+x+'1'+y for x in '02' for y in '02'}
    assert all(legal(w, b) for w in S | T for b in ('00123', '30123'))
    assert {g(w) for w in S} == T and {g(w) for w in T} == S
    assert all(g(g(w)) == w for w in S | T)
    assert g('30123') == '00123'
    assert g('23210') == '13210' and g('21230') == '13012'
    # Both square induced edge sets and both cycle restrictions are checked separately.
    restrictions = []
    for vertices, path, isolated, neighbours in [
        (S, ['21210', '23210', '23230'], '21230', ['31230', '21231']),
        (T, ['13010', '13210', '13212'], '13012', ['13032', '12012']),
    ]:
        square_edges = {edge(a, b) for a in vertices for b in vertices
                        if sum(x != y for x, y in zip(a, b)) == 1}
        assert len(square_edges) == 4
        selected = {e for e in cycle_edges if e[0] in vertices and e[1] in vertices}
        expected = {edge(path[0], path[1]), edge(path[1], path[2])}
        assert selected == expected
        at = cycle.index(isolated)
        actual_neighbours = {cycle[(at-1) % len(cycle)], cycle[(at+1) % len(cycle)]}
        assert actual_neighbours == set(neighbours) and actual_neighbours.isdisjoint(vertices)
        assert pool.isdisjoint(square_edges)
        restrictions.append({'vertices': sorted(vertices), 'square_edges': sorted(square_edges),
                             'path': path, 'isolated_corner': isolated,
                             'cycle_neighbours': sorted(actual_neighbours),
                             'independent_retained_edge_count': len(selected),
                             'pool_square_edge_count': 0})
    # This normalizer is read as index data only; no witness edge is inspected.
    match = [c for c in json.loads((BASE.parent.parent / 'general_protected_capacity/port-support-capacity-results-v2.json').read_text())['cases']
             if (c['source'], c['changed_position'], c['new_colour'], c['target']) == ('00123:0', 0, 3, '00123:0')]
    assert len(match) == 1 and match[0]['normalizer'] == [0, -1, [3, 2, 1, 0]]
    result = {'status': 'PASS_ONE_SELECTED_REFLECTION_PAIR',
              'source_sha256': sha(SOURCE), 'candidate_sha256': sha(CANDIDATE),
              'script_sha256': sha(Path(__file__)), 'restrictions': restrictions,
              'restored_target_retains_two_edges_and_omits_same_corner': True,
              'capacity_after_shared_corner_deletion': 2+2-2,
              'full_graph_scan': False, 'HC_search': False,
              'actual_cycle_edge_intersection_computed': False,
              'scope': 'Only the displayed 00123 source cycle, source pool and prescribed involution; no arbitrary-cycle or arbitrary-normalizer assertion.'}
    (BASE / 'review-00123-results-v1.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
