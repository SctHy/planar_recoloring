"""Independent direct-legality readback of frozen local rows; no graph search."""
from pathlib import Path
from itertools import permutations
import hashlib
import json
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[7]
SOURCE_SHA = '7a90f79db489447b0bad3019217fd369a5cc25986288247981cbe7f3462acba3'
MAIN_SHA = '3806a0c7f8ec374ea92e70152f939e92e35c3c76564f9e69e8c06160999bcb58'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def word(text):
    return tuple(int(c) for c in text)


def text(word):
    return ''.join(str(c) for c in word)


def edge(a, b):
    return tuple(sorted((a, b)))


def legal(x, u):
    return all(x[i] != x[(i + 1) % 5] and x[i] != u[i] for i in range(5))


def main():
    src = HERE / 'phase6-source.tex'
    assert sha(src) == SOURCE_SHA
    source = src.read_text()
    blocks = dict(re.findall(r'% BEGIN ([A-Z0-9-]+)\n(.*?)% END \1', source, re.S))
    standard = set(re.findall(r'% BEGIN (?:C1|FHC)-([0-4]{5})', source)) | {'00000', '00001', '00112'}

    def literal_edges(name):
        return {edge(word(a), word(b)) for a, b in re.findall(r'([0-3]{5})-([0-3]{5})', blocks[name])}

    K = {'00001': literal_edges('COMMON-00001') - literal_edges('POOL-00001-0'),
         '00112': literal_edges('PORTS-00112') - literal_edges('POOL-00112-0')}
    assert {k: len(v) for k, v in K.items()} == {'00001': 11, '00112': 11}

    def first_map(u):
        for s in range(5):
            for eps in (1, -1):
                for p in permutations(range(4)):
                    n = text(tuple(p[u[(s + eps * i) % 5]] for i in range(5)))
                    if n in standard:
                        return n, (s, eps, p)
        raise AssertionError(u)

    def restore(x, transform):
        s, eps, p = transform
        inverse = {p[i]: i for i in range(4)}
        result = [None] * 5
        for i in range(5):
            result[(s + eps * i) % 5] = inverse[x[i]]
        return tuple(result)

    author = json.loads((HERE / 'one-change-family-results.json').read_text())
    previous = json.loads((HERE / 'previous-two-center-results.json').read_text())
    actual_previous = HERE.parent / 'degree_pair_v2' / 'one-change-family-results.json'
    assert sha(HERE / 'previous-two-center-results.json') == sha(actual_previous)
    assert author['cases'][:30] == previous['cases']
    assert len(author['cases']) == author['case_count'] == 60
    checked = []
    for row in author['cases']:
        t, v = word(row['hard']), word(row['vertex'])
        j, q = row['position'], row['new_colour']
        u = tuple(q if i == j else t[i] for i in range(5))
        n, transform = first_map(u)
        assert row['actual_target'] == text(u)
        assert row['target_type'] == n
        assert row['prescribed_normalizer'] == [transform[0], transform[1], list(transform[2])]
        valid = legal(v, u)
        assert row['vertex_legal'] == valid
        if not valid:
            assert row['status'] == 'INAPPLICABLE_WITNESS_VERTEX_ILLEGAL'
            checked.append({'hard': row['hard'], 'vertex': row['vertex'], 'j': j, 'q': q, 'legal': False})
            continue
        # Check proposed immediate recolorings by the definition of F_u;
        # this deliberately does not use the author's B_i formula.
        neighbours = set()
        for i in range(5):
            for c in range(4):
                if c == v[i]:
                    continue
                candidate = tuple(c if k == i else v[k] for k in range(5))
                if legal(candidate, u):
                    neighbours.add(candidate)
        protected = {edge(v, w) for w in neighbours} & K[row['hard']]
        component = 0
        if n == '00000':
            words = [word(w) for w in re.findall(r'\b[0-3]{5}\b', blocks['FACTOR-00000'])]
            assert len(words) == 30
            components = [{restore(x, transform) for x in words[i:i + 15]} for i in (0, 15)]
            memberships = [i for i, vertices in enumerate(components) if v in vertices]
            assert len(memberships) == 1
            component = memberships[0]
            scope = 'constant_component_containing_vertex'
        elif n in K:
            scope = 'hard_target_no_nonvacuous_HC_claim'
        else:
            scope = 'ordinary_single_component'
        pool = {edge(restore(a, transform), restore(b, transform))
                for a, b in literal_edges(f'POOL-{n}-{component}')}
        safe = protected - pool
        degree = len(neighbours)
        raw_bound = max(0, 2 + len(protected) - degree)
        safe_bound = max(0, 2 + len(safe) - degree)
        assert row['target_component'] == component and row['scope'] == scope
        assert row['degree'] == degree and row['neighbours'] == sorted(map(text, neighbours))
        assert row['incident_hardK'] == ['-'.join(map(text, e)) for e in sorted(protected)]
        assert row['incident_target_pool_overlap'] == ['-'.join(map(text, e)) for e in sorted(protected & pool)]
        assert row['raw_local_lower_bound'] == raw_bound and row['safe_local_lower_bound'] == safe_bound
        assert row['raw_local_criterion'] == (degree >= 2 and raw_bound > 0)
        assert row['safe_local_criterion'] == (degree >= 2 and safe_bound > 0)
        checked.append({'hard': row['hard'], 'vertex': row['vertex'], 'j': j, 'q': q,
                        'target': text(u), 'type': n, 'component': component, 'legal': True,
                        'scope': scope, 'd': degree, 'g': len(safe), 'lower': safe_bound,
                        'incident_safe_edges': ['-'.join(map(text, e)) for e in sorted(safe)]})

    main_path = ROOT / 'planar_recoloring_hamilton_thresholds.tex'
    assert sha(main_path) == MAIN_SHA, main_path
    main_source = main_path.read_text()
    records = re.findall(r'([0-4]{5}):(\d+) (\d+) (\d+) ([0-4]{5}):(\d+) ([0-3]{5})-([0-3]{5})',
                         dict(re.findall(r'% BEGIN ([A-Z0-9-]+)\n(.*?)% END \1', main_source, re.S))['INTERFACES-ALL'])
    assert len(records) == 283
    # Three witnesses suffice. Prefer pair arguments, except the unique
    # 13023 certificate for 00112 -> 00110.
    selections = [('00001', '32132', j, q) for j, q in ((0, 1), (0, 2), (1, 1), (2, 2), (2, 3), (3, 2), (4, 0))]
    selections += [('00112', '13230', j, q) for j, q in ((0, 3), (1, 1), (1, 2), (2, 0), (3, 0), (4, 1))]
    selections += [('00112', '13023', 4, 0)]
    selected = []
    for hard, vertex, j, q in selections:
        row, = [r for r in checked if (r['hard'], r['vertex'], r['j'], r['q']) == (hard, vertex, j, q)]
        assert row['lower'] > 0 and row['scope'] != 'hard_target_no_nonvacuous_HC_claim'
        matching = [r for r in records if r[:6] == (hard, '0', str(j), str(q), row['type'], str(row['component']))]
        assert len(matching) == 1
        row['superseded_literal_record'] = ' '.join(matching[0][:6]) + ' ' + '-'.join(matching[0][6:])
        selected.append(row)
    assert len(selected) == 14
    ordinary = [r for r in selected if r['scope'] == 'ordinary_single_component']
    assert len(ordinary) == 13
    assert sum(r['d'] == 3 and r['g'] == 2 for r in ordinary) == 9
    assert sum(r['d'] == 2 for r in ordinary) == 4
    for name, template in author['templates'].items():
        v = word(template['vertex'])
        B = [sorted(c for c in range(4) if c not in (v[(i - 1) % 5], v[i], v[(i + 1) % 5])) for i in range(5)]
        assert B == template['coordinate_alternative_sets']
    result = {'verdict': 'PASS', 'python_version': sys.version.split()[0], 'review_method':
              'separate direct-legality local readback; no author-code import, graph construction or Hamilton search',
              'source_sha256': SOURCE_SHA, 'main_input_sha256': MAIN_SHA,
              'author_result_sha256': sha(HERE / 'one-change-family-results.json'),
              'previous_result_exact_v2_bytes': True, 'first30_rows_exactly_inherited': True,
              'local_rows_checked': 60, 'selected_certificates': selected,
              'ordinary_interface_count': 13, 'constant_component_count': 1,
              'collective_degree3_pair_cases': 9, 'degree2_ordinary_cases': 4,
              'fourth_center_adds_no_ordinary_interface': True,
              'retention_or_opponent_cycle_edges_used': False,
              'all53_interface_claim': False,
              'checked_rows': checked}
    (HERE / 'local-review-results.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('selected_certificates', 'checked_rows')}, indent=2))


if __name__ == '__main__':
    main()
