"""Check two fixed local three-edge substitutions only, with no search."""
from pathlib import Path
from collections import Counter
import re,json,hashlib

HERE=Path(__file__).resolve().parent


def main():
    text=(HERE/'literal-input.tex').read_text()
    blocks=dict(re.findall(r'% BEGIN ([A-Z0-9-]+)\n(.*?)% END \1',text,re.S))
    edge=lambda u,v:tuple(sorted((u,v)))
    c2=re.findall(r'\b[01][0-3]{5}\b',blocks['PC2-00001'])
    original={edge(u,v) for u,v in zip(c2,c2[1:]+c2[:1])};vs=set(c2)
    D={edge(u,v) for u,v in re.findall(r'([0-3]{5})-([0-3]{5})',blocks['COMMON-00001'])}
    assert len(vs)==len(c2)==88 and len(D)==19
    rows=lambda ee,r:{edge(u[1:],v[1:]) for u,v in ee if u[0]==v[0]==str(r)}
    assert all(D<=rows(original,r) for r in (0,1))
    def move(a,b,c):
        remove={edge(str(r)+a,str(r)+b) for r in (0,1)}|{edge('0'+c,'1'+c)}
        add={edge(str(r)+b,str(r)+c) for r in (0,1)}|{edge('0'+a,'1'+a)}
        return remove,add
    moves=[move('12310','12313','12312'),move('13232','13212','13213')]
    def apply(ee,which):
        remove,add=moves[which]
        assert remove<=ee and not add&ee
        assert all(not (u[0]==v[0] and edge(u[1:],v[1:]) in D) for u,v in remove)
        return (ee-remove)|add
    def analyse(ee):
        deg=Counter(u for e in ee for u in e);assert set(deg)==vs and set(deg.values())=={2}
        assert all((u[0]==v[0] and sum(a!=b for a,b in zip(u[1:],v[1:]))==1) or (u[0]!=v[0] and u[1:]==v[1:]) for u,v in ee)
        adjacency={u:{v for e in ee if u in e for v in e if v!=u} for u in vs}
        components=[];todo=set(vs)
        while todo:
            start=min(todo);previous=None;current=start;cycle=[]
            while current not in cycle:
                cycle.append(current);nexts=adjacency[current]-({previous} if previous is not None else set())
                nxt=min(nexts);previous,current=current,nxt
            assert current==start
            todo-=set(cycle);components.append(cycle)
        return {'cycle_components':len(components),'cycle_sizes':sorted(map(len,components)),
            'cycles':components,'D19_preserved_both_rows':all(D<=rows(ee,r) for r in (0,1)),
            'two_YY_edges_each_row':all({edge('12312','12313'),edge('13212','13213')}<=rows(ee,r) for r in (0,1)),
            'replacement_edges_rows':{u+'-'+v:[edge(u,v) in rows(ee,r) for r in (0,1)] for u,v in [('13120','23120'),('21320','31320')]}}
    after1=apply(original,0);after2=apply(original,1);both=apply(after1,1)
    assert both==apply(after2,0)
    result={'status':'complete','old':analyse(original),'after_first':analyse(after1),'after_second':analyse(after2),'after_both':analyse(both),
        'moves':[{'removed':[list(e) for e in sorted(r)],'added':[list(e) for e in sorted(a)]} for r,a in moves],
        'moves_commute':True,'input_sha256':hashlib.sha256((HERE/'literal-input.tex').read_bytes()).hexdigest(),
        'scope':'Only two specified fixed-edge substitutions, with exact degree and component checks; no seed search.'}
    (HERE/'move-results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:({kk:vv for kk,vv in v.items() if kk!='cycles'} if isinstance(v,dict) else v) for k,v in result.items()}))


if __name__=='__main__':main()
