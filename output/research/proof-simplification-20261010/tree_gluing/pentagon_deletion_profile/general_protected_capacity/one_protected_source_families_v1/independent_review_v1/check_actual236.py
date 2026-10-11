#!/usr/bin/env python3
"""Independent actual236case fixedK/oppositeHC source check.

No author helper or result JSON is imported/read. Source words always
stay in the original standard-source coordinates. TargetK/POOL/vertices
are restored by the original interface firstmap, even in reverse role.
"""
from pathlib import Path
from collections import Counter
import difflib
import hashlib
import json
import platform
import re
import sys
import independent_source_reader as R
from fixed_k_source_reader import ActualSource,HARD

BASE=Path(__file__).resolve().parent
EXPECTED={
    'reference-phase8.tex':'3806a0c7f8ec374ea92e70152f939e92e35c3c76564f9e69e8c06160999bcb58',
    'reference-phase9.tex':'ecea0571029a8527630442b2242bc21ec76f67bc44b2f768b9228c5f494203a9',
    'candidate-input-v1.tex':'b0af636d6261154154a1845d96a135acd9c079ff12f05e2f095fb5cd85751449',
    'prior-independent125-results.json':'332a703a5a1adf4f54ecc74a55287f5757854dcd3bf19c477133e2ad60c020d2',
    'prior-independent125-frozen-manifest.json':'bc1ee0441dfdbb55abf3817d4e0f8d973fcb794ef54e2c59bffa3246fc031aa1',
    'independent_source_reader.py':'9d0a8f4683718265126b274c230dba96666a3ee6af76c8bfa67397d154718fb0',
    'fixed-side-local-proof-input.tex':'a944d12a3416a6519e939b819edc7c9f898ab5ee90abafd869c93ba4aae82529'}


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def paragraph(text,start,end):
    a=text.index(start);b=text.index(end,a)+len(end)
    return text[a:b]


def family_table(text):
    section=paragraph(text,r'\paragraph{Fixed-side source selectors (236 interfaces).}',r'\end{array}')
    matches=re.findall(r'([0-4]{5})&(.*?)\\\\',section,re.S)
    assert len(matches)==21 and len({t for t,row in matches})==21
    result={}
    for t,row in matches:
        words=re.findall(r'\b[0-3]{5}\b',row)
        assert words and len(words)==len(set(words))
        assert re.sub(r'[0-3]{5}|[\s,\\]','',row)==''
        result[t]=words
    assert sum(map(len,result.values()))==78
    assert len({w for words in result.values() for w in words})==47
    return result


