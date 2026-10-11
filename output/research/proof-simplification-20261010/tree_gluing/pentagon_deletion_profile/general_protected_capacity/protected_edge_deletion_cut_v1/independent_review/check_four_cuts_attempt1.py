#!/usr/bin/env python3
"""Independent four actual deletion-cut checks; no root cuthelper/results.

The HC-side graph is rebuilt from its literal component vertices and
proper legal one-coordinate mutations. It is not a selectedcycle graph.
Original interface firstmaps are retained in both proofroles.
"""
from itertools import permutations
from pathlib import Path
import hashlib
import json
import platform
import re
import sys
import independent_source_reader as R

BASE=Path(__file__).resolve().parent
EXPECTED={
    'main-input.tex':'b7a048389c00d075d733581bc98fbfd397765b384777e5959076264ab0dbd557',
    'independent_source_reader.py':'9d0a8f4683718265126b274c230dba96666a3ee6af76c8bfa67397d154718fb0',
    'prior-independent236-results.json':'e8d8584a2269ec8cd86b81c69f94b5027b18f0f6297780adcc58639d3f8843a1',
    'prior-independent236-frozen-manifest.json':'1fcdc133ec47da271375072dd5dfc367524164849a109211c500653ddc36f114'}
CASES=[
    (('00101:0',3,3,'00121:0'),'forward',R.edge('32302','32312')),
    (('01014:0',2,3,'01024:0'),'forward',R.edge('30130','30230')),
    (('01024:0',0,3,'01234:0'),'reverse',R.edge('13130','23130')),
    (('01234:0',0,2,'01024:0'),'forward',R.edge('10102','30102'))]


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def components(V,E):
    adj={v:set() for v in V}
    for a,b in E:adj[a].add(b);adj[b].add(a)
    unseen=set(V);result=[]
    while unseen:
        start=min(unseen);unseen.remove(start);seen={start};todo=[start]
        while todo:
            for neighbor in adj[todo.pop()]:
                if neighbor in unseen:unseen.remove(neighbor);seen.add(neighbor);todo.append(neighbor)
        result.append(seen)
    return sorted(result,key=lambda S:(len(S),sorted(S)))


def cross(E,S):return {e for e in E if (e[0] in S)!=(e[1] in S)}


