# 视觉效果、列表和常见元素

## 已有Bridge适配器

### Shadow

目标类型任意，Bridge `FEATURE_SPECS.shadow`支持`set_feature/clear_feature`，存储`customData.shadow`和`customData.hover.shadow/pointer`，需要Shadow Engine：

```json
{"op":"set_feature","feature":"shadow","targets":["shapeId"],"config":{"shadows":[{"shadowColor":"rgba(0,0,0,0.3)","shadowBlur":"12px","shadowOffsetX":"6px","shadowOffsetY":"8px"}],"hoverPointer":true}}
```

`shadowColor`可CSS色或相对亮度数值；blur/offset的无单位数是相对比例，只有`22px`这类字符串是绝对像素。不要用复制偏移的多边形假造阴影。通过`set_feature`，不要直接写gradient/document/echarts等受限customData；Bridge会拒绝不安全字段。阴影静态效果可随PNG检查，hover shadow必须另做鼠标验证。

### Callout

目标是rectangle，Callout Engine根据`customData.callout`渲染标题栏、图标和bound body text。Bridge适配器：

```json
{"op":"set_feature","feature":"callout","targets":["boxId"],"config":{"type":"warning","colorType":"alpha"}}
```

真实type包括`note/info/tip/success/failure/warning/error/quote/cite/example/danger/bug/question/abstract`；先以runtime feature spec为准。`title`不是随便叠加一个文本，复杂标题/正文须使用Engine的真实绑定规则或`drawing_primitives kind=callout`。Edge/外部连接不要假定Callout header是正文容器。PNG可证明当前渲染，不证明编辑时避让。

### Code highlight

目标是text，source文字保持原始换行与缩进：

```json
{"op":"set_feature","feature":"code_highlight","targets":["codeTextId"],"config":{"language":"python","theme":"atom-one-dark","embedFont":true,"fontSize":16}}
```

Bridge存储`customData.codeHighlight`，Engine渲染高亮；theme/language必须是宿主真实配置，不因字符串看起来合法就当支持。不要为适配窄框删减源码；先用native `drawing_measure`，调整容器/字体/局部PNG。高亮是渲染，不执行代码；PNG对可读性需实际查看。

### Gradient 和富文本

已有Bridge `gradient`适配器仅接受direction `horizontal/vertical/diagonal/radial`和至少两个`{offset,color}` stops，拒绝raw JavaScript gradient；`rich_text`支持全局bold/fontWeight/color/gradient及局部bold/color，不支持partial_gradient。旧样例中的`customData.gradient`代码字符串不能直接回写。

## ECharts 1.3.0：数据图与编辑往返

先发现宿主实际Engine版本和运行状态。绘图脚本目录下`echarts/Feature-Echarts-Engine.md`与`Action-Echarts-Manager.md`已更新到1.3.0；**源码更新、包内受管副本、已加载Engine是三件事**，旧bundle不能仅因目录中另有新脚本就算已升级。按真实命令手动挂载，禁止改授信/autorun或盲目复制覆盖用户脚本。

### 类型、数据与图型选择

已发布的16个示例是：柱状、水平条形、折线、面积、多系列分组、堆叠柱状、堆叠面积、柱线混合双Y轴、饼、环、玫瑰、数值XY散点、雷达、漏斗、仪表盘、自定义JSON热力图。**不是16个不同的type枚举**：可视表单有12种基础type（`bar/horizontalBar/line/area/pie/donut/rose/scatter/mixed/radar/funnel/gauge`），另有`custom`；分组/堆叠是系列配置，热力图示例走custom，不虚构专用热力图表单。

- 比较类别用bar/horizontalBar，长类目优先水平条形；时间趋势用line/area；组成累计用stacked；独立量纲用mixed并清楚标左右Y轴；相关性用数值XY而不是把X当等间隔类目。
- 占比用pie/donut/rose，阶段转化用funnel，多维同尺度比较用radar，单指标进度用gauge。只按用户数据和目的选择，不为了展示16种能力把同一数据重复画满画布。
- Engine的规范数据为`schemaVersion:2`：`labels`、`series:[{name,values,type?,color?,yAxisIndex?}]`、散点`xValues`；另有`stacked/dataZoom`、轴标题、`valueSeriesIndex`、`gaugeRow/gaugeMin/gaugeMax`等。多系列表格/CSV/Excel TSV支持表头、引号和系列命名；非法数值报错，不替成0。
- 雷达至少三个维度且非负；饼/环/玫瑰/漏斗值非负且至少一个正值；仪表盘上下限有序且所选值在量程内。未知量纲/范围不猜造。完整ECharts options可走custom，不能传可执行formatter函数字符串来绕过受控JSON。

