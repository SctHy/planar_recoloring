"""Independent literal reconstruction; no candidate checker imports or searches."""
from pathlib import Path
from itertools import product, permutations
import hashlib, json, re

HERE = Path(__file__).resolve().parent
INPUT = HERE.parents[1] / 'clique_lifts/protected_interfaces/constant_orbit_pools/literal-input.tex'
STANDARD = ('00000', '00001', '00011', '00012', '00101', '00102',
            '00112', '00121', '00123', '01012', '01023', '00004',
            '00014', '00104', '00114', '00124', '01014', '01024',
            '01104', '01124', '01204', '01234')
PERMS = tuple(permutations('0123'))

def edge(a,b): return tuple(sorted((a,b)))
def cyc(ws): return {edge(ws[i-1],ws[i]) for i in range(len(ws))}
def rotate(w,r): return ''.join(w[(i+r)%5] for i in range(5))
def rot_edges(es,r): return {edge(rotate(a,r),rotate(b,r)) for a,b in es}
def forward(w,s,eps,p):
    return ''.join('4' if w[(s+eps*i)%5]=='4' else p[int(w[(s+eps*i)%5])] for i in range(5))
def back(w,s,eps,p):
    out=['?']*5
    for i,c in enumerate(w): out[(s+eps*i)%5]=str(p.index(c))
    return ''.join(out)
def normal(t):
    for s in range(5):
        for eps in (1,-1):
            for p in PERMS:
                v=forward(t,s,eps,p)
                if v in STANDARD: return v,(s,eps,p)
    raise AssertionError(t)
def restore_edges(es,g): return {edge(back(a,*g),back(b,*g)) for a,b in es}

def main():
    txt=INPUT.read_text()
    blocks=dict(re.findall(r'% BEGIN ([A-Z0-9-]+)\n(.*?)% END \1',txt,re.S))
    def words(name): return re.findall(r'\b[0-3]{5}\b',blocks[name])
    def edges(name): return {edge(a,b) for a,b in re.findall(r'\b([0-3]{5})-([0-3]{5})\b',blocks[name])}
    states={}; full={}; oldK={}
    cw=words('FACTOR-00000')
    for t in STANDARD:
        legal={''.join(w) for w in product('0123',repeat=5)
               if all(w[i]!=w[(i+1)%5] for i in range(5))
               and all(t[i]=='4' or w[i]!=t[i] for i in range(5))}
        comps=[set(cw[:15]),set(cw[15:])] if t=='00000' else [legal]
        assert set.union(*comps)==legal
        for i,vs in enumerate(comps):
            key=t+':'+str(i); states[key]=vs
            if t=='00000': es=cyc(cw[15*i:15*(i+1)])
            elif t in ('00001','00112'): es=edges('COMMON-00001' if t=='00001' else 'PORTS-00112')
            else: es=cyc(words(('FHC-' if '4' in t else 'C1-')+t))
            assert all(a in vs and b in vs and sum(x!=y for x,y in zip(a,b))==1 for a,b in es)
            full[key]=es; oldK[key]=es-edges('POOL-'+t+'-'+str(i))

    literal=re.findall(r'([0-4]{5}:[01])\s+([0-4])\s+([0-3])\s+([0-4]{5}:[01])\s+([0-3]{5})-([0-3]{5})',blocks['INTERFACES-ALL'])
    given={(a,int(j),c,b):edge(u,v) for a,j,c,b,u,v in literal}
    assert len(given)==len(literal)==313
    computed={}
    for a,vs in states.items():
        t=a[:5]
        for j,old in enumerate(t):
            if old=='4': continue
            for c in '0123':
                if c==old: continue
                changed=t[:j]+c+t[j+1:]; n,g=normal(changed)
                for b in states:
                    if b[:5]!=n: continue
                    restored={back(w,*g) for w in states[b]}
                    if vs & restored: computed[(a,j,c,b)]=g
    assert set(computed)==set(given)
    assert all(given[k] in oldK[k[0]] & restore_edges(oldK[k[3]],g) for k,g in computed.items())

    orbits={}
    for a in ('00000:0','00000:1'):
        assert {rotate(w,1) for w in states[a]}==states[a]
        assert rot_edges(full[a],1)==full[a]
        rem=set(full[a]); oo=[]
        while rem:
            orb=rot_edges({min(rem)},0)
            orb=set().union(*(rot_edges(orb,r) for r in range(5)))
            assert len(orb)==5 and orb<=rem
            oo.append(orb); rem-=orb
        assert len(oo)==3; orbits[a]=oo
    combinations=[]
    for x,y in product(range(3),repeat=2):
        K=dict(oldK)
        for a,n in (('00000:0',x),('00000:1',y)): K[a]=full[a]-orbits[a][n]
        changed=[]
        for k,g in computed.items():
            common=K[k[0]] & restore_edges(K[k[3]],g)
            assert common
            if given[k] not in common: changed.append({'interface':k,'old':given[k],'new':min(common)})
        combinations.append({'pools':[x,y],'interfaces':len(computed),'reselection':changed})

    pools={'00000:0':orbits['00000:0'][1],'00000:1':orbits['00000:1'][0]}
    seeds={('00000:0','1'):edge('23121','23123'),('00000:0','2'):edge('31231','31232'),
           ('00000:0','3'):edge('21231','23231'),('00000:1','1'):edge('21213','23213'),
           ('00000:1','2'):edge('31321','32321'),('00000:1','3'):edge('21321','21323')}
    two_direction=[]
    for (a,c),e in seeds.items():
        p=next(p for p in PERMS if p[0]=='0' and p[int(c)]=='1')
        plus=(1,1,p); minus=(4,-1,p)
        core=full[a] & restore_edges(oldK['00001:0'],plus) & restore_edges(oldK['00001:0'],minus)
        assert len(core)==2 and e in core-pools[a]
        normalized=[edge(forward(u,*g),forward(v,*g)) for g in (plus,minus) for u,v in (e,)]
        assert all(z in oldK['00001:0'] for z in normalized)
        pulled=[]
        for r in range(5):
            j=(-r)%5; changed='00000'[:j]+c+'00000'[j+1:]
            n,g=normal(changed)
            assert n=='00001' and g[2]==p and g[0]==(j-4*g[1])%5
            TK=restore_edges(oldK['00001:0'],g)
            pulled.append(rot_edges(TK,-r))
            moved=next(iter(rot_edges({e},r)))
            assert moved in (full[a]-pools[a]) & TK
        assert full[a] & set.intersection(*pulled)==core
        assert len({frozenset(es) for es in pulled})==2
        two_direction.append({'source':a,'excluded':c,'seed':e,'core':sorted(core),
                              'normalized_plus':normalized[0],'normalized_minus':normalized[1]})
    result={'input_sha256':hashlib.sha256(INPUT.read_bytes()).hexdigest(),
            'independently_enumerated_interfaces':len(computed),
            'all_nine_pool_choices':combinations,'preferred_pools':[1,0],
            'two_direction_certificate':two_direction,
            'claim':'six parametric families; target-K full rotation equivariance not assumed'}
    (HERE/'independent-results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='all_nine_pool_choices'},indent=2))

if __name__=='__main__': main()
