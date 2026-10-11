"""Apply a reviewable manuscript dependency reduction without editing main."""
from pathlib import Path
import difflib
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[7]
EXPECTED = '3806a0c7f8ec374ea92e70152f939e92e35c3c76564f9e69e8c06160999bcb58'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    data = (ROOT / 'planar_recoloring_hamilton_thresholds.tex').read_bytes()
    assert digest(data) == EXPECTED
    old = data.decode()
    fragment = (HERE / 'symbolic-family-candidate.tex').read_text()
    anchor = '\\begin{lemma}[Protected-edge identities]\\label{lem:pentagon-protection}'
    assert old.count(anchor) == 1
    new = old.replace(anchor, fragment + '\n' + anchor)
    previous = '''For the 313 standard-source interfaces, the appendix gives 283
individual common edges and six constant-source parameter families
covering the other 30 cases. Checking the five-digit endpoints in
the specified cycles and outside their pools proves each individual
record. The six families follow from two possible normalizing
directions and four protected target edges, as shown there.'''
    replacement = '''For the 313 standard-source interfaces, the preceding local degree
bound supplies thirteen ordinary hard-source cases and one constant
target component. For the other cases, the appendix supplies 269
individual common edges and six constant-source parameter families
covering 30 cases. Checking the five-digit endpoints in the specified
cycles and outside their pools proves each needed individual record.
The appendix retains all 283 nonconstant-source records, including
the fourteen now supplied by the local bound. The six constant-source
families follow from two normalizing directions and four protected
target edges, as shown there.'''
    assert new.count(previous) == 1
    new = new.replace(previous, replacement)
    check_old = 'The constant-source cases are supplied by six parameter families; the other 283 retain individual edge records.'
    check_new = 'The constant-source cases are supplied by six parameter families; fourteen hard-source cases also follow from the local degree bound, leaving 269 individual edge records as proof premises. All 283 nonconstant-source records are retained in the appendix.'
    assert new.count(check_old) == 1
    new = new.replace(check_old, check_new)
    block_pattern = r'% BEGIN ([A-Z0-9-]+)\n(.*?)% END \1'
    old_blocks = dict(re.findall(block_pattern, old, re.S))
    new_blocks = dict(re.findall(block_pattern, new, re.S))
    assert old_blocks == new_blocks and len(old_blocks) == 53
    (HERE / 'main-input.tex').write_bytes(data)
    (HERE / 'local-family-manuscript-candidate.tex').write_text(new)
    (HERE / 'candidate.diff').write_text(''.join(difflib.unified_diff(old.splitlines(True), new.splitlines(True),
        fromfile='planar_recoloring_hamilton_thresholds.tex (phase8 v3)',
        tofile='local-family-manuscript-candidate.tex (phase9 separated)')))
    old_v1 = (HERE.parent / 'degree_pair_v1' / 'degree-pair-candidate.tex').read_text()
    assert old_v1.count('Each target has degree three') == 1
    new_v1 = old_v1.replace('Each target has degree three', 'Each specified target vertex has degree three')
    (HERE / 'degree-pair-v1-wording-corrected.tex').write_text(new_v1)
    (HERE / 'v1-wording-correction.diff').write_text(''.join(difflib.unified_diff(old_v1.splitlines(True), new_v1.splitlines(True),
        fromfile='degree_pair_v1/degree-pair-candidate.tex (preserved)',
        tofile='degree-pair-v1-wording-corrected.tex')))
    result = {'verdict': 'PASS', 'main_input_sha256': EXPECTED,
              'candidate_sha256': digest(new.encode()), 'marked_literal_blocks_exact': 53,
              'main_input_bytes': len(data), 'candidate_bytes': len(new.encode()),
              'byte_delta': len(new.encode()) - len(data),
              'individual_record_proof_premises_before': 283,
              'individual_record_proof_premises_after': 269,
              'literal_interface_records_retained': 283,
              'all_main_statements_and_old_labels_preserved': True,
              'live_main_edited': False,
              'v1_history_preserved_sha256': digest(old_v1.encode()),
              'v1_correction': 'Each specified target vertex has degree three'}
    (HERE / 'candidate-source-review.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
