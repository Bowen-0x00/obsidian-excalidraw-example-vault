# 排版、Arrow特殊属性、动画与外部导出

## Distribute

现有Bridge支持`distribute`与`align`，输入明确native IDs。简单独立元素：

```json
{"op":"distribute","targets":["a","b","c"],"direction":"horizontal","includeBoundText":true}
```

Bridge horizontal/vertical算法按外包围盒总跨度与总尺寸计算等边距；绘图脚本`distribute/Action-Distribute-Horizontally/Vertically.md`则先BFS合并group/container/bound text为不可分割实体、按视觉中心等距、首尾不动，还处理单实体在frame中居中。两者不是等价实现，不能把MCP独立元素distribute用于复杂群组后声称保留全部内部布局。

复杂组先显式求group/container/bound-text闭包、计算每组真实bounds，再translate整组并去重绑定text位移，或在受信宿主复用原Action的算法。文字已跟随容器移动时不能二次移动；箭头绑定/锁定图元须读回校验。对角线/文字排版看`Action-Distribute-Diagonally.md`与`Action-Distribute-Text.md`，不造第三个direction；没有对应adapter就受信脚本复用，不假称Bridge支持。paste auto-distribute是粘贴Hook，不能当全画布自动布局。

## 尺寸适配：先定用途，再插素材

库里的坐标单位和原始尺寸不是最终阅读尺寸。Agent须主动决定大小，不要求用户给坐标，也不能把“小但无碰撞”当成已完成。PNG导出`scale`只提高输出像素，**不会改变元素之间的大小关系**。

| 对象/时机 | 已有入口 | 适用边界 |
| --- | --- | --- |
| 素材尚未插入 | `drawing_library(insert,scale=s)`；compose的`nodes[].library.scale` | 整项等比缩放；默认1不是自动fit。compose的node.size只影响布局空间，不会替代library.scale |
| 素材/整页已插入 | `drawing_apply`的`scale_selection {targets:[完整成员ID],factor:s,fromCenter:false}` | 原生整体缩放位置、点列、文字和frame子元素；含透明anchor和全部装饰，不只选可见主图元 |
| 单个普通形状或图片 | `resize {target,width,height,anchor:"top-left"}` | 仅改该元素尺寸和绑定文字布局，不自动缩放组员/字号；line/arrow被拒绝，SVG line carrier用scale_selection |

1. `query/get`取得精确`bounds`，`preview`看真实内容。已有图按ID读取full，并确认groupIds、frameId、锁定、绑定和实例成员；不要把整个共享外层group误当某个小符号。使用插入返回的`insertedElementIds/sourceIdMap/anchorElementId`定位本次素材。
   模板中已通过预览确认的整页底色/内页rectangle是合法包含背景；需要时以`patch_custom_data.merge:{isContainer:true}`声明容器语义再检查，不移动/删除底板来消除“重叠”。不得给真正冲突的业务节点乱标container，也不把所有库矩形自动当背景。
2. 选内容区`W×H`，给图文留内边距。等比装入用`s=min(W/sourceWidth,H/sourceHeight)`；按目标宽或高用相应比值，另一维同步计算。`s>1`允许放大。页模板以frame宽高为页面基准，普通符号以整项真实bounds为基准；含标题等突出部分时另查整体bounds，防止相邻页相碰。库scale现有范围`0<s<=20`，不把这个范围误写成PNG倍率。
3. 插入前优先传scale，减少重排。插入后算的是`factor=目标尺寸/当前尺寸`，不是源尺寸的绝对scale；多次修改每次重新读当前尺寸，不能反复乘同一绝对倍率。精确选区用targets，原生group确认无多余内容时才用groupId。`fromCenter:false`便于保留左上角；要求居中则显式true。
4. 演示新页未指定尺寸时，以1280×720作为版式起点，先适配模板再测量/填标题、正文和图片。模板比例不同则保留比例，选择合适同系列版式、留白或按用户允许重排；不把4:3模板静默拉伸成16:9。`drawing_present`现有输入是**presentation顶层scale**，不是page.scale/width/height；各页源尺寸不同时分次调用或逐页insert后适配，不能传不存在的自动fit字段。
5. 电路/架构先按角色和端口密度确定符号目标大小，同类同尺度；不同角色不强行同宽高。读真实stub后在**缩放后**重算端口scene坐标和fixedPoint，再接线。对已连线符号缩放其完整实例（含anchor），不选只接一端的外部箭头；邻边随绑定更新后读回检查。放大透明anchor而不放大可见SVG不算适配。
6. 按目标阅读字号测量新文字。底板放大后再填字；已有完整页整体放大会连字号一起放大，随后按用户意图调整正文排版，不靠压小字体掩盖底板或空间不足。确实需要更多内容时调整布局/页尺寸或拆页，不删减业务内容。
7. read确认实际尺寸、相对位置、frame归属、ID/源码和绑定；check→全图及单页/局部PNG→实际看图→review。必须把“底板不足、符号主次比例失衡、字太小”作为视觉问题修正；程序无重叠不等于尺寸合适。锁定/原生API缺失则明确报告，不伪称已resize。

