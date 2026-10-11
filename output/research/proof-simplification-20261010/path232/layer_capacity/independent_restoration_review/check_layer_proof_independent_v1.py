"""Independent primary-cycle reader and14 layer proof cases; no peer imports."""
from pathlib import Path
from itertools import product,permutations,combinations
import re,json,hashlib
HERE=Path(__file__).resolve().parent
def edge(u,v):return tuple(sorted((u,v)))
def parse(w):return tuple(map(int,w))
def chars(w):return tuple('abcd'.index(c) for c in w)
def cyclic(ws):return {edge(u,v) for u,v in zip(ws,ws[1:]+ws[:1])}
def raw(V):return {edge(u,v) for u,v in combinations(sorted(V),2) if sum(a!=b for a,b in zip(u,v))==1}
def legal(t):return {w for w in product(range(4),repeat=3) if w[0]!=w[1]!=w[2] and all(w[i]!=t[i] for i in range(3))}
def rank(t):return 0 if t[0]==t[1] or t[1]==t[2] else 1 if t[0]==t[2] else 2
def main():
    source=(HERE/'selected-cycles-primary.tex').read_text();candidate=HERE/'layer-proof-candidate-v1.tex';text=candidate.read_text();assert hashlib.sha256(candidate.read_bytes()).hexdigest()=='7d8db274e8529a31261988b92e2908852a3422952f0c77f5cdda4a5151800d08'
    sections={'001':source.split('001&')[1].split('010&')[0],'010':source.split('010&')[1].split('012&')[0],'012':source.split('012&')[1].split('\\end{array}')[0]}
    C={t:[parse(w) for w in re.findall(r'\b[0-3]{3}\b',s)] for t,s in sections.items()}
    for t,ws in C.items():assert len(ws)==len(set(ws)) and set(ws)==legal(parse(t)) and cyclic(ws)<=raw(set(ws))
    def image(ws,p,rev):
        out=[tuple(p[c] for c in w) for w in ws]
        return [w[::-1] for w in out] if rev else out
    def allowed(t):
        found={}
        for base,ws in C.items():
            for p in permutations(range(4)):
                for rev in (False,True):
                    b=tuple(p[c] for c in parse(base));b=b[::-1] if rev else b
                    if b==t:
                        mapped=image(ws,p,rev);found[frozenset(cyclic(mapped))]=mapped
        return list(found.values())
    assert [len(allowed(parse(t))) for t in ('001','010','012')]==[1,2,1]
    assert cyclic(C['001'])==cyclic(image(C['001'],(0,1,3,2),False))
    assert cyclic(C['010'])==cyclic(image(C['010'],(0,1,3,2),False))
    assert cyclic(C['012'])==cyclic(image(C['012'],(2,1,0,3),True))
    def special(t):
        if t[0]==t[1]!=t[2]:a,b=t[0],t[2]
        elif t[0]!=t[1]==t[2]:a,b=t[1],t[0]
        else:return set()
        out=set()
        for v in set(range(4))-{a,b}:
            W={w for w in legal((a,a,a))&legal(t) if w[1]==v};edges=raw(W);assert len(edges)==1;out|=edges
        return out
    # Parse all six literal paths from the frozen candidate itself.
    support=text.split('% BEGIN SELECTED-SUPPORT')[1]
    layer_rows=re.findall(r'^(E|M_0|A)&([abcd])&([^\n]+)',support,re.M);assert len(layer_rows)==6
    layer_reports=[]
    for label,v,entry in layer_rows:
        t={'E':'001','M_0':'010','A':'012'}[label];ws=C[t];colour='abcd'.index(v)
        paths=[[chars(w) for w in p.split(',')] for p in re.findall(r'\[([abcd]{3}(?:,[abcd]{3})*)\]',entry)]
        W={w for w in ws if w[1]==colour};assert sum(map(len,paths))==len(W) and {w for p in paths for w in p}==W
        expected={edge(u,v) for path in paths for u,v in zip(path,path[1:])};assert expected=={e for e in cyclic(ws) if set(e)<=W}
        layer_reports.append({'cycle':label,'middle_colour':v,'path_orders':list(map(len,paths)),'edge_count':len(expected)})
    cross_reports=[]
    for t,ws in C.items():
        H={e for e in cyclic(ws) if e[0][1]!=e[1][1]};assert len(H)==4
        central={'001':1,'010':0,'012':3}[t];leaves={'001':{2,3},'010':{2,3},'012':{0,2}}[t]
        assert all(central in {u[1],v[1]} for u,v in H)
        assert all(sum({u[1],v[1]}=={central,leaf} for u,v in H)==2 for leaf in leaves)
        if t=='001':assert [sum(u[2]==colour for u,v in H) for colour in (0,2,3)]==[2,1,1]
        elif t=='010':assert all(u[0]==v[0]==1 for u,v in H)
        else:assert all(u[0] in {1,2} and v[0] in {1,2} and u[2] in {0,1} and v[2] in {0,1} for u,v in H)
        cross_reports.append({'cycle':t,'middle_change_edges':4,'star_centre':central,'star_leaf_multiplicities':[2,2]})
    pairs=[('aab','aac'),('aab','abb'),('aab','acb'),('aab','cab'),('aab','bab'),('aba','aca'),('aba','cba'),('abc','abd'),('abc','adc')]
    orbit=set()
    for a,b in pairs:
        for p in permutations(range(4)):
            for rev in (False,True):
                x=tuple(p[c] for c in chars(a));y=tuple(p[c] for c in chars(b))
                orbit.add((x[::-1],y[::-1]) if rev else (x,y))
    allpairs={(t,s) for t in product(range(4),repeat=3) for s in product(range(4),repeat=3) if len(set(t))>1 and len(set(s))>1 and sum(a!=b for a,b in zip(t,s))==1 and rank(t)<=rank(s)}
    assert orbit==allpairs
    specs={('aab','aac'):[('*',(4,3,3))],('aab','abb'):[(2,(2,2,2))],('aab','acb'):[('*',(2,2,2))],('aab','cab'):[(2,(3,2,2)),(3,(1,1,1))],('aba','aca'):[(3,(4,3,3))],('abc','abd'):[('*',(6,4,4))],('abc','adc'):[(0,(9,5,5)),(2,(9,5,5))]}
    table=text.split('Seven families use:')[1].split('Thus each gives')[0]
    # The last pair prints "each", so its triple occurs only once.
    table_expected=[(4,3,3),(2,2,2),(2,2,2),(3,2,2),(1,1,1),(4,3,3),(6,4,4),(9,5,5)]
    assert [tuple(map(int,x)) for x in re.findall(r'\(([0-9]+),([0-9]+),([0-9]+)\)',table)]==table_expected
    reports=[]
    for source_t,target_t in pairs:
        t,s=chars(source_t),chars(target_t);U=legal(t)&legal(s);H=raw(U);F=(special(t)|special(s))&H
        L=set(range(4))-{t[0],s[0]};R=set(range(4))-{t[2],s[2]}
        for v in range(4):
            layer={e for e in H if e[0][1]==e[1][1]==v};expected=len(L-{v})*(len(L-{v})-1)//2*len(R-{v})+len(R-{v})*(len(R-{v})-1)//2*len(L-{v}) if v not in {t[1],s[1]} else 0
            assert len(layer)==expected
        for v,w in combinations(set(range(4))-{t[1],s[1]},2):assert sum({e[0][1],e[1][1]}=={v,w} for e in H)==len(L-{v,w})*len(R-{v,w})
        for Ci,Dj in product(allowed(t),allowed(s)):
            Ec,Ed=cyclic(Ci),cyclic(Dj);blocks=[]
            if (source_t,target_t) in specs:
                for v,expected in specs[(source_t,target_t)]:
                    rawblock={e for e in H if (e[0][1]!=e[1][1] if v=='*' else e[0][1]==e[1][1]==v)};B=rawblock-F;m=len(B);x=sum(e in Ec for e in B);y=sum(e in Ed for e in B);assert (m,x,y)==expected
                    blocks.append({'middle':v,'raw_edges':len(rawblock),'removed_special':len(rawblock&F),'safe_universe_edges':m,'source_retained':x,'target_retained':y,'lower_bound':x+y-m})
                lower=sum(max(0,b['lower_bound']) for b in blocks)
            elif (source_t,target_t)==('aab','bab'):
                prism={e for e in H if e[0][1]==e[1][1]==1};assert len(prism)==9 and not (prism&F)
                rows=[{e for e in prism if e[0][0]==e[1][0]==u} for u in (2,3)];rungs={e for e in prism if e[0][0]!=e[1][0]}
                assert all(len(row)==3 and sum(e in Ec for e in row)==1 for row in rows) and sum(e in Ec for e in rungs)==2
                Erows=[{e for e in row if e in Ec} for row in rows];Erungs={e for e in rungs if e in Ec}
                triangle_case=all(all(e in Ed for e in chosen) for chosen in Erows);rung_case=all(e in Ed for e in Erungs)
                assert triangle_case!=rung_case
                lower=2;blocks=[{'middle':1,'mode':'two_triangle_edges' if triangle_case else 'two_rungs','lower_bound':2}]
            else:
                assert (source_t,target_t)==('aba','cba') and not F
                P={e for e in H if e[0][1]==e[1][1]==0};omitted={edge(chars('bab'),chars('bac')),edge(chars('bab'),chars('bad'))};assert len(P)==9 and omitted<=P and all(e not in Ec and e not in Ed for e in omitted)
                B=P-omitted;assert (len(B),sum(e in Ec for e in B),sum(e in Ed for e in B))==(7,3,5)
                Q={e for e in H if e[0][1]==e[1][1]==2};assert (len(Q),sum(e in Ec for e in Q),sum(e in Ed for e in Q))==(4,3,2)
                lower=2;blocks=[{'middle':0,'raw_edges':9,'jointly_unused_deleted':2,'universe_edges':7,'source_retained':3,'target_retained':5,'lower_bound':1},{'middle':2,'universe_edges':4,'source_retained':3,'target_retained':2,'lower_bound':1}]
            assert lower>=2
            reports.append({'source':source_t,'target':target_t,'source_edges_sha256':hashlib.sha256(repr(sorted(Ec)).encode()).hexdigest(),'target_edges_sha256':hashlib.sha256(repr(sorted(Ed)).encode()).hexdigest(),'blocks':blocks,'safe_lower_bound':lower})
    assert len(reports)==14
    result={'status':'PASS_INDEPENDENT_LAYER_PROOF','candidate_sha256':hashlib.sha256(candidate.read_bytes()).hexdigest(),'primary_equation_sha256':hashlib.sha256((HERE/'selected-cycles-primary.tex').read_bytes()).hexdigest(),'allowed_fixed_boundary_edge_sets':[1,2,1],'classification_ordered_pairs':len(allpairs),'nine_families_exhaustive':True,'six_literal_layer_identities':layer_reports,'three_middle_cross_star_rules':cross_reports,'fourteen_allowed_orientation_cases':reports,'actual_full_cycle_edge_intersection_computed':False,'Hamilton_search':False,'scope':'selected three cycles and all their color/reversal images; arbitrary-order restoration not computationally searched'}
    (HERE/'independent-layer-review-results-v1.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('six_literal_layer_identities','three_middle_cross_star_rules','fourteen_allowed_orientation_cases')}))
if __name__=='__main__':main()
