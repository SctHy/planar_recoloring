"""Nine exact constant-pool redesigns, with target-family equivariance checks."""
from pathlib import Path
from itertools import product
import hashlib, json, re, time
from base_check import (STANDARD, HARD, edge, word_tuple, word_text,
                        cycle_edges, transform, normalize, restore)

HERE=Path(__file__).resolve().parent


def main():
    start=time.perf_counter()
    inp=HERE/'literal-input.tex'
    text=inp.read_text()
    blocks=dict(re.findall(r'% BEGIN ([A-Z0-9-]+)\n(.*?)% END \1',text,re.S))
    def words(name):
        return [word_tuple(w) for w in re.findall(r'\b[0-3]{5}\b',blocks[name])]
    def edges(name):
        return {edge(word_tuple(a),word_tuple(b)) for a,b in
                re.findall(r'\b([0-3]{5})-([0-3]{5})\b',blocks[name])}
    states={}; original_K={}; full_edges={}; old_pools={}
    cc=words('FACTOR-00000'); assert len(cc)==30
    for t in STANDARD:
        vs={w for w in product(range(4),repeat=5)
            if all(w[i]!=w[(i+1)%5] for i in range(5))
            and all(t[i]=='4' or w[i]!=int(t[i]) for i in range(5))}
        components=[set(cc[:15]),set(cc[15:])] if t=='00000' else [vs]
        for index,component in enumerate(components):
            key=f'{t}:{index}'
            states[key]=component
            if t=='00000': ee=cycle_edges(cc[index*15:(index+1)*15])
            elif t in HARD: ee=edges('COMMON-00001' if t=='00001' else 'PORTS-00112')
            else: ee=cycle_edges(words(('FHC-' if '4' in t else 'C1-')+t))
            pp=edges(f'POOL-{t}-{index}')
            assert pp<=ee and len(pp)==(7 if t in HARD else 8)
            assert all(a in component and b in component and
                       sum(x != y for x,y in zip(a,b))==1 for a,b in ee)
            original_K[key]=ee-pp; full_edges[key]=ee; old_pools[key]=pp
    records=re.findall(r'([0-4]{5}:[01])\s+([0-4])\s+([0-3])\s+([0-4]{5}:[01])\s+([0-3]{5})-([0-3]{5})',blocks['INTERFACES-ALL'])
    assert len(records)==313
    parsed=[]
    for source,ps,cs,target,ws,zs in records:
        pos,new=int(ps),int(cs); t=word_tuple(source[:5])
        changed=t[:pos]+(new,)+t[pos+1:]
        nt,g=normalize(changed); assert nt==target[:5]
        restored=lambda es,g=g:{edge(restore(a,g),restore(b,g)) for a,b in es}
        old_TK=restored(original_K[target])
        assert edge(word_tuple(ws),word_tuple(zs)) in original_K[source]&old_TK
        parsed.append({'source':source,'position':pos,'new_excluded':new,
                       'target':target,'mapping':g,'old_witness':edge(word_tuple(ws),word_tuple(zs))})

    rotation=(1,1,(0,1,2,3))
    def rotate_edges(es,r=1):
        g=(r%5,1,(0,1,2,3))
        return {edge(transform(a,g),transform(b,g)) for a,b in es}
    orbits={}
    for key in ('00000:0','00000:1'):
        assert {transform(w,rotation) for w in states[key]}==states[key]
        assert rotate_edges(full_edges[key])==full_edges[key]
        remaining=set(full_edges[key]); oo=[]
        while remaining:
            seed=min(remaining)
            orbit=set().union(*(rotate_edges({seed},r) for r in range(5)))
            assert len(orbit)==5 and orbit<=remaining
            oo.append(orbit); remaining-=orbit
        assert len(oo)==3
        orbits[key]=oo

    details=[]
    for first,second in product(range(3),repeat=2):
        chosen={'00000:0':first,'00000:1':second}
        KK=dict(original_K)
        for key,n in chosen.items(): KK[key]=full_edges[key]-orbits[key][n]
        failures=[]; changed_witnesses=0; witnesses=[]; reselected=[]
        for d in parsed:
            TK={edge(restore(a,d['mapping']),restore(b,d['mapping'])) for a,b in KK[d['target']]}
            common=KK[d['source']]&TK
            if not common:
                failures.append({k:d[k] for k in ('source','position','new_excluded','target')})
            else:
                changed_witnesses+=d['old_witness'] not in common
                if d['old_witness'] not in common:
                    reselected.append({**{k:d[k] for k in ('source','position','new_excluded','target')},
                        'old_witness':[word_text(w) for w in d['old_witness']],
                        'new_witness':[word_text(w) for w in min(common)]})
                witnesses.append({**{k:d[k] for k in ('source','position','new_excluded','target')},
                                  'witness':[word_text(w) for w in min(common)]})
        details.append({'pool_orbits':[first,second],'all_313_common_K':not failures,
                        'failure_count':len(failures),'failures':failures,
                        'old_witnesses_needing_reselection':changed_witnesses,
                        'old_witnesses_reselected':reselected,
                        'witnesses':witnesses if not failures else []})

    # Constant-source target K is unchanged and must be checked independently.
    cd=[d for d in parsed if d['source'][:5]=='00000']
    assert len(cd)==30
    index={(d['source'],d['position'],d['new_excluded']):d for d in cd}
    TK_index={key:{edge(restore(a,d['mapping']),restore(b,d['mapping']))
                   for a,b in original_K[d['target']]} for key,d in index.items()}
    equivariance_failures=[]
    for key,TK in TK_index.items():
        source,pos,new=key
        for r in range(1,5):
            dest=(source,(pos-r)%5,new)
            moved=rotate_edges(TK,r)
            if moved!=TK_index[dest]:
                equivariance_failures.append({'source':source,'position':pos,
                    'new_excluded':new,'rotation':r,'new_position':dest[1],
                    'moved_target_K_edges':len(moved),'actual_target_K_edges':len(TK_index[dest]),
                    'symmetric_difference':len(moved^TK_index[dest]),
                    'first_moved_not_actual':[word_text(w) for w in min(moved-TK_index[dest])]})

    # Weaker bounded question: can one witness edge still transport around
    # each orbit even if the complete chosen target K family is not equivariant?
    orbit_witnesses=[]
    for key in ('00000:0','00000:1'):
        for new in (1,2,3):
            common_core=set(full_edges[key])
            for r in range(5):
                common_core &= rotate_edges(TK_index[(key,(-r)%5,new)],-r)
            orbit_witnesses.append({'source':key,'new_excluded':new,
                                   'full_C15_transportable_edges':len(common_core),
                                   'edges':[[word_text(w) for w in e] for e in sorted(common_core)]})
    for detail in details:
        first,second=detail['pool_orbits']; combo={'00000:0':first,'00000:1':second}
        six=[]
        for ow in orbit_witnesses:
            key=ow['source']; candidates={edge(word_tuple(a),word_tuple(b)) for a,b in ow['edges']}
            candidates -= orbits[key][combo[key]]
            six.append({'source':key,'new_excluded':ow['new_excluded'],
                        'transportable_protected_edges':len(candidates),
                        'witness':[word_text(w) for w in min(candidates)] if candidates else None})
        detail['six_orbit_witnesses']=six
        detail['one_witness_per_rotation_orbit']=all(d['witness'] for d in six)
        # Check each of the 30 transported witnesses against the actual
        # normalized target, without assuming target-family equivariance.
        transported=[]
        for d in six:
            if not d['witness']: continue
            key=d['source']; new=d['new_excluded']
            seed=edge(*(word_tuple(w) for w in d['witness']))
            protected=full_edges[key]-orbits[key][combo[key]]
            for r in range(5):
                moved=next(iter(rotate_edges({seed},r)))
                dest=(key,(-r)%5,new)
                assert moved in protected & TK_index[dest]
                transported.append({'source':key,'position':dest[1],
                    'new_excluded':new,'rotation':r,
                    'target':index[dest]['target'],
                    'witness':[word_text(w) for w in moved]})
        detail['transported_constant_interfaces']=transported
        detail['transported_constant_interface_count']=len(transported)

    result={'scope':'exact nine local pool redesigns; no manuscript edits or Hamilton searches',
        'input_sha256':hashlib.sha256(inp.read_bytes()).hexdigest(),
        'pool_orbits':{key:[[[word_text(w) for w in e] for e in sorted(orb)] for orb in oo]
                       for key,oo in orbits.items()},
        'candidate_results':details,
        'strict_target_K_equivariant':not equivariance_failures,
        'target_K_equivariance_failure_count':len(equivariance_failures),
        'first_target_K_equivariance_failure':equivariance_failures[0] if equivariance_failures else None,
        'constant_orbit_witness_cores':orbit_witnesses,
        'elapsed_seconds':time.perf_counter()-start}
    (HERE/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    summary={k:v for k,v in result.items() if k not in ('pool_orbits','candidate_results')}
    summary['candidate_results']=[{k:v for k,v in d.items() if k not in ('witnesses','six_orbit_witnesses','transported_constant_interfaces','old_witnesses_reselected')}
                                  for d in details]
    print(json.dumps(summary))


if __name__=='__main__': main()
