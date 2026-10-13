# 版式、字号、配色与对比度

目录：网格 · 字号阶梯 · 配色 · 对比度 · 图片 · 版式 JSON（compose_slide / check_layout 输入）

## 网格（16:9，13.333 × 7.5 in）

- 安全边距：左右 0.6–0.8 in，上下 0.45–0.6 in
- 12 栏网格，栏间距约 0.25 in；常用分栏：12（通栏）、6+6、5+7、4+8、4+4+4
- 标题带：y ≈ 0.45–1.35 in；正文区从 y ≈ 1.6 in 开始
- 同一套 PPT 的标题位置、页边距、页码位置保持一致
- 4:3（10 × 7.5 in）同比例缩窄，栏数可降到 8

## 字号阶梯（16:9）

| 角色 | 字号 | 备注 |
|---|---|---|
| 封面主标题 | 40–54pt | 可加粗 |
| 页标题 | 32–44pt | 一套内固定一个值 |
| 副标题 / 小节 | 20–28pt | |
| 正文 / 要点 | 14–20pt | 一套内固定 1–2 个值 |
| 图注 / 注释 / 来源 | ≥10pt | 低于 10pt 视为错误 |

- 行距 1.1–1.3；段后 4–10pt
- 中文用无衬线（微软雅黑 / 等线 / 思源黑体），英文和数字可配 Segoe UI / Arial / Calibri
- 原 PPT 有颜色或加粗强调的词，新版里同样要突出（换成新配色）
- 溢出顺序：先调版式（加宽 / 分栏 / 缩图）→ 再把正文降 1–2pt（不低于 14pt，注释不低于 10pt）→ 仍放不下就告诉用户建议拆页。**不删原文。**

## 配色

- 每套 1 主色 + 1 辅色 + 1 点缀色 + 中性色（深色字 / 浅色底）
- 点缀色只用于强调词、数字、小图标，面积 < 10%
- 图表系列色按主色 → 辅色 → 点缀色 → 中性色依次取
- 深色背景配浅色字（#FFFFFF / #F5F7FA），浅色背景配深色字（#1F2937 / #111827），避免纯黑纯白大面积对撞时可略调灰

## 对比度

按 WCAG 相对亮度对比度，以文字框下方背景的「最不利区域」计算（`check_layout.py` 对文字区采样并取对比度的第 10 百分位；只是背景层近似，有前景叠层时必须看实际渲染）：

- 普通文字（<18pt，或 <14pt 加粗）：≥ 4.5:1
- 大字（≥18pt，或 ≥14pt 加粗）：≥ 3:1

不达标时：换字色 → 在文字下加半透明色块（透明度 15–35%）→ 重新生成该区域更干净的背景。

## 图片

- 保持原始宽高比，用裁切（`fit: cover`）或留白（`fit: contain`），不要拉伸
- 显示尺寸下有效分辨率 ≥ 150 dpi；不够时缩小显示尺寸，或说明来源分辨率不足
- 可加圆角（`radius`）、柔和阴影（`shadow`），同一套保持一致

## 可换色背景与独立花纹层

具体选择流程见 [背景定制](background-design.md)。原生 `background_color` 可精确改纯色；
独立透明装饰用已有 `image` 元素即可，无需新渲染脚本。元素按数组顺序从底到顶绘制：
底色 → 装饰图片 → 原生正文/内容图片。不要同时放一张不透明全页背景遮住可换底色。
完整边框需匹配画布，避免 cover 裁掉边线；透明度、边框净空和叠层对比必须实际渲染检查。

```json
{
  "aspect": "16:9",
  "slides": [{
    "background_color": "#11243A",
    "elements": [
      {"id": "ornament", "type": "image", "path": "backgrounds/frame-s01.png",
       "x": 0, "y": 0, "w": 13.333, "h": 7.5, "fit": "contain",
       "allow_overlap_with": ["title"]},
      {"id": "title", "type": "text", "text": "原有标题", "role": "title",
       "x": 0.8, "y": 0.6, "w": 11.7, "h": 0.9, "size": 36, "color": "#FFFFFF"}
    ]
  }]
}
```

示例的 frame-s01.png 必须是真正透明、已经检查过的资产；此处路径不是随包附带的成品。
简约风省略 ornament 元素，并取消相应 生图通道 请求。图片内部花纹不是原生矢量路径，交付需如实说明。

## 版式 JSON

`compose_slide.py` 把「背景图 + 版式 JSON」生成为可编辑 pptx；`check_layout.py` 读同一个 JSON 做质检。字段都可省略的写在括号里。

