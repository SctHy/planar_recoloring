"""Independent fixed C2/core40/C3 and inherited-interface reader; no helpers/search."""
from pathlib import Path
from itertools import product,combinations,permutations
from collections import Counter
import re,json,hashlib

HERE=Path(__file__).resolve().parent
STANDARD=('00000','00001','00011','00012','00101','00102','00112','00121','00123','01012','01023','00004','00014','00104','00114','00124','01014','01024','01104','01124','01204','01234')


def main():
    seed_data=json.loads((HERE/'C2-second-patch-results-v1.json').read_text())
    seed=seed_data['reports'][0]['certificate']
    answer=json.loads((HERE/'core40-path-results-v2.json').read_text())['answer']
    first=json.loads((HERE/'protected-C2-switch-results-v1.json').read_text())['certificate']
    text=(HERE/'interface-literal-input-v1.tex').read_text()
    blocks=dict(re.findall(r'% BEGIN ([A-Z0-9-]+)\n(.*?)% END \1',text,re.S))
    edge=lambda u,v:tuple(sorted((u,v)))
    cycle_edges=lambda c:{edge(u,v) for u,v in zip(c,c[1:]+c[:1])}
    pairs=lambda tag:{edge(u,v) for u,v in re.findall(r'([0-3]{5})-([0-3]{5})',blocks[tag])}
    states={''.join(map(str,w)) for w in product(range(4),repeat=5)
        if all(w[i]!=w[(i+1)%5] and w[i]!=(0,0,0,0,1)[i] for i in range(5))}
    Aedges=sorted(edge(u,v) for u,v in combinations(sorted(states),2) if sum(a!=b for a,b in zip(u,v))==1)
    assert len(states)==44 and len(Aedges)==74
    oldK=pairs('COMMON-00001')-pairs('POOL-00001-0')
    deleted={edge('12313','12323'),edge('13230','23230')}
    K=(oldK-deleted)|{edge('13120','23120')}
    R={edge('21210','21213'),edge('21230','31230')};D=K|R
    assert len(oldK)==12 and deleted<=oldK and len(K)==11 and len(D)==13 and not K&R
    assert K=={edge(*e) for e in seed['K11']}
    assert D=={edge(*e) for e in seed['D13']}=={edge(*e) for e in answer['D13']}
    assert R=={edge(*e) for e in seed['two_reserves']}=={edge(*e) for e in answer['two_reserves']}
    product_edges={edge(str(r)+u,str(r)+v) for r in (0,1) for u,v in Aedges}|{edge('0'+w,'1'+w) for w in states}
    product_vertices={str(r)+w for r in (0,1) for w in states}
    cuts={edge('12312','12313'),edge('13212','13213'),edge('13210','13230')}
    required={edge(str(r)+u,str(r)+v) for r in (0,1) for u,v in D}|{edge('1'+u,'1'+v) for u,v in cuts}
    def components(ee):
        deg=Counter(u for e in ee for u in e)
        assert set(deg)==product_vertices and set(deg.values())=={2} and ee<=product_edges
        adj={u:{v for e in ee if u in e for v in e if v!=u} for u in product_vertices}
        todo=set(product_vertices);sizes=[]
        while todo:
            start=next(iter(todo));seen={start};queue=[start]
            for u in queue:
                for v in adj[u]-seen:seen.add(v);queue.append(v)
            todo-=seen;sizes.append(len(seen))
        return sorted(sizes)
    current=cycle_edges(first['C2_words']);replay_sizes=[components(current)]
    change=seed['first_local_change'];remove={edge(*e) for e in change['removed']};add={edge(*e) for e in change['added']}
    assert remove<=current and not add&current
    current=(current-remove)|add;assert required<=current;replay_sizes.append(components(current))
    assert seed['rectangle_switch_base_edges']==[list(Aedges[i]) for i in seed['rectangle_switch_indexes']]
    for i in seed['rectangle_switch_indexes']:
        u,v=Aedges[i];h={edge('0'+u,'0'+v),edge('1'+u,'1'+v)};vertical={edge('0'+u,'1'+u),edge('0'+v,'1'+v)}
        present=current&(h|vertical);assert present in (h,vertical) and not present&required
        current=(current-present)|((h|vertical)-present);assert required<=current
        replay_sizes.append(components(current))
    c2=seed['C2_words'];assert len(c2)==len(set(c2))==88 and set(c2)==product_vertices
    assert cycle_edges(c2)==current=={edge(*e) for e in seed['C2_edges']} and components(current)==[88]
    core=answer['core40_path'];BB={'12312','12313','13212','13213'}
    assert len(core)==len(set(core))==40 and set(core)==states-BB
    assert (core[0],core[-1])==('13210','13230') and edge(*answer['cut'])==edge(core[0],core[-1])
    path_edges={edge(u,v) for u,v in zip(core,core[1:])}
    assert path_edges<=set(Aedges) and D<=path_edges
    paths=[['12312','12313'],['13212','13213'],core]
    match={edge(p[0],p[-1]) for p in paths}
    assert match==cuts=={edge(*e) for e in answer['matching_cuts']}
    assert len(set().union(*map(set,match)))==6 and not match&D
    assert {edge('1'+u,'1'+v) for u,v in match}<=current
    by_pair={edge(p[0],p[-1]):p for p in paths};derived=[];count=0
    for u,v in zip(c2,c2[1:]+c2[:1]):
        derived.append(u)
        if u[0]==v[0]=='1' and edge(u[1:],v[1:]) in match:
            p=by_pair[edge(u[1:],v[1:])]
            if p[0]!=u[1:]:p=p[::-1]
            assert (p[0],p[-1])==(u[1:],v[1:]);derived.extend('2'+w for w in p);count+=1
    assert count==3 and derived==answer['derived_C3_words']
    assert len(derived)==len(set(derived))==132 and set(derived)=={str(r)+w for r in (0,1,2) for w in states}
    e3=cycle_edges(derived)
    assert all((u[0]==v[0] and edge(u[1:],v[1:]) in Aedges) or (abs(int(u[0])-int(v[0]))==1 and u[1:]==v[1:]) for u,v in e3)
    rows=lambda ee,r:{edge(u[1:],v[1:]) for u,v in ee if u[0]==v[0]==str(r)}
    assert all(D<=rows(current,r) for r in (0,1)) and all(D<=rows(e3,r) for r in (0,1,2))
    def norm(boundary):
        for s in range(5):
            for eps in (1,-1):
                for p in permutations(range(4)):
                    w=''.join(str(p[int(boundary[(s+eps*i)%5])]) for i in range(5))
                    if w in STANDARD:return w,(s,eps,p)
        raise AssertionError(boundary)
    def transform(w,g):
        s,eps,p=g;return ''.join(str(p[int(w[(s+eps*i)%5])]) for i in range(5))
    def restore(w,g):
        s,eps,p=g;inv={str(p[c]):str(c) for c in range(4)};z=['']*5
        for i,c in enumerate(w):z[(s+eps*i)%5]=inv[c]
        return ''.join(z)
    records=re.findall(r'([0-4]{5}:[01])\s+([0-4])\s+([0-3])\s+([0-4]{5}:[01])\s+([0-3]{5})-([0-3]{5})',blocks['INTERFACES-ALL']);assert len(records)==283
    damaged=[];affected=0
    for source,pos,new,target,u,v in records:
        if source!='00001:0' and target!='00001:0':continue
        affected+=1;pos=int(pos);boundary=list(source[:5]);boundary[pos]=new
        nt,g=norm(''.join(boundary));assert nt==target[:5]
        if (source=='00001:0' and edge(u,v) in deleted) or (target=='00001:0' and edge(transform(u,g),transform(v,g)) in deleted):
            damaged.append((source,pos,int(new),target,g))
    assert [(s,p,n,t) for s,p,n,t,g in damaged]==[('00001:0',1,3,'00102:0'),('00001:0',4,2,'00001:0'),('00001:0',4,3,'00001:0')]
    cycle_other=re.findall(r'\b[0-3]{5}\b',blocks['C1-00102']);Kother=cycle_edges(cycle_other)-pairs('POOL-00102-0')
    repairs=[edge('21313','21323'),edge('13120','23120'),edge('12310','32310')];repair_details=[]
    for (source,pos,new,target,g),witness in zip(damaged,repairs):
        targetK=K if target=='00001:0' else Kother
        common=K&{edge(restore(u,g),restore(v,g)) for u,v in targetK};assert witness in common
        repair_details.append({'position':pos,'new_excluded':new,'target':target,'replacement':list(witness),'common_edges':[list(e) for e in sorted(common)]})
    critical={edge('31212','31232'),edge('12132','32132'),edge('21313','21323'),edge('13123','23123')};assert critical<=K
    result={'status':'PASS','generated_local_states':44,'generated_local_edges':74,
        'new_C2_words':88,'new_C2_single_Hamilton_cycle':True,'new_C2_fixed_move_cycle_sizes':replay_sizes,
        'core_path_words':40,'core_path_endpoints':['13210','13230'],'core_path_contains_all13_D_edges':True,
        'row1_matching_cuts':[list(e) for e in sorted(match)],'all_cuts_present_disjoint_and_unprotected':True,
        'derived_C3_words':132,'derived_C3_word_for_word_equals_supplied':True,
        'all132_product_states_exactly_once':True,'all132_cyclic_product_steps_legal':True,
        'all13_D_edges_retained_in_every_row_of_both_seeds':True,'new_K11_exact_oldK_minus_h_minus_k3_plus_g':True,
        'all313_interfaces_inherited_with_exactly_three_individual_repairs':True,
        'affected_old_individual_records_checked':affected,'remaining_old_records_inherited':280,'repairs':repair_details,
        'six_constant_families_preserved_by_four_critical_target_edges':True,
        'input_sha256':hashlib.sha256((HERE/'interface-literal-input-v1.tex').read_bytes()).hexdigest(),
        'C2_source_sha256':hashlib.sha256((HERE/'C2-second-patch-results-v1.json').read_bytes()).hexdigest(),
        'C3_source_sha256':hashlib.sha256((HERE/'core40-path-results-v2.json').read_bytes()).hexdigest(),
        'scope':'Independent fixed-word and inherited-interface proof-certificate review; no peer helper import, DFS, seed search, or full interface kernel replay.'}
    (HERE/'review-results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__=='__main__':main()
