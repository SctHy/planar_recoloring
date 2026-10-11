"""Verify the finite graph inputs of the all-t endpoint obstruction, no search."""
from pathlib import Path
from itertools import product,combinations
import re,json,hashlib

HERE=Path(__file__).resolve().parent


def main():
    text=(HERE/'interface-literal-input-v1.tex').read_text()
    blocks=dict(re.findall(r'% BEGIN ([A-Z0-9-]+)\n(.*?)% END \1',text,re.S))
    claim=json.loads((HERE/'K-patch-results-v1.json').read_text())
    edge=lambda u,v:tuple(sorted((u,v)))
    states={''.join(map(str,w)) for w in product(range(4),repeat=5)
        if all(w[i]!=w[(i+1)%5] and w[i]!=(0,0,0,0,1)[i] for i in range(5))}
    edges={edge(u,v) for u,v in combinations(states,2) if sum(a!=b for a,b in zip(u,v))==1}
    adj={u:{v for e in edges if u in e for v in e if v!=u} for u in states}
    eps=lambda a,b:1 if (int(b)-int(a))%3==1 else -1
    chi=lambda w:eps(w[0],w[1])*eps(w[2],w[3])*(1 if w[4]=='0' else -1)
    X={u for u in states if chi(u)==1};Y=states-X
    YY={e for e in edges if set(e)<=Y};XX={e for e in edges if set(e)<=X}
    assert len(states)==44 and len(edges)==74 and len(X)==20 and len(Y)==24
    assert not XX and YY=={edge('12312','12313'),edge('13212','13213')}
    assert adj['13210']=={'13212','13213','13230','23210'}
    triple={edge('13210','23210'),edge('13230','13232'),edge('13230','23230')}
    oldD={edge(u,v) for u,v in re.findall(r'([0-3]{5})-([0-3]{5})',blocks['COMMON-00001'])}
    pool={edge(u,v) for u,v in re.findall(r'([0-3]{5})-([0-3]{5})',blocks['POOL-00001-0'])}
    oldK=oldD-pool;assert len(oldK)==12 and triple<=oldK
    for p in claim['patches']:
        K={edge(*e) for e in p['patched_K']};assert len(K)==12 and triple<=K
    result={'status':'PASS','graph_states':44,'graph_edges':74,'small_independent_class':20,'large_class':24,
        'only_large_internal_edges':[list(e) for e in sorted(YY)],
        'full_neighbourhood_13210':sorted(adj['13210']),
        'three_edges_protected_in_both_patches':[list(e) for e in sorted(triple)],
        'obstruction':'Degree balance forces both YYedges in M and L, with their fourvertices endpoints. The two protected edges at13230 saturate it inL. All neighbours of13210 except23210 are saturated inL, so protected13210-23210 is its only Ledge and13210 must be an Mendpoint. M cannot useBBvertices alreadymatched, nonendpoint13230, or protectededge13210-23210: contradiction.',
        'scope':'For every PC2seed and every number ofcrossmatchingcuts, the stated matching/linear-forest single-row insertion cannot preserve these threeedges. Droppingone isnecessary, not sufficient.',
        'input_sha256':hashlib.sha256((HERE/'interface-literal-input-v1.tex').read_bytes()).hexdigest(),
        'patch_claim_sha256':hashlib.sha256((HERE/'K-patch-results-v1.json').read_bytes()).hexdigest(),
        'no_seed_forest_or_Hamilton_search':True}
    (HERE/'review-results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__=='__main__':main()
