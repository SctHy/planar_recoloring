"""Bind phase10's actual adopted manuscript and already completed reviews.

This script audits hashes and writes delivery metadata. It does not re-run the
236 mathematical checks or alter any manuscript or historical frozen packet.
"""
from pathlib import Path
import copy
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone

STAGE = Path(__file__).resolve().parent
RESEARCH = STAGE.parent
WORKSPACE = RESEARCH.parents[2]
SOURCE_HASH = 'b7a048389c00d075d733581bc98fbfd397765b384777e5959076264ab0dbd557'
PDF_HASH = '4f6bbe50a7fbfb853e367dd2674679e2b3e9c1eefc801eba7ff6a0e373dd496f'
NOW = datetime.now(timezone.utc).isoformat()

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read(path):
    return json.loads(path.read_text())

def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

audit = read(STAGE / 'source-verification.json')
assert audit['verdict'] == 'PASS' and audit['complete_partition'] == 313
assert audit['source_sha256'] == SOURCE_HASH and audit['pdf_sha256'] == PDF_HASH
for suffix, expected in [('tex', SOURCE_HASH), ('pdf', PDF_HASH)]:
    name = f'planar_recoloring_hamilton_thresholds.{suffix}'
    assert digest(WORKSPACE / name) == expected
    assert digest(STAGE / 'final' / name) == expected
    assert digest(STAGE / 'candidate-v2' / f'fixed-side-source-families-candidate-v2.{suffix}') == expected
    assert digest(STAGE / 'original' / name) == digest(RESEARCH / 'continuation-9' / 'final' / name)
info = subprocess.run(['/opt/homebrew/bin/pdfinfo', str(WORKSPACE / 'planar_recoloring_hamilton_thresholds.pdf')], text=True, capture_output=True, check=True).stdout
assert next(int(line.split(':', 1)[1]) for line in info.splitlines() if line.startswith('Pages:')) == 41
provenance = read(STAGE / 'integration-provenance.json')
for relative, expected in provenance['branch_records'].items():
    assert digest(RESEARCH / relative) == expected

invariants = read(RESEARCH / 'current-source-invariants.json')
invariants.update({
    'latest_stage': 'continuation-10',
    'files': {'planar_recoloring_hamilton_thresholds.tex': SOURCE_HASH, 'planar_recoloring_hamilton_thresholds.pdf': PDF_HASH},
    'pages': 41,
    'phase9_to_phase10_statements_byte_exact': 41,
    'phase9_to_phase10_unchanged_literal_blocks': 52,
    'phase9_to_phase10_changed_literal_blocks': ['INTERFACES-ALL'],
    'phase10_individual_interfaces': 47,
    'phase10_fixed_K_HC_selector_cases': 236,
    'phase10_constant_family_cases': 30,
    'phase10_complete_partition': 313,
    'phase10_selector_rows': 21,
    'phase10_selector_memberships': 78,
    'phase10_distinct_selector_words': 47,
    'phase10_all5_hardhard_individual': True,
    'historical_phase9_counts_retained_as_history': True,
    'last_live_hash_check_utc': NOW,
})
write(RESEARCH / 'current-source-invariants.json', invariants)

