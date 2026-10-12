# 正文结果的 Lean 形式化审计

审计对象是仓库当前版本的 `main.tex`。下表逐项列出正文中带标签的
`theorem`、`lemma`、`proposition`、`claim` 和 `remark`（共 46 项）。
“部分”表示 Lean 中有一个严格的局部特例或下界片段，但不能替代正文中
带有相同量词和假设的命题；“有限证书”表示补充材料的 Python 检查器有
有限数据证据，但该检查不是 Lean 证明。

## 已覆盖的可复用 Lean 内容

这些声明本身可以由 Lean 内核检查（它们不是正文标签的完整替代）：

| 文件 | 内核检查的内容 |
| --- | --- |
| `PlanarRecoloring/Core.lean` | `FiniteGraph`、`Coloring`、`Proper`、单顶点重着色邻接、可用颜色；邻接关系的自反性/对称性；显式列表路径的 `Consecutive` 和 `SpanningPath`。 |
| `PlanarRecoloring/Bridge.lean` | `exists_avoiding_of_two`、`exists_avoiding_of_three`、`bridge_colours_three` 以及 `cyclic_three_colours`：线性三层和循环三层的严格局部桥接步。 |
| `PlanarRecoloring/LowerBound.lean` | 两个孤立顶点、二色状态的四元超立方体：`q2_not_hamilton_connected` 和 `q2_has_no_triangle`，即 `prop:degenerate-sharp` 在 `d=0` 的障碍片段。 |
| `PlanarRecoloring/Frozen.lean` | 立方体四着色的合法性、每条坐标翻转边以及 `cube_colouring_is_frozen`。它对应三角自由下界的有限局部模型，不是 `thm:trianglefree-hc` 的证明。 |
| `PlanarRecoloring/Hamilton.lean` | `HamiltonPath`、`HamiltonCycle`、`HamiltonConnected`、`VertexPancyclic` 的列表定义，路径反向和若干显式列表引理；没有证明正文中的任何全局阈值。 |
| `PlanarRecoloring/Fibre.lean` | `FibrePath`、`ClosedFibrePath`、不交列表的无重复拼接、允许两侧不同内部关系的接口边拼接及连续性保持；这是两纤维抽象接口，不是正文的循环多纤维提升。 |
| `PlanarRecoloring/PermutationParity.lean` | `d=1,k=3` 时 `K_2` 的六状态表示、排列奇偶性边翻转、无 Hamilton 路（指定端点）及无三角形。 |
| `PlanarRecoloring/ProductParity.lean` | 二进制积的列表表示、单坐标翻转的 xor 奇偶性、索引路径的奇偶传播及奇长度闭路障碍。 |
| `PlanarRecoloring/General.lean` | 对称/无环图、边和退化性的列表接口；可用颜色、显式单顶点重着色、颜色置换以及相应的基础引理。该文件已由根模块导入并通过内核检查，但这些接口本身不证明正文的全局标签。 |

上述模块均不含 `axiom`、`sorry` 或 `admit`。形式化目录的这些基础接口
仍然不能替代下面逐标签列出的正文定理；尤其是具有平面嵌入、任意长度
纤维拼接或外部文献假设的命题，尚没有对应的 Lean 定理。

## 逐标签结论

### 退化图和纤维接口

