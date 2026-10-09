# 无字背景、装饰和材质提示词

执行通道以 [生图通道](image-backends.md) 为准，默认native，不再固定所有工具参数到IFAPI。
先确认 [四档美化](beautify-tiers.md) 与 [全套设计](deck-style-contract.md)，按实际需要选下面模板。
需要人物/场景融合读 [图片融合](image-blending.md)；一体化书本/环境读 [史诗示例](epic-integrated-background.md)。

## 分批出图与负载控制

旧固定批量/等待/禁止4K规定已移除。按 [请求体预检](payload-budget.md) 在IFAPI桌面发送前测完整body，
超过本地字节预算才重建更小的独立请求；native默认无此门禁，relay按实际链路。工具枚举/能力与质量重试仍适用。
生成后核对真alpha/无字/风格，按可读性选择原图或检查副本；不自动把所有图压到低分辨率。

## 通用硬约束（拼进每一条提示词末尾）

```
No text of any kind: no letters, no Chinese characters, no numbers, no pseudo-text, no logos, no watermarks, no signatures, no UI labels.
Leave clean, low-contrast, uncluttered negative space for {留白说明}.
Presentation slide background, {比例} composition, crisp and professional at the explicitly requested pixel size; respect the chosen backend capabilities and requested resolution.
```

## 生成模板（模式 1 / 3）

```
A {风格方向} presentation background for a {主题} deck, {页面角色说明}.
Color palette: {主色}, {辅色}, {点缀色}; overall tone {明暗/冷暖}.
Visual elements: {背景元素}, placed mainly {元素位置}, subtle and decorative.
{通用硬约束}
```

页面角色说明与留白建议：

| 角色 | 角色说明 | 留白 |
|---|---|---|
| 封面 | hero cover with a strong but restrained focal motif | 左侧或中部大面积标题区 |
| 目录 | calm agenda page | 左侧标题条 + 右侧列表区 |
| 章节页 | bold section divider, more color than content pages | 中部或左侧大标题区 |
| 内容页 | quiet content page, decoration only at edges or corners | 顶部标题带 + 中部大块正文 / 图片区 |
| 结尾页 | closing page echoing the cover motif | 中部致谢 / 联系信息区 |

## 按页内容与配图定制（模式 1 / 3，仅明确选择后）

```
Create a text-free slide background for a page about {本页视觉主题摘要}, role {页面角色}.
Use these cues from the supplied foreground images: {色调、质感、主体方向}; complement them without duplicating their subjects.
Keep this approved background family: {全套材质、色调、线条语言}.
Base color: {已选底色}; accent colors: {已选点缀色}.
This page's motif: {本页纹样}; border variant: {本页边框形态}; decoration intensity: {已选强度}.
Keep these normalized x/y/w/h zones quiet and free of decoration: {safe_zones}.
Place ornament only in {允许装饰的边缘与角落}, with lower density on text-heavy pages.
Do not reproduce source photos, people, logos, charts, labels or quotations in the background.
{通用硬约束}
```

### 独立花纹边框 / 角饰

```
Create one standalone ornamental {边框或角饰} layer for a presentation slide.
Match the approved {纹样家族、材质、配色}, with this page variation: {变化说明}.
Use a genuinely transparent background and transparent open center; keep all artwork within {边缘范围}.
Keep the title, body and foreground-picture safe zones completely clear: {safe_zones}.
Preserve the full frame and its aspect ratio; no cropped corners, no opaque center panel.
No text, letters, numbers, pseudo-text, logos, watermarks, charts or photographs.
Use the explicitly requested pixel size; respect the selected resolution and backend capabilities.
```

透明度是待检查的输出要求，不代表工具保证能生成 alpha。只在透明开口合格后当作独立装饰使用。
无独立编辑需求时可把纹样边框合并进本页无字背景请求，避免不必要的额外调用。

### 简约风覆盖模板

```
Create a minimal, text-free presentation background in {已选底色与轻微色调变化}.
Keep generous quiet space fitted to {safe_zones}; prioritize the existing text and foreground pictures.
No ornamental pattern, no decorative frame, no filigree, no embossed texture, no glow border,
no thematic illustration or repeated subject. At most a subtle flat color transition if approved.
{通用硬约束}
```

