"""Exact membership and endpoint-matching necessary screens; no seed search."""
from pathlib import Path
from itertools import combinations,product
from collections import Counter
import hashlib,json,re
import check_interface_feasibility_v1 as m
import check_K_patch_v1 as forest

HERE=Path(__file__).resolve().parent
BAD=set(map(m.word_tuple,m.BAD_VERTICES))
FIRST_REMOVE=m.edge(*map(m.word_tuple,('12313','12323')))
SECOND_REMOVALS=[('13210','23210'),('13230','13232'),('13230','23230')]
ADDITIONS=[('13120','23120'),('21320','31320')]

def main():
    inp=HERE/'interface-literal-input-v1.tex';text=inp.read_text()
    blocks=dict(re.findall(r'% BEGIN ([A-Z0-9-]+)\n(.*?)% END \1',text,re.S))
    def words(n):return [m.word_tuple(w) for w in re.findall(r'\b[0-3]{5}\b',blocks[n])]
    def edges(n):return {m.edge(m.word_tuple(a),m.word_tuple(b)) for a,b in re.findall(r'([0-3]{5})-([0-3]{5})',blocks[n])}
    def cycle(ws):return {m.edge(a,b) for a,b in zip(ws,ws[1:]+ws[:1])}
    K={};constant=words('FACTOR-00000');V=None
    for t in m.STANDARD:
        vs={w for w in product(range(4),repeat=5) if all(w[i]!=w[(i+1)%5] and (t[i]=='4' or w[i]!=int(t[i])) for i in range(5))}
        if t=='00001':V=vs
        for i in range(2 if t=='00000' else 1):
            if t=='00000':ports=cycle(constant[15*i:15*(i+1)])
            elif t in ('00001','00112'):ports=edges('COMMON-00001' if t=='00001' else 'PORTS-00112')
            else:ports=cycle(words(('FHC-' if '4' in t else 'C1-')+t))
            K[f'{t}:{i}']=ports-edges(f'POOL-{t}-{i}')
    H={m.edge(a,b) for a,b in combinations(V-BAD,2) if sum(x!=y for x,y in zip(a,b))==1}
    reserves=sorted(e for e in edges('POOL-00001-0') if not set(e)&BAD)
    records=re.findall(r'([0-4]{5}:[01])\s+([0-4])\s+([0-3])\s+([0-4]{5}:[01])\s+([0-3]{5})-([0-3]{5})',blocks['INTERFACES-ALL']);assert len(records)==283
    seeds={(0,1):('23121','23123'),(0,2):('31231','31232'),(0,3):('21231','23231'),
           (1,1):('21213','23213'),(1,2):('31321','32321'),(1,3):('21321','21323')}
    reports=[]
    for second in SECOND_REMOVALS:
        for add in ADDITIONS:
            KK={k:set(es) for k,es in K.items()}
            KK['00001:0']-= {FIRST_REMOVE,m.edge(*map(m.word_tuple,second))}
            KK['00001:0'].add(m.edge(*map(m.word_tuple,add)))
            lost=[];empty=[]
            for source,pos,new,target,a,b in records:
                pos,new=int(pos),int(new);t=m.word_tuple(source[:5]);nt,g=m.normalize(t[:pos]+(new,)+t[pos+1:]);assert nt==target[:5]
                targetK={m.edge(m.restore(u,g),m.restore(v,g)) for u,v in KK[target]}
                common=KK[source]&targetK;old=m.edge(m.word_tuple(a),m.word_tuple(b))
                if not common:empty.append({'source':source,'position':pos,'new_excluded':new,'target':target})
                if old not in common:lost.append({'source':source,'position':pos,'new_excluded':new,'target':target,
                                                'replacement':None if not common else [m.word_text(v) for v in min(common)],
                                                'common_count':len(common)})
            family_pass=True
            for i in range(2):
                for color in (1,2,3):
                    for pos in range(5):
                        actual=m.edge(*(tuple(m.word_tuple(w)[(k-pos)%5] for k in range(5)) for w in seeds[i,color]))
                        _,g=m.normalize(tuple(color if k==pos else 0 for k in range(5)))
                        targetK={m.edge(m.restore(u,g),m.restore(v,g)) for u,v in KK['00001:0']}
                        family_pass &= actual in KK[f'00000:{i}']&targetK
            pools=[]
            if not empty and family_pass:
                for R in combinations(reserves,2):
                    D=KK['00001:0']|set(R);screen=forest.propagate(V-BAD,H,D)
                    if not screen['pass']:
                        pools.append({'reserves':[[m.word_text(v) for v in e] for e in R],**screen});continue
                    F={m.edge(*map(m.word_tuple,e)) for e in screen['forced_edges']}
                    fdeg=Counter(v for e in F for v in e)
                    available={e for e in H if e in F or all(fdeg[v]<2 for v in e)}
                    adeg=Counter(v for e in available for v in e)
                    forced_ends={v for v in V-BAD if adeg[v]==1}
                    possible_cuts={e for e in H-D if all(fdeg[v]<=1 for v in e)}
                    bad_ends={v for v in forced_ends if not any(v in e for e in possible_cuts)}
                    pools.append({'reserves':[[m.word_text(v) for v in e] for e in R],
                                  'min1_max2_forest_screen':screen,
                                  'forced_endpoint_states':sorted(map(m.word_text,forced_ends)),
                                  'possible_matching_cut_count':len(possible_cuts),
                                  'forced_endpoints_without_matching_neighbour':sorted(map(m.word_text,bad_ends)),
                                  'necessary_endpoint_matching_pass':not bad_ends})
            reports.append({'second_removed_K_edge':second,'added_K_edge':add,'K11':sorted([m.word_text(v) for v in e] for e in KK['00001:0']),
                            'individual_empty_interfaces':empty,'changed_old_witness_records':lost,
                            'all30_constant_images_keep_old_witness':family_pass,'reserve_pair_screens':pools,
                            'necessary_endpoint_matching_pass_count':sum(p.get('necessary_endpoint_matching_pass',False) for p in pools)})
    result={'reports':reports,'no_Hamilton_or_seed_search':True,
            'scope':'After the proven second endpoint obstruction: only interface membership and min1/max2/possible matching-neighbour necessary tests.',
            'input_sha256':hashlib.sha256(inp.read_bytes()).hexdigest()}
    (HERE/'second-K-patch-results-v1.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps([{'remove':r['second_removed_K_edge'],'add':r['added_K_edge'],'empty':r['individual_empty_interfaces'],
                      'families':r['all30_constant_images_keep_old_witness'],'endpoint_matching_passes':r['necessary_endpoint_matching_pass_count']} for r in reports]))

if __name__=='__main__':main()