checkpoint = read(RESEARCH / 'research-checkpoint.json')
checkpoint.update({
    'stage': 'phase10 adopted; remaining47 simplification remains research',
    'delivered_pdf_pages': 41,
    'source_sha256': SOURCE_HASH,
    'pdf_sha256': PDF_HASH,
    'representative_protected_entries': 74,
    'remaining_individual_protected_records': 47,
    'next_active_research': 'Seek shorter reviewed analytic families for remaining28HC-HC+14mixed-hard+5hard-hard; do not repeat unsuccessful simple forced-star closure or equate finite coverage with a uniform theorem',
    'active_next_tasks': [
        'Assess remaining47 from frozen capacity/support/weak-port evidence for a genuinely shorter complete proof',
        'Preserve stronger phase9 arbitrary-twoHC local result and all frozen failures/UNKNOWN',
        'General planar girthfive fourcolour H/HC remains open',
    ],
    'latest_frozen_final': 'continuation-10/final',
    'latest_research_stage': 'continuation-10',
    'candidate_page_count': 41,
    'adopted_page_count': 41,
    'active_goal_status': 'paused',
    'goal_tool_status_at_user_resumption': 'paused',
    'goal_status_not_modified_by_agent': True,
    'work_continuation_authorization': 'User explicitly said go on after pausing; current work resumed under that instruction',
    'research_objective_complete': False,
    'representative_entries_counting_rule': '47individual+21state-selector rows+6constantparameter rows; heterogeneous entries, not number of actual checks',
    'current_goal_turn_classification': 'progress: independently reviewed236replacement adopted, actual41page source/PDF checked; sustained objective not complete',
    'updated_at_utc': NOW,
})
checkpoint['adopted'][2] = 'phase4 historical: six constant-source families plus283individual; currentphase10 keeps47individual+236local+30constant'
checkpoint['adopted'].append('236individualC5 witnesses replaced by21source-state rows andfixedK/oppositeHC d-g<=1 proof;313coverage retained, actual41pagePDF')
checkpoint['union_star_source_families'].update({
    'adopted': True,
    'historical_adoption_stage': 'continuation-9',
    'active_in_current_manuscript': False,
    'status': 'historically adopted42page125proof frozen; currentmanuscript uses fixedK/oppositeHC rule; stronger arbitrary-twoHC statement retained in phase9 records',
})
checkpoint['fixed_K_HC_selector_feasibility'].update({
    'adopted': True,
    'actual_remaining_individual': 47,
    'status': 'actualv2 independently reviewed236g/d/K/pool/firstmap cases; rootadopted41pagePDF/source audit andvisualQA PASS',
    'boundary': 'Only opposite wholeHC is arbitrary; fixedK side may be a hard seed. DP optimality is relative to frozen observation masks. Globalclassification/unchangedcertificates inherited.',
    'case_types': {'HC_HC': 202, 'hard_source_to_HC': 19, 'HC_source_to_hard': 15},
    'remaining_case_types': {'HC_HC': 28, 'hard_source_to_HC': 7, 'HC_source_to_hard': 7, 'hard_hard': 5},
})
checkpoint['general_protected_capacity']['historical_scope_note'] = 'This object records phase8 finite capacity research; manuscript_C5_certificate_changes false applies to that study, not later phase9/10 adoptions.'
checkpoint['reviewed_unadopted_candidates'][-1] = 'historicalphase7 complete path232 deletion-profile proof: independentPASS, two43page candidates unadopted; phase8layercapacity adopted, currentmain41pages'
write(RESEARCH / 'research-checkpoint.json', checkpoint)
write(STAGE / 'research-checkpoint.json', checkpoint)
snapshots = STAGE / 'current-snapshots'
snapshots.mkdir(exist_ok=True)
for name in ['current-source-invariants.json', 'research-checkpoint.json', '持续简化研究.md', '研究进展.md']:
    shutil.copyfile(RESEARCH / name, snapshots / name)

