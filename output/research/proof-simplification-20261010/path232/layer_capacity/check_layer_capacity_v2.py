#!/usr/bin/env python3
"""Fixed layer and middle-change block capacities; no cycle search."""
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
    tic=time.monotonic();src=MAIN.read_text()
    eq=re.search(r'\\begin\{equation\}\n\\label\{eq:path232-cycles\}.*?\\end\{equation\}',src,re.S).group(0)
    frozen=BASE/'selected-cycles-source-v1.tex'
    if frozen.exists():assert frozen.read_text()==eq+'\n'
    else:frozen.write_text(eq+'\n')
    C={}
    for t in ('001','010','012'):
        segment=eq.split(t+'&',1)[1].split('[2pt]',1)[0].split('\\end{array}',1)[0]
        C[t]=[tuple(map(int,w)) for w in re.findall(r'(?<![0-9])[0-3]{3}(?![0-9])',segment)]
        boundary=tuple(map(int,t));assert set(C[t])==fibre(boundary)
        assert len(C[t])==len(set(C[t])) and ce(C[t])<=graph(fibre(boundary))
    # Directly certify the fixed-boundary symmetries behind allowed().
    for t in ('001','010'):
        assert ce(C[t])==ce(transform(C[t],(0,1,3,2)))
    assert ce(C['012'])==ce(transform(C['012'],(2,1,0,3),True))
    supports={}
    for t,cycle in C.items():
        E=ce(cycle);supports[t]={}
        for v in range(4):
            V={x for x in cycle if x[1]==v};Ev={e for e in E if e[0][1]==e[1][1]==v}
            if V:supports[t][str(v)]={'vertices':len(V),'cycle_edges':len(Ev),'path_component_sizes':components(V,Ev),'literal_edges':[list(map(word,e)) for e in sorted(Ev)]}
    families=[('aab','aac'),('aab','abb'),('aab','acb'),('aab','bab'),('aab','cab'),('aba','aca'),('aba','cba'),('abc','abd'),('abc','adc')]
    vertex=lambda s:tuple('abcd'.index(c) for c in s)
    records=[]
    for st,tt in families:
        s,t=vertex(st),vertex(tt);U=fibre(s)&fibre(t);H=graph(U);F=(special(s)|special(t))&H
        orientations=[]
        for i,A in enumerate(allowed(s,C)):
            for j,B in enumerate(allowed(t,C)):
                AE,BE=ce(A),ce(B);layers=[]
                for v in range(4):
                    V={x for x in U if x[1]==v};Hv={e for e in H if e[0][1]==e[1][1]==v}
                    if not V:continue
                    Av,Bv,Fv=AE&Hv,BE&Hv,F&Hv
                    a,b,m,f,x,y=len(Av),len(Bv),len(Hv),len(Fv),len(Av&Fv),len(Bv&Fv)
                    coarse=max(0,a+b-m-f);exact=max(0,a+b-m-x-y+f)
                    omitted=len(Hv-(AE|BE|F))
                    sharp=max(0,a+b-m-x-y+f+omitted)
                    actual=(Av&Bv)-Fv
                    assert len(actual)>=sharp>=exact>=coarse
                    layers.append({'middle':'abcd'[v],'n':len(V),'m':m,'source_retained':a,'target_retained':b,'forbidden_union':f,'source_forbidden_loss':x,'target_forbidden_loss':y,'joint_omitted_safe':omitted,'coarse_capacity':coarse,'exact_loss_capacity':exact,'omitted_capacity':sharp,'actual_safe_common':len(actual),'safe_common_edges':[list(map(word,e)) for e in sorted(actual)]})
                cross={e for e in H if e[0][1]!=e[1][1]}
                crossactual=(AE&BE&cross)-F
                ca,cb,cm,cf,cx,cy=len(AE&cross),len(BE&cross),len(cross),len(F&cross),len(AE&F&cross),len(BE&F&cross)
                crosscoarse=max(0,ca+cb-cm-cf)
                crossexact=max(0,ca+cb-cm-cx-cy+cf)
                assert len(crossactual)>=crossexact>=crosscoarse
                crossrecord={'m':cm,'source_retained':ca,'target_retained':cb,'forbidden_union':cf,'coarse_capacity':crosscoarse,'exact_loss_capacity':crossexact,'actual_safe_common':len(crossactual)}
                orientations.append({'source_orientation':i,'target_orientation':j,'layers':layers,'sum_coarse':sum(x['coarse_capacity'] for x in layers),'sum_exact_loss':sum(x['exact_loss_capacity'] for x in layers),'sum_omitted_capacity':sum(x['omitted_capacity'] for x in layers),'actual_layer_safe_common':sum(x['actual_safe_common'] for x in layers),'actual_cross_safe_common':len(crossactual),'middle_change_block':crossrecord,'layer_plus_cross_coarse':sum(x['coarse_capacity'] for x in layers)+crosscoarse,'layer_plus_cross_exact_loss':sum(x['exact_loss_capacity'] for x in layers)+crossexact})
        records.append({'family':[st,tt],'orientation_cases':len(orientations),'min_coarse':min(x['sum_coarse'] for x in orientations),'min_exact_loss':min(x['sum_exact_loss'] for x in orientations),'min_with_omission':min(x['sum_omitted_capacity'] for x in orientations),'min_layer_plus_cross_coarse':min(x['layer_plus_cross_coarse'] for x in orientations),'min_layer_plus_cross_exact_loss':min(x['layer_plus_cross_exact_loss'] for x in orientations),'orientations':orientations})
    result={'verdict':'PASS','scope':'Nine canonical fixed-selected-cycle families and every M orientation; no Hamilton search','source_main_sha256':sha(MAIN),'input_source_equation_sha256':sha(frozen),'script_sha256':sha(Path(__file__)),'selected_layer_supports':supports,'family_count':len(records),'canonical_orientation_cases':sum(r['orientation_cases'] for r in records),'families':records,'coarse_success_families':[r['family'] for r in records if r['min_coarse']>=2],'exact_loss_success_families':[r['family'] for r in records if r['min_exact_loss']>=2],'exact_loss_fail_families':[r['family'] for r in records if r['min_exact_loss']<2],'layer_plus_cross_success_families':[r['family'] for r in records if r['min_layer_plus_cross_exact_loss']>=2],'layer_plus_cross_fail_families':[r['family'] for r in records if r['min_layer_plus_cross_exact_loss']<2],'elapsed_seconds':time.monotonic()-tic,'new_cycle_search':False}
    (BASE/'layer-capacity-results-v2.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'case_count':result['canonical_orientation_cases'],'families':[{k:r[k] for k in ('family','min_coarse','min_exact_loss','min_with_omission','min_layer_plus_cross_coarse','min_layer_plus_cross_exact_loss')} for r in records],'supports':supports,'elapsed':result['elapsed_seconds']},indent=2))

if __name__=='__main__':main()
