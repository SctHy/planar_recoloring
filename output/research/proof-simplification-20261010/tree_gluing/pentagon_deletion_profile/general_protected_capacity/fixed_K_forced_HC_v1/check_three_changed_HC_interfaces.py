#!/usr/bin/env python3
"""Only00123 full graph/closure; read saved residual observations and original maps."""
from collections import Counter
from itertools import product
from pathlib import Path
import hashlib
import json
import platform
import re
import time

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
INPUTS = ['forced_star_closure_v1/forced-star-results.json',
          'forced_star_closure_v1/check_forced_stars.py',
          'forced_star_closure_v1/phase8-source.tex',
          'one_protected_vs_hc_v2/symmetric-one-sided-results-v2.json',
          'one_protected_vs_hc_v2/phase6-source.tex']
HARD = {'00001', '00112'}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def edge(a, b):
    return tuple(sorted((a, b)))


def legal(word, boundary):
    return all(word[i] != word[(i+1) % 5] and word[i] != boundary[i]
               for i in range(5))


def local(word, boundary):
    return {word[:i]+c+word[i+1:] for i in range(5) for c in '0123'
            if c not in {word[i], word[(i-1) % 5], word[(i+1) % 5], boundary[i]}}


def restore(word, mapping):
    start, direction, permutation = mapping
    out = [''] * 5
    for i, colour in enumerate(word):
        out[(start+direction*i) % 5] = str(permutation.index(colour))
    return ''.join(out)


def map_graph(graph, mapping):
    return {restore(v, mapping): {restore(w, mapping) for w in ns}
            for v, ns in graph.items()}


def force_closure(graph):
    allowed = {v: set(ns) for v, ns in graph.items()}
    forced = {v: set() for v in graph}
    trace = []
    while True:
        force, exclude = set(), set()
        causes = []
        for v in sorted(graph):
            assert len(allowed[v]) >= 2 and len(forced[v]) <= 2
            assert forced[v] <= allowed[v]
            if len(allowed[v]) == 2:
                new = {edge(v, w) for w in allowed[v]-forced[v]}
                force |= new
                if new:
                    causes.append({'state': v, 'rule': 'two-allowed',
                                   'edges': [list(e) for e in sorted(new)]})
            if len(forced[v]) == 2:
                new = {edge(v, w) for w in allowed[v]-forced[v]}
                exclude |= new
                if new:
                    causes.append({'state': v, 'rule': 'two-forced',
                                   'edges': [list(e) for e in sorted(new)]})
        assert not force & exclude
        trace.append({'pass': len(trace)+1,
                      'new_forced_edges': [list(e) for e in sorted(force)],
                      'new_excluded_edges': [list(e) for e in sorted(exclude)],
                      'causes': causes})
        if not force and not exclude:
            break
        for v, w in sorted(force):
            assert w in allowed[v] and v in allowed[w]
            forced[v].add(w)
            forced[w].add(v)
        for v, w in sorted(exclude):
            assert w not in forced[v] and v not in forced[w]
            allowed[v].remove(w)
            allowed[w].remove(v)
    return allowed, forced, trace


