# 项目结构与文件管理

本项目根目录以根 README.md 和 AGENTS.md 所在目录为准。目录管理仅覆盖这个 Git 仓库内部。

```text
PPT-Beautify-Assist/
├── README.md               项目入口和使用说明
├── AGENTS.md               代理维护规则
├── CHANGELOG.md            版本变化
├── VERSION                 当前技能版本
├── requirements.txt        Python 依赖
├── LICENSE                 MIT 许可证
├── .gitignore              本地文件排除规则
├── 01-skills/
│   ├── README.md
│   └── ppt-beautify-studio/
│       ├── README.md
│       ├── SKILL.md
│       ├── agents/         界面元数据及 README
│       ├── config/         默认配置及 README
│       ├── references/     按需参考及 README
│       ├── scripts/        技能辅助脚本及 README
│       └── subskills/ui-ux-design/  内置设计子技能，含SKILL.md、agents和references
├── 02-docs/                 项目管理、审查和发布文档
├── 03-examples/             布局 JSON 示例
├── 04-tests/                离线回归
└── 05-tools/                仓库维护工具
```

## 放置规则

- 新的项目业务目录沿用两位数字前缀，每个维护目录提供 README，说明用途、入口和维护方式。
- README.md、AGENTS.md、VERSION、requirements.txt 等入口与配置文件保留在根目录。
- 安装技能时复制 `01-skills/ppt-beautify-studio/` 到 Codex 的 `skills/ppt-beautify-studio/`；安装目录和技能包内部不加编号。
- 使用者生成的 PPT、素材、个人偏好、密钥和完整请求体不作为项目源码归档。临时发行与检查结果可放在被 Git 忽略的 `dist/`。
- `.git/`、缓存、虚拟环境和临时构建输出无需 README；其余现有维护目录都提供说明。

## 从旧结构迁移

| 原目录 | 当前目录 |
|---|---|
| `skills/` | `01-skills/` |
| `docs/` | `02-docs/` |
| `examples/` | `03-examples/` |
| `tests/` | `04-tests/` |
| `tools/` | `05-tools/` |

当前检查入口：

```bash
python 05-tools/check_repository.py
python -m unittest discover -s 04-tests -v
```

改名同步更新文档、本地链接、测试导入和发布命令。技能包内容及全局安装仍为 1.8.0，本次目录整理不改变技能功能。