例如读取某符号60×45，要240×180，插入用`scale:4`；已插为120×90则用`factor:2`，不是再乘4。这是计算示例，不是每个ALU/MUX的固定尺寸。

## 原生选区旋转与缩放

Bridge 0.13.0新增`rotate`、`scale_selection`，通过现有`drawing_apply`批量提交，没有另造MCP工具或复制缩放算法。宿主`App.selectionTool.ts::maybeHandleResize` → `resizeElements.ts::transformElements` → `rotateSingleElement/rotateMultipleElements/resizeSingleElement/resizeMultipleElements`；实际安装包入口是`excalidrawAPI.App.maybeHandleResize`，不可用时报`NATIVE_TRANSFORM_UNAVAILABLE`，不回退逐项改JSON。

```json
{"op":"rotate","groupId":"真实原生group ID","degrees":90}
{"op":"scale_selection","targets":["节点A ID","节点B ID","内部箭头ID"],"factor":1.5,"fromCenter":true}
{"op":"patch_element","target":"单节点ID","patch":{"angle":1.5707963267948966}}
```

- `groupId`与`targets`二选一。targets是精确选区；groupId读取当前`groupIds`，包括嵌套组中的成员，不用logicalId代替。绑定text由owner处理一次；单独选绑定text会提升到owner。
- `rotate.degrees`是相对角度，正数顺时针；`element.angle`及patch.angle是绝对弧度。共同中心由真实边界求出；不是各自绕自身中心修改angle。
- `factor>0`，默认中心缩放；`fromCenter:false`保留未旋转多选边界左上角，单个已旋转元素则对应其本地西北角。位置、点列、形状与文字同缩放，字号/最小尺寸/anchored资源遵从原生规则；不提供镜像或非等比整组缩放。
- 内部箭头保留双向绑定；节点的外部箭头更新端点，外部节点保留。若明确选中箭头但没有选其绑定端点，报`TRANSFORM_PARTIAL_BINDING`；原生变换若改变连接目标则报`TRANSFORM_BINDING_CHANGED`，不静默丢业务关系。
- 原生Frame不允许旋转；缩放包含frame children及绑定文字。锁定选区或被更新邻边/文字报`ELEMENT_LOCKED`。最小尺寸导致无变更报`NATIVE_TRANSFORM_NO_CHANGE`。
- 执行器同步切换到隔离Scene副本，恢复App scene/state/selection/Hook后才提交变更，保留同一事务revision检查与undo。失败不提交之前暂存的变换。返回`transforms`包含center、selectedIds、updatedIds、degrees/factor和真实实现来源。
- `afterTransformElements`宿主Hook可能异步写live API，因此准备阶段不触发。表格行列边界联动、泳道吞并/剥离等Engine特定手势**不是**这两个原生几何操作的承诺；相关元数据不自动重解释。
- 90°整数倍的世界坐标bbox/直线点列纳入现有碰撞检查；任意非直角旋转与曲线仍unknown，不伪造check=pass。完成后read/check→PNG→实际看图→review。

真实宿主验证：同组双节点+内部标签箭头绕共同中心顺时针90°，再放大1.5倍，节点文字20→30；外部节点及文字不变，外部箭头跟随；另验证绝对π弧度、已旋转单节点缩放、负坐标freedraw点列/压力、SVG path源保留、Frame children缩放、锁定/失败不提交与undo。PNG均实际查看，非对所有扩展Engine作全面手势兼容保证。

## 原生 Line Crossings：弧跳、留白、交点

