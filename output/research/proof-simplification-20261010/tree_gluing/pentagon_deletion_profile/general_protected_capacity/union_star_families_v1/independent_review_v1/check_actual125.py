#!/usr/bin/env python3
"""Independent actual fifteen-family source review; no author helpers.

Reference JSON is used only for the original 125 interface identities.
Every word, cycle, pool and normalizer input comes from actual TeX.
Old twelve component closures are inherited from this reviewer's own
hash-bound check after verifying unchanged literal component/pool blocks.
"""
from itertools import permutations
from pathlib import Path
from collections import Counter
import difflib
import hashlib
import json
import platform
import re
import sys
import independent_source_reader as R

BASE=Path(__file__).resolve().parent
EXPECTED={
    'reference-phase8.tex':'3806a0c7f8ec374ea92e70152f939e92e35c3c76564f9e69e8c06160999bcb58',
    'candidate-input-v1.tex':'275058ea128ac1f462766a6d08baa90cb32358b55a32e4d210b18920646424d5',
    'frozen-reference-case-index.json':'36ee26c64c667dbb7bea0bc88eed3b3162c85cbae16038da3a01cd59eeca68b1',
    'prior-independent27-results.json':'d2acdea96a30e7582c79f24fd4e42ad00c0a64328b9ba72ff9a9d94463b9ac7f',
    'independent_source_reader.py':'9d0a8f4683718265126b274c230dba96666a3ee6af76c8bfa67397d154718fb0',
    'prior-independent27-frozen-manifest.json':'77997fc64a907ef22ae965dc13a7d8683f21d0f0081e9bb513373931ca589f20'}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def paragraph(text,start,end):
    a=text.index(start);b=text.index(end,a)+len(end)
    return text[a:b]


def family_table(text):
    section=paragraph(text,r'\paragraph{Three-edge-union source selectors (125 interfaces).}',r'\end{array}')
    matches=re.findall(r'([0-4]{5})&(.*?)\\\\',section,re.S)
    assert len(matches)==15 and len({t for t,row in matches})==15
    result={}
    for t,row in matches:
        words=re.findall(r'\b[0-3]{5}\b',row)
        assert words and len(words)==len(set(words))
        # No unseen token may silently become a selector.
        assert re.sub(r'[0-3]{5}|[\s,\\]','',row)==''
        result[t]=words
    assert sum(map(len,result.values()))==48
    assert len({w for words in result.values() for w in words})==27
    return result


