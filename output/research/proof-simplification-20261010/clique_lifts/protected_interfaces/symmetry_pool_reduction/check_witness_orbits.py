"""Weak witness transport under natural boundary actions; whole K need not be invariant."""
from pathlib import Path
from itertools import product,permutations
from collections import Counter
import hashlib,json,re,time
from base_check import STANDARD,HARD,edge,word_tuple,word_text,cycle_edges,transform,normalize,restore

HERE=Path(__file__).resolve().parent


def main():
    started=time.perf_counter()
    raw=(HERE/'literal-input.tex').read_bytes(); text=raw.decode()
    blocks=dict(re.findall(r'% BEGIN ([A-Z0-9-]+)\n(.*?)% END \1',text,re.S))
    def words(tag):return [word_tuple(w) for w in re.findall(r'\b[0-3]{5}\b',blocks[tag])]
    def edge_list(tag):return [edge(word_tuple(a),word_tuple(b)) for a,b in re.findall(r'\b([0-3]{5})-([0-3]{5})\b',blocks[tag])]
    def move(es,g):return {edge(transform(a,g),transform(b,g)) for a,b in es}
    def pull(es,g):return {edge(restore(a,g),restore(b,g)) for a,b in es}
    cc=words('FACTOR-00000'); states={}; support={}; pools={}
    for t in STANDARD:
        legal={w for w in product(range(4),repeat=5) if all(w[i]!=w[(i+1)%5] for i in range(5))
               and all(t[i]=='4' or w[i]!=int(t[i]) for i in range(5))}
        components=[set(cc[:15]),set(cc[15:])] if t=='00000' else [legal]
        for i,vs in enumerate(components):
            key=f'{t}:{i}';states[key]=vs;pools[key]=edge_list('POOL-'+t+'-'+str(i))
            if t=='00000':support[key]=cycle_edges(cc[15*i:15*(i+1)])
            elif t in HARD:support[key]=set(edge_list('COMMON-00001' if t=='00001' else 'PORTS-00112'))
            else:support[key]=cycle_edges(words(('FHC-' if '4' in t else 'C1-')+t))
    # Retain the already-verified constant pools (orbit indices 1,0).
    constant_pools={}
    for key,index in (('00000:0',1),('00000:1',0)):
        remaining=set(support[key]);oo=[]
        while remaining:
            seed=min(remaining);orb=set().union(*(move({seed},(r,1,(0,1,2,3))) for r in range(5)))
            assert len(orb)==5 and orb<=remaining;oo.append(orb);remaining-=orb
        constant_pools[key]=oo[index]
    records=re.findall(r'([0-4]{5}:[01])\s+([0-4])\s+([0-3])\s+([0-4]{5}:[01])\s+([0-3]{5})-([0-3]{5})',blocks['INTERFACES-ALL'])
    assert len(records)==313
    parsed=[];lookup={}
    for n,(source,ps,cs,target,a,b) in enumerate(records):
        pos,new=int(ps),int(cs);t=word_tuple(source[:5]);nt,g=normalize(t[:pos]+(new,)+t[pos+1:])
        assert nt==target[:5]
        physical=frozenset(restore(w,g) for w in states[target])
        d={'id':n,'source':source,'position':pos,'new_excluded':new,'target':target,'normalizer':g,
           'physical_target_states':physical,'old_witness':edge(word_tuple(a),word_tuple(b))}
        parsed.append(d);lookup[(source,pos,new,physical)]=n
    nonconstant=[d['id'] for d in parsed if not d['source'].startswith('00000:')]
    assert len(nonconstant)==283
    natural={}
    for source in {parsed[n]['source'] for n in nonconstant}:
        t=word_tuple(source[:5])
        natural[source]=[(s,eps,p) for s in range(5) for eps in (1,-1)
                         for p in permutations(range(4)) if transform(t,(s,eps,p))==t]
    maps={}
    for n in nonconstant:
        d=parsed[n];rows=[]
        for g in natural[d['source']]:
            s,eps,p=g;pos=(eps*(d['position']-s))%5;new=p[d['new_excluded']]
            physical=frozenset(transform(w,g) for w in d['physical_target_states'])
            dest=lookup[(d['source'],pos,new,physical)]
            rows.append((g,dest))
        maps[n]=rows
    unseen=set(nonconstant);orbits=[]
    while unseen:
        rep=min(unseen);orb={n for g,n in maps[rep]}
        assert orb<=unseen and all({n for g,n in maps[m]}==orb for m in orb)
        orbits.append((rep,sorted(orb)));unseen-=orb
    raw_target={d['id']:pull(support[d['target']],d['normalizer']) for d in parsed}
    raw_cores={}
    for rep,orb in orbits:
        d=parsed[rep];W=set(support[d['source']])
        for g,dest in maps[rep]:
            W &= pull(support[d['source']]&raw_target[dest],g)
        raw_cores[rep]=W
    variants=[]
    for name in ('existing-nonconstant-pools','nonconstant-four-two-pools'):
        PP={key:set(pool) for key,pool in pools.items()};PP.update(constant_pools)
        if name=='nonconstant-four-two-pools':
            for key,pool in pools.items():
                if key.startswith('00000:'):continue
                PP[key]=set(pool[-2:]) if key[:5] in HARD else {pool[0],pool[1],pool[-2],pool[-1]}
                assert PP[key]<=set(pool) and len(PP[key])==(2 if key[:5] in HARD else 4)
        KK={key:support[key]-PP[key] for key in support}
        targetK={d['id']:pull(KK[d['target']],d['normalizer']) for d in parsed}
        common={d['id']:KK[d['source']]&targetK[d['id']] for d in parsed}
        assert all(common.values()),'pool candidate loses a directed interface'
        families=[];saved=0;covered=0;fallback=[]
        for rep,orb in orbits:
            d=parsed[rep];W=set(support[d['source']])
            for g,dest in maps[rep]:W &= pull(common[dest],g)
            witnesses=[]
            if W:
                seed=min(W);by_dest={}
                for g,dest in maps[rep]:
                    moved=next(iter(move({seed},g)));assert moved in common[dest]
                    by_dest.setdefault(dest,(g,moved))
                assert set(by_dest)==set(orb)
                for dest,(g,e) in sorted(by_dest.items()):
                    witnesses.append({'id':dest,'action':g,'witness':[word_text(w) for w in e]})
                saved+=len(orb)-1;covered+=len(orb)
            else:fallback+=orb
            blockers=[]
            if not W and raw_cores[rep]:
                for seed in sorted(raw_cores[rep]):
                    failures=[]
                    for g,dest in maps[rep]:
                        moved=next(iter(move({seed},g)))
                        if moved in common[dest]:continue
                        dd=parsed[dest]; canonical=next(iter(move({moved},dd['normalizer'])))
                        reasons=[]
                        if moved in PP[dd['source']]:
                            fixed=set(pools[dd['source']][:2]) if dd['source'][:5] not in HARD else set()
                            reasons.append('source-fixed-seed-cut' if moved in fixed else 'source-reserve-pool')
                        if canonical in PP[dd['target']]:
                            fixed=set(pools[dd['target']][:2]) if dd['target'][:5] not in HARD else set()
                            reasons.append('target-fixed-seed-cut' if canonical in fixed else 'target-reserve-pool')
                        failures.append({'dest_id':dest,'action':g,'image_edge':[word_text(w) for w in moved],
                            'normalized_target_edge':[word_text(w) for w in canonical],'reasons':reasons})
                    blockers.append({'raw_seed':[word_text(w) for w in seed],'failures':failures})
            families.append({'representative':{k:d[k] for k in ('id','source','position','new_excluded','target')},
                'orbit_records':orb,'orbit_size':len(orb),'transport_core_size':len(W),
                'raw_transport_core_size':len(raw_cores[rep]),
                'raw_transport_core_edges':[[word_text(w) for w in e] for e in sorted(raw_cores[rep])],
                'raw_seed_pool_blockers':blockers,
                'transport_seed':[word_text(w) for w in min(W)] if W else None,
                'transported_witnesses':witnesses})
        count_bound=[]
        for n in nonconstant:
            d=parsed[n];R=support[d['source']]&pull(support[d['target']],d['normalizer'])
            bound=len(PP[d['source']])+len(PP[d['target']])
            count_bound.append({'id':n,'source':d['source'],'target':d['target'],
                                'raw_common_edges':len(R),'removed_pool_sum':bound,
                                'pigeonhole_guarantee':len(R)>bound})
        variants.append({'name':name,'all_313_common_K':True,
            'pool_sizes':{key:len(pool) for key,pool in PP.items()},
            'pool_edges':{key:[[word_text(w) for w in e] for e in sorted(pool)] for key,pool in PP.items()},
            'natural_interface_orbits':len(orbits),'families_with_transport_core':sum(bool(f['transport_core_size']) for f in families),
            'nonconstant_interfaces_covered_by_family':covered,'representative_records_saved':saved,
            'remaining_representative_records':283-saved,'fallback_record_ids':fallback,
            'families':families,'pigeonhole_guarantees':sum(d['pigeonhole_guarantee'] for d in count_bound),
            'raw_count_bounds':count_bound})
        printed=[]
        for f in families:
            if f['transport_seed']:
                printed.append({'kind':'transport-family','orbit_size':f['orbit_size'],
                    **f['representative'],'witness':f['transport_seed']})
            else:
                for n in f['orbit_records']:
                    printed.append({'kind':'individual','orbit_size':1,
                        **{k:parsed[n][k] for k in ('id','source','position','new_excluded','target')},
                        'witness':[word_text(w) for w in min(common[n])]})
        assert len(printed)==283-saved
        variants[-1]['printed_representatives']=sorted(printed,key=lambda d:d['id'])
        lines=['# Research print-compression candidate only; all family memberships remain finite checks.',
               '# kind orbit-size source position new-excluded target witness']
        for d in variants[-1]['printed_representatives']:
            lines.append(f"{d['kind']} {d['orbit_size']} {d['source']} {d['position']} {d['new_excluded']} {d['target']} {'--'.join(d['witness'])}")
        (HERE/(name+'-representatives.txt')).write_text('\n'.join(lines)+'\n')
        failed=[]
        for f in families:
            if f['transport_seed']:continue
            reason='full natural-group raw transport core is empty before pools' if not f['raw_transport_core_size'] else 'two raw transport seeds are blocked by protected-pool exclusions'
            for n in f['orbit_records']:
                d=parsed[n]
                failed.append({**{k:d[k] for k in ('id','source','position','new_excluded','target')},
                    'family_representative_id':f['representative']['id'],'family_size':f['orbit_size'],
                    'reason':reason,'raw_transport_core_size':f['raw_transport_core_size'],
                    'valid_individual_witness':[word_text(w) for w in min(common[n])]})
        assert len(failed)==37
        (HERE/(name+'-failed-interfaces.json')).write_text(json.dumps(failed,indent=2)+'\n')
    # Preserve the existing ordinary seed cuts in order, then retain exactly
    # two unused reserves. Hard common seed edges all survive in every row.
    lines=['% Candidate only. Constant pools, cycles, seed words and interface input are unchanged.']
    for key,pool in pools.items():
        if key.startswith('00000:'):continue
        ordered=pool[-2:] if key[:5] in HARD else [pool[0],pool[1],pool[-2],pool[-1]]
        lines.append('\\paragraph{Candidate pool for '+key+'.}')
        lines.append('\\[\\texttt{'+',\\ '.join('--'.join(word_text(w) for w in e) for e in ordered)+'}\\]')
    (HERE/'four-two-pools.tex').write_text('\n'.join(lines)+'\n')
    result={'scope':'283 fixed nonconstant-source interfaces, two fixed-pool versions, actual target-component actions',
        'input_sha256':hashlib.sha256(raw).hexdigest(),'variants':variants,
        'elapsed_seconds':time.perf_counter()-started}
    (HERE/'witness-orbit-results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'scope':result['scope'],'elapsed_seconds':result['elapsed_seconds'],
        'variants':[{k:v[k] for k in ('name','all_313_common_K','natural_interface_orbits','families_with_transport_core',
            'nonconstant_interfaces_covered_by_family','representative_records_saved','remaining_representative_records','pigeonhole_guarantees')} for v in variants]}))


if __name__=='__main__':main()
