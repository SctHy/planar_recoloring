"""Verify the seven short cycle certificates used in pair_cycles.tex.
This is a finite certificate check, not the proof of the all-order theorem.
"""
from itertools import permutations, combinations

CASES = {
    "331": ({0,1,2},{0,3,4}, "03 04 14 10 20 24 23 13"),
    "332": ({0,1,2},{0,1,3}, "23 03 01 21 20 10 13"),
    "333": ({0,1,2},{0,1,2}, "10 20 21 01 02 12"),
    "342": ({0,1,2},{0,1,3,4}, "24 04 01 03 13 14 10 20 21 23"),
    "343": ({0,1,2},{0,1,2,3}, "12 10 20 21 01 02 03 23 13"),
    "443": ({0,1,2,3},{0,1,2,4}, "32 12 10 20 21 01 02 04 24 14 34 31 30"),
    "444": ({0,1,2,3},{0,1,2,3}, "23 21 20 10 12 02 32 30 31 01 03 13"),
}

def vertices(A,B): return {(a,b) for a in A for b in B if a != b}
def edge(x,y): return x[0] == y[0] or x[1] == y[1]
def ek(x,y): return tuple(sorted((x,y)))
def parse(s): return [(int(w[0]),int(w[1])) for w in s.split()]

def colour_autos(A,B, include_swap=False):
    I=A&B; out=[]
    for pa in permutations(A):
        ma=dict(zip(sorted(A),pa))
        if {ma[x] for x in I} != I: continue
        for pb in permutations(B):
            mb=dict(zip(sorted(B),pb))
            if {mb[x] for x in I} != I: continue
            if any(ma[x] != mb[x] for x in I): continue
            out.append(lambda x,ma=ma,mb=mb:(ma[x[0]],mb[x[1]]))
    if include_swap:
        # only the (3,3,2) representative needs the side exchange:
        # sigma swaps the two non-common colours 2 and 3.
        sig={0:0,1:1,2:3,3:2}
        for ma in [sig]:
            out.append(lambda x,ma=ma:(ma[x[1]],ma[x[0]]))
    return out

for typ,(A,B,w) in CASES.items():
    V=vertices(A,B); C=parse(w)
    assert len(C)==len(V) and set(C)==V, (typ,len(C),len(V),set(C)^V)
    assert all(edge(C[i],C[(i+1)%len(C)]) for i in range(len(C)))
    all_edges={ek(x,y) for x,y in combinations(sorted(V),2) if edge(x,y)}
    autos=colour_autos(A,B,typ=="332")
    base={ek(C[i],C[(i+1)%len(C)]) for i in range(len(C))}
    orbit=set()
    for f in autos: orbit |= {ek(f(x),f(y)) for x,y in base}
    assert orbit == all_edges, (typ,len(orbit),len(all_edges),all_edges-orbit)
    print(typ, "|V|",len(V), "|E|",len(all_edges), "|Gamma|",len(autos), "edge orbit",len(orbit))

# Interface-neighbour check.  A list transition is one of the allowed moves.
U=set(range(5))
Ls=[set(c) for r in (3,4) for c in combinations(sorted(U),r)]
def F(A,B): return vertices(A,B)
for A in Ls:
  for B in Ls:
    S=F(A,B)
    # unchanged; one list replaced by another 3-list with symmetric diff 2;
    # or swap a 3-list and a containing 4-list.
    for Ap in Ls:
      for Bp in Ls:
        ok = (A==Ap and B==Bp)
        ok |= (A==Ap and len(B)==len(Bp)==3 and len(B^Bp)==2)
        ok |= (B==Bp and len(A)==len(Ap)==3 and len(A^Ap)==2)
        ok |= (len(A)==len(Bp)==3 and len(B)==len(Ap)==4 and A <= B and Bp <= Ap and A==Bp and B==Ap)
        ok |= (len(A)==len(Bp)==4 and len(B)==len(Ap)==3 and B <= A and Ap <= Bp and A==Bp and B==Ap)
        if not ok: continue
        J=S & F(Ap,Bp)
        if len(J)<4: raise AssertionError((A,B,Ap,Bp,len(J)))
        for p in S:
          assert any(q in J and q != p and edge(p,q) for q in S), (A,B,Ap,Bp,p,J)
print("all allowed interfaces have a common adjacent state")
