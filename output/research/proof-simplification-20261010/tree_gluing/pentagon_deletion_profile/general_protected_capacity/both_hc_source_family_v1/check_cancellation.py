#!/usr/bin/env python3
"""Verify alpha/beta cancellation from frozen scalars; no new neighbours."""
from pathlib import Path
from collections import Counter
import hashlib,json,platform
HERE=Path(__file__).resolve().parent

def run():
    p=HERE/'frozen-both-hc-local-results.json';raw=p.read_bytes();data=json.loads(raw)
    selected=json.loads((HERE/'set-cover-results.json').read_text())
    counts=Counter();observations=[];annotations={}
    for row in data['records']:
        a=row['interface'];t,j,q=a['source'],a['position'],a['colour']
        assert t[j]!=q and t[j]!='4'
        for o in row['all_local_observations']:
            x=o['state'];assert x[j]!=t[j] and x[j]!=q
            neighbours={x[(j-1)%5],x[(j+1)%5]}
            alpha=int(t[j] not in neighbours);beta=int(q not in neighbours and q!=x[j])
            ds,dt,dc,f=o['source_degree'],o['target_degree'],o['common_incident_count'],o['forbidden_common_count']
            assert dt==ds+alpha-beta and dc==ds-beta
            closed=max(0,4-ds-alpha-f)
            assert closed==o['safe_common_edge_lower_bound']==max(0,4-ds-dt+dc-f)
            observations.append(dict(interface={k:a[k] for k in ('source','source_component','position','colour','target_type','target_component')},state=x,source_degree=ds,alpha=alpha,beta=beta,pool_forbidden_common=f,closed_lower_bound=closed))
            counts[f'd{ds}/a{alpha}/f{f}/positive{int(closed>0)}']+=1
            if t in selected['source_families'] and x in selected['source_families'][t]['selected_words']:
                J=[i for i in range(5) if t[i]!='4' and t[i] in {x[(i-1)%5],x[(i+1)%5]}]
                key=t+':'+x;annotation=dict(source=t,state=x,source_degree=ds,useful_coordinates=J)
                assert key not in annotations or annotations[key]==annotation
                annotations[key]=annotation
    assert len(observations)==10379
    selected_observations=[]
    for t,family in selected['source_families'].items():
        for choice in family['coverage_map']:
            a=choice['interface'];x=choice['selected_state'];o=choice['certificate']
            alpha=int(a['source'][a['position']] not in {x[(a['position']-1)%5],x[(a['position']+1)%5]})
            assert o['source_degree']+alpha==3 and o['forbidden_common_count']==0
            selected_observations.append(dict(source=t,interface_index=choice['interface_index'],position=a['position'],colour=a['colour'],state=x,source_degree=o['source_degree'],alpha=alpha,f=0,closed_lower_bound=1))
    assert len(selected_observations)==27 and len(annotations)==9
    out=dict(status='PASS',python=platform.python_version(),input_sha256=hashlib.sha256(raw).hexdigest(),selected_cover_input_sha256=hashlib.sha256((HERE/'set-cover-results.json').read_bytes()).hexdigest(),code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),candidate_observations_checked=len(observations),degree_change_identity='dt=ds+alpha-beta',common_degree_identity='dc=ds-beta',closed_rule='max(0,4-ds-alpha-f)',all_frozen_scalars_match=True,selected27_all_ds_plus_alpha_equals3_and_f0=True,selected_word_annotations=[annotations[k] for k in sorted(annotations)],selected27_coverage=selected_observations,scalar_type_counts=dict(sorted(counts.items())),observations=observations,scope='Pure extraction and algebraic scalar comparison over all frozen10379original candidate observations; no neighbour regeneration or Hamilton computation.')
    (HERE/'cancellation-results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ('status','candidate_observations_checked','closed_rule','all_frozen_scalars_match','selected27_all_ds_plus_alpha_equals3_and_f0','selected_word_annotations')},indent=2))

if __name__=='__main__':run()
