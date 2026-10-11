"""Hypothetical K deletion and maximal-admissible interface checks; no seed search."""
from pathlib import Path
from itertools import permutations,product
import hashlib,json,re

HERE=Path(__file__).resolve().parent
STANDARD=('00000','00001','00011','00012','00101','00102','00112','00121',
          '00123','01012','01023','00004','00014','00104','00114','00124',
          '01014','01024','01104','01124','01204','01234')
PERMS=tuple(permutations(range(4)))
REMOVED=('12313','12323')
BAD_VERTICES={'12312','12313','13212','13213'}

def edge(a,b):return tuple(sorted((a,b)))
def word_tuple(w):return tuple(map(int,w))
def word_text(w):return ''.join(map(str,w))

def normalize(t):
    for s in range(5):
        for eps in (1,-1):
            for p in PERMS:
                transformed=tuple(4 if t[(s+eps*i)%5]==4 else p[t[(s+eps*i)%5]] for i in range(5))
                n=word_text(transformed)
                if n in STANDARD:return n,(s,eps,p)
    raise AssertionError(t)

def restore(w,g):
    s,eps,p=g;inverse=tuple(p.index(i) for i in range(4));out=[None]*5
    for i in range(5):out[(s+eps*i)%5]=inverse[w[i]]
    return tuple(out)

def main():
    inp=HERE/'interface-literal-input-v1.tex';text=inp.read_text()
    blocks=dict(re.findall(r'% BEGIN ([A-Z0-9-]+)\n(.*?)% END \1',text,re.S))
    def words(name):return [word_tuple(w) for w in re.findall(r'\b[0-3]{5}\b',blocks[name])]
    def edges(name):return {edge(word_tuple(a),word_tuple(b)) for a,b in re.findall(r'([0-3]{5})-([0-3]{5})',blocks[name])}
    def cycle_edges(words):return {edge(a,b) for a,b in zip(words,words[1:]+words[:1])}
    states={};raw={};K={}
    constants=words('FACTOR-00000');assert len(constants)==30
    for t in STANDARD:
        vs={x for x in product(range(4),repeat=5)
            if all(x[i]!=x[(i+1)%5] and (t[i]=='4' or x[i]!=int(t[i])) for i in range(5))}
        components=[set(constants[:15]),set(constants[15:])] if t=='00000' else [vs]
        for index,component in enumerate(components):
            key=f'{t}:{index}';states[key]=component
            raw[key]={edge(a,b) for a in component for b in component
                      if sum(x!=y for x,y in zip(a,b))==1}
            if t=='00000':ports=cycle_edges(constants[index*15:(index+1)*15])
            elif t in ('00001','00112'):ports=edges('COMMON-00001' if t=='00001' else 'PORTS-00112')
            else:ports=cycle_edges(words(('FHC-' if '4' in t else 'C1-')+t))
            K[key]=ports-edges(f'POOL-{t}-{index}')
            assert K[key]<=raw[key]
    assert len(K)==23 and len(K['00001:0'])==12 and len(K['00112:0'])==11
    removed=edge(*map(word_tuple,REMOVED));assert removed in K['00001:0']
    reduced={k:set(v) for k,v in K.items()};reduced['00001:0'].remove(removed)
    admissible={k:set(v) for k,v in K.items()}
    blocked=set(map(word_tuple,BAD_VERTICES))
    admissible['00001:0']={e for e in raw['00001:0'] if not set(e)&blocked}
    assert len(admissible['00001:0'])==64 and reduced['00001:0']<=admissible['00001:0']
    records=re.findall(r'([0-4]{5}:[01])\s+([0-4])\s+([0-3])\s+([0-4]{5}:[01])\s+([0-3]{5})-([0-3]{5})',blocks['INTERFACES-ALL'])
    assert len(records)==283
    details=[]
    for source,pos_s,new_s,target,a,b in records:
        pos,new=int(pos_s),int(new_s);t=word_tuple(source[:5]);changed=t[:pos]+(new,)+t[pos+1:]
        nt,g=normalize(changed);assert nt==target[:5]
        old_target={edge(restore(x,g),restore(y,g)) for x,y in K[target]}
        new_target={edge(restore(x,g),restore(y,g)) for x,y in reduced[target]}
        max_target={edge(restore(x,g),restore(y,g)) for x,y in admissible[target]}
        witness=edge(word_tuple(a),word_tuple(b));old_common=K[source]&old_target
        assert witness in old_common
        common=reduced[source]&new_target;maximum=admissible[source]&max_target
        changed_source=source=='00001:0';changed_target=target=='00001:0'
        if not (changed_source or changed_target):assert common==old_common
        details.append({'source':source,'position':pos,'new_excluded':new,'target':target,
                        'normalizer':{'shift':g[0],'orientation':g[1],'permutation':g[2]},
                        'old_witness':[a,b],'old_common_K_count':len(old_common),
                        'reduced_common_K_count':len(common),'old_witness_survives':witness in common,
                        'maximal_admissible_common_count':len(maximum),
                        'source_modified':changed_source,'target_modified':changed_target,
                        'replacement_witness':None if not common else [word_text(v) for v in min(common)],
                        'maximal_admissible_example':None if not maximum else [word_text(v) for v in min(maximum)]})
    critical=[('31212','31232'),('12132','32132'),('21313','21323'),('13123','23123')]
    assert all(edge(*map(word_tuple,e)) in reduced['00001:0'] for e in critical)
    seeds={(0,1):('23121','23123'),(0,2):('31231','31232'),(0,3):('21231','23231'),
           (1,1):('21213','23213'),(1,2):('31321','32321'),(1,3):('21321','21323')}
    families=[]
    for i in range(2):
        for color in (1,2,3):
            base=list(map(word_tuple,seeds[i,color]))
            for position in range(5):
                actual=edge(*(tuple(w[(k-position)%5] for k in range(5)) for w in base))
                t=tuple(color if k==position else 0 for k in range(5));nt,g=normalize(t)
                assert nt=='00001'
                target={edge(restore(a,g),restore(b,g)) for a,b in reduced['00001:0']}
                assert actual in K[f'00000:{i}']&target
                families.append({'component':i,'new_excluded':color,'position':position,
                                 'witness':[word_text(v) for v in actual],'survives':True})
    lost=[d for d in details if not d['old_witness_survives']]
    empty=[d for d in details if d['reduced_common_K_count']==0]
    impossible=[d for d in details if d['maximal_admissible_common_count']==0]
    output={'hypothetical_removed_K_edge':REMOVED,'old_K_count':12,'candidate_reduced_K_count':11,
            'maximal_admissible_raw_edges':64,'blocked_new_row_endpoint_states':sorted(BAD_VERTICES),
            'individual_records':len(details),'constant_family_case_images':len(families),
            'four_critical_target_edges_survive':critical,'six_constant_families_all_survive':True,
            'lost_old_witness_count':len(lost),'lost_old_witness_records':lost,
            'reduced_K_empty_interface_count':len(empty),'reduced_K_empty_interfaces':empty,
            'maximal_admissible_empty_interface_count':len(impossible),'maximal_admissible_empty_interfaces':impossible,
            'details':details,'constant_family_images':families,
            'source_input_sha256':hashlib.sha256(inp.read_bytes()).hexdigest(),
            'scope':'hypothetical local membership only; no table changes, no seed construction/search'}
    (HERE/'interface-feasibility-results-v1.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k not in ('details','constant_family_images')}))

if __name__=='__main__':main()