这是更新后的Excalidraw-ymjr**渲染器**能力，不是额外Engine、素材或MCP Feature。作用于原生`line`/`arrow`的`customData.lineCrossings`；原始points、ID和绑定保持不变，交叉邻居移动后由宿主重算呈现。原生几何优先，**禁止默认叠白色/背景色矩形遮罩、手画桥弧/圆点或切成多条线模拟断开**；gap是实际抬笔留白，彩色背景不穿帮。

| 值 | 表达 | 选择规则 |
|---|---|---|
| `arc` | 跨越方绘制弧跳 | 业务/电气上不连接；默认垂直线跨过水平线 |
| `gap` | 让路方在交叉处留白 | 不连接；默认水平线让路，建议相交两线都标gap |
| `dot` | 实心交点 | 仅当用户语义确认在此连接/汇流；**视觉标记不新增端点绑定或netlist关系** |
| `none` | 普通交叉，无跳线处理 | 显式关闭此样式；不是“保证两线物理不连接”的语义替代 |

### 现有MCP调用，不新增DSL

`drawing_apply`的原生创建可以直接传customData。两条线都声明相同模式，不依赖侧栏“下一笔继承”的会话状态：

```json
[
  {"op":"create_linear","kind":"line","ref":"horizontal","x":0,"y":120,"points":[[0,0],[300,0]],"style":{"strokeWidth":2,"roughness":0},"customData":{"lineCrossings":"arc"}},
  {"op":"create_linear","kind":"arrow","ref":"vertical","x":150,"y":0,"points":[[0,0],[0,240]],"endArrowhead":"arrow","style":{"strokeWidth":2,"roughness":0},"customData":{"lineCrossings":"arc"}}
]
```

连接已知节点时，把同一字段放在connect的**顶层customData**，不是style，不是`set_feature`：

```json
{"op":"connect","ref":"bus","from":"@source","to":"@target","elbowed":true,"style":{"strokeWidth":2,"roughness":0},"customData":{"lineCrossings":"gap"}}
```

已有连线按明确ID做merge，保留其他扩展与绑定；批量是多个操作，并非patch_custom_data支持targets：

```json
[
  {"op":"patch_custom_data","target":"水平线ID","merge":{"lineCrossings":"gap"}},
  {"op":"patch_custom_data","target":"垂直线ID","merge":{"lineCrossings":"gap"}}
]
```

关闭用`merge:{"lineCrossings":"none"}`，或`remove:["lineCrossings"]`；不要替换整份customData。迁移旧遮罩图时先确认哪些ID确为模拟交叉的装饰，仅移除这些冗余遮罩/假弧/假点，保留原业务线、标签和用户主动叠放内容，不全图clear重建。

当前planner的`diagram.edges`和`drawing_primitives`连接输入**不会自动转发任意edge.customData**。不要把字段塞进图描述后当已生效：保留完整plan.operations，再附`patch_custom_data {target:"@edge:关系逻辑ID",merge:{lineCrossings:"arc"}}`，或apply后用真实refs/ID修改；primitive按其返回ref处理。使用`drawing_templates(style="visio")`也不会自动加交叉语义。

### 优先级与适用边界

- `customData.lineJumpPriority`是数字；当前源码只有**两条线都提供数字且不同**时才按较大值跨越，否则回到垂直/水平规则，同向或斜线再按ID确定。要水平线弧跳，就给水平线10、垂直线0，并把两者lineCrossings设为arc；不要只给一根线10就声称强制优先级成功。
- arc桥弧/gap半宽当前默认8个scene单位，近邻交点可能缩小；不是PNG固定像素，也没有已暴露的radius配置。不要靠装饰图元改半径。
- 首选直线/折线/正交elbow箭头。靠近端点/拐角、极短线段、平行或共线重叠有排除规则；曲线、block-arrow和svgPathShape走特殊渲染分支，不保证与普通点列有相同交叉效果，不把所有line载体都设为走线。
- T型分支由几何端点与线段位置识别，不应强行桥接；用户提供规范描述了自动圆点，源码也有junction记录，**本轮真实PNG的T分支未显示圆点**。不可把自动圆点当已验证的导出保证；需要这一语义时实际查看并报告差异，不悄悄补一个假圆点或修改用户插件。
- `dot`不修改startBinding/endBinding/boundElements，不能用它代替connect/rebind的业务关系。`arc/gap`也只解决线—线交叉，不免除穿节点、标签遮挡、箭头端点错误等检查。
- 侧栏Line Crossings可改选中line/arrow，并通过`currentItemLineCrossings`影响后续手绘线；Agent自动创建仍逐条显式传值，避免修改全局绘制偏好。Native CLI与Bridge schema不同，先读其schema确认customData是否允许；未确认时走已验证MCP，不照抄op到原生CLI。

