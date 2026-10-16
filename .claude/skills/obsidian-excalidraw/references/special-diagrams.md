# Mindmap、WaveDrom、Git 与 GIF

## Mindmap

真实能力来自绘图脚本目录下`mindmap/Feature-Mindmap-Engine.md`与`Action-Create/Import/Detach/Export-Mindmap-*`。Engine提供折叠图标、Tab/Enter新节点、方向键导航、空格编辑及增删节点后的布局；`window.MindmapAPI.runLayout(sceneElements, commitToHistory=false, activeEa)`是实际公开脚本入口。

Bridge现有mindmap adapter支持set/clear_feature，目标不限type，配置包括`status/root/parent/level/settings/curveArrow`；这只是元数据，不会自动从自然语言造出整个树。创建时先用原生node和arrow API构造树，读回真实ID，再给节点设置root/parent/level。避免跨图悬空引用和循环父子关系，保留双向绑定。

```json
{"op":"set_feature","feature":"mindmap","targets":["rootNativeId"],"config":{"status":"open","root":"rootNativeId","parent":null,"level":1,"settings":{"direction":"LR","arrowType":"normal","defaultGap":15,"enableFixedPoint":true}}}
```

子节点`root`指同一native root；`parent`指实际父节点；`level`是正整数。root/settings中的ID字符串不是自动解析的logical ref，必须用创建结果的native ID。

状态按真实Engine使用`"open"/"close"`；本包Bridge 0.12.0已将旧的`"closed"`声明与校验修正为`"close"`。已有原生close图不迁移；旧Agent请求应更新，不提供closed别名。状态元数据本身不等于递归隐藏/布局已执行，仍需Engine的真实点击/快捷键或受信API流程并读回子节点hide。

需要确定布局时，受信EA脚本绑定明确画布并调用`await window.MindmapAPI.runLayout(treeElements,true,ea)`，不得漏传activeEa。方向实际有`LR/RL/TD/BU`，arrowType `normal/elbow/curve`；curve碰撞检查仍有边界，不拿PNG好看等同所有几何通过。detaching要同时处理parent/descendants和边界arrow，不能只删root字段。

Mindmap Markdown导出Action读取bound text/原文、按发出arrow遍历子节点并按y排序，但会suggester/inputPrompt选择文件名。Agent自动导出应先确定新输出文件，再复用该遍历逻辑，检查cycle/丢节点；不自动覆盖既有Markdown。导出的Markdown是结构文本，不是证明原生布局/交互已验证。

## WaveDrom / wave-drom

`wave-drom/Feature-Wavedrom-Engine.md`内置WaveDrom运行时，按`customData.wavedrom=true`与`customData.code`渲染波形，并缓存SVG/Image。Action Manager是编辑面板，不是无交互创建API。Bridge已有`wavedrom` adapter：先创建透明rectangle，再设置源代码：

```json
{"op":"set_feature","feature":"wavedrom","targets":["waveBoxNativeId"],"config":{"code":"{ signal: [{ name: 'clk', wave: 'p......' }, { name: 'data', wave: 'x.345x.', data: ['A','B','C'] }] }"}}
```

代码是WaveDrom JSON/JSON5数据，不是任意JS。保留source；改code后清相关cache、按native测量适配carrier，等真实SVG/image加载后export。矩形是可编辑carrier，波形源可修改；不是每根波形线都自动变成独立原生可编辑line。PNG要实测波形、标签/总线数据，不把空矩形当成功；无运行时则报告缺依赖。

Bridge 0.12.1的PNG导出复用真实WaveDrom Engine：缓存与当前code匹配且图像解码就绪才使用，否则有界等待实际SVG/image生成并在临时导出workbench捕获；失败返回complete=false与wavedrom资源原因。不修改原carrier/源数据来导出，不能依赖“首轮先空白、第二轮才显示”的时序。

## Git（用户原名保留）

已调查的绘图脚本集合未发现Git专用目录/Engine/Action；不能宣称已支持Git版本管理脚本，也不能把git擅自改成gif。

若用户指Git历史/分支图：Agent可在用户明确仓库中只读真实`git log --graph`/提交父子数据，再用普通原生节点和箭头表达commit/branch/merge关系；短hash标签对应真实commit，merge保留多个parent。这是Git数据→绘图的工作流，不是现有绘图脚本的Git adapter。禁止擅自commit/push/rebase/reset或修改仓库，图形结果仍经PNG确认。用户明确Git含义再选语义，常规能力发现可以先完成而不打断其他功能。

## GIF（实际另有此能力）

`gif/Action-Toggle-GIF.md`写`customData.gif={index:0,frameCount:...}`并清imageCache；`Feature-GIF-Engine.md`提供键盘步进和悬浮UI。输入应是真实GIF资源，插件底层解码/多帧缓存需就绪，修改index不是GIF文件本身被重新编码。

MCP可插入真实image并保留来源，GIF元数据与Engine需受信宿主配置；本包没有gif FEATURE_SPEC，不造`set_feature gif`。默认PNG仅证明当前一帧；逐帧/播放需真实view验证，不能声称导出PNG保存了动画。原图、源GIF和交互状态分别保留。

通用Engine/URI/信任边界见[script-execution](script-execution.md)；图片获取见[images-assets](images-assets.md)。
