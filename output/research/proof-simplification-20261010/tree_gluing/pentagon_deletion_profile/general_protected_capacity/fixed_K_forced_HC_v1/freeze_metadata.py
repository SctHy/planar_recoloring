#!/usr/bin/env python3
"""Freeze completed phase11 metadata; no graph or closure replay."""
from pathlib import Path
import hashlib
import json
import platform
import shutil
import sys

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
PREFIX = HERE.name+'/'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run():
    assert platform.python_version() == '3.14.6'
    assert not (HERE/'frozen-manifest-v1.json').exists()
    x = json.loads((HERE/'fixed-K-forced-HC-results.json').read_text())
    short = json.loads((HERE/'short-forcing-chain-verification.json').read_text())
    assert x['status'] == short['status'] == 'PASS'
    for name, digest in x['input_sha256'].items():
        assert sha(BASE/name) == digest
    snapshot = HERE/'backend-inventory-snapshot.json'
    assert not snapshot.exists()
    shutil.copyfile('/private/var/folders/60/c_yt4kyd5mv8gr_wfcbmq96c0000gn/T/Codex/math-science-computation/backend-inventory.json', snapshot)
    inputs = list(x['input_sha256'])+['forced_star_closure_v1/computation-record.json',
                                    'one_protected_vs_hc_v2/computation-record.json']
    provenance = {'inputs': {name: sha(BASE/name) for name in inputs},
                  'main_policy': 'Main and existing frozen artifacts not edited.',
                  'actual_computation': {'only_graph': '00123', 'vertices': 57,
                                         'full_edges': 122, 'closure_runs': 1,
                                         'local_saved_observations': 41,
                                         'interfaces_directly_checked': 3,
                                         'interfaces_settled_by_negative_lemma': 39,
                                         'python': x['python'], 'seconds': x['elapsed_seconds']},
                  'independent_check': 'Four direct local stars, hard protected-K port membership, two pools and original recorded map only.',
                  'mathematical_review': 'Fixed-K necessary-edge lower bound and no-exclusion negative lemma read separately; independent peer confirmed endpoint-completeness reasoning.',
                  'evidence_scope': 'One new positive fixed-K/any-opposite-HC mixed interface; other41 eligible unchanged and5hard/hard excluded.'}
    (HERE/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
    p = HERE/'computation-record.json'
    r = json.loads(p.read_text())
    assert r['task']['sha256'] == sha(HERE/'task.md')
    r['task'].update(file=PREFIX+'task.md',
                     object='Fixed protected K against forced/allowed necessary HC stars on42 remaining eligible interfaces, with only00123 graph recalculated',
                     deliverables=['sound positive criterion and no-exclusion negative lemma',
                                   'one-graph exact computation and41 saved-star comparisons',
                                   'four-star analytic port proof and independent premise checks',
                                   'scope report and validated metadata'])
    r['mathematical_context'].update(
        assumptions=['HC existence only on the whole-component ordinary side, inherited from frozen manuscript context.',
                     'The opposite K is specified and excludes its own pool; safe incidences exclude the HC-side fixed pool.',
                     'All original first maps retained without renormalization.',
                     'Frozen18 no-exclusion graph summaries and complete negative one-sided endpoint observations support the analytic negative boundary.'],
        domain='47 remaining nonconstant identities:28ordinary/ordinary,14mixed,5hard/hard;42eligible;39 settled analytically,3mixed checked on00123 using41 local observations',
        precision={'mode': 'exact', 'working_digits': None, 'target_tolerance': ''})
    r['implementation_discovery'] = {
        'mathematica': {'candidate_implementations': ['exact finite graph-set necessity closure'],
                       'existence_evidence': 'Finite set operations could implement the rule; no CAS-specific requirement.',
                       'local_availability': 'unavailable', 'availability_evidence': 'Current backend inventory records no Mathematica executable.'},
        'sagemath': {'candidate_implementations': ['exact finite graph-set necessity closure'],
                    'existence_evidence': 'Finite graph operations could implement the rule; no specialist Sage semantics required.',
                    'local_availability': 'unavailable', 'availability_evidence': 'Current backend inventory records native Sage unavailable.'},
        'python': {'candidate_implementations': ['stdlib legal-word graph, simultaneous undirected force/exclude closure, saved-map edge restoration',
                                                'separate direct-coordinate four-star premise checker'],
                   'existence_evidence': 'Both delivered scripts completed with retained PASS outputs.',
                   'local_availability': 'available', 'availability_evidence': f'Actual material CPython{platform.python_version()}, executable{sys.executable}.'}}
    r['decision'] = {'selected_backend': 'python', 'backend_version': platform.python_version(),
                     'selection_reason': 'Frozen evidence is Python-native; exact stdlib sets suffice for one57-vertex graph and41 recorded stars. No whole previous computation replay is needed.',
                     'fallback_reason': 'No local Mathematica or Sage executable available in the current inventory; exact Python operations suffice and no external CAS was requested.'}
    r['execution'] = {'status': 'complete', 'interface': 'local-cli',
                      'command_or_input': 'python3 -B fixed_K_forced_HC_v1/check_three_changed_HC_interfaces.py; then python3 -B fixed_K_forced_HC_v1/check_short_forcing_chain.py (from common base)',
                      'code_artifact': PREFIX+'check_three_changed_HC_interfaces.py'}
    own = [('task.md','input'), ('backend-inventory-snapshot.json','input'),
           ('check_three_changed_HC_interfaces.py','code'), ('check_short_forcing_chain.py','code'),
           ('fixed-K-forced-HC-results.json','result'), ('short-forcing-chain-verification.json','result'),
           ('fixed-K-closure-lemma.tex','report'), ('report.md','report'),
           ('provenance.json','report'), ('freeze_metadata.py','code')]
    r['artifacts'] = [dict(path=PREFIX+name, role=role, sha256=sha(HERE/name)) for name,role in own]
    r['artifacts'] += [dict(path=name, role='input', sha256=sha(BASE/name)) for name in inputs]
    r['result'] = {'status': 'complete',
                   'summary': 'Newly covers1 residual mixed interface:00112 position1→3, sourceK12320–32320 maps to HC00123 forced31201–31231. Other2 changed-HC mixed zero;39 no-exclusion eligible unchanged;5hard/hard excluded. One57-vertex122-edge closure gives14forced8excluded5passes,41saved-star readbacks; prospective237nonconstant/residual46.',
                   'result_artifact': PREFIX+'fixed-K-forced-HC-results.json'}
    r['verification'] = {'methods': ['Single independently generated00123 legality graph:57vertices122edges and connected; printed component words agree as vertex set only.',
                                     'Sound simultaneous force/exclude closure summary exactly matches frozen14forced8excluded5passes.',
                                     'Independent parsing of00112 protected basis/pools and original mapped safe-K readback at all41 candidate states.',
                                     'Separate direct four-star local legality/map/port/pool verification; no graph replay.',
                                     'Analytic necessary-HC-edge lower bound and independent peer review of no-exclusion negative lemma.',
                                     'Frozen input SHA256 unchanged before/after; standard metadata validation scoped to schema and hashes.'],
                         'evidence_level': 'bounded-check', 'residual_or_error': 'not-applicable: exact finite graph and integer incidence counts',
                         'limitations': x['limits']+['A zero bound is criterion-inconclusive, not a nonintersection claim.',
                                                   'The237 count inherits original236; no global arbitrary-both-HC or uniform symbolic family claim.',
                                                   'No manuscript-size measurement or adoption claim.',
                                                   'Record validator does not prove mathematical lemmas or rerun computation.']}
    p.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'record_sha256': sha(p), 'result_sha256': sha(HERE/'fixed-K-forced-HC-results.json'),
                      'lemma_sha256': sha(HERE/'fixed-K-closure-lemma.tex'), 'inputs_unchanged': True}))


if __name__ == '__main__':
    run()
