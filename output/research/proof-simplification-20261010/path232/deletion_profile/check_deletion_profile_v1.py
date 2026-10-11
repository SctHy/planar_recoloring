#!/usr/bin/env python3
"""Exact replay of symbolic deletion identities, not a proof by PASS.

No Hamilton-cycle search. The prose candidate proves the general bound;
this script verifies its six symbolic identities and four applications
against frozen cycle words and every colour/reversal image.
"""
import hashlib
import itertools
import json
import re
import time
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[4]
PALETTE = range(4)


def edge(x, y):
    return tuple(sorted((x, y)))


def cycle_edges(cycle):
    return {edge(x, cycle[(i + 1) % len(cycle)]) for i, x in enumerate(cycle)}


def fibre(t):
    return {x for x in itertools.product(PALETTE, repeat=3)
            if x[0] != x[1] and x[1] != x[2]
            and all(x[i] != t[i] for i in range(3))}


def recolouring_edges(vertices):
    return {edge(x, y) for x, y in itertools.combinations(sorted(vertices), 2)
            if sum(a != b for a, b in zip(x, y)) == 1}


def transform(x, p, rev):
    return tuple(p[a] for a in (x[::-1] if rev else x))


def components(vertices, edges):
    unseen = set(vertices)
    found = []
    while unseen:
        seed = unseen.pop()
        group, stack = {seed}, [seed]
        while stack:
            u = stack.pop()
            for x, y in edges:
                v = y if x == u else x if y == u else None
                if v in unseen:
                    unseen.remove(v)
                    group.add(v)
                    stack.append(v)
        found.append(group)
    return sorted(len(x) for x in found)


def special(t):
    if t[0] == t[1] != t[2]:
        a, b = t[0], t[2]
        c, d = sorted(set(PALETTE) - {a, b})
        return {edge((b, c, d), (d, c, d)), edge((b, d, c), (c, d, c))}
    if t[0] != t[1] == t[2]:
        return {edge(x[::-1], y[::-1]) for x, y in special(t[::-1])}
    return set()


