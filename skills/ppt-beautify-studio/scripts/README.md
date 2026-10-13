# 本地辅助脚本

| 类别 | 入口 |
|---|---|
| 配置和请求体 | `studio_settings.py`、`request_preflight.py` |
| 提取与工作区 | `extract_pptx.py`、`extract_pdf.py`、`init_workspace.py` |
| 布局与渲染 | `compose_slide.py`、`check_layout.py`、`render_preview.py` |
| 图像与素材 | `blend_image.py`、`font_assets.py`、`review_proxy.py`、`material_patch.py` |
| 恢复 | `save_checkpoint.py` |
| 内部模块 | `_common.py`、`layout_components.py` |

对命令行入口先运行 `python <脚本路径> --help`。提取 JSON 与布局 JSON 不可混用。
渲染依赖 Office/LibreOffice；联网下载与个人配置更新按用户任务授权执行。
输出写入用户项目工作区，不写回技能源目录。`material_patch.py` 用于兼容旧稿，不代替真实生成面板。