def run():
    started = time.perf_counter()
    before = {name: sha(BASE/name) for name in INPUTS}
    saved = json.loads((BASE/INPUTS[3]).read_text())
    old = json.loads((BASE/INPUTS[0]).read_text())
    assert saved['status'] == old['status'] == 'PASS'
    summaries = old['graph_closure']
    assert len(summaries) == 19
    no_exclusion = {t for t, v in summaries.items() if v['excluded_edges'] == 0}
    assert len(no_exclusion) == 18 and '00123' not in no_exclusion
    assert all(summaries[t]['passes'] <= 2 for t in no_exclusion)
    remaining = [r for r in saved['records']
                 if r['interface']['source'] != '00000' and not r['covered']]
    assert len(remaining) == 47
    groups = Counter(r['group'] for r in remaining)
    assert dict(groups) == {'hard-hard5': 5, 'hard-source-HC-target26': 7,
                            'ordinary-HH230': 28, 'HC-source-hard-target22': 7}
    changed = [r for r in remaining
               if '00123' in (r['interface']['source'], r['interface']['target_type'])]
    assert len(changed) == 3
    blocks = dict(re.findall(r'% BEGIN ([^\n]+)\n(.*?)% END \1',
                             (BASE/INPUTS[4]).read_text(), re.S))
    assert len(blocks) == 53
    pools = {}
    for name, content in blocks.items():
        if name.startswith('POOL-'):
            _, t, ci = name.split('-')
            pools[t, int(ci)] = {edge(a, b) for a, b in
                                 re.findall(r'\b([0-3]{5})-([0-3]{5})\b', content)}
    hard_basis = {edge(a, b) for a, b in re.findall(
        r'\b([0-3]{5})-([0-3]{5})\b', blocks['PORTS-00112'])}
    assert len(hard_basis) == 13 and len(pools['00112', 0]) == 2
    assert pools['00112', 0] <= hard_basis
    protected_hard = hard_basis - pools['00112', 0]
    assert all(legal(v, '00112') for e in hard_basis for v in e)
    words = {''.join(w) for w in product('0123', repeat=5)
             if legal(''.join(w), '00123')}
    graph = {v: local(v, '00123') for v in words}
    assert len(words) == 57 and all(ns <= words for ns in graph.values())
    assert sum(map(len, graph.values()))//2 == 122
    listed = next(content for name, content in blocks.items()
                  if name in {'C1-00123', 'FHC-00123'})
    printed = re.findall(r'\b[0-3]{5}\b', listed)
    assert len(printed) == len(set(printed)) == 57 and set(printed) == words
    # Printed ordering supplies a known full HC but is not read as selected
    # edges by the necessity closure; the graph derives only from legality.
    reached, pending = {min(words)}, [min(words)]
    while pending:
        v = pending.pop()
        new = graph[v]-reached
        reached |= new
        pending.extend(new)
    assert reached == words
    allowed, forced, trace = force_closure(graph)
    forced_edges = {edge(v, w) for v, ns in forced.items() for w in ns}
    allowed_edges = {edge(v, w) for v, ns in allowed.items() for w in ns}
    full_edges = {edge(v, w) for v, ns in graph.items() for w in ns}
    summary = {'vertices': len(words), 'full_edges': len(full_edges),
               'forced_edges': len(forced_edges),
               'excluded_edges': len(full_edges-allowed_edges), 'passes': len(trace)}
    assert summary == summaries['00123']
    first_forced = {edge(v, w) for v, ns in graph.items() if len(ns) == 2 for w in ns}
    records = []
    observations_checked = 0
    for row in changed:
        interface = row['interface']
        direction = 'F' if interface['target_type'] == '00123' else 'R'
        mapping = interface['mapping']
        if direction == 'F':
            assert interface['source'] == '00112'
            full, allow, force = (map_graph(g, mapping) for g in (graph, allowed, forced))
            K = protected_hard
            hc_pool = {edge(restore(a, mapping), restore(b, mapping))
                       for a, b in pools['00123', 0]}
            observation = row['forward_fixed_source_K']
            hc_boundary = interface['actual_target']
        else:
            assert interface['source'] == '00123' and interface['target_type'] == '00112'
            full, allow, force = graph, allowed, forced
            K = {edge(restore(a, mapping), restore(b, mapping)) for a, b in protected_hard}
            hc_pool = pools['00123', 0]
            observation = row['reverse_fixed_restored_target_K']
            hc_boundary = '00123'
        assert observation is not None and not observation['covered']
        candidates = {v for e in K for v in e} & set(full)
        assert candidates == {c['state'] for c in observation['all_local_observations']}
        incident = {v: {w for a, b in K for w in ([b] if a == v else [a] if b == v else [])}
                    for v in candidates}
        observations = []
        for c in observation['all_local_observations']:
            v = c['state']
            assert legal(v, hc_boundary)
            assert full[v] == set(c['HC_side_neighbours'])
            safe = {w for w in full[v] & incident[v] if edge(v, w) not in hc_pool}
            assert safe == set(c['safe_fixed_K_neighbours'])
            assert len(full[v]) == c['HC_side_degree']
            assert len(safe) == c['safe_incident_count']
            assert c['protected_edge_lower_bound'] == max(0, 2+len(safe)-len(full[v])) == 0
            forced_safe = force[v] & safe
            allowed_unsafe = allow[v]-safe
            lower = max(0, len(forced_safe), 2-len(allowed_unsafe))
            observations_checked += 1
            observations.append({'state': v, 'full_HC_neighbours': sorted(full[v]),
                                 'safe_fixed_K_neighbours': sorted(safe),
                                 'allowed_HC_neighbours': sorted(allow[v]),
                                 'forced_HC_neighbours': sorted(force[v]),
                                 'forced_safe_neighbours': sorted(forced_safe),
                                 'allowed_unsafe_neighbours': sorted(allowed_unsafe),
                                 'original_lower_bound': 0, 'closure_lower_bound': lower})
        best = max(c['closure_lower_bound'] for c in observations)
        records.append({'interface': interface, 'group': row['group'],
                        'direction': direction, 'HC_standard_type': '00123',
                        'original_mapping_retained': True,
                        'candidate_vertices': len(candidates), 'closure_lower_bound': best,
                        'newly_covered': best > 0,
                        'positive_certificates': [c for c in observations if c['closure_lower_bound'] > 0],
                        'all_local_observations': observations})
    assert observations_checked == 41
    other = [r for r in remaining if r not in changed and r['group'] != 'hard-hard5']
    assert len(other) == 39
    negative_justifications = []
    for row in other:
        eligible = []
        for direction, key, type_key in [('F', 'forward_fixed_source_K', 'target_type'),
                                          ('R', 'reverse_fixed_restored_target_K', 'source')]:
            if row[key] is not None:
                t = row['interface'][type_key]
                assert t in no_exclusion and not row[key]['covered']
                eligible.append({'direction': direction, 'HC_standard_type': t,
                                 'frozen_closure_summary': summaries[t]})
        assert eligible
        negative_justifications.append({'interface': row['interface'], 'group': row['group'],
                                       'eligible_directions': eligible,
                                       'reason': 'No-exclusion closure lemma: every forced safe edge would already give a positive degree-two endpoint in complete saved observations.'})
    assert before == {name: sha(BASE/name) for name in INPUTS}
    new = [r for r in records if r['newly_covered']]
    result = {'status': 'PASS', 'python': platform.python_version(),
              'input_sha256': before, 'code_sha256': sha(Path(__file__)),
              'remaining47_groups': dict(sorted(groups.items())),
              'eligible_remaining_interfaces': 42,
              'excluded_hard_hard_interfaces': 5,
              'no_exclusion_types_reused': sorted(no_exclusion),
              'no_exclusion_interfaces_settled_analytically': 39,
              'only_graph_recomputed': '00123', 'graph_summary': summary,
              'closure_initial_degree2_forced_edges': [list(e) for e in sorted(first_forced)],
              'closure_forced_edges': [list(e) for e in sorted(forced_edges)],
              'closure_excluded_edges': [list(e) for e in sorted(full_edges-allowed_edges)],
              'closure_trace': trace,
              'direct_changed_interfaces_checked': len(records),
              'actual_saved_observations_checked': observations_checked,
              'newly_covered_interfaces': len(new), 'new_covered_identities': [r['interface'] for r in new],
              'remaining_individual_interfaces_after_rule': 47-len(new),
              'records': records, 'analytically_unchanged_records': negative_justifications,
              'elapsed_seconds': time.perf_counter()-started,
              'limits': ['Only the specified fixed K side is fixed; the opposite whole-component HC is arbitrary.',
                         'No inference of Hamiltonicity from closure; a whole00123 HC is supplied by the frozen ordinary component.',
                         'Exactly one full legal graph and one closure calculated; no18-graph or230-interface paired-HC rerun.',
                         'Original normalizers are copied, never recomputed; fixed00112 K and pools independently parsed.',
                         'Finite42 eligible remaining-case scope;5 hard/hard excluded.',
                         'No Main edit or mutation of frozen inputs; no HC search or paired-K intersection enumeration.']}
    (HERE/'fixed-K-forced-HC-results.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items()
                      if k not in {'records', 'analytically_unchanged_records', 'closure_trace',
                                   'closure_initial_degree2_forced_edges', 'closure_forced_edges',
                                   'closure_excluded_edges'}}, indent=2))
    print(json.dumps([{'interface': r['interface'], 'direction': r['direction'],
                       'closure_lower_bound': r['closure_lower_bound'],
                       'positive_certificates': r['positive_certificates']} for r in records], indent=2))


if __name__ == '__main__':
    run()