def paths(words):
    result = set()
    for path in words:
        vertices = [tuple(map(int, w)) for w in path.split()]
        result |= {edge(x, y) for x, y in zip(vertices, vertices[1:])}
    return result


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    started = time.monotonic()
    input_path = BASE / 'selected-cycles-input-v1.json'
    data = json.loads(input_path.read_text())
    literal = {tuple(map(int, t)): [tuple(map(int, w)) for w in words]
               for t, words in data['cycles'].items()}
    main_tex = ROOT / 'planar_recoloring_hamilton_thresholds.tex'
    text = main_tex.read_text()
    eq = re.search(r'\\label\{eq:path232-cycles\}(.*?)\\end\{equation\}', text, re.S).group(1)
    for t, c in literal.items():
        words = ' '.join(''.join(map(str, x)) for x in c)
        # TeX 010 and 012 rows continue on a second line.
        part = eq.split(''.join(map(str, t)) + '&', 1)[1].split('[2pt]', 1)[0]
        got = re.findall(r'(?<![0-9])[0-9]{3}(?![0-9])', part)
        assert got == words.split(), (t, got)

    all_allowed = {}
    for t, c in literal.items():
        assert set(c) == fibre(t)
        assert len(c) == len(set(c))
        assert cycle_edges(c) <= recolouring_edges(set(c))
        for p in itertools.permutations(PALETTE):
            for rev in (False, True):
                s = transform(t, p, rev)
                edges = frozenset(edge(transform(x, p, rev), transform(y, p, rev))
                                  for x, y in cycle_edges(c))
                all_allowed.setdefault(s, set()).add(edges)
    for t, sets in all_allowed.items():
        if not (t[0] == t[2] != t[1]):
            assert len(sets) == 1, (t, len(sets))

    descriptions = [
        ('E-singleton-unused', (0, 0, 1), 2, 2, ['312 212 232 132'], [4]),
        ('E-middle-unused', (0, 0, 1), 1, 2, ['320 120 123 323'], [4]),
        ('E-repeated-end-unused', (0, 0, 1), 0, 2, ['213 210 230', '212 232'], [2, 3]),
        ('A-root-middle', (0, 1, 2), 1, 0, ['101 103 203 303 301 201'], [6]),
        ('A-end-middle-boundary', (0, 1, 2), 0, 1, ['103 101 131 121', '123 120 130'], [3, 4]),
        ('A-end-unused', (0, 1, 2), 2, 3, ['103 203 303', '323 123'], [2, 3]),
    ]
    identity_records = []
    for name, t, j, colour, path_words, sizes in descriptions:
        outside = {x for x in literal[t] if x[j] == colour}
        actual_edges = {e for e in cycle_edges(literal[t]) if set(e) <= outside}
        assert actual_edges == paths(path_words), name
        assert components(outside, actual_edges) == sizes, name
        identity_records.append({'name': name, 'boundary': t, 'coordinate': j,
                                 'colour': colour, 'paths': path_words,
                                 'component_sizes': sizes})

    families = [
        ('EE-singleton', (0, 0, 1), (0, 0, 2), (10, 13, 2, 1, 1, 0, 3)),
        ('EA-middle', (0, 0, 1), (0, 2, 1), (10, 15, 1, 1, 1, 0, 2)),
        ('EA-endpoint', (0, 0, 1), (2, 0, 1), (9, 11, 1, 2, 2, 0, 2)),
        ('AA-endpoint', (0, 1, 2), (0, 1, 3), (11, 17, 0, 2, 2, 2, 3)),
    ]
    family_records = []
    total = 0
    for name, t, s, expected in families:
        local = []
        for p in itertools.permutations(PALETTE):
            for rev in (False, True):
                tt, ss = transform(t, p, rev), transform(s, p, rev)
                C, = all_allowed[tt]
                D, = all_allowed[ss]
                U = fibre(tt) & fibre(ss)
                H = recolouring_edges(U)
                F = (special(tt) | special(ss)) & H
                q = []
                for boundary, edges in ((tt, C), (ss, D)):
                    outside = fibre(boundary) - U
                    Eoutside = {e for e in edges if set(e) <= outside}
                    q.append(len(components(outside, Eoutside)))
                    assert sum(set(e) <= U for e in edges) == len(U) - q[-1]
                R = set()
                if name == 'AA-endpoint':
                    R = {edge(transform(x, p, rev), transform(y, p, rev))
                         for x, y in [((1, 0, 1), (2, 0, 1)),
                                      ((1, 0, 1), (3, 0, 1))]}
                    assert R <= H and not (R & (C | D | F))
                bound = 2 * len(U) - sum(q) - len(H) - len(F) + len(R)
                got = (len(U), len(H), len(F), *q, len(R), bound)
                assert got == expected, (name, tt, ss, got, expected)
                common_safe = (C & D) - F
                assert len(common_safe) >= bound >= 2
                total += 1
                local.append(len(common_safe))
        family_records.append({'family': name, 'canonical_boundaries': [t, s],
                               'n_m_f_qC_qD_R_bound': expected,
                               'image_checks': len(local),
                               'actual_safe_common_min': min(local)})

    # Record the exact failure of the same coarse count in the M families.
    unresolved = []
    for name, t, s in [('EM', (0, 0, 1), (1, 0, 1)),
                       ('MA', (0, 1, 0), (2, 1, 0))]:
        U = fibre(t) & fibre(s)
        H = recolouring_edges(U)
        F = (special(t) | special(s)) & H
        for C in sorted(all_allowed[t], key=lambda x: sorted(x)):
            for D in sorted(all_allowed[s], key=lambda x: sorted(x)):
                qs = []
                for boundary, es in [(t, C), (s, D)]:
                    outside = fibre(boundary) - U
                    qs.append(len(components(outside, {e for e in es if set(e) <= outside})))
                lower = 2 * len(U) - sum(qs) - len(H) - len(F)
                unresolved.append({'family': name, 'outside_components': qs,
                                   'coarse_bound': lower,
                                   'actual_safe_common': len((C & D) - F)})

    result = {'verdict': 'PASS', 'scope': 'Six deletion identities and four analytic families; existing allowed cycles only.',
              'proof_boundary': 'The general lemma and layer counts are proved in TeX. Exact replay does not replace those arguments.',
              'inputs': {input_path.name: digest(input_path),
                         'planar_recoloring_hamilton_thresholds.tex': digest(main_tex)},
              'candidate_sha256': digest(BASE / 'deletion-profile-candidate-v1.tex'),
              'script_sha256': digest(Path(__file__)),
              'allowed_boundary_count': len(all_allowed),
              'allowed_edge_set_count': sum(map(len, all_allowed.values())),
              'deletion_identities': identity_records,
              'families': family_records,
              'total_family_image_checks': total,
              'remaining_M_families': unresolved,
              'no_cycle_search': True, 'elapsed_seconds': time.monotonic() - started}
    output = BASE / 'deletion-profile-results-v1.json'
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ['verdict', 'total_family_image_checks', 'elapsed_seconds']}))
    print('results:', output)


if __name__ == '__main__':
    main()