| 主文标签 | 状态 | 对应内容或缺口 |
| --- | --- | --- |
| `thm:main-degenerate` | 待形式化 | 聚合定理；其 Hamilton-connected、vertex-pancyclic 和精确阈值均未证明。 |
| `lem:list-cycle` | 待形式化 | 尚无任意长度列表的循环选取引理；`bridge_colours_three` 不是此命题。 |
| `lem:single-lift` | 待形式化 | 尚无单顶点 clique-fibre 的 Hamilton cycle 提升。 |
| `lem:bridge-colours` | **部分** | `Bridge.lean:bridge_colours_three` 只处理三个列表、谓词表示的局部情形；正文允许任意 `t\ge1` 和有限集合。 |
| `lem:clique-endpoints` | 待形式化 | 端点控制、删除一个基状态和纤维拼接均未编码。 |
| `thm:degenerate-hc` | 待形式化（含外部依赖） | 需要排列图 `A_{k,n}` 的 Hamilton-connected 结果（正文引 `HLTH04`）以及完整归纳。 |
| `thm:degenerate-vp` | 待形式化 | 需要闭合提升、长度区间覆盖和异常二色情形的证明。 |
| `rem:not-edge-pancyclic` | 待形式化 | 星图中无三角形边的反例未在 Lean 中建立。 |
| `prop:degenerate-sharp` | **部分** | `LowerBound.lean` 证明 `d=0` 的四元超立方体障碍；`PermutationParity.lean` 另证明 `d=1,k=3` 的 `K_2` 六状态奇偶障碍。一般 `K_{d+1}` 的 `d\ge2` 奇偶性与统一阈值未形式化。 |
| `thm:main-planar` | 待形式化 | 聚合定理；依赖下列平面、三角自由、森林结果。 |
| `lem:product` | **部分** | `ProductParity.lean` 编码二进制积的单坐标翻转奇偶障碍和奇长度闭路排除；超立方体偶端点路径构造及含三元因子的 Hamilton-connected 正向定理仍未编码。 |
| `lem:path-fibre` | 待形式化 | 多坐标纤维沿路径的可达出口归纳未编码。 |
| `lem:independent-hc` | 待形式化 | 独立集纤维的 Hamilton-connected 恢复未编码。 |
| `lem:fibre-lift` | 待形式化（有局部接口） | `Fibre.lean` 已证明不交两纤维路径沿接口边的线性拼接；正文所需循环分层、端点匹配和 Hamilton cycle 提升仍未编码。 |
| `lem:independent-restoration` | 待形式化 | 独立集的 Hamilton cycle 恢复未编码。 |
| `lem:single-hc` | 待形式化 | 最小状态度数条件下的单顶点 Hamilton-connected 恢复未编码。 |

### 平面和三角自由类别

| 主文标签 | 状态 | 对应内容或缺口 |
| --- | --- | --- |
| `lem:marked-five` | 待形式化（结构） | 平面三角剖分、Euler 计数和距离三的两个五度点均没有平面嵌入数据结构或证明。 |
| `thm:planar-hc` | 待形式化（含外部依赖） | 依赖 `lem:marked-five`、退化恢复、七色度数计数及 icosahedron 冻结着色；正文还引用 `BP16`。 |
| `lem:pair-five-endpoints` | 有限证书，未 Lean 形式化 | Appendix A 的七种类型和端点分类由补充检查器核验；无 Lean 状态图和 Hamilton 路径证明。 |
| `lem:pair-five-reset` | 有限证书，未 Lean 形式化 | 依赖上项有限类型及任意长度的可达出口归纳。 |
| `thm:trianglefree-hc` | 待形式化（含外部依赖） | 依赖 Grötzsch 三着色定理、上述相邻对恢复及完整平面归纳；四维立方体下界只有局部 Lean 模型。 |
| `lem:marked-two` | 待形式化（结构） | girth-six 平面 Euler 计数和距离三的两个二度点未编码。 |
| `thm:girth6-hc` | 待形式化（含外部依赖） | 依赖 `lem:marked-two`、独立集恢复、退化定理及周期三着色冻结反例。 |
| `thm:forest-hc` | 待形式化 | 退化上界和 `\R_3(P_3)`/`\R_3(K_2)` 下界均未在 Lean 中建立。 |

正文在 `thm:trianglefree-hc` 后还有一个未带 `\\label` 的 bipartite
corollary；它同样没有 Lean 证明。

### girth-five 的四颜色子类

