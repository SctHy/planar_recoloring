#!/usr/bin/env python3
"""Bind completed saved-mask feasibility outputs; do not replay computations."""
from pathlib import Path
import hashlib
import json
import platform
import shutil
import sys

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
PREFIX = HERE.name + '/'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run():
    assert platform.python_version() == '3.14.6'
    assert not (HERE / 'frozen-manifest-v1.json').exists()
    result = json.loads((HERE / 'saved-one-protected-selector-results.json').read_text())
    small = json.loads((HERE / 'small-mask-verification.json').read_text())
    assert result['status'] == small['status'] == 'PASS'
    for name, digest in result['input_sha256'].items():
        assert sha(BASE / name) == digest
    inventory_source = Path('/private/var/folders/60/c_yt4kyd5mv8gr_wfcbmq96c0000gn/T/Codex/math-science-computation/backend-inventory.json')
    inventory = HERE / 'backend-inventory-snapshot.json'
    assert not inventory.exists()
    shutil.copyfile(inventory_source, inventory)
    inputs = ['one_protected_vs_hc_v2/symmetric-one-sided-results-v2.json',
              'one_protected_vs_hc_v2/check_symmetric.py',
              'one_protected_vs_hc_v2/phase6-source.tex',
              'one_protected_vs_hc_v2/computation-record.json',
              'union_star_families_v1/union-source-cover-results.json',
              'union_star_families_v1/find_union_covers.py']
    provenance = {'scope': 'Saved observation masks only; no graph, normalizer or Hamilton search.',
                  'inputs': {name: sha(BASE / name) for name in inputs},
                  'original_first_map_policy': 'Copy each interface mapping exactly; never call a normalizer.',
                  'review': 'Analytic incident-count lemma and per-source same-mask dominance reviewed; independent peer confirmed F/R fixed-side quantifiers.',
                  'primary': {'python': result['python'], 'elapsed_seconds': result['elapsed_seconds']},
                  'small_subset_check': small['independent_exhaustive_subset_checks'],
                  'main_policy': 'Main and all earlier frozen artifacts were not edited.'}
    (HERE / 'provenance.json').write_text(json.dumps(provenance, indent=2)+'\n')
    record_path = HERE / 'computation-record.json'
    record = json.loads(record_path.read_text())
    assert record['task']['sha256'] == sha(HERE / 'task.md')
    record['task'].update(file=PREFIX+'task.md',
                         object='Bounded exact per-source word-mask minimum covers from frozen bidirectional one-fixed-K observations',
                         deliverables=['saved-mask optimizer and independent small-subset checker',
                                       'actual236 coverage with original F/R directions and first maps',
                                       'literal feasibility comparison against current125 selectors',
                                       'validated computation record and immutable manifest'])
    record['mathematical_context'].update(
        assumptions=['Only the opposite component HC is arbitrary; the protected K side remains fixed.',
                     'Safe fixed edges exclude both prescribed pools using frozen observations.',
                     'All original interface first maps and component identities are retained without recalculation.',
                     'Current125 baseline is compared by exact original interface identity.',
                     'Candidate words are restricted to frozen positive local observations.'],
        domain='313 frozen original interfaces; optimize236 covered nonconstant cases,111 extras, and111 extras retaining48 old memberships; at most15 covered cases per source',
        precision={'mode': 'exact', 'working_digits': None, 'target_tolerance': ''})
    record['implementation_discovery'] = {
        'mathematica': {'candidate_implementations': ['exact finite bitmask DP'],
                       'existence_evidence': 'General exact finite set operations suffice; no CAS-specific semantics needed.',
                       'local_availability': 'unavailable',
                       'availability_evidence': 'Current ReadOrCreate inventory cache reports no Mathematica installation or wolframscript.'},
        'sagemath': {'candidate_implementations': ['exact finite bitmask DP'],
                    'existence_evidence': 'General exact finite set operations suffice; no algebraic graph backend needed.',
                    'local_availability': 'unavailable',
                    'availability_evidence': 'Current ReadOrCreate inventory cache reports native Sage unavailable.'},
        'python': {'candidate_implementations': ['stdlib integer bitmasks and exact subset DP', 'itertools combinations for two small independent checks'],
                   'existence_evidence': 'Both delivered programs completed and saved PASS results.',
                   'local_availability': 'available',
                   'availability_evidence': f'Actual live execution CPython{platform.python_version()}, executable{sys.executable}.'}}
    record['decision'] = {'selected_backend': 'python', 'backend_version': platform.python_version(),
                          'selection_reason': 'Python-native frozen JSON and stdlib integer masks give auditable exact per-source covers; at most2^15 masks and no graph or CAS routines.',
                          'fallback_reason': 'No local Mathematica or Sage executable is recorded; exact Python integer operations suffice and no external CAS was requested.'}
    record['execution'] = {'status': 'complete', 'interface': 'local-cli',
                           'command_or_input': 'python3 -B one_protected_selector_feasibility_v1/find_saved_one_protected_covers.py; then python3 -B one_protected_selector_feasibility_v1/check_small_saved_masks.py (from common base directory)',
                           'code_artifact': PREFIX+'find_saved_one_protected_covers.py'}
    own = [('task.md', 'input'), ('backend-inventory-snapshot.json', 'input'),
           ('find_saved_one_protected_covers.py', 'code'), ('check_small_saved_masks.py', 'code'),
           ('saved-one-protected-selector-results.json', 'result'),
           ('small-mask-verification.json', 'result'), ('feasibility.md', 'report'),
           ('provenance.json', 'report'), ('freeze_metadata.py', 'code')]
    record['artifacts'] = [dict(path=PREFIX+name, role=role, sha256=sha(HERE/name))
                           for name, role in own] + [dict(path=name, role='input', sha256=sha(BASE/name))
                                                     for name in inputs]
    record['result'] = {'status': 'complete',
                        'summary': '236cases:21source rows,78 minimum memberships,47 distinct words,residual47. Extra111:18rows,64memberships,42distinct. Keeping old48memberships already supports34 extras; exact44 additions give92 total memberships,48 distinct words,21rows,residual47.',
                        'result_artifact': PREFIX+'saved-one-protected-selector-results.json'}
    record['verification'] = {
        'methods': ['All saved10706 F and10808 R observations: exact scalar and list-count readback; no graph recalculation.',
                    '313 identity uniqueness, exact236 positive count,125 containment,111 extras, witness cover and unchanged input hash assertions.',
                    'Mathematical same-mask dominance proves per-source DP recurrence minimum within the frozen word universe.',
                    'Independent exhaustive combinations recover exact minima and lexicographic first subsets for two small hard-source mask families.',
                    'Zero-addition boundary checks for retained selectors at00121 and00124.',
                    'Generic2+g-d counting lemma and fixed-side F/R quantifiers reviewed separately from record validation.'],
        'evidence_level': 'bounded-check', 'residual_or_error': 'not-applicable: exact integer masks and counts',
        'limitations': result['limits']+['No Main edit or full candidate.',
                                       'Component completeness and actual K/pool incidence are inherited from the frozen author observations, not established by this DP.',
                                       'Schema/hash validation does not rerun the optimizer or prove any mathematical implication.']}
    record_path.write_text(json.dumps(record, indent=2)+'\n')
    print(json.dumps({'record_sha256': sha(record_path), 'result_sha256': sha(HERE/'saved-one-protected-selector-results.json'),
                      'inputs_unchanged': True}))


if __name__ == '__main__':
    run()
