"""Freeze completed exact residual research, without modifying Main."""
from pathlib import Path
from datetime import datetime, timezone
import copy
import hashlib
import json
import sys

BASE = Path(__file__).resolve().parent
RESEARCH = BASE.parents[3]
WORKSPACE = RESEARCH.parents[2]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read(path):
    return json.loads(path.read_text())

def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')

assert not (BASE/'computation-record.json').exists(), 'Preserve frozen records'
assert not (BASE/'frozen-manifest.json').exists(), 'Preserve frozen records'
cuts = read(BASE/'cut-results.json')
closure = read(BASE/'HC-HC-avoidance-closure-results.json')
cut_keys = {tuple(c['case']) for c in cuts['cases'] if c['positive_cut_obstruction']}
closure_keys = {tuple(c['case']) for c in closure['cases'] if c['positive_avoidance_obstruction']}
assert len(cut_keys) == 4 and len(closure_keys) == 9 and len(cut_keys|closure_keys) == 10
assert cuts['source_sha256'] == closure['source_sha256'] == sha(BASE/'phase10-source.tex')
assert sha(WORKSPACE/'planar_recoloring_hamilton_thresholds.tex') == cuts['source_sha256']
review = BASE/'independent_review'
assert list(review.glob('computation-record*.json')), 'Wait for independent review freeze'
assert list(review.glob('frozen-manifest*.json')), 'Wait for independent review freeze'

record = copy.deepcopy(read(RESEARCH/'continuation-10/computation-record.json'))
record['created_at_utc'] = datetime.now(timezone.utc).isoformat()
record['task'] = {
    'file': 'task.md', 'sha256': sha(BASE/'task.md'),
    'object': 'Residual-only fixedK safe-edge deletion cut andconditional necessary-HC closure research',
    'deliverables': ['Exact42eligible/70direction cut checks', 'Exact28HC-HC/56direction conditionalclosure checks', 'Proof lemmas,actual-coordinate witnesses andbounded failure evidence retained', 'Independentfour-cut review archived; Main41pages/47individual records unchanged'],
}
record['mathematical_context'] = {
    'assumptions': ['Hash-bound phase10 source andprior independently reviewed source readers/component premises', 'FixedK side andopposite full printed-HC component B; S=(K intersect E(B)) minus B pool', 'Original interfacefirstnormalizer andcoordinates retained', 'A Hamiltoncycle is degree2,connected andcontains no proper forcedcycle'],
    'domain': 'Only47residual interfaces:42eligibleforcut checks,28HC-HC fornewconditionalclosure. Fivehard-hard excluded. No236adoptedcase replay.',
    'precision': {'mode': 'exact', 'working_digits': None, 'target_tolerance': ''},
}
record['implementation_discovery']['python']['candidate_implementations'] = ['stdlib exact finite graphs andnecessaryconstraint propagation']
record['implementation_discovery']['python']['existence_evidence'] = 'Actualcut andconditionalclosure producer runs complete in under1second combined'
record['implementation_discovery']['python']['availability_evidence'] = 'LiveCPython'+sys.version.split()[0]
record['decision']['backend_version'] = sys.version.split()[0]
record['decision']['selection_reason'] = 'Small exactfinite graph set/deletion/DFS andmonotone necessaryconstraint propagation; noCAS orHCsearch required'
relative = str(BASE.relative_to(WORKSPACE))
record['execution'] = {'status': 'complete', 'interface': 'local-cli',
    'command_or_input': f'python3 -B {relative}/check_deletion_cuts.py\npython3 -B {relative}/check_HC_HC_avoidance_closure.py\npython3 {relative}/finalize_records.py',
    'code_artifact': 'check_deletion_cuts.py'}
specs = [
    ('task.md','input'), ('input-manifest.json','input'),
    ('phase10-source.tex','input'), ('reference-phase9.tex','input'),
    ('prior-independent125-results.json','input'),
    ('independent_source_reader.py','code'), ('fixed_k_source_reader.py','code'),
    ('check_deletion_cuts.py','code'), ('check_HC_HC_avoidance_closure.py','code'),
    ('finalize_records.py','code'), ('cut-results.json','result'),
    ('HC-HC-avoidance-closure-results.json','result'),
    ('cut-obstruction-lemma.tex','report'), ('avoidance-closure-lemma.tex','report'),
    ('three-fibre-cut-candidate.tex','report'), ('report.md','report'),
]
for path in sorted(review.rglob('*')):
    if not path.is_file() or '__pycache__' in path.parts:
        continue
    name = str(path.relative_to(BASE))
    role = 'code' if path.suffix == '.py' else 'report' if path.suffix == '.md' else 'log' if path.suffix == '.txt' else 'input'
    specs.append((name, role))
record['artifacts'] = [{'path': name,'role': role,'sha256': sha(BASE/name)} for name,role in specs]
record['result'] = {'status':'complete','summary':'4newcut and9conditionalclosure positive HC-HC cases overlap3;union10newanalytic candidates,notadopted. Mainunchanged41pages/47individual witnesses. Researchscope complete doesnotcomplete sustainedobjective.','result_artifact':'HC-HC-avoidance-closure-results.json'}
record['verification'] = {
    'methods': ['Hash-bound exactoriginalmap/K/pool/full-component mutationneighbor construction', 'Exhaustivevertex deletion disconnect checks onlywithin70residualdirections', 'Monotone necessaryHamiltondegree/forcedpropercycle certificates within56residualHC-HC directions', 'Generichandproof F subset C subset A; cuts/degree contradictions necessary', 'Separately frozen independentfour-cut actualsource review andcoordinate correction evidence', 'LiveMainhash equality andstandardrecord artifacthash binding'],
    'evidence_level':'exact-check',
    'residual_or_error':'notapplicable: finite exactsets, nofloatingpoint',
    'limitations': ['Candidatefinite coverage increase isnot confirmedproofsimplification orshorter manuscript; noMainadoption.', 'QuantificationonlyoppositewholeHC; fixedK andpool/normalizer hypotheses retained.', 'Rootreusesreviewedsource parsers/component premises; thisisnot a second independent graph-reader implementation.', 'Independentreviewscope isstated initsownreport; do not infer all56or70directions wereindependently replayed.', 'Failureofcut/closure necessarytest doesnotimply anavoidingHC exists.', 'NoHCsearch/fulllegalwordenumeration/generalplanargirthfive proof/MRSormemoryupdate.', 'Backendgoalstatus andsustainedobjective unchanged; stageboundedresearch completion only.'],
}
write(BASE/'computation-record.json', record)
manifest = {'schema_version':'1.0','stage':'phase11 residual deletion/cut/conditionalclosure research,unadopted','research_objective_complete':False,
    'files':[{'path':a['path'],'sha256':a['sha256']} for a in record['artifacts']]+[{'path':'computation-record.json','sha256':sha(BASE/'computation-record.json')}]}
write(BASE/'frozen-manifest.json', manifest)
print(json.dumps({'status':'FROZEN','artifacts':len(record['artifacts']),'manifest_members':len(manifest['files']),'new_HC_HC_candidates':10,'record_sha256':sha(BASE/'computation-record.json'),'manifest_sha256':sha(BASE/'frozen-manifest.json')}))
