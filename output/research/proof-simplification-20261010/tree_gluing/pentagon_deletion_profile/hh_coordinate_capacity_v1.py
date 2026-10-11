#!/usr/bin/env python3
"""Bounded selected-cycle coordinate-capacity study, no HC search.

For the HH interfaces only, K is the selected HC minus its pool.
No actual intersection of the two selected cycle edge sets is computed.
The script records independent counts a,b,m,f,rC,rD for each coordinate.
"""
from collections import Counter
from itertools import product, permutations
from pathlib import Path
import hashlib
import json
import re
import time

BASE = Path(__file__).resolve().parent
SOURCE = BASE.parents[1] / 'continuation-6/final/planar_recoloring_hamilton_thresholds.tex'
STANDARD = ('00000', '00001', '00011', '00012', '00101', '00102',
            '00112', '00121', '00123', '01012', '01023', '00004',
            '00014', '00104', '00114', '00124', '01014', '01024',
            '01104', '01124', '01204', '01234')
HARD = {'00001', '00112'}
PERMS = tuple(permutations(range(4)))


def edge(x, y):
    return tuple(sorted((x, y)))


def transform(x, g):
    s, eps, p = g
    return tuple(4 if x[(s + eps * i) % 5] == 4 else p[x[(s + eps * i) % 5]] for i in range(5))


def normalize(t):
    for s in range(5):
        for eps in (1, -1):
            for p in PERMS:
                n = ''.join(map(str, transform(t, (s, eps, p))))
                if n in STANDARD:
                    return n, (s, eps, p)
    raise AssertionError(t)


def restore(x, g):
    s, eps, p = g
    inv = tuple(p.index(i) for i in range(4))
    result = [None] * 5
    for i in range(5):
        result[(s + eps * i) % 5] = inv[x[i]]
    return tuple(result)


def coordinate(e):
    x, y = e
    changed = [i for i in range(5) if x[i] != y[i]]
    assert len(changed) == 1
    return changed[0]


def cycle_edges(c):
    assert len(c) == len(set(c))
    result = {edge(x, c[(i + 1) % len(c)]) for i, x in enumerate(c)}
    for e in result:
        coordinate(e)
    return result


def legal(t):
    return {x for x in product(range(4), repeat=5)
            if all(x[i] != x[(i + 1) % 5] for i in range(5))
            and all(t[i] == 4 or x[i] != t[i] for i in range(5))}


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


