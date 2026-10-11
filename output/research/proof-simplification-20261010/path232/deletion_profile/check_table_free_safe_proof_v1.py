#!/usr/bin/env python3
"""Literal readback and exact counting for the table-free analytic proof.

No cycle search. The TeX argument is the proof; this replay checks its
literal profiles, common-grid counts and all existing allowed images.
"""
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


def im(edges, p, rev):
    return frozenset(dp.edge(dp.transform(x, p, rev), dp.transform(y, p, rev))
                     for x, y in edges)


def vertex(word):
    return tuple('abcd'.index(c) for c in word)


def path_edges(words):
    vertices = list(map(vertex, words))
    return {dp.edge(x, y) for x, y in zip(vertices, vertices[1:])}


def main():
    started = time.monotonic()
    candidate = BASE / 'table-free-safe-proof-candidate-v1.tex'
    text = candidate.read_text()
    data = json.loads((BASE / 'selected-cycles-input-v1.json').read_text())
    cycles = {tuple(map(int, t)): [tuple(map(int, w)) for w in words]
              for t, words in data['cycles'].items()}
    edges = {t: dp.cycle_edges(c) for t, c in cycles.items()}
    all_allowed = {}
    for t, es in edges.items():
        assert set(cycles[t]) == dp.fibre(t)
        assert es <= dp.recolouring_edges(set(cycles[t]))
        for p in itertools.permutations(range(4)):
            for rev in (False, True):
                all_allowed.setdefault(dp.transform(t, p, rev), set()).add(im(es, p, rev))

    profiles = [
        ('E', (0, 0, 1), 2, 2, [['dbc', 'cbc', 'cdc', 'bdc']]),
        ('E', (0, 0, 1), 1, 2, [['dca', 'bca', 'bcd', 'dcd']]),
        ('E', (0, 0, 1), 0, 2, [['cbd', 'cba', 'cda'], ['cbc', 'cdc']]),
        ('E', (0, 0, 1), 0, 1, [['bca', 'bcd'], ['bda', 'bdc']]),
        ('A', (0, 1, 2), 1, 0, [['bab', 'bad', 'cad', 'dad', 'dab', 'cab']]),
        ('A', (0, 1, 2), 0, 1, [['bad', 'bab', 'bdb', 'bcb'], ['bcd', 'bca', 'bda']]),
        ('A', (0, 1, 2), 2, 3, [['bad', 'cad', 'dad'], ['dcd', 'bcd']]),
        ('A', (0, 1, 2), 0, 2, [['cab', 'cdb', 'cda'], ['cad']]),
        ('M', (0, 1, 0), 0, 1, [['bcb', 'bab', 'bdb'], ['bad', 'bcd'], ['bac', 'bdc']]),
        ('M', (0, 1, 0), 2, 1, [['dcb', 'bcb', 'bab', 'bdb', 'cdb'], ['cab', 'dab']]),
        ('M', (0, 1, 0), 0, 2, [['cac', 'cad', 'cab'], ['cdb', 'cdc']]),
        ('M', (0, 1, 0), 2, 2, [['cac', 'bac', 'bdc', 'cdc'], ['dac']]),
    ]
    helper = text.split('\\paragraph{Cycle identities used by the count.}', 1)[1]
    displays = re.findall(r'\\\[(.*?)\\\]', helper, re.S)
    assert len(displays) == 4
    expected_by_family = []
    for kind in ('E', 'A', 'M'):
        expected_by_family.append([path for name, _, _, _, groups in profiles if name == kind for path in groups])
    literal_by_family = [[path.split(',') for path in re.findall(r'\[([abcd,]+)\]', display)]
                         for display in displays[:3]]
    assert literal_by_family == expected_by_family, (literal_by_family, expected_by_family)
    profile_records = []
    for kind, t, coordinate, colour, groups in profiles:
        outside = {v for v in cycles[t] if v[coordinate] == colour}
        expected_vertices = {vertex(w) for path in groups for w in path}
        expected_edges = set().union(*(path_edges(path) for path in groups))
        actual_edges = {e for e in edges[t] if set(e) <= outside}
        assert outside == expected_vertices
        assert actual_edges == expected_edges
        assert dp.components(outside, actual_edges) == sorted(map(len, groups))
        profile_records.append({'family': kind, 'coordinate': coordinate, 'colour': colour,
                                'paths': groups, 'component_sizes': sorted(map(len, groups))})
    root_words, = re.findall(r'\[([abcd,]+)\]', displays[3])
    expected_root = ['bac', 'cac', 'cad', 'cab', 'dab', 'dac', 'dad', 'bad']
    assert root_words.split(',') == expected_root
    assert {e for e in edges[(0, 1, 0)] if e[0][1] == e[1][1] == 0} == path_edges(expected_root)
    assert not any(vertex('bab') in e for e in path_edges(expected_root))

    # The inter-grid omission used in MA is invariant under both M directions.
    for t in ((0, 1, 0), (0, 1, 2)):
        for es in all_allowed[t]:
            assert all(t[1] in (x[0], x[2]) for x, y in es if x[1] != y[1])

    # Read CT values from the actual candidate, rather than assuming transcription.
    ct_rows = re.findall(r'(aab|abc|aba)\\to (aac|acb|cab|abd|bab|cba)&'
                         r'(\d+)&(\d+)&(\d+)&(\d+)&(\d+)&(\d+)', text)
    expected_rows = [
        ('aab', 'aac', '10', '13', '2', '2', '0', '3'),
        ('aab', 'acb', '10', '15', '1', '2', '0', '2'),
        ('aab', 'cab', '9', '11', '1', '4', '0', '2'),
        ('abc', 'abd', '11', '17', '0', '4', '2', '3'),
        ('aab', 'bab', '10', '15', '0', '5', '2', '2'),
        ('aba', 'cba', '12', '21', '0', '4', '3', '2'),
    ]
    assert ct_rows == expected_rows
    records = []
    checks = 0
    for src, dst, n, m, f, qcap, rfloor, lower in ct_rows:
        t, s = vertex(src), vertex(dst)
        n, m, f, qcap, rfloor, lower = map(int, (n, m, f, qcap, rfloor, lower))
        minima, q_values, r_values, triangle_records = [], [], [], []
        for C in all_allowed[t]:
            for D in all_allowed[s]:
                U = dp.fibre(t) & dp.fibre(s)
                H = dp.recolouring_edges(U)
                F = (dp.special(t) | dp.special(s)) & H
                qs = []
                for boundary, es in ((t, C), (s, D)):
                    outside = dp.fibre(boundary) - U
                    qs.append(len(dp.components(outside, {e for e in es if set(e) <= outside})))
                R = set()
                if (src, dst) == ('abc', 'abd'):
                    R = {dp.edge(vertex('bab'), vertex('cab')), dp.edge(vertex('bab'), vertex('dab'))}
                elif (src, dst) == ('aab', 'bab'):
                    for u in (2, 3):
                        row = {e for e in H if e[0][0] == e[1][0] == u
                               and e[0][1] == e[1][1] == 1}
                        assert len(row) == 3 and len(C & row) == 1
                        de = D & row
                        assert len(de) == 1 or (len(de) == 2 and C & row <= de)
                        omitted = row - C - D
                        assert len(omitted) >= 1
                        R.add(min(omitted))
                        triangle_records.append({'first_coordinate': u, 'E_retained': len(C & row),
                                                 'M_retained': len(de), 'joint_unused': len(omitted)})
                elif (src, dst) == ('aba', 'cba'):
                    R = {dp.edge(vertex(x), vertex(y)) for x, y in
                         [('bab', 'bac'), ('bab', 'bad'), ('dad', 'dcd')]}
                    assert not any(vertex('bab') in e for e in C if e[0][1] == e[1][1] == 0)
                assert (len(U), len(H), len(F)) == (n, m, f)
                assert sum(qs) <= qcap and len(R) >= rfloor
                assert R <= H and not R & (C | D | F)
                assert 2 * n - qcap - m - f + rfloor == lower >= 2
                q_values.append(qs)
                r_values.append(len(R))
                for p in itertools.permutations(range(4)):
                    for rev in (False, True):
                        tt, ss = dp.transform(t, p, rev), dp.transform(s, p, rev)
                        CC, DD = im(C, p, rev), im(D, p, rev)
                        HH, FF, RR = im(H, p, rev), im(F, p, rev), im(R, p, rev)
                        assert CC in all_allowed[tt] and DD in all_allowed[ss]
                        assert RR <= HH and not RR & (CC | DD | FF)
                        safe = (CC & DD) - FF
                        assert len(safe) >= lower
                        minima.append(len(safe))
                        checks += 1
        records.append({'family': [src, dst], 'n_m_f_qcap_Rfloor_bound': [n, m, f, qcap, rfloor, lower],
                        'canonical_orientation_path_counts': q_values,
                        'R_sizes': r_values, 'row_triangle_checks': triangle_records,
                        'image_checks': len(minima), 'actual_safe_common_min': min(minima)})

    support_record_path = BASE / 'unified-safe-proof-results-v1.json'
    support_record = json.loads(support_record_path.read_text())
    assert support_record['input_sha256'] == dp.digest(BASE / 'selected-cycles-input-v1.json')
    assert support_record['verdict'] == 'PASS'
    main_tex = dp.ROOT / 'planar_recoloring_hamilton_thresholds.tex'
    main = main_tex.read_text()
    eq = re.search(r'\\label\{eq:path232-cycles\}(.*?)\\end\{equation\}', main, re.S).group(1)
    for t, c in cycles.items():
        segment = eq.split(''.join(map(str, t)) + '&', 1)[1].split('[2pt]', 1)[0]
        assert re.findall(r'(?<![0-9])[0-9]{3}(?![0-9])', segment) == [''.join(map(str, x)) for x in c]
    record = {
        'verdict': 'PASS', 'scope': 'Complete analytic nine-family proof; all original allowed cycles preserved.',
        'proof_boundary': 'The TeX proves deletion counts, omitted-edge capacities, square and hexagon supports. Replay validates its literal input and scope.',
        'candidate_sha256': dp.digest(candidate), 'script_sha256': dp.digest(Path(__file__)),
        'input_sha256': dp.digest(BASE / 'selected-cycles-input-v1.json'),
        'main_sha256': dp.digest(main_tex), 'literal_profile_count': len(profile_records),
        'literal_profiles': profile_records, 'retention_families': records,
        'new_retention_image_checks': checks,
        'previous_support_record': {support_record_path.name: dp.digest(support_record_path)},
        'support_families': support_record['support_families'],
        'nine_family_boundary_classification': support_record['classification_boundary_pairs'],
        'allowed_boundaries': len(all_allowed), 'allowed_edge_sets': sum(map(len, all_allowed.values())),
        'approximate_English_tokens': {
            'old_proof_plus_appendix_conventions_table': support_record['approximate_English_tokens']['current_proof_plus_appendix_conventions_table'],
            'table_free_candidate': len(re.findall(r"[A-Za-z]+(?:[-'][A-Za-z]+)*",
                                      re.sub(r'\\[A-Za-z]+\*?', ' ', re.sub(r'%[^\n]*', '', text)))),
        },
        'no_cycle_search': True, 'elapsed_seconds': time.monotonic() - started,
    }
    output = BASE / 'table-free-safe-proof-results-v1.json'
    output.write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps({k: record[k] for k in ['verdict', 'literal_profile_count', 'new_retention_image_checks', 'approximate_English_tokens', 'elapsed_seconds']}))
    print('results:', output)


if __name__ == '__main__':
    main()
