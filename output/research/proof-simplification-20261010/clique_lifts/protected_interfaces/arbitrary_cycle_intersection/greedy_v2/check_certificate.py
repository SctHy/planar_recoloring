"""Independently replay the three recorded switches, with no discovery routine."""
from pathlib import Path
from itertools import product,combinations
import json,re,hashlib

HERE=Path(__file__).resolve().parent


def main():
    result=json.loads((HERE/'greedy-results.json').read_text())
    v1=json.loads((HERE/'switch-results.json').read_text())
    cycles=[v1['answer']['alternate_cycle'],v1['answer']['unchanged_cycle']]
    text=(HERE/'literal-input.tex').read_text()
    blocks=dict(re.findall(r'% BEGIN ([A-Z0-9-]+)\n(.*?)% END \1',text,re.S))
    edge=lambda u,v:tuple(sorted((u,v)))
    edges=lambda c:{edge(u,v) for u,v in zip(c,c[1:]+c[:1])}
    pool0={edge(u,v) for u,v in re.findall(r'([0-3]{5})-([0-3]{5})',blocks['POOL-00101-0'])}
    restore=lambda w:''.join('1023'[int(w[(-i)%5])] for i in range(5))
    pools=[pool0,{edge(restore(u),restore(v)) for u,v in pool0}]
    def validate(c,side):
        boundary=('00101','10101')[side]
        vs={''.join(map(str,w)) for w in product(range(4),repeat=5)
            if all(w[i]!=w[(i+1)%5] and w[i]!=int(boundary[i]) for i in range(5))}
        assert len(c)==len(set(c))==64 and set(c)==vs
        assert all(sum(a!=b for a,b in zip(u,v))==1 for u,v in edges(c))
        assert len(pools[side])==8 and pools[side]<=edges(c)
    for side,c in enumerate(cycles):validate(c,side)
    counts=[len(edges(cycles[0])&edges(cycles[1]))]
    for step in result['accepted_steps']:
        side=step['side'];c=cycles[side];i,j=step['cut_indices']
        after=c[:i+1]+c[i+1:j+1][::-1]+c[j+1:]
        assert {edge(*e) for e in step['removed_edges']}==edges(c)-edges(after)
        assert {edge(*e) for e in step['added_edges']}==edges(after)-edges(c)
        validate(after,side);cycles[side]=after
        counts.append(len(edges(cycles[0])&edges(cycles[1])))
        assert (counts[-2],counts[-1])==(step['raw_before'],step['raw_after'])
        assert counts[-1]<counts[-2]
    assert cycles==result['cycles'] and counts==[8,6,5,3]
    common=edges(cycles[0])&edges(cycles[1]);K=(edges(cycles[0])-pools[0])&(edges(cycles[1])-pools[1])
    assert common=={edge('21010','31010'),edge('21020','23020'),edge('21210','21213')}
    assert K=={edge('21020','23020'),edge('21210','21213')}
    out={'status':'PASS','raw_counts':counts,'all_three_switches_replayed':True,
        'both_final_cycles_Hamilton':True,'all8_pool_edges_retained_eachside':True,
        'final_common_K_count':2,'zero_common_K_not_found':True,
        'result_sha256':hashlib.sha256((HERE/'greedy-results.json').read_bytes()).hexdigest(),
        'scope':'Independent certificate replay. Stopping at a single-switch local minimum does not prove a global minimum.'}
    (HERE/'certificate-review.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out))


if __name__=='__main__':main()
