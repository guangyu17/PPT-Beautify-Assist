# 生图通道与持久选择（v1.7）

这是所有旧参考中“只用IF API”“固定模型/size/output_path”的上位替代规则。设计prompt可复用，执行字段按实际通道。
本技能不再限定供应商；未获用户明确修改时原生native默认，不为每次会话重复问服务选择。

## 持久化与优先级

任务中的明确临时选择 > 用户明确设置的持久偏好 > config/defaults.json（native、tier为空）。
项目恢复时优先保留已有backend/tier快照，若用户后来持久换通道，说明未完成素材将如何续作，不静默重跑旧资产。
偏好文件在 `$CODEX_HOME/ppt-beautify-studio/preferences.json`（未设CODEX_HOME则用户.codex），不在Git仓库内。
只存backend、tier、relay配置**路径**、IFAPI模型和门禁状态，不存密码/token/API key。
用户说“以后都用…/切换中转/改成…”才用set；仅“这次用…”只记录当前项目，不改持久偏好。
持久未指定档位时，新项目问一次四档；通道默认native不问。任何更换服务均不能自行解释成用户同意。

```text
python <SKILL_DIR>/scripts/studio_settings.py show
python <SKILL_DIR>/scripts/studio_settings.py set --backend native --confirmed
python <SKILL_DIR>/scripts/studio_settings.py set --backend ifapi --confirmed
python <SKILL_DIR>/scripts/studio_settings.py set --backend relay --relay-config <absolute-private-config.json> --confirmed
python <SKILL_DIR>/scripts/studio_settings.py set --tier high --confirmed
```

--confirmed是调用者记录明确用户指令，不是软件验证了人类批准；不能用这个开关伪造同意。
没有relay配置时读取relay技能约定的现有发现机制，不将密钥输入到此设置工具。

## native：默认原生 imagegen

完整读取宿主提供的 `$imagegen` SKILL.md，使用实际存在的内置 `image_gen` 工具。
不需要API密钥；不把 `mcp__ifapi_image.imagegen` 误当原生。当前会话没有内置工具时说明能力缺失，
不自动转CLI/IFAPI/relay，也不谎称原生已测试。用户明确选择其他后端后才换。
本地图片编辑按imagegen要求先让目标图可见，再编辑；不能凭文件路径臆造工具字段。
原生输出以工具实际返回为准，不承诺output_path；复制选定结果到项目素材目录，保持版本并更新引用。
多资产通常每个资产单独原生调用，这是imagegen本身的语义，不是旧IFAPI“每批2张”限制。
分辨率、透明背景及参数按工具真实能力/用户档位选择，不强制1K、不虚构model/seed/quality参数。
原生模式默认不适用临时IFAPI请求体门禁；仍尊重原生服务实际限制和成本，不等于无限大小/无限调用。
若聊天本身仍通过IFAPI桌面转发，即使图片用原生仍可能遇到会话413；识别实际失败链路，不把“native豁免”当已修好中转。

## ifapi：桌面图像连接

读 `$ifapi-image`；使用其图像工具，显式model=`gpt-image-2.5-sunburst`，
prompt、参考绝对路径、size和output_path只使用当前工具提供的字段。参考多少张、请求哪个尺寸按测量及实际枚举决定。
**调用前**按 [请求体预检](payload-budget.md) 验证同一次最终序列化请求体；工具参数中只有路径，
不是最终传输body。没有隐藏请求的抓取能力就标needs_capture并停，不用小图估计冒充通过。
工具还可能自动返回图片到会话；生成后下一次responses请求仍需重新测量，不能凭上一份pass复用到新历史。
该门禁不读取/修改IFAPI桌面配置、不实现旁路API；不猜端口、不探测用户localhost代理。

## relay：用户自选中转

读 `$relay-imagegen`，复用 `scripts/relay_imagegen.py`，不改现有脚本、不另造API客户端。
私有JSON格式/模型/endpoint由该技能负责。明确relay_config_path时加 --config，不打印其内容；
未指定时可用既有发现规则。来源不可用只报告，不自行更换中转或模型。
用户已要求所有素材统一归档，因此可以传明确输出路径/目录到当前项目；命令参数先读该脚本 --help。
把prompt放项目prompts/，最终图及non-secret sidecar归对应generated目录。
默认模型/size等按relay技能和用户请求，不能把IFAPI专用sunburst模型硬塞给relay；也不把它的CLI当原生。
relay默认没有IFAPI的临时63MB相关门禁；若用户明确此relay也走IFAPI桌面，则以transport=ifapi-desktop启用检查。
relay自身的请求大小/模型/分辨率限制仍然适用。

## 所有通道共同规则

无字背景/材质、原图保留、真实alpha检查、主题图标一致性、累计质量重试和真实渲染不变。
高档材质面板使用**当前选定的生图通道**生成；用户要求IFAPI专供而当前选native时按本次明确要求处理并记录，
不要悄悄多服务混用。每张日志记录backend、实际模型（工具未透露则unknown）、参数、输出与检查结论。
暂时不可用的服务不算执行成功；不存在的参数不能随prompt升级而虚构。