def main():
    for name,digest in EXPECTED.items():assert sha(BASE/name)==digest,name
    phase8=(BASE/'reference-phase8.tex').read_text();phase9=(BASE/'reference-phase9.tex').read_text()
    candidate=(BASE/'candidate-input-v1.tex').read_text()
    original=R.marked(phase8);adopted=R.marked(phase9);current=R.marked(candidate)
    assert len(original)==len(adopted)==len(current)==53 and set(original)==set(adopted)==set(current)
    assert all(original[name]==adopted[name]==current[name] for name in original if name!='INTERFACES-ALL')
    convention=r'Here is the exact normalization convention\.(.*?)In particular a standard boundary first normalizes by the identity\.'
    assert re.search(convention,candidate,re.S).group(0)==re.search(convention,phase9,re.S).group(0)
    statements=r'\\begin\{(lemma|theorem|corollary|proposition)\}(.*?)\\end\{\1\}'
    old_statements=re.findall(statements,phase8,re.S)
    assert re.findall(statements,candidate,re.S)==re.findall(statements,phase9,re.S)==old_statements
    assert len(old_statements)==41
    old_records=R.interfaces(original['INTERFACES-ALL'])
    retained=R.interfaces(current['INTERFACES-ALL']);phase9_retained=R.interfaces(adopted['INTERFACES-ALL'])
    old_keys={key for key,e in old_records};retained_keys={key for key,e in retained}
    assert len(old_records)==len(old_keys)==283 and len(retained)==len(retained_keys)==47
    assert retained_keys<={key for key,e in phase9_retained}<=old_keys
    assert retained==[row for row in old_records if row[0] in retained_keys]
    removed=[row for row in old_records if row[0] not in retained_keys]
    assert len(removed)==236
    hardhard={key for key,e in old_records if key[0][:5] in HARD and key[3][:5] in HARD}
    assert len(hardhard)==5 and hardhard<=retained_keys
    assert all(not(key[0][:5] in HARD and key[3][:5] in HARD) for key,e in removed)
    families=family_table(candidate)
    prior=json.loads((BASE/'prior-independent125-results.json').read_text())
    assert prior['status']=='INDEPENDENT_ACTUAL_SOURCE_125_FAMILY_CHECK_PASSED'
    assert prior['input_sha256']['reference-phase8.tex']==EXPECTED['reference-phase8.tex']
    old_components=prior['component_checks'];assert len(old_components)==15
    source=ActualSource(current,adopted,old_components)
    assert set(families)==source.standard_types-{'00000'}
    preliminary=(BASE/'fixed-side-local-proof-input.tex').read_text()
    assert preliminary.rstrip() in candidate
    annotations=[]
    for t,words in families.items():
        V,E,P,K,has_hc=source.component(t,0)
        assert source.first_normalizer(t)==(t,(0,1,tuple(R.COLOURS)))
        for word in words:
            assert R.is_legal(word,t) and word in V
            N=R.neighbours(word,t);assert N<=V
            annotations.append({'source':t,'word':word,'source_degree':len(N),
                                'mutation_lists':R.mutation_lists(word,t),'source_has_printed_HC':has_hc})
    lookup={key:(i+1,e) for i,(key,e) in enumerate(old_records)}
    checks=[]
    for key,old_edge in removed:
        source_key,j,q,target_key=key;t,sc=source_key.split(':');target,tc=target_key.split(':')
        assert sc=='0' and t in families and t[j]!='4' and str(q)!=t[j]
        boundary=t[:j]+str(q)+t[j+1:]
        actual_type,mapping=source.first_normalizer(boundary)
        assert actual_type==target
        V,E,P,Ks,source_hc=source.component(t,int(sc))
        targetV,targetE,targetP,targetK,target_hc=source.component(target,int(tc))
        restoredV={R.restore(w,mapping) for w in targetV}
        Q={R.edge(R.restore(a,mapping),R.restore(b,mapping)) for a,b in targetP}
        Kt={R.edge(R.restore(a,mapping),R.restore(b,mapping)) for a,b in targetK}
        assert len(Q)==len(targetP) and len(Kt)==len(targetK) and Q.isdisjoint(Kt)
        assert all(R.is_legal(w,boundary) for w in restoredV)
        assert all(R.transform(R.restore(w,mapping),mapping)==w for w in targetV)
        assert {R.edge(R.transform(a,mapping),R.transform(b,mapping)) for a,b in Q}==targetP
        assert {R.edge(R.transform(a,mapping),R.transform(b,mapping)) for a,b in Kt}==targetK
        assert all(a in restoredV and b in restoredV for a,b in Kt|Q)
        candidates=[];witnesses=[];excluded=[]
        for word in families[t]:
            if not R.is_legal(word,boundary):
                excluded.append({'word':word,'reason':'not target legal'});continue
            if word not in restoredV:
                excluded.append({'word':word,'reason':'target legal but in another target component'});continue
            assert word in V
            Ns=R.neighbours(word,t);Nt=R.neighbours(word,boundary)
            assert Ns<=V and Nt<=restoredV
            rows=[]
            for direction,eligible,N,K,P_hc,hc_side in (
                ('forward',target_hc,Nt,Ks,Q,'restored target'),
                ('reverse',source_hc,Ns,Kt,P,'standard source')):
                if not eligible:continue
                full_star={R.edge(word,y) for y in N}
                good=(K&full_star)-P_hc
                d,g=len(full_star),len(good)
                assert d>=2 and 0<=g<=d and len(full_star-good)==d-g
                assert d==sum(len(L)-1 for L in R.mutation_lists(word,boundary if direction=='forward' else t))
                assert good<=K and good.isdisjoint(P_hc)
                row={'word':word,'direction':direction,'Hamilton_cycle_side':hc_side,
                     'degree_d':d,'safe_fixedK_star_count_g':g,'d_minus_g':d-g,
                     'HC_side_full_neighbours':sorted(N),'HC_side_full_incident_star':sorted(full_star),
                     'safe_fixedK_incident_edges':sorted(good),'other_incident_edges':sorted(full_star-good),
                     'eligible_HC_side_has_printed_whole_component_HC':True}
                rows.append(row)
                if d-g<=1:witnesses.append(row)
            candidates.append({'word':word,'normalized_target_word':R.transform(word,mapping),
                               'valid_direction_observations':rows})
        assert witnesses,key
        checks.append({'case':key,'original_individual_index_1based':lookup[key][0],
            'original_printed_edge':old_edge,'actual_target_boundary':boundary,
            'original_interface_first_normalizer':[mapping[0],mapping[1],list(map(int,mapping[2]))],
            'canonical_source_pool':sorted(P),'canonical_source_fixed_K':sorted(Ks),
            'canonical_target_pool':sorted(targetP),'canonical_target_fixed_K':sorted(targetK),
            'exact_restored_target_pool':sorted(Q),'exact_restored_target_fixed_K':sorted(Kt),
            'source_has_printed_whole_component_HC':source_hc,'target_has_printed_whole_component_HC':target_hc,
            'all_common_source_selector_candidates':candidates,'excluded_source_selector_words':excluded,
            'positive_fixedK_vs_oppositeHC_witnesses':witnesses,
            'selected_common_component_word_and_eligible_direction_d_minus_g_le1_exists':True,
            'source_coordinate_words_used_without_role_renormalization':True})
    checked_keys={tuple(case['case']) for case in checks}
    assert len(checked_keys)==len(checks)==236 and len({c['original_individual_index_1based'] for c in checks})==236
    assert retained_keys.isdisjoint(checked_keys) and retained_keys|checked_keys==old_keys
    old_phase9_keys={tuple(c['case']) for c in prior['case_checks']}
    assert len(old_phase9_keys)==125 and old_phase9_keys<=checked_keys
    # Normalize only the declared manuscript replacement regions back to the
    # adopted phase9 actualsource; all other bytes must be identical.
    old_proof=paragraph(phase9,'For the 313 standard-source interfaces,',r'\end{proof}')
    new_proof=paragraph(candidate,'For the 313 standard-source interfaces,',r'\end{proof}')
    old_note=paragraph(phase9,'The finite data used for the endpoint-sensitive statements','These are bounded certificate replays, not arbitrary-size graph searches.')
    new_note=paragraph(candidate,'The finite data used for the endpoint-sensitive statements','These are bounded certificate replays, not arbitrary-size graph searches.')
    old_phrase='Six constant-source families cover 30 cases; fifteen source-selector rows cover 125 by three-edge incident unions, leaving 158 individual edge records.'
    new_phrase='Six constant-source families cover 30 cases; twenty-one source-selector rows cover 236 by the fixed-side incident-degree criterion, leaving 47 individual edge records.'
    assert new_note==old_note.replace(old_phrase,new_phrase)
    start=phase9.index(r'\paragraph{Three-edge-union source selectors (125 interfaces).}')
    end=phase9.index(r'\paragraph{The 158 remaining individual nonconstant-source interfaces.}',start)
    old_family=phase9[start:end]
    start=candidate.index(r'\paragraph{Fixed-side source selectors (236 interfaces).}')
    end=candidate.index(r'\paragraph{The 47 remaining individual nonconstant-source interfaces.}',start)
    new_family=candidate[start:end]
    normalized=candidate.replace(new_proof,old_proof).replace(new_note,old_note).replace(new_family,old_family)
    normalized=normalized.replace(r'\paragraph{The 47 remaining individual nonconstant-source interfaces.}',r'\paragraph{The 158 remaining individual nonconstant-source interfaces.}')
    normalized=normalized.replace(current['INTERFACES-ALL'],adopted['INTERFACES-ALL'])
    assert normalized==phase9,'unrelated manuscript change'
    components=source.component_checks
    inherited={k:v for k,v in components.items() if v['closure_mode'].startswith('inherited')}
    fresh={k:v for k,v in components.items() if v['closure_mode'].startswith('fresh')}
    assert len(inherited)==15
    roles=Counter('HC-HC' if c['source_has_printed_whole_component_HC'] and c['target_has_printed_whole_component_HC'] else 'hard-source' if not c['source_has_printed_whole_component_HC'] else 'hard-target' for c in checks)
    selected=[next((w for w in c['positive_fixedK_vs_oppositeHC_witnesses'] if w['direction']=='forward'),c['positive_fixedK_vs_oppositeHC_witnesses'][0]) for c in checks]
    output={'status':'INDEPENDENT_ACTUAL_SOURCE_236_FIXEDK_OPPOSITEHC_CHECK_PASSED',
        'runtime':{'executable':sys.executable,'python_version':platform.python_version()},
        'input_sha256':EXPECTED,'script_sha256':sha(Path(__file__)),
        'fixed_K_reader_sha256':sha(BASE/'fixed_k_source_reader.py'),
        'author_helpers_imported':False,'author_result_JSON_read':False,
        'source_selector_rows_read_from_actual_candidate':families,'source_selector_row_count':21,
        'source_selector_entry_count':78,'source_selector_distinct_word_count':47,'source_word_annotations':annotations,
        'other_marked_blocks_byteexact_count':52,'all_math_statements_byteexact_count':41,
        'math_statement_counts':dict(Counter(t for t,s in old_statements)),
        'first_normalizer_convention_byteexact':True,'all_other_manuscript_bytes_equal_adopted_phase9_after_declared_edits':True,
        'original_individual_count':283,'retained_individual_count':47,'replacement_family_case_count':236,
        'unchanged_constant_family_case_count':30,'accounted_standard_source_interface_count':313,
        'retained_and_replaced_partition_original283_without_duplicate_or_omission':True,
        'all_previous125_replacement_indices_included':True,'all5_bothhard_indices_still_individually_printed':sorted(hardhard),
        'component_checks':components,'inherited_component_count':len(inherited),'fresh_component_count':len(fresh),
        'case_count_by_source':dict(Counter(c['case'][0] for c in checks)),'case_count_by_role':dict(roles),
        'selected_first_forward_else_reverse_direction_count':dict(Counter(w['direction'] for w in selected)),
        'selected_first_forward_else_reverse_d_g_count':dict(Counter(str((w['degree_d'],w['safe_fixedK_star_count_g'])) for w in selected)),
        'all_positive_d_g_observation_count':dict(Counter(str((w['degree_d'],w['safe_fixedK_star_count_g'])) for c in checks for w in c['positive_fixedK_vs_oppositeHC_witnesses'])),
        'case_checks':checks,'actual_family_text':new_family,
        'proof_scope':'One fixed protectedK versus any wholeHC only on the opposite side; no arbitrary-pairHC upgrade. Source-coordinate words and original interfacefirstmap retained in eitherrole. HardK seed-commonport property/globalclassification andunchanged47individual/30constantcertificates inherited. NoHCsearch/fullstateenumeration/globalproducerreplay/Main edit.'}
    result_path=BASE/'review-results-v1.json';assert not result_path.exists()
    result_path.write_text(json.dumps(output,indent=2)+'\n')
    diff_path=BASE/'candidate-v1-independent.diff';assert not diff_path.exists()
    diff_path.write_text(''.join(difflib.unified_diff(phase9.splitlines(True),candidate.splitlines(True),fromfile='reference-phase9.tex',tofile='candidate-input-v1.tex')))
    print(json.dumps({'status':output['status'],'actual_source_sha256':EXPECTED['candidate-input-v1.tex'],
        'cases':236,'rows':21,'entries':78,'distinct_words':47,'inherited_components':len(inherited),
        'fresh_components':{k:v['state_count'] for k,v in fresh.items()},'case_roles':dict(roles),
        'selected_direction_counts':output['selected_first_forward_else_reverse_direction_count'],
        'selected_d_g_counts':output['selected_first_forward_else_reverse_d_g_count'],
        'accounting':'47+236+30=313','bothhard_remaining':5},indent=2))


if __name__=='__main__':main()
