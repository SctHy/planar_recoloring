# 重大修订说明

本次修订针对审稿意见中的 P0/P1 证明缺口完成了正文、有限验证器和投稿包同步。当前实物为正文 27 页、证书附件 12 页；正文和附件均以 pdfLaTeX 各编译两遍。

主要数学修订：

- 重写 `subdivided-star lift`。树边按颜色重复类型显式构造，说明每次改变中心颜色时所需的列表交集，并处理非二元纤维的三角形/方形接口；同时明确辅助顶点与中心不相邻，因此不会产生原审意见所担心的冲突。
- 将 `(2,3,2)` bad-run 的拼接写成任意长度的归纳不变量：保留首层四条接口边，并在最新层保留至少两条可用内部边。
- 将五边形恢复中的 component-graph connectivity、protected-edge product 和 tree-splicing 写成独立引理，明确产品坐标、pool/reserve 边、公共保护边和逐步拼接不变量。
- 展开含桥的面长计数、删除五边形后的外侧面计数、桥双重计数以及唯一二度点分支中的对偶传播闭包证明；修正 `Subcubic blocks` 的定理标签。
- 在正文中加入冻结着色定义、Bartier 等工作的 connectivity/Hamiltonicity 区分、icosahedron 的显式六色模型和 arrangement-graph 参数约定。

有限证书与复现：

- `verify_protected_pentagons.py` 新增全部 `23^2 = 529` 个产品类型、两层/三层 seed、protected-edge 保留和 alternating reserve splice 的有限重放；当前报告记录 16,008 个产品 block cycle。
- `verify_all.py --check-manifest` 独立检查投稿包中每个交付文件的字节数和 SHA-256，并核对清单覆盖范围。
- 当前完整检查为 3 个正向套件通过、9 个负例拒绝；证书源码 SHA-256 保持为 `104d1d399dcebfa4a6411933989a01d24f771400a9d5bbdf98a9808c874c0410`。
- 证书只覆盖列出的有限局部状态、接口和产品重放；任意长度 bad-run、任意底层圈的 component-graph/tree-splicing 以及结构归纳仍由正文解析证明承担，不能把有限通过误读为全局形式化验证。

交付检查：

- 根目录正文和 `output/publication/` 独立编译结果均为 27 页；附件均为 12 页。
- 重新生成 `manifest.json` 和 `output/publication.zip`；ZIP 直接包含交付文件，不包含 LaTeX 辅助文件、缓存或临时渲染。
- 作者、单位、通讯方式、基金/数据/AI 声明仍需在正式投稿前按实际信息填写，未在本次修订中虚构。
