# UI/UX Design 子技能

版本1.0.0；名称`ui-ux-design`，前身为用户安装的distinctive-ai-design。
本项目独立编写后继指导，没有把上游未声明许可的整包或文章正文复制入库。

- [SKILL.md](SKILL.md)：设计探索、实现选型和验证入口。
- [参考](references/README.md)：动效、shader/3D、评审和来源。
- [界面元数据](agents/README.md)：展示名与调用提示。

随ppt-beautify-studio安装到其subskills/ui-ux-design，不重复复制到skills根目录。主技能通过相对路径读取，独立任务也可按路径加载或在宿主发现后调用`$ui-ux-design`。单独ZIP用于需要独立安装的环境；不要同时安装两份同名入口。
