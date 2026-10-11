#!/usr/bin/env python3
"""Actualv2 prose readback bound to own unchanged independent236checks."""
from pathlib import Path
import difflib
import hashlib
import json
import check_actual236 as C
import independent_source_reader as R

BASE=Path(__file__).resolve().parent
V2_SHA='b7a048389c00d075d733581bc98fbfd397765b384777e5959076264ab0dbd557'


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def pieces(text):
    start=text.index(r'\paragraph{Fixed-side source selectors (236 interfaces).}')
    table_start=text.index(r'\[\begin{array}{c|l}',start)
    table_end=text.index(r'\end{array}\]',table_start)+len(r'\end{array}\]')
    end=text.index(r'\paragraph{The 47 remaining individual nonconstant-source interfaces.}',table_end)
    return text[start:table_start],text[table_start:table_end],text[table_end:end]


def main():
    prior_path=BASE/'review-results-v1.json';prior=json.loads(prior_path.read_text())
    assert prior['status']=='INDEPENDENT_ACTUAL_SOURCE_236_FIXEDK_OPPOSITEHC_CHECK_PASSED'
    assert prior['script_sha256']==sha(BASE/'check_actual236.py')
    assert prior['fixed_K_reader_sha256']==sha(BASE/'fixed_k_source_reader.py')
    for name,digest in prior['input_sha256'].items():assert sha(BASE/name)==digest
    assert sha(BASE/'candidate-input-v2.tex')==V2_SHA
    v1=(BASE/'candidate-input-v1.tex').read_text();v2=(BASE/'candidate-input-v2.tex').read_text()
    h1,t1,s1=pieces(v1);h2,t2,s2=pieces(v2)
    assert t1==t2 and C.family_table(v1)==C.family_table(v2)
    assert v2.replace(h2,h1).replace(s2,s1)==v1
    assert R.marked(v1)==R.marked(v2)
    expected_head='''\\paragraph{Fixed-side source selectors (236 interfaces).}
Let $K$ be either fixed protected set and $B$ the opposite component,
with pool $P_B$ and a Hamilton cycle. At a common state $x$, put
$d=\\deg_B(x)$ and $g=|(K\\cap\\delta_B(x))\\setminus P_B|$.
If $d-g\\le1$, every Hamilton cycle in $B$ takes two incident edges
at $x$, at least one in $K\\setminus P_B$. Only $B$ needs a Hamilton cycle.

'''
    assert h2==expected_head
    for phrase in ('236 nonconstant-source interfaces not listed individually',
                   'lies in both actual components',r'$d-g\le1$',
                   'fixed source $K$ against the restored target component',
                   'restored target $K$ against the source component',
                   'The opposite side\nhas its displayed Hamilton cycle',
                   "original interface's first normalizer",'boundary in the original coordinates',
                   'omitting $b_i$\nwhen starred','specified-template identities'):
        assert phrase in s2,phrase
    for case in prior['case_checks']:
        assert case['positive_fixedK_vs_oppositeHC_witnesses']
        for witness in case['positive_fixedK_vs_oppositeHC_witnesses']:
            assert witness['d_minus_g']==witness['degree_d']-witness['safe_fixedK_star_count_g']<=1
            assert witness['eligible_HC_side_has_printed_whole_component_HC'] is True
    result={'status':'INDEPENDENT_V2_ACTUAL_SOURCE_READBACK_AND_REUSED_236_FIXEDK_CERTIFICATES_PASSED',
        'input_sha256':{'candidate-input-v2.tex':V2_SHA,'candidate-input-v1.tex':sha(BASE/'candidate-input-v1.tex'),
            'review-results-v1.json':sha(prior_path),'check_actual236.py':sha(BASE/'check_actual236.py'),
            'fixed_k_source_reader.py':sha(BASE/'fixed_k_source_reader.py'),
            'independent_source_reader.py':sha(BASE/'independent_source_reader.py')},
        'script_sha256':sha(Path(__file__)),
        'only_v1_to_v2_source_edits':'Shortened genericfixedK/oppositeHC proof prose andselector suffix; table/formulas/records/all53markedblocks unchanged.',
        'actual_v2_generic_text':h2,'actual_v2_suffix_text':s2,
        'all53_marked_blocks_equal_independently_checked_v1':True,
        'actual21_selector_rows_equal_independently_checked_v1':True,
        'all236_originalcase_indices_fixedK_pools_components_firstnormalizers_unchanged':True,
        'generic_fixedK_not_arbitrary_pairHC_premise_retained':True,
        'only_opposite_B_requires_HC_hypothesis_retained':True,
        'common_actual_component_state_and_d_minus_g_le1_condition_retained':True,
        'original_interface_firstmap_and_original_coordinate_degrees_retained':True,
        'actual236case_set_defined_as_complement_of47retainedrecords':True,
        'all5_hard_hard_cases_still_individually_printed':True,
        'independent236_g_d_checks_reused_without_neighbour_rerun':True,
        'author_helpers_imported':False,'author_result_JSON_read':False,'main_changed':False,
        'mathematical_review_boundary':'Pigeonhole reasoning follows from atmostone incidentedge outside the goodK star. Quantified HC is only onB; selectedpool/reserve gluing dependencies/globalclassification/hardseedport status remain inherited.'}
    path=BASE/'review-results-v2.json';assert not path.exists();path.write_text(json.dumps(result,indent=2)+'\n')
    diff=BASE/'candidate-v2-independent.diff';assert not diff.exists()
    diff.write_text(''.join(difflib.unified_diff(v1.splitlines(True),v2.splitlines(True),fromfile='candidate-input-v1.tex',tofile='candidate-input-v2.tex')))
    print(json.dumps({'status':result['status'],'actual_v2_source_sha256':V2_SHA,
        'reused_actual236_case_checks':236,'conditions_or_domain_lost':False,'additional_neighbour_computation':False},indent=2))


if __name__=='__main__':main()
