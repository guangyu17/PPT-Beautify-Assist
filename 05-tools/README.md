# 仓库维护工具

从仓库根运行：

```bash
python 05-tools/check_repository.py
```

检查版本一致性、维护目录 README、本地 Markdown 链接、Python 语法、JSON/YAML 与围栏 JSON 示例。
所有嵌套SKILL.md还检查名称与目录一致、名称唯一、描述/正文完整及可解析的frontmatter；不以主技能通过代替子技能检查。
仅读取文件，不联网、不修改技能安装和个人配置。依赖 PyYAML，已列入 requirements.txt。
这项检查补充现有离线回归，不代替真实渲染或技能行为评估。
