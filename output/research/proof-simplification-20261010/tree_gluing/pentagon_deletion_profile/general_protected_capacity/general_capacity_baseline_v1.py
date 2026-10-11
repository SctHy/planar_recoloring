#!/usr/bin/env python3
"""Full-fibre capacity for all 313 selected protected-base interfaces.

No HC search and no actual K/L or A/B edge intersection are computed.
HH vectors are compared exactly against the independently audited study.
"""
from collections import Counter
from itertools import product, permutations
from pathlib import Path
import hashlib
import json
import re
import time

BASE = Path(__file__).resolve().parent
RESEARCH = BASE.parents[2]
SOURCE = RESEARCH / 'continuation-6/final/planar_recoloring_hamilton_thresholds.tex'
EXPECTED_SOURCE = '7a90f79db489447b0bad3019217fd369a5cc25986288247981cbe7f3462acba3'
STANDARD = ('00000', '00001', '00011', '00012', '00101', '00102',
            '00112', '00121', '00123', '01012', '01023', '00004',
            '00014', '00104', '00114', '00124', '01014', '01024',
            '01104', '01124', '01204', '01234')
HARD = {'00001', '00112'}
PERMS = tuple(permutations(range(4)))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def edge(x, y):
    return tuple(sorted((x, y)))


def coordinate(e):
    x, y = e
    changed = [j for j in range(5) if x[j] != y[j]]
    assert len(changed) == 1
    return changed[0]


def cycle_edges(c):
    assert len(c) == len(set(c))
    es = {edge(x, c[(i + 1) % len(c)]) for i, x in enumerate(c)}
    assert len(es) == len(c)
    for e in es:
        coordinate(e)
    return es


def transform(x, g):
    s, eps, p = g
    return tuple(4 if x[(s + eps * j) % 5] == 4 else p[x[(s + eps * j) % 5]] for j in range(5))


def normalize(t):
    for s in range(5):
        for eps in (1, -1):
            for p in PERMS:
                nt = ''.join(map(str, transform(t, (s, eps, p))))
                if nt in STANDARD:
                    return nt, (s, eps, p)
    raise AssertionError(t)


def restore(x, g):
    s, eps, p = g
    inv = tuple(p.index(c) for c in range(4))
    result = [None] * 5
    for j in range(5):
        result[(s + eps * j) % 5] = inv[x[j]]
    return tuple(result)


def legal(t):
    return {x for x in product(range(4), repeat=5)
            if all(x[j] != x[(j + 1) % 5] for j in range(5))
            and all(t[j] == 4 or x[j] != t[j] for j in range(5))}


def raw_edges(U):
    result = set()
    for x in U:
        for j in range(5):
            for c in range(4):
                if c == x[j]:
                    continue
                y = x[:j] + (c,) + x[j + 1:]
                if y in U:
                    result.add(edge(x, y))
    return result


def component_sets(vertices, es):
    adj = {x: set() for x in vertices}
    for x, y in es:
        adj[x].add(y)
        adj[y].add(x)
    unseen, components = set(vertices), []
    while unseen:
        start = unseen.pop()
        seen, stack = {start}, [start]
        while stack:
            x = stack.pop()
            for y in adj[x] & unseen:
                unseen.remove(y)
                seen.add(y)
                stack.append(y)
        components.append(frozenset(seen))
    return set(components)


def counts(es):
    c = Counter(map(coordinate, es))
    return [c[j] for j in range(5)]


