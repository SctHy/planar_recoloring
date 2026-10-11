# Hamiltonian and Hamilton-connected thresholds for planar recolouring graphs

主论文是 `planar_recoloring_hamilton_thresholds.tex` / `.pdf`；
独立证书附件是 `supplement/article_certificates.tex` / `.pdf`。
`output/publication/` 包含整理后的投稿文件、复核报告和文件哈希，
`output/publication.zip` 是同一文件包。

当前简化版为正文 24 页、独立证书附件 12 页。正文保持 11pt 字号和一英寸
页边距；端点构造抽成公共引理，相邻对的接口论证合并处理，重复的反例和
阈值说明已收紧。附件的端点路径和 splice pools 使用双栏，字面证书保持原样。

稿件按 [OpenAI math 稿件](https://github.com/openai/math) 的常见叙述结构修订：
引言列出三条主定理，明确已有文献与本文加强的关系，说明证明路线，
将长证书移到可独立编译的附件，并保留明确的开放问题。
正文没有采用未通过审查的旧证明片段。

主要修订：

- 重写摘要和引言；提前放置阈值表，补入 bipartite 和 block-subcubic 两类。
- 将退化图证明共享的纤维记号统一，压缩重复步骤；补全 `d+3`
  对 Hamilton-connectedness 和 vertex-pancyclicity 的统一最优性证明。
- 将已有 block-subcubic 结果提升为正式定理，并说明 cutvertex 总度可以无界。
- 修正相邻顶点恢复中三元素／四元素列表变化的表述和检查范围。
- 补全五边形保护边、目标 pool 排除、两层／三层种子和全部 313 个接口的检查。
- 使用正文实际采用的三条路径循环，验证所有对称像和安全公共边。
- 替换过程性研究记录，给出最终证书契约和复现命令。

从当前目录运行：

```sh
python3 supplement/verify_all.py
pdflatex planar_recoloring_hamilton_thresholds.tex
pdflatex planar_recoloring_hamilton_thresholds.tex
cd supplement
pdflatex article_certificates.tex
pdflatex article_certificates.tex
```

验证需要 Python 3.10 或更高版本，只使用标准库；编译直接使用 pdfLaTeX。
每份文档编译两遍以解析交叉引用，PDF 和编译辅助文件默认生成在源码旁；
辅助文件由 Git 忽略。
证书格式、检查覆盖范围和历史文件说明见
[supplement/README.md](supplement/README.md)。

投稿前需要填入实际作者、单位、联系信息，并按目标期刊处理作者声明、
AI 使用披露和模板。当前成果是完成编辑与有限证书复核的正式研究稿；
整篇解析证明仍需要独立同行审读。未将一般 planar girth-five 的四色情形
写成已经解决的定理。

修改前原稿及哈希清单保存在
`output/editorial/publication-revision-20261012-001822/original/` 和
同级 `original-manifest.json`。历史 41 页完整稿保持原样。
本次简化前的 26 页正文、14 页附件及完整文件包另保存在
`output/editorial/proof-layout-revision-20261012-005742/original/`，
同级保存修订差异和排版检查结果。
