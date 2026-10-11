#!/usr/bin/env python3
"""Fixed selected-cycle layer counts, with no prior checker imports/search."""
from pathlib import Path
import hashlib,itertools,json,re,time

BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[4]
MAIN=ROOT/'planar_recoloring_hamilton_thresholds.tex'
edge=lambda x,y:tuple(sorted((x,y)))
word=lambda x:''.join(map(str,x))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def fibre(t):
    return {x for x in itertools.product(range(4),repeat=3)
            if x[0]!=x[1] and x[1]!=x[2] and all(x[i]!=t[i] for i in range(3))}

def graph(V):
    return {edge(x,y) for x,y in itertools.combinations(V,2)
            if sum(a!=b for a,b in zip(x,y))==1}

def ce(C): return {edge(x,y) for x,y in zip(C,C[1:]+C[:1])}

def transform(C,p,reverse=False):
    return [tuple(p[c] for c in (x[::-1] if reverse else x)) for x in C]

def components(V,E):
    unseen=set(V);out=[]
    while unseen:
        stack=[unseen.pop()];part=set(stack)
        while stack:
            x=stack.pop()
            nbr={y for e in E if x in e for y in e if y!=x}&unseen
            unseen-=nbr;part|=nbr;stack+=list(nbr)
        out.append(part)
    return sorted(map(len,out))

def allowed(t,C):
    if t[0]==t[1]:
        a,b=t[0],t[2];u=sorted(set(range(4))-{a,b});return [transform(C['001'],(a,b,*u))]
    if t[1]==t[2]:
        a,b=t[1],t[0];u=sorted(set(range(4))-{a,b});return [transform(C['001'],(a,b,*u),True)]
    if t[0]==t[2]:
        a,b=t[0],t[1];u=sorted(set(range(4))-{a,b});p=(a,b,*u)
        return [transform(C['010'],p),transform(C['010'],p,True)]
    d,=set(range(4))-set(t);return [transform(C['012'],(*t,d))]

def special(t):
    if t[0]==t[1]:
        a,b=t[0],t[2];c,d=sorted(set(range(4))-{a,b})
        return {edge((b,c,d),(d,c,d)),edge((b,d,c),(c,d,c))}
    if t[1]==t[2]:return {edge(x[::-1],y[::-1]) for x,y in special(t[::-1])}
    return set()

