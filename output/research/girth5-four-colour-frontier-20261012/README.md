# girth5-four-colour-frontier-20261012

研究记录：一般平面围长五图四色 Hamiltonicity（`h(P_5) = 4`）能否沿现有
保护五边形路线推进。

- `task.md` — 任务范围。
- `研究进展.md` — 研究结论：新计数引理、局部 C5 纤维精确计算、更新后的前沿。
- `counting-lemma-candidate.tex` — "一个高度数顶点的五面"引理的候选 LaTeX。
- `pentagon_boundary_fibres.py` — 精确有限计算（标准库）。
- `pentagon-boundary-report.json` — 计算输出的完整报告。

复现：

```sh
python3 pentagon_boundary_fibres.py    # 约 3 分钟
```

本轮不修改正文、附件、检查器或投稿包。正文的一般 P_5 边界保持
`4 <= h(P_5) <= 5`。
