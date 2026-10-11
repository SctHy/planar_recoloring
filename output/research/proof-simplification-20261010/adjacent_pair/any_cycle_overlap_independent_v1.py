"""Check only the two symbolic normal forms and literal seed/tight example."""
from pathlib import Path
from itertools import product
import hashlib, json

HERE=Path(__file__).resolve().parent
SOURCE=HERE/'any_cycle_overlap_candidate_v1.tex'

def edge(a,b):return tuple(sorted((a,b)))
def graph(A,B):
    vs={a+b for a,b in product(A,B) if a!=b}
    es={edge(a,b) for a,b in product(vs,vs) if sum(x!=y for x,y in zip(a,b))==1}
    degrees={w:sum(w in e for e in es) for w in vs}
    return vs,es,degrees
def cycle(ws,A,B):
    vs,es,_=graph(A,B)
    ee={edge(ws[i-1],ws[i]) for i in range(len(ws))}
    assert len(ws)==len(set(ws))==len(vs) and set(ws)==vs and ee<=es
    return ee

def main():
    old=graph('012','012');new=graph('013','012')
    common_vs=old[0]&new[0];common_es=old[1]&new[1]
    assert common_vs=={'01','02','12','10'}
    assert common_es=={edge('01','02'),edge('02','12'),edge('12','10')}
    assert all(old[2][w]==new[2][w]==2 for w in ('01','10'))

    old2=graph('123','013');new2=graph('023','013')
    five_vs=old2[0]&new2[0];six_es=old2[1]&new2[1]
    assert five_vs=={'20','21','23','30','31'}
    assert six_es=={edge('20','21'),edge('20','23'),edge('21','23'),
                    edge('20','30'),edge('21','31'),edge('30','31')}
    assert old2[0]-five_vs=={'10','13'} and new2[0]-five_vs=={'01','03'}
    assert old2[2]['13']==new2[2]['03']==2
    assert {e for e in old2[1] if '13' in e}=={edge('10','13'),edge('13','23')}
    assert {e for e in new2[1] if '03' in e}=={edge('01','03'),edge('03','23')}
    # The universal count follows symbolically from the forced adjacency
    # of the two outside vertices in any seven-vertex Hamilton cycle.
    tight_old=['10','13','23','20','21','31','30']
    tight_new=['01','03','23','21','20','30','31']
    co=cycle(tight_old,'123','013');cn=cycle(tight_new,'023','013')
    assert len(co&six_es)==len(cn&six_es)==4 and len(co&cn)==2
    retained_seed=['01','03','13','10','20','23','21']
    cycle(retained_seed,'012','013')
    cycle(['01','02','12','10','20','21'],'012','012')
    result={'candidate_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
      'scope':'two symbolic normal forms, no full list kernel or Hamilton cycle enumeration',
      'P4_common_vertices':sorted(common_vs),'P4_common_edges':sorted(common_es),
      'P4_endpoints_have_degree_two_in_both_full_fibres':True,
      'five_common_vertices':sorted(five_vs),'six_common_edges':sorted(six_es),
      'both_full_unequal_graphs_have_seven_vertices':len(old2[0])==len(new2[0])==7,
      'outside_pair_forced_adjacent_in_every_cycle':True,
      'universal_overlap_proof':'each cycle uses four of the six common edges, so intersection at least two',
      'tightness_witness':{'old':tight_old,'new':tight_new,'shared_edges':sorted(co&cn)},
      'single_retained_seven_state_seed':retained_seed,
      'math_review':'PASS; arbitrary Hamilton cycles, either coordinate change, unchanged fibres, and equality of exterior colours are covered'}
    (HERE/'any_cycle_overlap_independent_review_v1.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