### Agent调用与UI边界

当前Bridge的`set_feature echarts` type仍是`bar/line/pie/scatter/custom`。高级图使用**`type:"custom"`＋真实完整options**；不要把`horizontalBar/mixed/radar`等UI枚举直接当旧Bridge可接受参数，也不要对普通draw/表格需求默认使用ECharts。

```json
{"op":"set_feature","feature":"echarts","targets":["实际矩形ID"],"config":{"type":"custom","options":{"animation":false,"legend":{"data":["收入","利润率"]},"grid":{"left":50,"right":55,"top":40,"bottom":40},"xAxis":{"type":"category","data":["Q1","Q2","Q3"]},"yAxis":[{"type":"value","name":"收入"},{"type":"value","name":"利润率 %"}],"series":[{"name":"收入","type":"bar","data":[120,160,210]},{"name":"利润率","type":"line","yAxisIndex":1,"data":[18,22,24]}]}}}
```

目标是保留数据的原生rectangle及`customData.echarts`，不是整图PNG。Bridge将options存为`echarts.value` JSON字符串；它不调用可视表单，也不提供`rawData`编辑模型参数。可视Engine保存`{type,value,rawData}`，`rawData`是规范模型；`readStoredChart`优先读rawData，没有时把完整旧options作为custom保留，不只抽取series[0]。通过Bridge写完整options可在JSON编辑器往返，但不承诺自动恢复为可视多系列表单。不要手拼rawData元数据冒充已有MCP接口。

用户可双击图表或运行Manager原地编辑；实时预览、表格/批量文本切换、深浅预览、数据缩放、量程/双轴等由真实编辑器实现。`applyChartData`用独立EA工作台，更新已有元素ID；源文字只在成功提交中删除，取消保留。PNG只能证明静态图，不证明双击、hover图例或dataZoom交互已验收。

### 导出与证据

1.3.0挂载时向document注入离线ECharts；`renderCustomDocument`不依赖旧的contentEl注入路径；`handleSvgRender`从元素自己的options生成SVG，不必等画布iframe存在。仍按当前revision导出，核对`complete/resourceIssues`并实际看PNG中的系列、坐标、图例和量纲；不能把“接口callable/返回边框”当内容完整。Engine和Bridge各有导出路径，不混称一种接口。

本次已读取源码、16图总览及实际编辑器截图；既有16示例包含原生源及渲染结果，示例数据是合成数据，不是业务事实。旧DSL实验的空框是当时宿主状态的历史失败，用户已修复，不再作为当前能力限制；其历史记录不改写成当时通过。新宿主/旧受管副本仍需按真实版本与PNG判断，不能继承一次修复为永久成功保证。
本轮另在真实宿主用当前Bridge的`type:"custom"`绘制柱线双Y轴与热力图，两者PNG资源完整并已实际查看；它们和33格原生表格在同一验收画布。没有把16个既有示例全部重新运行，也没有把UI截图当本轮完整交互测试。

来源：`normalizeChartData/parseTextToData/validateChartData/generateEchartsOptions/readStoredChart/applyChartData/handleSvgRender/mountFeature`；示例发布清单`temp/echarts-1.3.0-showcase/asset-manifest.json`。这些是宿主源码/示例证据，不是新增MCP工具。

## 文字与行内 LaTeX：必须显式转换

普通`create_text/set_text/label`与`rich_text`不是MathJax渲染器；例如`运行极值 $m_{new}=\max(m_{old},S_i)$`直接传进去只会显示源码。新图在内容规划时就识别公式，不等到交付才把它当“文字样式”。用户要求展示源码、代码示例、货币或转义美元符号时保留字面内容。

### 复用真实宿主脚本

来源是绘图脚本目录下`latex/Action-Extract-Latex.md`，frontmatter名称“提取文本内的 LaTeX”（已读版本1.0.0），不是默认bundle中的Engine或新的MCP工具。先根据宿主`settings.scriptFolderPath`发现/读取文件，不硬编码个人机器路径；脚本存在不代表当前vault已经注册或已执行。

代码确认的行为：
- 只处理`ea.getViewSelectedElements()`中的**text**，选中矩形并不等于选中其绑定文字。正则为`/(\$\$[\s\S]+?\$\$|\$[\s\S]+?\$)/g`；去掉一层/两层delimiter后调`await ea.addLaTex(x,y,tex)`，跳过空公式。
- 按现有文本的实际`\n`拆行，普通片段用`ea.addText`，横向推进用Canvas `measureText`；公式以`fontSize/15`缩放，并按当前字号垂直居中。`$$…$$`在这个脚本里**仍沿当前行排版**，不是自动独立居中的Markdown display块。
- 每个源text在末尾由`ea.deleteViewElements`删除；生成新的text/image ID。`ea.clear()`仅清EA工作台，不是清空画布。公式是插件原生LaTeX image资源，源TeX由`imagesDict[fileId].latex`及保存文件的`Embedded Files`保留；`customData.latex:{scale:…}`本身不是完整源公式。

