# Git / GitHub 使用

远程仓库：<https://github.com/SctHy/planar_recoloring>（私有）。
默认分支为 `main`，通过 HTTPS 和 GitHub CLI 登录凭据推送。

论文源码、PDF、证书、验证脚本，以及 `output/` 中的研究记录和历史备份
均纳入版本管理。`.gitignore` 排除 LaTeX 中间文件、Python 缓存、`tmp/`
和本地凭据文件。忽略文件仍保留在本机。

项目协作规则见 [AGENTS.md](AGENTS.md)。Agent 每次完成一项修改和相应验证后，
自动暂存本次相关文件并创建本地 Git 提交，包括只修改文档的情况，无需再次确认。
远端推送按用户明确的当次或长期授权执行。结束时报告提交号和验证结果。

在项目目录查看改动并保存一个版本：

```sh
git status
git diff
git add <本次修改的文件或目录>
git diff --cached
git commit -m "说明本次修改"
git push
```

从 GitHub 获取更新：

```sh
git pull --ff-only
```

本项目配置 `pull.ff=only`，本地和远程分支分叉时会停止拉取，留待明确处理。
Git 提交作者仅在本仓库配置，不修改全局作者设置。

在另一台电脑首次获取项目：

```sh
gh auth login
git clone https://github.com/SctHy/planar_recoloring.git
cd planar_recoloring
```

论文与有限证书的复现命令见 `README.md` 和 `supplement/README.md`。
历史研究候选文件与当前论文采用的证明之间的边界保持原有文档说明。
