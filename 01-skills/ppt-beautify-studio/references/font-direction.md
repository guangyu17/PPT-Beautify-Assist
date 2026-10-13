# 字体方向、下载与安装

## 先配字体角色，不是随机换字体

每套 PPT 规划中文标题、英文标题、正文、图注/数据四个角色；通常2个字体家族即可，
字体对比靠字形气质、字重和大小，不把整套变成字体样本册。
标题可以有表现力，正文必须易读。参考截图无法可靠确定原字体，不把猜测当识别结果。

| 主题 | 标题候选方向 | 正文方向 | 使用边界 |
|---|---|---|---|
| 史诗/故事/奇幻介绍 | 中文有书卷感的宋/明体，或少量书法展示字；英文可用 Cinzel 类古典衬线 | 易读宋体或黑体，保持笔画清晰 | 花体用于短标题，不能把地图标签和长段正文全改成花体 |
| 东方文化/历史叙事 | 楷体、宋体，或有授权的书写展示体 | 宋体/黑体 | 书法不等于大段正文适合手写，先看实际汉字 |
| 简约商务/学术 | 稳重黑体或清晰宋体，中粗标题 | 同方向的清晰正文或协调的第二家族 | 不自动加古典花体；用户说“正楷”时尊重其楷体偏好，不强行等同黑体 |
| 科技/数据产品 | 几何感无衬线，中英数字宽度协调 | 清晰无衬线，数字和单位完整 | 不用装饰字体替代数据标签 |
| 杂志/文化品牌 | 有性格衬线标题＋中性无衬线正文 | 克制正文 | 题材与原品牌优先，不用字体本身替代排版 |

候选来源可从 Adobe Source Han / Noto CJK、Google Fonts 官方仓库中的 Cinzel、Ma Shan Zheng 等开始。
这些是选型候选，不代表所有文件已安装、全汉字覆盖、可随意再分发或适合每个品牌。
Ma Shan Zheng 等书写字体仅在确实适合的短标题试用；简约商务若指定楷体，可以用本机可用的
楷体/KaiTi 作候选，但绝不能从 Windows 目录复制字体打包给别人。

## 工作顺序

1. `font_assets.py inventory` 列出本机系统/当前用户字体文件，再用 `inspect <font>` 读取实际 family/style。
   不以“存在类似文件名”就断言目标字体可用于当前 Office 进程。
2. 记录到 `fonts/font-plan.json`：每个角色的 family、style/weight、文件、来源、许可证、备选字体；
   用真实标题、代表性中文长句、数字和标点制作样张，检查是否缺字、乱码或字体替代。
3. 主题适合且已获选型批准的字体缺失时，从字体作者/Google Fonts/Adobe/Noto 官方页核验来源与许可，
   下载 raw TTF/OTF 和许可证到当前工作区，禁止不明 exe 安装器、盗版站、从系统字体库盗拷分发。
4. 安装会改变用户环境：先说明字体名称和用途并取得明确同意（已明确授权本次安装则不重复问）。
   仅安装当前用户，不请求管理员权限、不改已有同名字体。辅助脚本默认 dry-run，确认后才 `--apply`。
5. 关闭由本任务启动且已不需要的渲染进程，重新启动渲染器读取字体；不关闭用户正在编辑的 Office。
   在真实 PPTX 中设置字体，重新渲染查看，不把 Pillow 字体预览当成 Office 已使用该字体的证明。
6. 缺字或跨机器替代时换已确认的可用候选并重新渲染，不栅格化正文、不静默变成默认字体。
   本流程不承诺字体自动嵌入 PPTX；需要嵌入时核验字体嵌入标志/许可并使用已验证的 Office/已有成熟工具，
   不把字体在本机安装成功等同收件人电脑也可用。

## 官方来源查找线索

以实际访问结果为准，不写死下载版本或承诺长期路径有效：

```text
https://github.com/google/fonts/tree/main/ofl/cinzel
https://github.com/google/fonts/tree/main/ofl/mashanzheng
https://github.com/adobe-fonts/source-han-serif
https://github.com/adobe-fonts/source-han-sans
https://github.com/notofonts/noto-cjk
```

下载前阅读所选版本随附的 OFL/LICENSE、字体名和文件格式。许可证保留到 fonts/licenses；
可用范围不明则不安装/分发该字体，改用已授权替代。字体下载失败时保留失败记录，不假称装好了。
对于可变字体/多语言字体集，优先已验证的静态 TTF/OTF；脚本不下载 ZIP、不自动解压字体包。

## 工具用法

```text
python <SKILL_DIR>/scripts/font_assets.py inventory
python <SKILL_DIR>/scripts/font_assets.py inspect <font-file>
python <SKILL_DIR>/scripts/font_assets.py download --workspace <workspace> --url <reviewed-raw-font-https-url> --license-url <raw-license-url> --source-page <official-page> --filename TitleFont.ttf --license-reviewed
python <SKILL_DIR>/scripts/font_assets.py install-user <workspace>/fonts/downloaded/TitleFont.ttf --workspace <workspace>
python <SKILL_DIR>/scripts/font_assets.py install-user <workspace>/fonts/downloaded/TitleFont.ttf --workspace <workspace> --apply
```

最后一条仅在取得实际安装同意后执行。记录本机安装副本路径和注册信息到 logs，
工程内的下载字体/许可证仍保留；系统安装位置是 Windows 需要的例外，不把其他项目素材散落到用户目录。
脚本拒绝覆盖已注册的不同字体；注册成功后仍须在 Office 样张中验证。

compose 的 `font` 为中文/东亚字体，`latin_font` 为英文；可在元素、段落和 run 层设置。
例如中文标题用选定宋体/展示体，正文用选定黑体，英文短标题用 Cinzel，但必须确认这些字形确实存在。
装饰字体只应用于允许的标题层级；保留原文强调。字体改动会改变字宽/换行，必须对所有受影响页重新
运行布局检查与 [视觉自检](visual-review-loop.md)。脚本字符度量的回退估算不能代替 Office 实际测量。
