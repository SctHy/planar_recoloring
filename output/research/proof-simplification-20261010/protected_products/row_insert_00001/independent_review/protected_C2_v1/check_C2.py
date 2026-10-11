"""Independent fixed-certificate replay of the protected88-state C2; no search."""
from pathlib import Path
from itertools import product,combinations
from collections import Counter
import re,json,hashlib

HERE=Path(__file__).resolve().parent


def main():
    answer=json.loads((HERE/'protected-C2-switch-results-v1.json').read_text())['certificate']
    source=json.loads((HERE/'local-switch-results-v1.json').read_text())['explicit_variants'][0]
    olddata=json.loads((HERE/'obstruction-results-v1.json').read_text())
    text=(HERE/'original-literal-input.tex').read_text()
    blocks=dict(re.findall(r'% BEGIN ([A-Z0-9-]+)\n(.*?)% END \1',text,re.S))
    edge=lambda u,v:tuple(sorted((u,v)))
    cycle_edges=lambda c:{edge(u,v) for u,v in zip(c,c[1:]+c[:1])}
    oldc=re.findall(r'\b[01][0-3]{5}\b',blocks['PC2-00001'])
    states={''.join(map(str,w)) for w in product(range(4),repeat=5)
        if all(w[i]!=w[(i+1)%5] and w[i]!=(0,0,0,0,1)[i] for i in range(5))}
    Aedges=sorted(edge(u,v) for u,v in combinations(sorted(states),2) if sum(a!=b for a,b in zip(u,v))==1)
    assert Aedges==[edge(*e) for e in olddata['edges']] and len(Aedges)==74
    product_vertices={str(r)+w for r in (0,1) for w in states}
    product_edges={edge(str(r)+u,str(r)+v) for r in (0,1) for u,v in Aedges}|{edge('0'+w,'1'+w) for w in states}
    oldD={edge(u,v) for u,v in re.findall(r'([0-3]{5})-([0-3]{5})',blocks['COMMON-00001'])}
    oldpool={edge(u,v) for u,v in re.findall(r'([0-3]{5})-([0-3]{5})',blocks['POOL-00001-0'])}
    Kstar=(oldD-oldpool)-{edge('12313','12323')}|{edge('13120','23120')}
    R={edge(*e) for e in answer['two_reserves']};D=Kstar|R
    assert len(Kstar)==12 and len(R)==2 and not Kstar&R and len(D)==14
    assert D=={edge(*e) for e in answer['D14']}
    required={edge(str(r)+u,str(r)+v) for r in (0,1) for u,v in D}|{edge('1'+u,'1'+v) for u,v in [('12312','12313'),('13212','13213')]}
    def components(ee):
        degree=Counter(u for e in ee for u in e)
        assert set(degree)==product_vertices and set(degree.values())=={2} and ee<=product_edges
        adjacency={u:{v for e in ee if u in e for v in e if v!=u} for u in product_vertices}
        todo=set(product_vertices);sizes=[]
        while todo:
            start=next(iter(todo));seen={start};queue=[start]
            for u in queue:
                for v in adjacency[u]-seen:seen.add(v);queue.append(v)
            todo-=seen;sizes.append(len(seen))
        return sorted(sizes)
    current=cycle_edges(oldc);stage_sizes=[components(current)]
    for change in source['changes']:
        remove={edge(*e) for e in change['remove']};add={edge(*e) for e in change['add']}
        assert remove<=current and not add&current
        current=(current-remove)|add;stage_sizes.append(components(current))
    assert current==set().union(*(cycle_edges(c) for c in source['result_cycles']))
    assert required<=current
    switches=[];rectangle_sizes=[components(current)]
    for which in answer['rectangle_switch_indexes']:
        u,v=Aedges[which]
        horizontal={edge('0'+u,'0'+v),edge('1'+u,'1'+v)}
        vertical={edge('0'+u,'1'+u),edge('0'+v,'1'+v)}
        present=current&(horizontal|vertical)
        assert present in (horizontal,vertical) and not present&required
        remove=present;add=(horizontal|vertical)-present
        current=(current-remove)|add
        assert required<=current
        rectangle_sizes.append(components(current))
        switches.append({'index':which,'A_edge':[u,v],'remove':[list(e) for e in sorted(remove)],'add':[list(e) for e in sorted(add)]})
    words=answer['C2_words']
    assert len(words)==len(set(words))==88 and set(words)==product_vertices
    assert cycle_edges(words)==current=={edge(*e) for e in answer['C2_edges']}
    assert components(current)==[88] and required<=current
    result={'status':'PASS','generated_A_vertices':44,'generated_A_edges':74,
        'C2_words':88,'C2_single_cycle':True,'all88_product_states_exactly_once':True,
        'all_cyclic_steps_legal':True,'D14_count':14,'all14_D_edges_retained_in_both_rows':True,
        'both_YY_edges_in_row_digit1':True,'initial_three_local_changes_cycle_sizes':stage_sizes,
        'rectangle_stage_cycle_sizes':rectangle_sizes,'rectangle_switches':switches,
        'certificate_edges_equal_replayed_moves_and_C2_words':True,
        'next_insertion_obstruction_does_not_negate_C2_existence':True,
        'input_sha256':hashlib.sha256((HERE/'original-literal-input.tex').read_bytes()).hexdigest(),
        'certificate_sha256':hashlib.sha256((HERE/'protected-C2-switch-results-v1.json').read_bytes()).hexdigest(),
        'source_factor_sha256':hashlib.sha256((HERE/'local-switch-results-v1.json').read_bytes()).hexdigest(),
        'scope':'Literal fixed-seed and explicit-move replay only; no search, no protected C3 claimed.'}
    (HERE/'review-results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__=='__main__':main()