### 验证与能力来源

先按目标ID读full，确认line/arrow、原始points和业务绑定；apply后重新读回customData及关系，再全图PNG实际查看。交叉配对需要场景上下文，ids局部PNG必须包含两根相交线，单根预览不能证明全图无交叉。没有新renderer的旧宿主可能保存字段却不显示效果；字段能写≠能力已生效，不静默退回遮罩技巧。

本轮已在真实更新宿主验证：arc/gap/dot/none、两线数字priority反转；浅蓝背景下gap露出原背景、无交叉遮罩；connect创建的双向绑定elbow箭头弧跳→gap切换；patch前后ID/points/绑定与元素数量保持。PNG实际查看；T分支圆点缺口单独保留。没有以这轮PNG证明SVG/所有特殊箭头或交互帧率。

来源：用户提供的Line Crossings规范；内核`packages/element/src/crossings.ts`（检测/优先级/path）、`shape.ts`（普通/elbow分支）、`renderElement.ts`（Canvas交点）、`packages/excalidraw/actions/actionProperties.tsx::actionChangeLineCrossings`及`App.tsx`（UI继承）。文档中的8px/60FPS不是Agent必须硬编码的布局常数或已测性能承诺。

## 箭头选型：关系语义先于装饰

先区分五件事：`start/endArrowhead`决定类型/方向；**`customData.blockArrowWidth`决定PPT宽箭身厚度**；`strokeWidth`决定轮廓描边；`arrowHeadSize`决定头部比例；原生points/绑定/waypoints决定长度与路由。宽度不是line元素的width/height，也不是PNG倍率。先按语义和本轮视觉偏好选型，同类一致；已有图只改用户要求的线。

| 关系/用途 | 推荐起点 | 约束 |
| --- | --- | --- |
| 架构图、数据流、数据通路 | `startArrowhead:null,endArrowhead:"triangle"`，实线、细线身 | 实心三角指向数据去向；不是所有架构关系都是数据流，依赖/控制另用有图例的细虚线 |
| 流程推进、架构主路径、阶段转换、教学/对比图的强调连接 | `block_arrow`实心或`block_arrow_outline`轮廓，宽短/细长按空间和层级选 | PPT是箭头视觉类型，**不限于PPT页或少数阶段图**；密集拓扑按角色控制粗细，不能全线粗化遮挡其它关系 |
| 普通控制/依赖/轻量流程 | 普通`arrow`或小`triangle`；依赖可dashed | 明确线型含义，不能把所有实线自动改成虚线；分支仍要完整“通过/未通过”等标签 |
| UML泛化/实现 | 指向父类/接口的一端`triangle_outline`；实现dashed | 不用实心数据流三角替换泛化；`from/to`仍保留真实业务方向 |
| UML组合/聚合 | 整体端`diamond`/`diamond_outline`，另一端按语义null | 菱形不是“装饰性数据流箭头” |
| 双向交换 | 语义确为双向时两端头，或两条有各自标签的有向边 | 不因布局对称强加双向；请求/响应不同标签优先分线 |
| 无向连接/电路线 | 两端null；必要时用原生line | 不强加流向；circle/bar仅用于用户约定的端口/终止/棒端语义，不能冒充ER基数或电气连接 |

Bridge 0.13.5支持：`arrow,bar,circle,circle_outline,triangle,triangle_outline,diamond,diamond_outline,block_arrow,block_arrow_outline,null`。先用当前capabilities/feature schema核对，旧Bridge可能只开放outline；不要仅凭插件支持就向旧MCP提交未开放头型。chevron等其它内核类型仍不在此白名单；不传`"block"`、`"none"`或`"filled_triangle"`，不静默换头型冒充。

### 创建、增量修改与参数边界

