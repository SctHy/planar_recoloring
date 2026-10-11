"""Freeze phase11 research and mutable current-status snapshots.

Record paths are relative to RESEARCH; validate with --base-dir RESEARCH.
No manuscript, phase10 packet or branch packet is edited.
"""
from pathlib import Path
from datetime import datetime, timezone
import copy
import hashlib
import json
import shutil
import sys

STAGE = Path(__file__).resolve().parent
RESEARCH = STAGE.parent
WORKSPACE = RESEARCH.parents[2]
CAP = RESEARCH/'tree_gluing/pentagon_deletion_profile/general_protected_capacity'
NOW = datetime.now(timezone.utc).isoformat()

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read(path):
    return json.loads(path.read_text())

def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')

assert not (STAGE/'computation-record.json').exists(), 'Preserve frozen stage record'
branches = ['fixed_K_forced_HC_v1','protected_edge_deletion_cut_v1','remaining_hard_symbolic_v1']
for folder in branches:
    p = CAP/folder
    manifest_files = list(p.glob('frozen-manifest*.json'))
    assert len(manifest_files) == 1, folder
    manifest = read(manifest_files[0])
    branch_record = read(p/'computation-record.json')
    branch_base = CAP if branch_record['task']['file'].startswith(folder+'/') else p
    if 'files' in manifest:
        members = [(branch_base/item['path'],item['sha256']) for item in manifest['files']]
    else:
        members = [(branch_base/name,digest) for name,digest in manifest['members'].items()]
    for path,digest in members:
        assert sha(path)==digest,(folder,str(path))
    assert (p/'computation-record.json').exists()

cuts = read(CAP/'protected_edge_deletion_cut_v1/cut-results.json')
closure = read(CAP/'protected_edge_deletion_cut_v1/HC-HC-avoidance-closure-results.json')
intrinsic = read(CAP/'fixed_K_forced_HC_v1/fixed-K-forced-HC-results.json')
mixed = read(CAP/'remaining_hard_symbolic_v1/full-conditional-closure-results.json')
ka = {tuple(c['case']) for c in cuts['cases'] if c['positive_cut_obstruction']}
kb = {tuple(c['case']) for c in closure['cases'] if c['positive_avoidance_obstruction']}
assert len(ka)==4 and len(kb)==9 and len(ka|kb)==10
assert intrinsic['newly_covered_interfaces']==mixed['positive_cases']==1
new_mixed = ('00112:0',1,3,'00123:0')
assert new_mixed not in ka|kb
new_keys = sorted((ka|kb)|{new_mixed})
assert len(new_keys)==11
main_hashes = {'tex':'b7a048389c00d075d733581bc98fbfd397765b384777e5959076264ab0dbd557','pdf':'4f6bbe50a7fbfb853e367dd2674679e2b3e9c1eefc801eba7ff6a0e373dd496f'}
for suffix,digest in main_hashes.items():
    name=f'planar_recoloring_hamilton_thresholds.{suffix}'
    assert sha(WORKSPACE/name)==digest==sha(RESEARCH/'continuation-10/final'/name)

