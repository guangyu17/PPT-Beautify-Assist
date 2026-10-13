# 统一工作区与素材归档

首次处理文件时，以原文件所在目录为父目录建立 `<文件名>_beautify/`，所有生成/下载/派生资产都留在其中。
不覆盖、移动或删除用户原件；重跑复用同源工作区，不在源目录散落 png、字体、prompt、临时 PPT。

```text
<原文件所在目录>/<文件名>_beautify/
  extracted/                原始提取内容、源页与证据
  backgrounds/generated/    生图通道 场景/背景原始返回图
  backgrounds/derived/      渐变透明、调色、补边后的背景 PNG
  foregrounds/original/     保留原始分辨率的独立前景图
  foregrounds/cutouts/      抠图 RGBA 与已验证蒙版
  foregrounds/derived/      前景裁切与其他派生版本
  ornaments/generated/      生图通道 边框、角饰
  ornaments/derived/        校准尺寸、透明度调整后的装饰
  fonts/downloaded/         官方下载的 TTF/OTF
  fonts/licenses/           随附许可证及授权证据
  fonts/previews/            字体角色样张
  downloads/images/         外部原始图片
  downloads/references/     发送给 生图通道 的轻量参考副本
  prompts/                  每次生成/编辑提示词
  layouts/                  分版本版式 JSON
  previews/                 实际逐页渲染、拼图、复核图
  output/                   分版本最终 PPTX 及交付说明
  logs/                     生成队列、视觉检查、安装、资产清单
```

工作区初始化：

```text
python <SKILL_DIR>/scripts/init_workspace.py <source.pptx>
python <SKILL_DIR>/scripts/init_workspace.py --parent <selected-parent> --name <outline-title>
```

脚本校验源文件与已有项目的对应关系；不会吞并未登记目录。老版本工作区已经有资料时，先读清单后
在原工作区非破坏性地补充子目录与登记，或在相同父目录用新名字创建工作区；不能自动移动旧素材或清空目录。
多份输入以主要源文件所在目录为基准；父目录不可写就先说明并请用户指定位置，不偷偷改去 Temp。
剪贴板附件/临时下载只有 Temp 路径时，先把它当临时输入，使用当前任务持久工作目录或用户指定目录建项目，
说明位置；纯大纲同样使用指定目录或当前工作目录。上述例外不把项目长期保存在系统临时目录。

## 每次工具调用的落点

- 当前通道支持输出路径时指定项目分类绝对路径；原生工具不假定有output_path，先生成后复制工具实际返回文件到项目，采用 `sNN-purpose-rNN.png`。
  若工具实际返回到其他位置，核验文件后复制归档到工作区，记录真实返回路径与归档路径，不假称遵守了 output_path；
  后续 compose 只引用归档结果。不删除工具临时返回文件，也不覆盖同名资产。
- 发送参考图放 downloads/references；保存提示词到 prompts，队列状态到 logs/generation-log.json。
  全部资产共用可追溯日志；调度按通道支持、用户预算与请求实测决定，不因分类目录而重复生成。
- 本地派生保留源图；渐隐结果由 blend_image.py 同目录保存 .asset.json（来源、哈希、参数与画布）。
  字体由 font_assets.py 保存下载来源、许可证与校验值。外部图片也记录来源页、下载 URL、用途和许可情况。
- 总清单 logs/assets.json 记录相对路径、asset_id、类别、来源、原始/派生关系、页号、版本、SHA-256、生成次数；
  不记录 API 密钥。复用基于实际文件和参数，不仅凭文件名；关联源文件、字体或布局变更使视觉检查失效。
- 运行环境/Office/Python 本身不复制进项目；字体经明确同意安装到系统要求的当前用户字体目录是唯一必要副本，
  工程仍保存下载原件与安装记录。禁止把本次字体/图片或用户截图塞进全局 skill 包。配置偏好在CODEX_HOME专用目录，服务密钥由所选通道保管，项目只引用配置路径。

## 旧版日志与路径兼容

新项目生成日志用 logs/generation-log.json、视觉日志用 logs/visual-review.json。
继续旧项目时先检查 backgrounds/generation-log.json 和 previews/visual-review.json；保存它们，
在新日志记录迁移来源并延续 asset_id/累计尝试次数，不能借换目录重置重试预算。
backgrounds/background-plan.json、fonts/font-plan.json 等设计计划留在对应分类；无需改动已工作的旧路径。
批次/修复输出另存新版本，不递归删除用户文件或其他对话素材。新交付仅包含实际使用且允许交付的资产，
字体许可禁止再分发时只给字体名称、来源和替代说明，不把受限字体直接打包。


## v1.4 设计合同与叠层版本

layouts/deck-style.json 保存全套风格/页数/逐页家族及真实审批状态；layouts/background-stack-rNN.json
保存每次多层参数。背景合成和自动导出的独立层放 backgrounds/derived/，不要仅保存最终合成丢掉层。
一体化生成的原图来源、授权合并范围、可编辑性取舍与原图锚点写入日志，旧原件保留。


## v1.5 低载荷检查与续作

previews/review-proxies/ 保存有限字节的检查JPEG及.review.json，原始高分辨率渲染仍保留，不替换成品资产。
logs/resume-state-rNN.json 与 logs/checkpoint-rNN.json 保存短状态和文件/哈希，不包含图片编码、全文或聊天历史。
具体工具与会话413恢复见 [载荷控制](payload-budget.md)。工具返回摘要只输出路径/计数，不递归打印素材目录。

## v1.6 组件资产

主题图标放ornaments/generated/icons与ornaments/derived/icons，磨砂取样及.material.json放ornaments/derived。组件计划属于整套合同与逐页布局，记录图标语义、许可/生成来源、底图/裁切依赖；新目录按需创建，原件不覆盖。
