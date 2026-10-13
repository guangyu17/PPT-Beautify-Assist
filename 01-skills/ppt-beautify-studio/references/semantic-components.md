# 材质文本区、线框、引导线与主题图标

## 参考图的差异诊断

较好的参考图不是只有更复杂的背景：人物占据左侧主要视觉区，标题与正文有显著层级；
“想要/需要”各自对应灯笼与罗盘徽记，右上罗盘和城堡形成背景的延伸，底部时间轴放在浅透面板内。
第二张局部图显示同款圆环、细线/菱形端点、短分隔线；第三张用圆形/双线/异形框组织人物，
用主箭头和垂直分支表达不同关系。当前生成例偏“背景＋散放文字”：文字层级、图标对应和时间关系没有成体系。

从截图不能确认面板是真亚克力、真模糊、折射或单纯浅白蒙版；本技能提供相应视觉实现，不假称识别了原材质参数。
也不能把参考图新增的引语、说明、年号、方向字或因果箭头照抄进原稿：美化模式仅使用原有文字/数值/关系，
缺少对应语义时可以提出建议但不能自行编造。无证据的时间顺序不画因果箭头。

## 必须先规划组件，而不只规划背景

把组件设计纳入 layouts/deck-style.json 的统一风格：

- `component_theme`：线宽与色、框型/角饰家族、图标材质与视角、panel材质/不透明度、时间节点/箭头语言。
- 每页 `component_plan`：原文证据→需要读者理解的关系→组件类型→实际位置/留白→资产来源→编辑性。
- 对比/动机两段用两个语义图标＋原生标题/说明；时间变化用带节点的轴；人物接续/援助关系用引导线；
  引语可用独立浅透区，地图/导航主题可用小型罗盘，不能所有页面机械加同一图标。
- 有明确时间/关系却只是把年份或人物散排时，优先补结构，而非继续升级背景。没有时间序列就不加时间轴。
- 默认建议保持有限组件家族/页，装饰为信息服务，不变成拥挤网页仪表盘。简约风保留清楚的线与节点，
  不自动上厚玻璃、雕花或复杂UI。华丽程度限于用户批准范围。

组件计划在样张中用真实文字和图标展示；至少包含最复杂内容页，不只验证封面。
图标/材质参考需要 IF API 时与所有背景共享串行队列、重试预算与413规则。

## A. 材质文本区：生图材质＋原生文字

按 [四档规则](beautify-tiers.md)，撤销旧版原生半透明矩形/静态背景模糊作为精致对话框的默认。
超高/高若用对话框，一定先用 [选定生图通道](image-backends.md) 生成无字材质底板，叠独立原生文字；
中/低默认省略，明确需要也真实生成，不能为了节省或工具不可用偷换原生框。
在component_plan记录材质、比例、净空与复用范围；选定美学后各页用同族资产，少量比例变体，不每页重造。

```
Generate one premium text-free {frosted acrylic / etched glass / parchment} dialogue panel asset.
Match the approved deck theme: {palette, line language and material finish}.
Front-facing, correct panel proportions, refined thin rim and restrained highlights,
quiet low-contrast reading center with generous safe inset; genuinely transparent outside the silhouette.
No title, no letters, no pseudo-text, no labels, no watermark, no background landscape.
Text will be a separate native editable object in PowerPoint.
```

检查真alpha、透底、高光和可读性；生成物不是实时玻璃，不能声称支持动态折射。panel材质没到就暂停或经用户同意省略，
不能回退为普通原生半透明矩形。正文一律原生，不能让图像模型写在面板上。
material_patch.py保留为旧稿兼容/用户明确要求背景模糊时的本地工具，不作为v1.7生成面板的替代。
新布局写studio_profile和material_source=generated，真实纹理路径与日志一一对应；脚本字段不是来源真实性证明。

## B. 线框与引导线

- 原生 frame 支持矩形、圆角、圆环、切角/对角变化和双线；图片可独立加 ellipse 掩膜。
  原生异形框只是近似视觉家族，不等于参考图精确的内凹雕花边框；需要精确花纹时用批准的独立矢量/IF API无字边饰。
