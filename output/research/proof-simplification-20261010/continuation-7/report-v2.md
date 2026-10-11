分离资料版 v2 已冻结，源码保持核验、完整编译及改动页视觉检查均通过。主稿和既有 deletion-profile candidates 未改，v1 也保持原字节。

- 源码：`simplification-candidate-v2.tex`，SHA `b29eaa658b17a0e3a61120b064bf4fb08349e53bffeea419e4ca1c16b5e82d26`。
- PDF：`simplification-candidate-v2.pdf`，SHA `9a2d2595859a68b5b52cf619631cd7a3ec423abfc0e68b695c012d18bdc0e2c2`。
- 原稿 SHA：`7a90f79db489447b0bad3019217fd369a5cc25986288247981cbe7f3462acba3`。
- 精确 diff：`candidate-v2.diff`；v1→v2 diff：`v1-to-v2.diff`；源码核验：`candidate-review-v2.json`；编译日志：`latex-build-v2.log`；记录：`computation-record-v2.json`。

41 个主要 theorem/lemma/proposition/corollary 陈述、53 个 marked literal blocks、三组选定循环公式均逐字保持。旧辅助标签 `tab:path232-safe-edges` 删除，其他 55 个标签原次序不变，所有引用有目标。全部编辑限于 `lem:pathsafe` 的 proof、对应附录和 Verification note 的一句更新。`Q_d` 和 `B_{aaa}` 引用既有定义；没有新增 DP/CT equation tag。

正文保留普遍的删点计数、六组 `n,m,f,r,k`、三组正 k 的漏边机制，以及另三族 square/hexagon 支持论证。正文以短引用把允许的 middle-cycle 两个边集、九族分类依据和十二个坐标类删点路径放在附录 C.2；附录直接由未变的 C.1 cyclic words 得到这些描述。路径诱导范围在正文和附录都明确为各自选定的循环。没有把该性质外推至任意 Hamilton cycles，也没有收窄原 all-allowed-cycles 量词。

计数推导是通用的：若一个循环在非空共同顶点集 U 外有 q 个路径分量，则 U 内恰有 n−q 条循环边；各减至多 f 条禁边，再从 m−f−k 的共同允许边宇宙作 inclusion–exclusion 得到 `2n−q_C−q_D−m−f+k`。六个共同图由固定 middle-coordinate 的 Cartesian grids 加中间坐标改色边得到；三组漏边信息弥补容量下界的差额。其余三族用共同 square 或 hexagon 的直接支持数。这替代旧十个指定共边及 orbit/index conventions，属于方法替换；三组选定循环及其小型支持事实仍是证据输入。

统一粗略字母 token 指标（剥除 TeX 命令名和注释，数学字母计入，数字状态不计）：旧 proof+旧 conventions/orbit/table 为 404；v1 新 proof 658；v2 正文 535、附录支持 222、合计 757。v2 增加直接逐坐标的分类说明，所以总文字比 v1 更多。原稿/候选完整源码字节为 140523/142329。PDF 页数为原稿 42、v1 43、v2 43；没有省页。v2 更清楚地分开一般计数和三个选定循环的支持资料。选择它的理由是可读性与取消十个接口见证，不能把它宣传为篇幅压缩。

`latexmk -pdf -interaction=nonstopmode -halt-on-error simplification-candidate-v2.tex` 返回 0，最终日志无 Warning、Overfull、Underfull。已渲染并逐页检查 19、20、28、32 页：计数数组、推导续页、Verification note 与新增附录 C.2 均无截断、重叠或坏引用。v1 的既有记录已先冻结，两个版本均保持 separate candidate，未纳入主稿。

数学路线已由 root 和 restoration 审读；本任务进一步验证实际适配源码与已冻结证明一致。可执行核验及编译不是形式化证明或正式 MRS 审稿。没有新增整个状态图枚举、接口全核重跑或 Hamilton 搜索。
