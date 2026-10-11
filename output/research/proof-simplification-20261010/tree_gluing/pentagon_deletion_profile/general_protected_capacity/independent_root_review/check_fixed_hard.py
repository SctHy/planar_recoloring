"""Independent fixed-J budget extraction from already verified v2 scalars.

Reuse only this reviewer's own finite-set functions and independently
verified scalar input. Reconstruct two20-state supports, not all fibres.
"""
from pathlib import Path
from collections import Counter
import hashlib,json,re,sys
from check_protected_capacity import edge,raw_edges,endpoints,counts,move_edges,restore

here=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
text=(here/'phase6-source.tex').read_text()
assert sha(here/'phase6-source.tex')=='7a90f79db489447b0bad3019217fd369a5cc25986288247981cbe7f3462acba3'
blocks=dict(re.findall(r'^% BEGIN ([^\n]+)\n(.*?)^% END \1$',text,re.S|re.M))
pairs=lambda name:{edge(x,y) for x,y in re.findall(r'\b([0-3]{5})-([0-3]{5})\b',blocks[name])}
hard={}
for t,b,k in [('00001','COMMON-00001',1),('00112','PORTS-00112',2)]:
    K=pairs(b)-pairs('POOL-'+t+'-0');J=raw_edges(endpoints(K));M=J-K
    assert (len(K),len(endpoints(K)),len(J),len(M))==(11,20,17,6)
    assert counts(M)[k]==0
    hard[t]=(K,J,M,k)
source=json.loads((here/'expected-port-support.json').read_text())
summary={};exceptions=[];details=[]
for c in source['cases']:
    if c['group'] not in ['nonconstant-source-hard-53','constant-source-30']:continue
    witnesses=[]
    for role in ['source','target']:
        t=c[role][:5]
        if t not in hard:continue
        K,J,M,k=hard[t]
        if role=='source':
            j=c['changed_position'];u=t[:j]+str(c['new_colour'])+t[j+1:]
            physical=list(range(5));ell=c['y']
        else:
            start,sign,p=c['normalizer'];physical=[(start+sign*j)%5 for j in range(5)]
            u=''.join(str(p[int(c['source'][(start+sign*j)%5])]) for j in range(5))
            ell=c['x']
        assert sum(x!=y for x,y in zip(t,u))==1
        legalM={e for e in M if all(all(v[j]!=u[j] for j in range(5)) for v in e)}
        delta=counts(legalM);exactell=[ell[j] for j in physical]
        witnesses.append({'role':role,'hard_type':t,'opposite_boundary':u,
                          'ell_exact':exactell,'missing_surviving':delta,
                          'fixed_saturated_hit':exactell[k]>0,
                          'full_missing_hit':max(exactell[j]-counts(M)[j] for j in range(5))>0,
                          'legal_missing_hit':max(exactell[j]-delta[j] for j in range(5))>0})
    key=[c['source'],c['changed_position'],c['new_colour'],c['target']]
    flags={field:any(w[field] for w in witnesses) for field in ['fixed_saturated_hit','full_missing_hit','legal_missing_hit']}
    summary.setdefault(c['group'],Counter()).update(total=1,**{k:int(v) for k,v in flags.items()})
    details.append({'case':key,'hard_sides':witnesses,**flags})
    if not flags['legal_missing_hit']:
        assert c['source']==c['target'] and c['source'][:5] in hard
        K,J,M,k=hard[c['source'][:5]];L=move_edges(K,c['normalizer'])
        W=endpoints(K)&endpoints(L);H=raw_edges(W)
        assert len(W)==6 and K&H==H and L&H==H
        degree=Counter(v for e in H for v in e)
        shape='P2+4K1' if len(H)==1 else 'P3+3K1'
        assert sorted(degree.values())==([1,1] if len(H)==1 else [1,1,2])
        exceptions.append({'case':key,'vertices':sorted(W),'edges':sorted(H),'shape':shape,'all_edges_retained_by_each':True})
assert summary['nonconstant-source-hard-53']=={'total':53,'fixed_saturated_hit':32,'full_missing_hit':44,'legal_missing_hit':51}
assert len(exceptions)==2
result={'status':'PASS_FIXED_HARD_MISSING_BUDGET_READBACK','backend_version':sys.version.split()[0],
 'source_sha256':sha(here/'phase6-source.tex'),'independently_verified_v2_counts_sha256':sha(here/'expected-port-support.json'),
 'coverage':summary,'two_exceptions':exceptions,'all_case_details':details,
 'identity':'For L edges, membership in J_t(u) is equivalent to membership in common G[V(K_t) intersect V(L)]; hence ell is exact, not merely a lower bound.',
 'HC_search':False,'full_fibre_graph_regeneration':False,'K_L_intersection_computed':False,
 'scope':'Fixed templates and specified53+30 cases; positivity51 is finite evidence, not symbolic classification.'}
(here/'fixed-hard-review-results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['all_case_details']},indent=2))
