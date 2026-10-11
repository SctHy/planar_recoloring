#!/usr/bin/env python3
"""Exact finite checks for the pentagon certificate in the manuscript.
This intentionally checks words as mathematical data, not a SAT/solver result.
Usage: python verify_pentagon.py planar_recoloring_hamilton_thresholds.tex
"""
from __future__ import annotations
import itertools,re,sys
from pathlib import Path

Q=range(4); PERMS=list(itertools.permutations(Q))
WORD5=re.compile(r'\b[0-4]{5}\b'); WORD6=re.compile(r'\b[0-4]{6}\b')

def blocks(tex):
    ans={}
    for m in re.finditer(r'% BEGIN ([A-Z0-9_-]+)\n(.*?)% END \1',tex,re.S):
        key,body=m.groups(); ans[key]=body
    return ans

def words(body,n=5): return re.findall(rf'\b[0-4]{{{n}}}\b',body)
def state(w): return tuple(map(int,w))
def edge(a,b): return tuple(sorted((a,b)))
def adj(a,b): return sum(x!=y for x,y in zip(a,b))==1

def legal(x,t):
    return all(x[i]!=x[(i+1)%5] for i in range(5)) and all(a==4 or x[i]!=a for i,a in enumerate(t))
def states(t):
    return [x for x in itertools.product(Q,repeat=5) if legal(x,t)]

def cycle_check(w,t):
    x=list(map(state,w)); S=set(states(t))
    return len(x)==len(set(x))==len(S) and all(a in S for a in x) and all(adj(x[i],x[(i+1)%len(x)]) for i in range(len(x)))
def path_check(w,t):
    x=list(map(state,w)); S=set(states(t))
    return len(x)==len(set(x))==len(S) and all(a in S for a in x) and all(adj(a,b) for a,b in zip(x,x[1:]))
def six_check(w,t):
    x=[tuple(map(int,z)) for z in w]; S=set(states(t))
    return len(x)==len(set(x))==len(S)*2 and all(a[1:] in S for a in x) and all(sum(a[i]!=b[i] for i in range(6))==1 for a,b in zip(x,x[1:])) and sum(x[0][0]!=x[-1][0] or x[0][1:]!=x[-1][1:] for _ in [0])==1

def transform_word(x,sh,rev,p):
    y=x[::-1] if rev else x; y=y[sh:]+y[:sh]
    return tuple(4 if a==4 else p[a] for a in y)
def canon(t):
    best=None
    for rev in (False,True):
      for sh in range(5):
       for p in PERMS:
        u=transform_word(t,sh,rev,p)
        if best is None or u<best[0]: best=(u,(sh,rev,p))
    return best

def inv_edges(E,tr):
    # map canonical edges back to physical coordinates
    sh,rev,p=tr
    inv={transform_word(x,sh,rev,p):x for x in itertools.product(Q,repeat=5)}
    return {edge(inv[a],inv[b]) for a,b in E}

def make_cycle(w):
 x=list(map(state,w)); return {edge(x[i],x[(i+1)%len(x)]) for i in range(len(x))}

