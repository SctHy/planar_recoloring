"""Natural boundary/component actions only; no cycle or seed search."""
from pathlib import Path
from itertools import product, permutations
import hashlib, json, re, time

HERE=Path(__file__).resolve().parent
INP=HERE.parents[1]/'clique_lifts/protected_interfaces/constant_orbit_pools/literal-input.tex'
TYPES=('00001','00011','00012','00101','00102','00112','00121','00123','01012','01023',
       '00004','00014','00104','00114','00124','01014','01024','01104','01124','01204','01234')
PERMS=tuple(permutations('0123'))

def move(w,g):
    s,eps,p=g
    return ''.join('4' if w[(s+eps*i)%5]=='4' else p[int(w[(s+eps*i)%5])] for i in range(5))

def closure(generators,identity):
    # Permutation convention: composition (a*b)(v)=a(b(v)).
    found={identity};todo=[identity]
    while todo:
        a=todo.pop()
        for b in generators:
            c=tuple(a[b[i]] for i in range(len(a)))
            if c not in found:found.add(c);todo.append(c)
    return frozenset(found)

def main():
    start=time.perf_counter();text=INP.read_text()
    blocks=dict(re.findall(r'% BEGIN ([A-Z0-9-]+)\n(.*?)% END \1',text,re.S))
    detail={}
    for t in TYPES:
        ws=sorted(''.join(w) for w in product('0123',repeat=5)
                  if all(w[i]!=w[(i+1)%5] and (t[i]=='4' or w[i]!=t[i]) for i in range(5)))
        ix={w:i for i,w in enumerate(ws)};identity=tuple(range(len(ws)))
        if t in ('00001','00112'):
            name='PC2-00001' if t=='00001' else 'C2-00112'
            listed={w[1:] for w in re.findall(r'\b[01][0-3]{5}\b',blocks[name])}
        else:
            name=('FHC-' if '4' in t else 'C1-')+t
            listed=set(re.findall(r'\b[0-3]{5}\b',blocks[name]))
        assert listed==set(ws)
        group=[];by_action={}
        for s in range(5):
            for eps in (1,-1):
                for p in PERMS:
                    g=(s,eps,p)
                    if move(t,g)!=t:continue
                    moved=[move(w,g) for w in ws]
                    assert set(moved)==set(ws)
                    action=tuple(ix[w] for w in moved)
                    fixed=[w for i,w in enumerate(ws) if action[i]==i]
                    record={'shift':s,'orientation':eps,'colour_images':''.join(p),
                            'fixed_count':len(fixed),'fixed_states':fixed,
                            'identity_on_states':action==identity,
                            'full_cycle_obstruction':action!=identity and len(fixed)>=3,
                            'P2_seed_obstruction':action!=identity and 2*len(fixed)>=3,
                            'P3_seed_obstruction':action!=identity and 3*len(fixed)>=3}
                    group.append(record);by_action.setdefault(action,[]).append(record)
        # Enumerate all subgroups of the at-most-twelve-element induced group.
        actions=set(by_action);subgroups={frozenset({identity})};todo=list(subgroups)
        while todo:
            h=todo.pop()
            for a in actions-h:
                hh=closure(list(h)+[a],identity)
                assert hh<=actions
                if hh not in subgroups:subgroups.add(hh);todo.append(hh)
        good=lambda h,rows:all(a==identity or rows*sum(i==a[i] for i in range(len(ws)))<=2 for a in h)
        allowed={}
        for rows,key in ((1,'cycle'),(2,'P2_seed'),(3,'P3_seed')):
            ok=[h for h in subgroups if good(h,rows)]
            maximum=max(map(len,ok))
            allowed[key]={'max_subgroup_order_not_ruled_out_by_fixed_points':maximum,
                          'maximal_order_examples':[[by_action[a][0] for a in sorted(h)]
                                                    for h in sorted(ok,key=lambda h:(len(h),sorted(h))) if len(h)==maximum],
                          'allowed_subgroup_orders':sorted({len(h) for h in ok})}
        def histogram(key):
            return {str(n):sum(d['fixed_count']==n for d in group)
                    for n in sorted({d['fixed_count'] for d in group})}
        detail[t]={'states':len(ws),'boundary_component_group_order':len(group),
                   'induced_group_order':len(actions),'action_kernel_order':sum(d['identity_on_states'] for d in group),
                   'fixed_point_histogram_including_identity':histogram('fixed_count'),
                   'nonidentity_cycle_obstruction_elements':sum(d['full_cycle_obstruction'] for d in group),
                   'nonidentity_P2_seed_obstruction_elements':sum(d['P2_seed_obstruction'] for d in group),
                   'nonidentity_P3_seed_obstruction_elements':sum(d['P3_seed_obstruction'] for d in group),
                   'group_elements':group,'subgroup_count':len(subgroups),'remaining_fixed_point_compatible_subgroups':allowed}
    result={'scope':'Exact complete-state group-action counts; no Hamilton cycle search or K-invariance impossibility inferred',
            'literal_input_sha256':hashlib.sha256(INP.read_bytes()).hexdigest(),
            'types':len(TYPES),'total_nonconstant_states':sum(d['states'] for d in detail.values()),
            'elapsed_seconds':time.perf_counter()-start,'by_type':detail}
    (HERE/'fixed-point-results.json').write_text(json.dumps(result,indent=2)+'\n')
    for t,d in detail.items():
        print(t,d['states'],'Gamma',d['boundary_component_group_order'],'hist',d['fixed_point_histogram_including_identity'],
              'bad_cycle/P2/P3',[d['nonidentity_'+k+'_obstruction_elements'] for k in ('cycle','P2_seed','P3_seed')],
              'maxH',[d['remaining_fixed_point_compatible_subgroups'][k]['max_subgroup_order_not_ruled_out_by_fixed_points'] for k in ('cycle','P2_seed','P3_seed')])
    print('seconds',result['elapsed_seconds'])

if __name__=='__main__':main()
