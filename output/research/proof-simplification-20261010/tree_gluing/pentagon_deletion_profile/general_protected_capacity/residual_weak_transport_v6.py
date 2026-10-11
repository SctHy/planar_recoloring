#!/usr/bin/env python3
"""Saved case unions plus six selected image memberships, no graph search."""
from pathlib import Path
import hashlib
import json
import platform
import re
import sys

BASE=Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def edge(a,b):
    return tuple(sorted((a,b)))


def transform(word,mapping):
    start,sign,perm=mapping
    return ''.join(str(perm[int(word[(start+sign*j)%5])]) for j in range(5))


def legal(word,boundary):
    return all(word[j]!=boundary[j] and word[j]!=word[(j+1)%5] for j in range(5))


def main():
    source=BASE/'phase6-protected-bases-input-v1.tex'
    group_path=BASE/'transport-variant-subsets-results-v4.json'
    transport_path=BASE/'weak-transport-families-results-v5.json'
    generic_path=BASE/'one_protected_vs_hc_v2/symmetric-one-sided-results-v2.json'
    universe_path=BASE/'hard-support-templates-results-v3.json'
    manifest_path=BASE/'frozen-manifest-v5.json'
    manifest=json.loads(manifest_path.read_text())
    for path in (source,group_path,transport_path,universe_path):
        assert sha(path)==manifest[path.name]
    assert sha(generic_path)=='6d16370fa156d7d739a6d8c2bec98ec75b8dbc640cb39183db1a89cb29499876'
    previous=json.loads(transport_path.read_text())
    generic=json.loads(generic_path.read_text())
    universe={tuple(s['case']) for s in json.loads(universe_path.read_text())['hard_side_profiles_all53']}
    T=set()
    for family in previous['selected_families']:
        variants=[v for c in family['checks'] for v in c['variants']] if 'checks' in family else family['variants']
        T|={tuple(w['case']) for v in variants for w in v['witnesses']}
    D=set()
    for record in generic['records']:
        if record['group'] in ('hard-source-HC-target26','HC-source-hard-target22') and record['covered']:
            c=record['interface']
            D.add((c['source']+':'+str(c['source_component']),c['position'],int(c['colour']),
                   c['target_type']+':'+str(c['target_component'])))
    assert (len(universe),len(T),len(D),len(T&D),len(T|D))==(53,30,34,22,42)
    assert T<=universe and D<=universe
    remaining=universe-(T|D)
    hardtypes={'00001','00112'}
    mixed_remaining={c for c in remaining if (c[0][:5] in hardtypes)!=(c[3][:5] in hardtypes)}
    assert len(mixed_remaining)==7
    blocks=dict(re.findall(r'% BEGIN ([A-Z0-9-]+)\n(.*?)% END \1',source.read_text(),re.S))
    def edges(name):
        return {edge(a,b) for a,b in re.findall(r'([0-3]{5})-([0-3]{5})',blocks[name])}
    hardK={'00001:0':edges('COMMON-00001')-edges('POOL-00001-0'),
           '00112:0':edges('PORTS-00112')-edges('POOL-00112-0')}
    ordinary_cache={}
    def ordinary(key):
        if key not in ordinary_cache:
            t,c=key.split(':')
            assert t not in hardtypes and t!='00000'
            words=re.findall(r'\b[0-3]{5}\b',blocks['C1-'+t])
            basis={edge(a,b) for a,b in zip(words,words[1:]+words[:1])}
            pool=edges('POOL-'+t+'-'+c)
            assert pool<=basis
            ordinary_cache[key]=(basis,pool)
        return ordinary_cache[key]
    groups={(g['hard_type'],g['canonical_changed_position'],g['opposite_colour']):g
            for g in json.loads(group_path.read_text())['groups']}
    selected=[('00001:0',edge('21313','21323'),[(1,2),(1,3)]),
              ('00112:0',edge('21301','21321'),[(0,1),(1,3)]),
              ('00112:0',edge('12320','32320'),[(2,2)])]
    families=[]
    all_new_cases=set()
    membership_count=0
    for t,port,changes in selected:
        assert port in hardK[t]
        checks=[]
        family_cases=set()
        for r,q in changes:
            g=groups[(t,r,q)]
            assert all(legal(w,g['opposite_boundary']) for w in port)
            for variant in g['variants']:
                mapping=variant['relative_opposite_normalizer']
                start,sign,perm=mapping
                assert start in range(5) and sign in (-1,1) and sorted(perm)==list(range(4))
                opposite=variant['opposite_component']
                assert transform(g['opposite_boundary'],mapping)==opposite[:5]
                target=edge(*(transform(w,mapping) for w in port))
                assert all(legal(w,opposite[:5]) for w in target)
                assert sum(a!=b for a,b in zip(*target))==1
                basis,pool=ordinary(opposite)
                assert target in basis and target not in pool
                assert list(port) in variant['retained_local_edges']
                cases={tuple(c) for c in variant['cases']}
                family_cases|=cases
                checks.append({'change':[r,q],'opposite_boundary':g['opposite_boundary'],
                    'opposite_component':opposite,'relative_map':mapping,'hard_port':port,
                    'protected_image':target,'image_in_cycle':True,'image_outside_pool':True,
                    'actual_cases':sorted(cases)})
                membership_count+=1
        all_new_cases|=family_cases
        families.append({'hard_type':t,'hard_port':port,'changes':changes,
                         'distinct_case_count':len(family_cases),'checks':checks})
    assert membership_count==6 and all_new_cases==mixed_remaining
    final=T|D|all_new_cases
    final_remaining=universe-final
    assert len(final)==49 and len(final_remaining)==4
    assert all(c[0][:5] in hardtypes and c[3][:5] in hardtypes for c in final_remaining)
    output={'status':'SIX_NAMED_IMAGE_MEMBERSHIPS_FOR_SEVEN_RESIDUAL_MIXED_INTERFACES_PASSED',
        'runtime':{'python_version':platform.python_version(),'executable':sys.executable},
        'input_sha256':{str(p.relative_to(BASE)):sha(p) for p in (source,group_path,transport_path,generic_path,universe_path,manifest_path)},
        'script_sha256':sha(Path(__file__)),
        'previous_transport_count':30,'bidirectional_generic_local_count':34,
        'previous_overlap_count':22,'starting_union_count':42,'starting_remaining':sorted(remaining),
        'new_selected_family_count':3,'named_image_membership_count':membership_count,
        'new_actual_case_count':len(all_new_cases),'new_families':families,
        'all_new_cases':sorted(all_new_cases),'ending_union_count':49,'ending_remaining':sorted(final_remaining),
        'ending_union_cases':sorted(final),
        'graph_or_membership_producers_rerun':False,'full_fibre_generated':False,'HC_search':False,
        'full_paired_protected_intersections_enumerated':False,'frozen_v4_v5_changed':False,'main_changed':False,
        'premise_boundary':'The34 generic-local cases retain any-HC scope from their source. The30 prior and7 new transport cases retain selected-basis/pool and prescribed-map scope. No composite symbolic proof of all49degree/transport cases or length improvement is claimed.'}
    path=BASE/'residual-weak-transport-results-v6.json'
    assert not path.exists(),'preserve an existing result'
    path.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:output[k] for k in ('status','starting_union_count','new_selected_family_count',
        'named_image_membership_count','new_actual_case_count','ending_union_count','ending_remaining')},indent=2))


if __name__=='__main__':
    main()
