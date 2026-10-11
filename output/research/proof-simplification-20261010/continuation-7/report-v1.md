完整候选 v1 已冻结并通过源码核验、编译和改动页视觉检查。主稿仍为 phase6 SHA `7a90f79db489447b0bad3019217fd369a5cc25986288247981cbe7f3462acba3`，未被修改。

- 候选源码：`simplification-candidate-v1.tex`，SHA `054e8162ebfd8f15e536e82a22e548c71906b8ea9735b62c983cd2d500d4bdc0`。
- 候选 PDF：`simplification-candidate-v1.pdf`，SHA `7d92ad256d54537069818da5f006895ae02144662f8caf3281ecdbdba685dbce`。
- 精确 diff：`candidate-v1.diff`；源码核验：`candidate-review-v1.json`；最终编译日志：`latex-build-v1.log`。

实际标签是 `lem:pathsafe`。41 个 theorem/lemma/proposition/corollary 的原陈述逐字不变；53 个 `% BEGIN ... % END` 字面块全部逐字不变；`eq:path232-cycles` 的 DE、DM、DA 字面公式逐字不变。只删除旧辅助表标签 `tab:path232-safe-edges`，因此标签总数 56→55，所有 ref/eqref/pageref 均有目标。源码改动严格限于 safe lemma 的 proof、对应附录引言及旧表专用小节、Verification note 的新增一句。

新证明用一个通用圈删点不等式处理六族，以共同图的顶点/边数、禁边、删点路径数和双方同时不用的边给出至少两个安全共边；其余三族分别用方格/六圈/方格支持。边界分类共有九族，同时保留 middle 型的两个允许边集。本文量词仍是原三组选定循环的所有色置换和反射像。outside induced paths 已明确在各自选定循环中，未声称全 fibre 的诱导子图是这些路径。`Q_d` 与 `B_{aaa}` 沿用 lemma 前已有定义；无新增 DP/CT 标签或编号。

这是真正的推理替换：不再依赖十个逐项指定共边、目标规范化 conventions 和源稳定子 orbit 索引。它没有取消选定循环字面，也仍需十二个坐标类的删点路径描述、六个容量数和三项同时漏边机制。不得外推为任意 Hamilton cycles 之间的共边定理。

它不是字数压缩。用“剥除 TeX 命令名和注释后的 ASCII 字母 token”统一计数（数学字母计入，数字三位状态不计），旧 proof+conventions/orbit/table 为 404，新 proof 为 658；相应源码字节 3287→4201。完整主稿字节 140523→141627。原稿 PDF 42 页，候选 43 页。`latexmk -pdf -interaction=nonstopmode -halt-on-error` 返回 0，最终日志无 Warning、Overfull、Underfull。已渲染并逐页检查新 PDF 的 19–21、28、32 页，公式、数组、续页与引用均无截断或重叠。附录 32 页只剩三个循环，空白较多；将分类依据与十二个循环描述移回该页，是自然的下一版排版方案。

数学推导已由 root 和 restoration 独立审读；本任务的可执行核验是源码保持、六行数值及十二个描述与已有冻结证明一致、编译与版面核验。没有新状态图核枚举、Hamilton 搜索、正式 MRS 审稿或数学形式化验证。
