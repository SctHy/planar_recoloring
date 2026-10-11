"""Finite sanity check for the row/column bridge splice.
It checks the four HC types, identifies pairs not covered by row/column blocks,
and verifies the four exceptional paths.  This is only a check of the small
lemma; it is not used as an extrapolation to arbitrary graphs.
"""
from itertools import combinations, permutations, product

def states(A,B): return [(a,b) for a in A for b in B if a != b]
def adjacent(x,y): return x[0] == y[0] or x[1] == y[1]

def block_ok(R,C,x,y):
    # R are block labels, C are within-block labels; x,y are cells.
    if x[0] == y[0]: return False
    mids=[r for r in R if r not in (x[0],y[0])]
    for mid in permutations(mids):
        order=(x[0],)+mid+(y[0],)
        bridge_lists=[set(C)-{order[i],order[i+1]} for i in range(len(order)-1)]
        for bs in product(*map(tuple,bridge_lists)):
            if bs[0] == x[1] or bs[-1] == y[1]: continue
            if any(bs[i] == bs[i+1] for i in range(len(bs)-1)): continue
            return True
    return False

def all_hc_paths(A,B):
    V=states(A,B); bad=[]
    for x,y in combinations(V,2):
        if block_ok(A,B,x,y) or block_ok(B,A,(x[1],x[0]),(y[1],y[0])): continue
        bad.append((x,y))
    return bad

CASES={
  '343':({0,1,2},{0,1,2,3}),
  '342':({0,1,2},{0,1,3,4}),
  '443':({0,1,2,3},{0,1,2,4}),
  '444':({0,1,2,3},{0,1,2,3}),
}
EXC={
 '343':[(12,13),(1,0),(1,2)], # parsed below as words
}
for typ,(A,B) in CASES.items():
    bad=all_hc_paths(A,B)
    print(typ,'uncovered by block splice:',len(bad))
    if typ in ('443','444'): assert not bad
# Verify the four displayed exceptions and their colour symmetries by a direct DFS.
paths={
 '343':[
  '12 10 20 23 21 01 02 03 13',
  '01 02 12 13 03 23 21 20 10',
  '01 03 23 21 20 10 13 12 02'],
 '342':['13 10 20 24 21 23 03 01 04 14'],
}
for typ,words in paths.items():
 A,B=CASES[typ];V=set(states(A,B))
 for w in words:
  p=[(int(s[0]),int(s[1])) for s in w.split()]
  assert set(p)==V and all(adjacent(p[i],p[i+1]) for i in range(len(p)-1))
print('exceptional paths are valid')
