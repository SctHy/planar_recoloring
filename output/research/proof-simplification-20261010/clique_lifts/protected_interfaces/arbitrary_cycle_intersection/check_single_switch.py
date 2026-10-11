"""Bounded two-opt neighbourhood of two fixed cycles in one fixed interface."""
from pathlib import Path
from itertools import product
import re,json,hashlib
import base_check as H

HERE=Path(__file__).resolve().parent


def main():
    text=(HERE/'literal-input.tex').read_text()
    blocks=dict(re.findall(r'% BEGIN ([A-Z0-9-]+)\n(.*?)% END \1',text,re.S))
    records=re.findall(r'([0-4]{5}:[01])\s+([0-4])\s+([0-3])\s+([0-4]{5}:[01])\s+([0-3]{5})-([0-3]{5})',blocks['INTERFACES-ALL'])
    source,pos,new,target,_,_=records[76]
    assert (source,pos,new,target)==('00101:0','0','1','00101:0')
    oldt=H.word_tuple(source[:5]);changed=(1,)+oldt[1:]
    nt,g=H.normalize(changed);assert nt==target[:5]
    ca=[H.word_tuple(w) for w in re.findall(r'\b[0-3]{5}\b',blocks['C1-00101'])]
    cb=[H.restore(w,g) for w in ca]
    def states(t):
        return {w for w in product(range(4),repeat=5)
            if all(w[i]!=w[(i+1)%5] and w[i]!=t[i] for i in range(5))}
    vs=[states(oldt),states(changed)]
    def legal(a,b):return sum(x!=y for x,y in zip(a,b))==1
    def validate(cycle,side):
        assert len(cycle)==len(set(cycle))==len(vs[side]) and set(cycle)==vs[side]
        assert all(legal(a,b) for a,b in H.cycle_edges(cycle))
    validate(ca,0);validate(cb,1)
    old_common=H.cycle_edges(ca)&H.cycle_edges(cb);assert len(old_common)==9
    answer=None;pair_checks=0;valid_switches=0
    for side,(cycle,other) in enumerate(((ca,cb),(cb,ca))):
        eo=H.cycle_edges(other)
        for i in range(len(cycle)):
            for j in range(i+2,len(cycle)):
                if i==0 and j==len(cycle)-1:continue
                pair_checks+=1
                a,b=cycle[i],cycle[(i+1)%len(cycle)]
                c,d=cycle[j],cycle[(j+1)%len(cycle)]
                if not legal(a,c) or not legal(b,d):continue
                alternate=cycle[:i+1]+cycle[i+1:j+1][::-1]+cycle[j+1:]
                validate(alternate,side);valid_switches+=1
                new_common=H.cycle_edges(alternate)&eo
                if len(new_common)<9:
                    encode=lambda e:[H.word_text(w) for w in e]
                    answer={'switched_side':'source' if side==0 else 'target',
                        'cut_indices':[i,j],'removed_edges':[encode(e) for e in sorted({H.edge(a,b),H.edge(c,d)})],
                        'added_edges':[encode(e) for e in sorted({H.edge(a,c),H.edge(b,d)})],
                        'new_common_edges':[encode(e) for e in sorted(new_common)],
                        'new_common_count':len(new_common),
                        'alternate_cycle':[H.word_text(w) for w in alternate],
                        'unchanged_cycle':[H.word_text(w) for w in other]}
                    break
            if answer:break
        if answer:break
    result={'status':'COUNTEREXAMPLE' if answer else 'NO_SINGLE_SWITCH_COUNTEREXAMPLE',
        'interface_record':76,'source':source,'target':target,'old_boundary':H.word_text(oldt),
        'actual_target_boundary':H.word_text(changed),
        'normalization':{'shift':g[0],'orientation':g[1],'permutation':g[2]},
        'cycle_orders':[len(ca),len(cb)],'old_common_count':9,
        'pair_checks':pair_checks,'valid_switches':valid_switches,'answer':answer,
        'input_sha256':hashlib.sha256((HERE/'literal-input.tex').read_bytes()).hexdigest(),
        'scope':'One fixed interface, single-switch neighbourhood of two fixed Hamilton cycles. No arbitrary Hamilton search or full interface replay.'}
    (HERE/'switch-results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='answer'}))
    if answer:print(json.dumps({k:v for k,v in answer.items() if k not in ('alternate_cycle','unchanged_cycle')}))


if __name__=='__main__':main()