def load_components(blocks):
    def words(name, width=5):
        return [tuple(map(int, w)) for w in re.findall(rf'\b[0-3]{{{width}}}\b', blocks[name])]

    def edge_words(name):
        return {edge(tuple(map(int, x)), tuple(map(int, y)))
                for x, y in re.findall(r'\b([0-3]{5})-([0-3]{5})\b', blocks[name])}

    components, metadata = {}, []
    constant = words('FACTOR-00000')
    assert len(constant) == 30
    for t in STANDARD:
        all_states = legal(tuple(map(int, t)))
        G = raw_edges(all_states)
        actual_components = component_sets(all_states, G)
        if t == '00000':
            labelled = [set(constant[:15]), set(constant[15:])]
            assert set(map(frozenset, labelled)) == actual_components
        else:
            assert actual_components == {frozenset(all_states)}
            labelled = [all_states]
        for i, states in enumerate(labelled):
            key = f'{t}:{i}'
            if t in HARD:
                basis_block = 'COMMON-00001' if t == '00001' else 'PORTS-00112'
                A = edge_words(basis_block)
                assert len(A) == 13
                seed = words('PC2-00001' if t == '00001' else 'C2-00112', 6)
                assert len(seed) == 2 * len(states) and len(seed) == len(set(seed))
                seed_edges = {edge(x, seed[(j + 1) % len(seed)]) for j, x in enumerate(seed)}
                for row in (0, 1):
                    row_edges = {edge(x[1:], y[1:]) for x, y in seed_edges if x[0] == y[0] == row}
                    assert A <= row_edges
                basis_kind = 'hard-D13'
            elif t == '00000':
                basis_block = 'FACTOR-00000'
                A = cycle_edges(constant[15 * i:15 * (i + 1)])
                assert A == raw_edges(states)
                basis_kind = 'constant-C15'
            else:
                basis_block = ('FHC-' if '4' in t else 'C1-') + t
                c = words(basis_block)
                assert set(c) == states
                A = cycle_edges(c)
                basis_kind = 'Hamilton-cycle'
            P = edge_words(f'POOL-{t}-{i}')
            assert P <= A and A <= raw_edges(states)
            assert len(P) == (2 if t in HARD else 5 if t == '00000' else 8)
            components[key] = {'states': states, 'basis': A, 'pool': P, 'kind': basis_kind}
            metadata.append({'component': key, 'states': len(states), 'basis_edges': len(A),
                             'pool_edges': len(P), 'protected_edges': len(A) - len(P),
                             'basis_block': basis_block, 'kind': basis_kind})
    assert len(components) == 23
    return components, metadata


def group_name(source, target):
    if source.startswith('00000:'):
        return 'constant-source-30'
    if source[:5] in HARD or target[:5] in HARD:
        return 'nonconstant-source-hard-53'
    return 'HH-230'