def counts(edges):
    counted = Counter(map(coordinate, edges))
    return [counted[j] for j in range(5)]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    started = time.monotonic()
    frozen = BASE / 'phase6-selected-input-v2.tex'
    provenance = BASE / 'phase6-input-provenance-v2.json'
    if not frozen.exists():
        src = SOURCE.read_text()
        selected = [(name, body) for name, body in
                    re.findall(r'% BEGIN ([A-Z0-9-]+)\n(.*?)% END \1', src, re.S)
                    if name.startswith('C1-') or name.startswith('FHC-') or name.startswith('POOL-') or name == 'FACTOR-00000']
        frozen.write_text(''.join(f'% BEGIN {name}\n{body}% END {name}\n' for name, body in selected))
        provenance.write_text(json.dumps({'source': str(SOURCE), 'source_sha256': sha(SOURCE),
                                         'frozen_sha256': sha(frozen), 'block_count': len(selected)}, indent=2) + '\n')
    prov = json.loads(provenance.read_text())
    assert sha(frozen) == prov['frozen_sha256']
    blocks = dict(re.findall(r'% BEGIN ([A-Z0-9-]+)\n(.*?)% END \1', frozen.read_text(), re.S))

    def words(name):
        return [tuple(map(int, w)) for w in re.findall(r'\b[0-3]{5}\b', blocks[name])]

    def pool(name):
        return {edge(tuple(map(int, x)), tuple(map(int, y)))
                for x, y in re.findall(r'\b([0-3]{5})-([0-3]{5})\b', blocks[name])}

    hh = {}
    constant = words('FACTOR-00000')
    assert len(constant) == 30
    for t in STANDARD:
        if t in HARD:
            continue
        prefix = 'FHC-' if '4' in t else 'C1-'
        comp_words = [constant[:15], constant[15:]] if t == '00000' else [words(prefix + t)]
        assert set.union(*(set(c) for c in comp_words)) == legal(tuple(map(int, t)))
        for index, c in enumerate(comp_words):
            es, P = cycle_edges(c), pool(f'POOL-{t}-{index}')
            assert P <= es
            hh[f'{t}:{index}'] = (c, es, P)
    assert len(hh) == 21

    cases = []
    for source, (c, C, P) in hh.items():
        t = tuple(map(int, source[:5]))
        for changed in range(5):
            if t[changed] == 4:
                continue
            for new in range(4):
                if new == t[changed]:
                    continue
                s = t[:changed] + (new,) + t[changed + 1:]
                nt, g = normalize(s)
                if nt in HARD:
                    continue
                for target, (canonical_d, _, canonical_pool) in hh.items():
                    if target[:5] != nt:
                        continue
                    d = [restore(x, g) for x in canonical_d]
                    D = cycle_edges(d)
                    Q = {edge(restore(x, g), restore(y, g)) for x, y in canonical_pool}
                    U = set(c) & set(d)
                    if not U:
                        continue
                    H = raw_edges(U)
                    F = (P | Q) & H
                    a, b, m, f, rC, rD = map(counts, (C & H, D & H, H, F, C & F, D & F))
                    coarse = [a[j] + b[j] - m[j] - f[j] for j in range(5)]
                    refined = [a[j] + b[j] - m[j] - rC[j] - rD[j] + f[j] for j in range(5)]
                    assert all(refined[j] >= coarse[j] for j in range(5))
                    cases.append({'source': source, 'changed_position': changed, 'new_colour': new,
                                  'target': target, 'normalizer': g, 'common_vertices': len(U),
                                  'a': a, 'b': b, 'm': m, 'f': f, 'rC': rC, 'rD': rD,
                                  'coarse_bounds': coarse, 'refined_bounds': refined,
                                  'coarse_hit_coordinates': [j for j in range(5) if coarse[j] >= 1],
                                  'refined_hit_coordinates': [j for j in range(5) if refined[j] >= 1]})
    assert len(cases) == 230, len(cases)
    coarse_hits = [x for x in cases if x['coarse_hit_coordinates']]
    refined_hits = [x for x in cases if x['refined_hit_coordinates']]
    by_source = {}
    for case in cases:
        group = by_source.setdefault(case['source'], {'total': 0, 'coarse': 0, 'refined': 0})
        group['total'] += 1
        group['coarse'] += bool(case['coarse_hit_coordinates'])
        group['refined'] += bool(case['refined_hit_coordinates'])

    typical, = [x for x in cases if (x['source'], x['changed_position'], x['new_colour']) == ('00101:0', 0, 1)]
    assert typical['normalizer'] == (0, -1, (1, 0, 2, 3))
    assert (typical['a'][0], typical['b'][0], typical['m'][0], typical['f'][0]) == (6, 6, 7, 1)
    assert typical['coarse_bounds'][0] == typical['refined_bounds'][0] == 4
    result = {
        'verdict': 'COMPLETE_BOUNDED_COUNT',
        'scope': 'All 230 current HH selected-cycle interfaces only; K=C\\pool. Hard D\\pool components excluded.',
        'interpretation': 'A positive count yields a protected common edge by inclusion-exclusion once its literal counts are proved. Negative counts are inconclusive. This file is a computation record, not a new general theorem.',
        'source_provenance': prov,
        'script_sha256': sha(Path(__file__)),
        'typical_note_sha256': sha(BASE / 'typical_00101_coordinate_capacity_v2.tex'),
        'HH_components': len(hh), 'interface_count': len(cases),
        'coarse_covered': len(coarse_hits), 'refined_covered': len(refined_hits),
        'coarse_uncovered': len(cases) - len(coarse_hits), 'refined_uncovered': len(cases) - len(refined_hits),
        'coverage_by_source': by_source,
        'constant_source_HH_interfaces': sum(x['source'].startswith('00000') for x in cases),
        'constant_target_HH_interfaces': sum(x['target'].startswith('00000') for x in cases),
        'typical_00101_to_10101': typical,
        'cases': cases,
        'actual_cycle_edge_intersection_computed': False,
        'HC_search': False, 'elapsed_seconds': time.monotonic() - started,
    }
    output = BASE / 'hh-coordinate-capacity-results-v1.json'
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ['interface_count', 'coarse_covered', 'refined_covered', 'elapsed_seconds']}))
    print('results:', output)


if __name__ == '__main__':
    main()