def main():
    for name,digest in EXPECTED.items():assert sha(BASE/name)==digest,name
    text=(BASE/'main-input.tex').read_text();blocks=R.marked(text)
    prior=json.loads((BASE/'prior-independent236-results.json').read_text())
    assert prior['status']=='INDEPENDENT_ACTUAL_SOURCE_236_FIXEDK_OPPOSITEHC_CHECK_PASSED'
    old_components=prior['component_checks']
    record_rows=R.interfaces(blocks['INTERFACES-ALL']);lookup={k:(i+1,e) for i,(k,e) in enumerate(record_rows)}
    assert len(record_rows)==len(lookup)==47
    types={'00000','00001','00112'}|{n.split('-')[1] for n in blocks if n.startswith(('C1-','FHC-'))}
    def first_normalizer(boundary):
        for start in range(5):
            for sign in (1,-1):
                for perm in permutations(R.COLOURS):
                    mapping=(start,sign,perm);target=R.transform(boundary,mapping)
                    if target in types:return target,mapping
        raise AssertionError('no firstmap: '+boundary)
    cache={};component_basis={};graph_cache={}
    def hc_component(t,c):
        key=t+':'+str(c);assert c==0 and t not in ('00000','00001','00112')
        if key not in cache:
            name=('FHC-' if '4' in t else 'C1-')+t;poolname='POOL-'+t+'-'+str(c)
            old=old_components[key]
            assert old['has_printed_whole_component_HC'] is True
            assert hashlib.sha256(blocks[name].encode()).hexdigest()==old['word_block_sha256']
            assert hashlib.sha256(blocks[poolname].encode()).hexdigest()==old['pool_block_sha256']
            assert old['all_legal_mutation_neighbours_inside_vertex_set'] is True
            words=re.findall(r'\b[0-3]{5}\b',R.body(blocks[name]));V=set(words)
            assert len(V)==len(words)==old['state_count'] and all(R.is_legal(w,t) for w in V)
            C={R.edge(a,b) for a,b in zip(words,words[1:]+words[:1])}
            assert len(C)==len(V) and all(sum(a!=b for a,b in zip(*e))==1 for e in C)
            P={R.edge(a,b) for a,b in re.findall(r'([0-3]{5})-([0-3]{5})',R.body(blocks[poolname]))}
            assert len(P)==8 and P<=C
            K=C-P
            assert K=={tuple(e) for e in old['actual_fixed_K']}
            assert P=={tuple(e) for e in old['actual_pool']}
            cache[key]=(V,C,P,K)
            component_basis[key]={'component_word_block':name,'state_count':len(V),'cycle_edge_count':len(C),
                'pool':sorted(P),'fixed_K':sorted(K),'word_block_sha256':old['word_block_sha256'],
                'pool_block_sha256':old['pool_block_sha256'],
                'own_frozen_complete_component_closure_inherited_after_exact_readback':True}
        return cache[key]
    def full_graph(t,c):
        key=t+':'+str(c)
        if key not in graph_cache:
            V,C,P,K=hc_component(t,c)
            N={word:R.neighbours(word,t) for word in V}
            assert all(N[word]<=V for word in V)
            E={R.edge(word,y) for word in V for y in N[word]}
            assert C<=E and len(components(V,E))==1
            graph_cache[key]=(V,E)
        return graph_cache[key]
    checks=[]
    for key,direction,bridge in CASES:
        assert key in lookup
        source_key,j,q,target_key=key;s,sc=source_key.split(':');t,tc=target_key.split(':')
        boundary=s[:j]+str(q)+s[j+1:]
        actual_type,mapping=first_normalizer(boundary);assert actual_type==t
        Vs,Cs,Ps,Ks=hc_component(s,int(sc));Vt,Ct,Pt,Kt=hc_component(t,int(tc))
        restoredVt={R.restore(w,mapping) for w in Vt}
        restoredKt={R.edge(R.restore(a,mapping),R.restore(b,mapping)) for a,b in Kt}
        restoredPt={R.edge(R.restore(a,mapping),R.restore(b,mapping)) for a,b in Pt}
        assert all(R.is_legal(w,boundary) for w in restoredVt)
        assert {R.edge(R.transform(a,mapping),R.transform(b,mapping)) for a,b in restoredKt}==Kt
        assert {R.edge(R.transform(a,mapping),R.transform(b,mapping)) for a,b in restoredPt}==Pt
        if direction=='forward':
            hc_key=target_key;V,E=full_graph(t,int(tc));P=Pt
            fixedK={R.edge(R.transform(a,mapping),R.transform(b,mapping)) for a,b in Ks}
            fixed_pool={R.edge(R.transform(a,mapping),R.transform(b,mapping)) for a,b in Ps}
            coordinate_note='canonical restoredtarget HCside: originalsource objects transformed by original firstmap'
        else:
            hc_key=source_key;V,E=full_graph(s,int(sc));P=Ps
            fixedK=restoredKt;fixed_pool=restoredPt
            coordinate_note='originalstandard source HCside: originaltarget objects restored by original firstmap'
        assert fixedK.isdisjoint(fixed_pool)
        F=(fixedK&E)-P;H=E-F
        assert F<=fixedK and F.isdisjoint(P|fixed_pool)
        assert bridge in H
        Hcomps=components(V,H);after=components(V,H-{bridge})
        sides=[S for S in after if (bridge[0] in S)!=(bridge[1] in S)]
        assert len(sides)==2
        S=min(sides,key=lambda U:(len(U),sorted(U)))
        assert 0<len(S)<len(V)
        remaining_cross=cross(H,S);full_cross=cross(E,S);deleted_cross=cross(F,S)
        assert remaining_cross=={bridge}
        assert full_cross==deleted_cross|{bridge} and deleted_cross<=F
        assert full_cross.isdisjoint(P|fixed_pool)
        # Both edge and vertex obstruction can be verified locally without
        # running a global bridge/articulation producer.
        degrees={word:sum(word in e for e in H) for word in V}
        min_degree=min(degrees.values());assert min_degree>=2
        original_cut_side=[R.restore(w,mapping) if direction=='forward' else w for w in sorted(S)]
        original_bridge=R.edge(*(R.restore(w,mapping) for w in bridge)) if direction=='forward' else bridge
        checks.append({'case':key,'direction':direction,'original47_record_index_1based':lookup[key][0],
            'original_printed_witness':lookup[key][1],'actual_target_boundary':boundary,
            'original_first_normalizer':[mapping[0],mapping[1],list(map(int,mapping[2]))],
            'HC_side_component':hc_key,'comparison_coordinates':coordinate_note,
            'canonical_source_pool':sorted(Ps),'canonical_target_pool':sorted(Pt),
            'exact_restored_target_pool':sorted(restoredPt),'exact_restored_target_K':sorted(restoredKt),
            'opposite_fixed_K_in_HC_coordinates':sorted(fixedK),'opposite_pool_in_HC_coordinates':sorted(fixed_pool),
            'HC_side_pool':sorted(P),'HC_state_count':len(V),'HC_full_graph_edge_count':len(E),
            'safe_K_deletion_F':sorted(F),'safe_K_deletion_edge_count':len(F),
            'remaining_H_edge_count':len(H),'remaining_H_component_count':len(Hcomps),'remaining_H_min_degree':min_degree,
            'named_bridge_in_H':bridge,'components_after_bridge_removal_count':len(after),
            'cut_side_S':sorted(S),'cut_side_state_count':len(S),'cut_complement_state_count':len(V-S),
            'full_graph_cut_edges':sorted(full_cross),'deleted_safe_K_cut_edges':sorted(deleted_cross),
            'remaining_H_cut_edges':sorted(remaining_cross),'only_remaining_cut_edge_is_named_bridge':True,
            'cut_full_edges_avoid_both_relevant_pools':True,
            'cut_side_in_original_interface_coordinates':original_cut_side,
            'bridge_in_original_interface_coordinates':original_bridge,
            'any_HC_on_HC_side_must_use_at_least_one_deleted_safe_fixedK_edge':True})
    output={'status':'INDEPENDENT_FOUR_ACTUAL_SAFE_K_BRIDGE_CUT_CERTIFICATES_PASSED',
        'runtime':{'executable':sys.executable,'python_version':platform.python_version()},
        'input_sha256':EXPECTED,'script_sha256':sha(Path(__file__)),
        'root_cut_helpers_imported':False,'root_computed_cut_JSON_read':False,
        'only_requested_four_directions_checked':True,'unique_HC_full_graphs_rebuilt':sorted(graph_cache),
        'component_basis_readback':component_basis,'case_checks':checks,
        'same_regular_HC_graph_for_third_and_fourth':checks[2]['HC_side_component']==checks[3]['HC_side_component']=='01024:0',
        'third_and_fourth_safe_deletion_sets_equal':checks[2]['safe_K_deletion_F']==checks[3]['safe_K_deletion_F'],
        'HC_scope':'Only the opposite wholecomponentHC is quantified. FixedK remains fromtheprinted selectedtemplate andPOOL. NoarbitrarypairHC upgrade;globalclassification/printedHCclosure andpool/reservegluing dependencies inherited.',
        'noHC_search_or_full_state_enumeration':True,'root70direction_or236predicate_repeated':False,'main_or_old_record_changed':False}
    path=BASE/'four-cut-results.json';assert not path.exists();path.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({'status':output['status'],'cuts':[{'case':c['case'],'direction':c['direction'],
        'firstmap':c['original_first_normalizer'],'HC_component':c['HC_side_component'],
        'S':c['cut_side_S'],'remaining_bridge':c['named_bridge_in_H'],
        'deleted_safe_cross_edges':c['deleted_safe_K_cut_edges'],'H_min_degree':c['remaining_H_min_degree']}
        for c in checks],'third_fourth_deletion_equal':output['third_and_fourth_safe_deletion_sets_equal']},indent=2))


if __name__=='__main__':main()
