分离版完整候选 v2 已冻结，主稿仍 phase6，所有既有阶段未改。

- 源码：`layer-capacity-manuscript-candidate-v2.tex`，SHA `68ce8760008895fcc1c27d54faf0fadc1ff5335901894f5cf89cd9e37ec9b506`。
- PDF：`layer-capacity-manuscript-candidate-v2.pdf`，SHA `536784cf48180fe687031dca335c37d232a3aadd1b2b0b948a311d41b264157a`。
- 独立符号输入：`layer-proof-input-v2.tex`，SHA `11a6bada97dd2f08f150306eeae48e02f7f1ddb7ccfc1147f15077804497dc03`。
- 源码核验、精确 baseline diff 和 v1→v2 diff 为 `full-candidate-review-v2.json`、`candidate-v2.diff`、`v1-to-v2.diff`。

41个主要数学陈述、53个 marked literal blocks、DE/DM/DA 公式全部逐字不变。只删除旧 safe-witness-table 辅助标签，其他55个标签顺序原样，全部引用有效。修改严格限于 safe-edge lemma proof、对应附录、Verification note 新增一句；没有循环依赖、旧表引用或 outside coordinate-deletion profiles。符号稿与完整稿的两片段字节一致。

正文完整保留普遍分块容斥及 EM、MA 两个局部机制，九分类与七个可见容量行移至附录 C.2。三句单侧层结构和 cross4 描述代替六行重复的 symbolic path words；选定循环仍原字面。v1 的所有容量行、EM/MA 实质论证原字节保留。直接 source-word checker 核验实际 v2 全14个 canonical orientation cases、层结构、star规律及特殊边扣除，PASS。v1 已获 root 与 restoration 独立数学审读 PASS，v2 另发 restoration 审读。

完整编译返回0，无 Warning、Overfull、Underfull。候选恢复42页，原稿42页，layer v1为43页，旧 DP两版均43页。已渲染并检查19、27、31页：正文原则与局部论证、Verification note、原圈加完整新附录容量表均无截断/重叠/坏引用；七行表全部在31页，末行与footer分开。精确最终编译日志是 `final-latex-v2.log`。

粗略字母 token：旧 proof+conventions/table404，新正文204、附录348、合计552；layer v1为602，DP v1/v2为658/757。完整源码140523→140936字节。收益是更短且更统一的证明机制、取消十二项删点路径资料与十个逐项共边，保持原页数；总文字仍多于旧表方案，不能宣称字数压缩。

编辑精确性建议已发 root：Cartesian layer/cross-edge 公式应明确 middle colours 在共同允许列表中，即不在 `{t_1,s_1}` 中；所有实际容量行都满足此条件，证明和数值没有改变。冻结 v2 不再编辑，父稿若采用可加入该简短限定。

原主稿 hash `7a90f79db489447b0bad3019217fd369a5cc25986288247981cbe7f3462acba3` 未变。没有 whole graph/kernel 重跑、HC搜索、正式 MRS 审稿或数学形式化验证。
