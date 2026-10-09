# 临时IF API请求体预检（v1.7替代旧固定限制）

用户报告已查明：一次约63MB请求体超过IF API桌面当前单次上限。这里采纳为用户提供的现场诊断，
不是本技能测得的日志或官方发布值。**63MB被拒不证明“<=63MB全能通过”。**
默认以60,000,000字节（十进制60MB）作为留余量的本地发送预算，可由用户按真实限制调整；
不等同60MiB或已验证服务上限。原生native模式默认不套此IFAPI临时门禁。

## 已撤销

撤销每批2张、并发固定1、5/15/30/60秒固定等待、禁止4K、强制1536输出、参考图固定1–2张、
96KiB/768px检查图、256KiB视图等**技能硬限制**。按当前通道实际能力、档位、可读性和测量结果决策。
visualize 自身的资源/尺寸合同及底层工具枚举仍须遵守，不能由此版本绕过。
单资产最多3次质量重试/页面4轮局部修复等成本保护继续保留，不是请求大小限额。
view_image 先看原始或可读副本均可，避免不必要地打印base64/全套XML仍属良好工程习惯，但不再设固定4次检查额度。

## 每次发送前如何测

执行 `request_preflight.py`，仅检查本地文件，不重放POST、不调用服务、不读取密钥。
精确模式需要**最终序列化的HTTP请求体**，包括历史、图片编码、工具/系统信息和客户端封装。
它不是prompt长度、磁盘图片之和或一个只有路径的工具参数JSON。Multipart需连boundary等也保存为同一次真实body。

```text
python <SKILL_DIR>/scripts/request_preflight.py --backend ifapi --body <private-final-body.bin> --complete-body -o <workspace>/logs/preflight-r01.json
```

- pass（exit0）：按调用者声明为完整body，实际读取其字节流得到大小/哈希，未超当前预算。
  只能发送这份相同body；任何正文、历史、参考图、wrapper变化都要重新检查。脚本不负责发送，不可能拦截隐藏桌面请求。
- oversize（exit1）：已知部分或完整body超过预算；禁止原样发送，构造更小请求再验。
- needs_capture（exit2）：缺少完整body，只能估计或不可观测，**不能给假pass**。检查工具不能证明隐藏内容没有追加。
- exempt（exit0）：native默认/非IFAPI relay，或用户确认桌面已修复后关闭门禁；不代表后端没有自己的限制。

当前 IF API MCP 若只暴露prompt/reference_paths，而不暴露桌面最终 `/responses` body，
本技能无法在其内部自动前置hook，也不编造捕获API。会显示needs_capture并停止自动IFAPI发送，说明要么由
桌面/调用方提供受支持的实际body导出与发送前集成，要么用户明确选择原生/其他中转。
默认原生因此可正常走可用的原生工具；原生工具本会话未提供时也必须说明，不能自动换回IFAPI。
不要让用户把可能含私密上下文的body上传到聊天或GitHub；本地保存仅为短期检查，报告只留路径/大小/哈希。

## 估计模式：帮忙定位，不用于放行

```json
{
  "text_bytes": 4096,
  "known_overhead_bytes": 2048,
  "unknown_history": true,
  "assets": [{"path": "../downloads/references/ref.png", "encoding": "base64", "occurrences": 1}]
}
```

```text
python <SKILL_DIR>/scripts/request_preflight.py --backend ifapi --manifest <workspace>/logs/request-estimate.json
```

会精确读取列出文件的磁盘字节、按Base64长度近似和出现次数求已知体积；missing history照样可能更大。
估计小于预算仍是needs_capture，不声称核验完整请求；即便unknown_history=false也不能把估计升级成精确。
IFAPI专属guard按实际transport路由，可在relay明确使用IFAPI桌面时加 `--transport ifapi-desktop`。

## 超限时按实际贡献减少

1. 将独立资产/独立页面分成独立语义请求并重新序列化；不能把JSON或同一次消息硬切几段当“分批”。
2. 清理重复参考与无关大图，压缩副本或裁关键区域；必要时降图尺寸，保留原件/透明度，字节再测。
3. 如果大头是聊天历史，单纯分图片不够；保存批准状态、风格合同、文件路径与累计尝试数到断点。
   用户确认新建不继承原大图历史的会话后，仅用断点路径恢复，不擅自新建聊天/删除历史。
4. 确认服务端是否已生成，unknown请求先核对，不在新批次重复收费。预检报告不重置生成重试预算。
5. 请求已小却仍413/403，记录短错误和实际路由，停止盲目重发；普通403也可能是权限，不能全部归尺寸。

检查图 `review_proxy.py` 留作可选缩小工具：默认1600px/512KiB仅为工具默认，可由任务调整，已移除原来小尺寸硬上限。
其audit只评估所选本地文件，不代替request_preflight精确body检查。save_checkpoint.py仍保留短状态/文件哈希续作能力。

## 修复后取消临时门禁

不会在1.7.1或其他日期/版本号到达时自动关闭。收到用户明确确认供应商修复且提供简短依据后：

```text
python <SKILL_DIR>/scripts/studio_settings.py set --ifapi-guard off --fix-evidence "用户确认桌面修复，版本及日期说明" --confirmed
```

需要恢复时用 `--ifapi-guard on --confirmed`。偏好记录证据，保留历史报告，不擅自更改代理body limit。
更新版本时默认配置仍带门禁；已有用户明确关闭的偏好不被升级覆盖。
