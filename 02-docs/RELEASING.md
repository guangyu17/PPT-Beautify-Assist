# 版本发布与 GitHub 同步

所有命令从仓库根执行。Python 3.10+，依赖见 requirements.txt。

## 1. 审查来源与版本

- 查看 `git status --short --branch`，保留现有修改；`git fetch origin` 后审查远程差异。
- 工作树干净且可快进时，使用 `git merge --ff-only origin/main`；有分歧时先处理，不强制覆盖。
- 比较收到的版本与 `01-skills/ppt-beautify-studio/`，记录新增、修改和删除，不盲目整包替换。
- 更新 VERSION、SKILL.md 的 metadata.version、README、CHANGELOG 和对应审查记录。
- 保留现有 MIT LICENSE；不修改外部技能或全局安装，不覆盖真实个人偏好。

## 2. 验证

```bash
python 05-tools/check_repository.py
python -m unittest discover -s 04-tests -v
```

有 skill-creator 时，再用它的 `scripts/quick_validate.py` 校验 `01-skills/ppt-beautify-studio`。
Windows 可使用 `python -X utf8`，避免中文路径或默认编码影响校验。
上述检查不调用在线服务。若组合/渲染逻辑改变，应再制作真实 Office 渲染样例并看图。
未调用的生图服务、未执行的视觉或行为测试，在报告中明确标记未测。

## 3. 检查提交内容

```bash
git diff --check
git diff --stat
git status --short
```

只暂存本次维护文件，查看 `git diff --cached` 后提交。不要提交密钥、个人偏好、完整请求体、
用户 PPT、照片、字体、日志、渲染文件、虚拟环境或缓存；.gitignore 只是辅助，不能代替审查。
不把 imagegen、ifapi-image、relay-imagegen 或 ppt-master 的源码和私密配置复制进来。

## 4. 构建发行包

从已经检查并提交的 Git 快照构建，不递归压缩整个本机目录：

```bash
git archive --format=zip --prefix=PPT-Beautify-Assist/ --output=/absolute/release/PPT-Beautify-Assist-v1.8.0.zip HEAD
git archive --format=zip --prefix=ppt-beautify-studio/ --output=/absolute/release/ppt-beautify-studio-v1.8.0.zip HEAD:01-skills/ppt-beautify-studio
```

路径和版本按实际修改。运行前确认输出文件不存在，避免覆盖旧包。
技能 ZIP 还应在 `ppt-beautify-studio/LICENSE` 加入该提交的根 LICENSE，保留版权及许可声明。
只打包技能文件；源码包包含文档、测试与维护工具，但不包含 `.git`。
验证两个 ZIP 的 CRC、成员内容与提交一致，生成 SHA256SUMS.txt；从临时解包目录执行离线测试。
本项目的临时发行包和检查输出可放入 `dist/`（已被 Git 忽略），或用户指定的位置。
长期维护的审查结论放入 `02-docs/`。维护流程不依赖项目外的编号目录。

## 5. 同步

用户任务包含 GitHub 同步时，普通 `git push origin main`，再确认 HEAD 与远程 main 一致。
若远程有新提交，先合并处理、重新验证受影响内容；不使用 force push。
普通代码推送不创建 GitHub Release 或 tag；这些是独立发布动作。

## 保留的产品边界

IF API 完整 body 的本地字节检查不能证明隐藏桌面封装后的请求大小。
版本号从 1.7 升到 1.8 不会自动关闭临时请求体保护；关闭仍需实际修复确认并记录在私有偏好中。