def main():
    local=BASE/'layer-proof-candidate-v1.tex';proof=local.read_text()
    eq=(BASE/'selected-cycles-source-v1.tex').read_text();C={}
    for t in ('001','010','012'):
        segment=eq.split(t+'&',1)[1].split('[2pt]',1)[0].split('\\end{array}',1)[0]
        C[t]=[tuple(map(int,w)) for w in re.findall(r'(?<![0-9])[0-3]{3}(?![0-9])',segment)]
        assert set(C[t])==fibre(tuple(map(int,t))) and ce(C[t])<=graph(set(C[t]))
    vertex=lambda s:tuple('abcd'.index(c) for c in s)
    # Read every literal selected-layer path from the candidate itself.
    section=proof.split('\\text{cycle}&v&\\text{paths}',1)[1].split('\\end{array}',1)[0]
    rows=re.findall(r'(E|M_0|A)&([abcd])&([^\n]+)',section)
    assert [(x,y) for x,y,_ in rows]==[('E','b'),('E','c'),('M_0','a'),('M_0','c'),('A','a'),('A','d')]
    typ={'E':'001','M_0':'010','A':'012'};profiles=[]
    for kind,v,text in rows:
        groups=[list(map(vertex,g.split(','))) for g in re.findall(r'\[([abcd,]+)\]',text)]
        V={x for x in C[typ[kind]] if x[1]=='abcd'.index(v)}
        Ev={e for e in ce(C[typ[kind]]) if e[0][1]==e[1][1]=='abcd'.index(v)}
        assert {x for g in groups for x in g}==V
        assert {edge(x,y) for g in groups for x,y in zip(g,g[1:])}==Ev
        profiles.append({'cycle':kind,'middle':v,'paths':[[word(x) for x in g] for g in groups]})
    for typx in ('001','010'):assert ce(C[typx])==ce(transform(C[typx],(0,1,3,2)))
    assert ce(C['012'])==ce(transform(C['012'],(2,1,0,3),True))
    stars=[]
    for t,hub,leaves in [('001',1,(2,3)),('010',0,(2,3)),('012',3,(0,2))]:
        X={e for e in ce(C[t]) if e[0][1]!=e[1][1]}
        assert len(X)==4
        assert {pair:sum(tuple(sorted((x[1],y[1])))==pair for x,y in X) for pair in [(min(hub,v),max(hub,v)) for v in leaves]}=={(min(hub,v),max(hub,v)):2 for v in leaves}
        if t=='001':assert {v:sum(x[2]==v for x,y in X) for v in (0,2,3)}=={0:2,2:1,3:1}
        if t=='010':assert all(x[0]==y[0]==1 for x,y in X)
        if t=='012':assert all(x[0] in (1,2) and x[2] in (0,1) for x,y in X)
        stars.append({'type':t,'middle_hub':hub,'two_edges_to_each_leaf':list(leaves),'cross_edges':[list(map(word,e)) for e in sorted(X)]})
    specs=[('aab','aac',['*'],[(4,3,3)]),('aab','abb',['c'],[(2,2,2)]),('aab','acb',['*'],[(2,2,2)]),('aab','cab',['c','d'],[(3,2,2),(1,1,1)]),('aba','aca',['d'],[(4,3,3)]),('abc','abd',['*'],[(6,4,4)]),('abc','adc',['a','c'],[(9,5,5),(9,5,5)])]
    ct=proof.split('t\\to s&\\text{blocks}&(m,x,y)',1)[1].split('\\end{array}',1)[0]
    printed=re.findall(r'(aab|aba|abc)\\to ([abcd]{3})&([^&]+)&([^\n]+)',ct)
    assert [(s,t) for s,t,_,_ in printed]==[(s,t) for s,t,_,_ in specs]
    table=[];cases=0
    for (s,t,bl,counts),(ps,pt,pbl,pcount) in zip(specs,printed):
        assert re.findall(r'H_([abcd*])',pbl)==bl
        nums=[tuple(map(int,x)) for x in re.findall(r'\((\d+),(\d+),(\d+)\)',pcount)]
        if len(nums)==1 and len(counts)==2:assert '\\text{ each}' in pcount;nums*=2
        assert nums==counts
        S,T=vertex(s),vertex(t);U=fibre(S)&fibre(T);H=graph(U);F=(special(S)|special(T))&H;verified=[]
        for i,A in enumerate(allowed(S,C)):
            for j,B in enumerate(allowed(T,C)):
                esA,esB=ce(A),ce(B);actual=[]
                for b,expected in zip(bl,counts):
                    K={e for e in H if (e[0][1]!=e[1][1] if b=='*' else e[0][1]==e[1][1]=='abcd'.index(b))}-F
                    triple=(len(K),len(esA&K),len(esB&K));assert triple==expected
                    actual.append(triple)
                bound=sum(max(0,x+y-m) for m,x,y in actual);assert bound>=2
                verified.append({'source_orientation':i,'target_orientation':j,'triples':actual,'capacity':bound});cases+=1
        table.append({'family':[s,t],'blocks':bl,'counts':counts,'verified_orientations':verified})
    em=[];S,T=vertex('aab'),vertex('bab');U=fibre(S)&fibre(T);H=graph(U);E=ce(allowed(S,C)[0]);P={e for e in H if e[0][1]==e[1][1]==1};F=special(S)|special(T)
    assert len(P)==9 and not(P&F)
    horizontals={e for e in E&P if e[0][0]==e[1][0]};verticals={e for e in E&P if e[0][2]==e[1][2]}
    assert len(horizontals)==len(verticals)==2
    assert all(sum(e[0][0]==v for e in horizontals)==1 for v in (2,3))
    for j,D in enumerate(allowed(T,C)):
        selected=ce(D)
        assert (horizontals if j==0 else verticals)<=selected
        em.append({'M_orientation':j,'included_E_prism_edges':'one per row triangle' if j==0 else 'two vertical edges','safe_common_count':len((E&selected&P)-F)});cases+=1
    ma=[];S,T=vertex('aba'),vertex('cba');U=fibre(S)&fibre(T);H=graph(U);F=special(S)|special(T);assert not F
    R={edge(vertex('bab'),vertex(x)) for x in ('bac','bad')};D=ce(allowed(T,C)[0])
    for i,A in enumerate(allowed(S,C)):
        E=ce(A);Ha={e for e in H if e[0][1]==e[1][1]==0};Hc={e for e in H if e[0][1]==e[1][1]==2}
        assert len(Ha)==9 and R<=Ha and not R&(E|D)
        assert len(E&Ha)==3 and len(D&Ha)==5
        assert (len(Hc),len(E&Hc),len(D&Hc))==(4,3,2)
        assert not any(vertex('bab') in e for e in E&Ha)
        assert {e for e in D&Ha if vertex('bab') in e}=={edge(vertex('bab'),vertex('dab'))}
        ma.append({'M_orientation':i,'reduced_middle_a_universe':7,'source_target_retained':[3,5],'middle_c_counts':[4,3,2],'capacity':(3+5-7)+(3+2-4)});cases+=1
    assert cases==14
    old=(ROOT/'planar_recoloring_hamilton_thresholds.tex').read_text()
    start=old.index('\\begin{proof}',old.index('\\begin{lemma}[Safe common edges]'));end=old.index('\\end{proof}',start)+len('\\end{proof}')
    ti=old.index('\\subsection{Safe common-edge witnesses}');tj=old.index('\\clearpage',ti)
    metric=lambda s:len(re.findall(r'\b[A-Za-z]+\b',re.sub(r'\\[A-Za-z]+',' ',re.sub(r'(?m)%.*$','',s))))
    result={'verdict':'PASS','scope':'Actual short candidate readback for seven capacity families and two prism mechanisms; all fourteen M-orientation cases','candidate_sha256':sha(local),'input_equation_sha256':sha(BASE/'selected-cycles-source-v1.tex'),'main_sha256':sha(MAIN),'script_sha256':sha(Path(__file__)),'six_literal_layer_identities':profiles,'middle_change_star_identities':stars,'seven_capacity_families':table,'EM_prism_support':em,'MA_prism_omissions':ma,'canonical_orientation_cases':cases,'all_allowed_edge_sets_preserved_by_fixed_boundary_symmetries':True,'token_metric':'ASCII alphabetic tokens after TeX commands/comments removed; numerical triples excluded','tokens':{'original_safe_proof_conventions_table':metric(old[start:end]+old[ti:tj]),'new_proof':metric(proof.split('% BEGIN SAFE-PROOF',1)[1].split('% END SAFE-PROOF',1)[0]),'new_appendix_support':metric(proof.split('% BEGIN SELECTED-SUPPORT',1)[1].split('% END SELECTED-SUPPORT',1)[0])},'new_cycle_search':False,'evidence_boundary':'Certificate consistency readback accompanies the symbolic argument; it is not a proof for arbitrary Hamilton cycles or formal verification.'}
    (BASE/'layer-proof-review-v1.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('verdict','canonical_orientation_cases','tokens','candidate_sha256')},indent=2))

if __name__=='__main__':main()

