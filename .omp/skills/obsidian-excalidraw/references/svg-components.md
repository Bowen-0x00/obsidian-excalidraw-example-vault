# SVG Path 图形与可复用组件

SVG path 是本修改版中制作数字电路、微架构和任意工程符号的重要方式。目标不是把SVG栅格化，而是把路径承载在可编辑的 Excalidraw `line` 元素上，并保留路径源、viewBox、组件逻辑ID和可选标签/端口。

多色／单色图标新增路线见[icons](icons.md)：新组件支持rectangle＋`customData.svgLayers`有序多层路径和整体动态样式。以下`svgPathShape`单路径line流程仍适用，不用它的严格bbox归零规则或“每色一个carrier”限制新图层格式。

## 真实脚本依据

- 绘图脚本`generate/Action-Generate-Digital-SVG.md`：路径库→`measurePath(pathData)`测量真实SVG DOM bbox→`shiftPathData(path,bbox.x,bbox.y)`归一化→创建line carrier→写`customData.svgPathShape`与`svgViewBox`→单独创建标签。
- 绘图脚本`generate/Action-Generate-Digital-Microarch-Items.md`：同样的路径测量/归一化，按分类、网格、真实中心布局，写`componentName/category/isLibraryItem`，预览标签写`isPreviewLabel/parentItemName`，保存receipt。当前版本每项是独立line，**并未自动group标签或端口**；还会删除指定开发画布全部活跃元素，仅可在用户授权的独立开发图中复用，不能把整图清除带到通用脚本。
- Bridge `FEATURE_SPECS.svg_path_shape`/`createSvgPath`：`create_svg_path`操作构造line；`drawing_primitives`目前只有brace等内置类型，没有通用`kind:"svg"`/组件目录规划器。任意path走准确的`drawing_apply create_svg_path`或受信EA脚本，不捏造工具。
- 真实插件API和Engine通过`svgPathShape`渲染；line的`points`只承担carrier geometry，path字符串决定内部矢量形状。不要把原始路径的绝对坐标直接同时当scene x/y和path坐标。

## 路径规范化不变量

1. 输入是SVG path `d`字符串。支持的命令和参数必须由真实归一化器解析；路径含相对命令、弧线、多个子路径、负坐标时先用实际SVG DOM/path parser核对，不用正则猜。
2. 用真实DOM `getBBox()`得到`{x,y,width,height}`，不是按字符串或端点估算。若宿主无DOM/SVG测量，停止并报告，不能生成假bounds。
3. 将原路径完整平移`(-bbox.x,-bbox.y)`，再测量确认bbox原点接近0、尺寸匹配viewBox。两脚本的`shiftPathData`只处理其已有受控写法，不是通用SVG parser：科学计数法`1e-3`、紧凑数字`10-5`、起始相对m以及隐式命令都可能破坏该正则。通用输入使用已确认的SVG path解析/变换库，或从一开始在归一化局部坐标写path；缺真实解析器时不套正则冒称任意路径可正确处理。
4. 未缩放情况下scene位置为layout origin+bbox.x/y，尺寸为bbox.width/height；也可按单元格中心对齐或指定新的origin。缩放时viewBox保持**源**真实宽高，carrier width/height是**目标**显示尺寸，比例为target/viewBox。优先等比例，可负scene坐标；不要反向修改path源来假装resize。
5. Bridge要求path实测bbox为`{x:0,y:0,width:viewBox.width,height:viewBox.height}`，不是仅“在viewBox里面”。纯水平/垂直线bbox一维为0，不满足该操作的positive尺寸约束，使用原生create_linear；不能假填1px viewBox。getBBox不含完整描边/阴影范围，PNG padding和相邻间距另留余量。
6. line carrier不是Bridge支持的arrow绑定目标；业务连接使用透明rectangle anchor proxy或库insert返回的anchorElementId，明确group与稳定组件逻辑ID，proxy和路径属于同一construction unit。视觉端口线不自动产生电子引脚、网表或真实binding。

## 推荐组件结构

一个可入库的组件建议包含：

```text
component root
├─ line carrier: customData.svgPathShape/svgViewBox/componentName/category
├─ optional native bound label: text（预览标签不等于业务标签）
├─ optional port/anchor lines or anchor proxy
└─ groupId / agentLibrary metadata（仅在执行层生成）
```

逻辑层先描述：`id/name/category/path/ports/label/variants`；执行层负责native IDs、seed/version/index、group关系、精确bbox和保存。入库前分别给每个组件形成可移动、可复制、可预览的construction unit；内部重叠合法，跨组件重叠仍需check。`isLibraryItem:true`/`componentName`等标记用于维护和识别，不代替真实item ID。

示例组件意图记录（推荐组织数据，不是已实现的新DSL或可直接调用的ports schema）：

