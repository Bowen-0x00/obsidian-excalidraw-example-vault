# 原生图元与 Feature 操作参考

入口：`drawing_primitives(context_token, items=[...], style="handdrawn"或原生属性对象)`生成真实operations；再`drawing_apply`。规划不提交画布。字体与文字尺寸调用正在运行的EA测量；不得按字数猜宽。真实输出需check→PNG→实际看图→review。

## draw：自由笔画，不是roughness开关

```json
{"kind":"draw","id":"annotation","x":20,"y":30,"points":[[0,0],[10,-8],[28,-10],[45,2],[70,0]],"pressures":[0.2,0.5,0.7,0.6,0.2],"simulatePressure":false,"style":{"strokeColor":"#2563eb","strokeWidth":3}}
```

通过本地Excalidraw `convertToExcalidrawElements`→`newFreeDrawElement`原生constructor生成freedraw。points是局部坐标，可负；pressure必须0–1且每点一个值。没有pressure时simulatePressure=true。Agent提供笔画意图与点列，执行层生成ID/version/seed，不要拼完整freedraw JSON。自由笔画可编辑点和笔刷属性，文字注释仍优先用可搜索原生text。

手绘风格另用named style `handdrawn`，保持确定性布局/绑定，不默认把所有节点变成freehand。

## 多边形

```json
{"kind":"polygon","id":"hexagon","x":0,"y":0,"sides":6,"sideLength":70,"rotation":-90,"label":"六边形"}
```

或明确`points:[[0,0],[180,0],[140,90],[30,120]]`；执行层闭合首尾，原生类型line+polygon=true。

来源：绘图脚本`generate/Action-Generate-Polygon.md:75–129`。原Action的自定义边长按等转角走前n−1边再闭合，并不能保证最后边长满足输入。本接口不伪称支持任意给定边长约束；非正多边形用实际vertices，regular用真实几何边长公式。

## 立方体/长方体

```json
{"kind":"cuboid","id":"memory-block","x":20,"y":20,"width":160,"height":100,"depth":55,"angle":35,"dottedBack":true,"label":"存储阵列"}
```

适配`Action-Generate-Cuboid.md:85–125`：原生正面矩形+顶部/侧面闭合line；背部可选dotted三条线；所有成员group。x/y是整个投影区域左上，正面有深度偏移；外部连接优先绑定正面body。angle单位degree，上右投影。不是立方体整图SVG或PNG。

## 四向大括号

```json
{"kind":"brace","id":"grouping","side":"bottom","targets":["真实节点ID1","真实节点ID2"],"gap":10,"label":"数据通路"}
```

或`box:{x,y,width,height}`或明确x/y/length。side=`top/bottom/left/right`。来源四个绘图脚本`brace/Action-Add-*-Brace-Path.md`，复用Q/L路径，top/left的负坐标整体归一化到viewBox，不只改carrier bbox。使用单个原生line+svgPathShape/svgViewBox，保持shape编辑与样式；不是图片。

任意SVG path符号/可复用组件的通用流程见[svg-components](svg-components.md)：复用真实Digital/Microarch生成脚本，DOM测量、归一化校验、源viewBox与目标尺寸分离、line carrier和独立文字/anchor分组。不是给drawing_primitives添加不存在的kind=svg；普通path使用drawing_apply的create_svg_path。

## callout

```json
{"kind":"callout","id":"note","x":0,"y":0,"width":400,"type":"warning","title":"注意","body":"这段完整中文说明会按实际字体测量换行。","colorType":"alpha","shadow":false}
```

复用`Feature-Callout-Engine.md`真实矩形/36px表头、图标、颜色、body定位hook；正文是原生bound text。type及颜色范围以runtime feature spec为准；title保存到实际`customData.callout.title`，不是在自动表头上再叠一段假标题。

来源：`callout/Action-Create-Callout.md:52–88`及`Feature-Callout-Engine.md:96–240`。不执行Action的suggester UI，不默认加巨大相对阴影。

## 代码高亮

先按[typography](typography.md)从当前宿主集合选出并验证`codeFamily`；它是Agent工作变量，不是固定字体名或新MCP字段。下面是构造item的JavaScript示意，不可把变量名作为family字符串提交：

```javascript
const item = {kind:"code",id:"python-example",x:0,y:0,text:"def add(a, b):\n    return a + b",language:"python",theme:"atom-one-light",fontFamily:codeFamily,fontSize:18};
```

