from pathlib import Path
import datetime, hashlib, json

base = Path(__file__).resolve().parent
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
result = json.loads((base/'review-results.json').read_text())
assert result['status']=='PASS_BOUNDED_TWO_SCOPE_READBACK'
files = [('phase6-source.tex','input'),('expected-baseline.json','input'),
         ('expected-port-support.json','input'),('check_protected_capacity.py','code'),
         ('review-results.json','result'),('task.md','input'),('report.md','report'),
         ('create_record.py','code')]
record = {
 'schema_version':'1.0', 'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'task':{'file':'task.md','sha256':sha(base/'task.md'),
         'object':'Independent complete scalar readback of 313 specified protected interfaces on full and joint endpoint-support universes',
         'deliverables':['two-scope exact readback','mathematical sufficiency and monotonicity argument','hard-template saturated-coordinate verification']},
 'mathematical_context':{
    'assumptions':['Actual frozen phase6 templates and pools; first standard normalizer for each target',
                   'Ordinary cycle bases and hard D13 bases are distinct; protected edge set is basis minus its own pool',
                   'Endpoint support is only an edge-universe reduction and does not replace the full fibre'],
    'domain':'23 small C5 fibre components; exactly 313 specified interfaces split into 230 HH,53 nonconstant-source hard and30 constant-source cases',
    'precision':{'mode':'exact','working_digits':None,'target_tolerance':''}},
 'implementation_discovery':{
    'mathematica':{'candidate_implementations':['exact finite edge-set enumeration'],
       'existence_evidence':'General finite graph enumeration is expressible; no CAS implementation selected.',
       'local_availability':'unavailable','availability_evidence':'Cached backend inventory probed 2026-10-09 reports no local executable.'},
    'sagemath':{'candidate_implementations':['exact finite graph enumeration'],
       'existence_evidence':'General graph enumeration is expressible; no Sage implementation selected.',
       'local_availability':'unavailable','availability_evidence':'Cached backend inventory probed 2026-10-09 reports no local executable.'},
    'python':{'candidate_implementations':['stdlib product, parsing and exact scalar edge-universe counts'],
       'existence_evidence':'Independent check_protected_capacity.py executed successfully.',
       'local_availability':'available','availability_evidence':'Actual result records Python 3.14.6; cached 3.14.3 value is stale.'}},
 'decision':{'selected_backend':'python','backend_version':result['backend_version'],
             'selection_reason':'At most 4^5 states per template and313 small induced graphs make exact stdlib counting sufficient.',
             'fallback_reason':'No CAS, numerical approximation or Hamilton search is needed.'},
 'execution':{'status':'complete','interface':'local-cli',
              'command_or_input':'python3 check_protected_capacity.py','code_artifact':'check_protected_capacity.py'},
 'artifacts':[{'path':p,'role':role,'sha256':sha(base/p)} for p,role in files],
 'result':{'status':'complete','summary':'All313 scalar vectors in both frozen scopes match; refined support capacities cover305, while full-state capacities cover270. Exact hard support counts and monotonicity checks pass.',
           'result_artifact':'review-results.json'},
 'verification':{'methods':['Independent actual-source template/pool parsing and canonical-normalizer construction',
                 'All313 scalar-vector comparison in two scopes without protected-set intersections',
                 'Coordinatewise support-bound monotonicity and exact hard-support edge-universe counts',
                 'Separate hand proof of universe containment, inclusion-exclusion and edgewise monotonicity'],
    'evidence_level':'exact-check','residual_or_error':'not-applicable: exact integer finite counts',
    'limitations':['Coverage305/313 is bounded selected-template evidence, not a uniform symbolic C5 theorem.',
                   'Endpoint support has20 states for each hard K11 and does not replace44/51-state fibres.',
                   'No Hamilton search or actual K/L common-edge enumeration; manuscript not edited by this branch.',
                   'Record validator establishes schema/hashes only, not mathematical correctness.']}}
(base/'computation-record.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print('Created computation-record.json with',len(files),'hashed artifacts')