不要照抄frontmatter的“无依赖/完美继承/全面兼容”作运行保证：
- 实际仍依赖宿主可用的Extras MathJax；先查`latex.available`，失败保留原文并报告，不能因脚本跳过失败公式就删掉原标签。
- 这个正则没有转义美元/代码块/货币语义处理，也不校验所有delimiter配对；`$$`空串、跨行、嵌套美元先核对意图，不全图盲转。不要在公式源码中做普通文字自动换行，避免把`\frac`等命令切断。
- 仅按已有`\n`推进，**不会按转换后的公式宽高重新自动换行/加行距**；分式、求和、大括号等高公式可能挤邻行。固定宽度、原来的居中/右对齐、旋转、bold/partial style不是完整保留承诺。脚本设置文字strokeColor不保证MathJax公式同色；已观察到蓝色文字配黑色公式，按最终用途看PNG，不假称颜色继承通过。
- 没有显式迁移源文字的groupIds/frameId/containerId、箭头标签或链接；没有创建整个混排块的group。**禁止直接对已绑定标签/箭头标签/锁定元素批量运行后假称身份与绑定保持。**
- `deleteViewElements`及末尾`addElementsToView(false,false,false)`没有await；Action结束/Notice/URI退出不是保存回执。一次性Native CLI会清理所属EA，不能把这个原脚本未经生命周期处理直接当可靠CLI任务；不改用户源脚本，必要时经授权复用核心API并await提交/保存。
- 末尾`newElementsOnTop=false`会把新片段置于现有元素后方；在填色容器中，公式与文字可能**已存在但被底板盖住**。frame归属/group正确、几何check=pass也不能证明可见。先处理层级再移除旧标签；可信EA可对明确新增IDs调用现有`moveViewElementToZIndex(id,目标层位)`，保持原有无关元素相对顺序，不直接手填fractional index。没有宿主层级入口时，新图用MCP先创建底板、再创建text/LaTeX组合，不能用复制遮罩或透明化用户底板掩盖问题。

### 执行顺序与关联恢复

1. 明确canvas/file，读full，记录原文、文字样式、位置、容器/箭头owner、group/frame、锁定与邻边。确认MathJax已就绪。只处理用户意图中的公式，保留一份完整原文供恢复/后续编辑，不将源码当可见公式交付。
2. 新建未绑定混排文字可以在排好语义行后选中并运行原Action；已绑定文字先创建**未绑定的暂存副本**，原标签与owner保留到新公式全部生成、资源就绪并检查成功。只选本次text IDs，不选全图、整组或只选外框。失败读回已执行部分，保留/恢复原文，不用新run盲目重放。
3. 用[script-execution](script-execution.md)中的真实宿主入口。Action命令相对路径是`latex/Action-Extract-Latex`，前缀取真实manifest ID；宿主Advanced URI带明确vault/filepath。需要可信EA时用`ea.selectElementsInView(actualTextIds)`；只传URI不会替你选中文字。无GUI远端不能自己发宿主URI，也没有`drawing_extract_latex/drawing_run_script`；不要擅开白名单或假设已经有远端adapter。
4. 读回新增ID、真实公式尺寸/fileId和源TeX，逐项与源公式核对。不要因为普通text不再含`$`就算成功；错误公式、MathJax错误图或缺失资源同样不能交付。源公式在Embedded Files保留是合法源码，不属于“可见源码泄漏”。
5. 转换结果是**多个原生元素组成的混排块**，不是一个仍可`set_text`的原标签。先确保新片段位于所属填色底板之上，再删除被替换的旧bound text（走原生解除关系入口），保留容器/箭头ID及业务连接；将新片段与对应owner适当编组、用`add_to_frame`恢复frame归属，维护旧→新成员映射和完整原文。一个容器不能绑定多个混排片段为单个bound text；依靠显式group保持整体编辑，不伪造`containerId`。几何检查确实把公式内容与背景矩形认作冲突时，只对真实的图文容器声明`isContainer:true`，不把业务碰撞随意标成合法包含。
6. 由实际公式与文字bounds重排：行高至少容纳当行最高公式及间距，按容器有效区域整体对齐；必要时扩大容器、调整邻边，保留完整业务文字。不靠缩小公式到不可读或换成普通Unicode/截图掩盖问题。后续移动/缩放选完整混排块与owner；更新标签需更新对应片段或用保存的原文重新转换，不能对已删除的源text调用set_text。
7. 脚本外部写入后重新read最新revision，必要时按同file rebind，然后check→全图/局部PNG→真看图→review。普通`label_equals`不再代表整个混排块，按各文字片段、源TeX和业务边核对完整性。检查没有非预期裸露的`$…$`、`\sqrt`、`\sum`、下划线或花括号源码；分式上下标、行距、颜色、容器和连线都需实际可读。

