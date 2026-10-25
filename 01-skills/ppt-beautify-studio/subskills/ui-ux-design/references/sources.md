# 研读来源与适配范围

核对日期2026-10-25。只总结公开可读内容及官方技术事实，不复制文章或上游skill正文。

## 设计方法

[Anshu Chimala / Lenny's Newsletter：How to turn your AI into a world-class designer](https://www.lennysnewsletter.com/p/how-to-turn-your-ai-into-a-world)。当前可读技巧1–6：利用外部随机线索拓宽探索；由个人偏好细化设计意图；使用独立图像评审；组合图像与视觉效果；用视频表现复杂运动/状态过渡；通过减法改善表达。第7节仅标题可见，付费正文未纳入。

文章提到shader和3D可与图像结合，但没有提供完整技术教程。本项目的媒介选择表、时间轴记录、触摸/减少动态/资源管理、PPT适配和验证清单是独立的执行适配，不归因于原文。文章里的模型/服务/成本例子不作为固定依赖或可用性承诺。

[distinctive-ai-design固定来源](https://github.com/houxin0010/distinctive-ai-design/tree/92c68366767b98924fe2719c16659e7f1e93c7af) 为此前安装的前身。该来源树未见LICENSE；本次重命名后继以自有表述重新编写，不将其正文/测试代码/整包重新发布。

## 官方技术依据

- [MDN：prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion)：读取用户减少动态偏好；不是自动保证所有动画可访问。
- [MDN：webglcontextlost](https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/webglcontextlost_event)：画布可能丢失WebGL上下文；恢复/回退仍需实现和验证。
- [Three.js：ShaderMaterial](https://threejs.org/docs/pages/ShaderMaterial.html)：该材质使用GLSL并适用于WebGLRenderer；其他后端依项目版本核验。
- [Three.js：AnimationMixer](https://threejs.org/docs/pages/AnimationMixer.html)：clip/action播放、秒制deltaTime及缓存清理的依据。
- [Three.js：GLTFLoader](https://threejs.org/docs/pages/GLTFLoader.html)：加载结果可包含animations数组；具体动画是否存在需检查真实资产。
- [Three.js：Rendering on Demand](https://threejs.org/manual/pages/rendering-on-demand.html)：无持续运动时可在变化发生时渲染。
- [Three.js：Cleanup](https://threejs.org/manual/pages/cleanup.html)：纹理、几何和材质等需显式释放；按资源所有权处理。
- [Three.js：Responsive Design](https://threejs.org/manual/pages/responsive.html)：画布尺寸、摄像机和像素密度需按显示场景处理。
- [Microsoft：Morph](https://support.microsoft.com/en-us/powerpoint/training/use-the-morph-transition-in-powerpoint)：跨页共享对象的平滑过渡，图表不支持同样的Morph处理；支持性按目标Office核验。
- [Microsoft：3D animation effects](https://support.microsoft.com/en-us/powerpoint/3d-animation-effects-in-powerpoint)：原生3D动画依版本/平台；Web端创建与播放能力不同，不能以桌面支持推断所有客户端一致。

技术链接用于实现前核验；本技能不会因为文档存在而自动安装库、生成付费媒体或证明宿主支持动画。
