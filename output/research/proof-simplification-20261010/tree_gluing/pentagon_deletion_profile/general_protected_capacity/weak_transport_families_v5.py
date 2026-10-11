#!/usr/bin/env python3
"""Saved-list candidate scan plus selected named-edge transport checks.

No producer reruns, full fibres, HC searches or full paired protected
intersections. Literal opposite bases are read only for the selected ports.
"""
from pathlib import Path
import hashlib
import json
import platform
import re
import sys

BASE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def edge(a,b):
    return tuple(sorted((a,b)))


def transform(word,mapping):
    start,sign,perm = mapping
    return ''.join(str(perm[int(word[(start+sign*j) % 5])]) for j in range(5))


def image(e,mapping):
    return edge(*(transform(w,mapping) for w in e))


def legal(word,boundary):
    return (all(word[j] != word[(j+1) % 5] for j in range(5))
            and all(word[j] != boundary[j] for j in range(5)))


def main():
    source = BASE/'phase6-protected-bases-input-v1.tex'
    saved_path = BASE/'transport-variant-subsets-results-v4.json'
    manifest_path = BASE/'frozen-manifest-v4.json'
    manifest = json.loads(manifest_path.read_text())
    for name in (source.name,saved_path.name):
        assert sha(BASE/name) == manifest[name]
    saved = json.loads(saved_path.read_text())
    assert len(saved['groups']) == 30 and saved['hard_incidence_count'] == 58
    text = source.read_text()
    blocks = dict(re.findall(r'% BEGIN ([A-Z0-9-]+)\n(.*?)% END \1',text,re.S))

    def read_edges(name):
        return {edge(a,b) for a,b in re.findall(r'([0-3]{5})-([0-3]{5})',blocks[name])}

    hard_bases = {'00001:0':read_edges('COMMON-00001'),'00112:0':read_edges('PORTS-00112')}
    hard_protected = {t:E-read_edges('POOL-'+t[:5]+'-0') for t,E in hard_bases.items()}
    cache = {}

    def basis_and_pool(key):
        if key in cache:
            return cache[key]
        t,c = key.split(':')
        if key in hard_bases:
            basis = hard_bases[key]
        else:
            assert t != '00000', 'selected families do not read constant bases'
            words = re.findall(r'\b[0-3]{5}\b',blocks['C1-'+t])
            basis = {edge(a,b) for a,b in zip(words,words[1:]+words[:1])}
        pool = read_edges('POOL-'+t+'-'+c)
        assert pool <= basis
        cache[key] = basis,pool
        return cache[key]

    def group_key(group):
        return (group['hard_type'],group['canonical_changed_position'],group['opposite_colour'])

    groups = {group_key(g):g for g in saved['groups']}
    candidates = []
    for signature,g in sorted(groups.items()):
        ports = [e for e in sorted(hard_protected[signature[0]])
                 if all(list(e) in v['retained_local_edges'] for v in g['variants'])]
        candidates.append({'hard_type':signature[0],'change':list(signature[1:]),
            'opposite_boundary':g['opposite_boundary'],'variant_count':len(g['variants']),
            'incidence_count':g['incidence_count'],'fixed_hard_port_candidates_from_saved_lists':ports})
    assert sum(bool(c['fixed_hard_port_candidates_from_saved_lists']) for c in candidates) == 28
    selected = [
        ('hard00112_e14','00112:0',edge('13230','23230'),[(0,3),(1,2),(2,0),(2,3),(3,0),(4,1),(4,3)]),
        ('hard00001_f12','00001:0',edge('21230','23230'),[(0,1),(0,3),(2,1),(2,3),(3,1),(3,2)])]
    witness_rows = re.findall(r'([0-3]{5}:\d)\s+(\d)\s+(\d)\s+([0-3]{5}:\d)\s+([0-3]{5})-([0-3]{5})',blocks['INTERFACES-ALL'])
    witness_lookup = {(s,int(r),int(q),t):edge(a,b) for s,r,q,t,a,b in witness_rows}

    def check_named_port(port,g,v):
        assert port in hard_protected[g['hard_type']]
        assert all(legal(w,g['opposite_boundary']) for w in port)
        mapping = v['relative_opposite_normalizer']
        start,sign,perm = mapping
        assert start in range(5) and sign in (-1,1) and sorted(perm) == list(range(4))
        assert transform(g['opposite_boundary'],mapping) == v['opposite_component'][:5]
        target = image(port,mapping)
        assert all(legal(w,v['opposite_component'][:5]) for w in target)
        assert sum(a != b for a,b in zip(*target)) == 1
        basis,pool = basis_and_pool(v['opposite_component'])
        assert target in basis and target not in pool
        assert list(port) in v['retained_local_edges']
        witnesses = []
        for case in v['cases']:
            new_physical = port if case[0] == g['hard_type'] else target
            witnesses.append({'case':case,'old_physical_witness':witness_lookup[tuple(case)],
                              'new_physical_witness':new_physical})
        return {'opposite_component':v['opposite_component'],'relative_map':mapping,
                'hard_port':port,'ordinary_or_hard_template_image':target,
                'image_in_basis':True,'image_outside_pool':True,'witnesses':witnesses}

    families = []
    for name,t,port,changes in selected:
        checks = []
        for r,q in changes:
            g = groups[(t,r,q)]
            checks.append({'change':[r,q],'opposite_boundary':g['opposite_boundary'],
                'incidence_count':g['incidence_count'],
                'variants':[check_named_port(port,g,v) for v in g['variants']]})
        images = sorted({(v['opposite_component'],tuple(v['ordinary_or_hard_template_image']))
                         for c in checks for v in c['variants']})
        cases = sorted({tuple(w['case']) for c in checks for v in c['variants'] for w in v['witnesses']})
        families.append({'name':name,'hard_type':t,'fixed_hard_port':port,
            'changes':changes,'incidence_count':sum(c['incidence_count'] for c in checks),
            'distinct_actual_interface_count':len(cases),'distinct_image_membership_count':len(images),
            'distinct_image_memberships':[{'component':t,'image':e} for t,e in images],
            'checks':checks})
    assert [f['incidence_count'] for f in families] == [14,12]
    assert [f['distinct_image_membership_count'] for f in families] == [10,9]

    g = groups[('00112:0',4,0)]
    A,B = edge('21301','21321'),edge('32301','32321')
    expected = {(4,1,(0,1,2,3)),(4,1,(0,1,3,2)),(1,-1,(0,1,2,3)),(1,-1,(0,1,3,2))}
    assert {(v['relative_opposite_normalizer'][0],v['relative_opposite_normalizer'][1],
             tuple(v['relative_opposite_normalizer'][2])) for v in g['variants']} == expected
    orientation_checks = [check_named_port(A if v['relative_opposite_normalizer'][1] == 1 else B,g,v)
                          for v in g['variants']]
    assert len(orientation_checks) == 4
    family = {'name':'hard00112_orientation_pair5','hard_type':'00112:0',
        'change':[4,0],'opposite_boundary':'00110','opposite_component':'00011:0',
        'hard_ports':{'rotation':A,'reflection':B},'incidence_count':5,
        'map_parameterization':'rho(start4,+1) or eta(start1,-1), followed by id or swap2and3',
        'variants':orientation_checks,'common_saved_local_port_exists':False}
    families.append(family)
    nine = [c for c in families[0]['checks'] if tuple(c['change']) in ((2,0),(2,3),(3,0))]
    assert sum(c['incidence_count'] for c in nine) == 9
    all_cases = {tuple(w['case']) for f in families[:2] for c in f['checks']
                 for v in c['variants'] for w in v['witnesses']}
    all_cases |= {tuple(w['case']) for v in orientation_checks for w in v['witnesses']}
    assert len(all_cases) == 30
    output = {'status':'FINITE_NAMED_PORT_TRANSPORT_FAMILIES_CHECKED',
        'runtime':{'executable':sys.executable,'python_version':platform.python_version()},
        'input_sha256':{source.name:sha(source),saved_path.name:sha(saved_path),manifest_path.name:sha(manifest_path)},
        'script_sha256':sha(Path(__file__)),
        'candidate_group_count':len(candidates),'group_count_with_saved_fixed_hard_port':28,
        'candidate_classification':candidates,'selected_families':families,
        'nine_interface_same_port_subfamily':{'hard_type':'00112:0','hard_port':edge('13230','23230'),
            'changes':[[2,0],[2,3],[3,0]],'incidence_count':9,'group_checks':nine},
        'selected_group_count':14,'selected_hard_incidence_count':31,'distinct_selected_interface_count':len(all_cases),
        'selected_transformed_edge_membership_check_count':sum(len(c['variants']) for f in families[:2] for c in f['checks'])+4,
        'prior_thirty_group_producer_rerun':False,'prior313_interface_computation_rerun':False,
        'full_fibre_generated':False,'HC_search':False,'new_normalizers_generated':False,
        'full_original_paired_protected_intersections_enumerated':False,
        'whole_template_or_pool_equivariance_claimed':False,
        'proof_boundary':'Named ports in the frozen selected bases and prescribed recorded maps only. Larger fixed-port families remain finite map classification; no printed-length gain or arbitrary-cycle theorem follows.'}
    destination = BASE/'weak-transport-families-results-v5.json'
    assert not destination.exists(), 'preserve an existing executed result'
    destination.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:output[k] for k in ('status','candidate_group_count',
        'group_count_with_saved_fixed_hard_port','selected_group_count','selected_hard_incidence_count',
        'distinct_selected_interface_count','selected_transformed_edge_membership_check_count')},indent=2))


if __name__ == '__main__':
    main()