### 只有远端MCP、没有宿主脚本入口时

不要把“脚本不可直接调用”变成原样输出源码的理由。新图可按语义把普通文字和公式分开，复用现有`create_text`与`create_latex`；不另写第二套通用正则解析器或新DSL。`tex`只传公式内容、不带外层`$`：

```json
{"op":"create_latex","ref":"max-formula","x":80,"y":160,"tex":"m_{new}=\\max(m_{old},S_i)","scaleX":1.4666666667,"scaleY":1.4666666667}
```

示例比例来自原脚本22号字/15，不是所有公式的固定比例或PNG倍率。创建后读真实尺寸，与原生文字一起安排基线/换行，再group/add_to_frame；先在未绑定的替换内容上验证全部公式成功，最后才移除旧标签。`drawing_measure`测的是文字，不会自动测量/解析混合LaTeX；复杂数学content可用现有规划器latex内容入口或创建后read。缺MathJax时明确前提，不用字面源码、全图栅格图或假公式替代。

### 实际验证与范围

已在宿主ymjr + Bridge0.13.2、MathJax就绪时运行用户原Action：4个混排源text（含一行多公式、多行中文、`$$…$$`）变为7个普通文字片段与5个LaTeX image，标题保持；保存后的5个Embedded Files逐项保留原TeX，PNG实际显示希腊字母、根号、上下标与求和。不是自动适配任意Markdown/转义规则的证明。
另验证已绑定节点的安全替换：只转换未绑定副本，恢复group/frame并用现有EA层级API将片段置于填色节点之上；原owner、下游节点和箭头的ID/几何/双向绑定保持，公式和中文在最终PNG中真实可见。原Action与用户图未修改；这不是“直接运行Action就自动保留绑定/层级”的声明。

## Smart list 与 Bullet

这两个功能不同：

- **Smart List Engine**：对选中的已有元素写`customData.list={type:"order"|"unorder",index?:number}`，Engine在Canvas旁实时画序号/项目标记，不创建额外文字元素；`continue`会按上方最近列表延续order index。列表是交互渲染，不把Unicode `1.`/`•`写入业务文字。PNG可检查当前静态编号，但Engine必须运行。
- **Bullet Engine**：用户通过面板启用后点击画布，真实生成“椭圆容器+文本”的原生元素组；默认设置来自`plugin.settings.scriptEngineSettings.bullet_settings`：`fontSize`、`circleSize`、`colorList`、`fontColor`。它是可移动可编辑的真实元素，不是Smart List的同义词。自动生成需要真实UI/Engine或授权非交互EA脚本复用`addText({box:"ellipse"...})`，不要声称Bridge已有bullet Feature。

Smart List的安全更新可用受信脚本：读取选中元素→copy到EA→merge `customData.list`→await `addElementsToView`；不要直接拼完整元素JSON。Bullet的点击放置需要实际宿主Canvas，默认脚本是面板交互，URI只能触发不能提供点击坐标。

## 常见生成图元

现有`drawing_primitives`能规划`draw/polygon/cuboid/brace/callout/code/checkbox/connection`，与`native-features.md`配合。`generate/Action-Generate-Digital-SVG.md`和`Action-Generate-Digital-Microarch-Items.md`是用户脚本参考，不是本包自动调用的隐含模板；运行前读取、备份、绑定明确画布，使用真实测量和`svgPathShape/svgViewBox`。

所有视觉效果遵循：原生编辑性优先；Feature元数据和Engine依赖记录；check→PNG→实际看图。不存在真实adapter的功能用[script-execution](script-execution.md)和用户授权的受信EA脚本，不能把面板按钮包装成无交互MCP。

来源：Bridge `FEATURE_SPECS`中的`shadow/callout/code_highlight/rich_text/gradient`；绘图脚本目录下`shadow`、`callout`、`code-highlight`、`list/Feature-Smart-List-Engine.md`、`generate/Feature-Bullet-Engine.md`及`native-features.md`。
