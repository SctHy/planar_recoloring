"""Replay the symbolic rules on the bounded path232 kernel only."""
import itertools
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
P=range(4)
WORDS={
 (0,0,1):'120 123 323 313 213 210 230 130 132 232 212 312 310 320',
 (0,1,0):'101 121 321 323 123 103 303 302 301 201 203 202 102 132 232 231 131',
 (0,1,2):'131 101 103 203 303 301 201 231 230 130 120 123 323 320 321 121',
}
WORDS={t:tuple(tuple(map(int,x)) for x in w.split()) for t,w in WORDS.items()}

def edge(x,y): return tuple(sorted((x,y)))
def cycle_edges(w): return frozenset(edge(x,y) for x,y in zip(w,w[1:]+w[:1]))
def transformed(t,w,p,rev):
    t=tuple(p[c] for c in t)
    w=tuple(tuple(p[c] for c in x) for x in w)
    return (t[::-1],tuple(x[::-1] for x in w)) if rev else (t,w)
def kind(t): return 'A' if len(set(t))==3 else 'M' if t[0]==t[2] else 'E'
def canonical(t,rev=False):
    k=kind(t)
    if k=='E':
        a=t[1]; b=t[0] if t[0]!=a else t[2]; h=sorted(set(P)-{a,b})
        base=(0,0,1); p=(a,b,*h); rev=t[0]!=a
    elif k=='M':
        a=t[0]; b=t[1]; h=sorted(set(P)-{a,b})
        base=(0,1,0); p=(a,b,*h)
    else:
        base=(0,1,2); p=(*t,next(iter(set(P)-set(t)))); rev=False
    return transformed(base,WORDS[base],p,rev)[1]
def special(t):
    if kind(t)!='E': return frozenset()
    a=t[1]; b=t[0] if t[0]!=a else t[2]; result=set()
    for c in set(P)-{a,b}:
        q=[(u,c,w) for u,w in itertools.product(P,repeat=2)
           if u not in (a,c) and w not in (a,c)
           and u!=t[0] and w!=t[2]]
        assert len(q)==2
        result.add(edge(*q))
    return frozenset(result)
def pairs(text):
    return [edge(tuple(map(int,x)),tuple(map(int,y))) for x,y in (q.split('-') for q in text.split())]
def path_edges(text):
    w=[tuple(map(int,x)) for x in text.split()]
    return {edge(x,y) for x,y in zip(w,w[1:])}

def main():
    identity_specs={
      (0,0,1): ['210 213 313','310 312 212','320 120 123','230 130 132'],
      (0,1,0): ['102 202 203 201 301 302 303 103','121 321 323 123','131 231 232 132'],
      (0,1,2): ['101 103 203 303 301 201','121 321 320 323 123 120','130 230 231'],
    }
    for t,paths in identity_specs.items():
        internal={e for e in cycle_edges(WORDS[t])-special(t) if e[0][1]==e[1][1]}
        assert internal==set().union(*(path_edges(w) for w in paths))
    rules=[
      ('E-E/end',(0,0,1),(0,0,2),0,0,'210-213 120-123'),
      ('E-E/middle',(0,0,1),(0,1,1),0,0,'120-320 120-123'),
      ('E-M/orientation0',(0,0,1),(1,0,1),0,0,'210-213 310-312'),
      ('E-M/orientation1',(0,0,1),(1,0,1),0,1,'212-312 213-313'),
      ('E-A/middle',(0,0,1),(0,2,1),0,0,'210-213 213-313'),
      ('E-A/end',(0,0,1),(2,0,1),0,0,'310-312 320-120'),
      ('M-A/orientation0',(0,1,0),(2,1,0),0,0,'301-302 302-303'),
      ('M-A/orientation1',(0,1,0),(2,1,0),1,0,'121-123 321-323'),
      ('A-A/end',(0,1,2),(0,1,3),0,0,'320-321 230-231'),
      ('A-A/middle',(0,1,2),(0,3,2),0,0,'101-103 103-203'),
    ]
    full_cycles={}
    for t,w in WORDS.items():
        for p in itertools.permutations(P):
            for rev in (False,True):
                tt,ww=transformed(t,w,p,rev)
                full_cycles.setdefault(tt,set()).add(cycle_edges(ww))
    full_pairs=set()
    for t,cc in full_cycles.items():
        for s,dd in full_cycles.items():
            if t>=s or sum(x!=y for x,y in zip(t,s))!=1: continue
            for ce in cc:
                for de in dd:
                    full_pairs.add(frozenset(((t,ce),(s,de))))
    coverage=set(); checks=0
    for family,t,s,srev,trev,ee in rules:
        sw=canonical(t,bool(srev)); tw=canonical(s,bool(trev)); witness=pairs(ee)
        assert len(set(witness))==2
        for p in itertools.permutations(P):
            for rev in (False,True):
                tt,ww=transformed(t,sw,p,rev); ss,vv=transformed(s,tw,p,rev)
                ce=cycle_edges(ww); de=cycle_edges(vv)
                transformed_witness=[]
                for e in witness:
                    _,ew=transformed(t,e,p,rev)
                    transformed_witness.append(edge(*ew))
                assert all(e in ce-special(tt) and e in de-special(ss) for e in transformed_witness),family
                assert all(e[0][1]==e[1][1] for e in transformed_witness)
                coverage.add(frozenset(((tt,ce),(ss,de))))
                checks+=1
    square_checks=0
    for sr,tr in itertools.product((False,True),repeat=2):
        t=(0,1,0); s=(0,2,0); sw=canonical(t,sr); tw=canonical(s,tr)
        for p in itertools.permutations(P):
            for rev in (False,True):
                tt,ww=transformed(t,sw,p,rev); ss,vv=transformed(s,tw,p,rev)
                ce=cycle_edges(ww); de=cycle_edges(vv); middle=p[3]
                common={e for e in ce&de if e[0][1]==e[1][1]==middle}
                assert len(common)>=2
                assert len({e for e in ce if e[0][1]==e[1][1]==middle})==3
                assert len({e for e in de if e[0][1]==e[1][1]==middle})==3
                coverage.add(frozenset(((tt,ce),(ss,de))))
                square_checks+=1
    assert coverage==full_pairs
    result={'evidence_level':'bounded-check','internal_path_identities':3,
            'symbolic_two_edge_rule_rows':len(rules),'symbolic_rule_transform_checks':checks,
            'M_M_square_intersection_transform_checks':square_checks,
            'allowed_cycles':sum(map(len,full_cycles.values())),
            'all_adjacent_cycle_pairs':len(full_pairs),'pairs_covered_by_nine_families':len(coverage),
            'uncovered_pairs':0,'failures':0,
            'limitations':'Only the fixed four-colour path232 kernel is replayed. Arbitrary original-graph order and run length remain justified by the manuscript induction and strip construction.'}
    (ROOT/'analytic-family-results-v1.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
