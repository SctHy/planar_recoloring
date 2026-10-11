完整自然分块候选 v1 已冻结；主稿仍为 phase6，未改。

- 源码 `layer-capacity-manuscript-candidate-v1.tex` SHA `b9160b6ce3596356bafc50c097a7ee87022bf7ff6b033272a234063c0cfd3171`。
- PDF SHA `54cfd88518c8125d7f56971fda372fb011584779c0952b1167a2c7c05e1b88d7`，43页；原稿42页。
- 符号候选输入 `layer-proof-input-v1.tex` SHA `7d8db274e8529a31261988b92e2908852a3422952f0c77f5cdda4a5151800d08`。
- 精确 diff、实际源码保存核验和最终日志分别为 `candidate-v1.diff`、`full-candidate-review-v1.json`、`final-latex-v1.log`。

41 个主要数学陈述、53 个 marked literal blocks、DE/DM/DA 的公式全部逐字保持。仅删除旧 witness table 辅助 label，56→55，所有引用有目标。编辑严格限于 `lem:pathsafe` 的 proof、对应附录及 Verification note 的新增说明；没有新编号、循环依赖或 outside coordinate-deletion profiles。

新证明用各 fixed-middle 层及 middle-change edges 的自然不交分块容斥覆盖七族，以 EM 两种 triangle/rung 包含和 MA 两个共同漏边机制补齐。全部九族和 M 两方向均保留。候选本地 source-word checker 直接核验14个 canonical orientation cases 和选定循环支持，独立数学审读由 root 已通过，restoration 另在审读。编译/字面核验不等于数学形式化验证。

粗略字母 token 为正文318、附录284、合计602（旧404、phase7 v1 658、v2 757）；完整源码字节140523→141206。故这是更简洁的结构方法，尚不是相对原稿的文字或页数压缩。完整编译返回0，最终无 Warning/Overfull/Underfull。已渲染并检查19、20、28、32页，无截断、重叠或坏引用；新资料将 Verification note 的尾段推至28页，造成总页数增加一页。后续分离版需保持所有论证完整，不靠删关键内容追求42页。

没有编辑主稿，没有重跑整个接口核，没有 Hamilton 搜索，也没有启动正式 MRS 审稿流程。
