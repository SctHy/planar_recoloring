"""Direct primary-source replay of the seven frozen square certificates."""
from pathlib import Path
from itertools import product,permutations
import json,re,hashlib
HERE=Path(__file__).resolve().parent
def word(w):return tuple(map(int,w))
def edge(u,v):return tuple(sorted((u,v)))
def cyclic(ws):return {edge(u,v) for u,v in zip(ws,ws[1:]+ws[:1])}
def main():
    source=HERE/'phase6-source.tex';s=source.read_text();blocks=dict(re.findall(r'% BEGIN ([A-Z0-9-]+)\n(.*?)% END \1',s,re.S))
    types=set(re.findall(r'% BEGIN (?:C1|FHC)-([0-4]{5})',s))|{'00000','00001','00112'}
    def entries(t):return [word(w) for w in re.findall(r'\b[0-3]{5}\b',blocks[('FHC-' if '4' in t else 'C1-')+t])]
    def pool(t):return {edge(word(a),word(b)) for a,b in re.findall(r'([0-3]{5})-([0-3]{5})',blocks[f'POOL-{t}-0'])}
    def norm(t):
        for shift in range(5):
            for eps in (1,-1):
                for p in permutations(range(4)):
                    n=''.join('4' if t[(shift+eps*i)%5]==4 else str(p[t[(shift+eps*i)%5]]) for i in range(5))
                    if n in types:return n,(shift,eps,p)
        raise AssertionError(t)
    def inv(w,g):
        shift,eps,p=g;out=[0]*5
        for i in range(5):out[(shift+eps*i)%5]=p.index(w[i])
        return tuple(out)
    rows=[]
    specifications=[('00014',0,3,0,[word(w) for w in ('23101','23131','23201','23231')],(3,2)),('01014',0,2,0,[word(w) for w in ('10302','12302','30302','32302')],(3,3)),('01014',0,3,0,[word(w) for w in ('10203','13203','20203','23203')],(2,3)),('01014',2,2,0,[word(w) for w in ('10320','12320','30320','32320')],(3,3)),('01124',2,2,0,[word(w) for w in ('12012','12032','32012','32032')],(2,3)),('01204',2,0,0,[word(w) for w in ('10132','12132','30132','32132')],(3,2)),('00123',0,3,2,[word(w) for w in ('21210','21230','23210','23230')],(2,2))]
    for t,i,c,omissions,V,counts in specifications:
        st=word(t);target=st[:i]+(c,)+st[i+1:];nt,g=norm(target);W=entries(t);Z=[inv(w,g) for w in entries(nt)];C=cyclic(W);D=cyclic(Z);F=pool(t)|{edge(inv(a,g),inv(b,g)) for a,b in pool(nt)}
        assert set(V)<=set(W) and set(V)<=set(Z)
        H={edge(a,b) for a in V for b in V if sum(x!=y for x,y in zip(a,b))==1};assert len(H)==4
        a=sum(e in C for e in H);b=sum(e in D for e in H);assert (a,b)==counts and not any(e in F for e in H)
        if t=='00123':
            T=[word(w) for w in ('13010','13012','13210','13212')];J={edge(a,b) for a in T for b in T if sum(x!=y for x,y in zip(a,b))==1}
            assert nt=='00123' and g==(0,-1,(3,2,1,0)) and {inv(w,g) for w in V}==set(T)
            for sequence in [('21210','23210','23230'),('13010','13210','13212')]:
                assert all(edge(word(u),word(v)) in C for u,v in zip(sequence,sequence[1:]))
            for isolated,expected in [('21230',{'31230','21231'}),('13012',{'13032','12012'})]:
                index=W.index(word(isolated));neighbours={''.join(map(str,W[(index-1)%len(W)])),''.join(map(str,W[(index+1)%len(W)]))};assert neighbours==expected
            assert inv(word('23210'),g)==word('13210') and inv(word('21230'),g)==word('13012')
            assert not any(e in pool(t) for e in H|J)
            corner=word('21230');incident=[e for e in H if corner in e];assert len(incident)==2
            assert all(e not in C and e not in D for e in incident)
        rows.append({'source':t,'position':i,'new_colour':c,'target':nt,'normalizer':[g[0],g[1],list(g[2])],'vertices':[''.join(map(str,w)) for w in V],'source_retention':a,'target_retention':b,'pool_union_edges':0,'structural_common_corner_omissions':omissions,'lower_bound':a+b-4+omissions})
    result={'status':'PASS_SEVEN_FIXED_SQUARE_CERTIFICATES','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'candidate_sha256':hashlib.sha256((HERE/'square-capacity-candidate-v1.tex').read_bytes()).hexdigest(),'cases':rows,'all_bounds_positive':all(r['lower_bound']>0 for r in rows),'Hamilton_search':False,'actual_cycle_edge_intersection_computed':False,'scope':'seven fixed selected pairs; source cycle restrictions and prescribed first maps only'}
    (HERE/'selected-certificate-review-v1.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='cases'}))
if __name__=='__main__':main()
