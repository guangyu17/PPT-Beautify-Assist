# 图片融合：人物抠图、场景延展与 PNG 渐变透明

## 参考图的视觉拆解（观察，不声称掌握原作者源文件）

本次参考是浅色史诗叙事演示：封面左侧约三分之一为干净的白色/冷雾文字区；
右侧为雪山与两名旅人，山势、雪线和雾气向左渐隐。内容页右侧为高细节俯瞰地图，
左侧为标题与要点，地图边缘以云雾融入浅底。四周细线角饰统一画面。
核心不是整张照片降低透明度，而是**让文字侧渐隐，人物/地图主体保持清晰**。
截图无法证明原图 alpha、层级或字体来源；只能反推视觉配方，不能声称复原原始 prompt。
原截图里的标题、地图标签、图标文字须单独原生重建，不能让 生图通道 重新生成文字。

## 什么时候使用哪种处理

提取 PPT 原图并看实际裁切/背景：方形并不一定有问题，不能逢矩形就抠图。
记录每张关键图的角色（人物/产品/环境/地图/证据截图）、主体 bbox、原透明度、
硬边是否干扰、正文位置，再选方法，并在样张中确认。

| 图像角色 / 问题 | 优先处理 | 不应做的事 |
|---|---|---|
| 人物/产品主体，被矩形底限制 | 原有透明素材优先；生图通道 参考抠图或已有可靠蒙版，输出独立 RGBA | 羽化整个人使脸/手透明；抠掉衣服/毛发细节；臆造产品外观 |
| 山水/场景图右侧配文 | 保留主体的方向性 alpha 渐隐，搭配协调纯色底 | 全图统一半透明导致主体灰白、文字区仍有杂纹 |
| 原图太窄，需展开式场景 | 生图通道 从原图延展画布，补环境，不伸缩人物；之后本地渐隐 | 直接横向拉伸方图；把新增地形当成真实资料 |
| 地图/架构图/截图含事实 | 内容层保持完整可读；只处理外部空白边缘 | 生成模型重画标签、改边界、淡掉数值；把小字融没 |
| 原图本来适合独立图框 | 保留矩形或协调裁切 | 为追求“高级”盲目抠图或生成背景 |

模式 1/3 可主动推荐并按已确认方向执行。模式 2 仅还原原页已有的渐隐/透明效果，不擅自新增美化。
不确定是否可以改变人物/地图等关键信息时先询问。简约商务可用极轻的侧边渐隐，不自动增加雾气、花纹或史诗元素。

## 可反推的提示词模板

所有模板按 [生图通道](image-backends.md) 执行，默认native；只有ifapi使用sunburst模型并做临时请求体预检。尺寸/参考数量按能力和测量决定，累计质量重试不变。
文字位置用 safe_zones 描述，不输入整段正文。下面默认示例主视觉在右，可按实际布局左右翻转。

### A. 雪山史诗场景：视觉接近第一张参考（背景与人物可分层）

```
Text-free cinematic epic fantasy slide scene, icy mountain wilderness, desaturated slate-blue and silver-white palette.
Jagged snow peaks, layered ridgelines and a winding snowy path dominate the right two-thirds.
Two small travelers seen from behind, one carrying a pack and one in a long cloak, stand on the lower-right path;
keep their silhouettes and feet crisp, with plausible scale, pose and natural shadows.
Atmospheric perspective: distant mountains dissolve into soft cold mist toward the left.
Reserve the left 35–40% as quiet pale negative space for later editable text;
no peaks, people, sharp texture or hard rectangular seam in that area.
Rich detail only in the right scene, restrained contrast at the transition, editorial presentation composition.
No text, glyphs, lettering, numbers, labels, logos, signatures, watermarks, UI chrome or border.
Use the explicitly requested pixel size. Use only the actual backend-supported resolution selected for this task.
```

已有角色图时用 `referenced_image_paths` 传原角色/场景的合规缩小副本，并补：
“Preserve the provided subjects' identities, attire, pose and proportions; do not invent replacement people.”
需要人物独立移动时，另做抠图；用户明确选择一体化视觉背景则无需重复抠图，须披露主体不再独立移动。不要让人物同时出现在背景和前景造成双影。
此模板首先生成视觉场景，不保证真实透明；alpha 由后续确定性处理实现。

### B. 俯瞰史诗地图：视觉接近第二张参考

```
Text-free oblique aerial fantasy landscape illustration, rocky mountain ranges, snowy upper-right peaks,
valleys, rivers and small distant settlements, muted earth-green and stone-gray with cool silver mist.
Main illustrated terrain on the right 65–70% of the slide, high detail in the center-right, naturally irregular edges.
Terrain edges dissolve into pale mist toward the left and lower-left; reserve the left third as clean light space.
Do not create a rectangular map card. No captions, place names, symbols that resemble writing, markers with labels,
compass letters, legend, title, page numbers, watermark, UI or decorative frame.
Keep the illustrated landform clear where editable labels will be added later.
Use the requested pixel size; use the selected supported resolution.
```

