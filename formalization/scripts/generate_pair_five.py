#!/usr/bin/env python3
from itertools import combinations, permutations
import re,json, pathlib
root=pathlib.Path(__file__).resolve().parents[2]
text=(root/'supplement/article_certificates.tex').read_text()
TYPES=("331","332","333","342","343","443","444")
# extract cycles
block=re.search(r'% BEGIN PAIR-CYCLES(.*?)% END PAIR-CYCLES',text,re.S).group(1)
cycles={}
for line in block.splitlines():
    m=re.search(r'(?m)(331|332|333|342|343|443|444)\s*&\s*([0-4]+)/([0-4]+)\s*&\s*(.*?)(?:\\\\)?$',line)
    if not m: continue
    typ,a,b,body=m.groups()
    words=body.strip().rstrip('\\').split()
    cycles[typ]=(a,b,words)
# endpoints
endpoint_rows=re.findall(r'For \$(\d{3})\$:.*?\\begin\{verbatim\}\n(.*?)\\end\{verbatim\}',text,re.S)
endwords={typ:[line.split() for line in body.strip().splitlines() if line.strip()] for typ,body in endpoint_rows}
print({k:len(v) for k,v in endwords.items()})

def adj(x,y): return (x[0]==y[0] and x[1]!=y[1]) or (x[0]!=y[0] and x[1]==y[1])
def enc(w): return int(w[0])*5+int(w[1])
def decode(i): return f'{i//5}{i%5}'
def verts(a,b): return sorted(enc(str(x)+str(y)) for x in sorted(set(a)) for y in sorted(set(b)) if x!=y)
def autos(a,b):
    a=set(a); b=set(b); out=[]
    for im in permutations('01234'):
        p=dict(zip('01234',im)); pa={p[x] for x in a};pb={p[x] for x in b}
        if pa==a and pb==b:
            out.append((p,False))
        if pa==b and pb==a:
            out.append((p,True))
    return out

def transword(word,p,sw):
    def f(w):
        return (p[w[1]]+p[w[0]]) if sw else (p[w[0]]+p[w[1]])
    return [enc(f(w)) for w in word]

def feasible(v):
    # return all ordered feasible endpoints and witness paths via DP, canonical graph
    n=len(v); idx={s:i for i,s in enumerate(v)}
    nei=[[] for _ in v]
    for i,x in enumerate(v):
        for j,y in enumerate(v):
            if adj(decode(x),decode(y)): nei[i].append(j)
    out={}
    for st in range(n):
        dp={(1<<st,st):[v[st]]}
        # simple iterative masks
        for mask in range(1<<n):
            for at in range(n):
                p=dp.get((mask,at))
                if p is None: continue
                for nx in nei[at]:
                    if not(mask>>nx&1):
                        key=(mask|1<<nx,nx)
                        if key not in dp: dp[key]=p+[v[nx]]
        full=(1<<n)-1
        for en in range(n):
            if en!=st and (full,en) in dp:
                out[(v[st],v[en])]=dp[(full,en)]
    return out
# canonical edge cycle table using transformations and rotations
def cycle_for_edges(typ):
    a,b,w=cycles[typ]; v=verts(a,b); result={}
    for p,sw in autos(a,b):
        q=transword(w,p,sw)
        # oriented cyclic sequence; add both directions via reverse later
        for ori in (q,list(reversed(q))):
            n=len(ori)
            for i,s in enumerate(ori):
                t=ori[(i+1)%n]
                rot=ori[i:]+ori[:i]
                result.setdefault((s,t),rot)
    # all edges should present both orientation
    expected={(x,y) for x in v for y in v if x!=y and adj(decode(x),decode(y))}
    assert set(result)==expected,(typ,len(result),len(expected),expected-set(result))
    return result
# representative canonical map data
rep={}
for typ in TYPES:
    a,b,w=cycles[typ];
    ep=feasible(verts(a,b))
    # ensure paths from words cover all exact endpoints after autos
    paths={}
    for word in endwords[typ]:
        for p,sw in autos(a,b):
            q=transword(word,p,sw); paths.setdefault((q[0],q[-1]),q)
            qr=list(reversed(q)); paths.setdefault((qr[0],qr[-1]),qr)
    assert set(paths)==set(ep), (typ,len(paths),len(ep),set(ep)-set(paths))
    rep[typ]={'a':a,'b':b,'cycle_edges':cycle_for_edges(typ),'paths':paths,'verts':verts(a,b)}
    print(typ, len(rep[typ]['verts']), len(rep[typ]['cycle_edges']),len(paths))
# normalize valid masks
small=[]
for m in range(32):
    ls=''.join(str(i) for i in range(5) if m>>i&1)
    if len(ls) in (3,4): small.append((m,ls))

def norm_for(m,n):
    A=''.join(str(i) for i in range(5) if m>>i&1);B=''.join(str(i) for i in range(5) if n>>i&1)
    if len(A) not in (3,4) or len(B) not in (3,4): return (0,False,list(range(5)),list(range(5)))
    x,y=(A,B) if len(A)<=len(B) else (B,A)
    typ=f'{len(x)}{len(y)}{len(set(x)&set(y))}'
    assert typ in TYPES,(m,n,A,B,typ)
    ra,rb,_=cycles[typ]
    # choose swap based on sizes; try false then true
    for sw in (False,True):
        ta,tb=(A,B) if not sw else (B,A)
        for im in permutations('01234'):
            p=dict(zip('01234',im))
            pa={p[c] for c in ra};pb={p[c] for c in rb}
            if pa==set(ta) and pb==set(tb):
                inv=[im.index(str(i)) for i in range(5)]
                # p is complete tuple im where im[j]=p(j)
                kind=TYPES.index(typ)
                return kind,sw,[int(z) for z in im],inv
    raise AssertionError((A,B,typ))
normal={}
for m,A in small:
    for n,B in small:
        normal[(m,n)]=norm_for(m,n)
assert len(normal)==225
# output JSON concise numeric records for generator
out={'types':list(TYPES),'cycles':{t:{'a':rep[t]['a'],'b':rep[t]['b'], 'edge':{f'{s},{u}':p for (s,u),p in rep[t]['cycle_edges'].items()}} for t in TYPES},
     'paths':{t:{f'{s},{u}':p for (s,u),p in rep[t]['paths'].items()} for t in TYPES},
     'normal':{f'{m},{n}':{'kind':k,'swap':sw,'p':p,'q':q} for (m,n),(k,sw,p,q) in normal.items()}}
out_path = root / 'formalization' / 'pair_five' / 'pair_five_data.json'
out_path.write_text(json.dumps(out, separators=(',', ':')))
print(f'wrote {out_path} ({out_path.stat().st_size} bytes)')
