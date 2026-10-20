# 常见图型与多风格参考

这些是可执行输入和工作流，不是渲染结果。使用`drawing_templates(action="list")`看图型与style列表；`action="get",name=...`取一份简短recipe，修改业务内容后执行。**不得把示例业务当用户事实。**

## 新图开始：一次视觉偏好选择

用户未指定视觉方案的新图，先用**当前Agent客户端真实提供的ask/选择工具**弹出一轮选项；不是调用不存在的drawing_style_dialog，也不是自动弹Obsidian面板。先可做只读status/discovery以提供真实可用字体，不先创建用户画布再等选择。只有用户要求这次绘图，才询问这次偏好；维护Skill/回答能力问题不额外弹偏好问卷。

### 何时问、问多少

- 只问未确定的维度；用户已经说“手绘、灰度、深色、文楷”等就锁定对应项。之前为**同一套图/演示文稿**选过则复用本会话选择，不每页重问、不跨无关项目偷偷套用。修改已有图默认继承原图，除非用户明确要求重新设计。
- **style 和 review 是高优先级必答项**，只省略已有明确选择来源的项；“帮我画好图／请重试／继续／赶时间”不是不问。用户只指定专业风格，仍要问未定 review、色板／背景和字体意图；选择“style交给Agent”不自动授权 review。
- 用户明确“不要询问／全部你决定／使用默认值”才按授权维度采用保守默认并说明依据。无回答就等待，不自动点击推荐。仅“直接画”若未明确免询问，也不能代替 style／review 的选择。没有选择工具用编号问题，等待回复，不假装弹窗已显示。
- 一轮最多5题：未定 style、review 优先，其后色板、背景、字体／字重。每题2–5个具体选项，保留客户端自定义输入；不要额外造Other。不因减少往返删掉询问，也不因局部修图重复询问已选项。
- 为每项记录 `{value,source,evidence}`；source为`user`明确指定、`answer`本轮回答、`inherited`原图／同套图明确沿用、`delegated`用户明确授权默认值。创建前提交`brief`，不得虚构证据。CLI固定示例也要显式采用其已声明设计或传用户选择，不能借无人交互偷偷跳过。

| 问题 | 2–5个选项（只保留未定项） | 说明 |
| --- | --- | --- |
| 视觉风格 | 专业平整 / Visio工程 / Rough.js手绘 / PPT演示 / 交给Agent | 映射真实professional/visio/handdrawn/presentation；电路可推荐blueprint（替换一个选项，总数不超5） |
| 色板 | 克制蓝绿 / 明亮多彩 / 莫兰迪低饱和 / 中性单色 / 自定义色板（仅客户端支持自定义内容时） | 每项附实际主色hex小列表和用途；选定后解析完整前景/底色，不只是配色名称 |
| 背景/明暗 | 白底浅色 / 暖白浅色 / 深底高对比 / 沿用模板（确有模板） / 交给Agent | “亮色系”可能指鲜艳accent而不是白背景，色板与背景两题分别回答；暗色不靠导出时反转伪装 |
| 验收等级 | low·快速基本检查 / medium·可读交付（推荐） / high·严格细查 | 先解析用户提示词，已明确不重问；等级与模型effort、手绘/专业风格独立，高级不要求所有箭头绑定，按[分级验收](acceptance.md)实际执行 |
| 字体与字重 | 清晰正文·标题强调 / 清晰正文·常规字重 / 手写注释（有候选时） / 沿用原图或模板 / 交给Agent按角色选 | 先按[typography](typography.md)取得当前集合并判断候选；用户选意图，不必逐个字体作答，实际名称由Agent解析并验证 |

默认“标题加粗”只针对标题/分区名，正文regular；不用全图粗体模拟专业感。用户单独指定“全部加粗/不加粗/某些强调”时以明确要求为准。中文和拉丁字母混用时以宿主实测宽度布局；手绘线条和手写字体是两个独立偏好，允许“手绘线条+无衬线字”，不能强绑。
字体不是固定套餐：正文/代码/标识符/注释可按角色选择不同实际family；新宿主重新发现，未知项保留不确定性。按[typography](typography.md)分类与验证，不能把某台机器安装的名字、style profile或代码例子当全局保证。
验收选择落实为check/review/compose/apply的acceptance_level，不是写在图中当说明。medium默认重点避免穿字、文字互压与遮挡，high再细查语义路径/层级风格；大背景框承载文字是合法重叠，不硬性分离所有坐标相交。

