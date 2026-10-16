# 交互、导航与查阅能力

这些能力大多由宿主绘图脚本的常驻Engine拦截鼠标/键盘/缩放/渲染Hook实现。写入customData只是配置，不自动挂载Engine。静态PNG不能证明交互生效。

## 能力矩阵

| 能力 | 真实持久数据/入口 | Agent可用路径 | 主要限制 |
|---|---|---|---|
| Hover | `customData.hover`，包含`id`数组、`pointer`和可选`shadow`；Hover Engine处理`handleCanvasPointerMove` | 优先`set_feature shadow`的`hoverShadows/hoverPointer`；没有覆盖的hover目标用受信脚本 | 依赖Hover Engine；PNG只看静态shadow，不证明鼠标触发 |
| Line highlight | `customData.highlightLine=true`；`line-highlight/Feature-Line-Highlight-Engine.md`响应pointer move/up并渲染粗色光晕 | `patch_custom_data`或受信脚本给明确line/arrow及绑定节点写标志，再读回 | 没有line_highlight Feature；原Engine把getSelectedElements结果当单个element，运行时若返回数组就不会激活，必须实测/修宿主版本，不能宣称已通过 |
| Zoom hide | `customData.zoomHide=[minZoom,maxZoom]`；Engine按`appState.zoom.value`把`customData.hide`切换为true/false | `patch_custom_data`或受信脚本写区间，按需挂载ZoomHide Engine；不要手动长期写hide覆盖Engine | 直接updateScene中的zoom.value已实测为0.3/0.8；Wheel Hook在不同版本的单位另需核对，不把UI百分比数字直接填入 |
| Detail | Target:`customData.detail={status:"show"或"hide",ids:[child IDs],relative:boolean}`；Child:`customData.isDetailOf=targetID` | 用受信脚本绑定，或`patch_custom_data`配置后挂载Detail Engine；ids必须是同一画布实际ID | 点击target右上角图标切换；relative为拖拽时子元素跟随；MCP没有自动布局/绑定推断 |
| Checkbox | Text的`customData.isCheckbox`，文本保持`- [ ]`/`- [x]` | 已有Bridge `set_feature`：`{"op":"set_feature","feature":"checkbox","targets":["textId"],"config":{"checked":true,"addMarkdownPrefix":true}}` | 真实切换是Shift+点击；必须挂Checkbox Engine；PNG只证明当前勾选外观 |
| Layer | `customData.layer="Architecture"`、可选`customData.hide`；Layer Engine维护active/show/selectable状态 | 已有Bridge `set_feature layer`：`config:{name:"Architecture",hidden:false}`；切换显示/选择层仍是Layer Action/UI或受信脚本 | hide是Engine状态，切换后需读回；静态PNG不提供用户层面板 |
| Outline | `customData.titleLevel`/`outlineLevel`，或`customData.outlineText`；也可直接使用frame | 受信脚本或patch_custom_data设置真实标题metadata，再启用Outline Engine/Action；Engine会按层级或编号排序 | 已明确frame/编号/层级时直接选对应模式；只有语义歧义才问，不把普通样式选择交给用户 |
| Thumbnail | Thumbnail Action在Excalidraw view中创建缩略图Canvas导航面板，Engine挂载`renderStaticScene`和鼠标事件 | 用URI触发已注册Action，或宿主受信脚本调用已安装Action；不把面板当画布元素 | 是宿主UI，不属于scene，不进入PNG；需要真实view和UI验证 |

## 真实字段与局部配置

### Detail

绑定时不要复制完整scene JSON。先读target和child的精确ID，执行等价的受信EA更新：

```javascript
const target = ea.getElement(targetId);
target.customData = {...target.customData,
  detail: {status: "show", ids: childIds, relative: true}
};
for (const id of childIds) {
  const child = ea.getElement(id);
  child.customData = {...child.customData, isDetailOf: targetId};
}
await ea.addElementsToView(false, true, true);
```

展开/收起由`customData.detail.status`和子元素`customData.hide`控制；Engine还负责图标、点击拦截和拖拽闭包。删除/移动child前先解除detail关系。

### Zoom

```json
{"op":"patch_custom_data","target":"elementId","merge":{"zoomHide":[0.5,1.2]},"remove":[]}
```

这里只是安全元数据示例；只有ZoomHide Engine运行时才有动态效果。范围外Engine会写`hide:true`，范围内写回`false`。禁止在每次PNG前手动清除hide，这会破坏用户运行时配置。

### Outline

```javascript
const e = ea.getElement(textId);
e.customData = {...e.customData, outlineText: "2.1"};
// 或使用 titleLevel / outlineLevel（二者不要同时写）
await ea.addElementsToView(false, true, true);
```

Outline Engine的三种真实模式是`frame`、`text - level`、`text - text`。它按`outlineText`数字段或title/outline level计算显示编号；这是查阅导航元数据，不等于把“2.1”写进原始文字。

## 运行顺序

1. `drawing_context(bind)` → `drawing_read(detail="full")`，获取真实IDs和当前revision。
2. 通过MCP adapter或受信宿主脚本配置元数据；每批写后读回新revision。
3. 确认对应Engine已挂载：读取宿主Feature状态/EA_Core hooks，或者在受信宿主中执行明确Engine脚本。一次性CLI脚本结束后Engine不会持久运行。
4. 真实交互测试：hover移入/移出、Shift+点击checkbox、点detail图标、滚动zoom、打开thumbnail并点缩略图、切换outline/layer导航。
5. 另行做`drawing_check`与PNG；报告PNG与交互验证是两类证据。

## 当前运行验证与宿主限制

隔离的真实ymjr 2.27.3-1中：Checkbox Shift+点击、selection工具下Hover状态、Mindmap布局与图标折叠、updateScene缩放跨区间hide切换已实际观察；Layer元数据已保存。Detail图标显示但本轮真实点击未观察到状态改变，不能称折叠通过。Outline Engine可生成编号数据，但原Action报ReactDOM未定义（宿主需真实React/ReactDOM上下文）；Thumbnail面板已打开，本轮点击未观察到视口变化，导航尚未验证。Line-highlight在此版本getSelectedElements确实返回数组，原脚本的单元素判断不兼容。上述限制应在任务环境检查/修对应宿主脚本，不能通过“写了字段”掩盖。
Thumbnail原Engine的DOM listener把`handleMouseEvents(event,ea,api)`直接传给addEventListener，浏览器只传event，函数中的ea/api没有上下文；拖红框导航需实际修正对应宿主版本的闭包绑定，不把仅面板存在称导航通过。当前测试没有修改用户原Engine。


来源（相对绘图脚本目录）：`hover/Feature-Hover-Engine.md`、`Action-Toggle-Hover.md`；`line-highlight/Feature-Line-Highlight-Engine.md`；`zoom/Feature-Zoom-Hide-Engine.md`；`detail/Feature-Detail-Engine.md`和`Action-Toggle-Detail.md`；`checkbox/Feature-Checkbox-Engine.md`；`layer/Feature-Layer-Engine.md`；`outline/Feature-Outline-Engine.md`；`thumbnail/Feature-Thumbnail-Engine.md`。交互执行边界见[script-execution](script-execution.md)。
