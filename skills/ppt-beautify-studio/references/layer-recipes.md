# 可重放的多层透明度与角度渐变

允许主代理在多次视觉修复中增加/删去/重排透明图层，分别调 opacity、渐变方向、节点和曲线。
每版保存新 JSON，重放源资产＋完整配方；不是对上次合成图反复不可逆地乘 alpha。
若有意把上一轮 AI 图作为下一轮编辑参考，另存版本链与原图锚点并复核漂移；仍共享资产累计调用预算。

## 支持能力与坐标

`blend_image.py --recipe ... -o ...png`：读取从底到顶的 `layers`，每层为 image 或 color，
用 source-over 合成。输出整张背景、每个处理后的独立 RGBA 层与 .asset.json 哈希/参数清单。
可以将独立层作为 compose_slide 的全页 image 逐层回填，保持可移动/替换；只需合并背景且用户同意时才用合成 PNG。
正文永远由 compose_slide 原生生成，不能放进栅格配方。

- 每层 `opacity` 0–1（不透明度），`brightness`/`saturation` 0–2；同一层多个 gradients 蒙版相乘。
- 不同层是 source-over（上层覆盖下层），**不是**把所有层 opacity 简单相加。两个 .5 白雾层叠加总体 .75，
  不是 .5 或1。迭代要看最终对比，避免不知不觉把主图洗白。
- `angle` 为渐变从起点到终点的方向：0°左→右，90°上→下，180°右→左，270°下→上。
  斜向按实际像素空间投影并以四角最小/最大值归一到0–1，不按视觉猜度数。
  这不是图片旋转；需要图形旋转时在 compose 图片的 rotation 修改，并检查四角裁切/注册。
- `stops` 为严格递增的 `[位置0..1, alpha0..1]`；允许从0升到1再降到0。
  渐变宽度/速率由节点间距决定，越窄变化越快。端点之外延用最近端点的 alpha。
- `curve`：linear、smoothstep、smootherstep；`gamma` 默认1，作用于每段曲线插值进度，>1延后变化，<1提前变化。
  边界缓不缓、变化早不早和最终不透明度是不同参数，不要统称“透明一点”。
- 可选 mask 为同像素画布的已验证黑白蒙版；原 alpha 会被保留并相乘，不能把 alpha 已经为0的像素凭空恢复。
- image 路径相对 recipe JSON 或绝对路径。所有图片/蒙版必须与 canvas 同尺寸；脚本拒绝隐式缩放/裁切。
  如需先对齐，保留原件另存注册副本并记录变换。单配方最多16层、单层最多8个渐变，避免无意义叠层。

## 示例：主图＋斜向文字雾层＋底部渐隐

下例是假定图像已经校准到1600×900的本地处理示例，不是向 生图通道 申请1600×900。

```json
{
  "canvas": {"width": 1600, "height": 900},
  "layers": [
    {"id": "base", "type": "color", "color": "#F5F7F8"},
    {"id": "integrated-scene", "type": "image", "path": "../backgrounds/generated/scene-registered.png",
     "opacity": 1.0, "brightness": 1.02, "saturation": 0.85},
    {"id": "reading-mist", "type": "color", "color": "#F5F7F8", "opacity": 0.72,
     "gradients": [{"angle": 350, "stops": [[0, 0], [0.44, 0], [0.62, 1], [1, 1]],
                    "curve": "smootherstep", "gamma": 1.2}]},
    {"id": "bottom-mist", "type": "color", "color": "#F5F7F8", "opacity": 0.38,
     "gradients": [{"angle": 90, "stops": [[0, 0], [0.76, 0], [1, 1]],
                    "curve": "smoothstep", "gamma": 1.0}]}
  ]
}
```

```text
python <SKILL_DIR>/scripts/blend_image.py --recipe <workspace>/layouts/background-stack-r01.json -o <workspace>/backgrounds/derived/background-stack-r01.png
```

产生 background-stack-r01-layers/layer-01.png 等同画布图层，按报告顺序放入实际 PPTX；
若底色需要原生可改，使用 background_color 并略去同色的不透明 base 图层，否则它会盖住原生底色。
修改时另存 r02 配方/输出：可以只改 reading-mist 的角度或 opacity，不需要重新调用 生图通道。
脚本不认识画面里的书/人物，主代理须避免雾层遮住主体；必要时增加已验证蒙版或调整图层范围。

## 迭代规则

先指出具体问题→只改相关层/1–2个参数→重建 PNG 层/实际 PPTX→真实渲染→看图对照。
允许反复叠加，但每层要有明确目的；没解决问题不要机械加白层。四轮本地修复/两轮停滞上限和
生图通道 最多三次重试仍按视觉自检执行；样张批准不意味着可无限改全局风格。
每版记录新增/删除层、角度、节点、gamma、不透明度和依赖哈希，保留可回退的最佳版本。