checkpoint = read(RESEARCH/'research-checkpoint.json')
checkpoint.update({
    'stage':'phase10 adopted41pages; phase11 residual research frozen, notadopted',
    'latest_research_stage':'continuation-11',
    'active_next_tasks':['Extract a few short conditionalobstruction mechanisms andindependently readback sixextraHC-HC traces','Compare acomplete newcandidate proofcost beforeadoption; keep41page reviewedmain now','Retain generalplanargirthfive fourcolourH/HC UNKNOWN'],
    'next_active_research':'Make necessary-HC deletionobstructions genuinely cheaper than existing47edge witnesses; nofurtherrawcoverage counting without proofcost benefit',
    'current_goal_turn_classification':'progress: phase10actual41page adoption frozen; phase11found11unadopted residual analytic candidates andspecifictransport limits',
    'updated_at_utc':NOW,
    'phase11_residual_research':{
        'adopted':False,'current_main_individual_records':47,'current_main_local_cases':236,
        'cut_eligible_cases':42,'cut_directions':70,'cut_positive_cases':4,
        'conditional_HC_HC_cases':28,'conditional_HC_HC_directions':56,'conditional_positive_cases':9,
        'cut_conditional_overlap':3,'union_new_HC_HC':10,'new_mixed':1,'total_new_candidates':11,
        'prospective_local_cases_if_adopted':247,'prospective_individual_records_if_adopted':36,
        'prospective_only':True,'new_actual_manuscript_candidate_pages':None,
        'independent_four_cut_actual_case_review':'PASS','six_extra_conditional_cases_independent_trace_review':False,
        'mixed_full_conditional_closure':'1/14,sameasfourstarintrinsiccandidate,noadditionalcase',
        'hardhard_symbolic_shortening':'notfound;same9K-memberships asoldfiveindividual records',
        'prototype_cut_fragment_bytes':1483,'original_four_literal_records_bytes_excluding_separators':124,
        'new_candidate_indices':new_keys,
        'boundary':'Numericalcoverageisnotproofshortening; fixedK/oppositeHC only; noMainchange/generaltheorem/MRSormemoryupdate',
    },
})
write(RESEARCH/'research-checkpoint.json',checkpoint)
write(STAGE/'research-checkpoint.json',checkpoint)
ongoing = RESEARCH/'持续简化研究.md'
text = ongoing.read_text()
text = text.replace('两个困难保护集的 20 端点诱导图各只有六条未保护边，正在提取缺边预算的短族证明。有限正性覆盖仍非统一解析定理，现行五圈证书不变；这些范围详见 [第八阶段](continuation-8/研究进展.md)。','两个困难保护集的 20 端点诱导图各只有六条未保护边；缺边预算及两个特殊支撑的有限记录继续保留。第八阶段这项容量研究当时未修改五圈证书；后续第九、十阶段的实际替代另见上文。这些有限正性范围仍非统一解析定理，详见 [第八阶段](continuation-8/研究进展.md)。')
text += '\n第十一阶段已从剩余47条继续研究，找到10个双圈和1个混合接口的解析候选：删安全K边后的三个割形状、必要度数矛盾、以及00123中的四星强迫链。四个割案例实际独立复核通过；另外六个新增条件闭包案例尚未第二次独立回读轨迹。现有三割片段1483字节、原四条字面记录124字节（不计分隔），没有更短完整稿的证据，故暂不采用。主稿仍41页／47个别记录，候选247局部／36个别仅为研究账目。详见[第十一阶段](continuation-11/研究进展.md)。\n'
ongoing.write_text(text)
progress = RESEARCH/'研究进展.md'
text = progress.read_text()
paragraph = '第十一阶段继续研究得到11个新的残余接口解析候选，但未确认更短的完整替代，主稿保持上述41页版本。四个割案例已独立回读；另外六个条件轨迹的独立回读仍待完成。新计算、具体失败边界与未采用原因见[第十一阶段](continuation-11/研究进展.md)。\n\n'
index = text.index('\n\n',text.index('当前版本'))+2
progress.write_text(text[:index]+paragraph+text[index:])
snapshots = STAGE/'current-snapshots'
snapshots.mkdir(exist_ok=True)
for name in ['current-source-invariants.json','research-checkpoint.json','持续简化研究.md','研究进展.md']:
    shutil.copyfile(RESEARCH/name,snapshots/name)

summary = {'status':'BOUNDED_RESEARCH_COMPLETE_NOT_ADOPTED','created_at_utc':NOW,
    'current_main_pages':41,'current_main_partition':[47,236,30],'current_main_source_sha256':main_hashes['tex'],'current_main_pdf_sha256':main_hashes['pdf'],
    'new_HC_HC_candidate_indices':sorted(ka|kb),'new_mixed_candidate_index':new_mixed,'new_candidates':11,
    'prospective_partition_if_all_adopted':[36,247,30],
    'independent_case_scope':{'cut_cases':4,'additional_six_conditional_trace_cases':0},
    'branch_records':{folder:sha(CAP/folder/'computation-record.json') for folder in branches},
    'no_main_change':True,'formal_MRS_updated':False,'memory_updated':False,'research_objective_complete':False,
    'goal_backend_last_observed_status':'paused','user_authorized_work_continuation':'go on'}
write(STAGE/'research-results.json',summary)

record = copy.deepcopy(read(RESEARCH/'continuation-10/computation-record.json'))
record['created_at_utc']=NOW
record['task']={'file':'continuation-11/task.md','sha256':sha(STAGE/'task.md'),'object':'Continue proofsimplification throughresidual-safeK cut/forcing research,retain unadopted candidates andactual41page main','deliverables':['Frozen three bounded researchbranches andfour-case independentreview','Exact11candidate union withoverlap handled','Currentmain41pages/47records unchanged;prospective counts not adopted','Durable scope/failure/UNKNOWN records,notcompleted sustainedobjective']}
record['mathematical_context']={'assumptions':['Phase10 reviewedsource/globalclassification andallpreviousproofscope retained','FixedK,actualoriginalnormalizer,pools,completeHCside andfinite necessaryHamiltonconditions','Independentfourcut cases; sixadditionalconditional traces remain root exactcomputation evidence,notindependentreplay'],
    'domain':'Onlyresidual47interface research:42eligible;10newHC-HC plus1mixed candidate. Generalplanargirthfive problem stillopen.',
    'precision':{'mode':'exact','working_digits':None,'target_tolerance':''}}
