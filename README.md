# PPT Beautify Assist

**当前版本：1.10.0** · 主技能：`ppt-beautify-studio` · 内置子技能：`ui-ux-design` 1.0.0

项目内部按下面的顺序维护；项目根目录就是本 README 所在目录。

| 目录 | 用途与入口 |
|---|---|
| [01-skills](01-skills/README.md) | 可安装技能的正式源码 |
| [02-docs](02-docs/README.md) | 维护、审查与发布文档 |
| [03-examples](03-examples/README.md) | 可复用的布局示例 |
| [04-tests](04-tests/README.md) | 离线回归测试 |
| [05-tools](05-tools/README.md) | 仓库检查工具 |

维护规则见 [AGENTS.md](AGENTS.md)，目录职责与归档约定见 [项目结构](02-docs/PROJECT-STRUCTURE.md)。

将现有 PPT、PDF 页面、截图或大纲，变成风格统一、文字可编辑、图片可分层的演示文稿。
先确定整套页数、视觉风格和版式家族，再做真实样张；用户确认后才生成整套。

> 这是一个 Codex 技能及本地辅助工具项目，不是独立 PowerPoint 插件，也不是新的图像 API 客户端。
> 默认使用 **GPT 原生 imagegen**；可持久切换至 **IF API** 或 **relay-imagegen 自定义中转**。
> 安装技能不意味着当前聊天一定拥有原生图像工具；工具缺失时会明确说明，不静默改用付费中转。

## 1.10.0 的变化

