---
name: obsidian-excalidraw
description: 在 Obsidian Excalidraw 修改版中创建、修改原生可编辑图；自然语言、可选场景DSL、原生素材与公式、PNG验收；异常时可选用户开启的CDP只读诊断，修图仍走正常API并保留用户内容。
---

# Obsidian Excalidraw：原生绘图与真实 PNG 闭环

## 可靠启动与交付入口

完整使用教学图法选择及机制验收需要 **0.10.4 或更新运行包**；drawing_begin应有design提案参数，drawing_review应有expression_checks。运行包与Skill必须同时更新并重载；不要只复制文档假装API已升级。Bridge仍为0.13.7。

**0.10.5 动态字体工作流**：当前注册集合不是上限；有明确收益才按[授权规范](references/runtime-fonts.md)扩充。系统导入与网络下载、会话加载与vault持久化分别确认；插件须实际具备新EA方法。此更新不新增字体MCP、不改Bridge、不授权自动下载或覆盖文件。

**0.10.6 原生图标工作流**：需要图标时按[icons](references/icons.md)发现本地SVG来源，使用新宿主rectangle＋svgLayers保留多色／单色矢量及动态style。复用现有操作，不新增图标MCP或自动转换器；宿主需实际包含2.29.0-9配套组件，更新Skill不自动升级插件。

先调用 **`drawing_begin(request:用户原始需求,action:"prepare")`**。它实际返回本包Skill、验收/字体/工作流全文、任务专用参考、正确原生示例和当前宿主发现结果，不依赖客户端是否自动激活Skill。硬件另载微架构规范，数学另载内容分流；已有图加明确file_path可读取当前画布和真实评审历史。返回规范不等于模型已理解，更不等于用户已经回答偏好。

偏好和需求齐全后用`drawing_begin(create|bind,brief,filename|file_path)`进入同一任务；原有context、DSL、原生入口复用同样的brief门禁。**逻辑微架构/电路**在brief.representation声明部件/端口/信号，并用drawing_contract映射body/wire IDs。**物理剖面/封装/爆炸图与讲解页**在brief.visual_plan声明目的、参考证据、视图、对象、承载/包含关系和示意边界，不为通过门禁虚构信号网络。[执行契约](references/workflow-details.md)、[视觉设计层](references/visual-design.md)。

**最终交付必须调用`drawing_deliver(context_token,revision,preview_id)`取得`status:"deliverable"`回执。** 它重新核对当前文件/版本、全图PNG及哈希、同一PNG已completed的评审、需求和表达契约。`applied_needs_review`、`rendered_needs_visual_review`、`needs_repair`、check=pass或PNG已生成都不是完成。失败/continue/needs_attention只报告实际进度及剩余问题，不在最终文字中改写成成功；回执也不冒充独立科学/电气审核。


## 绘制前先问：该用什么可视结构解释？

新教学／机制图先读[teaching-design](references/teaching-design.md)。写清读者要看懂什么，提出2–3个实际表达候选，说明取舍并推荐，再用真实ask让用户选。**图法不是配色／手绘选项。** 用户明确“你决定”、已有确认方案或局部修改继承时才跳过；记录真实来源，不虚构批准。一套多图先确认逐章图法清单，不每章重问，也不统一套文字框流程。

可用drawing_begin(prepare,design:未确认提案)返回design_options，再交给客户端ask；创建前brief.teaching_plan必须有selected与choice。机制方案按goal声明sequence_window/matrix_groups/bitwidth_compare/memory_map/time_steps等实际编码；process/overview/reference允许流程／速查表，但须明确选择，不用它们冒充已画机制。

绘后必须核对**实际对象是否表达目标**，不是文字里有没有提到术语。mask要有格子，分页要有块及映射，分组要有边界；段落框写“对角带／Block Table”不算。check/review/deliver重建编码核对当前原生元素，TEACHING_*硬错误不可视觉豁免。实际PNG看过后还需逐goal的expression_checks，说明“不读长段正文能看出什么”；all-pass布尔值不能代替。

## 先选表达，不按题材强套图法