record['implementation_discovery']['python']['existence_evidence']='Threeactual bounded exactfinite branches androotunion/hashchecks completed'
record['implementation_discovery']['python']['availability_evidence']='LiveCPython'+sys.version.split()[0]
record['decision']['backend_version']=sys.version.split()[0]
record['execution']={'status':'complete','interface':'local-cli','command_or_input':'python3 output/research/proof-simplification-20261010/continuation-11/finalize_records.py\nBranchcommands andactualscope are bound ineach frozen branchcomputation-record.json','code_artifact':'continuation-11/finalize_records.py'}
specs=[('continuation-11/task.md','input'),('continuation-11/finalize_records.py','code'),('continuation-11/研究进展.md','report'),('continuation-11/research-results.json','result'),('continuation-11/research-checkpoint.json','report'),
    ('continuation-11/finalize_records-first-attempt.py','code'),('continuation-11/first-attempt-manifest-format-error.txt','log'),
    ('continuation-11/finalize_records-second-attempt.py','code'),('continuation-11/second-attempt-manifest-base-error.txt','log'),
    ('continuation-10/final/planar_recoloring_hamilton_thresholds.tex','input'),('continuation-10/final/planar_recoloring_hamilton_thresholds.pdf','input'),('continuation-10/source-verification.json','input'),('continuation-10/pdf-visual-qa.json','input')]
for name in ['current-source-invariants.json','research-checkpoint.json','持续简化研究.md','研究进展.md']:
    specs.append(('continuation-11/current-snapshots/'+name,'report'))
for folder in branches:
    p=CAP/folder
    wanted={'computation-record.json','report.md'}
    wanted.update(x.name for x in p.glob('frozen-manifest*.json'))
    wanted.update(x.name for x in p.glob('*results.json'))
    wanted.update(x.name for x in p.glob('*lemma.tex'))
    if folder=='protected_edge_deletion_cut_v1':
        wanted.add('three-fibre-cut-candidate.tex')
    for name in sorted(wanted):
        path=p/name
        assert path.is_file(),path
        role='report' if path.suffix in ('.md','.tex') else 'input'
        specs.append((str(path.relative_to(RESEARCH)),role))
record['artifacts']=[{'path':name,'role':role,'sha256':sha(RESEARCH/name)} for name,role in specs]
record['result']={'status':'complete','summary':'This boundedresearchstage completed;11newcandidate interfaces found with4actualcutcases independentlyreviewed. ActualMainremains41pages/47individual records; alladoption/shortcut thresholds preserved. Prospective247/36notadopted,sixextra conditionaltraces needindependentreadback,generalproblem open.','result_artifact':'continuation-11/research-results.json'}
record['verification']={'methods':['Exactunion of4cut/9closure positives withoverlap3,plus1mixed repeated byparallelbranch','Frozenbranch hash manifests andstandardrecords retained','Fouractual cutcases independently recomputed;generic necessarydegree rules handreviewed','Small00123fourstar actualmap/K/pool andneighbor verification','LiveMainSHA equality toreviewedphase10 finalsource/PDF','Schema/path/hashrecordvalidation only,notmathvalidation'],
    'evidence_level':'exact-check','residual_or_error':'notapplicable: exact finite sets/hashes',
    'limitations':['Candidate coverage doesnotmean proofshortening; no newcomplete manuscript/PDF trial orMainedit.','OnlyoppositeHC arbitrary; fixedK/pool/reservepremises retained.','Sixextra conditionaltrace cases not independently readback; nofull313replay/globaltheoremproof.','Stable necessaryconstraints donot establish avoidingHC existence.','Generalplanargirthfivefourcolour H/HC remainsUNKNOWN;sustainedobjective notcomplete.','NoformalMRS/memoryupdates;internalreview notexternalpeerreview/formalverification.','Goalbackendlastobservedpaused,usergoonauthorized actualmanual work;agentdidnotchangestatus.']}
write(STAGE/'computation-record.json',record)
manifest={'schema_version':'1.0','base_dir':'research root proof-simplification-20261010','stage':'continuation-11 researchunadopted','research_objective_complete':False,
    'files':[{'path':a['path'],'sha256':a['sha256']} for a in record['artifacts']]+[{'path':'continuation-11/computation-record.json','sha256':sha(STAGE/'computation-record.json')}]}
write(STAGE/'frozen-manifest.json',manifest)
print(json.dumps({'status':'FROZEN','new_candidates':11,'adopted_main_pages':41,'adopted_individuals':47,'record_artifacts':len(record['artifacts']),'manifest_members':len(manifest['files']),'record_sha256':sha(STAGE/'computation-record.json'),'manifest_sha256':sha(STAGE/'frozen-manifest.json')}))