只用于新建的虚构装饰地图或已授权的风格化重建；用户提供的实际地图/地理证据不可用该模板随意重画。
原标签、位置、关系从素材逐项提取，以原生文本/形状回填；看不清不猜。

### C. 原方形场景向文字侧展开（参考编辑）

```
Extend the provided scene into a wider presentation canvas, preserving the existing subject, face,
clothing, products and scene geometry exactly. Do not stretch the image or change the camera perspective.
Extend only the surrounding environment toward {left/right}, using coherent lighting and texture.
Reserve {safe_zones} as quiet negative space. Transition into {slide base color} with natural atmosphere,
without a visible rectangular boundary. Do not duplicate the subject; no text, labels, logos or new data.
```

延展后的新背景是 AI 重建，需要披露；不足的真实证据不能靠该模板补造。根据实际工具尺寸适配画布，
记录裁切/补边变换，不能让主体缩放漂移。只需羽化时不要额外调用延展。

### D. 保留人物的透明底抠图（参考编辑）

```
Isolate the exact subject from the reference on a genuinely transparent background.
Preserve identity, face, hair strands, clothing details, silhouette, hands, feet, colors and proportions.
Remove only the surrounding background. Keep the original canvas size and subject position for registration.
No extra person, object, text, white rectangle, checkerboard pattern or painted matte.
```

检查实际 alpha、发丝/鞋边、白边和主体身份；失败用已有可靠抠图/蒙版，不把白底或棋盘格当透明。
本技能的 `blend_image.py` 不是人物分割模型，不能宣称它会自动认人抠图。

## 真正的 PNG 渐变透明：确定性后处理

用 `blend_image.py`，原图另存，像素尺寸/位置保持不变，输出 RGBA PNG：

```text
python <SKILL_DIR>/scripts/blend_image.py <workspace>/backgrounds/generated/scene.png -o <workspace>/backgrounds/derived/scene-fade-r01.png --fade-left 0.15 0.60 --fade-bottom 0 0.10
```

`--fade-left 0.15 0.60` 表示原图左侧 x≤15% 全透明，15%–60% 平滑过渡，x≥60% 保留原 alpha；
`--fade-right/top/bottom` 从对应边缘向内计算。用三次平滑曲线避免直线灰带，多个方向的蒙版相乘。
这些只是起始参数，依据文字区、人物 bbox 与参考图调整；不是所有 PPT 一律 fade 到 60%。
`--opacity 0.8` 是整体不透明度，可另调；`--brightness`、`--saturation` 为 0–2 的可选系数，默认1。
`--mask` 接受与原图同尺寸的已验证黑白蒙版（黑删白留），不自动推断人物位置。
现有 alpha 与新渐隐相乘，不会把原来的透明区变实心。允许多层累计效果，但保存各层配方并从原始资产重放，不对上次导出图无记录地反复羽化。
斜向渐变、多节点渐变、不同层叠加见 [多层配方](layer-recipes.md)。

推荐层级：**原生可改底色 → 同画布场景渐隐 PNG → 完整人物抠图（如需）→ 边饰 → 原生标题/正文/标签**。
主体若处于渐隐区，移动渐隐带或加保持清晰的独立主体层；不能仅为了文字留白把人淡没。
照片需独立可移动时用 image 元素；全页渐隐图可用 background + background_color。
透明区必须显示选定底色而非黑色。`check_layout.py` 已按 alpha 与底色合成背景采样；
前景叠层仍需要真实渲染视觉检查，不能只靠数值估计。

## 视觉验收

至少看白/目标底色上的全页，以及人物边缘/渐隐接缝局部：无矩形硬边、无灰色光晕、无白边，
主体清晰不透明、文字区干净、标题没有压到山峰/地图细节；画面自然连贯但文字仍完全可编辑。
按照 [视觉自检闭环](visual-review-loop.md) 用实际 PPTX 渲染图和 visualize 比较，出问题先调本地渐隐，
只在构图/抠图质量确需改变时才重新调用 生图通道。


## 一体化视觉与整套规则

需要比局部羽化更强的场景改造时，可按 [旅行手札反推](epic-integrated-background.md) 把授权原图与环境
一起生成无字完整背景；这是默认独立图片原则的明确可选例外，生成前说明编辑性取舍。
整套风格必须先按 [设计合同](deck-style-contract.md) 确认；局部 angle/gamma/opacity 修复不能偷偷换画风。
