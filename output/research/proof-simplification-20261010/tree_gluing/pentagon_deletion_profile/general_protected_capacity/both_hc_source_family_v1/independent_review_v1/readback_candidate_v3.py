#!/usr/bin/env python3
"""Read actual v3 and reuse unchanged independently checked27 inputs."""
from pathlib import Path
import difflib
import hashlib
import json
import re
import check_actual_sources as independent_reader

BASE=Path(__file__).resolve().parent
V3_SHA='505c432f4a18a36056f50f5ba1a56ac4513ca02aa64520580d4de64b3dfff62f'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def take_paragraph(text,start,end):
    a=text.index(start);b=text.index(end,a)+len(end)
    return text[a:b]


def main():
    v3_path=BASE/'candidate-input-v3.tex'
    prior_path=BASE/'review-results-v2.json'
    assert sha(v3_path)==V3_SHA
    prior=json.loads(prior_path.read_text())
    assert prior['script_sha256']==sha(BASE/'check_actual_sources.py')
    assert prior['status']=='INDEPENDENT_ACTUAL_SOURCE_27_FAMILY_CHECK_PASSED'
    for name,h in prior['input_sha256'].items():assert sha(BASE/name)==h
    ref=(BASE/'reference-phase8.tex').read_text()
    v2=(BASE/'candidate-input-v2.tex').read_text()
    v3=v3_path.read_text()
    ref_blocks=independent_reader.marked(ref)
    v2_blocks=independent_reader.marked(v2)
    v3_blocks=independent_reader.marked(v3)
    assert len(v3_blocks)==53 and set(v3_blocks)==set(ref_blocks)
    assert v3_blocks==v2_blocks
    assert sum(v3_blocks[n]==ref_blocks[n] for n in ref_blocks)==52
    assert independent_reader.family_table(v3)==independent_reader.family_table(v2)
    convention=r'Here is the exact normalization convention\.(.*?)In particular a standard boundary first normalizes by the identity\.'
    assert re.search(convention,v3,re.S).group(0)==re.search(convention,ref,re.S).group(0)
    assert 'lem:c5-one-boundary-local' not in v3 and 'ordinary components' not in v3
    assert 'the other 283 retain individual edge records' not in v3
    assert 'three-edge incident unions, leaving 256 individual edge records' in v3
    old_proof=take_paragraph(ref,'For the 313 standard-source interfaces,','\\end{proof}')
    new_proof=take_paragraph(v3,'For the 313 standard-source interfaces,','\\end{proof}')
    old_note=take_paragraph(ref,'The finite data used for the endpoint-sensitive statements','These are bounded certificate replays, not arbitrary-size graph searches.')
    new_note=take_paragraph(v3,'The finite data used for the endpoint-sensitive statements','These are bounded certificate replays, not arbitrary-size graph searches.')
    old_note_phrase='The constant-source cases are supplied by six parameter families; the other 283 retain individual edge records.'
    new_note_phrase='Six constant-source families cover 30 cases; two further source families cover 27 by three-edge incident unions, leaving 256 individual edge records.'
    assert new_note==old_note.replace(old_note_phrase,new_note_phrase)
    family_start=v3.index('\\paragraph{Two source families (27 interfaces).}')
    family_end=v3.index('\\paragraph{The 256 remaining individual nonconstant-source interfaces.}',family_start)
    family_text=v3[family_start:family_end]
    normalized=v3.replace(new_proof,old_proof).replace(new_note,old_note)
    normalized=normalized.replace(family_text,'')
    normalized=normalized.replace('\\paragraph{The 256 remaining individual nonconstant-source interfaces.}',
                                  '\\paragraph{The 283 nonconstant-source interfaces.}')
    normalized=normalized.replace(v3_blocks['INTERFACES-ALL'],ref_blocks['INTERFACES-ALL'])
    # Removing the inserted paragraph leaves its original leading blank line.
    assert normalized==ref,'unrelated manuscript change outside the declared regions'
    for c in prior['case_checks']:
        assert c['positive_witnesses']
        for w in c['positive_witnesses']:
            assert w['full_incident_star_union_count']==w['ds_plus_alpha']==3
            assert w['f']==0 and w['common_pool_incident_edges']==[]
    diff_path=BASE/'candidate-v3-independent.diff'
    assert not diff_path.exists()
    diff_path.write_text(''.join(difflib.unified_diff(ref.splitlines(True),v3.splitlines(True),
        fromfile='reference-phase8.tex',tofile='candidate-input-v3.tex')))
    output={'status':'INDEPENDENT_V3_SOURCE_READBACK_AND_REUSED_27_CERTIFICATES_PASSED',
        'input_sha256':{'candidate-input-v3.tex':sha(v3_path),'reference-phase8.tex':sha(BASE/'reference-phase8.tex'),
            'candidate-input-v2.tex':sha(BASE/'candidate-input-v2.tex'),'review-results-v2.json':sha(prior_path)},
        'script_sha256':sha(Path(__file__)),
        'v2_independent_checker_sha256':sha(BASE/'check_actual_sources.py'),
        'actual_v3_family_text':family_text,
        'all53_marked_blocks_equal_v2':True,'other52_blocks_equal_phase8':True,
        'source_words_degrees_J_equal_v2':True,'first_normalizer_convention_equal_phase8':True,
        'remaining256_interface_rows_equal_v2':True,'independent27_original_case_indices_reused':True,
        'all27_have_selected_witness_with_full_star_union3_and_common_pool_f0':True,
        'numeric_bound_numbered_lemma_removed':True,'old283_count_fixed':True,
        'all_other_manuscript_bytes_equal_phase8_after_declared_edits':True,
        'author_helpers_imported':False,'author_result_JSON_read':False,
        'neighbour_computation_repeated_for_v3':False,'main_changed':False,
        'proof_boundary':'The actual v3 common-edge argument is reviewed separately in report. f0 means no common incident edge is in either pool; it need not exclude pool edges from the entire star union. Product gluing still uses the specified cycles containing their printed pool/reserve edges.'}
    path=BASE/'review-results-v3.json'
    assert not path.exists()
    path.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({'status':output['status'],'actual_v3_sha256':V3_SHA,
        'other_marked_blocks_equal':52,'reused_independent_case_checks':27,
        'unrelated_source_edits':False},indent=2))


if __name__=='__main__':
    main()