```json
{"op":"connect","ref":"data","from":"source ID","to":"target ID","start":{"anchor":"right","mode":"orbit"},"end":{"anchor":"left","mode":"orbit"},"startArrowhead":null,"endArrowhead":"triangle","arrowHeadSize":1,"elbowed":true,"style":{"strokeWidth":2,"roughness":0,"roundness":{"type":2,"value":6}}}
{"op":"set_arrow_style","targets":["已有箭头ID"],"endArrowhead":"triangle","arrowHeadSize":1,"strokeWidth":2}
{"op":"set_arrow_style","targets":["已有PPT箭头实际ID"],"endArrowhead":"block_arrow_outline","arrowHeadSize":0.8,"strokeWidth":2}
{"op":"patch_custom_data","target":"已有PPT箭头实际ID","merge":{"blockArrowWidth":36}}
```

- connect/create_linear的头型和arrowHeadSize在operation顶层；diagram/compose/primitives的连接头型也在每条edge/item顶层。不要只在style中塞endArrowhead指望高层默认覆盖正确。规划器默认arrow不表达用户意图，必须显式选择；高层不自动转发arrowHeadSize/blockArrowWidth，按返回native refs补`set_arrow_style/patch_custom_data`。
- `set_arrow_style`只接受strokeWidth/startArrowhead/endArrowhead/arrowHeadSize/edge；颜色/虚实线用`patch_element.patch`，固定转角另patch.roundness。省略edge以保留已有固定radius；`edge:"round"`会重置为无value的默认圆角。更换头型保留ID/points/标签/双向绑定，不重建箭头或手贴三角形。
- `arrowHeadSize`是0.125–8的**倍率**，不是px；这是接口边界，不是审美建议。细线从1起，建议0.75–1.25附近看PNG再调；线宽以1.5–2.5为常用起点。放大头不能解决路径太短；端部段要留头部、节点边距与标签净空。
- **箭身宽**：`customData.blockArrowWidth`为正有限数、单位是scene单位；选择明确值以免描边变化联动默认厚度。省略时当前实现为`max(16,strokeWidth*6)`。宿主UI滑杆当前4–120、步长2，这是**面板范围**，不是已证明的MCP/内核硬上限或建议全部用120。旧字段`arrowHeadLineWidth`只作兼容读取，写新图/本轮宽度用blockArrowWidth，不同时制造两个冲突来源。恢复默认时先读实际customData，只移除本轮需要的宽度字段；残留旧字段仍可能生效，不能把0当“默认宽度”。
- **长度独立于宽度**：由真实起终点/点列/绑定路径确定，不能用arrow.width/height或resize把线身“压扁”。保持端点只调粗细用同ID的patch_custom_data；用户要求变短/变长才调整被授权的端点/节点/waypoints并复核绑定，不能为造粗短外观拉脱节点。只要改尺寸而非改方向，不新增startArrowhead或重建箭头。
- **新版头部比例**：当前`getBlockArrowPolygon`使用`headWidth=blockArrowWidth*2.5*arrowHeadSize`，每个block头的长度为`min(headWidth*0.8,总路径长*0.45)`；改变箭身宽会连带改变头部，头倍率则可独立微调。45%是当前实现的防重叠截断，不是美观保证；粗短箭头可能头部主导，不能靠无限放大arrowHeadSize求显眼。该公式以当前真实版本为准，旧宿主需看样张，不把它当跨版本渲染契约。
- **填充/描边**：block_arrow默认内部取strokeColor；outline默认内部取canvasBackgroundColor；新版两者在backgroundColor非transparent时都优先用显式backgroundColor，fillStyle参与填充。轮廓型不是天然透明洞，也不会自动继承所在容器背景。需要特定填充用patch_element.patch的backgroundColor/fillStyle，描边粗细仍用strokeWidth；改箭身宽不要顺手改颜色。浅/暗/彩色容器都看真实PNG。

  | 颜色属性 | 普通细线箭头 | block_arrow / block_arrow_outline |
  | --- | --- | --- |
  | strokeColor | 线身和通常的头部颜色 | 外轮廓描边颜色；filled未设显式填充时也作为内部默认色 |
  | backgroundColor | 不能用它代替线身颜色，不按宽箭内部填充解释 | 两种PPT箭头均支持独立内部填充色；非transparent时优先使用 |
  | fillStyle | 不作为普通线身的粗细/颜色控制 | 宽箭多边形的填充方式；solid适合平整风格 |

  改已有PPT箭头颜色用原生`patch_element`，例如`{"op":"patch_element","target":"实际箭头ID","patch":{"strokeColor":"#9a3412","backgroundColor":"#fed7aa","fillStyle":"solid"}}`；创建时这些字段在create_linear/connect的style中。它与`patch_custom_data.merge.blockArrowWidth`是不同职责；不能把backgroundColor塞进set_arrow_style或只加大strokeWidth冒充填充。颜色可以相同，也可以深色轮廓＋浅色内部；服从本次严格色板/对比需求，不硬编码示例配色。若已显式填同色，两种block类型外观接近是允许的，不凭名称认定一种永远实心、另一种永远透明。
