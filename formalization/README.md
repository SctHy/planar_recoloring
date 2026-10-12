# `main.tex` 的 Lean 4 形式化边界

这里是与论文正文配套的、可独立编译的 Lean 4 核心形式化。项目固定
Lean 4.34.1，只依赖随 Lean 发布的 `Std`，因此不需要下载 mathlib。

已由内核检查的内容如下：

- `PlanarRecoloring/Core.lean` 定义有限图的 Boolean 邻接矩阵、合法着色、
  单顶点重着色邻接、可用颜色，以及显式列表路径的覆盖条件；
- `PlanarRecoloring/General.lean` 补充无环/对称简单图接口、列表版退化性、
  颜色置换、重着色后的合法性与可用颜色保持引理；
- `PlanarRecoloring/Hamilton.lean` 定义 Hamilton 路、Hamilton 圈、
  Hamilton-connected 和 vertex-pancyclic 的显式列表版本，并证明端点/覆盖辅助引理；
  对称关系下的列表路径反向和 Hamilton 路端点交换也已由内核检查；
- `PlanarRecoloring/Fibre.lean` 把正文纤维拼接的一个严格抽象接口编码为
  `FibrePath`，证明允许两侧内部关系不同的不交纤维路径可沿接口边拼接，并保持覆盖、无重复和连续性；
- `PlanarRecoloring/FibreChain.lean` 将上述接口推广到任意非空纤维链，证明展平后的路径保留覆盖、无重复、端点和桥接连续性，并可在闭合桥下构成 `ClosedFibrePath`；
- `PlanarRecoloring/FibreHamilton.lean` 将覆盖有限图顶点集的纤维路径接入
  `HamiltonPath`/`HamiltonCycle` 定义，并提供显式列表上的 `HamiltonPathOn`/`HamiltonCycleOn` 转换；所有路径存在性假设仍为显式输入；
- `PlanarRecoloring/Extension.lean` 用 `Option (Fin n)` 表示恢复一个顶点，严格证明扩展合法性的可用颜色判据、单纤维重着色邻接和共享颜色的跨纤维边；并将保持恢复顶点颜色的基图边编码为 `RestorationBridge`，把闭合纤维链提升为恢复图上的关系级 Hamilton 圈证书；
- `PlanarRecoloring/PermutationParity.lean` 形式化 `d=1,k=3` 的 `K_2` 六状态
  重染色图：每条合法边翻转三色排列奇偶性，因此指定端点间不存在六点 Hamilton 路，
  且图无三角形；
- `PlanarRecoloring/ProductParity.lean` 对用 `List Bool` 表示的二进制积定义单坐标翻转，
  证明翻转改变 xor 奇偶性、路径沿边逐步翻转，偶数路径保持端点奇偶性，且路径长度保持、
  路径可反向，并排除奇长度闭路；
- `PlanarRecoloring/Bridge.lean` 证明正文 Lemma `bridge-colours` 的三层局部版本：
  两层至少有两个颜色，中间层至少有三个颜色时，可以避开给定端点并选择相邻颜色不同的桥接颜色，
  并给出三层循环的两两不同选择；
- `PlanarRecoloring/BridgeLists.lean` 将该选择推广到任意长度的列表：每层至少有两个颜色、
  且至少一层有三个颜色时，证明存在首尾避开指定端点且相邻选择不同的完整选择序列；
- `PlanarRecoloring/CyclicLists.lean` 将任意长度选择序列闭合为循环，在至少一层有三个颜色时证明首尾也不同；
- `PlanarRecoloring/CyclicBinary.lean` 处理所有列表相同且恰有两个颜色的偶数长度交替特例，并证明奇数长度不可能闭合；
- `PlanarRecoloring/LowerBound.lean` 形式化 `degenerate-sharp` 在 $d=0$ 的有限障碍。
  两个孤立顶点使用二色时得到四元超立方体；奇偶性证明 `00` 与 `11` 不能由三步重着色路径连接，
  从而给出 Hamilton-connected 下界，并另外证明该图没有三角形；
- `PlanarRecoloring/Frozen.lean` 验证正文中立方体四着色的冻结性质：每条立方体边的两端颜色不同，
  且每个顶点的三个邻点恰好出现其余三种颜色。

本轮（第三节及其前置接口）的增量集中在可组合的证书层：
`HamiltonPathOn`、`HamiltonCycleOn` 用显式有限顶点列表表达关系级 Hamilton 性质；
`FibrePath.toHamiltonPathOn` 和 `ClosedFibrePath.toHamiltonCycleOn` 将纤维证书直接转换为这些性质，
而 `restoration_fibre_cycle_hamiltonCycleOn` 将恢复顶点的桥接假设、路径覆盖和闭合条件一次接入。
第二节的二色循环选色已增加首对异质层的双向构造；任意位置异质层的旋转引理仍保留为下一步。

运行验证：

```sh
lean PlanarRecoloring/LowerBound.lean
```

完整 Lake 目标需要 Lean 4.34.1 与 Lake。若使用仓库外的 elan 安装，运行：

```sh
cd formalization
lake build
```

在当前开发机也可使用解压的 Lean：

```sh
PATH=/tmp/lean-download/tool/lean-4.34.1-darwin_aarch64/bin:$PATH lake build
```

也可以直接检查单个文件：

```sh
lean PlanarRecoloring/Core.lean
lean PlanarRecoloring/General.lean
lean PlanarRecoloring/Hamilton.lean
lean PlanarRecoloring/Fibre.lean
lean PlanarRecoloring/PermutationParity.lean
lean PlanarRecoloring/ProductParity.lean
lean PlanarRecoloring/Bridge.lean
lean PlanarRecoloring/BridgeLists.lean
lean PlanarRecoloring/CyclicLists.lean
lean PlanarRecoloring/CyclicBinary.lean
lean PlanarRecoloring/LowerBound.lean
lean PlanarRecoloring/Frozen.lean
lean PlanarRecoloring/FibreChain.lean
lean PlanarRecoloring/Extension.lean
```

这不是把全文主定理宣称为已形式化。正文中的平面嵌入与 Euler 计数、
Grötzsch 三着色、排列图 Hamilton-connected 结果、补充附件的有限证书、
任意阶循环纤维提升、结构归纳和列表周期选择仍是待形式化的接口；它们依赖正文引用的
Choo--MacGillivray、Havel 等外部结果或尚未定义的平面图数据结构。本目录
只报告上述自足定理的 Lean 检查结果，不用 `sorry`、`axiom` 或计算报告替代这些证明。
