# 四色 Hamilton-connectedness 子类核查：2026-10-10

## 结论

对下面两个类，当前证据都只能写
\[
4\le \operatorname{hc}\le 5:
\]

- 平面、围长至少五、至多七个不同的五圈；
- 平面、围长至少五且 \(\Delta\le 3\)。

不能把正文表格改成 `hc=4`。现有正文证明的是四色 Hamilton 性，不是四色 Hamilton-connectedness。

## 下界与上界

下界对两个类相同：\(C_6\) 属于两个类，\(\mathcal R_3(C_6)\) 有周期冻结着色 `012012`，因而不连通，更不可能 Hamilton-connected，所以阈值至少为四。上界五来自前面的 triangle-free planar Hamilton-connected theorem，因为围长至少五的图是 triangle-free。

## 证明缺口

至多七个五圈的四色归纳在一般情形使用 Hamilton cycle 的 independent-set restoration；其 Hamilton-connected 版本只覆盖两个端点在删去的部分上的限制不同的情况。相同 restriction 的端点没有被处理。相邻二度点、subdivided-star 和其他特殊分支也只给出 Hamiltonian lift。

\(\Delta\le3\) 的四色归纳还依赖 `(2,3,2)` 路、分离二度点以及 protected-pentagon restoration。这些步骤均以较小图的 Hamilton cycle 为输入，没有任意规定端点的路径版本。现有有限回放只核验列出的局部 cycle、seed、pool 和接口记录，不能把这些局部回放外推成任意阶的 Hamilton-connected 定理。

## 文献核查

针对平面围长至少五的重染色，Bartier--Bousquet--Feghali--Heinrich--Moore--Pierron 的结果证明四色重染色图连通，并讨论直径；摘要没有 Hamiltonian 或 Hamilton-connected 结论。它不能填补上述端点控制缺口。

因此正文保留 `4 <= hc <= 5`，并在四色子类章节明确记录缺口；只有得到 endpoint-preserving restoration lemmas，或找到并完整验证四色反例，才应改动该表。
