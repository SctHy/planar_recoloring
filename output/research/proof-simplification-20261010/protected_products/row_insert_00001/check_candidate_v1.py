"""Literal readback and full reconstruction of the frozen candidate."""
from pathlib import Path
from itertools import combinations, product
import hashlib,json,re

HERE=Path(__file__).resolve().parent

def edge(u,v):return tuple(sorted((u,v)))

def components(es):
    adj={}
    for u,v in es:adj.setdefault(u,[]).append(v);adj.setdefault(v,[]).append(u)
    assert len(adj)==88 and all(len(ns)==2 for ns in adj.values())
    unseen=set(adj);cycles=[]
    while unseen:
        start=min(unseen);prev=None;u=start;words=[]
        while not words or u!=start:
            words.append(u);unseen.remove(u);v=next(v for v in sorted(adj[u]) if v!=prev);prev,u=u,v
        cycles.append(words)
    return cycles

def main():
    candidate=HERE/'candidate-v1.tex';text=candidate.read_text()
    Dblock=text.split('D={}&')[1].split('R={}&')[0]
    D={edge(a,b) for a,b in re.findall(r'([0-3]{5})\\,([0-3]{5})',Dblock)}
    Rblock=text.split('R={}&')[1].split('\\qquad K=')[0]
    R={edge(a,b) for a,b in re.findall(r'([0-3]{5})\\,([0-3]{5})',Rblock)}
    assert len(D)==13 and len(R)==2 and R<=D
    K=D-R
    tblock=text.split('cycle lengths after the toggle')[1].split('The final graph')[0]
    table=re.findall(r'\(([0-3]{5}(?:,[0-3]{5})+)\)&([0-9,]+)',tblock)
    assert len(table)==7
    paths=[p.split(',') for p,_ in table]
    core_path=re.findall(r'\b[0-3]{5}\b',text.split('\\begin{verbatim}')[1].split('\\end{verbatim}')[0]);assert len(core_path)==40
    V=sorted(''.join(map(str,v)) for v in product(range(4),repeat=5)
             if all(v[i]!=v[(i+1)%5] and str(v[i])!='00001'[i] for i in range(5)))
    E={edge(u,v) for u,v in combinations(V,2) if sum(a!=b for a,b in zip(u,v))==1}
    assert len(V)==44 and len(E)==74 and D<=E
    original=HERE/'original-literal-input.tex';oldtext=original.read_text()
    def block(n):return re.search('% BEGIN '+n+'\n(.*?)% END '+n,oldtext,re.S).group(1)
    words=re.findall(r'\b[01][0-3]{5}\b',block('PC2-00001'));assert len(words)==88
    es={edge(a,b) for a,b in zip(words,words[1:]+words[:1])}
    stages=[]
    for path,(_,literal_sizes) in zip(paths,table):
        assert all(edge(u,v) in E for u,v in zip(path,path[1:]))
        toggle={edge(r+u,r+v) for r in '01' for u,v in zip(path,path[1:])}|{edge('0'+path[0],'1'+path[0]),edge('0'+path[-1],'1'+path[-1])}
        es^=toggle;cs=components(es);sizes=[len(c) for c in cs]
        assert sorted(sizes)==sorted(map(int,literal_sizes.split(',')))
        stages.append({'base_path':path,'component_sizes':sizes})
    assert len(cs)==1 and set(cs[0])=={r+v for r in '01' for v in V}
    assert all(edge(r+u,r+v) in es for r in '01' for u,v in D)
    M={('12312','12313'),('13212','13213'),('13210','13230')}
    assert len({v for e in M for v in e})==6 and not M&D
    assert all(edge('1'+u,'1'+v) in es for u,v in M)
    core=set(V)-{'12312','12313','13212','13213'}
    assert set(core_path)==core and len(core_path)==len(core)
    P_edges={edge(u,v) for u,v in zip(core_path,core_path[1:])}
    assert core_path[0]=='13210' and core_path[-1]=='13230' and D<=P_edges<=E
    replacement={('12312','12313'):['12312','12313'],('13212','13213'):['13212','13213'],('13210','13230'):core_path}
    derived=[]
    for a,b in zip(cs[0],cs[0][1:]+cs[0][:1]):
        derived.append(a);key=edge(a[1:],b[1:])
        if a[0]==b[0]=='1' and key in M:
            path=replacement[key];path=path if path[0]==a[1:] else path[::-1]
            assert path[-1]==b[1:];derived.extend('2'+v for v in path)
    assert len(derived)==132 and set(derived)=={r+v for r in '012' for v in V}
    C3={edge(a,b) for a,b in zip(derived,derived[1:]+derived[:1])}
    assert len(C3)==132
    for a,b in C3:
        assert (a[0]==b[0] and edge(a[1:],b[1:]) in E) or (abs(int(a[0])-int(b[0]))==1 and a[1:]==b[1:])
    assert all(edge(r+u,r+v) in C3 for r in '012' for u,v in D)
    known=json.loads((HERE/'core40-path-results-v2.json').read_text())['answer']
    assert C3=={edge(a,b) for a,b in zip(known['derived_C3_words'],known['derived_C3_words'][1:]+known['derived_C3_words'][:1])}
    oldD={edge(a,b) for a,b in re.findall(r'([0-3]{5})-([0-3]{5})',block('COMMON-00001'))}
    oldR={edge(a,b) for a,b in re.findall(r'([0-3]{5})-([0-3]{5})',block('POOL-00001-0'))}
    assert R<=oldR and K==(oldD-oldR)-{('12313','12323'),('13230','23230')}|{('13120','23120')}
    interface=json.loads((HERE/'second-K-patch-results-v1.json').read_text())['reports'][4]
    assert K==set(map(tuple,interface['K11'])) and not interface['individual_empty_interfaces'] and interface['all30_constant_images_keep_old_witness']
    output={'status':'PASS','candidate_sha256':hashlib.sha256(candidate.read_bytes()).hexdigest(),
            'original_input_sha256':hashlib.sha256(original.read_bytes()).hexdigest(),
            'V44_count':len(V),'E74_count':len(E),'D13':sorted(D),'pool2':sorted(R),'K11':sorted(K),
            'seven_toggle_reconstruction':stages,'C2_words':cs[0],'core40_path':core_path,'matching_cuts':sorted(M),
            'derived_C3_words':derived,'all132_states_once':True,'all13_ports_in_every_row':True,
            'full313_membership_certificate_matches_candidate_K':True,
            'limitations':['The auxiliary set changes: old K12 is not retained. Main manuscript remains untouched.']}
    (HERE/'candidate-readback-v1.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k not in ('C2_words','derived_C3_words','core40_path')}))

if __name__=='__main__':main()
