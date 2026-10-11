"""Independent 14 canonical selected-cycle interfaces; no search/helpers."""
from pathlib import Path
from itertools import product,permutations,combinations
from collections import Counter
import hashlib,json,re

HERE=Path(__file__).resolve().parent
LETTERS={'a':0,'b':1,'c':2,'d':3}

def edge(u,v):return tuple(sorted((u,v)))
def cycle_edges(ws):return {edge(u,v) for u,v in zip(ws,ws[1:]+ws[:1])}
def legal(t):return {w for w in product(range(4),repeat=3) if w[0]!=w[1]!=w[2] and all(w[i]!=t[i] for i in range(3))}
def raw_edges(V):return {edge(u,v) for u,v in combinations(V,2) if sum(a!=b for a,b in zip(u,v))==1}
def q_outside(ws,U):
    outside=set(ws)-U
    return 0 if not outside else sum(ws[i] in outside and ws[i-1] not in outside for i in range(len(ws)))
def txt(w):return ''.join(map(str,w))
def parse_word(w):return tuple(map(int,w))
def sym(w):return tuple(LETTERS[c] for c in w)

def main():
    full=HERE/'full-candidate-v1.tex';compact=HERE/'compact-candidate-v2.tex';ftext=full.read_text();ctext=compact.read_text()
    literal=json.loads((HERE/'selected-cycles-input-v1.json').read_text())
    primary=(HERE/'main-normalized-cycles-v1.tex').read_text()
    primary_rows={'001':primary.split('001&')[1].split('010&')[0],
                  '010':primary.split('010&')[1].split('012&')[0],
                  '012':primary.split('012&')[1].split('\\end{array}')[0]}
    assert all(re.findall(r'\b[0-3]{3}\b',primary_rows[t])==ws for t,ws in literal['cycles'].items())
    C={t:[parse_word(w) for w in ws] for t,ws in literal['cycles'].items()}
    for t,ws in C.items():
        assert len(ws)==len(set(ws)) and set(ws)==legal(parse_word(t))
        assert cycle_edges(ws)<=raw_edges(set(ws))
    def allowed(t):
        t=parse_word(t);found={}
        for base,ws in C.items():
            for p in permutations(range(4)):
                for rev in (False,True):
                    bt=tuple(p[v] for v in parse_word(base));bt=bt[::-1] if rev else bt
                    if bt!=t:continue
                    mapped=[tuple(p[v] for v in w) for w in ws];mapped=[w[::-1] for w in mapped] if rev else mapped
                    found[frozenset(cycle_edges(mapped))]=mapped
        return list(found.values())
    assert [len(allowed(t)) for t in ('001','010','012')]==[1,2,1]
    stabilizers={'E_unused_colour_swap':cycle_edges(C['001'])==cycle_edges([tuple((0,1,3,2)[v] for v in w) for w in C['001']]),
                 'M_unused_colour_swap':cycle_edges(C['010'])==cycle_edges([tuple((0,1,3,2)[v] for v in w) for w in C['010']]),
                 'A_reverse_plus_endpoint_colour_swap':cycle_edges(C['012'])==cycle_edges([tuple((2,1,0,3)[v] for v in w[::-1]) for w in C['012']])}
    assert all(stabilizers.values())
    def special(t):
        t=parse_word(t)
        if t[0]==t[1]!=t[2]:a,b=t[0],t[2]
        elif t[0]!=t[1]==t[2]:a,b=t[1],t[0]
        else:return set()
        P=set()
        for c in set(range(4))-{a,b}:
            Q={w for w in legal((a,a,a)) if w[1]==c}
            common=legal(t)&Q;es=raw_edges(common);assert len(es)==1;P|=es
        return P
    # Read every full literal path profile from the candidate itself.
    identity=ftext.split('\\paragraph{Cycle identities used by the count.}')[1]
    chunks={'001':identity.split('In $E(aab)$')[1].split('In $A(abc)$')[0],
            '012':identity.split('In $A(abc)$')[1].split('In $M_0(aba)$')[0],
            '010':identity.split('In $M_0(aba)$')[1].split('For $M_1$')[0]}
    specs={'001':([(2,2),(1,2),(0,2),(0,1)],[1,1,2,2]),
           '012':([(1,0),(0,1),(2,3),(0,2)],[1,2,2,2]),
           '010':([(0,1),(2,1),(0,2),(2,2)],[3,2,2,2])}
    profiles=[]
    for t,chunk in chunks.items():
        paths=[[sym(w) for w in p.split(',')] for p in re.findall(r'\[([abcd]{3}(?:,[abcd]{3})*)\]',chunk)]
        coords,groups=specs[t];assert len(paths)==sum(groups)
        at=0
        for (coordinate,colour),number in zip(coords,groups):
            pp=paths[at:at+number];at+=number
            vertices={w for w in C[t] if w[coordinate]==colour}
            assert {w for p in pp for w in p}==vertices
            assert sum(map(len,pp))==len(vertices)
            expected={edge(u,v) for p in pp for u,v in zip(p,p[1:])}
            actual={e for e in cycle_edges(C[t]) if set(e)<=vertices}
            assert expected==actual
            profiles.append({'cycle':t,'coordinate':coordinate,'colour':colour,'path_orders':list(map(len,pp)),
                             'literal_paths':[[txt(w) for w in p] for p in pp]})
    expected_compact=[[4],[4],[3,2],[2,2],[6],[4,3],[3,2],[3,1],[3,2,2],[5,2],[3,2],[4,1]]
    assert [p['path_orders'] for p in profiles]==expected_compact
    ctrows=re.findall(r'([abcd]{3})\\to ([abcd]{3})&([0-9]+)&([0-9]+)&([0-9]+)&([0-9]+)&([0-9]+)&([0-9]+)',ftext)
    compactrows=re.findall(r'([abcd]{3})\\to ([abcd]{3})&([0-9]+)&([0-9]+)&([0-9]+)&([0-9]+)&([0-9]+)&([0-9]+)',ctext)
    assert ctrows==compactrows and len(ctrows)==6
    reports=[]
    for source,target,n,m,f,r,k,bound in ctrows:
        t,s=txt(sym(source)),txt(sym(target));U=legal(parse_word(t))&legal(parse_word(s));H=raw_edges(U)
        F=(special(t)|special(s))&H
        assert (len(U),len(H),len(F))==tuple(map(int,(n,m,f)))
        layer_counts=sorted((len({w for w in U if w[1]==v}),len({e for e in H if e[0][1]==e[1][1]==v})) for v in range(4) if any(w[1]==v for w in U))
        middle_edges=sum(e[0][1]!=e[1][1] for e in H)
        for Ci,Cj in product(allowed(t),allowed(s)):
            Ec,Ed=cycle_edges(Ci),cycle_edges(Cj)
            q=q_outside(Ci,U)+q_outside(Cj,U);assert q<=int(r)
            if (source,target)==('abc','abd'):
                R={edge(sym('bab'),sym('cab')),edge(sym('bab'),sym('dab'))}
            elif (source,target)==('aab','bab'):
                R=set()
                for u in (2,3):
                    row={w for w in U if w[0]==u and w[1]==1}
                    triangle=raw_edges(row);assert len(triangle)==3
                    assert len(Ec&triangle)==1
                    target_kept=len(Ed&triangle);assert target_kept in (1,2)
                    if target_kept==2:assert Ec&triangle<=Ed
                    unused=triangle-(Ec|Ed);assert unused;R.add(min(unused))
            elif (source,target)==('aba','cba'):
                R={edge(sym('bab'),sym('bac')),edge(sym('bab'),sym('bad')),edge(sym('dad'),sym('dcd'))}
                assert all(e[0][0]==1 or e[0][2]==1 for e in Ec|Ed if e[0][1]!=e[1][1])
            else:R=set()
            assert len(R)==int(k) and R<=H-F and not R&(Ec|Ed)
            lower=2*len(U)-q-len(H)-len(F)+len(R)
            safe=(Ec&Ed)-F;assert len(safe)>=lower>=int(bound)>=2
            reports.append({'source':t,'target':s,'source_cycle_sha256':hashlib.sha256(repr(sorted(Ec)).encode()).hexdigest(),
                            'target_cycle_sha256':hashlib.sha256(repr(sorted(Ed)).encode()).hexdigest(),
                            'common_vertices':len(U),'common_raw_edges':len(H),'forbidden_count':len(F),
                            'outside_path_sum':q,'unused_edges':[[txt(w) for w in e] for e in sorted(R)],
                            'DP_lower_bound':lower,'actual_safe_common_edges':len(safe),
                            'fixed_middle_layer_sizes':layer_counts,'middle_change_edges':middle_edges})
    supports=[]
    for t,s,family in [('001','011','EE-transfer'),('012','032','AA-middle'),('010','020','MM')]:
        for Ci,Cj in product(allowed(t),allowed(s)):
            Ec,Ed=cycle_edges(Ci),cycle_edges(Cj);F=special(t)|special(s)
            if family=='EE-transfer':
                W={edge(sym('bca'),sym('bcd')),edge(sym('bca'),sym('dca'))};assert W<=(Ec&Ed)-F
            elif family=='AA-middle':
                hexagon=[sym(w) for w in ['bab','bad','cad','dad','dab','cab']];HH=cycle_edges(hexagon)
                assert len(Ec&HH)==len(Ed&HH)==5 and len(Ec&Ed&HH)>=4 and not F
            else:
                square={w for w in legal((0,0,0)) if w[1]==3};HH=raw_edges(square)
                assert len(HH)==4 and len(Ec&HH)==len(Ed&HH)==3 and len(Ec&Ed&HH)>=2 and not F
            safe=(Ec&Ed)-F;assert len(safe)>=2
            supports.append({'family':family,'actual_safe_common_count':len(safe)})
    assert len(reports)==8 and len(supports)==6
    result={'status':'PASS','allowed_fixed_boundary_edge_set_counts':[1,2,1],
            'stabilizers':stabilizers,'twelve_literal_profiles':profiles,
            'compact_CT_transcription_equal':True,'compact_coordinate_profile_orders_equal':True,
            'selected_input_matches_frozen_main_equation':True,
            'eight_canonical_CT_cycle_pairs':reports,'six_canonical_support_cycle_pairs':supports,
            'no_Hamilton_search':True,'full_candidate_sha256':hashlib.sha256(full.read_bytes()).hexdigest(),
            'compact_candidate_sha256':hashlib.sha256(compact.read_bytes()).hexdigest(),
            'scope':'14 canonical selected-cycle interfaces only. All labelled color/reversal images follow by the analytic equivariance argument.'}
    (HERE/'review-results-v1.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('twelve_literal_profiles','eight_canonical_CT_cycle_pairs','six_canonical_support_cycle_pairs')}))

if __name__=='__main__':main()