record = copy.deepcopy(read(RESEARCH / 'continuation-9' / 'computation-record.json'))
record['created_at_utc'] = NOW
record['task'] = {
    'file': 'task.md', 'sha256': digest(STAGE / 'task.md'),
    'object': 'Adopt and verify21source-state rows plusfixedK/oppositeHC rule replacing236individual C5 protected interfaces',
    'deliverables': [
        'Reviewed complete manuscript retaining313cases andoriginal thresholds/endpoints',
        'Actual adopted41page source/PDF, provenance andreview records frozen',
        'Stronger previous local result andfailed/UNKNOWN evidence preserved; sustained research not declared complete',
    ],
}
record['mathematical_context'] = {
    'assumptions': [
        'Retained global boundary/component classification andunmodified proofs',
        'FixedK onone side; opposite completecomponent B has a Hamiltoncycle',
        'Actual commoncomponent state, originalfirstmap, restoredK/pool andfull legal mutationdegree',
        'd-g<=1, whereg counts fixedK neighbors avoiding B pool',
        'Selected cycles retain their printed reserve/pool edges forunchanged globalgluing',
    ],
    'domain': '236nonconstant selected interfaces:202HC-HC+19hard-source+15hard-target;47individual+236local+30constant=313. Original theorem domains andprescribed endpoints unchanged.',
    'precision': {'mode': 'exact', 'working_digits': None, 'target_tolerance': ''},
}
record['implementation_discovery']['python']['existence_evidence'] = 'Actual root source/partition audits andindependent236reader executed successfully; thisrecordwriter checks delivery hashes only'
record['implementation_discovery']['python']['availability_evidence'] = 'Live CPython'+sys.version.split()[0]+'; priorindependent exact236run used3.14.6'
record['decision']['backend_version'] = sys.version.split()[0]
record['execution'] = {
    'status': 'complete', 'interface': 'local-cli',
    'command_or_input': 'python3 output/research/proof-simplification-20261010/continuation-10/check_adopted_source.py --source planar_recoloring_hamilton_thresholds.tex --pdf planar_recoloring_hamilton_thresholds.pdf --output output/research/proof-simplification-20261010/continuation-10/source-verification.json\n/Library/TeX/texbin/latexmk -pdf -interaction=nonstopmode -halt-on-error planar_recoloring_hamilton_thresholds.tex\npython3 output/research/proof-simplification-20261010/continuation-10/finalize_records.py',
    'code_artifact': 'check_adopted_source.py',
}
artifact_specs = [
    ('task.md', 'input'),
    ('original/planar_recoloring_hamilton_thresholds.tex', 'input'),
    ('original/planar_recoloring_hamilton_thresholds.pdf', 'input'),
    ('original/manifest.json', 'input'),
    ('check_adopted_source.py', 'code'),
    ('finalize_records.py', 'code'),
    ('candidate-v2-root-audit.json', 'result'),
    ('source-verification.json', 'result'),
    ('root-audit-first-attempt-failure.txt', 'log'),
    ('final/planar_recoloring_hamilton_thresholds.tex', 'result'),
    ('final/planar_recoloring_hamilton_thresholds.pdf', 'result'),
    ('final-latex.log', 'log'),
    ('adopted.diff', 'report'),
    ('integration-provenance.json', 'input'),
    ('pdf-visual-qa.json', 'result'),
    ('independent-review/report-v2.md', 'report'),
    ('independent-review/review-results-v1.json', 'input'),
    ('independent-review/review-results-v2.json', 'input'),
    ('independent-review/computation-record-v2.json', 'input'),
    ('independent-review/frozen-manifest-v2.json', 'input'),
    ('研究进展.md', 'report'),
    ('research-checkpoint.json', 'report'),
]
artifact_specs += [(f'tmp/pdfs/main-page-{page}.png', 'result') for page in [1, 22, 27, 40, 41]]
artifact_specs += [(f'current-snapshots/{name}', 'report') for name in ['current-source-invariants.json', 'research-checkpoint.json', '持续简化研究.md', '研究进展.md']]
record['artifacts'] = [{'path': name, 'role': role, 'sha256': digest(STAGE / name)} for name, role in artifact_specs]
record['result'] = {
    'status': 'complete',
    'summary': 'Phase10 delivery complete: actual main equals reviewedv2,21rows/78members/47words replace236individual witnesses;47+236+30=313,41statements/52otherblocks preserved,clean41pagePDF andfiveactualpages viewed. This does not complete the sustained research objective orresolve generalfourcolour planar girthfive H/HC.',
    'result_artifact': 'source-verification.json',
}
record['verification'] = {
    'methods': [
        'Handreview of fixedK/oppositeHC incident-count pigeonhole proof d-g<=1',
        'Independentactual236component/firstnormalizer/restoredK/pool/g/d checks; allhard-hard retained',
        'Independent8new fullcomponent closures plus15hash-bound ownprevious closures inherited',
        'Rootactual283minus47case complement,313partition,41statements/14originalprimaryresults/blocklemma/52blocks/normalizer/reference audit',
        'GuardedSHA-bound adoption andactualclean41pageTeX build',
        'Fiveaffected/representative actualmainPDF pages rendered andvisually inspected',
        'Currentdelivery hash/page checks andfrozenreview/schema/path binding',
    ],
    'evidence_level': 'exact-check',
    'residual_or_error': 'not applicable: exact finite sets andliteral source hashes',
    'limitations': [
        'Only opposite Hamiltoncycle is arbitrary; fixedK side usesprintedcycle/commonports. NotarbitrarytwoHC theorem.',
        'Globalclassification,hardseedCOMMON claims,47individual+30constant certificates andother proofs inherited.',
        'This finite replacement is not a proof ofgeneral planar girthfive fourcolour Hamiltonicity/HC.',
        'MaskDP minima are conditional onfrozenobservations; membership count reduction omitsK/pool/g/d/map checks.',
        'Internalreview is notexternalpeerreview/formalverification; recordvalidationchecks schema/paths/hashes only.',
        'FiveactualPDF pages inspected; otherlayoutsinherited. Englishlettertokens increased5 despite41page reduction.',
        'Goalbackend stillrecordedpaused atusergoon; agentdidnotchangestatus. Stagecomplete doesnotmeanresearchobjectivecomplete.',
        'NoformalMRS ormemoryupdate. Strongerphase9proof andfirstlocatorfailure retained.',
    ],
}
write(STAGE / 'computation-record.json', record)
manifest = {
    'schema_version': '1.0',
    'stage': 'continuation-10 actualadopted236replacement',
    'created_at_utc': NOW,
    'research_objective_complete': False,
    'user_authorized_work_continuation': 'go on',
    'goal_backend_status_at_resumption': 'paused',
    'files': [{'path': item['path'], 'sha256': item['sha256']} for item in record['artifacts']] + [{'path': 'computation-record.json', 'sha256': digest(STAGE / 'computation-record.json')}],
}
write(STAGE / 'frozen-manifest.json', manifest)
print(json.dumps({'delivery': 'PASS', 'pages': 41, 'partition': [47, 236, 30], 'record_artifacts': len(record['artifacts']), 'manifest_members': len(manifest['files']), 'python': sys.version.split()[0], 'record_sha256': digest(STAGE / 'computation-record.json'), 'manifest_sha256': digest(STAGE / 'frozen-manifest.json')}, ensure_ascii=False))
