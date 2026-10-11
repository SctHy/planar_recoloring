"""Save final selected evidence and provenance; validation is a separate step."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[7]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2) + '\n')


def main():
    old = (HERE / 'main-input.tex').read_text()
    new = (HERE / 'local-family-manuscript-candidate.tex').read_text()
    source_review = json.loads((HERE / 'candidate-source-review.json').read_text())
    local_review = json.loads((HERE / 'local-review-results.json').read_text())
    assert local_review['verdict'] == source_review['verdict'] == 'PASS'
    statement = r'\\begin\{(theorem|lemma|proposition|corollary)\}(.*?)\\end\{\1\}'
    assert re.findall(statement, old, re.S) == re.findall(statement, new, re.S)
    labels = re.findall(r'\\label\{([^}]+)\}', old)
    assert labels == re.findall(r'\\label\{([^}]+)\}', new)
    assert len(labels) == 55
    live = ROOT / 'planar_recoloring_hamilton_thresholds.tex'
    assert sha(live) == local_review['main_input_sha256']
    log = (HERE / 'local-family-manuscript-candidate.log').read_text()
    warnings = re.findall(r'^.*(?:Warning|Overfull|Underfull).*$', log, re.M)
    assert not warnings, warnings
    pages = re.findall(r'Output written on .*?\((\d+) pages,', log)
    assert pages == ['43']
    write('candidate-build-review.json', {
        'verdict': 'PASS', 'candidate_sha256': sha(HERE / 'local-family-manuscript-candidate.tex'),
        'pdf_sha256': sha(HERE / 'local-family-manuscript-candidate.pdf'),
        'compile_exit_code': 0, 'final_warnings': warnings,
        'primary_statement_count_exact': len(re.findall(statement, old, re.S)),
        'marked_literal_blocks_exact': 53, 'old_labels_exact': len(labels),
        'pages_before': 42, 'pages_after': 43,
        'source_bytes_delta': source_review['byte_delta'],
        'visual_pages_checked': [22, 23],
        'visual_findings': 'alternatives and family tables legible, aligned and unclipped; adjoining proof normal',
        'proof_dependency_reduction': '14 individual records replaced by 13 ordinary local families and 1 constant-component family',
        'adoption_recommendation': 'retain research candidate; do not adopt solely for manuscript shortening',
        'live_main_unchanged': True,
        'evidence_boundary': 'source delta, exact literal/statements/labels and build/layout review; not theorem completion'})
    v1 = HERE.parent / 'degree_pair_v1' / 'degree-pair-candidate.tex'
    assert sha(v1) == 'fb17932a530cf3d070fef987bfeac742a19cdea65a50d916726fd97014bd1f5b'
    write('provenance.json', {
        'phase6_source_sha256': sha(HERE / 'phase6-source.tex'),
        'main_input_sha256': sha(HERE / 'main-input.tex'),
        'live_main_sha256_at_final_readback': sha(live),
        'existing_author_script_sha256': sha(HERE / 'check_four_center_families.py'),
        'existing_author_result_sha256': sha(HERE / 'one-change-family-results.json'),
        'author_generator_rerun_in_this_continuation': False,
        'author_execution_metadata': 'inherited existing output; original invocation and runtime were not reconstructed',
        'previous_two_center_result_sha256': sha(HERE / 'previous-two-center-results.json'),
        'previous_two_center_copy_matches_v2_bytes': True,
        'independent_reader_sha256': sha(HERE / 'review_four_center_families.py'),
        'independent_readback_result_sha256': sha(HERE / 'local-review-results.json'),
        'independent_readback_basis': 'separate implementation directly tests one-coordinate legality; no original code import',
        'preserved_v1_candidate_sha256': sha(v1),
        'v1_wording_correction_kept_separate': True,
        'all_C5_marked_literal_blocks_unchanged': True,
        'no_live_main_edit': True,
        'scope': 'fixed four-center local readback; three centers suffice for 13 ordinary and 1 constant-component proof family'})
    roles = {
        'phase6-source.tex': 'input', 'main-input.tex': 'input',
        'previous-two-center-results.json': 'input', 'one-change-family-results.json': 'input',
        'task.md': 'report', 'check_four_center_families.py': 'code',
        'review_four_center_families.py': 'code', 'create_separated_candidate.py': 'code',
        'finalize_records.py': 'code', 'local-review-results.json': 'result',
        'symbolic-family-candidate.tex': 'report', 'local-family-manuscript-candidate.tex': 'report',
        'local-family-manuscript-candidate.pdf': 'report', 'candidate.diff': 'report',
        'candidate-source-review.json': 'result', 'candidate-build-review.json': 'result',
        'degree-pair-v1-wording-corrected.tex': 'report', 'v1-wording-correction.diff': 'report',
        'report.md': 'report', 'provenance.json': 'provenance',
        'candidate-latexmk-output.txt': 'result', 'candidate-text.txt': 'result',
        'candidate-proof-22.png': 'report', 'candidate-proof-23.png': 'report'}
    discovery = {
        'mathematica': {'candidate_implementations': ['finite exact set operations for local legal neighbours'],
            'existence_evidence': 'general exact set operations suffice; a CAS implementation is not needed',
            'local_availability': 'unavailable',
            'availability_evidence': 'current-host backend inventory cache hit 2026-10-09T20:19:58.944412+00:00 records no installation or executable'},
        'sagemath': {'candidate_implementations': ['finite exact set operations for local legal neighbours'],
            'existence_evidence': 'general exact set operations suffice; a CAS implementation is not needed',
            'local_availability': 'unavailable',
            'availability_evidence': 'same current-host inventory records native sage unavailable'},
        'python': {'candidate_implementations': ['stdlib direct-legality readback of immediate recolourings and primary literal pools'],
            'existence_evidence': 'review_four_center_families.py executed the separate direct-legality reader',
            'local_availability': 'available',
            'availability_evidence': 'live Python 3.14.6 and completed 60-row exact local readback'}}
    record = {'schema_version': '1.0', 'created_at_utc': datetime.now(timezone.utc).isoformat(),
        'task': {'file': 'task.md', 'sha256': sha(HERE / 'task.md'),
            'object': 'four-center exact local premise review and analytic 13 ordinary plus 1 constant-component protected families',
            'deliverables': ['symbolic local degree proof and parameter table', 'separate manuscript candidate and diff',
                'v1 wording correction without historical edit', 'review, provenance and computation record']},
        'mathematical_context': {
            'assumptions': ['target Hamilton cycle spans the component containing the legal witness vertex',
                'source K is actual phase6 COMMON or PORTS minus its two-edge pool',
                'target pool is restored by the manuscript prescribed first normalizer',
                'hard target seeds do not imply whole-target Hamilton cycles',
                'all simultaneous colour and coordinate images transport the pools as well as boundaries'],
            'domain': '60 saved one-coordinate local rows for four fixed vertices; positive union is 13 ordinary targets and constant component1 only',
            'precision': {'mode': 'exact', 'working_digits': None, 'target_tolerance': ''}},
        'implementation_discovery': discovery,
        'decision': {'selected_backend': 'python', 'backend_version': local_review['python_version'],
            'selection_reason': 'Python-native frozen inputs and independently auditable direct-legality reader; at most1200 immediate candidates, no state graph',
            'fallback_reason': 'Mathematica and Sage unavailable in current-host inventory; exact Python stdlib is sufficient'},
        'execution': {'status': 'complete', 'interface': 'local-cli',
            'command_or_input': 'python3 -B review_four_center_families.py; python3 -B create_separated_candidate.py; latexmk -pdf -interaction=nonstopmode -halt-on-error local-family-manuscript-candidate.tex; python3 -B finalize_records.py',
            'code_artifact': 'review_four_center_families.py'},
        'artifacts': [{'path': name, 'role': role, 'sha256': sha(HERE / name)} for name, role in roles.items()],
        'result': {'status': 'complete', 'summary': 'All60 frozen local rows agree with a separate direct-legality reader. A mathematical cycle-degree bound proves13 ordinary plus1 constant-component families; three centers suffice. Candidate lowers individual proof premises283 to269, preserves53 literal blocks,41 statements and55 labels, but grows42 to43pages; main unchanged.',
            'result_artifact': 'local-review-results.json'},
        'verification': {'methods': ['mathematical cycle-degree proof and forbidden-colour formula',
            'direct one-coordinate legality readback independent of author B_i neighbour generation',
            'primary hardK, first normalizer and literal pool membership checks for60 local rows',
            'exact saved-v2 byte and inherited-row identity', '14 local families uniquely matched to existing283 records',
            'exact unchanged53 marked blocks,41 statements and55 labels',
            'successful warning-free compilation and visual review of modified pages22 and23'],
            'evidence_level': 'proof-certificate', 'residual_or_error': 'exact arithmetic; raw-only and inconclusive cases explicitly excluded',
            'limitations': ['fixed first-normalizer source-hard pools only; arbitrary target pools or opponent maps are not covered',
                'no all53 hard-interface claim; no313 case rerun', 'constant component1 only',
                'hard target whole-HC conclusions excluded; illegal witness or zero degree bound is inconclusive',
                'original author generator not rerun; its execution metadata not reconstructed',
                'no fibre graph, Hamilton search, opponent cycle edge set or retention number',
                'proof dependencies reduced, but the candidate adds2735 TeX bytes and one PDF page',
                'record validation checks schema and hashes, not mathematics or external independent peer review']}}
    write('computation-record.json', record)
    print(json.dumps({'record_written': True, 'artifact_count': len(roles),
                      'candidate_sha256': sha(HERE / 'local-family-manuscript-candidate.tex'),
                      'pdf_sha256': sha(HERE / 'local-family-manuscript-candidate.pdf'),
                      'record_sha256': sha(HERE / 'computation-record.json')}, indent=2))


if __name__ == '__main__':
    main()