原生text+codeHighlight Engine，source保持完整。**不插入换行改变程序源码/缩进**；长行增加展示宽度或按用户已提供换行。highlight不是执行代码。编辑用set_text后再check/PNG；language/theme按runtime配置校验。
显式传所选fontFamily，不依赖primitive历史默认名称；等宽、代码符号覆盖与手写是不同维度。若无可确认的代码候选，保留源码并报告缺口，不用数码显示体/空格补偿冒充代码等宽。样本测量不证明全部字形未fallback。
本参考对应的Engine内置主题为atom-one-light和atom-one-dark；先确认本机runtime配置，其它theme必须有真实配置，不接受“名字看起来合法”就当有配色。

来源：`code-highlight/Action-Toggle-Code-Highlight.md:99–130`、`Feature-Code-Highlight-Engine.md`；避免语言识别不明时弹UI，Agent明确language。

## checkbox

```json
{"kind":"checkbox","id":"check-done","x":0,"y":0,"text":"完成结构检查","checked":true}
```

原生text，set_feature checkbox维护Markdown `- [x]`/`- [ ]`前缀及customData.isCheckbox。改变checked使用同一text ID的set_feature，不重建。不能把checkbox误塞到rectangle，不能只画一个不可交互勾图标。

来源：`checkbox/Action-Toggle-Checkbox.md:89–117`、`Feature-Checkbox-Engine.md`。真实交互是先hover命中文本，再Shift+点击切换；PNG只证明当前状态。需要真实view验证与读回，不能把metadata存在称为交互通过，详见`interaction-navigation.md`。

## 高级连接
CPU/硬件数据通路先读[microarchitecture](microarchitecture.md)，不能只用默认side中心连接所有信号；按实际符号stub/RF数据与控制端口分别指定fixedPoint、命名stub和反馈track。primitive connection是几何连接器，不是电气端口/总线/流水级自动布局器。

```json
{"kind":"connection","id":"data-edge","from":"真实source ID","to":"真实target ID","routing":"orthogonal","start":{"anchor":"right","fixedPoint":[1,0.3]},"end":{"anchor":"left","fixedPoint":[0,0.7]},"label":"数据","startArrowhead":null,"endArrowhead":"triangle"}
```

routing=`straight/orthogonal/curve`；代码读取当前精确节点geometry，正交路径避障；显式waypoints使用scene坐标。始终维护start/end与目标boundElements双向关系，标签原生绑定。native head包括arrow/bar/circle及outline/triangle/diamond；PPT实心block_arrow与轮廓block_arrow_outline先核对runtime集合，箭身宽按refs补patch_custom_data.blockArrowWidth（不是strokeWidth/几何width），细节见[箭头尺寸](layout-export-animation.md)。
微架构信号默认只允许轴向直连或正交折线。低层connect缺省elbowed=false且无waypoints时直接连接两点，不会自动避障；两端不对齐须显式计算正交拐点。routing=orthogonal/flag并非审计替代品，应用保存后读full逐段核对世界dx/dy及首末端口方向，详见[microarchitecture](microarchitecture.md)。
按[箭头语义与固定圆角](layout-export-animation.md)选择头型/线身，不默认所有关系arrow；本例triangle用于数据流，不推广到UML。profile只提供基础线型，不能代替每条关系的start/endArrowhead；固定肘形radius通过实际生成的connect.style.roundness或按refs patch，不把routing=curve当圆角。

来源：`connection/Action-Advanced-Connector.md`，不是调用其交互面板。曲线精确碰撞检查尚有unknown，必须明确限制；不能用“curve看起来绕开”冒充硬检查通过。library line素材先用返回anchorElementId，不能直接绑定不支持的line target。

两根业务线相交时使用原生`customData.lineCrossings`，不手画桥弧/白色矩形遮罩；arc/gap表示不连接，dot只作已确认连接的视觉标记，仍保留真实绑定。输入路由与逐IDpatch范例见[layout-export-animation](layout-export-animation.md)的Line Crossings；不要假设primitive连接或diagram.edges会转发任意customData。

## 合法包含与叠放

多个面组成一个cuboid、一个库item的装饰/框/文字属于明确construction unit，metadata记agentPrimitive/agentLibrary.instanceId。只有单位内部叠放合法；不同单位之间仍检查，不能仅因groupIds相同就关闭碰撞检查。异常或复杂几何unknown不能冒充通过。