- 直接研读 [Lenny's Newsletter设计文章](https://www.lennysnewsletter.com/p/how-to-turn-your-ai-into-a-world) 的公开技巧1–6，扩展“探索、定义、交付”为可执行的设计brief、代表状态、实际评审与减法；第7节付费正文未纳入。
- `distinctive-ai-design` 更名后继为内置 [ui-ux-design](01-skills/ppt-beautify-studio/subskills/ui-ux-design/README.md) 1.0.0：独立编写设计、动画编排、图像与shader/3D结合、视频连续性、触摸/减少动态、性能与资源生命周期指导。
- 新增 [PPT动画/3D适配](01-skills/ppt-beautify-studio/references/motion-3d-ppt.md)：区分PowerPoint原生动画、Morph、3D模型和预渲染无字媒体，记录motion_plan，并分别验证静态阅读版与目标宿主放映。
- 保持原文、页序、原生文字、样张门和已有预算。现有组合脚本仍是静态组合器，不把设计计划或网页shader称作已实现的PPT动画。
- PPT包内包含子技能，不需外部旧技能；另提供ui-ux-design单独ZIP供其他环境使用，本机不重复安装两份同名入口。

来源、迁移及检查见 [1.10.0记录](02-docs/V1.10.0-REVIEW.md)；技术出处见 [子技能来源](01-skills/ppt-beautify-studio/subskills/ui-ux-design/references/sources.md)。

## 1.9.0 已有能力

- 新增 [有辨识度的 PPT 设计](01-skills/ppt-beautify-studio/references/distinctive-design.md)：把受众、观看场景、讲述目标和目标感受落实为设计 brief；方向之间比较构图、阅读路径、字体和图像角色，避免仅换配色。
- 模式1视觉重设计和模式3使用新指导。已有明确方向只细化该方向；局部修复直接处理问题；PDF/截图忠实还原仍以原稿为准。
- 真实 PPTX 渲染后每轮聚焦1–3个主要问题，先做最多两轮审美精修；与原有每页4轮本地修复共用预算，审美轮次结束不豁免丢字、遮挡和溢出等缺陷。
- 减法针对无用途的装饰，保护原文、强调、数据、图例和来源。独立评审仅在允许委派时使用，否则明确自查；不以主观分数冒充视觉或功能验证。
- 研读 [distinctive-ai-design](https://github.com/houxin0010/distinctive-ai-design/tree/92c68366767b98924fe2719c16659e7f1e93c7af) 后独立编写 PPT 场景指导；不复制其源码，不增加运行依赖，不改 Python 工具、个人偏好或默认生图通道。

来源、融合范围及检查见 [1.9.0 审查记录](02-docs/V1.9.0-REVIEW.md)，详细变化见 [CHANGELOG](CHANGELOG.md)。

## 1.8.0 已有能力

- 新增 [故事线规划](01-skills/ppt-beautify-studio/references/storyline-pyramid.md)：商业汇报先规划结论标题、分论点和事实支撑，再确认页数与风格。
- 缺少事实时明确标注待补，不编造数字或定性结论。学术、叙事等场景仅在用户要求时使用这套商业框架。
- 现有 PPT 的逻辑诊断为可选项；仅换背景/配色、不动文字时不主动诊断。PDF/截图忠实还原不套用故事线重构。
- 新增代理维护规则、各目录 README、更新记录及仓库检查工具；Python 技能工具和配置格式未改变。

详细变化见 [CHANGELOG](CHANGELOG.md)，来源差异和审查修订见 [1.8.0 审查记录](02-docs/V1.8.0-REVIEW.md)。

## 1.7.0 已有能力

- 新增 **超高／高／中／低四档**；不是三个档位。档位控制设计投入与素材复杂度，不破坏原文保真和可编辑性。
- 默认原生生图。用户单独说“以后使用某通道”即可保存偏好，不在每次对话重新询问服务商。
- **材质对话框、玻璃/亚克力/纸纹卡片使用真实生图素材**，文字单独原生排版。不用普通透明矩形或模糊补丁冒充精致材质。
- 撤销旧版固定每批2张、固定等待、禁止4K、768px/96KiB预览等硬规则。
- IF API 桌面临时改为 **每次发送前检查最终请求体字节数**，而非只检查图片分辨率。
- 新增持久偏好工具、请求体预检工具、可运行离线测试和可发布项目结构。
- 保留图片融合、渐变透明、多层可回放配方、原生时间轴/线框/关系线、字体规划、素材归档和视觉自检。

## 四档美化

| 档位 | 适合/投入 | 素材策略 |
|---|---|---|
| **超高 ultra** | 在允许的风格内充分使用主题图标、材质、逐页场景与精细融合 | 每个组件要有内容目的；不盲目加花。材质框必须生图，先报预计量 |
| **高 high** | 重点页精修、全套统一，少用多余框体 | 可生成并复用边框/关键图标；背景是否生成仍听用户需求，不默认每页重画 |
| **中 medium** | 减少调用与上下文，优先复用 | 现有图片＋本地融合、少量共享背景/章节图；默认不做材质对话框 |
| **低 low** | 简约商务/学术方向 | 边框、已有图片、原生文字及纯色底为主；不主动生成复杂全页背景 |

“超高＋简约”仍是简约，只在排版、字体、留白、图像质量上精修，不自动变成奇幻风。
中/低档若明确需要材质框，同样使用生图素材；否则直接省略，不降级为丑的平板框。
所有档位都保留：整套规划、样张确认、原文完整、原生文字、真实渲染和问题披露。

## 三种工作模式

1. **美化现有 PPTX**：默认文字、页数、顺序不变，重新设计背景/版式。
2. **图片/PDF/扁平 PPT 还原**：以原貌为准，不擅自美化或重写。
3. **大纲生成**：商业汇报先规划故事线与事实缺口，再确认完整页数与结构、制作风格样张。其他场景按用户材料与目标组织。

示例请求：

```text
用 $ppt-beautify-studio 美化这份PPT，高档，保留全部原文和页序。
背景不必每页生成，边框可以复用；使用默认原生生图。

用 $ppt-beautify-studio 把这份PDF还原成可编辑PPT，不改设计。

用 $ppt-beautify-studio 按这份大纲制作，超高档但保持简约；先给整套设计方案和样张。
```

## 安装与依赖

### 技能安装

将本项目 `01-skills/ppt-beautify-studio` 文件夹（包含subskills/ui-ux-design）整体复制到：

```text
$CODEX_HOME/skills/ppt-beautify-studio
```

未设置 `CODEX_HOME` 时通常是用户目录的 `.codex/skills/ppt-beautify-studio`。
已有安装应先备份自己的修改；不覆盖个人服务配置或项目素材。此项目未包含任何服务密钥。
主技能直接读取内置子技能，嵌套技能是否出现在宿主选择列表需刷新发现后确认。独立UI任务可按该路径加载`ui-ux-design/SKILL.md`；本机不要再复制一份同名子技能到skills根目录。
从旧distinctive-ai-design迁移时，先把旧安装完整备份到发现目录之外，再退出旧名称的发现入口；只更新PPT安装不会自行清除其他环境中的旧技能。

### Python 与真实渲染

Python **3.10+**（本次测试使用3.12），推荐在虚拟环境中安装：

```bash
python -m venv .venv
# 按本机系统激活 .venv 后：
python -m pip install -r requirements.txt
python 05-tools/check_repository.py
python -m unittest discover -s 04-tests -v
```

在 Codex 桌面中，也可让代理通过 `load_workspace_dependencies` 使用自带的 Python/库。
渲染 `.pptx` 需要 **LibreOffice** 或 Windows 上可用的 **Microsoft PowerPoint**。
PDF 使用已有 PDFium 库渲染，不强制安装 PyMuPDF；系统未装 Office 渲染器时只保留草稿，不冒充验收通过。

### 外部技能（不随此仓库复制）

| 依赖 | 使用范围 |
|---|---|
| `imagegen` | 默认原生图像生成/编辑；使用其内置工具，不自动转CLI |
| `ifapi-image` | 仅用户选择 IF API 时；[中转站链接](https://ifapi.org/sign-up?aff=iykE) |
| `relay-imagegen` | 仅用户选择自定义中转时，复用现有脚本/私密配置 |
| `visualize` | 风格样张与真实渲染的对照展示，不是自动视觉检测器 |
| `ppt-master` | PPTX原图/主题/图表提取复用；默认与本技能相邻，可用 `--ppt-master` 指定路径 |

这些技能的脚本、许可证和配置由各自项目维护；本项目不修改它们。

## 生图通道：选择一次，后续复用

默认配置文件 `01-skills/ppt-beautify-studio/config/defaults.json`：
- backend：`native`
- tier：空（新项目未指定档位时问一次）
- IF API临时请求体保护：开启，仅当使用对应链路时适用

实际个人偏好写在 **仓库外**：

```text
$CODEX_HOME/ppt-beautify-studio/preferences.json
```

例如在聊天里说：

```text
以后这项技能默认用GPT原生生图。
以后这项技能改用IF API。
以后改用relay-imagegen，私密配置在我指定的本地文件中。
以后默认高档，这次不必再问档位。
```

也可在明确授权后由代理使用辅助工具（以下命令从仓库根运行）：

```bash
python 01-skills/ppt-beautify-studio/scripts/studio_settings.py show
python 01-skills/ppt-beautify-studio/scripts/studio_settings.py set --backend native --confirmed
python 01-skills/ppt-beautify-studio/scripts/studio_settings.py set --backend ifapi --confirmed
python 01-skills/ppt-beautify-studio/scripts/studio_settings.py set --backend relay --relay-config /absolute/private/config.json --confirmed
python 01-skills/ppt-beautify-studio/scripts/studio_settings.py set --tier high --confirmed
```

`--confirmed` 只是代理记录用户明确指令，不是软件自动获得了授权。
本设置文件只存服务类型/配置路径，不保存 API key。relay凭据只按 relay-imagegen 的私密配置方式保存。
“这次使用…”只影响当前项目；“以后默认…”才更新持久偏好。不可用时不会静默换服务。

## 63MB / 413：真实体积预检，而非固定小图

用户现场报告曾发送约 **63MB** 请求而被 IF API 桌面拒绝。
本项目将其作为已提供的诊断，**没有独立复现或取得供应商官方上限**。
默认采用 **60,000,000字节（十进制60MB）** 本地预算留出余量，可按实际限制调整；不是“63MB以下必成功”的承诺。

### 重要的集成边界

`request_preflight.py` 可以准确测量本地 **最终序列化请求体文件** 的字节数和 SHA-256。
它不是代理拦截器，不会自动拿到桌面内部的 `/responses` 请求，也不会重放请求。

如果 IF API 工具只提供 `prompt/reference_paths`，而桌面会再追加历史、图片编码或封装，那么只测工具参数不足以放行。
**没有完整最终body时返回 `needs_capture`，不伪造检查通过。** 此时需调用方/桌面提供受支持的请求体导出与发送前集成，
或由用户明确选择原生/其他中转；本技能不会创建一个未经授权的旁路客户端。

```bash
python 01-skills/ppt-beautify-studio/scripts/request_preflight.py \
  --backend ifapi --body /private/final-body.bin --complete-body \
  -o /project/logs/preflight-r01.json
```

| 结果 | 退出码 | 含义 |
|---|---:|---|
| `pass` | 0 | 调用者声明的完整body实测未超本地预算，只适用于这份相同字节内容 |
| `exempt` | 0 | 默认原生/非IFAPI relay，或用户确认修复后已关闭临时门禁 |
| `oversize` | 1 | 超预算，先重建更小的独立请求、减少重复参考/编码负载，再重新检查 |
| `needs_capture` | 2 | 完整body不可见或只有估计，不能声称发送前核验完成 |

原生模式默认无此 IF API临时门禁，但仍有原生工具自身的实际限制。
若聊天本身仍通过 IF API 桌面转发，图像用原生也不保证会话请求不出413；必须看失败的真实链路。

超限可把独立页面/资产分成独立请求，或缩减历史/重复参考；不能把一个JSON机械切块直接发送。
完整请求可能包含私密上下文，**不上传GitHub、不贴进聊天、不放入发行包**；报告只记录路径/体积/哈希。

### 将来修复后关闭

不会因版本叫 **1.7.1** 就自动关闭。用户确认桌面修复后，可记录简短依据：

```bash
python 01-skills/ppt-beautify-studio/scripts/studio_settings.py set \
  --ifapi-guard off --fix-evidence "用户确认某版本已修复，含日期/测试摘要" --confirmed
```

需要恢复时使用 `--ifapi-guard on --confirmed`。升级包不会覆盖已经保存的个人选择。

## 材质对话框与可编辑性

超高/高使用真实生图的无字面板（原生 imagegen、IF API 或relay，依当前设置），把原文独立排进去。
默认不额外叠原生灰白层/高光，避免洗掉生成材质。中/低默认不用这种面板。
新布局需填写：

```json
{
  "studio_profile": {"tier": "high", "backend": "native"},
  "aspect": "16:9",
  "slides": [{"elements": [{
    "type": "panel", "id": "story-card", "x": 1, "y": 2, "w": 8, "h": 2,
    "material_source": "generated", "texture": "../ornaments/generated/panel.png",
    "text": "原生可编辑正文", "size": 24
  }]}]
}
```

缺少真实面板文件会报错，不自动补一个普通矩形。`material_source` 字段只能声明来源，真实来源还须生成日志验证。
复杂纹理不是原生矢量，面板整体可移动/替换，不承诺内部纹路可逐笔编辑；正文始终原生。
如果用户选择原图与场景一体化背景，先披露合并主体不能独立拖动，原图仍保存。

## 项目素材结构

每次任务在原文件旁创建 `<文件名>_beautify/`，图片、字体与工作文件不进入本代码仓库：

```text
extracted/                 原文、原图、OOXML和证据
backgrounds/generated/     生图背景
backgrounds/derived/       融合、透明度与调色副本
foregrounds/              原始前景、抠图、派生图
ornaments/                边框、主题图标、生图面板
fonts/                    下载字体、许可证与样张
downloads/                外部图片及参考副本
prompts/                  提示词
layouts/                  整套设计合同与分版本布局
previews/                 实际渲染与视觉检查
output/                   最终PPTX
logs/                     生成、预检、检查与续作记录
```

## 仓库结构

```text
README.md
AGENTS.md                 代理维护规则
CHANGELOG.md              更新记录
requirements.txt
.gitignore
VERSION
01-skills/ppt-beautify-studio/
  SKILL.md
  agents/openai.yaml
  config/defaults.json
  references/             按模式与能力逐步加载
  scripts/                本地提取、组合、渲染、设置、预检等工具
  subskills/ui-ux-design/  内置共享设计、动画、着色器与3D方法库
04-tests/test_studio.py       离线回归，不触发服务调用或修改真实偏好
03-examples/                 不含密钥/真实素材的协议样例
02-docs/                     发布说明与版本审查
05-tools/check_repository.py  文档、版本、语法与目录检查
```

核心脚本还包括 `extract_pptx.py`、`extract_pdf.py`、`compose_slide.py`、`check_layout.py`、`render_preview.py`、
`blend_image.py`、`init_workspace.py`、`font_assets.py`、`review_proxy.py`、`save_checkpoint.py`。
只运行某步骤时使用其 `--help`，不要把抽取JSON直接当成布局JSON。

## 测试与已知边界

- 离线测试覆盖：原生默认/持久配置、真实body字节/哈希、63MB拒绝样本、估计不误放行、修复证据门、
  生图面板合同、原生文字保留、旧版兼容、渐变与连接线。
- 离线测试用临时合成素材，不表示已调用原生、IF API 或relay生图；没有偷偷安装字体或写用户服务配置。
- 真实PPTX视觉仍需要本机Office渲染器以及代理逐页看图。脚本检查不是美学评分，也不能自动证明所有事实保真。
- 原生imagegen、IFAPI最终body捕获、自定义relay真实连接分别依赖宿主能力，不因本项目存在就自动可用。
- `material_patch.py` 保留为旧稿兼容/明确要求的背景模糊工具，不再是新高档材质面板的替代方案。


## 维护与许可

目录导航：[技能](01-skills/README.md) · [示例](03-examples/README.md) · [测试](04-tests/README.md) · [文档](02-docs/README.md) · [维护工具](05-tools/README.md)。
项目顶层目录按数字排序，每个维护目录提供 README；技能包内部标准目录保持原名。
代理维护规则见 [AGENTS.md](AGENTS.md)，发布和同步步骤见 [RELEASING](02-docs/RELEASING.md)。

仓库：[guangyu17/PPT-Beautify-Assist](https://github.com/guangyu17/PPT-Beautify-Assist)。
本仓库采用 [MIT License](LICENSE)。外部技能、字体、图像及其服务条款各自独立，不随本仓库许可自动授权。