def main():
    for name,digest in EXPECTED.items():assert sha(BASE/name)==digest,name
    ref=(BASE/'reference-phase8.tex').read_text()
    candidate=(BASE/'candidate-input-v1.tex').read_text()
    original=R.marked(ref);current=R.marked(candidate)
    assert len(original)==len(current)==53 and set(original)==set(current)
    assert all(original[name]==current[name] for name in original if name!='INTERFACES-ALL')
    convention=r'Here is the exact normalization convention\.(.*?)In particular a standard boundary first normalizes by the identity\.'
    assert re.search(convention,candidate,re.S).group(0)==re.search(convention,ref,re.S).group(0)
    statements=r'\\begin\{(lemma|theorem|corollary|proposition)\}(.*?)\\end\{\1\}'
    original_statements=re.findall(statements,ref,re.S)
    assert re.findall(statements,candidate,re.S)==original_statements
    assert len(original_statements)==41
    old_records=R.interfaces(original['INTERFACES-ALL'])
    retained=R.interfaces(current['INTERFACES-ALL'])
    old_keys={key for key,e in old_records};retained_keys={key for key,e in retained}
    assert len(old_records)==len(old_keys)==283
    assert len(retained)==len(retained_keys)==158 and retained_keys<=old_keys
    assert retained==[row for row in old_records if row[0] in retained_keys]
    removed=[row for row in old_records if row[0] not in retained_keys]
    assert len(removed)==125
    # Read only case identities, not certificates/observations from the frozen reference.
    index=json.loads((BASE/'frozen-reference-case-index.json').read_text())
    reference_cases=set()
    for record in index['records']:
        if not record['covered']:continue
        i=record['interface']
        key=(i['source']+':'+str(i['source_component']),int(i['position']),int(i['colour']),
             i['target_type']+':'+str(i['target_component']))
        assert key not in reference_cases
        reference_cases.add(key)
    assert len(reference_cases)==125 and reference_cases=={key for key,e in removed}
    del index
    families=family_table(candidate)
    standard_types={'00000','00001','00112'}|{name.split('-')[1] for name in current if name.startswith(('C1-','FHC-'))}
    assert len(standard_types)==22
    def first_normalizer(boundary):
        for start in range(5):
            for sign in (1,-1):
                for perm in permutations(R.COLOURS):
                    mapping=(start,sign,perm);t=R.transform(boundary,mapping)
                    if t in standard_types:return t,mapping
        raise AssertionError('no normalizer: '+boundary)
    prior=json.loads((BASE/'prior-independent27-results.json').read_text())
    assert prior['status']=='INDEPENDENT_ACTUAL_SOURCE_27_FAMILY_CHECK_PASSED'
    assert prior['script_sha256']==sha(BASE/'independent_source_reader.py')
    assert prior['input_sha256']['reference-phase8.tex']==sha(BASE/'reference-phase8.tex')
    old_components=prior['complete_selected_component_checks']
    assert len(old_components)==12
    cache={};component_checks={}
    def component(t,c):
        key=t+':'+str(c)
        assert c==0 and t not in ('00000','00001','00112')
        if key not in cache:
            name=('FHC-' if '4' in t else 'C1-')+t;pool_name='POOL-'+t+'-'+str(c)
            assert current[name]==original[name] and current[pool_name]==original[pool_name]
            words=re.findall(r'\b[0-3]{5}\b',R.body(current[name]));V=set(words)
            assert len(V)==len(words)>2 and all(R.is_legal(w,t) for w in words)
            E={R.edge(a,b) for a,b in zip(words,words[1:]+words[:1])}
            assert len(E)==len(V) and all(sum(a!=b for a,b in zip(*e))==1 for e in E)
            P={R.edge(a,b) for a,b in re.findall(r'([0-3]{5})-([0-3]{5})',R.body(current[pool_name]))}
            assert len(P)==8 and P<=E
            if key in old_components:
                inherited=old_components[key]
                assert inherited['cycle_block']==name and inherited['state_count']==len(V)
                assert inherited['all_legal_mutation_neighbours_inside_cycle_vertices'] is True
                neighbour_checks=inherited['local_neighbour_memberships_checked'];mode='inherited-own-frozen-closure-after-byteexact-readback'
            else:
                N={w:R.neighbours(w,t) for w in V}
                assert all(neighbours<=V for neighbours in N.values())
                neighbour_checks=sum(map(len,N.values()));mode='fresh-legal-local-neighbour-closure'
            cache[key]=(V,E,P)
            component_checks[key]={'cycle_block':name,'cycle_block_sha256':hashlib.sha256(current[name].encode()).hexdigest(),
                'pool_block_sha256':hashlib.sha256(current[pool_name].encode()).hexdigest(),
                'state_count':len(V),'cycle_edge_count':len(E),'pool_edge_count':len(P),
                'all_vertices_legal':True,'cycle_connected':True,'pool_subset_cycle':True,
                'all_legal_mutation_neighbours_inside_cycle_vertices':True,
                'local_neighbour_memberships_checked':neighbour_checks,'closure_mode':mode,
                'complete_component_reason':'The legal connected cycle vertex set is closed under every legal one-coordinate mutation, so is an entire connected component.'}
        return cache[key]
    annotations=[]
    for t,words in families.items():
        V,E,P=component(t,0)
        assert first_normalizer(t)==(t,(0,1,tuple(R.COLOURS)))
        for word in words:
            assert R.is_legal(word,t) and word in V
            N=R.neighbours(word,t)
            assert N<=V
            annotations.append({'source':t,'word':word,'source_degree':len(N),'mutation_lists':R.mutation_lists(word,t)})
    lookup={key:(i+1,e) for i,(key,e) in enumerate(old_records)}
    checks=[]
    for key,old_edge in removed:
        source_key,j,q,target_key=key;t,c=source_key.split(':');target,tc=target_key.split(':')
        assert t in families and c==tc=='0' and t[j]!='4' and str(q)!=t[j]
        boundary=t[:j]+str(q)+t[j+1:]
        actual_type,mapping=first_normalizer(boundary)
        assert actual_type==target
        V,E,P=component(t,0);targetV,targetE,targetP=component(target,0)
        restoredV={R.restore(word,mapping) for word in targetV}
        restoredE={R.edge(R.restore(a,mapping),R.restore(b,mapping)) for a,b in targetE}
        Q={R.edge(R.restore(a,mapping),R.restore(b,mapping)) for a,b in targetP}
        assert len(Q)==8 and Q<=restoredE
        assert all(R.is_legal(w,boundary) and R.transform(w,mapping) in targetV for w in restoredV)
        assert all(R.transform(R.restore(w,mapping),mapping)==w for w in targetV)
        assert {R.edge(R.transform(a,mapping),R.transform(b,mapping)) for a,b in Q}==targetP
        all_common=[];witnesses=[]
        for word in families[t]:
            if not R.is_legal(word,boundary):continue
            assert word in restoredV
            Ns=R.neighbours(word,t);Nt=R.neighbours(word,boundary);common=Ns&Nt;union=Ns|Nt
            assert Ns<=V and Nt<=restoredV
            alpha=int(t[j] not in {word[(j-1)%5],word[(j+1)%5]})
            ds,dt,dc=len(Ns),len(Nt),len(common)
            assert ds==sum(len(L)-1 for L in R.mutation_lists(word,t))
            assert len(union)==ds+dt-dc==ds+alpha
            added=Nt-Ns
            expected_added={word[:j]+t[j]+word[j+1:]} if alpha else set()
            assert added==expected_added
            forbidden={R.edge(word,y) for y in common if R.edge(word,y) in P or R.edge(word,y) in Q}
            row={'word':word,'source_degree_ds':ds,'target_degree_dt':dt,'common_degree_dc':dc,
                 'alpha':alpha,'ds_plus_alpha':ds+alpha,'full_incident_star_union_count':len(union),
                 'source_neighbours':sorted(Ns),'target_neighbours':sorted(Nt),'common_neighbours':sorted(common),
                 'new_target_only_moves':sorted(added),'common_pool_incident_edges':sorted(forbidden),'f':len(forbidden),
                 'normalized_target_word':R.transform(word,mapping)}
            all_common.append(row)
            if len(union)<=3 and not forbidden:witnesses.append(row)
        assert witnesses,key
        checks.append({'case':key,'original_individual_index_1based':lookup[key][0],
            'original_printed_edge':old_edge,'actual_target_boundary':boundary,
            'first_normalizer':[mapping[0],mapping[1],list(map(int,mapping[2]))],
            'target_component':target_key,'canonical_source_pool':sorted(P),
            'canonical_target_pool':sorted(targetP),'exact_restored_target_pool':sorted(Q),
            'source_and_target_complete_component_checked_or_inherited':True,
            'all_common_source_set_candidates':all_common,'positive_witnesses':witnesses,
            'selected_legal_component_state_union_le3_common_pool_f0_exists':True})
    assert len(checks)==125 and len({c['original_individual_index_1based'] for c in checks})==125
    actual_checked={tuple(c['case']) for c in checks}
    assert retained_keys.isdisjoint(actual_checked) and retained_keys|actual_checked==old_keys
    # Source edits are confined to the proof summary, verification note,
    # inserted family paragraph and original individual-record block/header.
    old_proof=paragraph(ref,'For the 313 standard-source interfaces,',r'\end{proof}')
    new_proof=paragraph(candidate,'For the 313 standard-source interfaces,',r'\end{proof}')
    old_note=paragraph(ref,'The finite data used for the endpoint-sensitive statements','These are bounded certificate replays, not arbitrary-size graph searches.')
    new_note=paragraph(candidate,'The finite data used for the endpoint-sensitive statements','These are bounded certificate replays, not arbitrary-size graph searches.')
    old_phrase='The constant-source cases are supplied by six parameter families; the other 283 retain individual edge records.'
    new_phrase='Six constant-source families cover 30 cases; fifteen source-selector rows cover 125 by three-edge incident unions, leaving 158 individual edge records.'
    assert new_note==old_note.replace(old_phrase,new_phrase)
    a=candidate.index(r'\paragraph{Three-edge-union source selectors (125 interfaces).}')
    b=candidate.index(r'\paragraph{The 158 remaining individual nonconstant-source interfaces.}',a)
    family_text=candidate[a:b]
    normalized=candidate.replace(new_proof,old_proof).replace(new_note,old_note).replace(family_text,'')
    normalized=normalized.replace(r'\paragraph{The 158 remaining individual nonconstant-source interfaces.}',r'\paragraph{The 283 nonconstant-source interfaces.}')
    normalized=normalized.replace(current['INTERFACES-ALL'],original['INTERFACES-ALL'])
    assert normalized==ref,'unrelated manuscript change'
    fresh={k:v for k,v in component_checks.items() if v['closure_mode'].startswith('fresh')}
    reused={k:v for k,v in component_checks.items() if v['closure_mode'].startswith('inherited')}
    assert len(reused)==12
    output={'status':'INDEPENDENT_ACTUAL_SOURCE_125_FAMILY_CHECK_PASSED',
        'runtime':{'executable':sys.executable,'python_version':platform.python_version()},
        'input_sha256':EXPECTED,'script_sha256':sha(Path(__file__)),
        'author_helpers_imported':False,'author_result_JSON_used_for_math_check':False,
        'frozen_reference_JSON_use':'Only the original 125 covered interface identities, compared with the independently derived actual TeX complement; no certificate/observation values used.',
        'source_family_words_read_from_actual_candidate':families,'source_selector_row_count':15,
        'source_selector_entry_count':48,'source_selector_distinct_word_count':27,'source_word_annotations':annotations,
        'other_marked_blocks_byteexact_count':52,'first_normalizer_convention_byteexact':True,
        'all_math_statements_byteexact_count':41,'math_statement_counts':dict(Counter(t for t,s in original_statements)),
        'all_other_manuscript_bytes_equal_phase8_after_declared_edits':True,
        'original_individual_count':283,'retained_individual_count':158,'replacement_family_case_count':125,
        'unchanged_constant_family_case_count':30,'accounted_standard_source_interface_count':313,
        'retained_and_replaced_partition_original283_without_duplicate_or_omission':True,
        'actual125_complement_equals_frozen_reference_case_index':True,
        'component_checks':component_checks,'inherited_component_count':len(reused),'fresh_component_count':len(fresh),
        'case_count_by_source':dict(Counter(c['case'][0] for c in checks)),
        'positive_witness_union_size_counts':dict(Counter(w['full_incident_star_union_count'] for c in checks for w in c['positive_witnesses'])),
        'case_checks':checks,'actual_v1_family_text':family_text,
        'scope':'Actual 125 replacement cases and selected complete components; existing phase8 classification and unchanged individual/constant evidence inherited. No HC search, full-state enumeration, global producer replay or Main edit.'}
    result_path=BASE/'review-results-v1.json';assert not result_path.exists()
    result_path.write_text(json.dumps(output,indent=2)+'\n')
    diff_path=BASE/'candidate-v1-independent.diff';assert not diff_path.exists()
    diff_path.write_text(''.join(difflib.unified_diff(ref.splitlines(True),candidate.splitlines(True),fromfile='reference-phase8.tex',tofile='candidate-input-v1.tex')))
    print(json.dumps({'status':output['status'],'actual_source_sha256':EXPECTED['candidate-input-v1.tex'],
        'case_count':125,'source_rows':15,'entries':48,'distinct_words':27,'inherited_components':len(reused),
        'fresh_components':{k:v['state_count'] for k,v in fresh.items()},'accounting':'158+125+30=313',
        'witness_union_size_counts':output['positive_witness_union_size_counts']},indent=2))


if __name__=='__main__':main()
