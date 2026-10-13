# 原生组件 JSON 协议

这些是 `compose_slide.py` 和 `check_layout.py` 共同支持的新增字段，不是提示词伪参数。
`layout_components.py` 把组件展开成原生基础对象（面板/线/节点/文字/独立图片）；它不会自动理解语义，
原文、日期、关系和图标资产须由主代理依据材料确认。高阶组件中的坐标/宽高随顶层units转换，
padding/inset/node_radius始终英寸，字号/线宽始终pt；展开后统一英寸。

## v1.7 新项目profile与面板来源

所有新布局加入studio_profile={tier,backend}，四档与通道取值见 [四档协议](beautify-tiers.md)。
panel还须material_source=generated与真实texture文件；旧无profile样例仅为历史字段演示，不能直接用于新设计绕过门禁。
面板简单白层/模糊补丁不能冒充生图。下方原生highlight/line只做真实素材周围细节，不是主体质感来源。

## 面板与边框

```json
{
  "type": "panel", "id": "timeline-panel",
  "x": 4.1, "y": 5.3, "w": 8.2, "h": 1.55,
  "material": "acrylic", "shape": "rounded_rect",
  "fill": "#FFFFFF", "alpha": 0.3,
  "line_color": "#CBD6DF", "line_width_pt": 0.7,
  "inset": 0.035, "highlight_color": "#FFFFFF", "shadow": false,
  "padding": 0.18
}
```

`material`=translucent/acrylic；acrylic多一层原生内高光，不代表实时模糊/折射。
可加 `text` 或 `paragraphs`（同基础文本协议）、size/font/latin_font/color/valign；文字框自动按padding内缩。
v1.7的 `texture` 必须是实际生图材质PNG，先于surface放置；旧版的模糊取样只用于还原/兼容，不能替代新设计要求。纹理必须和面板几何对齐。
复杂时间轴可另放在panel之后，不必塞进panel.text。组件未自动豁免重叠，面板与文字属于有意叠层仍须确认。

```json
{"type":"frame","id":"portrait-frame","x":1,"y":2,"w":2.2,"h":2.2,
 "shape":"ellipse","double":true,"inset":0.05,"color":"#8F7A52","line_width_pt":0.8,"inner_width_pt":0.4}
```

panel/frame形状：rect、rounded_rect、ellipse、snip_round_rect、snip_diag_rect、round_diag_rect。
shape原语另支持diamond、star4、star8。image可用 `mask_shape: "ellipse"`，保持原比例以cover裁切进圆形，
并非把人物图整张拉伸变圆；圆框需物理宽高相等。

## 原生连接线

```json
{"type":"connector","id":"cause-link","x1":3.2,"y1":3.1,"x2":5.0,"y2":3.1,
 "route":"straight","line":{"color":"#254453","width_pt":0.8,"dash":"solid","alpha":0.85},
 "start_arrow":"none","end_arrow":"arrow"}
```

route=straight/elbow；dash=solid/dash/dot/dashDot/longDash；arrow=none/triangle/stealth/diamond/oval/arrow。
水平/竖直线宽或高为0是合法的，端点重合不合法。适用从右到左、从下到上，不能用负w/h的shape模拟。
图形移动后需手动/布局程序重算端点；当前不承诺自动粘连。端点与箭头tip视觉检查不能省略。

## 图标徽记

```json
{"type":"icon_badge","id":"need-symbol","x":4.5,"y":3.0,"w":0.8,"h":0.8,
 "symbol":"star8","color":"#203E4C","padding":0.16,"cardinal_marks":true}
```

简单symbol=star4/star8/diamond；复杂主题图标改用 `path` 指向核验过的无字透明图，path优先于symbol。
必须实际提供一个，不会生成空圈后声称有语义图标。circle需要等宽高，cardinal_marks生成四个小菱形。
圆环、图标及小菱形可独立编辑/替换。若要“北”等标签，须有内容/设计授权后另建原生文本框。

## 原生时间轴

```json
{"type":"timeline","id":"losses","x":4.5,"y":5.55,"w":7.3,"h":1.3,
 "orientation":"horizontal","spacing":"sequence","color":"#536D7B",
 "date_size":12,"label_size":17,"description_size":11,"node_radius":0.045,
 "events":[
   {"date":"1072","label":"触觉"},
   {"date":"1087","label":"视觉"},
   {"date":"1096","label":"听觉"},
   {"date":"1100","label":"独立自我"}
 ]}
```

示例事件来自本次用户参考图，仅演示字段，不是所有项目的默认内容。
orientation=horizontal/vertical；spacing=sequence/proportional。proportional需每事件提供数值time并严格递增，
脚本不自动排序、不补年份；date显示值可以另给原文。横轴可调label_width，事件description可选。
默认2–12个事件；拥挤/长文需扩大文字区或改布局，不为了兼容这个上限擅自删事件。
所有高阶对象展开后仍参与文字溢出/页边界/线穿文本检查；表格图表/曲折线与材质对比仍需真实渲染看图。

## 组合方式

先背景→可选模糊纹理＋panel→轴/连接线→节点/图标/图片框→原生文字；主代理也可调整层级但不能遮挡正文。
同一组件展开对象名为 `组件id-子对象名`，例如 losses-date0、losses-axis，方便定位。
有意重叠仅在真正看图后用具体 `allow_overlap_with` ID注明，不能泛化豁免整页。


默认关闭形状主题自带阴影，仅shadow=true时添加显式弱阴影，避免低alpha面板变灰。正文若未单独指定字体，继承整套defaults，不会强制回退为组件内硬编码字体。

生图面板默认alpha=0、无额外边线/内高光，以免原生灰白层覆盖精心生成的材质；仅明确填alpha/line/inset时添加局部辅助层。正文仍独立。
