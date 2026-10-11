"""Small exact necessary-condition screen; no Hamilton or seed search."""
from pathlib import Path
from itertools import combinations, product
from collections import Counter
import hashlib, json, re

HERE = Path(__file__).resolve().parent
BAD = {'12312', '12313', '13212', '13213'}
REMOVED = ('12313', '12323')

def edge(a, b):
    return tuple(sorted((a, b)))

def valid_forest(es):
    deg = Counter(v for e in es for v in e)
    if max(deg.values(), default=0) > 2:
        return False
    parent = {}
    def find(v):
        parent.setdefault(v, v)
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v
    for u, v in es:
        a, b = find(u), find(v)
        if a == b:
            return False
        parent[a] = b
    return True

def recolour(e, permutation):
    return edge(*(''.join(str(permutation[int(c)]) for c in v) for v in e))

def main():
    inp = HERE / 'original-literal-input.tex'
    text = inp.read_text()
    def block(name):
        return re.search('% BEGIN ' + name + '\n(.*?)% END ' + name, text, re.S).group(1)
    def edges(name):
        return {edge(u, v) for u, v in re.findall(r'([0-3]{5})-([0-3]{5})', block(name))}
    vertices = sorted(''.join(map(str, w)) for w in product(range(4), repeat=5)
                      if all(w[i] != w[(i+1)%5] and str(w[i]) != '00001'[i] for i in range(5)))
    raw = {edge(u, v) for u, v in combinations(vertices, 2)
           if sum(a != b for a, b in zip(u, v)) == 1}
    remaining = set(vertices) - BAD
    H = {e for e in raw if set(e) <= remaining}
    degree = Counter(v for e in H for v in e)
    assert len(remaining) == 40 and len(H) == 64 and min(degree[v] for v in remaining) == 2
    old_pool = edges('POOL-00001-0')
    old_K = edges('COMMON-00001') - old_pool
    K0 = old_K - {REMOVED}
    reserves = sorted(e for e in old_pool if not set(e) & BAD)
    assert len(K0) == 11 and len(reserves) == 6
    # Interface target-normalizer inverse maps for pos4->2 and pos4->3.
    # First map is its own inverse; second inverse of (0,2,3,1) is (0,3,1,2).
    inverse_maps = ((0, 2, 1, 3), (0, 3, 1, 2))
    def interfaces_pass(K):
        return all(K & {recolour(e, p) for e in K} for p in inverse_maps)
    def witnesses(K):
        return [sorted(K & {recolour(e, p) for e in K}) for p in inverse_maps]
    assert not interfaces_pass(K0)
    possible_additions = sorted(H - K0)
    screens = []
    for number in (0, 1, 2):
        survivors = []
        passed_interface = 0
        passed_K_forest = 0
        for additions in combinations(possible_additions, number):
            K = K0 | set(additions)
            if not interfaces_pass(K):
                continue
            passed_interface += 1
            if not valid_forest(K):
                continue
            passed_K_forest += 1
            pools = []
            for R in combinations(reserves, 2):
                if not set(R) & K and valid_forest(K | set(R)):
                    pools.append(R)
            if pools:
                survivors.append({'added_K_edges': additions,
                                  'K_size': len(K),
                                  'interface_common_edges': witnesses(K),
                                  'compatible_two_old_reserve_pairs': pools})
        screens.append({'number_of_added_K_edges': number,
                        'candidate_count': len(list(combinations(possible_additions, number))),
                        'pass_both_empty_interfaces': passed_interface,
                        'also_K_is_linear_forest': passed_K_forest,
                        'also_some_two_old_reserves_fit_linear_forest': len(survivors),
                        'survivors': survivors})
        if survivors:
            break
    result = {
        'H40_vertices': sorted(remaining), 'H40_edges': sorted(H),
        'H40_vertex_count': len(remaining), 'H40_edge_count': len(H),
        'H40_degree_distribution': dict(sorted(Counter(degree[v] for v in remaining).items())),
        'H40_has_no_leaves': True,
        'degree_two_vertex_examples': {v: sorted(next(w for w in e if w != v) for e in H if v in e)
                                       for v in sorted(remaining) if degree[v] == 2},
        'failed_guess': 'Removing the four YY endpoints leaves four leaf vertices; this is false.',
        'no_t_ge_4_lower_bound_claimed': True,
        'K0': sorted(K0), 'six_usable_old_reserves': reserves,
        'structural_K_augmentation_screen': screens,
        'Hamilton_or_seed_search_performed': False,
        'scope': 'Necessary membership, degree<=2 and no forced-cycle checks only; existence of PC2,PC3 or insertion is not claimed.',
        'input_sha256': hashlib.sha256(inp.read_bytes()).hexdigest()
    }
    (HERE / 'redesign-degree-results-v1.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('H40_vertices', 'H40_edges', 'K0', 'degree_two_vertex_examples')}, indent=2))

if __name__ == '__main__':
    main()
