"""Bind selected v2 artifacts to their existing v1/prior-review inputs."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

HERE = Path(__file__).resolve().parent
BASE = HERE.parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2) + '\n')


def main():
    result = json.loads((HERE / 'forced-outside-capacity-results.json').read_text())
    assert result['status'] == 'PASS_EXACT_LOCAL_FORCED_OUTSIDE_CAPACITY'
    assert result['summary']['interfaces'] == 230
    for name, expected in result['v1_digests_preserved'].items():
        assert sha(BASE / 'degree_aggregate_v1' / name) == expected
    write('provenance.json', {
        'input_storage': 'existing sibling artifacts reused; no input copies or v1 edits',
        'artifact_base_directory_for_record_validation': str(BASE),
        'v1_files_preserved': result['v1_digests_preserved'],
        'complete_fibre_assurance': result['complete_fibre_evidence'],
        'node125_comparison_input': {
            'path': 'one_sided_degree_v1/independent_local_review/both-hc-local-results.json',
            'sha256': result['node_comparison_input_sha256'],
            'used_fields': 'covered flags and interface scalar identities only; not selected edge sets'},
        'v1_interface_input_fields_used': ['source', 'target', 'changed_position', 'new_colour', 'normalizer', 'group'],
        'source_blocks_used': 'C1/FHC unordered vertex sets and POOL endpoint pairs; cycle order discarded',
        'selected_source_or_target_cycle_edges_used_for_bound': False,
        'source_degree_two_forced_edges': 'derived from local full-source graph degree, not a selected source cycle',
        'full_state_set_enumeration_replayed': False,
        'new_exact_local_mutations': result['summary']['local_coordinate_mutations_tested'],
        'main_edited': False,
        'new_beyond125': result['summary']['new_beyond125']})
    own = {'task.md': 'report', 'check_forced_outside_capacity.py': 'code',
           'forced-outside-capacity-results.json': 'result', 'analytic-capacity-candidate.tex': 'report',
           'report.md': 'report', 'provenance.json': 'provenance', 'finalize_records.py': 'code'}
    roles = {'degree_aggregate_v2/' + name: role for name, role in own.items()}
    roles.update({'degree_aggregate_v1/' + name: 'input' for name in result['v1_digests_preserved']})
    roles.update({'independent_root_review/review-results.json': 'input',
                  'one_sided_degree_v1/independent_local_review/both-hc-local-results.json': 'input'})
    discovery = {}
    for backend in ('mathematica', 'sagemath'):
        discovery[backend] = {'candidate_implementations': ['exact finite set/degree operations'],
            'existence_evidence': 'general exact operations suffice; CAS is unnecessary for these Python-native frozen artifacts',
            'local_availability': 'unavailable',
            'availability_evidence': 'current-host ReadOrCreate inventory cache dated2026-10-09T20:19:58.944412+00:00 records no executable'}
    discovery['python'] = {'candidate_implementations': ['stdlib exact local adjacency and forced outside-degree capacities'],
        'existence_evidence': 'check_forced_outside_capacity.py completed the230 requested fixed-interface bounds',
        'local_availability': 'available', 'availability_evidence': 'live Python3.14.6, successful actual run'}
    record = {'schema_version': '1.0', 'created_at_utc': datetime.now(timezone.utc).isoformat(),
        'task': {'file': 'degree_aggregate_v2/task.md', 'sha256': sha(HERE / 'task.md'),
            'object': 'forced internal-outside graph-degree capacity bound for arbitrary source and target Hamilton cycles',
            'deliverables': ['analytic inequality and optimal single-edit selector proof',
                'exact230-interface results', 'comparison with125 node cases', 'provenance and computation record']},
        'mathematical_context': {'assumptions': ['both cycles are arbitrary Hamilton cycles of their full components',
            'common-endpoint recolouring edges coincide', 'fixed source and prescribed restored target pools',
            'J has a source-degree-two endpoint on every edge, so every source Hamilton cycle contains J',
            'source HC existence implies d_J<=2', 'optimal selector requires one changed non-star boundary coordinate',
            'complete supplied vertex sets inherit the source-bound earlier313-case verification'],
            'domain': '230 fixed ordinary full fibre component interfaces; hard port-seed and constant-source cases excluded',
            'precision': {'mode': 'exact', 'working_digits': None, 'target_tolerance': ''}},
        'implementation_discovery': discovery,
        'decision': {'selected_backend': 'python', 'backend_version': result['python'],
            'selection_reason': 'exact stdlib operations over frozen Python-native vertex/pool inputs; no solver or state enumeration needed',
            'fallback_reason': 'Mathematica/Sage executables unavailable in current-host inventory; exact Python is adequate'},
        'execution': {'status': 'complete', 'interface': 'local-cli',
            'command_or_input': 'python3 -B degree_aggregate_v2/check_forced_outside_capacity.py; python3 -B degree_aggregate_v2/finalize_records.py; validate record with --base-dir general_protected_capacity',
            'code_artifact': 'degree_aggregate_v2/check_forced_outside_capacity.py'},
        'artifacts': [{'path': name, 'role': role, 'sha256': sha(BASE / name)} for name, role in roles.items()],
        'result': {'status': 'complete', 'summary': 'Optimal selector expands97 to125, exactly matching node125 case identities. Forced internal-O capacities do not add covered cases; they raise1 to2 guaranteed common safe edges for two00123 interfaces. Largest bound6. Old00101 pos0->1 stayszero. Allv1 hashes preserved.',
            'result_artifact': 'degree_aggregate_v2/forced-outside-capacity-results.json'},
        'verification': {'methods': ['analytic common-incidence inequality for arbitrary full-component Hamilton cycles',
            'source degree-two forces J and source Hamilton degree2 bounds remaining outside capacity',
            'single-edit optimal selector proof and original-node equivalence',
            'exact local legality, full-neighbour closure, first normalizer and common-pool readback',
            'all230 new bound cases compared with stored125 node identities',
            'v1 six input/code/result hashes unchanged before and after execution'],
            'evidence_level': 'proof-certificate', 'residual_or_error': 'exact integer operations; no additional positive cases from J on this finite range',
            'limitations': ['conditional inequality is general; optimal selector specifically uses a single non-star boundary edit',
                'positive counts only for230 supplied ordinary full components and fixed pools',
                'hard port seeds are not whole-component Hamilton cycles',
                'complete-state assurance inherited from prior source-bound review, not replayed',
                'only local immediate-neighbour tables are generated; no palette^5 enumeration, Hamilton search or selected C/D intersections',
                'no all-interface or arbitrary-size theorem completion and no main edit',
                'record validator requires --base-dir general_protected_capacity because sibling inputs are reused',
                'record validator checks schema and hashes, not mathematical semantics or external peer review']}}
    write('computation-record.json', record)
    print(json.dumps({'record_written': True, 'artifact_count': len(roles),
                      'result_sha256': sha(HERE / 'forced-outside-capacity-results.json'),
                      'record_sha256': sha(HERE / 'computation-record.json')}, indent=2))


if __name__ == '__main__':
    main()