创建任务单示例（真实值应来自本轮回答；下面只演示结构，不是用户已同意）：

```json
{
  "task_id": "release-flow-unique-request",
  "preferences": {
    "style": {"value":"professional","source":"answer","evidence":"用户选择专业平整"},
    "review": {"value":"high","source":"answer","evidence":"用户选择严格细查"},
    "palette": {"value":"蓝绿，#2563EB/#0F766E","source":"answer","evidence":"用户选择克制蓝绿"},
    "background": {"value":"#FFFFFF","source":"answer","evidence":"用户选择白底浅色"},
    "font": {"value":"已发现的清晰正文字体，标题强调","source":"answer","evidence":"用户选择清晰正文、标题强调"}
  },
  "requirements": [
    {"id":"approved","description":"通过审批后发布，方向正确"},
    {"id":"rejected","description":"驳回后回到修改，保留驳回分支"}
  ]
}
```

`drawing_context(create,brief:上述对象)`；已有图`bind(file_path,brief)`，读取可不提交brief，首次写入前必须补齐。DSL首次render也传`brief`；重复同task_id只修同一文件，不因编译／check失败换state_id创建副本。`brief`持久化于客户端私有状态，不写用户图中文字。它记录Agent引用的对话，不提供用户身份验证或硬件正确性证明。


### 色板起点：解析为实际允许颜色

下列是**可选设计起点**，不是工具内建profile或固定品牌规范。最终允许列表由选项+用户覆盖生成；深/浅背景与中性色需加入列表，颜色数量通常主/辅/强调2–4色加必要中性色，不每个节点随机取色。

| 色板 | 主/辅/强调候选 | 浅底/正文候选 | 适用 |
| --- | --- | --- | --- |
| 克制蓝绿 | `#2563EB #0F766E #B45309` | `#FFFFFF #F1F5F9 #0F172A #475569` | 架构、技术说明；暖色只作强调 |
| 明亮多彩 | `#2563EB #16A34A #EA580C #9333EA` | `#FFFFFF #F8FAFC #172033` | 演示分类，使用深正文而不是亮色小字 |
| 莫兰迪 | `#718A91 #84947C #AD8B83 #A493AD` | `#FAF8F3 #E8E3DA #353D43 #596168` | 低饱和填充/模块区分；主文字保持深色，不用浅灰糊成一片 |
| 中性单色/灰度 | `#111827 #4B5563 #9CA3AF` | `#FFFFFF #F3F4F6 #D1D5DB` | 打印、论文、严格低彩；状态不只靠明暗 |
| 深色方案 | `#60A5FA #5EEAD4 #FBBF24 #C4B5FD` | `#111827 #1F2937 #F9FAFB #CBD5E1` | 深背景与浅前景；不是直接把白底色板套到黑底 |

若用户选“深色+莫兰迪”，保留低饱和角色，但先选/测正文与填充的对比；不保证浅色表可不改直接复用。strict时未在允许列表的中性色、阴影颜色、渐变stops、alpha混合衍生色也不能偷偷添加。先展示解析后的最终色值列表并用一行复述；默认包含哪些背景/文字中性色要明确。用户只给两种颜色时尽量以透明填充/线型/粗细表达层级，确实不可读则指出冲突并只问是否扩展色值，不“自动加白”。

建议正文对背景对比至少4.5:1，大字3:1、关键边界3:1作为设计检查目标，不声称整张PNG自动通过WCAG；由实际sRGB相对亮度算配对，不凭“低饱和”判断可读性。状态/类别同时有标签或形状编码；色盲/黑白打印不能只依赖红绿或相邻浅灰。strict限制针对**本次生成/重样式的原生属性**，抗锯齿PNG会产生中间像素色；原图/图片/素材/公式不得擅自重染，需说明保留资源的范围，不伪称每个像素都在列表内。

### 偏好必须落实到现有API

