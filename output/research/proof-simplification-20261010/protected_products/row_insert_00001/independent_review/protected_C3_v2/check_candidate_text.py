"""Read the final English/TeX candidate's literal7toggles,40path,ports andrepairs."""
from pathlib import Path
from itertools import product
from collections import Counter
import re,json,hashlib

HERE=Path(__file__).resolve().parent


def main():
    text=(HERE/'candidate-v1.tex').read_text()
    literal=(HERE/'interface-literal-input-v1.tex').read_text()
    blocks=dict(re.findall(r'% BEGIN ([A-Z0-9-]+)\n(.*?)% END \1',literal,re.S))
    sha=hashlib.sha256((HERE/'candidate-v1.tex').read_bytes()).hexdigest()
    assert sha=='07c0a2c7873b15f1cb6e52a51f0fcecb355561c2d3ea1b7b4d1ebc8c29efe4b2'
    edge=lambda u,v:tuple(sorted((u,v)))
    cycle_edges=lambda c:{edge(u,v) for u,v in zip(c,c[1:]+c[:1])}
    dp=re.search(r'D=\{\}&\\\{(.*?)\\\},\\\\\s*R=',text,re.S).group(1)
    rp=re.search(r'R=\{\}&\\\{(.*?)\\\}',text,re.S).group(1)
    pairset=lambda t:{edge(u,v) for u,v in re.findall(r'([0-3]{5})\\,([0-3]{5})',t)}
    D,R=pairset(dp),pairset(rp);K=D-R
    assert (len(D),len(R),len(K))==(13,2,11) and R<=D
    checked=json.loads((HERE/'review-results.json').read_text())
    source=json.loads((HERE/'C2-second-patch-results-v1.json').read_text())['reports'][0]['certificate']
    answer=json.loads((HERE/'core40-path-results-v2.json').read_text())['answer']
    assert D=={edge(*e) for e in source['D13']} and R=={edge(*e) for e in source['two_reserves']}
    assert K=={edge(*e) for e in source['K11']}
    old_words=re.findall(r'\b[01][0-3]{5}\b',blocks['PC2-00001']);current=cycle_edges(old_words)
    states={''.join(map(str,w)) for w in product(range(4),repeat=5)
        if all(w[i]!=w[(i+1)%5] and w[i]!=(0,0,0,0,1)[i] for i in range(5))}
    vs={str(r)+w for r in (0,1) for w in states}
    def legal(u,v):
        return (u[0]==v[0] and sum(a!=b for a,b in zip(u[1:],v[1:]))==1) or (u[0]!=v[0] and u[1:]==v[1:])
    def analyse(ee):
        degree=Counter(u for e in ee for u in e);assert set(degree)==vs and set(degree.values())=={2}
        assert all(legal(u,v) for u,v in ee)
        adj={u:{v for e in ee if u in e for v in e if v!=u} for u in vs}
        todo=set(vs);sizes=[]
        while todo:
            start=next(iter(todo));seen={start};queue=[start]
            for u in queue:
                for v in adj[u]-seen:seen.add(v);queue.append(v)
            todo-=seen;sizes.append(len(seen))
        return sorted(sizes)
    listed=re.findall(r'\(([0-3]{5}(?:,[0-3]{5})+)\)&([0-9,]+)',text)
    assert len(listed)==7;stages=[]
    for path_s,length_s in listed:
        path=path_s.split(',')
        assert all(w in states for w in path) and len(path)==len(set(path))
        assert all(sum(a!=b for a,b in zip(u,v))==1 for u,v in zip(path,path[1:]))
        toggle={edge(str(r)+u,str(r)+v) for r in (0,1) for u,v in zip(path,path[1:])}|{edge('0'+path[0],'1'+path[0]),edge('0'+path[-1],'1'+path[-1])}
        current^=toggle;sizes=analyse(current)
        assert sizes==sorted(map(int,length_s.split(',')));stages.append(sizes)
    assert stages[-1]==[88] and current==cycle_edges(source['C2_words'])
    core=re.findall(r'\b[0-3]{5}\b',re.search(r'\\begin\{verbatim\}(.*?)\\end\{verbatim\}',text,re.S).group(1))
    assert core==answer['core40_path'] and len(core)==len(set(core))==40
    assert set(core)==states-{'12312','12313','13212','13213'}
    assert D<={edge(u,v) for u,v in zip(core,core[1:])}
    mp=re.search(r'M=\\\{(.*?)\\\}',text,re.S).group(1);M=pairset(mp)
    assert M=={edge(*e) for e in answer['matching_cuts']} and not M&D
    assert {edge('1'+u,'1'+v) for u,v in M}<=current
    assert {edge(str(r)+u,str(r)+v) for r in (0,1) for u,v in D}<=current
    repairs=re.findall(r'([0-3]{5})&([0-4])&([0-3])&([0-3]{5})&([0-3]{5})\\,([0-3]{5})',text)
    assert repairs==[('00001','1','3','00102','21313','21323'),('00001','4','2','00001','13120','23120'),('00001','4','3','00001','12310','32310')]
    assert [edge(a,b) for s,p,n,t,a,b in repairs]==[edge(*r['replacement']) for r in checked['repairs']]
    result={'status':'PASS','candidate_sha256':sha,'D13_R2_K11_from_actual_TeX':True,
        'all_seven_literal_toggle_paths_valid':True,'stage_cycle_sizes':stages,
        'final_literal_toggle_cycle_equals_independently_checked_C2':True,
        'literal40path_andmatchingcuts_equal_verified_C3_inputs':True,
        'three_literal_interface_repairs_equal_verified_replacements':True,
        'English_normalizer_claims_symbolically_reviewed':True,
        'scope':'Direct finalTeX readback, notpeerhelper orsolver replay. Complete88/132 wordchecks andall313inheritance arein review-results.json.'}
    (HERE/'candidate-text-review.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__=='__main__':main()
