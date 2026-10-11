#!/usr/bin/env python3
"""Case-set union only, from retained results; no mathematical producer reruns."""
from pathlib import Path
import hashlib
import json

BASE=Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    transport_path=BASE/'weak-transport-families-results-v5.json'
    degree_path=BASE/'one_sided_degree_v1/one-sided-degree-results-v1.json'
    allhard_path=BASE/'hard-support-templates-results-v3.json'
    manifest=json.loads((BASE/'frozen-manifest-v5.json').read_text())
    assert sha(transport_path)==manifest[transport_path.name]
    assert sha(allhard_path)==manifest[allhard_path.name]
    transport=json.loads(transport_path.read_text())
    degree=json.loads(degree_path.read_text())
    allhard=json.loads(allhard_path.read_text())
    universe={tuple(s['case']) for s in allhard['hard_side_profiles_all53']}
    assert len(universe)==53
    T=set()
    byfamily={}
    for f in transport['selected_families']:
        variants=[v for c in f['checks'] for v in c['variants']] if 'checks' in f else f['variants']
        cases={tuple(w['case']) for v in variants for w in v['witnesses']}
        byfamily[f['name']]=cases
        T|=cases
    hardtypes={'00001','00112'}
    def key(r):
        return (r['source']+':'+str(r['source_component']),r['position'],int(r['colour']),
                r['target_type']+':'+str(r['target_component']))
    degree_hard=[r for r in degree['records'] if r['source'] in hardtypes
                 and r['origin']=='existing283' and r['status']=='covered']
    D={key(r) for r in degree_hard}
    assert len(T)==30 and len(D)==19
    assert T<=universe and D<=universe
    union=T|D
    hardhard={c for c in universe if c[0][:5] in hardtypes and c[3][:5] in hardtypes}
    ordinarysource_hardtarget={c for c in universe if c[0][:5] not in hardtypes and c[3][:5] in hardtypes}
    hard_source_ordinarytarget={c for c in universe if c[0][:5] in hardtypes and c[3][:5] not in hardtypes}
    assert len(hardhard)==5 and len(ordinarysource_hardtarget)==22 and len(hard_source_ordinarytarget)==26
    output={'status':'EXACT_RETAINED_CASE_SET_UNION',
        'input_sha256':{str(p.relative_to(BASE)):sha(p) for p in (transport_path,degree_path,allhard_path)},
        'script_sha256':sha(Path(__file__)),
        'hard53_universe_count':len(universe),'transport_selected_count':len(T),'source_hard_any_opposite_HC_local_count':len(D),
        'overlap_count':len(T&D),'union_count':len(union),'uncovered_count':len(universe-union),
        'transport_cases':sorted(T),'source_hard_generic_local_cases':sorted(D),'overlap_cases':sorted(T&D),
        'union_cases':sorted(union),'local_only_additional_cases':sorted(D-T),'transport_only_cases':sorted(T-D),
        'uncovered_cases':sorted(universe-union),
        'per_transport_family':[{'name':name,'case_count':len(cases),
             'overlap_with_source_hard_any_HC_count':len(cases&D),
             'new_beyond_source_hard_any_HC_count':len(cases-D)} for name,cases in byfamily.items()],
        'hard_interface_role_partition':{'hard_source_ordinary_target_count':len(hard_source_ordinarytarget),
            'ordinary_source_hard_target_count':len(ordinarysource_hardtarget),'hard_hard_count':len(hardhard),
            'union_covered_by_role':{'hard_source_ordinary_target':len(union&hard_source_ordinarytarget),
            'ordinary_source_hard_target':len(union&ordinarysource_hardtarget),'hard_hard':len(union&hardhard)},
            'uncovered_by_role':{'hard_source_ordinary_target':sorted((universe-union)&hard_source_ordinarytarget),
            'ordinary_source_hard_target':sorted((universe-union)&ordinarysource_hardtarget),
            'hard_hard':sorted((universe-union)&hardhard)}},
        'premise_boundary':'Transport uses the stated selected opposite base/pool and prescribed maps. Source-hard generic local cases use hard K and the any-opposite-HC local inequality, not opposite selected-cycle membership. This extraction does not independently review either mathematical producer.',
        'graph_or_membership_producer_rerun':False,'frozen_v5_changed':False,'main_changed':False}
    path=BASE/'transport-degree-union-results-v1.json'
    assert not path.exists(),'preserve an existing result'
    path.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:output[k] for k in ('status','hard53_universe_count','transport_selected_count',
        'source_hard_any_opposite_HC_local_count','overlap_count','union_count','uncovered_count')},indent=2))


if __name__=='__main__':
    main()
