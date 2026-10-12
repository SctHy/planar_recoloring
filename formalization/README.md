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
- `PlanarRecoloring/Bridge.lean` 证明正文 Lemma `bridge-colours` 的三层局部版本：
  两层至少有两个颜色，中间层至少有三个颜色时，可以避开给定端点并选择相邻颜色不同的桥接颜色；
- `PlanarRecoloring/LowerBound.lean` 形式化 `degenerate-sharp` 在 $d=0$ 的有限障碍。
  两个孤立顶点使用二色时得到四元超立方体；奇偶性证明 `00` 与 `11` 不能由三步重着色路径连接，
  从而给出 Hamilton-connected 下界，并另外证明该图没有三角形；
- `PlanarRecoloring/Frozen.lean` 验证正文中立方体四着色的冻结性质：每条立方体边的两端颜色不同，
  且每个顶点的三个邻点恰好出现其余三种颜色。

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
lean PlanarRecoloring/Bridge.lean
lean PlanarRecoloring/LowerBound.lean
lean PlanarRecoloring/Frozen.lean
```

这不是把全文主定理宣称为已形式化。正文中的平面嵌入与 Euler 计数、
Grötzsch 三着色、排列图 Hamilton-connected 结果、补充附件的有限证书、
任意阶纤维拼接和结构归纳仍是待形式化的接口；它们依赖正文引用的
Choo--MacGillivray、Havel 等外部结果或尚未定义的平面图数据结构。本目录
只报告上述自足定理的 Lean 检查结果，不用 `sorry`、`axiom` 或计算报告替代这些证明。
