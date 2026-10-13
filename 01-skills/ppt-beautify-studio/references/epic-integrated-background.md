# 示例反推：旅行手札融入史诗场景

## 可见变化与推断边界

用户对照图：原页白底、左侧独立旧书、右侧三段叙事；美化页将书变成环境中的主视觉，
增加桌面旧地图、书摞、灯笼暖光；远景雪山与右上城堡形成冷色大气层；中央/右侧大片雾白支撑文字；
外框、指南针、竖向节点使页面像同一本旅行图鉴。背景可以更夸张，但信息区更干净而非更拥挤。

以下 prompt、HEX、位置、透明度、角度均为视觉上合理的**复现起点**，不是识别到的真实生成参数。
无法由截图判断原作者模型、seed、步数、采样器、CFG、参考强度、实际图层数或字体名称，不编造这些值。
截图里还有新增说明句、书页插图等改动，并非全是背景美化；原页末尾“陆行暂停 下一次升格，寻找替代办法”
在美化参考中没有明显出现，不能因此在模式 1 默默删掉。只学习视觉语言，原文/事实逐字保留，新增文案需明确授权。
原图软件边栏、顶栏和窗口灰底是截图界面，不是 PPT 风格，送图前裁出真实页面。

## 两条路线，由用户选择

### A. 独立内容层（默认）

原书图保留为独立图片，只用 生图通道 生成协调的桌面/灯光/雪山环境；若先生成了含书的场景，
把环境中书的位置清空再回填独立书图，或将生成的书抠出与清底分层。避免原书和背景书重复。
字体、时间线、图标标签、页码仍原生对象。书的 identity/书页内容如果重要，不让模型重画。

### B. 原图＋环境一体化（用户选择后允许）

可以直接把原书/人物/插画参考连同环境一起编辑，生成**一整张无文字视觉背景**，光影和边缘自然融合。
也允许在后续几次编辑中继续改环境/雾层，但保持主体身份与构图，并记录上一轮与原图引用，不超重试预算。
用户说“连原图一起美化”“一张完整背景”即是此选择；只说“更高级”不代表同意失去对象独立编辑能力。

生成前用一句话说明：合并后的书/人物只能随整个背景移动、更换，不能再独立拖动；原图仍归档保留。
选择这条路线后，这是对“所有图片独立可编辑”的明确局部例外，不能同时声称整图内每个物体仍独立可编辑。
正文/数字/地图标签不合并，原生文字始终在最上方；Logo/产品证据/数据图表默认不参与生成改写。
用户既要融合又要独立编辑时选 A，或从整图再重建透明前景＋清底。不能通过隐藏原图副本假装最终对象仍可独立编辑。

## 场景与版式复现起点

- 构图：左下 5%–52% 宽度为书/地图/灯笼；顶部与右上为远山城堡；右側 60%–91% 宽度为三段正文。
- 标题留白：x=.06,y=.10,w=.42,h=.18；正文区：x=.61,y=.28,w=.30,h=.55；底部原有注释单独留位。
  这些坐标按当前页图裁切估计，需与实际原文布局校准，不能把小图比例当成精确定位。
- 底色候选 #F5F7F8，主文字 #132B35，山体 #758695，羊皮纸 #CEB992，暖光 #C89B59。
- 标题用书卷感宋/明体或合适的史诗展示字；正文用清晰宋体/黑体。英文辅助可用古典衬线；
  具体字体按已安装/授权字体选定，不能仅凭截图断言是哪款字体。
- 场景强度可高：有明显环境纵深、云雾、暖灯与冷山对比。高对比局限于主图，正文区保持高亮低纹理。
- 边框细灰蓝线与角饰，同一整套使用统一风格；节点/指南针能原生实现时保持原生，若作图则独立无字资产。

## 总体美化 prompt（交给主代理，不直接交给生图工具）

```
先读完全部幻灯片，核实总页数、原文、图片和逐页内容密度。为整套制定“冷雾史诗旅行图鉴”的
统一设计合同：字体角色、银白/灰蓝底色、羊皮纸与暖金点缀、细线边饰、固定标题/页脚位置和有限版式家族。
原页的左图右文信息关系可升级为“左侧环境主视觉＋右侧三节点叙事”，但不删改任何原文。
让用户确认全套方向和原图是否可合并到背景，随后仅生成代表页样张。
如选一体化，使用原书作为参考，让它与旧地图、灯笼、雪山/城堡环境自然融为一张无字背景；
如选分层，保留独立书图并生成匹配环境。所有可编辑文字、数值、标签独立回填。
允许多次迭代局部白雾层、斜向/竖向 alpha 渐变及亮度，使场景丰富而正文不受干扰。
用真实 PPTX 渲染检查原文完整、边框净空、字体与渐变叠层，并用 visualize 对照；只在本轮暂未见明显问题后交付。
```

## 生图通道 一体化编辑 prompt（必须无字）

```
Use the supplied open-book image as the visual reference for the main subject.
Create a lavish epic-fantasy travel-journal environment for a presentation background, silver-white mist,
desaturated blue-gray mountain scenery, warm aged parchment and a small amber lantern accent.
Keep the reference book recognizable: its open pose, binding, worn cover, page proportions and ribbon.
Place it naturally on an old map-covered desk across the lower-left half, with a few closed books and a small lantern;
coherent contact shadows and warm local illumination, not a pasted rectangular photograph.
Layer distant snowy ridges across the top and far background, with a small majestic citadel in the upper-right distance.
Use atmospheric depth and soft fog. The environment can be richly detailed and dramatic around the left subject and page edges.
Keep the upper-left title area and right-side three-paragraph content area pale, quiet and low-contrast:
{normalized safe_zones from the approved actual layout}.
Blend all scene edges into a cool near-white page field without hard rectangular seams.
Do not paint words, handwriting, book-page text, map labels, numerals, logos, watermarks, UI chrome or pseudo-text.
Do not render titles, timelines, labels, page numbers or captions. Those will be added as native editable objects later.
Preserve important source imagery; do not invent factual diagrams or alter evidence.
Use the explicitly requested image dimensions; use the selected supported resolution.
```

需要书页山峰/指南针插画时，只有原图本就包含或用户允许装饰性重画才加；否则保留原书空白/已知图案。
用户要求框也融在同一背景时可加“thin ornate gray-blue border strictly outside safe_zones”，
但独立边框更便于修复与统一全套；不要多次生成同一个已批准框。文字区保护可先在生成中提出，再本地精调 alpha。

## 实际工具参数与后处理参数分开

实际工具字段按 [通道](image-backends.md) 区分：native只用内置工具实际字段，不强传model/output_path；
ifapi用sunburst模型与工具支持尺寸；relay复用其私密配置。分辨率按档位/需求，不禁止4K，
但请求画幅不是成品画幅时要校准裁切/补边，不能损失正文和主体。IFAPI桌面仅在完整body测量通过后发送。
seed/steps/CFG等未暴露参数不伪造。

多层 opacity、gradient angle、gamma 等是 **本地 blend_image.py 参数，不是 生图通道 参数**。
示例起点：远景 opacity .35–.65、正文雾层 .55–.85、底部淡出 .2–.45、独立前景主体 .9–1.0；
某些方向层已烘焙进生成图时不要重复叠加。每层及最终叠加效果均须看图，不能机械套所有层。
具体可执行配方见 [多层透明度与角度渐变](layer-recipes.md)。
