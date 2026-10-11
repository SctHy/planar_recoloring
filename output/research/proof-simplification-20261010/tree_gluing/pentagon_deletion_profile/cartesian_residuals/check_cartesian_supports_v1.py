"""Fixed7 selected-pair Cartesian supports; no peer imports or HC search."""
from pathlib import Path
from itertools import product,permutations,combinations
from collections import defaultdict,Counter
import hashlib,json,re,time

HERE=Path(__file__).resolve().parent
CASES=[('00014',0,3),('00123',0,3),('01014',0,2),('01014',0,3),('01014',2,2),('01124',2,2),('01204',2,0)]
def edge(u,v):return tuple(sorted((u,v)))
def parse(w):return tuple(map(int,w))
def text(w):return ''.join(map(str,w))
def cycle(ws):
    assert len(ws)==len(set(ws))
    out={edge(u,v) for u,v in zip(ws,ws[1:]+ws[:1])}
    assert all(sum(a!=b for a,b in zip(u,v))==1 for u,v in out)
    return out
def legal(t):return {w for w in product(range(4),repeat=5) if all(w[i]!=w[(i+1)%5] and (t[i]==4 or w[i]!=t[i]) for i in range(5))}
def show_edges(es):return ['-'.join(map(text,e)) for e in sorted(es)]
def main():
    began=time.monotonic();source=HERE/'phase6-source.tex';src=source.read_text();assert hashlib.sha256(source.read_bytes()).hexdigest()=='7a90f79db489447b0bad3019217fd369a5cc25986288247981cbe7f3462acba3'
    blocks=dict(re.findall(r'% BEGIN ([A-Z0-9-]+)\n(.*?)% END \1',src,re.S))
    ordinary=set(re.findall(r'% BEGIN C1-([0-3]{5})',src));starred=set(re.findall(r'% BEGIN FHC-([0-4]{5})',src));standard=ordinary|starred|{'00000','00001','00112'}
    def words(t):return [parse(w) for w in re.findall(r'\b[0-3]{5}\b',blocks[('FHC-' if '4' in t else 'C1-')+t])]
    def pool(t):return {edge(parse(u),parse(v)) for u,v in re.findall(r'([0-3]{5})-([0-3]{5})',blocks[f'POOL-{t}-0'])}
    def normalizer(t):
        for shift in range(5):
            for eps in (1,-1):
                for p in permutations(range(4)):
                    n=tuple(4 if t[(shift+eps*i)%5]==4 else p[t[(shift+eps*i)%5]] for i in range(5))
                    if text(n) in standard:return text(n),(shift,eps,p)
        raise AssertionError(t)
    def restore(w,g):
        shift,eps,p=g;inverse=[p.index(i) for i in range(4)];out=[None]*5
        for i in range(5):out[(shift+eps*i)%5]=inverse[w[i]]
        return tuple(out)
    rows=[]
    for t,position,new in CASES:
        source_words=words(t);C=cycle(source_words);P=pool(t);s=parse(t);s=s[:position]+(new,)+s[position+1:];nt,g=normalizer(s)
        target_words=[restore(w,g) for w in words(nt)];D=cycle(target_words);Q={edge(restore(u,g),restore(v,g)) for u,v in pool(nt)}
        assert set(source_words)==legal(parse(t)) and set(target_words)==legal(s);assert P<=C and Q<=D
        U=set(source_words)&set(target_words);F=P|Q;supports=[];scanned=Counter();profiles=Counter()
        for i,j in combinations(range(5),2):
            rest=[k for k in range(5) if k not in (i,j)];groups=defaultdict(set)
            for w in U:groups[tuple(w[k] for k in rest)].add((w[i],w[j]))
            for fixed,pairs in sorted(groups.items()):
                for size_i,size_j,kind in [(2,2,'Q4'),(2,3,'K2xK3'),(3,2,'K3xK2')]:
                    for choices_i in combinations(range(4),size_i):
                        for choices_j in combinations(range(4),size_j):
                            if not all((a,b) in pairs for a,b in product(choices_i,choices_j)):continue
                            def vertex(a,b):
                                w=[None]*5;w[i]=a;w[j]=b
                                for k,c in zip(rest,fixed):w[k]=c
                                return tuple(w)
                            H={edge(vertex(a,b),vertex(c,b)) for b in choices_j for a,c in combinations(choices_i,2)}|{edge(vertex(a,b),vertex(a,c)) for a in choices_i for b,c in combinations(choices_j,2)}
                            assert len(H)==(4 if kind=='Q4' else 9) and all(u in U and v in U and sum(a!=b for a,b in zip(u,v))==1 for u,v in H)
                            m=len(H);forbidden={e for e in H if e in F};a=sum(e in C for e in H);b=sum(e in D for e in H);f=len(forbidden);x=sum(e in C for e in forbidden);y=sum(e in D for e in forbidden);bound=a+b-m-x-y+f
                            scanned[kind]+=1;profiles[(kind,a,b,f,x,y,bound)]+=1
                            # Only one explicitly identified omitted edge can strengthen a 2/4+2/4 square.
                            # This is a candidate pattern requiring a separate structural proof, not an intersection computation.
                            omitted=[e for e in sorted(H) if e not in F and e not in C and e not in D] if kind=='Q4' and a==b==2 and bound==0 else []
                            if bound>0 or omitted:
                                supports.append({'kind':kind,'axes':[i,j],'choices':[list(choices_i),list(choices_j)],'fixed':{str(k):c for k,c in zip(rest,fixed)},'vertices':sorted(text(vertex(a,b)) for a,b in product(choices_i,choices_j)),'edges':show_edges(H),'a':a,'b':b,'m':m,'f':f,'rC':x,'rD':y,'bound_without_omissions':bound,'one_omission_bound':bound+bool(omitted),'one_common_omission':show_edges(omitted[:1]),'source_retained':show_edges(e for e in H if e in C),'target_retained':show_edges(e for e in H if e in D),'forbidden':show_edges(forbidden),'certification':'COUNT_CAPACITY' if bound>0 else 'NEEDS_STRUCTURAL_OMISSION_PROOF'})
        supports.sort(key=lambda r:(r['certification']!='COUNT_CAPACITY',r['kind']!='Q4',-r['bound_without_omissions'],-r['one_omission_bound'],r['axes'],r['vertices']))
        row={'source':t+':0','changed_position':position,'new_colour':new,'target':nt+':0','normalizer':[g[0],g[1],list(g[2])],'common_vertices':len(U),'scanned_supports':dict(scanned),'capacity_hits':sum(r['certification']=='COUNT_CAPACITY' for r in supports),'omission_candidates':sum(r['certification']!='COUNT_CAPACITY' for r in supports),'profiles':[{'kind':k[0],'a':k[1],'b':k[2],'f':k[3],'rC':k[4],'rD':k[5],'bound':k[6],'count':n} for k,n in sorted(profiles.items())],'supports':supports}
        rows.append(row)
    result={'scope':'seven prescribed phase6 HH residual selected pairs; genuine2-coordinate Cartesian supports only','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'case_count':len(rows),'capacity_covered':sum(bool(r['capacity_hits']) for r in rows),'with_omission_candidates':sum(bool(r['capacity_hits'] or r['omission_candidates']) for r in rows),'Hamilton_search':False,'actual_C_intersect_D_edges_computed':False,'K2_wrappers':False,'elapsed_seconds':time.monotonic()-began,'cases':rows}
    (HERE/'cartesian-support-results-v1.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({**{k:v for k,v in result.items() if k!='cases'},'case_summary':[{k:r[k] for k in ('source','changed_position','new_colour','target','scanned_supports','capacity_hits','omission_candidates')} for r in rows]}))
if __name__=='__main__':main()
