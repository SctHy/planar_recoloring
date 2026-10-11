六个普通 square 接口的独立固定证书核验 PASS。只审 `square-capacity-candidate-v1.tex` 第一张五行表（展开 q=2/3 为六接口），不审后面的 00123 reflection case。

输入直接取冻结 phase6 原稿，SHA `7a90f79db489447b0bad3019217fd369a5cc25986288247981cbe7f3462acba3`。独立解析 C1/FHC 与 POOL；它们共42个 relevant marked blocks 与实际 adopted main SHA `3806a0c7f8ec374ea92e70152f939e92e35c3c76564f9e69e8c06160999bcb58` 字节一致，normalizer 段落也字节一致。没有导入作者、peer 或 root 的 helper。

| source | position→colour | actual target | first normalized type | source/target retention | protected lower bound |
|---|---|---|---|---|---|
| 00014 | 0→3 | 30014 | 01124 | 3,2 | 1 |
| 01014 | 0→2 | 21014 | 01024 | 3,3 | 2 |
| 01014 | 0→3 | 31014 | 01024 | 2,3 | 1 |
| 01014 | 2→2 | 01214 | 01024 | 3,3 | 2 |
| 01124 | 2→2 | 01224 | 00124 | 2,3 | 1 |
| 01204 | 2→0 | 01004 | 00104 | 3,2 | 1 |

`check_six_squares.py` 从候选实际 table 解析变更位置、pattern、x/y 取值和 conditional retention。参数行使用 r=5−q，没有把两种占边数合并。按 manuscript 的 start0..4、direction+1/−1、四颜色排列 lexicographic 次序，重新产生每个 target 的 first normalizer，再逆变换其 printed cycle/pool 到实际坐标。JSON 保存了六个完整 normalizer、四个顶点、四条 square edge、两侧分别保留的边及 pool-empty 结果。

每个 square 都有四个不同顶点，在 source 和 actual target 下均是合法 C5 四色列表状态；任意两顶点一坐标相差形成的诱导图恰为四条边、每点度二。所需循环的原字面无重复且全部合法，包含闭合步的每条边是一坐标改色，池确是其循环子集。两个 pool 与 square edges 的交均为空，两侧独立占边数精确匹配表。

因四边宇宙中分别有 a,b 条被选边，容斥给 a+b−4 条共同边；pool-empty 保证它们均在两个 K 中。六例下界依次1,2,1,2,1,1，足以证明候选所说的“各至少一条，两个(3,3)例至少二条”。程序未计算实际 source-cycle 与 target-cycle 的整体交集，也未用实际共同边清单来反推容量论证。

这是六个指定循环/指定 first normalizer 的轻量 exact certificate review，不是新一般定理。没有 Hamilton 搜索、全313 replay、reflection 重复审查、主稿编辑、正式 MRS 审稿或形式化证明。运行约0.005秒。结果文件为 `six-square-review-results-v1.json`，标准计算记录为 `computation-record-v1.json`。