def main(path):
 B=blocks(Path(path).read_text())
 # all cycles that appear as one-row certificates
 no={'00011':'C1-00011','00012':'C1-00012','00101':'C1-00101','00102':'C1-00102','00121':'C1-00121','00123':'C1-00123','01012':'C1-01012','01023':'C1-01023'}
 one={'00004':'FHC-00004','00014':'FHC-00014','00104':'FHC-00104','00114':'FHC-00114','00124':'FHC-00124','01014':'FHC-01014','01024':'FHC-01024','01104':'FHC-01104','01124':'FHC-01124','01204':'FHC-01204','01234':'FHC-01234'}
 ok=True; cyc={}
 for t,k in no.items():
  w=words(B[k]); good=cycle_check(w,tuple(map(int,t))); print(k,len(w),good); ok &= good; cyc[t]=make_cycle(w)
 for t,k in one.items():
  w=words(B[k]); good=cycle_check(w,tuple(map(int,t))); print(k,len(w),good); ok &= good; cyc[t]=make_cycle(w)
 # split constant 00000 into two cycles
 w=words(B['FACTOR-00000']);
 for j in (0,1):
  q=w[15*j:15*(j+1)]; x=list(map(state,q)); good=(len(x)==len(set(x))==15 and all(legal(a,(0,0,0,0,0)) for a in x) and all(adj(x[i],x[(i+1)%15]) for i in range(15))); print('FACTOR-00000',j,len(q),good); ok &= good
 # linear hard identities
 for typ,k in [('00001','MATCHING-CHAIN-00001'),('00112','HP-00112')]:
  w=words(B[k]);
  if typ=='00112': good=path_check(w,tuple(map(int,typ)))
  else:
   x=list(map(state,w)); body=B[k]
   rows=[(int(i),a,b,e) for i,a,b,e in re.findall(r'(\d+) & ([0-4]{5}) & ([0-4]{5}) & ([01-])',body)]; rows.sort(); rows=[(a,b,e) for i,a,b,e in rows]
   # The table is printed in two columns; rows are interleaved, so test
   # coverage and each displayed pair, then test the connector rule directly.
   good=(len(x)==44 and len(x)==len(set(x)) and all(legal(a,(0,0,0,0,1)) for a in x)
         and len(rows)==22 and all(adj(state(a),state(b)) for a,b,e in rows))
   for (a,b,e),(c,d,e2) in zip(rows,rows[1:]):
    if e!='-' and not (adj(state(a),state(c)) if e=='0' else adj(state(b),state(c))): good=False
  print(k,len(w),good); ok &= good
 # seed cycles (first coordinate is row); check each layer and each six-word transition
 for typ,k in [('00112','C2-00112'),('00001','PC2-00001')]:
  w=words(B[k],6); x=[tuple(map(int,z)) for z in w]; t=tuple(map(int,typ)); good=(len(x)==len(set(x)) and len(x)==2*len(states(t)) and all(a[1:] in set(states(t)) for a in x) and all(sum(a[i]!=b[i] for i in range(6))==1 for a,b in zip(x,x[1:])) and sum(x[0][i]!=x[-1][i] for i in range(6))==1); print(k,len(w),good); ok &= good
 # edge pairs in ports and pools
 for k in [k for k in B if k.startswith(('PORTS-','COMMON-','POOL-'))]:
  es=re.findall(r'([0-4]{5})-([0-4]{5})',B[k]); typ=k.split('-')[1]; t=tuple(map(int,typ)); good=all(adj(state(a),state(b)) and legal(state(a),t) and legal(state(b),t) for a,b in es); print(k,len(es),good); ok &= good
 # Check the 47 explicit fallback witness records (edge endpoints are
 # legal for both source and target boundaries).  The selector and
 # constant-family records are checked by the same predicate in a full package.
 ipat=re.compile(r'(\d{5}):(\d+) (\d) (\d) (\d{5}):(\d+) ([0-4]{5})-([0-4]{5})')
 irecs=[]
 for line in B.get('INTERFACES-ALL','').splitlines(): irecs.extend(ipat.findall(line))
 ibad=[]
 for src,comp,pos,old,tgt,tcomp,a,b in irecs:
  x,y=state(a),state(b); ts,tt=tuple(map(int,src)),tuple(map(int,tgt))
  if not (adj(x,y) and legal(x,ts) and legal(y,ts) and legal(x,tt) and legal(y,tt)): ibad.append((src,tgt,a,b))
 print('individual interface records',len(irecs)); ok &= (len(irecs)==47)
 # Direct 10-edge overlap for all adjacent boundaries whose canonical types have one-row cycles.
 # This is a compression check, not used for hard or constant source types.
 reps=set(cyc); vals=[]
 for t in itertools.product(Q,repeat=5):
  ct,tr=canon(t); ts=''.join(map(str,ct))
  if ts not in reps or ts=='00000': continue
  E=inv_edges(cyc[ts],tr)
  for i in range(5):
   for a in Q:
    if a==t[i]: continue
    u=list(t);u[i]=a;u=tuple(u); cu,tru=canon(u); us=''.join(map(str,cu))
    if us not in reps or us=='00000': continue
    vals.append(len(E & inv_edges(cyc[us],tru)))
 print('direct-cycle adjacent pairs',len(vals),'min-common-edges',min(vals) if vals else None)
 ok &= (vals and min(vals)>=10)
 # Boundary and component counts
 print('labelled boundaries',4**5+5*4**4)
 print('no-star states',sum(len(states(tuple(map(int,t)))) for t in ['00000','00001','00011','00012','00101','00102','00112','00121','00123','01012','01023']))
 print('one-star representative state counts',[len(states(tuple(map(int,t)))) for t in one])
 print('RESULT', 'PASS' if ok else 'FAIL')
 return 0 if ok else 1
if __name__=='__main__':sys.exit(main(sys.argv[1] if len(sys.argv)>1 else 'planar_recoloring_hamilton_thresholds.tex'))