看参考图或准备讲解页时先读[visual-design](references/visual-design.md)：目的、关系、图法、载体分开；区分忠实重绘/结构重绘/只借风格，记录可见事实与不确定内容。PPT不是一种图法，硬件也不总是逻辑网络。封装剖面/层叠/爆炸/投影走physical_structure；讲解页面走explanatory_page；真实数据通路仍走microarchitecture/circuit。

0.10.3新增[technical-illustration](references/technical-illustration.md)及配套运行实现：projected_box/layer_stack/grid_array/leader/measured text，通过既有drawing_primitives执行。action=render＋同state_id复用原生ID、外部修改冲突、检查和PNG。0.10.2及更早版本不包含这些新增kind。默认静态二维可编辑示意，不宣称PPT全特效/3D/CAD等价。

## 创建前门禁：先问 style 和 review，不先画再补问

**新图默认必须先用真实 `ask` 一轮收集未定偏好，再创建画布。** 优先询问 **style（专业平整／工程／手绘／演示）和 review 等级（low／medium／high）**，同轮补齐色板、背景、字体／字重意图，最多五题。只读 status／discovery 可在询问前执行；create／DSL render／library insert／apply 不可以。没有 ask 就给编号选择并等待回答；“推荐 medium”不是用户已经选择 medium。

只跳过**已有明确来源的那一项**：用户本次明确指定、同一套图已选并说明沿用、局部修改继承原图，或用户明确说“不要询问／全部你决定／使用默认值”。“帮我画／画好图／请重试／继续／赶时间”不是放弃选择；仅说“专业风格”不等于同时选了配色、字体和 review。用户选择“风格交给 Agent”也不等于授权 Agent 决定 review。

开始前读[偏好选择](references/diagram-recipes.md)和[验收](references/acceptance.md)，记录本次需求清单及每项选择来源；创建时提交绘图任务单 `brief`。任务单是可核查的操作记录，不冒充工具已验证用户对话。未收到选择不生成“用户已同意”的证据；用户批评成图时先修原图，不重新弹样式问卷来回避问题。

## 数学内容先分流：不要求用户写 `$` 或点名 LaTeX

