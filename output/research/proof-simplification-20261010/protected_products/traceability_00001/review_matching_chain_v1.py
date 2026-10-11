"""Independent literal TeX parsing of the 22-pair quotient-chain certificate."""
from pathlib import Path
from itertools import product
from collections import Counter
import hashlib,json,re

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parents[1]/'tree_gluing'/'constant_pool_review'

def main():
    tex=HERE/'matching-chain-source-v1.tex'
    js=HERE/'matching-chain-source-v1.json'
    rows=re.findall(r'^([0-9]+) & ([0-3]{5}) & ([0-3]{5}) & (0|1|--) ',tex.read_text(),re.M)
    assert len(rows)==22 and [int(r[0]) for r in rows]==list(range(1,23))
    pairs=[(r[1],r[2]) for r in rows]
    bits=[int(r[3]) for r in rows[:-1]]
    assert rows[-1][3]=='--'
    reference=json.loads(js.read_text())
    assert pairs==list(map(tuple,reference['pairs'])) and bits==reference['outgoing_endpoint']
    states={''.join(map(str,x)) for x in product(range(4),repeat=5)
            if all(x[i]!=x[(i+1)%5] and str(x[i])!='00001'[i] for i in range(5))}
    words=[w for pair in pairs for w in pair]
    assert len(states)==44 and len(words)==44 and len(set(words))==44 and set(words)==states
    def legal(a,b):return a in states and b in states and sum(x!=y for x,y in zip(a,b))==1
    assert all(legal(a,b) for a,b in pairs)
    joins=[(pairs[i][bits[i]],pairs[i+1][0]) for i in range(21)]
    assert all(legal(a,b) for a,b in joins)
    assert [tuple(sorted(e)) for e in joins]==list(map(tuple,reference['actual_joins']))
    block={w:i for i,pair in enumerate(pairs) for w in pair}
    assert all(block[a]==i and block[b]==i+1 for i,(a,b) in enumerate(joins))
    load=Counter(w for e in joins for w in e)
    assert max(load.values())==2
    distribution=Counter(load[w] for w in states)
    result={'boundary':'00001','literal_tex_sha256':hashlib.sha256(tex.read_bytes()).hexdigest(),
            'literal_json_sha256':hashlib.sha256(js.read_bytes()).hexdigest(),
            'direct_state_generation':True,'22_pairs_legal_and_cover_44_states_once':True,
            '21_bits_match_literal_json':True,'21_connectors_are_legal_actual_edges':True,
            'contracted_connector_graph_is_the_ordered_22_vertex_path':True,
            'maximum_physical_vertex_connector_load':max(load.values()),
            'connector_load_distribution':{str(k):v for k,v in sorted(distribution.items())},
            'load_two_vertices':sorted(w for w in states if load[w]==2),
            'pairs':pairs,'bits':bits,'actual_directed_connectors':joins,
            'conclusion':'PASS: ordered matching blocks support alternating two-reserve product gluing',
            'does_not_assert_original_graph_traceable':True}
    (HERE/'independent-matching-chain-review-v1.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('pairs','bits','actual_directed_connectors')}))

if __name__=='__main__':main()
