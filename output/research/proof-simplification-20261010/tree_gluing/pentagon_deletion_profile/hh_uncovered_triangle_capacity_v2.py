#!/usr/bin/env python3
"""K3-retention capacity on the eight unresolved HH cases only.

K2 rows are ignored. No actual C/D edge intersection and no HC search.
"""
import importlib.util
from itertools import combinations
from pathlib import Path
import hashlib
import json
import re
import time

BASE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('hh', BASE / 'hh_coordinate_capacity_v1.py')
hh = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hh)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    started = time.monotonic()
    source = BASE / 'hh-coordinate-capacity-results-v1.json'
    prior = json.loads(source.read_text())
    remaining = [x for x in prior['cases'] if not x['refined_hit_coordinates']]
    assert len(remaining) == 8
    frozen = BASE / 'phase6-selected-input-v2.tex'
    assert sha(frozen) == prior['source_provenance']['frozen_sha256']
    blocks = dict(re.findall(r'% BEGIN ([A-Z0-9-]+)\n(.*?)% END \1', frozen.read_text(), re.S))

    def cycle(key):
        t = key[:5]
        assert t not in hh.HARD and t != '00000'
        prefix = 'FHC-' if '4' in t else 'C1-'
        words = [tuple(map(int, w)) for w in re.findall(r'\b[0-3]{5}\b', blocks[prefix + t])]
        return words, hh.cycle_edges(words)

    def pool(key):
        return {hh.edge(tuple(map(int, x)), tuple(map(int, y)))
                for x, y in re.findall(r'\b([0-3]{5})-([0-3]{5})\b', blocks['POOL-' + key.replace(':', '-')])}

    records = []
    for case in remaining:
        c, C = cycle(case['source'])
        canonical_d, _ = cycle(case['target'])
        g = case['normalizer']
        d = [hh.restore(x, g) for x in canonical_d]
        D = hh.cycle_edges(d)
        P = pool(case['source'])
        Q = {hh.edge(hh.restore(x, g), hh.restore(y, g)) for x, y in pool(case['target'])}
        U = set(c) & set(d)
        all_triangles, supports = [], []
        for j in range(5):
            rows = {}
            for x in U:
                rows.setdefault(x[:j] + x[j + 1:], set()).add(x)
            for other, vertices in sorted(rows.items()):
                if len(vertices) != 3:
                    continue
                H = {hh.edge(x, y) for x, y in combinations(sorted(vertices), 2)}
                assert len(H) == 3 and all(hh.coordinate(e) == j for e in H)
                F = (P | Q) & H
                a, b, f = len(C & H), len(D & H), len(F)
                rC, rD = len(C & F), len(D & F)
                assert a <= 2 and b <= 2
                lower = a + b - 3 - rC - rD + f
                rec = {'coordinate': j, 'fixed_other_colours': other,
                       'varying_colours': sorted(x[j] for x in vertices),
                       'a': a, 'b': b, 'm': 3, 'f': f, 'rC': rC, 'rD': rD,
                       'safe_retained_C': a - rC, 'safe_retained_D': b - rD,
                       'refined_lower_bound': lower}
                all_triangles.append(rec)
                if a >= 2 and b >= 2 and lower >= 1:
                    supports.append(rec)
        records.append({'source': case['source'], 'changed_position': case['changed_position'],
                        'new_colour': case['new_colour'], 'target': case['target'],
                        'normalizer': g, 'common_vertices': len(U),
                        'K3_rows_checked': len(all_triangles), 'positive_K3_supports': supports,
                        'all_K3_rows': all_triangles})
    result = {
        'status': 'FINITE_K3_CAPACITY_CHECK',
        'scope': 'Only eight unresolved selected HH cases, only genuine K3 rows. K2 single-edge rows not used.',
        'input_record': {source.name: sha(source)}, 'frozen_input_sha256': sha(frozen),
        'script_sha256': sha(Path(__file__)),
        'case_count': len(records), 'covered_by_K3': sum(bool(x['positive_K3_supports']) for x in records),
        'K3_row_count': sum(x['K3_rows_checked'] for x in records),
        'positive_K3_row_count': sum(len(x['positive_K3_supports']) for x in records),
        'records': records,
        'interpretation': 'A positive row has two raw retained triangle edges in each selected cycle and positive safe capacity after pool exclusions. The integer counts need a symbolic family proof before manuscript use.',
        'actual_cycle_edge_intersection_computed': False, 'HC_search': False,
        'elapsed_seconds': time.monotonic() - started,
    }
    output = BASE / 'hh-uncovered-triangle-capacity-results-v2.json'
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ['case_count', 'covered_by_K3', 'K3_row_count', 'positive_K3_row_count', 'elapsed_seconds']}))
    for rec in records:
        print(rec['source'], rec['changed_position'], rec['new_colour'], rec['target'], 'supports', rec['positive_K3_supports'])


if __name__ == '__main__':
    main()
