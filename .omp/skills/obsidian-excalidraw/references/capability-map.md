# 绘图脚本能力地图与缺口

这是对宿主绘图脚本和当前Bridge的对照，不把“能设想”写成现有API。本文脚本路径相对插件配置的绘图脚本目录；默认bundle只部署bundle.json列出的Engines，其他可选脚本须先发现、审查再运行，用户自定义脚本与设置保持不变。

| 能力组 | 之前Skill缺口 | 当前推荐入口/参考 |
|---|---|---|
| 硬件微架构/数据通路 | 普通rank＋矩形标签无法保证硬件表达；失败后曾降成阶段说明 | **[microarchitecture](microarchitecture.md)**：先部件/端口/信号/时序骨架，原生/库符号与固定区域，禁止降级/重复compose，硬件语义＋实际可读PNG验收 |
| 启动视觉偏好 | 默认风格未与用户确认、配色/字体/字重缺属性映射 | [diagram-recipes](diagram-recipes.md)：真实Agent选择UI一次询问未定项，严格hex范围、明暗/灰度、字体发现及原生属性落地；不是新MCP弹窗 |
| 语义箭头/固定圆角 | 仅枚举头型、round/sharp缺少选型和value | [layout-export-animation](layout-export-animation.md)：数据流triangle/PPT block/UML区分、宽箭身/绑定，矩形type3/value/arc与肘形type2/value；Bridge0.13.3修复旧set_arrow_style头型写空 |
| 图片获取/插入 | 只提image类型，没有自然语言找图→附件→原生插入流程 | [images-assets](images-assets.md)：真实来源、许可、资源解码、宿主附件，EA/addImage或MCPcreate_image |
| SVG path组件 | 只写brace/用户库导入，遗漏通用路径符号制作 | [svg-components](svg-components.md)：两个Digital生成脚本、DOM归一化、line载体、组件组和入库边界 |
| 文字/公式混排 | 只写纯LaTeX能力，普通text中的`$…$`不会自动解析 | [visual-content](visual-content.md)：复用latex/Action-Extract-Latex，选真实text；原文副本转换、group/frame/绑定恢复，缺宿主入口时现有text+create_latex组合 |
| Mindmap | 未说明父子/根ID、布局与折叠、Markdown导出 | [special-diagrams](special-diagrams.md)：现有mindmap Feature、实际MindmapAPI、open/close契约 |
| WaveDrom | 已捆绑Engine但没有波形工作流 | special-diagrams：透明rectangle+JSON/JSON5源，set_feature wavedrom，真实PNG |
| Git/GIF | git未发现专用脚本；gif实际另有Engine但未说明 | special-diagrams：Git只读历史→原生关系图；GIF多帧资源与step UI |
| Hover/checkbox/layer | 已有适配器但实际互动步骤不清 | [interaction-navigation](interaction-navigation.md)：Shift点击/状态、hover目标、layer过滤 |
| Line-highlight/zoom/detail/outline/thumbnail | 原宿主Engine或UI，不在默认MCPFeature中 | interaction-navigation：真实字段、挂载、运行限制，不造tool |
| Shadow/callout/code highlight/rich text/gradient | 简略提及，参数单位与状态/来源不清 | [visual-content](visual-content.md)和native-features：受控配置、源码与PNG |
| List/bullet | 只提演示页bullet，遗漏Smart List与序号放置 | visual-content：渲染型list和椭圆+bound text的bullet区分 |
| Distribute/arrow | 基础API存在，但组闭包、特殊拖拽/定长/测量缺指引 | [layout-export-animation](layout-export-animation.md)：两种算法差异、真实customData、交互验证 |
| 整组旋转/缩放 | 逐项angle/width/height不等于共同中心变换 | layout-export-animation：Bridge0.13.0 rotate/scale_selection复用真实手动入口，原生文字/点列/关联维护；宿主特定Hook边界 |
| 原生走线交叉Line Crossings | 原先可能手工白色遮罩/小弧模拟 | layout-export-animation：line/arrow customData.lineCrossings arc/gap/dot/none，create_linear/connect/逐IDpatch；无需Engine，T分支PNG缺口明确 |
| Animation/step appear | 只支持静态frames，缺动态图展示 | layout-export-animation：flow/dash/arrow、逐笔播放与分步hide，真实停止清理 |
| Export联动 | 只写PNG反馈，没覆盖Anki/Eagle副作用 | layout-export-animation：真实外部应用入口/授权/结果，不擅自发送用户数据 |
| 脚本执行 | URI开发能力此前是独立导出文件夹 | [script-execution](script-execution.md)：Skill内的统一可信URI/EA/Engine路径 |

## 额外重要能力：保留已有机制，按需发现