```json
{
  "slide_size": {"width": 13.333, "height": 7.5},
  "units": "in",
  "canvas": {"width": 1920, "height": 1080},
  "defaults": {"font": "Microsoft YaHei", "latin_font": "Segoe UI", "color": "#1F2937", "size": 18},
  "slides": [
    {
      "id": "s01",
      "background": "backgrounds/s01.png",
      "background_fit": "cover",
      "background_color": "#FFFFFF",
      "notes": "演讲者备注（可省略）",
      "elements": [
        {"type": "text", "role": "title", "x": 0.7, "y": 0.5, "w": 11.9, "h": 0.9,
         "text": "页标题", "size": 36, "bold": true, "color": "#FFFFFF", "align": "left", "valign": "middle"},
        {"type": "text", "role": "body", "x": 0.7, "y": 1.7, "w": 6.2, "h": 4.8,
         "paragraphs": [
           {"runs": [{"text": "要点一，"}, {"text": "强调词", "bold": true, "color": "#00D2D3"}], "bullet": true},
           {"text": "二级要点", "level": 1, "bullet": true, "size": 16}
         ],
         "line_spacing": 1.2, "space_after": 6, "fill": "#0B1026", "fill_alpha": 0.25},
        {"type": "image", "path": "extracted/media/s01_img1.png", "x": 7.3, "y": 1.7, "w": 5.3, "h": 4.8,
         "fit": "cover", "radius": 0.12, "shadow": true},
        {"type": "shape", "shape": "rounded_rect", "x": 0.7, "y": 6.6, "w": 2, "h": 0.06, "fill": "#00D2D3", "alpha": 1},
        {"type": "table", "x": 0.7, "y": 1.7, "w": 8, "h": 3, "rows": [["指标", "数值"], ["A", "12"]],
         "header": true, "size": 14, "header_fill": "#1E3A5F", "header_color": "#FFFFFF", "fill": "#FFFFFF", "color": "#1F2937"},
        {"type": "chart", "chart_type": "column", "x": 7, "y": 1.7, "w": 5.6, "h": 4,
         "categories": ["Q1", "Q2"], "series": [{"name": "收入", "values": [10, 14]}], "colors": ["#2BA3B5"], "legend": true, "size": 12}
      ]
    }
  ]
}
```

要点：

- `units`：`in`（默认）、`pt`、`px`（需 `canvas`，模式 2 直接用原图像素坐标最方便）
- `slide_size` 单位永远是英寸；也可写 `"aspect": "16:9" | "4:3"`
- 路径可写绝对路径，或相对版式 JSON 所在目录
- 文本：`text` 简写或 `paragraphs`/`runs`；`font`、`latin_font`、`size`、`bold`、`italic`、`underline`、`color` 可在元素、段落、run 三级覆盖；`align`：left/center/right/justify；`valign`：top/middle/bottom；`margin`（in，默认 0.05）；`wrap`（默认 true）；`autofit: "shrink"` 会按估算缩小字号但不低于 `min_size`（默认 10）
- 图片：`fit` = cover（裁切填满，默认）/ contain（等比放入）/ stretch（禁用于成品）；`radius` 为圆角半径（in）；`shadow`: true；`border`: {"color","width_pt"}
- 形状：`shape` = rect / rounded_rect / ellipse / diamond / star4 / star8 / snip_round_rect / snip_diag_rect / round_diag_rect；`fill`、`alpha`（0–1）、`line`: {"color","width_pt"}
- 图表：`chart_type` = column / bar / line / pie / doughnut / area / stacked_column / stacked_bar
- `role` 只用于质检（title / subtitle / body / caption / note / decor），不自动豁免任何文字；有意叠层用每个元素的 `allow_overlap_with: ["另一个元素id"]` 明确标注

## 实际运行与限制

使用 `load_workspace_dependencies` 找到自带 Python（包含 python-pptx、Pillow、numpy、pdfplumber、pypdf、pypdfium2），
不要假定系统 `python` 有依赖，也不要修改全局 Python。需要时所有命令中的 python 换成那个绝对路径。
图像服务不在脚本里直接请求，始终由 生图通道 工具调用；PDFium 是已有渲染库，不需要安装 PyMuPDF。

- `extract_pptx.py source.pptx -o extracted/deck.json [--media DIR] [--ppt-master ABS_DIR]`
  自动复用 ppt-master 守卫、intake 与 identity，原文件只读。抽取结果不是 compose 输入。
- `extract_pdf.py source.pdf -o extracted/pdf.json [--pages DIR] [--media DIR] [--dpi 200]`
  输出带文字层/图像证据及 needs_ocr 标志；PDF图像清单与位置信息需人工匹配。
- `compose_slide.py layout.json -o output/new.pptx`：默认不覆盖。仅重新构建自己的旧生成结果时可
  `--replace-generated`，绝不能针对用户原件；也支持 `notes`、图片圆角/阴影、原生表格和常用分类图表。
- `check_layout.py layout.json [-o report.json] [--pptx output.pptx] [--source-pptx source.pptx]`
  退出 1 表示发现错误，0 只表示未检出错误，**不是视觉质检合格**。表格/图表文字、母版与特殊字体需人工渲染核对。
  同源精确比较针对段落/单元格/类别/序列名和数值，调整段落拆分也可能报警，须逐字查证，不能盲目忽略。
