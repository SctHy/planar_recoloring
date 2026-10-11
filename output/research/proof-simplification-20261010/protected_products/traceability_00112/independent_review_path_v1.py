"""Independent direct generation; checks the frozen review without rewriting it."""
from pathlib import Path
from itertools import product
import hashlib,json

HERE=Path(__file__).resolve().parent

def main():
    p=HERE/'path-results.json';r=json.loads(p.read_text());words=r['path'];t='00112'
    states={''.join(map(str,x)) for x in product(range(4),repeat=5)
            if all(x[i]!=x[(i+1)%5] and str(x[i])!=t[i] for i in range(5))}
    assert len(words)==51 and len(set(words))==51 and set(words)==states
    steps=[]
    for a,b in zip(words,words[1:]):
        changed=[i for i in range(5) if a[i]!=b[i]]
        assert len(changed)==1
        steps.append({'from':a,'to':b,'changed_coordinate':changed[0]})
    out={'path_artifact_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
         'independent_enumeration':'all 4^5 words, proper C5, excluding boundary at every position',
         'state_count':len(states),'path_states':len(words),'all_states_once':True,
         'all_50_edges_legal':True,'steps':steps}
    assert out==json.loads((HERE/'independent-path-review.json').read_text())
    print('PASS: 51 states once, all 50 literal edges legal, frozen independent review reproduces')

if __name__=='__main__':main()
