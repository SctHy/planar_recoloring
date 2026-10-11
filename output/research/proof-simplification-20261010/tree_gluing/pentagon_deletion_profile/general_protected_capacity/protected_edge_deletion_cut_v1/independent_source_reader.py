#!/usr/bin/env python3
"""Independent actual-source review: no author helpers or result JSON.

Reimplement the printed first-normalizer rule; use printed cycle vertices
and local mutation lists. Neighbour closure proves the selected cycles
are complete components without enumerating all4^5 states or searching HC.
"""
from itertools import permutations
from pathlib import Path
import hashlib
import json
import platform
import re
import sys

BASE=Path(__file__).resolve().parent
EXPECTED={
    'reference-phase8.tex':'3806a0c7f8ec374ea92e70152f939e92e35c3c76564f9e69e8c06160999bcb58',
    'candidate-input-v1.tex':'21783ee56638ef617420fd6f9bf3e5b8bca1642a6a2fc1ccfb49d3d742e3bf8a',
    'candidate-input-v2.tex':'6bfed6b8fa76d392dc0766ded22a82da4a3a048fa132b9d43347e6cdae55e5f3'}
COLOURS='0123'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def edge(a,b):
    return tuple(sorted((a,b)))


def is_legal(word,boundary):
    return all(word[i]!=word[(i+1)%5] and (boundary[i]=='4' or word[i]!=boundary[i]) for i in range(5))


def mutation_lists(word,boundary):
    return [sorted(set(COLOURS)-{word[(i-1)%5],word[(i+1)%5]}-
                   (set() if boundary[i]=='4' else {boundary[i]})) for i in range(5)]


def neighbours(word,boundary):
    assert is_legal(word,boundary)
    return {word[:i]+c+word[i+1:] for i,L in enumerate(mutation_lists(word,boundary)) for c in L if c!=word[i]}


def transform(word,mapping):
    start,sign,perm=mapping
    return ''.join('4' if word[(start+sign*i)%5]=='4' else perm[int(word[(start+sign*i)%5])] for i in range(5))


def restore(word,mapping):
    start,sign,perm=mapping
    restored=['?']*5
    for i,c in enumerate(word):
        restored[(start+sign*i)%5]=str(perm.index(c))
    return ''.join(restored)


def marked(text):
    matches=list(re.finditer(r'% BEGIN ([A-Z0-9-]+)\n(.*?)% END \1',text,re.S))
    assert len({m.group(1) for m in matches})==len(matches)
    return {m.group(1):m.group(0) for m in matches}


def body(block):
    return block.split('\n',1)[1].rsplit('% END ',1)[0]


def interfaces(block):
    rows=re.findall(r'([0-4]{5}:\d)\s+(\d)\s+([0-3])\s+([0-4]{5}:\d)\s+([0-3]{5})-([0-3]{5})',body(block))
    return [((s,int(j),int(q),t),edge(a,b)) for s,j,q,t,a,b in rows]


def family_table(text):
    found=re.findall(r'Put \$w=([0-3]{5})\$\.(.*?)\\end\{array\}',text,re.S)
    assert len(found)==1
    shared,table=found[0]
    pattern=r'([0-3]{5}|w)(?:_([23]))?(?:\^(?:\{([0-4]+)\}|([0-4])))?'
    result={}
    for t in ('01023','01124'):
        row=re.search(r'\b'+t+r'&(.*?)(?:\\\\|$)',table,re.S)
        assert row is not None
        entries=[]
        for word,d,braced,single in re.findall(pattern,row.group(1)):
            entries.append({'word':shared if word=='w' else word,
                            'declared_degree':None if not d else int(d),
                            'declared_J':sorted(map(int,braced or single))})
        assert entries and len({e['word'] for e in entries})==len(entries)
        result[t]=entries
    return result


