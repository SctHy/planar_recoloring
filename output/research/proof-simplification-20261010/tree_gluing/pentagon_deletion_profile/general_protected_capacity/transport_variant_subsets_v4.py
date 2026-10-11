#!/usr/bin/env python3
"""Local retained-port comparison across recorded opposite transport variants.

No new cycles or full fibres are generated. The two fixed J supports
have at most17 edges. Only membership of their transported edges in the
already displayed opposite protected bases is inspected. Intersections
between opposite *variants* are recorded; the original paired hard K
and opposite L edge intersection is never computed.
"""
from collections import Counter, defaultdict
from pathlib import Path
import hashlib
import json
import re

BASE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def edge(a, b):
    return tuple(sorted((a, b)))


def coordinate(e):
    return next(j for j in range(5) if e[0][j] != e[1][j])


def counts(es):
    d = Counter(map(coordinate, es))
    return [d[j] for j in range(5)]


def transform(word, g):
    s, eps, p = g
    return ''.join(str(p[int(word[(s+eps*j) % 5])]) for j in range(5))


def main():
    frozen = BASE / 'phase6-protected-bases-input-v1.tex'
    prior_path = BASE / 'hard-support-templates-results-v3.json'
    prior = json.loads(prior_path.read_text())
    text = frozen.read_text()
    blocks = dict(re.findall(r'% BEGIN ([A-Z0-9-]+)\n(.*?)% END \1', text, re.S))

    def edge_words(name):
        return {edge(a,b) for a,b in re.findall(r'([0-3]{5})-([0-3]{5})', blocks[name])}

    cache = {}
    def protected(key):
        if key in cache:
            return cache[key]
        t, component = key.split(':')
        pool = edge_words('POOL-'+t+'-'+component)
        if t in ('00001','00112'):
            basis = edge_words('COMMON-00001' if t=='00001' else 'PORTS-00112')
        else:
            words = re.findall(r'\b[0-3]{5}\b', blocks['FACTOR-00000' if t=='00000' else 'C1-'+t])
            if t=='00000':
                words = words[15*int(component):15*(int(component)+1)]
            basis = {edge(words[i],words[(i+1)%len(words)]) for i in range(len(words))}
        assert pool <= basis
        cache[key] = basis-pool
        return cache[key]

    support = {}
    for key in ('00001:0','00112:0'):
        K = protected(key)
        V = {v for e in K for v in e}
        J = {edge(a,b) for a in V for b in V if sum(x!=y for x,y in zip(a,b))==1}
        assert len(V)==20 and len(J)==17
        support[key] = J
    groups = defaultdict(list)
    for s in prior['hard_side_profiles_all53']:
        groups[(s['hard_type'], s['canonical_changed_position'], s['opposite_colour'])].append(s)
    results = []
    for signature, incidences in sorted(groups.items()):
        variant_records = {}
        u = incidences[0]['opposite_boundary_in_hard_coordinates']
        delta = incidences[0]['surviving_missing_edge_budget']
        J = {e for e in support[signature[0]] if all(all(v[j]!=u[j] for j in range(5)) for v in e)}
        for s in incidences:
            h = s['relative_opposite_normalizer']
            variant_key = (s['opposite_component'], h[0], h[1], tuple(h[2]))
            opposite = protected(s['opposite_component'])
            retained = {e for e in J if edge(transform(e[0],h),transform(e[1],h)) in opposite}
            assert counts(retained) == s['opposite_retained_counts_in_fixed_support']
            if variant_key in variant_records:
                assert variant_records[variant_key]['retained']==retained
                variant_records[variant_key]['cases'].append(s['case'])
            else:
                variant_records[variant_key]={'retained':retained, 'cases':[s['case']],
                    'opposite_component':s['opposite_component'],'relative_opposite_normalizer':h}
        sets = [v['retained'] for v in variant_records.values()]
        core = set.intersection(*sets)
        min_counts = [min(counts(R)[j] for R in sets) for j in range(5)]
        union_choices = []
        for mask in range(1,32):
            js = [j for j in range(5) if mask & (1<<j)]
            lower = min(sum(counts(R)[j] for j in js) for R in sets)
            budget = sum(delta[j] for j in js)
            if lower > budget:
                union_choices.append((len(js), -(lower-budget), js, lower, budget))
        best_union = min(union_choices) if union_choices else None
        core_counts = counts(core)
        same_sets = all(R==sets[0] for R in sets)
        results.append({'hard_type':signature[0], 'canonical_changed_position':signature[1],
                        'opposite_colour':signature[2], 'opposite_boundary':u,
                        'incidence_count':len(incidences), 'transport_variant_count':len(sets),
                        'all_local_retaining_subsets_identical':same_sets,
                        'legal_support_edge_count':len(J),'surviving_missing_budget':delta,
                        'minimum_retained_counts':min_counts,
                        'uniform_count_hit_coordinates':[j for j in range(5) if min_counts[j]>delta[j]],
                        'common_opposite_variant_core':sorted(core), 'common_core_counts':core_counts,
                        'common_core_capacity_hit_coordinates':[j for j in range(5) if core_counts[j]>delta[j]],
                        'best_uniform_coordinate_union': None if best_union is None else {
                            'coordinates':best_union[2], 'minimum_retained_count':best_union[3],
                            'missing_edge_budget':best_union[4], 'capacity_bound':best_union[3]-best_union[4]},
                        'variants':[{'opposite_component':v['opposite_component'],
                             'relative_opposite_normalizer':v['relative_opposite_normalizer'],
                             'retained_local_edges':sorted(v['retained']), 'retained_counts':counts(v['retained']),
                             'cases':v['cases']} for v in variant_records.values()]})
    F = {edge(a,b) for a,b in [('12320','32320'),('13230','23230'),
                              ('21301','31301'),('31201','31301')]}
    family_J = {e for e in support['00112:0'] if all(all(v[j]!='00012'[j] for j in range(5)) for v in e)}
    assert F == {e for e in family_J if coordinate(e) in (0,2)}
    assert len(F)==4 and len(protected('00112:0') & F)==3
    maps = [[0,1,[0,1,2,3]],[2,-1,[0,2,1,3]]]
    family_group = next(g for g in results if (g['hard_type'],g['canonical_changed_position'],g['opposite_colour'])==('00112:0',2,0))
    assert family_group['incidence_count']==3
    assert {json.dumps(v['relative_opposite_normalizer']) for v in family_group['variants']} == {json.dumps(h) for h in maps}
    fixed_ports = {edge(a,b) for a,b in [('12320','32320'),('13230','23230'),('13103','13203')]}
    assert fixed_ports <= protected('00012:0')
    family_counts = []
    for h in maps:
        available = sum(edge(transform(a,h),transform(b,h)) in protected('00012:0') for a,b in F)
        assert available==2
        family_counts.append(available)
    output = {'status':'FINITE_LOCAL_OPPOSITE_TRANSPORT_VARIANT_COMPARISON',
              'input_sha256':{frozen.name:sha(frozen),prior_path.name:sha(prior_path)},
              'script_sha256':sha(Path(__file__)), 'canonical_boundary_group_count':len(results),
              'hard_incidence_count':len(prior['hard_side_profiles_all53']),
              'same_local_subset_group_count':sum(g['all_local_retaining_subsets_identical'] for g in results),
              'uniform_count_positive_group_count':sum(bool(g['uniform_count_hit_coordinates']) for g in results),
              'universal_opposite_core_positive_group_count':sum(bool(g['common_core_capacity_hit_coordinates']) for g in results),
              'uniform_coordinate_union_positive_group_count':sum(g['best_uniform_coordinate_union'] is not None for g in results),
              'all_literal_retention_vectors_match_frozen_v3':True,
              'groups':results,
              'two_orientation_four_edge_family': {'hard_type':'00112:0','opposite_boundary':'00012',
                  'canonical_change':[2,0],'universe':sorted(F),'hard_retained_count':3,
                  'opposite_component':'00012:0','relative_maps':maps,'opposite_retained_counts':family_counts,
                  'three_protected_opposite_template_ports':sorted(fixed_ports),
                  'common_protected_capacity':3+2-4,'actual_interface_count':3},
              'original_interface_hard_opposite_protected_edge_intersection_computed':False,
              'local_opposite_variant_intersection_computed':True,
              'full_fibre_graphs_generated':False,'HC_search':False,
              'proof_boundary':'Recorded transport variants only; intersections among local opposite variants identify finite shared retention, not a universal Hamilton-cycle or natural-equivariance theorem.'}
    path=BASE/'transport-variant-subsets-results-v4.json'
    path.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:output[k] for k in ('canonical_boundary_group_count','hard_incidence_count',
                       'same_local_subset_group_count','uniform_count_positive_group_count',
                       'universal_opposite_core_positive_group_count','uniform_coordinate_union_positive_group_count',
                       'all_literal_retention_vectors_match_frozen_v3')},indent=2))


if __name__=='__main__':
    main()