| 主文标签 | 状态 | 对应内容或缺口 |
| --- | --- | --- |
| `thm:main-four` | 待形式化 | 聚合定理；两个 girth-five 子类的 Hamiltonian 证明未编码。 |
| `lem:subdivided-star-four-subclass` | 待形式化 | 四份底部循环和树形交换、产品纤维提升均未编码。 |
| `lem:five-face-identity-subclass` | 待形式化（结构） | 平面嵌入中的面长、Euler 恒等式及五面为简单圈未编码。 |
| `cor:seven-pentagons-two-degenerate` | 待形式化 | 由面计数推出二退化的推论未编码。 |
| `thm:seven-pentagons` | 待形式化（含外部依赖） | 依赖上面两个结构结果、`lem:single-lift`、`lem:adjacent-two-four`、`lem:subdivided-star-four-subclass` 以及三着色输入。 |
| `lem:adjacent-two-four` | 待形式化 | 相邻二度点的七状态纤维循环和公共边拼接未编码。 |
| `lem:separated-two-g5` | 待形式化（含外部依赖） | 依赖 Grötzsch 三着色和 `lem:independent-restoration`。 |
| `prop:badrun` | 待形式化 | `\R_3(P_3)\square P_\ell` 的任意长度显式循环未编码。 |
| `lem:pathsafe` | 有限证书，未 Lean 形式化 | Appendix B 的三类好边界和安全边分类由补充数据/检查器支持。 |
| `lem:badblock` | 有限证书，未 Lean 形式化 | 依赖 `prop:badrun` 与安全边保留的任意长度坏段拼接。 |
| `lem:path232` | 有限证书，未 Lean 形式化 | 依赖上述好/坏边界证书及底部 Hamilton cycle 的分块拼接。 |
| `thm:subcubic` | 待形式化（含有限证书和外部依赖） | 依赖五边形附件 C--D、Grötzsch 三着色、面计数和 `lem:two-pentagons-restore`。 |

### 受保护五边形和块次三图

| 主文标签 | 状态 | 对应内容或缺口 |
| --- | --- | --- |
| `lem:pentagon-path-blocks` | 有限证书，未 Lean 形式化 | Appendix C 的 23 个组件分块由检查器核验；未定义相应 Lean 状态图。 |
| `lem:pentagon-protection` | 有限证书，未 Lean 形式化 | Appendix C--D 的 2304 个边界和 313 个标准源接口由有限记录支持。 |
| `lem:protected-product` | 待形式化（依赖有限证书） | 产品循环和保护边的任意组件拼接尚无 Lean 证明。 |
| `lem:pentagon-overlap` | 待形式化 | 重叠组件至少十个公共状态的组合计数未编码。 |
| `lem:pentagon-component-graph` | 待形式化 | 两个常值组件标签的重置和连通性归纳未编码。 |
| `lem:protected-tree-splicing` | 待形式化 | 有界度数树上的受保护边拼接未编码。 |
| `lem:two-pentagons-restore` | 待形式化 | 两个五边形的同步外部变化、组件图和树拼接未编码。 |
| `lem:subcubic-face-count` | 待形式化（结构） | 平面面长/度数计数恒等式未编码。 |
| `lem:two-separated-five-faces` | 待形式化（结构） | 桥、对偶三角剖分和两侧面计数的完整论证未编码。 |
| `thm:subcubic` | 待形式化 | 聚合定理；其归纳还依赖本节所有缺口。 |
| `thm:block-subcubic` | 待形式化 | 块割树、端块面计数和五边形恢复未编码。 |

## 外部结果和有限证据的边界

下面的输入目前不能被“有 Lean 接口”替代：

1. `HLTH04` 的排列图 Hamilton-connected 结果、Grötzsch 三着色定理以及正文引用的 `ChMa11`、`BP16` 等文献结果尚未导入并形式化。
2. 平面嵌入、面、对偶、girth、块割树和 Euler 公式没有在本目录定义；因此所有 `marked-*`、面计数和块结构命题仍是待形式化的数学内容。
3. `supplement/verify_all.py` 及其附属检查器只核验有限字面证书（合法性、覆盖、对称轨道、接口边和保护池）。正文明确说明它们不核验任意长度提升、未列阶数的产品循环、底部 Hamilton cycle 的存在或树形拼接。因此这些脚本不能把上述“有限证书”标签升级为 Lean 形式化。

## 可复现实验记录

在审计时运行了：

```sh
cd formalization
PATH=/tmp/lean-download/tool/lean-4.34.1-darwin_aarch64/bin:$PATH lake build
PATH=/tmp/lean-download/tool/lean-4.34.1-darwin_aarch64/bin:$PATH lake env lean PlanarRecoloring/General.lean
```

根 Lake 目标构建成功，单独检查 `General.lean` 也成功。当前形式化目录
不含 `axiom`、`sorry` 或 `admit`；“构建成功”只说明 Lean 接受当前源文件，
不表示
正文任何未列为“已覆盖”的标签已经形式化。该报告不新增 `axiom` 或
`sorry`，也不修改现有 Lean 源码。