- **曲折/包络**：粗箭占据面积大于centerline；头部、miter拐点、描边与标签都需要净空。现有几何check未认证完整宽箭多边形包络，必须视觉检查邻节点、标签、重叠和导出裁切。当前block多点且roundness非null会走曲线插值，不能把roundness type2当普通elbow同样的固定圆角保证；硬折线用roundness:null并读回/看图。block分支与普通lineCrossings不同，不保证相同跳线效果。
- 架构优先稳定的正交/直连，端口方向清晰、折点少；曲线只在业务/风格确需时用，精确曲线碰撞仍unknown。粗箭头不是总比细箭头好，密集架构只强调主数据通路；不要以“高级风格”删除业务边或遮盖交叉。
- 读回必须核对实际start/endArrowhead、源码样式、ID/点列与绑定，再看PNG。Bridge0.13.3修正了旧重复校验函数无返回值导致`set_arrow_style`把头型写成undefined的问题；旧宿主需更新Bridge，不能将返回成功当视觉生效。

### PPT宽箭尺寸工作流：粗短和细长都由Agent主动设计

1. **确定角色与用途**：强调主路径、两模块间转化、阶段推进、对比关系还是装饰性指向；有真实关系时保留原生arrow及binding，不用矩形+三角形拼贴或整张图片。PPT箭头是可复用图元，不要求用户给长度/坐标/宽度。
2. **先读空间再选比例**：看节点间净空、路径长度L、相邻对象/标签和目标阅读尺度。粗短侧重转化/强调，细长侧重跨区连接；同类关系统一W/描边/头比例，不机械全图同一个宽度。输出可见厚度约为`preview.actualScale*W`，不靠只提高PNG scale改变长宽比例。
3. **长度、箭身、头和描边分别设定**：下表只是独立样张的起点，不是所有图的常量或用户现有端点的移动授权。极短路径容不下头/文字时先调整合法空间、适当减头或减宽；不能删标签/业务边求通过，也不把文字硬塞进狭窄箭头。

| 视觉意图 | 独立示例起点（scene单位） | 调整重点 |
| --- | --- | --- |
| 粗短、强调转化 | L约160，W约36，arrowHeadSize约0.8，描边2 | 头/宽箭包络比centerline宽，给上下留白；标签通常放邻近净空 |
| 细长、跨区推进 | L约420，W约12，arrowHeadSize约1，描边1.5–2 | 缩略后仍可见，避免长而细到像普通线；端点与头部清楚 |
| 同一路径仅变粗/变细 | 保持points和bindings，只改W | 读回相同ID/端点/标签，不能通过改变strokeWidth冒充独立箭身调宽 |

4. **通过现有入口创建/修改**：

```json
{"op":"create_linear","kind":"arrow","ref":"emphasis","x":100,"y":100,"points":[[0,0],[160,0]],"startArrowhead":null,"endArrowhead":"block_arrow","arrowHeadSize":0.8,"style":{"strokeWidth":2,"strokeColor":"#2563eb","backgroundColor":"transparent","fillStyle":"solid","roughness":0},"customData":{"blockArrowWidth":36}}
```

以上为示意坐标的新独立箭头；连接实际节点时用`connect`的真实from/to、端口与必要waypoints，并在顶层customData传宽度。高层diagram.edges/primitive不承诺转发此字段，先compose/plan再按返回ref补`patch_custom_data`。**set_arrow_style目前没有blockArrowWidth字段**，不能塞入后假称生效；用上面的set_arrow_style控制头/描边、patch_custom_data控制宽度，两个操作可同一apply事务提交。标签沿用原生绑定text，换宽不改全文与字体角色。
5. **局部修改不变量**：先read(full)取目标ID、customData、points/angle、头型、stroke/background、锁定、标签与双向bindings；merge只改blockArrowWidth，保留所有无关字段。应用→保存后read，确认同ID、原路径/绑定/标签、实际宽值和描边独立，再当前revision check→PNG→实际看宽短/细长、头部、填充、净空与裁切→review。字段成功写入≠旧宿主已显示；不能隐藏不支持的实心头型或把check=pass当包络无重叠证明。
   若宽值和绑定读回正确，但PNG中箭尖/箭身相对真实端口出现随宽度变化的位移或标签遮罩异常，记录宿主渲染/导出兼容问题及具体IDs；不能把“同points”当视觉端点正确，更不能偷偷移动端口/拆绑定来补偿。字段与配色/尺寸可分别验证，剩余视觉问题不标completed。