- **Table**：新版优先[原生表格规范](table-native.md)：发现`nativeTable.callable`后通过`drawing_table`使用宿主八套主题、五种边框模板和schema-v2语义单元格；配套宿主仍是开发构建，不能假称已发布。旧Scripts2 Table Engine、Bridge `create_table`与DSL表格保持旧契约，不自动支持theme字段。新旧入口明确区分，不为展示新版效果逐格模拟。
- **Swimlane/ECharts/LaTeX**：已有主Skill流程及adapter，继续按runtime discovery执行。用户称swimeline时保留意图，实际机制为swimlane/isContainer；ECharts 1.3.0的类型、结构化options与编辑往返见[visual-content](visual-content.md)，不能把UI枚举等同Bridge枚举；LaTeX需真实Extras MathJax。
- **Link/follow**：`link/Feature-Link-Engine.md`处理onLinkClick、同文件`#^group=...`跳转及历史，`Action-Return-Link-Origin.md`回退；`follow/Action-Follow-Arrow-Forward/Backward.md`按实际绑定导航。原生link可以通过已有patch_element设置，但增强导航需Engine和真实view；不要为消除导航问题删除业务边。
- **No-bind/advanced connector**：`connection/Action-Toggle-No-Bind.md`是面板配置nobind，和显式connect/rebind操作不同。用户要禁止吸附时读实际字段/内核识别，不默认禁用所有绑定；连接优先native-features高级连接。
- **Dynamic library/calendar**：`library/Action-Dynamic-Library.md`、`Feature-Library-Engine.md`和`Feature-Calendar-Engine.md`。本包库API已发现dynamic/installed源，素材metadata/catalog仍由用户维护；不是联网下载库或通用日历服务。
- **Geometry recognition/Boolean operations**：`recognize/Feature-Shape-Recognize-Engine.md`和Action通过数学转化识别笔画；`generate/Action-Boolean-Operations.md`/Downloaded版可改变原元素。Bridge只发现Boolean runtime，没有semantic boolean_operation；不为了自动绘图擅自执行破坏性转换。用户请求才用实际宿主Action/可信API，原输入保留备份。
- **Clipboard/paste/text**：Paste Engine、Markdown Table Paste、Text Render/Shortcuts与部分格式Action各有作用。Agent改源码/文本用已确认的style/partial ranges，不能凭肉眼估字宽；自定义字体先发现。不要借剪贴板把用户无关数据发给外部服务。
- **Select/size/space/smart-art/tag/reminder/attachment**：真实Action提供选取、缩放、插空、联动、标签、提醒和附件打开。任务确需时按源脚本检查目标集合、UI依赖与写入副作用；不是当前Bridge已有通用tool。普通排版优先明确IDs的align/translate/resize，不自动修改用户提醒或文件标签。

## 表格：清晰表头与连续网格

适用于保留站、寄存器状态、队列、对照表和普通数据表。它们不是一组独立圆角卡片，**不要继承普通节点profile的自适应大圆角**。

配套原生宿主可用时，**先使用`drawing_table`和宿主主题／边框模板**，以下手工规范只用于旧表格与用户明确要求的局部定制；不要将其实现为第二套模板引擎。旧表格迁移或混合所有权编辑不在本次新工具契约内。

- 所有内部单元格显式`roundness:null`、`roughness:0`、实色填充，网格从约1场景单位细线开始；同列边界、同行基线严格对齐，相邻格无卡片间隙。外框也优先直角；用户确需圆角时仅考虑整体外轮廓，不给每格四角挖缺口。
- 表头和正文有清晰层级：同一语义色的深色表头＋浅色/白色正文，表头文字选足够对比的颜色。例：表头`#475569`/字`#FFFFFF`，正文`#F8FAFC`/字`#16324F`；保留站可用紫系、寄存器可用青系。只是非strict起点，不覆盖用户指定色板；不随机逐格染色。深色主题同样检查对比，不能机械套白底。
- 标题放在表上方，预留真实测量后的净空，不挤进第一格；表头行是字段名，正文行是状态/值。`Tag / Busy / Op / Vj / Vk / Qj / Qk`各占独立列，不把整行写进一个长标签。
- 先用实际family/字号测量各单元格。每列宽由本列最长内容＋左右padding决定，每行高由最高内容＋上下padding决定；常用水平8–12、垂直5–8作为起点，列标题不能被裁切。不要按字符数估宽，不为塞下表格压小字；长中文先合理换行/扩列，数值按需要右对齐，短状态可居中。
- 当前`create_table`接收统一`cellWidth/cellHeight`与整表shape style，**没有headerStyle/columnWidths等承诺**。先传`style.roundness:null`；返回真实cell refs后，在同revision批量patch表头的`backgroundColor`，并更新其真实bound text的`strokeColor`。不要只改矩形strokeColor就以为字变白，也不要手填boundElements。
- 需要异宽列时，可依据测量结果对已有单元格批量调整x/width并保持bound text、table metadata、组和root；必须检查读回的文字尺寸及列边界。使用原生矩形+bound text自行组合也可，但没有Table Engine元数据时只称“可编辑图形表格”，不假称行列增删/联动已具备。
- 现有表格小改保留ID、root/row/col/rowNum/colNum、分组与引用；不为改圆角/表头色重建。用户尚未通知的Table能力不提前假设，后续Engine更新后再按真实契约调整。
- 验收看真实PNG：表头一眼可辨、网格连续、全文未溢出、边框不穿字、列宽合理、有效字高可读。已有Tomasulo DSL的效果来自原生直角cell＋深浅分层，并不依赖新的表格渲染器；正式图仍走check→PNG→review。

## 已运行与未运行分开

代表性实际smoke：网络官方图片→附件→原生image→PNG；WaveDrom、callout、code highlight、shadow/checkbox图；checkbox真实Shift点击、hover、mindmap布局和折叠、zoom跨区间hide。箭头动画overlay像素跨帧变化与disable停止已实际观察。其余Engine/外部应用执行按环境条件说明；不声称全部脚本都已跑通。

运行中发现的真实宿主限制记录在interaction-navigation；这些是用户代码的情况，不应为了让Skill看起来“全支持”掩盖。默认不修改用户绘图脚本，不自动授信/autorun，也不把缺入口写成已实现MCP。
