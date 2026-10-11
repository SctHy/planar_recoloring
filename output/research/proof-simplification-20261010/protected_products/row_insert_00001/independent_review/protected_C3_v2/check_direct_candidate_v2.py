"""Final direct88-word TeX readback, independently deriving its132-cycle."""
from pathlib import Path
from itertools import product
import json,re,hashlib

HERE=Path(__file__).resolve().parent


def main():
    text=(HERE/'candidate-v2.tex').read_text();sha=hashlib.sha256((HERE/'candidate-v2.tex').read_bytes()).hexdigest()
    assert sha=='94a3d46d7c3c7c65984216924ebd72f315314833a2f9d885679ad1900455d6a4'
    seed=json.loads((HERE/'C2-second-patch-results-v1.json').read_text())['reports'][0]['certificate']
    answer=json.loads((HERE/'core40-path-results-v2.json').read_text())['answer']
    verified=json.loads((HERE/'review-results.json').read_text())
    edge=lambda u,v:tuple(sorted((u,v)))
    edges=lambda c:{edge(u,v) for u,v in zip(c,c[1:]+c[:1])}
    pairset=lambda t:{edge(u,v) for u,v in re.findall(r'([0-3]{5})\\,([0-3]{5})',t)}
    D=pairset(re.search(r'D=\{\}&\\\{(.*?)\\\},\\\\\s*R=',text,re.S).group(1))
    R=pairset(re.search(r'R=\{\}&\\\{(.*?)\\\}',text,re.S).group(1));K=D-R
    assert (len(D),len(R),len(K))==(13,2,11) and D=={edge(*e) for e in seed['D13']}
    assert R=={edge(*e) for e in seed['two_reserves']} and K=={edge(*e) for e in seed['K11']}
    verbatims=re.findall(r'\\begin\{verbatim\}(.*?)\\end\{verbatim\}',text,re.S);assert len(verbatims)==2
    c2=re.findall(r'\b[01][0-3]{5}\b',verbatims[0]);core=re.findall(r'\b[0-3]{5}\b',verbatims[1])
    assert c2==seed['C2_words'] and core==answer['core40_path']
    states={''.join(map(str,w)) for w in product(range(4),repeat=5)
        if all(w[i]!=w[(i+1)%5] and w[i]!=(0,0,0,0,1)[i] for i in range(5))}
    assert len(c2)==len(set(c2))==88 and set(c2)=={str(r)+w for r in (0,1) for w in states}
    BB={'12312','12313','13212','13213'}
    assert len(core)==len(set(core))==40 and set(core)==states-BB and (core[0],core[-1])==('13210','13230')
    legal=lambda u,v:(u[0]==v[0] and sum(a!=b for a,b in zip(u[1:],v[1:]))==1) or (abs(int(u[0])-int(v[0]))==1 and u[1:]==v[1:])
    assert all(legal(u,v) for u,v in edges(c2))
    assert all(sum(a!=b for a,b in zip(u,v))==1 for u,v in zip(core,core[1:]))
    assert D<={edge(u,v) for u,v in zip(core,core[1:])}
    M=pairset(re.search(r'M=\\\{(.*?)\\\}',text,re.S).group(1))
    assert M=={edge(*e) for e in answer['matching_cuts']} and not M&D and len(set().union(*map(set,M)))==6
    assert {edge('1'+u,'1'+v) for u,v in M}<=edges(c2)
    paths=[['12312','12313'],['13212','13213'],core]
    by_pair={edge(p[0],p[-1]):p for p in paths};c3=[];count=0
    for u,v in zip(c2,c2[1:]+c2[:1]):
        c3.append(u)
        if u[0]==v[0]=='1' and edge(u[1:],v[1:]) in M:
            p=by_pair[edge(u[1:],v[1:])]
            if p[0]!=u[1:]:p=p[::-1]
            c3.extend('2'+w for w in p);count+=1
    assert count==3 and c3==answer['derived_C3_words']
    assert len(c3)==len(set(c3))==132 and set(c3)=={str(r)+w for r in (0,1,2) for w in states}
    assert all(legal(u,v) for u,v in edges(c3))
    rows=lambda ee,r:{edge(u[1:],v[1:]) for u,v in ee if u[0]==v[0]==str(r)}
    assert all(D<=rows(edges(c2),r) for r in (0,1)) and all(D<=rows(edges(c3),r) for r in (0,1,2))
    table=re.findall(r'([0-3]{5})&([0-4])&([0-3])&([0-3]{5})&([0-3]{5})\\,([0-3]{5})',text)
    assert table==[('00001','1','3','00102','21313','21323'),('00001','4','2','00001','13120','23120'),('00001','4','3','00001','12310','32310')]
    assert [edge(a,b) for s,p,n,t,a,b in table]==[edge(*r['replacement']) for r in verified['repairs']]
    critical={edge('31212','31232'),edge('12132','32132'),edge('21313','21323'),edge('13123','23123')};assert critical<=K
    result={'status':'PASS','candidate_v2_sha256':sha,'literal88word_C2_equals_verified_seed':True,
        'literal40word_path_equals_verified_core_path':True,'literalD13_R2_K11_verified':True,
        'all_three_actual_row1_matchingcuts_verified':True,'derived132_C3_word_for_word_verified':True,
        'all88_and132_productstates_unique_and_complete':True,'all_cyclic_productedges_legal':True,
        'all13_ports_in_eachrow_ofbothseeds':True,
        'actual_three_table_repairs_andfourconstantcanonicalmemberships_verified':True,
        'all313_inheritance_uses_exact_same_K_andrepairs_as_independent_fullreview':True,
        'scope':'FinaldirectTeX readback andfixed132word derivation only; nosearch; priorindependent24affectedwitness audit suppliesall313inheritance.'}
    (HERE/'direct-candidate-v2-review.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__=='__main__':main()