能力来源：当前内核`packages/element/src/blockArrow.ts::getBlockArrowPolygon`、`shape.ts`的block分支、`packages/excalidraw/actions/actionProperties.tsx::actionChangeBlockArrowWidth`。Agent使用上述现有数据入口，不调用侧栏slider/修改currentItemBlockArrowWidth影响用户下一笔；不用重写renderer。


## 自定义固定圆角：不是只有round/sharp

矩形默认`{type:3}`使用自适应半径（当前内核默认上限32、小时按短边比例），因此容易显得圆。修改版`getCornerRadius`优先使用显式value，且矩形支持`roundType:"arc"`的圆弧而非默认二次贝塞尔：

```json
{"op":"create_shape","type":"rectangle","x":0,"y":0,"width":320,"height":160,"style":{"roughness":0,"roundness":{"type":3,"value":6,"roundType":"arc"}}}
{"op":"patch_element","target":"已有矩形ID","patch":{"roundness":{"type":3,"value":6,"roundType":"arc"}}}
{"op":"patch_element","target":"已有肘形箭头ID","patch":{"roundness":{"type":2,"value":6}}}
```

- value是画布坐标单位的半径，不是角度、百分比或PNG像素。普通独立节点矩形从6起，常用4–12按用途调整；**表格/寄存器字段单元格用roundness:null，不继承此圆角起点**，按[表格规范](capability-map.md#表格清晰表头与连续网格)形成连续网格。同类不同大小节点保持固定值；resize后读回value，不默认按宽高比例放大。整组原生scale可能有不同规则，读回再确认。
- type3是矩形等自适应族，type2是line/arrow/diamond比例族，type1是遗留；不是r值。`roundType:"arc"`仅确认矩形/iframe/embeddable该路径，不能推广成所有图元的圆角开关。
- 矩形尖角用`roundness:null`；正半径须有限，建议`0<r<=min(width,height)/2`且留实际内容区。不要因Bridge只检查finite就传负值/超大半径；ellipse本来是椭圆，不用此字段画圆角矩形。
- 普通折线的roundness会影响曲线形状；**肘形箭头**是另一条渲染路径，读取`roundness.value ?? 16`。因此null/sharp并不保证肘形转角为0；要硬直角用`{type:2,value:0}`，固定小转角用正值6等。短线段会限制实际可见弧度，不把value当保证的屏幕半径；block宽箭分支也不套用这条规则。
- `style.roundness`用于创建/节点局部style/profile.shape/profile.container/profile.edge；`patch.roundness`用于已有元素。它与edge同传时显式roundness优先，但后续set_arrow_style.edge会覆盖；不要只写顶层roundness或只给文字加roundness。原有用户形状不擅自全图换圆角。
- 真实PNG检查直角、小固定圆角与默认圆角，并对多尺寸/resize复核。圆角需保留绑定、文本内边距与连线端点；“圆角小”不等于连线可以穿入正文。

## Arrow特殊属性

| 属性/功能 | 真实入口/字段 | 限制与检查 |
|---|---|---|
| 箭头端点与头类型 | Bridge `set_arrow_style`/`arrow_style`；两种block类型按runtime集合；宽度走`patch_custom_data.merge.blockArrowWidth` | 保持原生绑定；宽度/头倍率/描边独立，完整包络须PNG复核 |
| 头部大小 | `customData.arrowHeadSize`，Bridge校验0.125–8 | 这是真实ymjr倍数，不等于像素宽度 |
| 特殊点拖拽约束 | `customData.fixedDragablePoints={dragablePointIndex,fixedPointsIndex,centerIndex}`，Arrow-Head-Resize Engine | 索引数组，-1表示末点；不是arrowHeadSize；必须与实际points一致 |
| 定长旋转 | `customData.fixedLength=true`，Fixed-Length Engine的handlePointDragging | 以局部[0,0]为基准保持拖拽半径；不是任意复杂折线路径总长度锁定 |
| 实时测量 | `customData.measure={ratio,unit}`，`plugin.measureEngine.updateMeasureText(elements,isLiveDrag)` | 代码测量首尾直线距离`hypot(dx,dy)/ratio`，并非折线路径长度；标签可能被复用/覆盖，不与业务箭头标签混用 |

已有非交互样式示例：

```json
{"op":"set_arrow_style","targets":["arrowId"],"endArrowhead":"block_arrow_outline","arrowHeadSize":1,"strokeWidth":2}
```

fixedLength/measure特殊Engine不在默认bundle内；按[script-execution](script-execution.md)发现并挂载宿主真实脚本。原定长/测量Action是浮动面板，不能在无UI自动等待。`Feature-Measure-Engine`直接维护文字/索引，使用前核对宿主版本与既有绑定，读回关系；未验证就不声称真实测量交互通过。

## Animation与演示

- **Arrow animation**：`animation/Feature-Arrow-Animation-Engine.md`读`customData.animation={type:"flow"|"dash"|"arrow",speed:number,color:CSS}`，Action仅是选线配置面板。Engine维护overlay canvas/RAF；PNG不保存运动。按实际speed范围/颜色配置，演示前后检查原箭头绑定和非动画内容。
- **Progressive drawing**：`Action-Progressive-Drawing-Animator.md`提供选中/全图逐笔、打字、播放暂停/停止/录屏模式。plugin `_ymjr_animator`存active/paused/progressMap；函数在Action作用域，未暴露MCP控制API。需要真实UI控制或用户授权改为非交互的本地脚本，不捏造`drawing_animation`。必须验证播放/暂停/停止与缓存恢复，不只截图第一帧。
- **Step appear**：`step-appear/Action-Step-Appear-Setup.md`沿选定引导线找实体并写`customData.appear={index}`，随后删除引导线；因此有明确删除副作用，只有该线被用户指定用于设置才运行。Engine基于hide逐步显示，需保留组和bound text同一index。PNG只代表当前步骤。
- 静态多页演示使用原生frame + drawing_present；动态演示和PPTX导出不是同一功能。没有真实视频/PPTX出口不能宣称已生成动画文件。

本包默认不部署上述animation/step-appear Engine。普通绘图不自动开启持续RAF/鼠标模式；用户要求演示再挂载，完成后按真实stop/disable恢复，不能通过Native CLI一次性script启动常驻动画。

真实smoke已观察Arrow animation overlay的像素hash与globalOffset跨RAF帧改变，调用`plugin["disable_ymjr.feature.animation-engine"]()`后overlay消失且loopId为null。逐笔/step-appear播放没有在本轮运行，不能把箭头动画证据覆盖这些独立能力。

## Export与其他软件

- PNG/SVG：现有MCP preview、EA createPNG/createSVG或Native CLI export；按明确文件/区域、资源和尺寸预算，实际看PNG。SVG/PNG是交付格式，不自动替换原图。
- **Anki**：`export/Action-Export-Image-To-Anki.md`生成选中元素SVG后浮动面板调用AnkiConnect，默认端口8765；真实payload为`action:"addNotes",version:6`，`notes`中deckName/modelName/fields/tags。原脚本写Default/Basic，不能代替用户所需deck/model。这是外部写入，需要用户明确导出授权、接口/字段正确与真实result确认；不自动创建卡片当smoke。
- **Eagle**：`Action-Export-Image-To-Eagle.md`纯图片用本机文件`/api/item/addFromPath`，混合图元用SVG dataURL的`/api/item/addFromURLs`；`Feature-Export-Eagle.md`也提供右键项。真实token从用户私有配置读取，不能把脚本里硬编码示例token复制到Skill或报告。HTTP ok不等于库item写入已核对，需真实返回/目标库确认；用户明确授权才发送。
- Embeddable DOM导出依赖`Feature-Export-Embeddable`真实capture；网络或DOM资源失败应incomplete，不用空边框冒充。外部应用联动不在drawing_preview的默认副作用内。

来源（相对绘图脚本目录）：`distribute/*`、`arrow/*`、`animation/*`、`step-appear/*`、`export/*`；Bridge `distribute/set_arrow_style`。接口版本和外部应用条件须在任务环境实际发现。