def main():
    started = time.monotonic()
    frozen = BASE / 'phase6-protected-bases-input-v1.tex'
    provenance_path = BASE / 'input-provenance-v1.json'
    if not frozen.exists():
        assert sha(SOURCE) == EXPECTED_SOURCE
        keep = {'FACTOR-00000', 'COMMON-00001', 'PORTS-00112', 'PC2-00001', 'C2-00112', 'INTERFACES-ALL'}
        selected = [(name, body) for name, body in re.findall(r'% BEGIN ([A-Z0-9-]+)\n(.*?)% END \1', SOURCE.read_text(), re.S)
                    if name in keep or name.startswith(('C1-', 'FHC-', 'POOL-'))]
        frozen.write_text(''.join(f'% BEGIN {name}\n{body}% END {name}\n' for name, body in selected))
        provenance_path.write_text(json.dumps({'source': str(SOURCE), 'source_sha256': sha(SOURCE),
                                              'frozen_sha256': sha(frozen), 'block_count': len(selected)}, indent=2) + '\n')
    provenance = json.loads(provenance_path.read_text())
    assert sha(frozen) == provenance['frozen_sha256']
    blocks = dict(re.findall(r'% BEGIN ([A-Z0-9-]+)\n(.*?)% END \1', frozen.read_text(), re.S))
    components, metadata = load_components(blocks)
    cases = []
    for source, compA in components.items():
        t = tuple(map(int, source[:5]))
        statesA, A, P = (compA[k] for k in ('states', 'basis', 'pool'))
        for changed in range(5):
            if t[changed] == 4:
                continue
            for new in range(4):
                if new == t[changed]:
                    continue
                s = t[:changed] + (new,) + t[changed + 1:]
                nt, g = normalize(s)
                for target, compB in components.items():
                    if target[:5] != nt:
                        continue
                    statesB = {restore(x, g) for x in compB['states']}
                    U = statesA & statesB
                    if not U:
                        continue
                    B = {edge(restore(x, g), restore(y, g)) for x, y in compB['basis']}
                    Q = {edge(restore(x, g), restore(y, g)) for x, y in compB['pool']}
                    H = raw_edges(U)
                    F = (P | Q) & H
                    a, b, m, f, rA, rB = map(counts, (A & H, B & H, H, F, A & F, B & F))
                    coarse = [a[j] + b[j] - m[j] - f[j] for j in range(5)]
                    refined = [a[j] + b[j] - m[j] - rA[j] - rB[j] + f[j] for j in range(5)]
                    assert all(refined[j] >= coarse[j] for j in range(5))
                    cases.append({'source': source, 'changed_position': changed, 'new_colour': new,
                                  'target': target, 'group': group_name(source, target), 'normalizer': g,
                                  'common_full_component_states': len(U),
                                  'a': a, 'b': b, 'm': m, 'f': f, 'rA': rA, 'rB': rB,
                                  'coarse_bounds': coarse, 'refined_bounds': refined,
                                  'coarse_hit_coordinates': [j for j in range(5) if coarse[j] >= 1],
                                  'refined_hit_coordinates': [j for j in range(5) if refined[j] >= 1]})
    assert len(cases) == 313
    expected_groups = {'HH-230': 230, 'nonconstant-source-hard-53': 53, 'constant-source-30': 30}
    assert dict(Counter(x['group'] for x in cases)) == expected_groups

    # Compare all 283 nonconstant case indices with the manuscript list,
    # ignoring its witness endpoints rather than computing protected overlap.
    index_pattern = r'([0-4]{5}:[01])\s+([0-4])\s+([0-3])\s+([0-4]{5}:[01])\s+[0-3]{5}-[0-3]{5}'
    printed = {(src, int(j), int(q), tgt) for src, j, q, tgt in re.findall(index_pattern, blocks['INTERFACES-ALL'])}
    nonconstant = {(x['source'], x['changed_position'], x['new_colour'], x['target'])
                   for x in cases if not x['source'].startswith('00000:')}
    assert len(printed) == 283 and printed == nonconstant

    prior_path = BASE.parent / 'hh-coordinate-capacity-results-v1.json'
    prior = json.loads(prior_path.read_text())
    prior_cases = {(x['source'], x['changed_position'], x['new_colour'], x['target']): x for x in prior['cases']}
    checked_HH = 0
    for case in cases:
        if case['group'] != 'HH-230':
            continue
        old = prior_cases[(case['source'], case['changed_position'], case['new_colour'], case['target'])]
        for field in ('a', 'b', 'm', 'f', 'coarse_bounds', 'refined_bounds', 'normalizer'):
            assert json.loads(json.dumps(case[field])) == old[field], (case, field)
        assert case['rA'] == old['rC'] and case['rB'] == old['rD']
        checked_HH += 1
    assert checked_HH == 230
    coverage = {}
    for group in expected_groups:
        subset = [x for x in cases if x['group'] == group]
        coverage[group] = {'total': len(subset)}
        for mode in ('coarse', 'refined'):
            covered = sum(bool(x[mode + '_hit_coordinates']) for x in subset)
            coverage[group][mode + '_covered'] = covered
            coverage[group][mode + '_uncovered'] = len(subset) - covered
            coverage[group][mode + '_changed_coordinate_covered'] = sum(x['changed_position'] in x[mode + '_hit_coordinates'] for x in subset)
    assert coverage['HH-230']['refined_covered'] == 222
    result = {
        'status': 'COMPLETE_BOUNDED_CAPACITY_COUNT',
        'scope': 'All 313 standard-source interfaces. Full common component states form H. Bases are C1/FHC/C15 or actual hard D13; K=base minus pool.',
        'proof_boundary': 'The general capacity inequality is proved separately. Numeric coverage is frozen finite evidence, not an analytic classification theorem.',
        'source_provenance': provenance, 'script_sha256': sha(Path(__file__)),
        'lemma_sha256': sha(BASE / 'general_capacity_lemma_v1.tex'),
        'HH_inheritance_record': {str(prior_path): sha(prior_path)},
        'HH_vectors_exactly_inherited': checked_HH,
        'printed_nonconstant_indices_exactly_matched': len(printed),
        'component_metadata': metadata, 'coverage_by_group': coverage,
        'interface_count': len(cases),
        'coarse_covered': sum(bool(x['coarse_hit_coordinates']) for x in cases),
        'refined_covered': sum(bool(x['refined_hit_coordinates']) for x in cases),
        'common_state_minimum': min(x['common_full_component_states'] for x in cases),
        'cases': cases,
        'actual_protected_edge_intersection_computed': False, 'actual_base_edge_intersection_computed': False,
        'HC_search': False, 'P3_retention_reproved': False,
        'elapsed_seconds': time.monotonic() - started,
    }
    output = BASE / 'general-capacity-baseline-results-v1.json'
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'interface_count': result['interface_count'], 'coverage': coverage,
                      'elapsed_seconds': result['elapsed_seconds']}, indent=2))
    print('results:', output)


if __name__ == '__main__':
    main()
