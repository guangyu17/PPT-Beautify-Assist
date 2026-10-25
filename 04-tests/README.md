# 离线回归测试

从仓库根运行：

```bash
python -m unittest discover -s 04-tests -v
```

`test_studio.py` 使用临时素材与配置，覆盖通道设置、请求体大小与哈希、面板合同、原生文字、渐变、连接线和预览副本。
测试不联网、不写真实用户偏好、不证明实际生图质量或 PowerPoint 视觉效果。
`test_repository_skills.py` 用临时源码树运行真实仓库检查器，覆盖有效嵌套子技能和名称不匹配、缺描述、空正文、坏YAML四种拒绝情形。
依赖见 [requirements.txt](../requirements.txt)；仓库文档与版本检查见 [tools](../05-tools/README.md)。
