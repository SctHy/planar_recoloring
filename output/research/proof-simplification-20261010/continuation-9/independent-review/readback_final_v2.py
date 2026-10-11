#!/usr/bin/env python3
"""Bind final actual v2 prose to this reviewer's unchanged 125 inputs."""
from pathlib import Path
import difflib
import hashlib
import json
import re
import check_actual125 as C
import independent_source_reader as R

BASE=Path(__file__).resolve().parent
FINAL_SHA='ecea0571029a8527630442b2242bc21ec76f67bc44b2f768b9228c5f494203a9'


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    prior_path=BASE/'review-results-v1.json';prior=json.loads(prior_path.read_text())
    assert prior['status']=='INDEPENDENT_ACTUAL_SOURCE_125_FAMILY_CHECK_PASSED'
    assert prior['script_sha256']==sha(BASE/'check_actual125.py')
    for name,digest in prior['input_sha256'].items():assert sha(BASE/name)==digest
    assert sha(BASE/'candidate-input-v2.tex')==FINAL_SHA
    v1=(BASE/'candidate-input-v1.tex').read_text();v2=(BASE/'candidate-input-v2.tex').read_text()
    before='For a common state $x$ under an edit $j:a\\to q$,'
    after='For a common state $x$ under a non-star edit $j:a\\to q$,'
    old='For each covered interface, some listed $x\\in S_t$ lies in the restored\n'
    new='For each of the 125 nonconstant-source interfaces not listed individually\nbelow, some $x\\in S_t$ lies in the restored\n'
    assert v1.count(before)==v2.count(after)==1 and v1.count(old)==v2.count(new)==1
    assert v1.replace(before,after).replace(old,new)==v2
    assert R.marked(v1)==R.marked(v2) and C.family_table(v1)==C.family_table(v2)
    for case in prior['case_checks']:
        assert case['positive_witnesses']
        for word in case['positive_witnesses']:
            assert word['full_incident_star_union_count']==word['ds_plus_alpha']<=3
            assert word['f']==0 and word['common_pool_incident_edges']==[]
        source,j,q,target=case['case']
        assert source[:5][j]!='4'
    result={'status':'INDEPENDENT_FINAL_V2_SOURCE_READBACK_AND_REUSED_125_CERTIFICATES_PASSED',
        'input_sha256':{'candidate-input-v2.tex':FINAL_SHA,'candidate-input-v1.tex':sha(BASE/'candidate-input-v1.tex'),
            'review-results-v1.json':sha(prior_path),'check_actual125.py':sha(BASE/'check_actual125.py'),
            'independent_source_reader.py':sha(BASE/'independent_source_reader.py')},
        'script_sha256':sha(Path(__file__)),
        'only_source_edits_from_v1':'Explicit non-star edit and explicit actual 125-case complement of the individually listed nonconstant-source interfaces.',
        'all53_marked_blocks_equal_independently_checked_v1':True,
        'actual15_selector_rows_equal_independently_checked_v1':True,
        'actual125_case_indices_component_cycles_pools_normalizers_unchanged':True,
        'all125_have_legal_component_witness_union_le3_common_pool_f0':True,
        'prior_independent125_certificates_reused_without_neighbour_rerun':True,
        'covered_case_set_now_defined_as_actual_complement':True,
        'nonstar_edit_hypothesis_now_explicit':True,
        'author_helpers_imported':False,'author_result_JSON_used_for_math_check':False,'main_changed':False,
        'proof_scope':'Common-star pool avoidance is the required condition, not whole-union pool avoidance. The arbitrary-pair-HC local intersection is applied to the specified pool-containing component cycles; gluing still requires pool/reserve edge containment.'}
    path=BASE/'review-results-v2.json';assert not path.exists()
    path.write_text(json.dumps(result,indent=2)+'\n')
    diff=BASE/'candidate-v2-independent.diff';assert not diff.exists()
    diff.write_text(''.join(difflib.unified_diff(v1.splitlines(True),v2.splitlines(True),fromfile='candidate-input-v1.tex',tofile='candidate-input-v2.tex')))
    print(json.dumps({'status':result['status'],'final_v2_sha256':FINAL_SHA,'reused_case_count':125,
                     'additional_neighbour_computation':False},indent=2))


if __name__=='__main__':main()
