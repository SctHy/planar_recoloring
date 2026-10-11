"""Mechanical sanity check for the three structural layer splices.
It only checks the displayed local identities; the proof is the layer-splice
argument in replacement.tex, not this script.
"""
from itertools import product

def adj(x,y):
    # x,y are strings uvw; one coordinate changes
    return sum(a!=b for a,b in zip(x,y))==1

def check(c,t):
    assert len(c)==len(set(c))
    assert all(adj(a,b) for a,b in zip(c,c[1:]+c[:1]))
    V={''.join(map(str,v)) for v in product(range(4),repeat=3)
       if v[0]!=v[1] and v[1]!=v[2] and all(v[i]!=t[i] for i in range(3))}
    assert set(c)==V,(len(c),len(V),V-set(c))

DE='323 123 120 320 310 312 212 232 132 130 230 210 213 313'.split()
DM='103 303 302 301 201 203 202 102 132 232 231 131 101 121 321 323 123'.split()
DA='120 123 323 320 321 121 131 101 103 203 303 301 201 231 230 130'.split()
for c,t in [(DE,(0,0,1)),(DM,(0,1,0)),(DA,(0,1,2))]: check(c,t)
print('all structural cycles pass')