```json
{
  "id":"mux-2to1",
  "name":"MUX 2:1",
  "category":"datapath",
  "path":"M 10 5 L 70 15 L 70 35 L 10 45 Z M 0 15 L 10 15 M 0 35 L 10 35 M 70 25 L 82 25",
  "label":"MUX 2:1",
  "ports":[{"name":"a","side":"left","ratio":[0,0.33]},{"name":"y","side":"right","ratio":[1,0.5]}]
}
```

执行结果中的path carrier再由MCP `create_svg_path`或可信EA `addLine`构造，不让模型手填ID/version/nonce/fractionalIndex。

## MCP路径

已连接Bridge时优先生成测量后的真实operations，再`drawing_apply`：

```json
{
  "op":"create_svg_path",
  "ref":"mux-2to1",
  "x":120,
  "y":80,
  "width":164,
  "height":80,
  "path":"M 10 0 L 70 10 L 70 30 L 10 40 Z M 0 10 L 10 10 M 0 30 L 10 30 M 70 20 L 82 20",
  "viewBox":{"width":82,"height":40},
  "style":{"strokeColor":"#1e1e1e","strokeWidth":2,"roughness":0},
  "customData":{"componentName":"MUX 2:1","category":"datapath","isLibraryItem":true}
}
```

这是当前Bridge的单path可执行operation示例：path已将原bbox的y=5整体平移到0，源viewBox=82×40，目标显示=164×80；`points`由执行器生成，不在输入中手填。metadata/component ports必须自行明确映射，不提供自动绑定推断。旧格式的多路径／不同颜色需多个carrier并group；新宿主多色图标优先[svgLayers矩形格式](icons.md)，保留有序图层而不必拆多个元素。原生text另保留，category标题和isPreviewLabel展示标签不默认入组件；源路径可改不等于每段都有原生顶点编辑。

对于用户库素材，SVG path carrier也按`drawing_library(insert)`原生导入，保留line+path编辑性；禁止用一张整页PNG替代组件。若用户要求加入`.excalidrawlib`，先生成/复核独立画布和预览，除非明确授权，不自动写入用户库。

整份SVG文档不是一个d字符串：rect/circle/ellipse/path、嵌套transform、不同stroke/fill、文字与图片需通过实际支持的转换保留语义。新svgLayers可以在单carrier保存多色path，但Action有限解析器不保留任意继承、transform、clip/CSS／滤镜；详见[图标转换边界](icons.md)。Agent可组合可表达的静态矢量符号，不承诺任意外部SVG无损导入；普通矩形／文本仍用原生元素。

## 可信EA/URI脚本路径

没有MCP但要复用现有两个Action：复制脚本到实际script root的独立开发副本，改正/配置明确`TARGET_CANVAS`，通过Advanced URI运行。脚本必须：

- 目标view精确校验；
- 组件输入保持数据表而非源码字符串散落；
- 真实`getBBox()`测量和归一化；
- 不以scrollX/scrollY作为永久布局原点；
- `await ea.addElementsToView(false,true,true)`并读回；
- 保存逻辑receipt：runId、script hash、目标、逻辑组件、native IDs、保存结果；
- 不删除非本任务用户内容，除非用户明确要求重建并有备份。

生成微架构/电路库时，先从现有库清单去重；组件分类/标签只放在预览说明或安全metadata，不能把预览标签误入用户实际item。参考图只约束风格，不覆盖实际PNG事实。

## 质量与导出

每轮：

1. 结构读回：line carrier存在、path/viewBox完整，label和端口不重叠，group/anchor有效；
2. 程序check：bounds、非预期组件间重叠、箭头穿线、文本containment和资源；
3. PNG全图：查看路径是否真的渲染、负坐标/弧线/孔洞/端点是否正确、中文标签是否完整；必要时局部PNG放大；
4. 修改path或布局后重新读当前revision和PNG，不把rounded反馈坐标回写精确场景；
5. 交付可编辑canvas、PNG、组件逻辑清单、实际native IDs/组边界、剩余unknown。路径源可编辑不等于连接端口语义已自动成立。

如果SVG含外部图片、脚本、foreignObject或未知滤镜，先按[images-assets](images-assets.md)做来源和安全审查；只保留真实可渲染部分。原生PNG看不到的交互/动画仍按对应Engine单独验证。

实际运行验证：隔离ymjr 2.27.3-1 + Bridge 0.12.0中用create_svg_path创建MUX梯形和含Q/a命令的复合曲线图，两者都是line carrier、源viewBox与2倍显示尺寸分离，scene含负坐标；标签原生text，各组独立，修改path后组/ID保持。完整PNG实际查看、check零问题、review completed。用户两个原生成脚本仅作为代码依据，没有运行其清场/重建逻辑或改写它们。
