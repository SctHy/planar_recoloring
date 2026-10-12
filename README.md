# Hamiltonian and Hamilton-connected thresholds for planar recolouring graphs

主论文是 `main.tex` / `.pdf`；
独立证书附件是 `supplement/article_certificates.tex` / `.pdf`。
`output/publication/` 包含整理后的投稿文件、复核报告和文件哈希，
`output/publication.zip` 是同一文件包。

与正文证明对应的 Lean 4 形式化位于 `formalization/`。它固定 Lean 4.34.1，
内核检查有限重染色图与 Hamilton 性质定义、重着色和颜色置换接口、三层桥接颜色引理、
任意纤维链与恢复顶点的严格拼接接口、循环桥接选色、二进制积的路径奇偶障碍、`K_2` 三色六状态的排列奇偶障碍、两个孤立顶点的二色障碍，
以及立方体四着色的冻结性质；平面结构归纳、外部引理
和补充证书的任意阶拼接仍按 `formalization/README.md` 所列边界保留为待形式化内容。

当前复审小修版为正文 27 页、独立证书附件 12 页。正文保持 11pt 字号和一英寸
页边距；端点构造抽成公共引理，相邻对的接口论证合并处理，重复的反例和
阈值说明已收紧。附件的端点路径和 splice pools 使用双栏，字面证书保持原样。
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
- 统一采用编号优先的结果排版，删除主文方括号标题，并将保护五边形的四个局部事实改为 Claim 1--4。
- 将引言阈值表收窄并居中，保留完整的类别与阈值信息。

仓库正文与 `output/publication/main.tex`、`.pdf`
保持对应；独立证书与 `output/publication/supplement/article_certificates.tex`、
`.pdf` 保持对应。投稿目录还包含相同版本的检查器、报告、
`computation-record.json` 和 `manifest.json`，`output/publication.zip` 直接打包
这些交付文件，不含 LaTeX 辅助文件或缓存。
作者、单位、通讯方式及基金、数据、AI、利益冲突等投稿声明尚未提供，当前源码和
投稿包保留空占位，正式投稿前需按实际信息填写。

从当前目录运行：

```sh
python3 supplement/verify_all.py --write-reports
python3 supplement/verify_all.py --check-manifest
pdflatex main.tex
pdflatex main.tex
cd supplement
pdflatex article_certificates.tex
pdflatex article_certificates.tex
```

第一条命令显式生成有限验证报告；不带选项运行 `verify_all.py` 仍等价于
`--write-reports`。第二条命令只读检查投稿包的 `manifest.json`、交付文件字节数和
SHA-256，不会重写报告或其他交付文件。报告内容不包含解释器小版本，因此在支持的
Python 3.10+ 环境中哈希保持稳定。验证只使用标准库；编译直接使用 pdfLaTeX。
每份文档编译两遍以解析交叉引用，PDF 和编译辅助文件默认生成在源码旁；
辅助文件由 Git 忽略。
证书格式、检查覆盖范围和历史文件说明见
[supplement/README.md](supplement/README.md)。

修改前原稿及哈希清单保存在
`output/editorial/publication-revision-20261012-001822/original/` 和
同级 `original-manifest.json`。历史 41 页完整稿保持原样。
本次简化前的 26 页正文、14 页附件及完整文件包另保存在
`output/editorial/proof-layout-revision-20261012-005742/original/`，
同级保存修订差异和排版检查结果。