选择结果只是本次Agent的工作计划，不是新增MCP schema。Agent记录profile、canvas/surface/text/accent色值、颜色→业务角色映射、实际family与文字角色、标题/正文大小、boldTargets、roundness及edge语义，再展开成现有字段。下例是**构造字段的JavaScript示意**：`bodyFamily`须先按typography流程解析为本次接口返回的精确名称，不得把变量名或占位文字作为family提交：

```javascript
const style = {
  "profile":"professional",
  "fontFamily": bodyFamily,
  "fontSize":20,
  "shape":{"roughness":0,"fillStyle":"solid","strokeWidth":2,"roundness":{"type":3,"value":6,"roundType":"arc"},"backgroundColor":"#F1F5F9"},
  "text":{"strokeColor":"#0F172A","lineHeight":1.2},
  "edge":{"strokeColor":"#2563EB","strokeWidth":2,"roughness":0,"roundness":{"type":2,"value":6}},
  "container":{"backgroundColor":"#FFFFFF","strokeColor":"#475569","roundness":{"type":3,"value":6,"roundType":"arc"}}
};
```

这是现有`diagram.style`的profile对象；**不是**调用`style:"morandi"`/`style:"dark"`。箭头头型仍逐edge显式指定；纯色板不自动决定UML语义。手绘选roughness1/hachure或用户指定solid，并独立控制字体；不能拿PNG滤镜替代原生属性。
此shape/container小圆角起点不适用于表格单元格：cell显式`roundness:null`、细连续网格、深色表头配浅色正文；返回真实refs后分别设置表头底色与bound text字色，详见[表格规范](capability-map.md#表格清晰表头与连续网格)。不要把整表拆成带间隙的大圆角卡片。

注意真实高层行为：planner会按variant/PALETTE补节点stroke/background、容器color，部分标题/文字颜色也由recipe固定；仅改profile并不能证明严格色板已生效。strict任务应逐节点/边/容器设置允许色，必要时按plan refs附加patch；apply后读完整实际样式，修正新增的未允许颜色，不能声称profile会自动覆盖每条默认色。

加粗用现有`set_feature rich_text`/`set_text_global_style`对**真实text IDs**设置bold/fontWeight；不是create_text顶层bold或虚构fontFamily后缀。按discovery确认Engine，更新后重新测量/排版；“不加粗”也检查已有模板的`customData.bold`、`customData.font.weight`及局部boldPartial。body和标题分开处理。LaTeX image、SVG素材内部字和普通text是不同资源，不能用text加粗工具假称全部生效。

明暗背景必须作用于真实画布或页面：现有MCP无通用“设置全局theme”工具时，使用用户允许且不遮挡内容的原生背景rectangle，明确`isContainer:true`、置于图元之后并纳入页面frame；导出时实际看到该背景。不擅改Obsidian全局主题/用户偏好，也不拿PNG暗色反转冒充源图dark。新版outline block未设显式backgroundColor时填画布背景，已设非transparent时优先该颜色；公式可能固定黑字，深色/容器页必须看实际呈现，不能当透明洞。PPT粗短/细长尺寸按[宽箭工作流](layout-export-animation.md)分别控制路径/箭身/头/描边；必要时按用户允许用浅色公式panel或已确认API，不留下看不见的内容。

### 选择后的验收

创建前用一行简报已选方案（风格／色板／背景／颜色编码／本次选定实际family及角色／标题字重／固定圆角／语义头型），无需再问“是否确认”。读回检查精确hex、roughness/fill、实际字体/字重、radius和头型；PNG检查对比、层级、字形/回退、输出字高、边线/公式/图片可见。保留用户选择，后续修布局不能悄悄重置字体或默认蓝色/大圆角/普通箭头。

这是Skill级启动交互，不是绘图服务器自行弹UI；支持ask的Agent应真实调用选择工具，只有文本客户端才用编号问题。未真实收到选择就不声称用户选过；没有运行实际绘图/PNG也不称视觉通过。
已实测原生样式示例：专业蓝绿、明亮演示、暖白莫兰迪/已注册文楷、灰度hachure/不加粗、深底高对比。读回实际色值/字体/标题bold，PNG查看后把对比不足的莫兰迪/灰度边框改为允许的深中性色；这证明属性落地，不声称新建了独立的选择器UI或已替用户作出选择。

## 风格

| profile | 确定性规则 | 使用条件 |
|---|---|---|
| professional | roughness0、浅色solid、克制语义色；实际family另按当前集合解析 | 默认文档图 |
| handdrawn | roughness1、hachure、手绘线边；布局/绑定仍确定 | 用户要手绘效果，不等于自由笔画 |
| visio | roughness0、sharp边、1.5线宽；字体按角色/语言显式解析 | 正交工程图、UML；不声称输出.vsdx |
| blueprint | 白底蓝线、清晰数据通路与端口 | 电路/微架构；默认保留库素材本身样式 |
| presentation | 较大字号与标题层级；字体覆盖与阅读尺度需实测 | 原生frame演示页，指定库版式优先 |

在普通图描述加`"style":"visio"`或`"style":"handdrawn"`。创建文字前将本次实际family显式写入style对象，例如JavaScript构造`{profile:"visio",fontFamily:bodyFamily,shape:{strokeWidth:2,roundness:{type:3,value:6,roundType:"arc"}}}`；`bodyFamily`不是新接口字段或可直接提交的字体名。底层profile有历史字体默认值，但它们不证明宿主可用，不能替代发现和角色选择。优先级：硬保护→用户显式局部/本轮视觉选择→原图未请求字段→role/variant→profile默认。已有图不自动全图换主题；库源样式默认保留，只有用户明确要求才对本次导入副本改样式。

`roughjs`/`rough-js`是`handdrawn`的已声明别名；`drawing_templates(list)`同时返回aliases。自然语言中的“手画/handdraw白板笔迹”用原生`draw`/freedraw，**不是第二个Rough.js renderer或名为handdraw的profile**；可混用freedraw轮廓、原生文字及有binding的arrow。不要为证明多风格把所有场景都画成同一种矩形。

Visio/电路/微架构中的必要线—线交叉，采用修改版原生lineCrossings：独立线路arc/gap，明确连通才dot，不用白色遮罩模拟断开。visio profile不自动推断交叉语义；规划后按关系ref补patch_custom_data，详见layout-export-animation的Line Crossings。

演示与GIF适合1280×900左右的可读构图；极宽/极长全图在auto PNG中会缩小文字。先按语义组织少量列/行/分区，不通过删业务关系或截短标签压尺寸。`layout.nodeGap>=32`、`rankGap>=40`；默认值优先，紧凑布局需遵守真实planner边界。

## 流程图

`drawing_templates(get,name="flowchart")`，再`drawing_plan`或`drawing_templates(plan,...)`。节点、关系、分支标签齐全；长中文先测量和语义换行。菱形不要过宽；失败回边用外围通道，不能为了美观删业务关系。

## UML类图

`drawing_templates(get,name="uml-class")`。`nodes`含`id,label,attributes,methods`；`edges`含关联、composition/aggregation端点头与multiplicity标签。`drawing_templates(plan,name="uml-class",context_token,data=diagram,style="visio")`生成原生三分区类框、分隔线、独立文字与group；提交后可继续改字段和方法。

- 实心diamond放整体端是composition；空心diamond对应aggregation。泛化triangle_outline在父类端，realization还应dashed。
- 不根据“UML”三个字自动选择类图；用户强调交互顺序时选sequence。
- class整体移动用成员闭包，不仅移外框；外部连接绑定class body。

## UML时序图

`drawing_templates(plan,name="uml-sequence",data={participants,messages,title},style="visio")`。参与者head、虚线lifeline与逐时消息是原生元素；返回消息用dashed。

```json
{
  "participants": [{"id":"user","label":"用户"},{"id":"api","label":"API"},{"id":"db","label":"数据库"}],
  "messages": [{"from":"user","to":"api","label":"请求"},{"from":"api","to":"db","label":"查询"},{"from":"db","to":"api","label":"结果","return":true}],
  "title":"请求时序"
}
```

透明原生port只服务于消息绑定，不能看不到port就断言消息没有锚点。当前recipe没有自动实现任意alt/loop/activation DSL；用户要求这些时通过明确原生容器/短线补齐并看PNG，不宣传成全UML标准验证器。

## 系统架构图

`drawing_templates(get,name="architecture")`，普通`drawing_plan`执行。group是一起移动，container是可见分区，两者分开。跨容器边不能变成说明文字来“消除穿线”。代码测量+路径避障，PNG检查标签留白和层级。

## 微架构/电路：硬件语义优先，不是普通架构模板

**先读[microarchitecture](microarchitecture.md)**，无论用户是否指定库。微架构须先确定部件、端口/信号、固定阶段/区域和验收清单；不能把单元收进阶段bullet卡片，也不能为check通过而删关系或降粒度。矩形可表达memory/RF/control，ALU/MUX/边界等按真实角色选形状与比例。

`drawing_templates(get,name="microarchitecture"|"circuit")`只是数字电路库示例，**不是完整CPU自动布局器**。当前kind分类共用通用rank；容器只是事后包围框，固定流水级和反馈通道需显式位置/尺寸/端口或低层原生operations。示例library来源必须换为实际发现的库，不假设个人路径。

可按文件名查找 `digital-circuit-components(svg).excalidrawlib`，但不能假设任何绝对路径或固定item数量。先通过 `drawing_library(list/query)` 发现安装库与真实vault相对路径；同名item用exact ID。顺序：query→get真实bounds/类型/资源→preview候选→**按角色/端口和目标内容区计算library.scale**→compose或native insert→以缩放后的几何连接与label→全图check/PNG。库素材svgPathShape仍是可编辑line carrier，不是整项PNG。node.size增加布局空位不会放大库符号；已导入尺寸不合适就对完整实例scale_selection，见[尺寸适配](layout-export-animation.md)。

`drawing_compose(context_token,base_revision,diagram)`接受普通nodes和：

```json
{"id":"alu","label":"算术逻辑单元","library":{"source":"指定库路径","item":"ALU","scale":2}}
```

库图元是line时不能假称能直接作为箭头绑定目标。组合器请求透明原生rectangle anchor，和整项编组；外部连接用返回anchorElementId，内部元素原样保留。`fromFixedPoint/toFixedPoint`是0–1比例，但必须按**当前素材的真实端口stub**计算，不能把示例0.28/0.72当固定MUX引脚：端口scene位置=`carrier origin + source stub × targetSize/viewBoxSize`，比例由当前anchor几何反算。库未声明电子引脚时只提供几何锚点，不臆造电气语义或网表验证。

每次native插入分别提交；出错返回已完成的stage/ID，不自动重放整图。重复item插入生成独立ID/group/frame，不共享身份。

## 多页演示：presentation-bundle

`drawing_templates(get,name="presentation")`提供同系列intro/slides页计划；先发现本机的 `presentation-bundle.excalidrawlib`，再将真实返回路径传给 `drawing_present`。本包不分发素材库，不假设本机已经安装这些模板。

`drawing_present(context_token,base_revision,presentation)`逐页原生插入frame模板，保留装饰、组与源→native ID映射，再用原生text填标题/正文。**先get源frame尺寸并计算presentation.scale，再填字；不能默认小底板scale=1然后把正文挤在上面。**各模板源尺寸不同则分次调用或逐项insert后适配；没有page.scale/width/height自动fit字段。不能手写frameId猜关联。title/body越界先检查底板尺寸、留白和布局，再按内容拆页，不裁业务文字。每页返回frameId与elementIds，用这些IDs导出单页PNG；还需全图overview与所有页实际看图后review。

```json
{
  "library":"Libraries/presentation-bundle.excalidrawlib",
  "pages":[
    {"template":"Simplicity (intro)","title":"绘图方案","subtitle":"原生可编辑与视觉反馈"},
    {"template":"Simplicity (slides)","title":"执行闭环","body":["自然语言组织语义","原生绘图和程序检查","PNG反馈与局部修正"]}
  ]
}
```
示例的library路径和template名称必须先经query/get确认；它们不是每台机器的默认值。当前输出是可编辑的Excalidraw演示页面，不自动声称PPTX。用户明确要求.pptx时需加载本机实际提供的对应PPTX Skill，并说明演示页导出与原生Excalidraw源之间的编辑边界；没有调用真实导出工具就不能改文件后缀假装PowerPoint。

## 含复杂图元的模板

需要draw、cuboid、brace、callout、代码高亮、checkbox或特定连接样式时，再读`references/native-features.md`并用`drawing_primitives`。常见图recipe和低层图元是互补关系；Skill始终要执行完整PNG评审循环。