**在选字体、测量或批量调用文字 helper 前，先区分数学公式、信号／代码、位流／波形和普通说明。** 矩阵、数学向量及转置、分式、求和、递推式、成组上下标默认用保留源TeX的 `create_latex`；必须先读[数学内容与混排](references/visual-content.md#数学内容分流-先认语义再选元素)。输入写成自然语言、`y = W x`、`W = [[...]]`或Unicode上下标，也不准因此当普通正文。

**禁止用空格／换行拼矩阵括号、Unicode上下标、多个偏移小text或分隔线模拟数学排版。** `Q[26:0]`、`frame_start`、`0x4078`、`10110010`、引脚名与波形值仍用原生文字；阵列格子、位段和门／线保留原生图元，不做整图公式。用户明确要代码／ASCII原样展示或局部修改只保留未请求内容时，记录例外，不全图自动转换。

创建前在已有brief需求中列出数学内容的范围，执行时保存公式ref→native image/fileId→源TeX及普通信号标签的映射；这不是新API字段。`latex.available:true`后实际调用并核对资源；缺MathJax或渲染失败要报告，不能悄悄退回文本模拟。数学内部排版稳定不等于外部无碰撞：用真实公式尺寸重排混排块，查看PNG的矩阵行列／括号、上下标归属、分式和基线，再做需求验收。数值测试、文字测量和`label_equals`都不能替代公式验收。


## 先选入口，只读相关参考

- **用户只说想画什么**：Agent负责选表达，不要求用户写DSL。普通一次性节点图用compose；需要可重复源文件、嵌套空间/表格/多端口组合时用可选[Scene DSL](references/scene-dsl.md)。
- **DSL路径**：真实`drawing_dsl(plan|render,document,...)`或包内`launcher.py dsl -- ...`；同state_id增量更新，实际PNG后仍review。不要把其document与compose的diagram混用，不用原生apply悄悄覆盖受管对象。
- **原生路径**：已有图小改、用户库、特殊扩展/交互/动画继续read/apply/library/present/原生CLI，不强迫经过DSL。先绑定明确目标，按下表只读所需能力；不为简单图遍读所有references。
- **需要图标时先读[原生矢量图标](references/icons.md)**：按实际本地图标目录发现／预览／fit，新宿主以rectangle＋`customData.svgLayers/svgViewBox`保留多色path；通过现有create_shape／patch操作改变stroke、fill和线宽。透明元素style可保留图层原色，背景色是图层填充覆盖而非底板。SVG文件夹不等于excalidrawlib，Action的有限解析器不承诺任意复杂SVG无损转换；不虚构图标MCP、不自动下载或改库设置。
- **只有CLI也可执行**：`launcher.py cli -- ...`是本包绘图客户端；`launcher.py dsl -- ...`是声明式场景；插件自身native CLI另见参考。三者都不替代真实宿主连接与PNG检查。
- **CDP只读排错（默认关闭）**：效果异常、字体/资源/表格/图层原因不明时，先`drawing_debug(status)`，再按[只读CDP](references/cdp-readonly.md)提示用户选择开启。启用后仅`drawing_debug(inspect)`读取明确已打开的宿主vault/画布；禁止任意JS、Input、断点、打开/保存/导出或CDP改图，不用browser绕过。诊断不授权修复；微调仍需当前Bridge revision／DSL源及正常PNG验收。

## 先决定目标和视觉，不要求用户写坐标
- **新版原生表格**：先发现`capabilities.nativeTable.callable`，为true时读[原生表格规范](references/table-native.md)，用`drawing_table(create|style)`调用宿主主题／边框模板，不逐格模拟。它需要配套schema-v2宿主构建；旧`create_table`和DSL表格不自动获得新能力，不虚构theme字段或把开发宿主当正式发布。

- 使用已发现的真实`drawing_*` MCP，前缀/schema以客户端为准；相对references路径属于当前Skill，客户端支持时才用`skill://obsidian-excalidraw/...`。
- 新图用唯一文件名创建独立`.excalidraw.md`；已有图按明确file_path绑定，保留file/contextToken/revision。不能用active/first、clear重画或手拼整场景JSON。
- 新图按上方门禁询问未定偏好。**style 与 review 必须逐项有明确来源**；详细选项见[视觉偏好](references/diagram-recipes.md)。验收等级不是模型 effort，不因 effort 低或请求简短而跳过。局部修改只继承用户未要求改变的属性。
- 已明确的属性直接落实，仍需询问其余未定项。专业平整可从正文20／标题28、roughness0、线宽2、小圆角`roundness:{type:3,value:6,roundType:"arc"}`起步；**表格／寄存器字段单元格例外：`roundness:null`**。默认数值不是用户偏好或已验证排版；实际字体测量、读回和PNG必须完成。
- 配色落实为实际hex；strict任务同时控制底色、正文、边框，不能偷偷补默认蓝色。手绘线条和字体独立选择；字体先discovery确认，颜色/字重/尺寸最终读回并查看PNG，不凭profile名称认定生效。
- **创建文字、选/换字体先读[通用字体工作流](references/typography.md)**：接口取得当前完整集合和来源→Agent按证据判断用途/未知项→按正文/代码/标签/注释等角色选实际family→用该family测量、落地、看PNG。不是本地字体白名单，也不让profile/代码primitive的历史默认名称替代发现；注册、字形覆盖、加载和实际fallback分别验证。已有图未请求换字则继承。
- **当前字体不足且新增候选有明显收益时，读[动态字体授权](references/runtime-fonts.md)**：先已有vault字体／宿主系统候选，再可信网络来源；系统导入与网络下载分别真实询问用户，说明精确来源、目标vault字体目录、许可与同步风险。临时注册、持久化、设置修改／同名覆盖分别授权。获准后通过已存在的可信EA入口调用真实API，核对保存文件和后续加载配置，再重新测量／看PNG；没有字体管理MCP就不虚构工具，拒绝／取消不执行。
- **路径风格先选几何**：`sharp`=普通多点折线（`elbowed:false`＋`roundness:null`），`round`=普通点列平滑转角（`roundness:{type:2,value:r}`），`elbow`=专用`elbowed:true`正交连接器，`curve`=修改版受控`customData.curveArrow:true` S型renderer。四者不是箭头头型；按[四种路径风格](references/layout-export-animation.md#路径不是箭头头型-sharp-round-elbow-s-curve)选择，curve/round精确碰撞仍可能unknown，不能把PNG好看当避障证明。
- **绘图前读[分级验收](references/acceptance.md)**：low基本检查，medium重点内容/可读/遮挡，high再细查连接与层级风格；高等级不强制每根箭头绑定。合法文字置于背景框上不算冲突；字互压、线穿字、后画对象盖字、换字体/字号导致不可读，中高等级优先修复。具体几何误报按issueId＋当前PNG＋理由处理，不能全局忽略。

## 硬件任务必须先分流

CPU数据通路/逻辑微架构/电路/寄存器堆/片上互连：**创建前必须读[microarchitecture](references/microarchitecture.md)**，先定独立部件、命名端口、信号表与固定区域。CPU封装剖面等物理图改读technical-illustration，不因为出现CPU/硬件就要求信号网。逻辑任务不能降成阶段bullet，检查失败也不得删关系、降粒度或重放整图刷通过。
硬件制作按专用参考的“契约→固定骨架→部件/端口→分批网络→保存后审计→全图/局部→最小补丁”执行。信号默认必须水平/竖直或正交elbow；两点起终点同时dx/dy非零就是斜线，不能只看angle0或check=pass。显式计算waypoints/逐段读回审计，保留ID和端点语义；符号多边形斜边不在此约束内。

## 默认低往返路径（0.8.10起）

**减少模型轮次，不减少绘图能力或验证。** 一次读齐本任务所需schema；可并行读取独立资料/只读状态。todo更新与下一步操作同一轮，不为一次进度更新单独等模型；用户显式要求计划时照做。
对已确认就是普通服务节点＋连线的任务才走以下快路径；教学／机制图先完成上述表达选择，不能为减少轮次跳过。硬件先读microarchitecture，复杂固定区域／端口用显式几何。布局报错先修实现；若表达不对就重选图法，不能为了check通过删掉机制、退化成段落链。

1. 有drawing_setup先status；核对`vault_path`是否为用户目标，**cwd不等于Bridge目标vault**。已连接时discovery核对字体/引擎。脚本覆盖保护出现时不伪造installation.json所有权、不搜历史token；按[接入排错](references/agent-setup.md)处理。`launched:false`不是启动成功；缺Advanced URI则提示用户手动运行准确命令，不反复connect轮换凭据。远端只status，不connect/start/reload宿主。
2. 偏好回答齐全后，`drawing_begin(create,request,filename,foldername,brief)`或明确file_path绑定；保存任务ID、需求清单、目标file、token和revision。同一任务只能修同一文件；重绑继承文件级验收历史，不能换task_id／state_id／新文件绕过失败。用户明确要求另一张图时才建立另一任务。
3. **普通一次性节点/流程/架构优先`drawing_compose(context_token,base_revision,diagram)`**；若本轮已选择DSL，改走[Scene DSL](references/scene-dsl.md)而不重复compose。compose在代码内完整plan→apply，不让模型复制大段operations；库组合按阶段提交并报告已执行集合，不宣称跨阶段原子。
4. 没有后续样式时compose传`inspect:true,acceptance_level:本次选择`；还需样式时先compose，再一次apply(inspect:true)按refs局部修正。expected覆盖任务关键内容/关系；后续省略等级/断言会继承同context设置。operations每项必须有`op`不是type；标题粗体用`{"op":"set_text_global_style","targets":["refs中真实textID"],"bold":true}`。不为绕检查重建整图。
5. `inspect:true`返回实际**PNG ImageContent**及JSON：`composition`或`applied`回执、`check`完整诊断、`preview`注册预览（含同revision全图canvasSummary/路径/hash）、毫秒`timings`。内部真实full-read+结构/几何/语义check→按该revision导出，不缓存过期结果、不自动review。默认false保持原接口；check失败仍展示PNG供修复，不能当完成。
6. **查看真实PNG**，再review；逐项提交需求覆盖证据，不能以“模型生成的标签都存在”替代用户需求验收。medium检查content/readability/occlusion，high增加connections/hierarchy_style。文字互压／遮挡不能标intentional；误报必须逐元素、逐问题提供当前局部PNG证据，禁止循环给所有issue复制理由。review=completed也不代表原始check=pass。
   completed后调用drawing_deliver，保留真实file/revision/previewId/sha256/reviewRound回执；不把review调用失败后的自然语言断言当成交付。
7. 有问题只改受影响元素／绑定文字／邻边，apply(inspect=true)后重新读回、PNG和验收。check失败首先核对实际字体、字号、尺寸和API字段，不盲目扩框。默认最多5轮，连续两轮无改善或上限到达则needs_attention；保留原文件报告问题，不换token／task_id／DSL state_id重置预算。

原因不明或PNG与属性不一致时，**不要盲目重画／反复调坐标**：考虑只读CDP获取原生绘制顺序、文字/绑定、表格、资源与视口证据。先确认用户开关；关闭时只提出选项，不自动启用。V8副作用保护拒绝的查询必须停止，不去掉保护重试；状态诊断不能替代实际PNG。

inspect是合并**已有**步骤，不是原子跨请求事务：check/render前用户改图会拒绝过期状态；提交后的检查/导出失败明确返回已提交receipt和phase，不能假称回滚。原生ID、绑定、资源与全图摘要不因此减少。

## 图描述与常用操作

- diagram：kind=flowchart/architecture/swimlane/freeform，nodes含唯一id/shape/label，edges含id/from/to/label/fromPort/toPort；containers/lanes保留归属，layout支持TB/LR、间距和可负origin。节点内容image/latex/echarts/embeddable及UML/电路等按下表读相应参考。
- edge的startArrowhead/endArrowhead放**edge顶层**，显式null表示无头；style放stroke/roughness/roundness。三角头triangle不是filled_triangle；两种block是整条宽箭身。高层不自动转发blockArrowWidth，按refs补patch_custom_data；set_arrow_style不接受该宽度字段。先发现实际头型集合，不能只因插件已更新就假设旧Bridge支持。
- PPT两种宽箭都能独立设strokeColor（轮廓）与backgroundColor（内部填充），fillStyle另控填充方式；普通细线身主要用strokeColor，不套宽箭填充语义。outline默认画布底色而非天然透明；改宽/改色分别操作并看实际PNG，不能用描边宽代替箭身宽。
- 需要先审查计划、手动坐标或复杂增量时，原有read/measure/plan/apply/check/preview/primitives等**全部保留**。plan.operations完整交给apply，尽量程序传递；原生CLI、EA与MCP schema不可混用。
- 语义断言示例：`{type:"label_equals",id:真实节点或textID,text:全文}`、`{type:"edge_label",from:起点ID,to:终点ID,text:"通过"}`。普通check不等于所有业务语义已覆盖。
- 原生 `create_text` 的字号／字体／行高在 `style.fontSize/fontFamily/lineHeight`，不是操作顶层；label用`label.style`。不要复用自写的错位字段helper。先用同一实际style测量再放置；保存后读回实际style、全文和尺寸，不一致就修字段，不按估计字宽移动整图。
- operations的`op`是执行动作；expected的`type`是断言种类；nodes的shape才是图元种类。三者不可混用。只按返回refs填写native IDs，不能把示例ID原样提交。用户没要求连线标签就不为装饰添加标签。
- set_text用真实text/owner；translate保持精度并去重bound text；resize改单元素尺寸不等于整组缩放；scale_selection/rotate使用完整group或精确targets，维护绑定。细节及所有操作见[完整工作流](references/workflow-details.md)。

## 完整摘要与不可省略的质量门

- drawing_read默认返回全部未删除元素、coverage=complete、file/revision/count/total、precision2、世界bounds；不是只选中元素。分页有total/truncated，ids查询不作全图证明。坐标取整只供反馈，绝不回写覆盖精确值。
- preview和inspect.preview均含同revision全图canvasSummary：id/type/geometry、必要文字、bindings、group/frame/锁定等；长文字标截断并用full按需读完整源，密集点列用pointCount。几何/空值/省略字段、并发与完整遍历详见[完整工作流](references/workflow-details.md)。
- 由PNG定位ID后局部改：scene坐标=sceneOrigin+原PNG像素/scale；阅读器缩放需先还原原像素。不能拿截图像素直接写x/y，不能手填boundElements/startBinding/endBinding或原生version/index。
- 完成标准：用户内容/关系齐全、资源complete、当前PNG实际看过、本等级阻断项解决、review=completed且drawing_deliver返回deliverable。几何unknown/重叠候选可凭具体当前PNG审查并披露限制，不等于自动几何证明；不为装饰/合法背景包含无限修图。禁止删边、裁全文或缩成不可读来“通过”。
- 硬件图必须按专用部件/端口/关键网络清单验收，expected不得空却宣称“语义100%通过”。几何pass不等于微架构正确，review也不自动证明专业质量。overview有效字高≈actualScale×fontSize；缩成6px的小字条带必须调整或实际查看必要局部，不把complete=true当可读。
- 微架构正交门：声明并映射representation后，check/review/deliver按保存的世界点列逐段检查并报告ID/段索引；未声明的其他线不能因此被称为已验证。只修route不降粒度、不盲目重放；实际修复轮数累计，不能用新token重置。
- 字体验收核对真实family、全文、字重、混合语言、易混字符和输出字高；属性名/测量相同不证明无fallback。换字体后重测并重排受影响对象。普通planner不是多角色字体引擎，混排走已确认的measure＋原生text操作，不传虚构role/font字段。
- 原生可编辑性优先：保留shape/text/arrow/frame/group、图片源/LaTeX源、SVG path、扩展配置；不能默认用整图图片替代。有分支时全文和“通过/未通过”标签都核对；长中文菱形适度换行，不横向撑成全图。
- 数学按前述语义分流，**不是只拦截裸`$…$`源码**。复用create_latex／DSL formula／compose latex内容入口；普通text和rich_text不渲染公式。保留源TeX、读回image资源及真实尺寸；中文说明与公式分开并编组。缺MathJax明确报告，不用ASCII／Unicode或截图降级；已有绑定标签替换先读[混排公式](references/visual-content.md)恢复owner、group/frame和层级。
- 线交叉用修改版lineCrossings的arc/gap/dot/none；dot不建立电气绑定。禁止白色遮罩、假小弧/圆点、拆线模拟交叉；样式和priority边界见排版参考。曲线/非直角旋转等精确检查仍可能unknown，不能伪称全通过。

## 按需读取，不删除高级能力

| 任务涉及 | 参考与执行要点 |
| --- | --- |
| 教学、学习、机制示意、每章配图 | **[teaching-design](references/teaching-design.md)**：绘前候选选择、逐goal编码、真实机制组件与表达有效性评审 |
| 参考图、PPT内的静态图、讲解图、组合视图 | [visual-design](references/visual-design.md)：目的/关系/图法/载体、参考证据、可编辑边界和组合设计 |
| 物理层叠、剖面、斜投影、封装结构 | [technical-illustration](references/technical-illustration.md)：共用原生组件、确定性投影/重复、同ID增量、物理关系与标注专项检查 |
| 可重复YAML/JSON源、嵌套空间、表格/端口、稳定增量 | [scene-dsl](references/scene-dsl.md)：可选编译器与真实drawing_dsl/CLI，同state_id更新、外部编辑冲突、完整PNG/review；不替代原生能力 |
| 硬件微架构、五级CPU、端口/总线/阵列/旁路 | **先读[microarchitecture](references/microarchitecture.md)**：部件级规划、固定流水边界、真实符号、数据/控制/反馈分离、禁止降粒度和重复compose；硬件清单＋全图/局部验收 |
| PNG异常、原因不明、需要详细debug | [cdp-readonly](references/cdp-readonly.md)：默认关闭、用户选开、固定受保护读查询；不做CDP微调，修复回到正常API/DSL |
| 未定风格、严格配色、字体/粗体、图型/演示 | [diagram-recipes](references/diagram-recipes.md)：真实选择UI、profile/hex映射、UML语义、逐页PNG；不是PPTX |
| 字体发现、按文字角色选型、语言覆盖/等宽/回退、改字体 | **[typography](references/typography.md)**：当前宿主完整集合、Agent证据分类、角色映射、实际family测量/落地、PNG验证；不假设任何固定字体已安装 |
| 当前注册字体不足、系统字体、网络字体与vault持久化 | **[runtime-fonts](references/runtime-fonts.md)**：有明显收益才扩充，系统／网络分级授权，核对保存与重载；插件EA能力不等于已有MCP字体工具 |
| 矩阵、数学向量／转置、分式、求和、递推／上下标、中文混排 | **先读[数学分流](references/visual-content.md#数学内容分流-先认语义再选元素)**：源TeX→原生LaTeX资源→实际尺寸→PNG专项验收；RTL信号名与位串不误转换 |
| 验收等级、合法叠放／文字遮挡、分级评审 | **[acceptance](references/acceptance.md)**：新图先问review，medium仅推荐；用户需求逐项覆盖、同文件任务累计历史、可读局部PNG与逐项误报证据，不强制全部箭头绑定 |
| 箭头/路由/固定圆角、缩放/旋转/排版、交叉、动画/导出 | [layout-export-animation](references/layout-export-animation.md)：绑定保持、真实半径、PPT宽箭身、有限预算；动画须播放验证 |
| 用户素材库、ALU/MUX、模板底板 | [library-catalog](references/library-catalog.md)：list/query/get/preview真实item；先尺寸适配再插入/填字/接线，不把scale1当fit |
| 网上/远端图片、公式资源 | [images-assets](references/images-assets.md)：实际字节/许可/宿主附件；远端路径非宿主路径，MCP可data:image，整个请求4MiB |
| draw、多边形、cuboid、brace、callout、代码、checkbox/高级连接 | [native-features](references/native-features.md)：真实原生operations，不弹面板等待；手绘freedraw不等于Rough.js profile |
| 自定义SVG组件、可复用符号 | [svg-components](references/svg-components.md)：真实DOM测量/viewBox、可编辑carrier/anchor，不用正则冒充通用SVG parser |
| 多色／单色图标、本地SVG目录、动态描边／填充／线宽 | **[icons](references/icons.md)**：svgLayers矩形载体、源色与整体style优先级、解析／许可边界、当前宿主小样验证 |
| ECharts 数据图、多系列/堆叠/双轴/数值XY | [visual-content](references/visual-content.md)：16个已发布示例、12种可视类型＋custom；当前MCP用真实options，不把UI类型名塞进旧Bridge枚举 |
| shadow/gradient/rich text/list/bullet、行内公式 | [visual-content](references/visual-content.md)：受控Feature、真实源与Engine、公式层级/关联恢复；不执行任意gradient代码 |
| 脑图/折叠/Markdown、WaveDrom、Git/GIF | [special-diagrams](references/special-diagrams.md)：真实root/parent/ID和runtime；PNG不证明动画多帧 |
| hover/checkbox/zoom/detail/layer/outline/thumbnail/link/follow | [interaction-navigation](references/interaction-navigation.md)：真实鼠标/键盘验证，不只写metadata |
| table/保留站/寄存器表、no-bind/dynamic library/recognition/clipboard等 | [capability-map](references/capability-map.md)：表格直角连续网格、表头/正文分色、实测列宽；复用当前create_table与元数据，不预设未来Table能力 |
| 宿主Action/Engine、URI、可信脚本/授权 | [script-execution](references/script-execution.md)：明确目标和已注册命令；URI分发≠完成，无任意script MCP/白名单自动授权 |
| CLI/本地EA、首次连接/远端部署 | [native-cli](references/native-cli.md)、[agent-setup](references/agent-setup.md)：真实status/schema、私有凭据；不能在无GUI远端connect/start |
| 完整摘要、并发、复杂局部修改 | [workflow-details](references/workflow-details.md)：精确值/分页/绑定、原生变换锁定与Hook边界、旧图局部修正 |

“绘图脚本目录”取插件settings.scriptFolderPath，不假设个人路径；受管脚本在Agent-Drawing子目录。Token只留私有状态目录，不打印/放图/报告；不自动授信、autorun或改全局主题。mode=remote时渲染在宿主，PNG/ledger属于远端，MCP ImageContent已可看，不需要X11。

交付真实vault文件、最终PNG、check/保存结果、review轮数与剩余限制；本包CLI与MCP共用ledger及delivery门禁，插件原生CLI-only无ledger时须明确记录实际评审。任何能力都以真实入口/源/API和实际运行证据为准，不捏造工具或完成状态。
