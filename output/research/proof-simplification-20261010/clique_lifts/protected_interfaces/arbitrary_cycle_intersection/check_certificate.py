"""Independent reader of the returned single-switch cycles; no helper import."""
from pathlib import Path
from itertools import product
import re,json,hashlib

HERE=Path(__file__).resolve().parent


def main():
    data=json.loads((HERE/'switch-results.json').read_text());a=data['answer']
    text=(HERE/'literal-input.tex').read_text()
    blocks=dict(re.findall(r'% BEGIN ([A-Z0-9-]+)\n(.*?)% END \1',text,re.S))
    source_old=re.findall(r'\b[0-3]{5}\b',blocks['C1-00101'])
    edge=lambda u,v:tuple(sorted((u,v)))
    edges=lambda words:{edge(u,v) for u,v in zip(words,words[1:]+words[:1])}
    def states(boundary):
        return {''.join(map(str,w)) for w in product(range(4),repeat=5)
            if all(w[i]!=w[(i+1)%5] and w[i]!=int(boundary[i]) for i in range(5))}
    def legal(cycle,boundary):
        assert len(cycle)==len(set(cycle))==64 and set(cycle)==states(boundary)
        assert all(sum(x!=y for x,y in zip(u,v))==1 for u,v in edges(cycle))
    alternate,target=a['alternate_cycle'],a['unchanged_cycle']
    legal(source_old,'00101');legal(alternate,'00101');legal(target,'10101')
    p='1023'
    assert target==[''.join(p[int(w[(-i)%5])] for i in range(5)) for w in source_old]
    i,j=a['cut_indices'];assert (i,j)==(2,52)
    assert alternate==source_old[:i+1]+source_old[i+1:j+1][::-1]+source_old[j+1:]
    removed=edges(source_old)-edges(alternate);added=edges(alternate)-edges(source_old)
    assert removed=={edge('31020','32020'),edge('31030','32030')}
    assert added=={edge('31020','31030'),edge('32020','32030')}
    old_common=edges(source_old)&edges(target);new_common=edges(alternate)&edges(target)
    assert len(old_common)==9 and len(new_common)==8
    source_pool={edge(u,v) for u,v in re.findall(r'([0-3]{5})-([0-3]{5})',blocks['POOL-00101-0'])}
    assert len(source_pool)==8 and source_pool<=edges(source_old) and source_pool<=edges(alternate)
    result={'status':'PASS','both_alternate_source_and_unchanged_target_Hamilton_cycles':True,
        'source_boundary':'00101','actual_target_boundary':'10101','states_each':64,
        'old_raw_common_edges':9,'new_raw_common_edges':8,
        'all8_old_source_pool_edges_retained':True,
        'reversed_inclusive_old_cycle_indices':[i+1,j],
        'removed_edges':[list(e) for e in sorted(removed)],'added_edges':[list(e) for e in sorted(added)],
        'new_common_edges':[list(e) for e in sorted(new_common)],
        'input_sha256':hashlib.sha256((HERE/'literal-input.tex').read_bytes()).hexdigest(),
        'discovery_sha256':hashlib.sha256((HERE/'switch-results.json').read_bytes()).hexdigest(),
        'scope':'One explicit counterexample to a cycle-choice-independent nine-edge raw-intersection lower bound. No claim of failure of any protected intersection.'}
    (HERE/'certificate-review.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__=='__main__':main()
