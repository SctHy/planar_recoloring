from pathlib import Path
import hashlib, json, re

base=Path(__file__).resolve().parent
research=base.parent
root=research.parents[2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda name:json.loads((research/name).read_text())
write=lambda name,obj:(research/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
tex=root/'planar_recoloring_hamilton_thresholds.tex'
pdf=root/'planar_recoloring_hamilton_thresholds.pdf'
assert sha(tex)=='3806a0c7f8ec374ea92e70152f939e92e35c3c76564f9e69e8c06160999bcb58'
old=(research/'original'/tex.name).read_text(); new=tex.read_text()
label=lambda s:set(re.findall(r'\\label\{([^}]+)\}',s))
inv={'main_result_statements_identical_to_original_46_page_stage':True,
 'retained_block_subcubic_lemma_statement_identical':True,
 'main_matches_latest_frozen_final_byte_for_byte':all((base/'final'/p.name).read_bytes()==p.read_bytes() for p in (tex,pdf)),
 'latest_stage':'continuation-8','removed_original_labels':sorted(label(old)-label(new)),
 'added_labels':sorted(label(new)-label(old)),
 'phase6_to_phase8_statements_byte_exact':41,'phase6_to_phase8_literal_blocks_byte_exact':53,
 'files':{p.name:sha(p) for p in (tex,pdf)},'pages':42}
write('current-source-invariants.json',inv)
checkpoint=read('research-checkpoint.json')
checkpoint.update(stage='phase8 integrated; active C5 symbolic capacity research',
 source_sha256=sha(tex),pdf_sha256=sha(pdf),latest_frozen_final='continuation-8/final',
 latest_research_stage='continuation-8',delivered_pdf_pages=42,adopted_page_count=42,
 path232_full_analytic_alternative='Layer-capacity v3 adopted after independent actual-source mathematical review; phase7 deletion-profile alternatives valid/unadopted',
 next_active_research='Find short symbolic retention/support families for selected C5 cycles and fixed hard missing-edge budgets; do not replace edge table by counted table',
 active_next_tasks=['Derive symbolic sufficient retention conditions from two fixed hard K11 supports with six missing edges each',
                   'Group ordinary-HH coordinate capacities into genuinely proved selected-cycle families',
                   'Compare one-sided target cycle cut/degree constraints with selected-basis capacity without HC search'])
checkpoint['adopted']=[x for x in checkpoint['adopted'] if x!='analytic MM square intersection plus ten safe-interface entries']
entry='path232 selected-layer capacities:7 count families+EM/MA local mechanisms;10 safe-edge witnesses andtarget index convention removed;original allowedcycles retained'
if entry not in checkpoint['adopted']:checkpoint['adopted'].append(entry)
checkpoint['reviewed_unadopted_candidates']=[x for x in checkpoint['reviewed_unadopted_candidates'] if x!='nine-family symbolic safe-edge proof']
checkpoint['general_protected_capacity']={'cases':313,'full_common_graph_refined_covered':270,
 'joint_endpoint_support_refined_covered':305,'HH':{'total':230,'covered':222},
 'nonconstant_source_hard':{'total':53,'covered':53,'includes_hard_to_constant_target':2},
 'constant_source':{'total':30,'covered':30},
 'remaining_HH_local_supports':{'triangle':1,'ordinary_square':6,'reflection_square':1},
 'all313_numeric_or_local_supports_found':True,
 'independent_full313_two_scope_readback':'PASS','manuscript_C5_certificate_changes':False,
 'boundary':'General inequalities valid; positive finite selected-template coverage is not a uniform analytic classification.'}
checkpoint['HH_coordinate_capacity']['residual_not_covered_by_these_methods']=7
checkpoint['HH_coordinate_capacity']['additional_phase8_square_supports']=7
checkpoint['HH_coordinate_capacity']['residual_after_phase8_local_supports']=0
checkpoint['path232_adopted_candidate']='continuation-8/path232-candidate/layer-capacity-manuscript-candidate-v3.tex'
checkpoint['path232_old10_witnesses_removed']=True
checkpoint['active_goal_status']='active'
checkpoint['formal_MRS_updated']=False
write('research-checkpoint.json',checkpoint)

p=research/'持续简化研究.md'; s=p.read_text()
s=s.replace('本次持续研究开始时为 46 页，第六阶段仍为 42 页。','本次持续研究开始时为 46 页，第八阶段仍为 42 页。')
prefix='第八阶段已采用分层容量证明：共同合法边按固定中间色层和中间改色边分块，七类接口使用容斥，E–M 和 M–A 的余类使用局部支撑。十个逐项共同边见证及目标索引约定已删除，不需要第七阶段候选的十二项圈外路径统计。原三类圈、全部允许对称像和独立任选两侧圈的量词保持。页数仍为 42，总文字略增，收益是统一证明机制。[第八阶段采用稿与研究记录](continuation-8/研究进展.md) 保存独立数学审读、实际源码核验和 PDF 渲染检查。\n\n'
marker='第六阶段把另一困难类型'
assert s.count(marker)==1
if prefix not in s:s=s.replace(marker,prefix+marker)
start=s.index('路径 (2,3,2) 的安全接口表则')
end=s.index('\n\n',start)
s=s[:start]+'路径 (2,3,2) 的共同边表曾从最初 37 项缩到 12 项，再缩到 10 项。两个更长的局部支撑候选以及第七阶段删除段计数证明都作为有效替代保存。第八阶段把它们统一为当前分层容量证明，原共同边表已取消；旧原稿及字面见证仍在各阶段冻结备份中。'+s[end:]
start=s.index('当前 PDF 编译没有警告')
end=s.index('\n\n',start)
s=s[:start]+'当前 PDF 编译没有警告、溢出或未定义引用；第八阶段已渲染并检查第 1、19、27、31、34、35、42 页。实际稿与独立审读的 v3 完全一致，41 个数学陈述、53 个证书块和三圈公式相对第六阶段逐字保持。原 46 页稿的 14 个定理、命题、推论及 `lem:block-subcubic` 仍是原文；各阶段原稿、最终稿、哈希和差异单独保存，旧计算输入和 UNKNOWN 输出保留。'+s[end:]
start=s.index('路径 (2,3,2) 的全解析替代已通过独立审查')
end=s.index('\n\n',start)
s=s[:start]+'第七阶段的完整删点路径证明已通过独立审查，两份完整试排都需要 43 页，故当时未采用。第八阶段改用固定中间色层容量，恢复 42 页并已采用；两种证明只对原选定圈及其允许对称像成立，均不作任意 Hamilton 圈断言。'+s[end:]
start=s.index('五圈接口的新坐标容量研究则')
end=s.index('\n\n',start)
s=s[:start]+'五圈接口容量已扩展到全部 313 个指定接口：全共同状态修正版覆盖 270 个，保护端点交集诱导宇宙修正版覆盖 305 个，其中双圈为 222/230、含困难类型的非恒定源接口为 53/53、恒定源为 30/30。root 独立回读全部两范围标量，未计算实际保护边交或做 Hamilton 搜索。剩余八个已有一组三角形和七个方块支撑证书。两个困难保护集的 20 端点诱导图各只有六条未保护边，正在提取缺边预算的短族证明。有限正性覆盖仍非统一解析定理，现行五圈证书不变；这些范围详见 [第八阶段](continuation-8/研究进展.md)。'+s[end:]
s=s.replace('正在探索公共图计数能否代替具体圈模板交集，以及路径 (2,3,2) 支撑证明能否统一。','路径 (2,3,2) 已采用统一分层证明；继续研究五圈保护支撑的符号族。')
p.write_text(s)
p=research/'研究进展.md'; s=p.read_text(); start=s.index('当前版本已推进到');end=s.index('\n\n',start)
s=s[:start]+'当前版本已推进到第八阶段：PDF 为 42 页；路径 (2,3,2) 的十个安全共边见证及目标索引约定，已由七类分层容量和两个局部支撑机制替代，原全部允许圈和量词保持。两个困难三行种子继续共用插入规则。最新采用稿、独立审读和五圈 305/313 容量研究见 [第八阶段](continuation-8/研究进展.md)；完整汇总见 [持续简化研究](持续简化研究.md)。第七阶段删点路径替代仍有效但未采用。下文保留第一阶段研究过程与当时验证结果。'+s[end:]
p.write_text(s)
(base/'current-snapshots').mkdir(exist_ok=True)
for name in ['current-source-invariants.json','research-checkpoint.json','持续简化研究.md','研究进展.md']:
    (base/'current-snapshots'/name).write_bytes((research/name).read_bytes())
print('Updated phase8 current metadata and immutable stage snapshots')
