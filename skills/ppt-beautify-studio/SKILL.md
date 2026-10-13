---
name: ppt-beautify-studio
description: >
  美化 PPT、重新设计幻灯片、把图片/PDF 转为可编辑 PPT、按大纲做 PPT（商业汇报支持结论先行的故事线规划）、
  换背景及图文融合。支持四档美化、原生/IF API/自定义中转生图、先定整套风格再生成。
  不用于仅修改几个字、讲解 PPT 软件操作或与 PPT 无关的文章写作。
metadata:
  version: "1.8.0"
  short-description: 四档 PPT 美化、多生图通道与真实请求体预检
---

# PPT 美化修改专家

全套内容盘点 → 风格/档位确认 → 真实样张 → 素材与原生内容分层 → 真实渲染、自主修复 → 新 PPTX。
保留本目录为 SKILL_DIR。只按需加载参考，不修改其他技能、用户原件或无关设置。

## 入口：档位与生图通道

先用 `scripts/studio_settings.py show` 读取持久偏好，读 [生图通道](references/image-backends.md) 与
[四档美化](references/beautify-tiers.md)。**默认原生 imagegen**，不需要为了默认选择反复询问用户。
用户明确改用 IF API/relay、持久档位或告知修复情况时才保存偏好；CLI运行不等于允许改配置。
持久档位为空且本次未指定时，给超高/高/中/低四档简短说明并问一次，不能把“拉满”解释为无预算无限生图。

原生通道按 `$imagegen` 的内置工具路径；当前未提供该工具就报告不可用，不把 IF API 或需密钥的CLI叫原生。
IF API 读 `$ifapi-image`，模型保留 `gpt-image-2.5-sunburst`；relay读 `$relay-imagegen`，复用其现成脚本与私密配置。
禁止无授权跨服务切换、打印/打包密钥。各通道结果均归档到项目分类目录。

## 临时 IF API 请求体保护

先读 [请求体预检](references/payload-budget.md)。用户已报告单次63MB请求被拒；仅为IF API桌面链路启用临时门禁。
发送前运行 `request_preflight.py`：测量完整最终序列化body并保存大小/哈希，不以图片文件大小冒充完整请求体。
超预算则减少/重建请求再检查；仅有工具参数或部分资产时标 needs_capture，不能伪称已检查、继续自动发送。
本技能不截获隐藏桌面请求；无法拿到完整body则说明集成缺口，不偷偷切服务。
原生生图默认不套此IF API门禁；relay只有明确经IF API桌面时启用。旧每批2张、固定等待、禁4K、96KiB/768px检查上限撤销。
是否分批由独立资产/通道能力/测量结果决定；重试仍有界。1.7.1等版本号不会自动取消保护，须有实际修复确认后才关闭。

## 模式与全套设计

| 输入/意图 | 按需参考 |
|---|---|
| 可编辑PPT美化：原文/页数/顺序默认不变 | [模式1](references/mode-beautify.md) |
| PDF页面、截图、扁平PPT忠实还原 | [模式2](references/mode-image-to-pptx.md) |
| 大纲/Word/Markdown新建演示 | [模式3](references/mode-outline.md) |

商业汇报的模式3在确认页数结构前按 [故事线](references/storyline-pyramid.md) 规划结论标题与事实缺口；学术、叙事等场景仅在用户要求时应用这套框架，否则按用户材料和目标规划。
模式1仅在用户要求或明显缺结论标题时提一次可选诊断建议，同意前不改字；只换背景/配色且不动文字时不主动建议。模式2不用。

先判断扁平页与真实意图，不仅按扩展名。模式1/3必须按 [全套设计合同](references/deck-style-contract.md)
盘点全部页数与内容，确认网格/字体/配色/排版家族、档位及允许出图量，之后才做代表页。
只拿到部分截图不能声称全套已规划。模式2不擅自统一原稿风格或降低还原质量来省图。

## 预览与审批

在所选档位范围内提供2–3个方向，每方向封面＋复杂内容页真实样张（低档可无生图，仍是原生PPT实际渲染）。
背景/材质先按资产需不需要生成，不强制为纯色发请求。**样张展示后结束本轮并等用户明确选择，批准前不生成其余页。**
模式3先确认页数结构；偏好持久化不代替本次风格批准。低/中档可复用已有图片与纹饰，不牺牲原文与可编辑性。

## 分层能力（按触发读取）

- [背景与装饰](references/background-design.md)：底色/逐页定制/花纹强度；简约不强制加华丽装饰。
- [图文融合](references/image-blending.md)、[一体化场景](references/epic-integrated-background.md)：抠图/延展/渐隐；
  用户明确同意后可合并视觉主体与环境，先披露该主体不再独立编辑，所有文字仍原生。
- [多层配方](references/layer-recipes.md)：可回放的alpha、角度、节点与曲线；本地参数不是生图API字段。
- [语义组件](references/semantic-components.md)、[组件JSON](references/component-schema.md)：主题图标、框线、引导线、时间轴。
  **材质对话框/卡片必须是真实生图面板素材＋原生文字**，尤其超高/高；不以纯原生矩形或模糊取样偷换。
  中/低默认省略这种框，明确需要时也须真实生图。简单线/节点保持原生，不要求每根线生图。
- [字体](references/font-direction.md)：主题对应标题/正文角色，官方许可归档；实际安装先获明确同意。
- [布局](references/layout-typography.md)、[项目归档](references/asset-workspace.md)：全资产在原文件旁 `<文件名>_beautify/` 分类保存。

## 质量与恢复

所有素材无需要编辑的文字；正文、日期、数据不得让模型编造。新布局写入 studio_profile={tier,backend}，
组合器检查panel有真实图片路径，来源由生成日志核验；语义选择仍是代理责任，不是自动算法已实现的承诺。
按 [视觉闭环](references/visual-review-loop.md) 实际渲染/看图/修复；visualize用于对照不是检测器，
看不清时用原图局部，不能只看缩略图就判通过。按需做可读检查副本，不套原来固定小图阈值。
每资产最多3次重试、每页4轮本地修复、连续2轮无改善则解释问题；此质量/费用保护不是已撤销的请求大小限制。
保存短断点与累计次数，不清空聊天、不自动另开聊天、不重复生成状态unknown的请求。
交付新PPTX及真实预览，不能用整页含字截图假装可编辑；不足与未经验证的步骤如实说明。