def main():
    texts={}
    for name,h in EXPECTED.items():
        assert sha(BASE/name)==h,name
        texts[name]=(BASE/name).read_text()
    ref=texts['reference-phase8.tex'];candidate=texts['candidate-input-v2.tex']
    original=marked(ref);v1=marked(texts['candidate-input-v1.tex']);current=marked(candidate)
    assert len(original)==53 and set(original)==set(v1)==set(current)
    for name in original:
        if name!='INTERFACES-ALL':
            assert original[name]==v1[name]==current[name],name
    normalizer_re=r'Here is the exact normalization convention\.(.*?)In particular a standard boundary first normalizes by the identity\.'
    convention=re.search(normalizer_re,ref,re.S).group(0)
    assert re.search(normalizer_re,candidate,re.S).group(0)==convention
    assert re.search(normalizer_re,texts['candidate-input-v1.tex'],re.S).group(0)==convention
    old_records=interfaces(original['INTERFACES-ALL'])
    retained=interfaces(current['INTERFACES-ALL'])
    expected_retained=[r for r in old_records if r[0][0][:5] not in ('01023','01124')]
    removed=[r for r in old_records if r[0][0][:5] in ('01023','01124')]
    assert len(old_records)==283 and len(retained)==256 and len(removed)==27
    assert len({key for key,e in old_records})==283
    assert retained==expected_retained
    assert interfaces(v1['INTERFACES-ALL'])==retained
    assert 'lem:c5-one-boundary-local' not in candidate
    assert 'the other 283 retain individual edge records' not in candidate
    assert '256' in candidate and '27' in candidate and '30' in candidate
    families=family_table(candidate);first=family_table(texts['candidate-input-v1.tex'])
    for t,entries in families.items():
        assert [(e['word'],e['declared_J']) for e in entries]==[(e['word'],e['declared_J']) for e in first[t]]
    assert [e['word'] for e in families['01023']]==['12310','23101','23201','23210','32301','32310']
    assert [e['word'] for e in families['01124']]==['12303','23031','32301']
    standard_types={'00000','00001','00112'}|{n.split('-')[1] for n in current if n.startswith(('C1-','FHC-'))}
    assert len(standard_types)==22
    def first_normalizer(boundary):
        for start in range(5):
            for sign in (1,-1):
                for perm in permutations(COLOURS):
                    mapping=(start,sign,perm)
                    target=transform(boundary,mapping)
                    if target in standard_types:
                        return target,mapping
        raise AssertionError('no standard type: '+boundary)
    cycle_cache={};component_checks={}
    def component(t,c):
        key=t+':'+str(c)
        assert c==0 and t not in ('00000','00001','00112')
        if key not in cycle_cache:
            name=('FHC-' if '4' in t else 'C1-')+t
            words=re.findall(r'\b[0-3]{5}\b',body(current[name]))
            V=set(words)
            assert len(V)==len(words) and len(words)>2
            assert all(is_legal(w,t) for w in words)
            E={edge(a,b) for a,b in zip(words,words[1:]+words[:1])}
            assert all(sum(a!=b for a,b in zip(*e))==1 for e in E)
            assert len(E)==len(V)
            pool={edge(a,b) for a,b in re.findall(r'([0-3]{5})-([0-3]{5})',body(current['POOL-'+t+'-'+str(c)]))}
            assert len(pool)==8 and pool<=E
            neighbour_checks=sum(len(neighbours(w,t)) for w in V)
            assert all(neighbours(w,t)<=V for w in V)
            cycle_cache[key]=(V,E,pool)
            component_checks[key]={'cycle_block':name,'state_count':len(V),'cycle_edge_count':len(E),
                'pool_edge_count':len(pool),'all_vertices_legal':True,'cycle_connected':True,
                'all_legal_mutation_neighbours_inside_cycle_vertices':True,
                'local_neighbour_memberships_checked':neighbour_checks,
                'complete_connected_component_reason':'A legal connected cycle vertex set closed under every legal one-coordinate mutation is exactly a connected component.'}
        return cycle_cache[key]
    source_annotations=[]
    for t,entries in families.items():
        V,E,pool=component(t,0)
        assert first_normalizer(t)==(t,(0,1,tuple(COLOURS)))
        for entry in entries:
            w=entry['word'];assert w in V
            ds=len(neighbours(w,t))
            J=[i for i in range(5) if t[i] in {w[(i-1)%5],w[(i+1)%5]}]
            assert ds==entry['declared_degree'] and J==entry['declared_J']
            source_annotations.append({'source':t,'word':w,'source_degree':ds,'J':J,
                'source_lists':mutation_lists(w,t)})
    reference_lookup={key:(i+1,e) for i,(key,e) in enumerate(old_records)}
    generated=[];checks=[]
    for t,entries in families.items():
        V,E,P=component(t,0)
        for j in range(5):
            if t[j]=='4':continue
            for q in COLOURS:
                if q==t[j]:continue
                boundary=t[:j]+q+t[j+1:]
                target,mapping=first_normalizer(boundary)
                assert target not in ('00000','00001','00112')
                key=(t+':0',j,int(q),target+':0')
                assert key in reference_lookup
                original_index,old_edge=reference_lookup[key]
                targetV,targetE,targetP=component(target,0)
                restoredV={restore(w,mapping) for w in targetV}
                restoredQ={edge(restore(a,mapping),restore(b,mapping)) for a,b in targetP}
                assert all(is_legal(w,boundary) for w in restoredV)
                assert all(transform(restore(w,mapping),mapping)==w for w in targetV)
                assert all(edge(transform(a,mapping),transform(b,mapping)) in targetP for a,b in restoredQ)
                assert len(restoredQ)==len(targetP)==8
                witnesses=[];all_common=[]
                for entry in entries:
                    w=entry['word']
                    if not is_legal(w,boundary):continue
                    assert w in restoredV and transform(w,mapping) in targetV
                    Ns=neighbours(w,t);Nt=neighbours(w,boundary);common=Ns&Nt
                    assert Nt<=restoredV
                    ds,dt,dc=len(Ns),len(Nt),len(common)
                    alpha=int(t[j] not in {w[(j-1)%5],w[(j+1)%5]})
                    beta=int(q not in {w[(j-1)%5],w[(j+1)%5]})
                    assert dt==ds+alpha-beta and dc==ds-beta
                    assert ds==sum(len(L)-1 for L in mutation_lists(w,t))
                    forbidden={edge(w,y) for y in common if edge(w,y) in P or edge(w,y) in restoredQ}
                    f=len(forbidden);safe=dc-f
                    union=Ns|Nt
                    assert len(union)==ds+dt-dc==ds+alpha
                    union_pool_edges={edge(w,y) for y in union if edge(w,y) in P or edge(w,y) in restoredQ}
                    direct=max(0,4-ds-dt+dc-f);closed=max(0,4-ds-alpha-f)
                    assert direct==closed
                    row={'word':w,'source_degree_ds':ds,'target_degree_dt':dt,'common_degree_dc':dc,
                        'alpha':alpha,'beta':beta,'ds_plus_alpha':ds+alpha,'f':f,
                        'source_neighbours':sorted(Ns),'target_neighbours':sorted(Nt),'common_neighbours':sorted(common),
                        'common_pool_incident_edges':sorted(forbidden),'safe_common_degree':safe,
                        'full_incident_star_union_count':len(union),'full_union_pool_incident_edges':sorted(union_pool_edges),
                        'direct_bound':direct,'closed_bound':closed,'normalized_target_word':transform(w,mapping)}
                    all_common.append(row)
                    if ds+alpha==3 and f==0:witnesses.append(row)
                assert witnesses,key
                generated.append(key)
                checks.append({'case':key,'original_individual_index_1based':original_index,
                    'actual_target_boundary':boundary,'first_normalizer':[mapping[0],mapping[1],list(map(int,mapping[2]))],
                    'target_component':target+':0','selected_target_cycle_complete_component_checked':True,
                    'canonical_target_pool':sorted(targetP),'exact_restored_target_pool':sorted(restoredQ),
                    'all_common_source_set_candidates':all_common,'positive_witnesses':witnesses,
                    'ds_plus_alpha3_f0_witness_exists':True,'bound_at_witness':1})
    assert len(generated)==len(set(generated))==27
    assert set(generated)=={key for key,e in removed}
    assert len({c['original_individual_index_1based'] for c in checks})==27
    assert sum(c['case'][0]=='01023:0' for c in checks)==15
    assert sum(c['case'][0]=='01124:0' for c in checks)==12
    output={'status':'INDEPENDENT_ACTUAL_SOURCE_27_FAMILY_CHECK_PASSED',
        'runtime':{'executable':sys.executable,'python_version':platform.python_version()},
        'input_sha256':EXPECTED,'script_sha256':sha(Path(__file__)),
        'author_helpers_imported':False,'author_result_JSON_read':False,
        'source_family_words_read_from_actual_candidate':families,'source_annotations':source_annotations,
        'other_marked_blocks_byteexact_count':52,'normalizer_convention_byteexact':True,
        'original_individual_count':283,'retained_individual_count':256,'replacement_family_case_count':27,
        'unchanged_constant_family_case_count':30,'accounted_standard_source_interface_count':256+27+30,
        'complete_selected_component_checks':component_checks,'case_checks':checks,
        'v1_to_v2_math_inputs_unchanged':True,'v2_old283_summary_removed':True,
        'v2_added_numbered_lemma_absent':True,'v1_wording_requires_star_terminology_and_count_correction':True,
        'full23_component_or2304_boundary_proof_replayed':False,'unchanged256_individual_edges_reaudited':False,
        'HC_search':False,'full_fibre_states_enumerated':False,'main_changed':False,
        'scope':'Independent actual-source normalizer,cycle/pool,and27local certificate review. Selected component completeness via local closure only; global23component classification and unchanged256/30certificates remain inherited reference premises. Mathematical proof and gluing-pool limitation are separately discussed in report.'}
    path=BASE/'review-results-v2.json'
    assert not path.exists(),'preserve an existing executed result'
    path.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({'status':output['status'],'case_count':len(checks),
        'other_blocks_equal':52,'retained_individuals':256,'accounted_total':313,
        'selected_components_checked':len(component_checks),
        'all27_ds_alpha3_f0':True,'v2_source_sha256':EXPECTED['candidate-input-v2.tex']},indent=2))


if __name__=='__main__':
    main()
