#!/usr/bin/env python3
"""Independent four-star premise/map/pool check; no full graph or HC search."""
from pathlib import Path
import hashlib
import json
import platform
import re

HERE = Path(__file__).resolve().parent
INPUT = HERE.parent/'one_protected_vs_hc_v2/phase6-source.tex'
OBSERVATIONS = HERE.parent/'one_protected_vs_hc_v2/symmetric-one-sided-results-v2.json'


def edge(a, b):
    return tuple(sorted((a, b)))


def direct_star(word, boundary):
    out = []
    for i in range(5):
        admissible = set('0123')-{boundary[i], word[(i-1)%5], word[(i+1)%5]}
        for colour in sorted(admissible-{word[i]}):
            out.append(word[:i]+colour+word[i+1:])
    return sorted(out)


def image(word, mapping):
    start, direction, colours = mapping
    return ''.join(colours[int(word[(start+direction*i)%5])] for i in range(5))


def run():
    expected = {'21301': ['21201', '31301'],
                '23201': ['21201', '23231'],
                '32301': ['31301', '32302'],
                '31201': ['21201', '31202', '31231', '31301']}
    for word, neighbors in expected.items():
        assert direct_star(word, '00123') == neighbors
    required_by_tips = {edge(v, w) for v in ('21301', '23201', '32301')
                        for w in expected[v]}
    assert {edge('21201', '21301'), edge('21201', '23201')} <= required_by_tips
    assert {edge('31301', '21301'), edge('31301', '32301')} <= required_by_tips
    remaining = set(expected['31201'])-{'21201', '31301'}
    assert remaining == {'31202', '31231'}
    forced = edge('31201', '31231')
    blocks = dict(re.findall(r'% BEGIN ([^\n]+)\n(.*?)% END \1', INPUT.read_text(), re.S))
    edges = lambda name: {edge(a,b) for a,b in re.findall(
        r'\b([0-3]{5})-([0-3]{5})\b', blocks[name])}
    source_port = edge('12320', '32320')
    assert source_port in edges('PORTS-00112')
    assert source_port not in edges('POOL-00112-0')
    assert forced not in edges('POOL-00123-0')
    saved = json.loads(OBSERVATIONS.read_text())
    original = next(r['interface'] for r in saved['records']
                    if r['interface']['source'] == '00112'
                    and r['interface']['position'] == 1
                    and r['interface']['colour'] == '3')
    mapping = original['mapping']
    assert mapping == [2, 1, '2013']
    assert edge(*(image(w, mapping) for w in source_port)) == forced
    assert image(original['actual_target'], mapping) == '00123'
    for word in source_port:
        for boundary in ('00112', original['actual_target']):
            assert all(word[i] != boundary[i] and word[i] != word[(i+1)%5]
                       for i in range(5))
    out = {'status': 'PASS', 'python': platform.python_version(),
           'source_sha256': hashlib.sha256(INPUT.read_bytes()).hexdigest(),
           'observations_sha256': hashlib.sha256(OBSERVATIONS.read_bytes()).hexdigest(),
           'code_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           'four_direct_full_stars': expected,
           'forced_tip_edges': [list(e) for e in sorted(required_by_tips)],
           'excluded_at_31201_by_saturated_neighbors': ['21201', '31301'],
           'remaining_at_31201': sorted(remaining),
           'forced_target_standard_edge': list(forced),
           'source_protected_edge': list(source_port),
           'source_membership_and_both_pool_exclusions_checked': True,
           'original_interface': original,
           'scope': 'Four direct local full-star premises plus one fixed-K membership, two pool exclusions and the saved original map identity; no whole graph or HC search.'}
    (HERE/'short-forcing-chain-verification.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    run()