- `render_preview.py deck.pptx -o previews/run-01 [--engine auto|powerpoint|libreoffice] [--soffice ABS_EXE] [--dpi 144]`
  用真实 Office 转 PDF 后由 PDFium 生成逐页 PNG、contact-sheet.png 和 render-report.json。
  支持直接输入 PDF。`--probe` 不启动软件；PowerPoint 在 Windows 用只读 COM，LibreOffice 用隔离配置。
  已有预览目录会拒绝重用，避免旧页混入；第二遍用 run-02。不使用 PPT 假渲染器。

原生组合目前不支持任意 SmartArt、复杂多轴图、动画与任意 SVG 内部语义还原；如遇到，读取保存的
OOXML/工作簿与源渲染，使用 ppt-master 的相应成熟能力或向用户解释缺口，不降级后假称“全可编辑”。
JSON 示例仅演示各对象字段，它们的坐标有意共用，不是一张可直接交付的无重叠页面。


## 打包版依赖

本技能可单独打包，但不附带或复制 ppt-master、ifapi-image、visualize、图像服务凭据或 Office。
安装在 skills/ppt-beautify-studio 后，抽取 PPTX 默认查找相邻 skills/ppt-master；安装位置不同时
通过 `--ppt-master` 传入正确绝对路径。运行需要 Python 依赖及可用的 LibreOffice/PowerPoint，
图像生成需要已连接的 生图通道。库和渲染器按“实际运行与限制”检测，不把创建时的本机路径当作其他机器配置。


## 视觉自检与透明度修复

每个生成/修改版本执行 [视觉自检闭环](visual-review-loop.md)。先看实际渲染中边框的内开口，
不能拿透明图片的外接矩形当成可用内容区。框与字挤在一起时优先调框、留白和层级，原文不能删。
`fill_alpha`/形状 `alpha` 是不透明度（0透明、1不透明），不是透明百分比；当前图片不支持 `opacity`。
图片透明度须处理原始 RGBA 的派生 PNG，或通过底色/原生遮罩调整实际视觉层次，不能只改预览 CSS。
可见图案实际位于文字下方时，重叠豁免不得代替清除干扰和再看图；脚本仍只能给出部分几何/估算证据。


## 融合 PNG、字体与素材路径（v1.3）

- 图片方框明显或人物需要独立移动：按 [图片融合](image-blending.md) 区分语义抠图、场景延展、纯 alpha 渐隐。
  `blend_image.py` 支持多边渐隐和已验证同画布蒙版，不执行语义人物检测；输出 PNG 和派生参数清单。
- 透明全页背景与原生底色组合时，背景对比采样会按 alpha 合成，不把透明像素的隐藏 RGB 误当底色。
  普通 foreground image 的复杂叠层仍须实际渲染检查。
- 字体按 [字体方向](font-direction.md) 给标题/正文分别配置；安装会影响用户环境，font_assets.py 默认为
  dry-run，授权后才 --apply。实际 glyph 覆盖与 Office 渲染另检查，不能承诺字体自动随 PPT 嵌入。
- 项目资产路径按 [统一工作区](asset-workspace.md)，新版增添 init_workspace.py、blend_image.py、font_assets.py，
  复用现有 Pillow/numpy，不另造人物分割模型、字体解析器或图像服务客户端。


## v1.4 全套风格与多层渐变

先按 [设计合同](deck-style-contract.md) 确认所有页的有限版式家族，不把字体/底色变化当作逐页独立风格。
blend_image.py 新增 `--recipe`，可执行多层 RGBA source-over、角度渐变、多节点、曲线与 gamma，
并导出独立处理层，详见 [配方协议](layer-recipes.md)。它不改变原 compose 图片的透明度字段边界：
图片透明效果仍通过真实 PNG alpha 表达，不能凭空添加 `opacity` 字段到 compose JSON。
单层纯色精确可改时优先原生形状；多节点斜向雾层则用配方 PNG，作为独立图片仍可移动/替换。


## v1.5 检查与会话载荷

真实渲染不降低质量，但送入对话的检查图使用 review_proxy.py；看不清细字时裁原图局部，不反复上传高清整页。
检查工具只报告本地字节预算，不知道完整会话的真实请求体。save_checkpoint.py 保存小型路径/哈希断点。
两种413分别按 [载荷控制](payload-budget.md) 恢复；不得把已完成的生图重复收费重跑。


## v1.6 组件与材质

原生panel/frame/connector/icon_badge/timeline语法与单位见 [组件JSON](component-schema.md)。
compose与lint共用layout_components展开逻辑，避免只在预览有效果却没进实际PPTX。
material_patch.py只用无字背景生成局部磨砂取样，取样失效需重做；正文必须原生。
语义选型与生图通道材质/图标prompt见 [组件设计](semantic-components.md)。画完背景而未处理这些语义结构不算设计完工。


## v1.7 覆盖规则

档位与通道以 [四档](beautify-tiers.md) / [通道](image-backends.md) 为准；取消历史小图/固定批量规则。旧material_patch示例仅兼容旧稿，新设计材质对话框必须真实生图且添加studio_profile。
