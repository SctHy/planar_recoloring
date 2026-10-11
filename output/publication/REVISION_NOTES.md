# 重大修订说明

本次修订针对审稿意见中的 P0/P1 证明缺口完成了正文、有限验证器和投稿包同步。当前实物为正文 27 页、证书附件 12 页；正文和附件均以 pdfLaTeX 各编译两遍。

本次名称风格修订按正文编号优先的规则处理：删除主文 36 个 theorem/lemma/proposition/corollary 的方括号标题，保留全部内部 `\label` 和交叉引用；protected-pentagon 小节的四个局部事实改为 Claim 1--4，普通工作术语保持小写。附件、证书记录和历史完整稿未改动。

本次复审小修进一步修正“两条分离五面”结构引理的面计数。令
`epsilon = 1_{z in B}`，则 `p_H = epsilon`、`q_H = r - epsilon + q'`，
从而正文使用
`f_5^in = ell + 6 - 2r - 2epsilon - 2q' + L`。
三个分支的数量下界均显式使用 `epsilon + q' <= 1`；有限检查、解析证明与未解决的总体问题仍按下文边界区分。

主要数学修订：

- 重写 `subdivided-star lift`。树边按颜色重复类型显式构造，说明每次改变中心颜色时所需的列表交集，并处理非二元纤维的三角形/方形接口；同时明确辅助顶点与中心不相邻，因此不会产生原审意见所担心的冲突。
- 将 `(2,3,2)` bad-run 的拼接写成任意长度的归纳不变量：保留首层四条接口边，并在最新层保留至少两条可用内部边。
- 将五边形恢复中的 component-graph connectivity、protected-edge product 和 tree-splicing 写成独立编号事实，明确产品坐标、pool/reserve 边、公共保护边和逐步拼接不变量。
- 在 protected-product 证明中明确公共保护边的产品坐标传输 `Phi_1 x Phi_2`，并将 component-graph 的两个 reset index 写成通向共同 checkpoint 的路径；附标签转移表说明实际 component graph 的连通性。
- 展开含桥的面长计数、删除五边形后的外侧面计数、桥双重计数以及唯一二度点分支中的对偶传播闭包证明；修正 `Subcubic blocks` 的定理标签。
- 在正文中加入冻结着色定义、Bartier 等工作的 connectivity/Hamiltonicity 区分、icosahedron 的显式六色模型和 arrangement-graph 参数约定。

有限证书与复现：

- `verify_protected_pentagons.py` 新增全部 `23^2 = 529` 个产品类型、两层/三层 seed、protected-edge 保留和 alternating reserve splice 的有限重放；当前报告记录 16,008 个产品 block cycle。
- `verify_all.py --write-reports` 显式生成三套正向报告、九个负例报告和汇总；不带选项运行仍保持该写入行为。
- `verify_all.py --check-manifest` 现在是只读检查，仅核对投稿包中每个交付文件的字节数、SHA-256 和清单覆盖范围，不覆盖任何报告。
- 报告不再写入 `platform.python_version()`；其字节和 manifest 哈希在支持的 Python 3.10+ 版本间保持稳定。
- 当前完整检查为 3 个正向套件通过、9 个负例拒绝；证书源码 SHA-256 保持为 `104d1d399dcebfa4a6411933989a01d24f771400a9d5bbdf98a9808c874c0410`。
- 证书只覆盖列出的有限局部状态、接口和产品重放；任意长度 bad-run、任意底层圈的 component-graph/tree-splicing 以及结构归纳仍由正文解析证明承担，不能把有限通过误读为全局形式化验证。

交付检查：

- 根目录正文和 `output/publication/` 独立编译结果均为 27 页；附件均为 12 页。
- 重新生成 `manifest.json` 和 `output/publication.zip`；ZIP 直接包含交付文件，不包含 LaTeX 辅助文件、缓存或临时渲染。
- 作者、单位、通讯方式、基金/数据/AI 声明仍需在正式投稿前按实际信息填写，未在本次修订中虚构。
