"""Replay all interface memberships for two one-edge K patches.

Also propagate only necessary no-isolate/maximum-degree-two constraints in
the new-row H40 forest. This is not a seed or Hamilton search.
"""
from pathlib import Path
from itertools import product, combinations
from collections import Counter
import hashlib, json, re
import check_interface_feasibility_v1 as m
import check_redesign_degree_v1 as degree_screen

HERE = Path(__file__).resolve().parent
PATCHES = [('13120', '23120'), ('21320', '31320')]
REMOVED = ('12313', '12323')
BAD = set(map(m.word_tuple, degree_screen.BAD))

def propagate(vertices, raw, forced):
    available, required = set(raw), set(forced)
    rounds = 0
    while True:
        rounds += 1
        forced_deg = Counter(v for e in required for v in e)
        avail_deg = Counter(v for e in available for v in e)
        if any(forced_deg[v] > 2 or avail_deg[v] < 1 for v in vertices):
            return {'pass': False, 'reason': 'forced degree>2 or isolated available vertex', 'rounds': rounds}
        strings = {tuple(m.word_text(v) for v in e) for e in required}
        if not degree_screen.valid_forest(strings):
            return {'pass': False, 'reason': 'forced cycle', 'rounds': rounds}
        next_available = {e for e in available if e in required or
                          all(forced_deg[v] < 2 for v in e)}
        next_required = required | {e for e in next_available if
                                   any(sum(v in f for f in next_available) == 1 for v in e)}
        if next_available == available and next_required == required:
            return {'pass': True, 'rounds': rounds,
                    'forced_edge_count': len(required), 'available_edge_count': len(available),
                    'forced_edges': sorted([m.word_text(u), m.word_text(v)] for u, v in required),
                    'available_degree_distribution': dict(sorted(Counter(sum(v in e for e in available) for v in vertices).items()))}
        available, required = next_available, next_required

def main():
    inp = HERE/'interface-literal-input-v1.tex'
    text = inp.read_text()
    blocks = dict(re.findall(r'% BEGIN ([A-Z0-9-]+)\n(.*?)% END \1', text, re.S))
    def words(name): return [m.word_tuple(w) for w in re.findall(r'\b[0-3]{5}\b', blocks[name])]
    def edges(name): return {m.edge(m.word_tuple(u), m.word_tuple(v)) for u,v in re.findall(r'([0-3]{5})-([0-3]{5})', blocks[name])}
    def cycle_edges(ws): return {m.edge(a,b) for a,b in zip(ws,ws[1:]+ws[:1])}
    constants=words('FACTOR-00000'); K={}; raw_hard=None; hard_vertices=None
    for t in m.STANDARD:
        vs={x for x in product(range(4),repeat=5)
            if all(x[i]!=x[(i+1)%5] and (t[i]=='4' or x[i]!=int(t[i])) for i in range(5))}
        components=[set(constants[:15]),set(constants[15:])] if t=='00000' else [vs]
        for i,component in enumerate(components):
            if t=='00000': ports=cycle_edges(constants[i*15:(i+1)*15])
            elif t in ('00001','00112'): ports=edges('COMMON-00001' if t=='00001' else 'PORTS-00112')
            else: ports=cycle_edges(words(('FHC-' if '4' in t else 'C1-')+t))
            K[f'{t}:{i}']=ports-edges(f'POOL-{t}-{i}')
        if t=='00001':
            hard_vertices=vs
            raw_hard={m.edge(a,b) for a,b in combinations(vs,2) if sum(x!=y for x,y in zip(a,b))==1}
    assert len(K)==23 and len(K['00001:0'])==12
    rows=re.findall(r'([0-4]{5}:[01])\s+([0-4])\s+([0-3])\s+([0-4]{5}:[01])\s+([0-3]{5})-([0-3]{5})',blocks['INTERFACES-ALL'])
    assert len(rows)==283
    seeds={(0,1):('23121','23123'),(0,2):('31231','31232'),(0,3):('21231','23231'),
           (1,1):('21213','23213'),(1,2):('31321','32321'),(1,3):('21321','21323')}
    core=hard_vertices-BAD; H={e for e in raw_hard if set(e)<=core}
    reserves=sorted(e for e in edges('POOL-00001-0') if not set(e)&BAD)
    reports=[]
    for patch in PATCHES:
        new_K={k:set(es) for k,es in K.items()}
        new_K['00001:0'].remove(m.edge(*map(m.word_tuple,REMOVED)))
        new_K['00001:0'].add(m.edge(*map(m.word_tuple,patch)))
        assert len(new_K['00001:0'])==12
        changed=[]
        for source,pos,new,target,u,v in rows:
            pos,new=int(pos),int(new); t=m.word_tuple(source[:5]); nt,g=m.normalize(t[:pos]+(new,)+t[pos+1:]); assert nt==target[:5]
            target_edges={m.edge(m.restore(a,g),m.restore(b,g)) for a,b in new_K[target]}
            common=new_K[source]&target_edges
            assert common, (patch,source,pos,new,target)
            witness=m.edge(m.word_tuple(u),m.word_tuple(v))
            if witness not in common:
                changed.append({'source':source,'position':pos,'new_excluded':new,'target':target,
                                'old_witness':[u,v], 'replacement':[m.word_text(w) for w in min(common)],
                                'common_K_count':len(common)})
        family_count=0
        for i in range(2):
            for color in (1,2,3):
                for pos in range(5):
                    actual=m.edge(*(tuple(m.word_tuple(w)[(k-pos)%5] for k in range(5)) for w in seeds[i,color]))
                    _,g=m.normalize(tuple(color if k==pos else 0 for k in range(5)))
                    target_edges={m.edge(m.restore(a,g),m.restore(b,g)) for a,b in new_K['00001:0']}
                    assert actual in new_K[f'00000:{i}']&target_edges
                    family_count+=1
        pool_screens=[]
        for R in combinations(reserves,2):
            required=new_K['00001:0']|set(R)
            assert not set(R)&new_K['00001:0']
            result=propagate(core,H,required)
            pool_screens.append({'two_reserves':[[m.word_text(v) for v in e] for e in R], **result})
        reports.append({'added_K_edge':patch,'patched_K':sorted([m.word_text(v) for v in e] for e in new_K['00001:0']),
                        'K_size':12,'all_283_individual_interfaces_have_common_K':True,
                        'all_30_constant_family_images_keep_original_witness':True,
                        'changed_individual_witness_count':len(changed),'changed_individual_witnesses':changed,
                        'two_old_reserve_necessary_forests':pool_screens,
                        'necessary_forest_propagation_pass_count':sum(p['pass'] for p in pool_screens)})
    result={'patches':reports, 'input_sha256':hashlib.sha256(inp.read_bytes()).hexdigest(),
            'no_seed_or_Hamilton_search':True,
            'limitations':['All interface membership is verified, but new protected PC2/PC3 seeds are not constructed.',
                           'Degree propagation is necessary only and does not prove a spanning linear forest with a compatible endpoint matching.']}
    (HERE/'K-patch-results-v1.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'patches':[{'added_K_edge':p['added_K_edge'],'changed_witnesses':p['changed_individual_witnesses'],
                                  'necessary_forest_passes':p['necessary_forest_propagation_pass_count']} for p in reports]}))

if __name__=='__main__': main()
