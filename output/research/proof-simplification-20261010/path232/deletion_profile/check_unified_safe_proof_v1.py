#!/usr/bin/env python3
"""Replay symbolic supports and literal MP rows; no cycle search."""
import importlib.util
import itertools
import json
import re
import time
from pathlib import Path

BASE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('dp', BASE / 'check_deletion_profile_v1.py')
dp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dp)


def image_edges(edges, p, rev):
    return frozenset(dp.edge(dp.transform(x, p, rev), dp.transform(y, p, rev))
                     for x, y in edges)


def triple(word):
    return tuple('abcd'.index(c) for c in word)


def word_count(text):
    text = re.sub(r'%[^\n]*', '', text)
    text = re.sub(r'\\[A-Za-z]+\*?', ' ', text)
    return len(re.findall(r"[A-Za-z]+(?:[-'][A-Za-z]+)*", text))


def main():
    started = time.monotonic()
    data = json.loads((BASE / 'selected-cycles-input-v1.json').read_text())
    cycles = {tuple(map(int, t)): [tuple(map(int, w)) for w in words]
              for t, words in data['cycles'].items()}
    E, M, A = (dp.cycle_edges(cycles[t]) for t in [(0, 0, 1), (0, 1, 0), (0, 1, 2)])
    candidate = BASE / 'unified-safe-proof-candidate-v2.tex'
    text = candidate.read_text()
    pattern = (r'(aab|aba)\\to (bab|cba)&([01])&([abcd]{3})\\text\{--\}'
               r'([abcd]{3}),\\ ([abcd]{3})\\text\{--\}([abcd]{3})')
    rows = re.findall(pattern, text)
    assert len(rows) == 4, rows
    expected_rows = [
        ('aab', 'bab', '0', 'cba', 'cbd', 'dba', 'dbc'),
        ('aab', 'bab', '1', 'cbc', 'dbc', 'cbd', 'dbd'),
        ('aba', 'cba', '0', 'dab', 'dac', 'dac', 'dad'),
        ('aba', 'cba', '1', 'bcb', 'bcd', 'dcb', 'dcd'),
    ]
    assert rows == expected_rows
    parametric_records = []
    action_checks = 0
    for src, tgt, orientation, x, y, z, w in rows:
        t, s = triple(src), triple(tgt)
        o = bool(int(orientation))
        if src == 'aab':
            C, D = E, image_edges(M, (1, 0, 2, 3), o)
        else:
            C, D = image_edges(M, (0, 1, 2, 3), o), image_edges(A, (2, 1, 0, 3), False)
        witness = {dp.edge(triple(x), triple(y)), dp.edge(triple(z), triple(w))}
        assert witness <= C & D
        assert not witness & (dp.special(t) | dp.special(s))
        for p in itertools.permutations(range(4)):
            for rev in (False, True):
                tt, ss = dp.transform(t, p, rev), dp.transform(s, p, rev)
                CC, DD = image_edges(C, p, rev), image_edges(D, p, rev)
                W = image_edges(witness, p, rev)
                assert W <= CC & DD
                assert not W & (dp.special(tt) | dp.special(ss))
                action_checks += 1
        parametric_records.append({'source': src, 'target': tgt, 'orientation': int(orientation),
                                    'witnesses': [x + '--' + y, z + '--' + w],
                                    'image_checks': 48})

    support_records = []
    # EE transfer: source 001, target 011 obtained by reverse of E(110).
    t, s = (0, 0, 1), (0, 1, 1)
    C, D = E, image_edges(E, (1, 0, 2, 3), True)
    square_vertices = {(1, 2, 0), (1, 2, 3), (3, 2, 0), (3, 2, 3)}
    square = dp.recolouring_edges(square_vertices)
    corner_edges = {e for e in square if (1, 2, 0) in e}
    assert len(corner_edges) == 2
    assert corner_edges <= C & D
    assert not corner_edges & (dp.special(t) | dp.special(s))
    assert not ((C & dp.special(t)) & D)
    assert not ((D & dp.special(s)) & C)
    for p in itertools.permutations(range(4)):
        for rev in (False, True):
            W = image_edges(corner_edges, p, rev)
            assert W <= image_edges(C, p, rev) & image_edges(D, p, rev)
            assert not W & (dp.special(dp.transform(t, p, rev)) |
                            dp.special(dp.transform(s, p, rev)))
            action_checks += 1
    support_records.append({'family': 'EE-transfer', 'image_checks': 48, 'safe_common_square_edges': 2})

    # AA middle: the selected root-prism path is five of this same hexagon.
    C, D = A, image_edges(A, (0, 3, 2, 1), False)
    hexagon = [(1, 0, 1), (1, 0, 3), (2, 0, 3), (3, 0, 3), (3, 0, 1), (2, 0, 1)]
    H = dp.cycle_edges(hexagon)
    assert len(C & H) == len(D & H) == 5
    assert len(C & D & H) == 4
    for p in itertools.permutations(range(4)):
        for rev in (False, True):
            HH, CC, DD = (image_edges(x, p, rev) for x in (H, C, D))
            assert len(CC & HH) == len(DD & HH) == 5
            assert len(CC & DD & HH) >= 4
            action_checks += 1
    support_records.append({'family': 'AA-middle', 'image_checks': 48, 'hexagon_retention': [5, 5], 'safe_common_min': 4})

    # MM: all four orientations each have three of the same common square.
    square = dp.recolouring_edges({(u, 3, w) for u in (1, 2) for w in (1, 2)})
    minima = []
    for o1, o2 in itertools.product((False, True), repeat=2):
        C = image_edges(M, (0, 1, 2, 3), o1)
        D = image_edges(M, (0, 2, 1, 3), o2)
        assert len(C & square) == len(D & square) == 3
        minima.append(len(C & D & square))
        for p in itertools.permutations(range(4)):
            for rev in (False, True):
                HH, CC, DD = (image_edges(x, p, rev) for x in (square, C, D))
                assert len(CC & HH) == len(DD & HH) == 3
                assert len(CC & DD & HH) >= 2
                action_checks += 1
    support_records.append({'family': 'MM-middle', 'image_checks': 192, 'orientation_pairs': 4,
                            'square_retention': [3, 3], 'safe_common_min': min(minima)})

    def kind(t):
        if len(set(t)) == 3:
            return 'A'
        return 'M' if t[0] == t[2] else 'E'

    rank = {'E': 0, 'M': 1, 'A': 2}
    classification = {}
    good = [t for t in itertools.product(range(4), repeat=3) if len(set(t)) > 1]
    for t, s in itertools.combinations(good, 2):
        j = [i for i in range(3) if t[i] != s[i]]
        if len(j) != 1:
            continue
        if rank[kind(t)] > rank[kind(s)]:
            t, s = s, t
        kt, ks = kind(t), kind(s)
        if kt == 'E':
            if t[0] != t[1]:
                t, s = t[::-1], s[::-1]
            a, b = t[0], t[2]
            changed = next(i for i in range(3) if t[i] != s[i])
            if changed == 2:
                assert ks == 'E' and s[2] not in (a, b)
                family = 'EE-singleton'
            elif changed == 1:
                family = 'EE-transfer' if s[1] == b else 'EA-middle'
                assert ks == ('E' if s[1] == b else 'A')
            else:
                family = 'EM' if s[0] == b else 'EA-endpoint'
                assert ks == ('M' if s[0] == b else 'A')
        elif kt == 'M':
            changed = next(i for i in range(3) if t[i] != s[i])
            family = 'MM-middle' if changed == 1 else 'MA'
            assert ks == ('M' if changed == 1 else 'A')
        else:
            changed = next(i for i in range(3) if t[i] != s[i])
            family = 'AA-middle' if changed == 1 else 'AA-endpoint'
            assert ks == 'A'
        classification[family] = classification.get(family, 0) + 1
    assert sum(classification.values()) == 252 and len(classification) == 9
    old = (dp.ROOT / 'planar_recoloring_hamilton_thresholds.tex').read_text()
    proof_start = old.index('\\begin{proof}', old.index('\\label{lem:pathsafe}'))
    proof_end = old.index('\\end{proof}', proof_start) + len('\\end{proof}')
    app_start = old.index('\\subsection{Safe common-edge witnesses}')
    app_end = old.index('\\end{table}', app_start) + len('\\end{table}')
    record = {
        'verdict': 'PASS', 'scope': 'Literal MP rows, three support families, direct nine-family classification. Existing cycles only.',
        'proof_boundary': 'The TeX analytic argument remains the proof; these checks validate its literal identities and quantifiers.',
        'candidate_sha256': dp.digest(candidate),
        'longer_candidate_sha256': dp.digest(BASE / 'unified-safe-proof-candidate-v1.tex'),
        'script_sha256': dp.digest(Path(__file__)),
        'input_sha256': dp.digest(BASE / 'selected-cycles-input-v1.json'),
        'main_sha256': dp.digest(dp.ROOT / 'planar_recoloring_hamilton_thresholds.tex'),
        'four_parametric_rows': parametric_records,
        'support_families': support_records,
        'image_checks_this_script': action_checks,
        'classification_boundary_pairs': classification,
        'previous_deletion_record': 'deletion-profile-results-v1.json',
        'word_count_method': 'Alphabetic tokens after removing TeX commands and comments; includes symbolic assignments.',
        'approximate_English_tokens': {
            'current_proof_plus_appendix_conventions_table': word_count(old[proof_start:proof_end] + old[app_start:app_end]),
            'unified_candidate_v1': word_count((BASE / 'unified-safe-proof-candidate-v1.tex').read_text()),
            'unified_candidate_v2': word_count(text),
        },
        'no_cycle_search': True, 'elapsed_seconds': time.monotonic() - started,
    }
    output = BASE / 'unified-safe-proof-results-v1.json'
    output.write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps({k: record[k] for k in ['verdict', 'image_checks_this_script', 'approximate_English_tokens', 'elapsed_seconds']}))
    print('results:', output)


if __name__ == '__main__':
    main()