用户要求精确可改的纯色底时，直接用原生 `background_color`，不为纯色本身发送 IF API 请求；
需要微妙背景质感时再使用简约模板。简约不等于默认调用华丽模板后只降低透明度。

## 优化模板（模式 1，有可用旧背景）

参考图 = 原页渲染图。

```
Use the reference slide only for its layout and mood. Redraw it as a cleaner, more refined background in the style of {风格方向}.
Remove all text, logos, data charts and editable labels from the reference. In separate-layer mode remove the foreground photos and icons too. In user-approved integrated-visual mode retain only the explicitly approved source subject, integrating its lighting and surroundings while keeping all text zones clean.
{通用硬约束}
```

## 还原模板（模式 2）

参考图 = 原页图。目的是去字补底，不是重设计。

```
Edit the reference image: remove all text, numbers, logos, icons and foreground photos, and reconstruct the hidden background behind them so the surface is continuous.
Keep the original composition, colors, gradients, textures and lighting exactly; do not redesign, do not add new elements.
Output the same framing and aspect ratio as the reference.
No text of any kind, no pseudo-text, no watermarks.
```

前景图补全 / 透明底：

```
Edit the reference crop: isolate the {物体} on a fully transparent background (or plain #00FF00 if transparency is unsupported), complete any parts hidden by overlapping text, keep identical pose, colors and proportions. No text.
```

## 风格方向库

挑 2–3 个与内容相符的做预览，不要硬凑。可以按用户反馈微调（更冷、更简洁、更活泼）。

| 方向 | 适合 | 配色示例 | 背景元素 | 字体建议 |
|---|---|---|---|---|
| 学术简约 | 课程汇报、论文答辩 | 深海蓝 #1E3A5F / 雾白 #F5F7FA / 青 #2BA3B5 | 细几何线、淡网格、角落渐变 | 思源黑体 / 微软雅黑 + Segoe UI |
| 科技渐变 | AI、数据、产品发布 | 午夜蓝 #0B1026 / 电光紫 #6C5CE7 / 霓虹青 #00D2D3 | 柔光渐变、粒子、抽象网络 | 微软雅黑 + Montserrat/Arial |
| 商务稳重 | 汇报、提案、财务 | 藏青 #1F2A44 / 白 #FFFFFF / 金 #C9A227 | 大色块分割、细金线、轻纹理 | 思源黑体 + Calibri |
| 清新自然 | 教育、环保、生活方式 | 雾绿 #E8F1EA / 森绿 #2E7D5B / 暖杏 #F2C18D | 水彩叶片、柔和光斑、纸纹 | 思源宋体标题 + 思源黑体正文 |
| 杂志编辑 | 品牌、文化、设计 | 米白 #F4EFE6 / 墨黑 #1B1B1B / 砖红 #C0442E | 大留白、撕纸边、颗粒质感 | 思源宋体 + Georgia |
| 暖色活力 | 社团、活动、营销 | 珊瑚 #FF6F61 / 奶油 #FFF4E6 / 靛蓝 #3D348B | 圆形色块、波浪、轻插画 | 站酷/思源黑体 + Poppins/Arial |
| 暗色高级 | 发布会、作品集 | 炭黑 #121212 / 暖灰 #2A2A2A / 香槟 #D4B483 | 聚光灯、丝绸质感、微反光 | 思源黑体 Light + Helvetica/Arial |

字体以本机能用为准；Windows 稳妥中文字体：微软雅黑、等线、思源黑体 / Source Han Sans（若安装）。

## 数量、留痕与失败

按档位与独立资产统计预览/最终/复用量，不按页数强制每页出图。日志记录当前backend、实际模型与支持的参数、
原图/参考、prompt、结果路径/哈希、生成累计次数及人工检查。原生工具可能输出在其管理目录，需复制归档。
请求大小按 [发送前预检](payload-budget.md)，仅IFAPI桌面临时启用；未知body不冒充通过。
连接/权限/质量失败按实际原因处理，最多3次重试，不重新生成已接受资产。超时状态未知先核对。
