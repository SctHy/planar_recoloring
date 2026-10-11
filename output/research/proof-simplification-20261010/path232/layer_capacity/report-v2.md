分离版符号候选 `layer-proof-candidate-v2.tex` 已冻结，SHA `11a6bada97dd2f08f150306eeae48e02f7f1ddb7ccfc1147f15077804497dc03`。v1 保持原字节。

证明仍完整：正文给安全边宇宙的通用不交分块容斥，EM 的 row-triangle/rung 两向包含，MA 两条共同遗漏及另一 square 的容量。附录明确列出九类边界变更、E/A 唯一允许边集及 M 两种边集、七组安全 `(m,x,y)`；没有把局部计数藏成外部程序前提。重复的六个 symbolic path rows 改成 E、M、A 各一句 selected-layer 结构描述，cross4 规律保留。七行容量表及 EM/MA 论证与已审 v1 字节一致，只改变位置。

实际 `check_layer_proof_v2.py` 从不变的原三个 cycle words 重新读取：验证 E 层 `[3,3],[4],[4]`，M 层 `[1,8],[4],[4]`（isolated bab），A 层 `[6],[6],[1,3]`（isolated bdb）；验证三个 middle-change star 描述；解析实际 v2 七行表并对所有 14 canonical orientation cases 核验安全占边数；验证 EM 两向包含和 MA 两向遗漏。`layer-proof-review-v2.json` PASS。全部允许色像及反射的 fixed-boundary stabilizers 保留；没有 arbitrary-cycle 外推。

对应完整主稿候选在 `continuation-8/path232-candidate/`，编译42页，与 phase6原稿页数相同。粗略字母 token 正文204、附录348、合计552；旧404、layer v1为602、先前 DP v1/v2为658/757。它以更简单的分块原则替代十二个删点路径描述和十个指定共边，且不增页；仍不能称总文字比旧稿更少。

已发 root 一个限定范围的编辑建议：附录 Cartesian layer/cross-edge 公式的 middle colours 应明确是允许的，即不在 `{t_1,s_1}` 中。所有实际容量行都只用这些合法颜色，数据与证明不变。冻结 v2 未改；若父稿集成，加“allowed”或显式索引范围可排除读法歧义。

没有新 HC 搜索、全接口核重跑或主稿编辑；固定证书 replay 与编译不构成数学形式化验证。