- 原生 connector 支持水平、竖直、斜向及折线、虚线/点线、起终箭头。线在内容对象下或独立留白通道中，
  避免穿过文字、人物脸和图标主体。端点不能只“差不多靠近”，真实渲染检查接触边界、间距与方向。
- 分支/因果关系必须来自资料；颜色可以区分代价/援助等已知关系，不能凭一个红色分支编造对立。
- 细线通常 .5–1.0pt，结构主线可稍重；不能细到当前输出分辨率看不清。统一颜色和端点样式，
  细菱形/星点可以用原生形状，复杂卷草花边由独立装饰图表达。
- 当前连接线按坐标放置，默认不自动粘连到其他形状；人物/框位置变化需重算线端点。
  lint可检直线穿过文本框；折线路径和箭头尖端仍须视觉检查，不自动把bbox重叠全部豁免。

## C. 主题语义图标，而非随机UI符号

先在原文找到概念，再映射图标。示例是建议不是必须：希望/照亮→灯笼；方向/自主选择→罗盘；
城邦/援助→城堡；记录/契约→手札。无法确定主题时使用简洁几何标记或不加图标，不要捏造含义。
同一概念跨页复用同一资产；姿态、线宽、颜色、阴影与光向统一，不混用填色卡通、写实照片和线性商务图标。

选择路径：用户已有图标→已获许可的同族图标/原生简单几何→IF API主题定制。不能用错误语义的现成图标填位置。
圆环和四向小菱形可以原生，内部灯笼等细节可以独立透明PNG。八角星能提示方向感，但不能假称精确复刻罗盘。
北字/方向字/图标说明始终原生；原文不存在的“北”、引语或新标签不能无授权添加。

选定通道的图标示例（可跨页复用，尺寸按小图可读性与工具实际能力）：

```
One isolated {lantern / compass rose / citadel / journal} icon symbolizing {verified page concept},
match the approved epic travel-atlas system: desaturated dark blue-gray fine engraved linework,
front-facing, coherent thin outlines, restrained ivory/amber accents, balanced centered silhouette.
No circular ring, no text, no letters, no direction labels, no numerals, no logo, no watermark.
Transparent background; leave clear padding around all edges. No surrounding landscape, no UI button.
```

环框由原生对象画，不能让每次图标都附带不同大小的环。检查真实透明、轮廓与小尺寸可读性，
失败不把白底当透明。整体页右上角的小罗盘是跨页定位装饰，可全套复用，不逐页重复请求。
项目归档使用 `ornaments/generated/icons/` 与 `ornaments/derived/icons/`，增加来源/语义/页号到总清单；
不要把用户截图裁出的文字图标带字当可编辑图标；从参考借鉴风格，不假称拥有可下载的原始图标资产。

## D. 时间轴

提供事件原文、原日期/年号，选择横向/纵向及 `sequence`（等间距顺序示意）或 `proportional`（按数值间隔）。
等间距不宣称真实时间比例；资料不足或仅有顺序时用sequence并说明，不能生成猜测年份。
日期、事件标签、说明都是原生文本，线与节点也是原生。必要时放在淡透材质区内，留足上下高度，
不要用IF API生成整张带日期的时间轴。节点太密则调整布局/分栏，不删字；更改页数仍需批准。

## 组件验收

逐项看：图标是否语义正确/跨页一致；环与图标有净空；线端点有意连接而非穿字；
时间顺序与数值准确；面板的明暗与透明对最终文字可读性有帮助；无假透明/重影字/拼接缝；
材质纹理不是正文，用户能独立编辑文字与线节点。遵守 [请求预检](payload-budget.md)，按实际可读性看整页/局部；不把磁盘图体积冒充完整IFAPI请求体。


**自动检查边界：** 若正文下方还有面板/纹理等先前视觉层，背景-only对比值只作为警告，不当成真正叠层对比结论；必须检查真实渲染。透明/框形bbox会产生预期重叠警告，保留报告，不能以无error假称全项视觉通过。
