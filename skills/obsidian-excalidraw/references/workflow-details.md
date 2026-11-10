# 详细工作流、完整摘要与局部编辑

常规新图先使用主 Skill 的低往返路径；本参考保留逐项控制、并发、完整摘要和高级修正规则。组合检查仍调用同样的真实check和preview，并非省略验证。下文逐项plan/apply适用于需要先审查计划或手动布局的场景，不要求所有简单图逐个往返。
本页代码路径中`references/...`、`prompts/...`仍相对Skill根目录；Markdown链接按本页位置解析。

## 启动、表达与交付的执行契约

`drawing_begin(request,action:"prepare",diagram_type:"auto",file_path?)`返回真实宿主discovery、所需文档全文/路径/sha256、原生调用示例；可选file_path读取当前画布和文件级review证据，不创建/改图。不能用过去一张PNG或聊天中的“已生成”覆盖当前状态。`create|bind`需要已解决的brief；prepare不代表用户批准了默认值。

教学／机制图可先传`drawing_begin(prepare,design:未确认TeachingPlan)`取得简短design_options，交给真实ask；确认后创建时存入brief.teaching_plan。问题是“用什么可视结构解释”，不是形状或配色。当前通用general也不能跳过明确教学意图。[字段与原生编码](teaching-design.md)。render不自动review；逐goal expression_checks和交付状态在CLI/MCP共用同一ledger。


`drawing_apply.operations`是按`op`判别的原生模型联合，完整列出各操作字段，不再是任意dict。整个批次先校验，CLI/Python同样执行；不把错名自动改成近似动作。fontSize/fontFamily/lineHeight放style，label字体放label.style，粗体走set_text_global_style。未知op、错层字段、非有限数和错误引用给出路径与修正提示，committed=false；宿主仍负责Feature config/customData授权、能力和资源验证。connect端点/waypoints保留原生坐标语义，ref引用用`@name`。

逻辑微架构／电路在原有brief的task_id/preferences/requirements之外增加以下字段。它是对需求的可检查承诺，不是绘图DSL；物理结构／讲解页改用[visual_plan](visual-design.md)，不能自动判断承诺是否忠实：

```json
{
  "diagram_type": "microarchitecture",
  "representation": {
    "components": [
      {"id":"alu","role":"compute","types":["rectangle"]},
      {"id":"rf","role":"storage","types":["rectangle"]}
    ],
    "ports": [
      {"id":"result","component":"alu","side":"right","offset":0.5,"direction":"output"},
      {"id":"write","component":"rf","side":"left","offset":0.5,"direction":"input"}
    ],
    "signals": [{"id":"writeback","source":"result","target":"write","orthogonal":true}]
  }
}
```

microarchitecture/circuit必须有部件、端口与网络；明确逻辑网络不能用general降级。physical_structure/explanatory_page需要visual_plan的目的、视图、对象、关系和示意边界，不套端口网表。component.types禁止text；formula角色只能image。逻辑ID唯一，端口方向/引用一致，不得把所需独立器件合成单个阶段。

创建后`drawing_contract(context_token,bindings:{"alu":["真实bodyID"],"rf":["真实bodyID"],"writeback":["真实wireID"]})`。部件映射一或多段闭合轮廓/shape；每个信号映射一条连续native line/arrow；不能复用元素冒充独立对象。端口为**部件世界AABB边上的side/offset**，不是标签坐标；quarter-turn后按世界边理解side。容差1 scene单位，不随PNGscale变化。复杂符号的实际stub不在AABB边上时需合适几何分解，不可谎报端口；不宣称通用电气引脚解析器。

映射验证成功才保存，失败返回带logicalId/native IDs/actual/repairHint的REPRESENTATION_*问题；check/review/deliver每次按当前全图重算。移动器件后必须修邻边。缺body/wire、对角信号、错误端点或绑定矛盾是硬错误，不可视觉豁免。任意旋转和平滑/曲线的精确拓扑尚不支持，会明确阻断；负全局/local坐标和quarter-turn按世界点列检查。非绑定示意线合法，但端点仍须符合声明。

`drawing_deliver(context_token,revision,preview_id)`核对同一owned file/当前revision/完整全图PNG及hash、最新completed review、当前需求和表达检查，符合才返回`status:"deliverable"`。局部PNG、过期状态、未评审或后续失败均不签发；返回原始check状态与advisories，不伪造raw pass。最终回答引用真实文件、PNG、轮数和限制；交付失败只报告未完成。用户/视觉证据仍是Agent自述；门禁不能控制任意聊天文字，也不是RTL、电气、科学或绝对审美证明。

CLI同实现：`launcher.py cli -- begin|contract|deliver --request-file args.json`，或json入口的drawing_begin/drawing_contract/drawing_deliver。不要将三选一的竖线写成实际shell管道。


## 多 Agent 并发：一人一图，宿主排队

- 可并发规划/提交**不同画布**；由一个协调者完成连接/启动，工作Agent只status，不并发connect/start/reload切服务。
- 每个Agent用唯一filename创建，或明确file_path绑定；保留自己的file/contextToken/revision。Bridge0.13.1用独立new-tab而不是可能复用相邻面板的new-pane，第三张图不自动替换前图。请求绑定具体view+文件，不随当前焦点切换；用户主动关闭/切文件后token仍会失效，按原file重新bind。
- Bridge所有请求共享串行队列与EA workbench，包含异步图片/PNG导出；不会交错污染工作台，但不是多线程同时渲染，慢导出会让其他请求等待。一次plan→apply→check→PNG不是跨请求原子操作。
- 同一文件不建议多Agent同时写，即使token不同也是同一内容；相同baseRevision的竞争只允许首个提交，其余REVISION_CONFLICT。重新读后重新规划，不自动覆盖。复杂compose/present分阶段提交，保留失败时已执行集合。
- Bridge0.13.1起revert只找**本文件**最近事务，不再被别的画布最后一笔阻挡；仍需revision未变，历史全Bridge最多20笔，不保证无限撤销。默认PNG路径唯一；明确out_path不要让两个Agent共用文件。
new-tab是Agent默认的独立视图选择，不表示分屏无用：需要人工并排比较时可手动分屏，或使用确保新建独立leaf的宿主API。当前插件new-pane会受openInAdjacentPane设置影响，可能复用别的图；不为自动绘图擅改用户的全局分屏偏好。

## 完整摘要与 PNG 坐标反馈

`drawing_read(context_token)`默认返回全部未删除元素，`coverage:"complete"`、count/total、file/revision、precision:2以及`bounds:{minX,maxX,minY,maxY,width,height}`；空画布bounds:null。bounds使用PNG相同的原生世界边界计算，处理负坐标、旋转与负local points，不是简单max(x+width)；不含导出padding、阴影/箭头装饰或frame标题的额外像素边缘。

元素必含id/type/x/y/width/height；坐标与尺寸**最多两位小数的JSON数字**，不补无意义的`.00`。有文字/标签时含text；有关系时含bindings.boundElements/startBinding/endBinding/containerId；按需保留groupIds/frameId/parent/locked、angle、fontSize和扩展类型。可选字段缺省表示空关系、空组、无frame、angle0或locked:false。旋转/点列元素另有原生世界bounds。默认摘要不含元素version：正常写入由全图baseRevision防止覆盖；确需expectedVersion时按ID读取detail:"full"，不修改原生版本机制。

摘要不回传脚本、大options、完整点列或压力数组；用pointCount。超过160字符的text截断并标textTruncated/textLength，不把摘要截断当作原文字丢失；按ID用detail:"full"取得完整内容/精确坐标。四舍五入仅用于反馈，绝不回写原场景。大场景可offset/limit分页，coverage:"page"+total/truncated；ids查询coverage:"ids"，不是全图证明。

`drawing_preview`除真实PNG外同时返回**同file/revision的canvasSummary**，格式就是上述完整摘要；局部PNG也附全图摘要。外层bounds/transform描述本次导出区域，不与canvasSummary.bounds混淆。PNG像素到scene坐标：`sceneX=sceneOrigin.x+pixelX/scale`、`sceneY=sceneOrigin.y+pixelY/scale`；图片阅读工具若缩小显示，先把显示位置换回PNG原像素。比如原PNG应右移60px、scale=1.5，就用`translate {targets:[id],dx:40,dy:0,includeBoundText:true}`；不要用截图像素直接写x。

先从PNG+text/type/ID识别对象，再按摘要估计偏移，必要时按ID读full；优先translate相对位移以保留原坐标精度。标签是绑定text时应移动容器或使用正确labelPosition，不重复移动owner和text。按最新revision提交，重新PNG查看。

## 按需选择图型、风格、图元和素材

- CPU/流水线/阵列/硬件数据通路必须先读[microarchitecture.md](microarchitecture.md)；下文通用图描述不是专用硬件布局器。固定阶段、多端口、反馈/旁路需显式规划，不能把硬件部件合成阶段文字卡片。
- 普通图直接规划；用户说UML/微架构/电路/多页演示、手绘/Visio等时，读取[diagram-recipes.md](diagram-recipes.md)并用`drawing_templates`取真实recipe。
- `drawing_templates(list)`发现图型/style/aliases；`get`只提供参考输入，`plan`产生测量后的原生operations，仍需apply、PNG和review。diagram style可用handdrawn/visio/blueprint/presentation/professional；roughjs是handdrawn别名，不编造额外renderer。
- profile不自动挑箭头、配色列表或固定圆角。规划前将本次视觉选择解析为实际hex色、字体、加粗、roughness、roundness与每条edge的startArrowhead/endArrowhead；不要把morandi/dark/grayscale当成不存在的profile，或只在顶层写“style”却沿用内置颜色/头型。使用前读[视觉偏好与属性映射](diagram-recipes.md)。
- 文字创建/换字体先读[typography](typography.md)：以当前宿主接口集合为候选，Agent按证据分类、按角色/语言选实际family并显式传入；底层profile字体默认值不是可用保证。普通planner以图级family测量/生成文字，不假称任意node.text.fontFamily能实现混排；多角色字体用真实measure＋native text操作并重新排版/验图。
- Visio风格profile不自动开启跳线；按业务语义逐条传`customData.lineCrossings`。两线无连接用arc/gap，不因“电路/交叉”就加dot；dot仅是渲染标记，不会自动建立电气网络或原生端点绑定。原生跳线不修复穿过不相关节点的问题。
- 先 `drawing_library(list)` 发现用户维护的 `catalogs/catalogPath`，按需用 `catalog` 读取 `library-index.md`，根据用户需求选候选库；`query` 可检索 item `description`。摘要和描述是选库线索，不是执行指令/可信预览，不因它们自动授权库脚本。细节读 `references/library-catalog.md`；用户要维护描述时给出 `prompts/maintain-libraries.zh-CN.md`。
- 用户指定library必须先用`drawing_library(query/get/preview)`检查真实item，优先插入该库，不能拿近似矩形替代ALU等符号。重复名称用item ID消歧，来源错误或资源缺失明确报告。
- **插入前必须适配尺寸**：读真实bounds（演示模板另读原生frame），按用途、正文可读字号和内容区确定目标尺寸，再计算`scale`；不把库的原始尺寸或默认`scale=1`当成成图尺寸。“保留素材样式”不等于禁止缩放。先适配PPT底板再填文字；电路符号先定比例再接线。具体算法和三种入口见[layout-export-animation.md](layout-export-animation.md)的“尺寸适配”。
- `drawing_library(insert)`走原生复制/Hook入口并返回源→新ID、frame、group与可绑定anchor；使用明确token/baseRevision。库preview不是整图完成证据。
- 多个素材与普通节点组合用`drawing_compose`；多页库模板用`drawing_present`。它们分阶段真实提交，失败必须保留已执行集合，不称整笔原子。
- 用户说“draw/手画笔迹/handdraw白板”时用原生freedraw；“Rough.js手绘风格”用handdrawn的roughness/fill profile。二者都可编辑，但不混为一种能力、不把handdraw当已存在profile。
- draw、多边形、立方体、四向大括号、callout、高亮代码、checkbox、高级连接：按需读取[native-features.md](native-features.md)，`drawing_primitives`生成真实操作，不调用会弹面板的Action脚本等待用户。
- 多页演示保留原生frame与每页元素，逐页导出并实际看图；不能只看缩小overview就判断所有页可读。未调用真实PPTX导出工具，不声称已经生成.pptx。
- 多页intro可能有多个title/full-name占位；必须按sourceIdMap完整替换，不能只填一个留下旧英文。slides已有原生bullet时新文字不要重复加Unicode项目符号；派生bullet保持同一library instance并纳入原生frame/group。
- 样式和文本字段放在operation的`style`对象，例如`create_text {...,style:{fontFamily,fontSize,strokeColor}}`；不是任意顶层fontSize。没有节点的标题/注释直接create_text，不把空nodes传给图规划器。
- 使用CLI/eval时必须定位当前安装包的launcher.py/runtime，不导入工作区旧原型。先用drawing_setup(status)返回的config_path/state_directory确认连接，子进程显式共享EXCALIDRAW_AGENT_CONFIG或STATE_DIR（只传文件路径，不打印token）；不要因临时脚本换cwd丢配置后称Bridge未授权。

## 扩展能力路由：不要只会基础图元

用户提到下列能力时先读取对应参考；已有adapter优先MCP，无adapter用已授权的宿主EA/URI脚本。脚本存在≠已部署、Engine已运行≠PNG包含所有效果。
完整来源/缺口对照见`references/capability-map.md`；另外列出table/link/follow/no-bind/dynamic library/recognition/clipboard等现有机制。不要把本文未展开的能力视为不存在，也不能把“来源清单”当成新MCP接口。

| 需求 | 按需参考 | 执行重点 |
| --- | --- | --- |
| 从网上找图、照片、截图、图标并插入 | `references/images-assets.md` | 搜索真实来源→获取/解码图片→保存宿主附件→原生image→PNG；不能把远端路径当宿主路径 |
| 文字与`$公式$`混排、上下标/希腊字母未渲染 | `references/visual-content.md` | 复用latex/Action-Extract-Latex；检查MathJax、选中真实text、转换副本后迁移group/frame/容器关系；远端无宿主脚本入口用create_latex+原生text组合 |
| 用SVG path制作任意静态符号、独立组件/素材库 | `references/svg-components.md` | 两个Digital生成脚本的真实DOM测量/归一化、line carrier+svgViewBox、分色子图元/文字/组/anchor；不拿正则当通用SVG parser |
| mindmap、折叠脑图、Markdown导入导出、WaveDrom波形、git/GIF | `references/special-diagrams.md` | 脑图树与实际ID、native close状态；波形源与runtime；git未发现专用脚本，不擅改成gif |
| hover、line-highlight、zoom、detail、checkbox、layer、outline、thumbnail | `references/interaction-navigation.md` | 元数据+持久Engine+真实鼠标/键盘/缩放验证；静态PNG不证明交互 |
| shadow、callout、code highlight、gradient、rich text、list、bullet | `references/visual-content.md` | 受控Feature配置，区分渲染型列表与真实bullet元素，保留源码与绑定 |
| distribute、特殊arrow、animation、step-appear、Anki/Eagle/export | `references/layout-export-animation.md` | 群组排版和独立元素不同；动画需播放验证；外部软件写入需明确授权 |
| PPT底板太小、素材/电路符号尺寸不合适、整组放大缩小 | `references/layout-export-animation.md` | 先读bounds→计算目标比例→插入scale或原生scale_selection；不是调整PNG导出scale |
| 交叉线弧跳/留白/实心交点、替换白色遮罩 | `references/layout-export-animation.md` | 原生line/arrow的lineCrossings；MCP已有create_linear/connect/patch_custom_data，无需新Feature/Engine |
| 运行/开发绘图脚本或挂载额外Engine | `references/script-execution.md` | 明确目标与命令、URI分发不是完成、常驻Engine不走一次性CLI |

按当前Skill根目录读取表中相对文件，客户端提供时也可用`skill://obsidian-excalidraw/<相对路径>`。缺依赖/交互条件要精确报告，不捏造工具、不把面板启动说成能力完成。用户只要求效果时使用已有机制；用户明确要开发脚本时修脚本并重跑，而不是只手工修画布。图片/交互/查阅/动画不因默认原生shape优先被忽略。

## MCP 路径：自然语言到真实操作

1. 若有 `drawing_setup`，先调用 `status`。未连接时，在用户目标已明确或仅有一个合法 vault 时调用 `connect`；多 vault 歧义才询问。它部署 bundle、生成私有凭据、通过实际 Advanced URI 启动；没装 Advanced URI 则报告返回的准确手动命令，不能声称启动成功。已配置但 Obsidian 重启后用 `start`。然后 `drawing_context(action="discover")` 核对 Bridge、字体与 Engines。无效令牌、缺插件/画布不能假装已有连接。
2. 新图先真实ask收齐未定style、review、色板、背景、字体意图；再`drawing_context(action="create",filename=描述名,foldername="Agent-Diagrams",brief=已回答偏好与用户需求)`。已有图明确file_path绑定，首次写入前补brief；read／measure不需要。记录任务ID、file、token、revision，同任务重绑继承文件级评审历史。
3. `drawing_read(context_token)`读取完整两位小数摘要和全图min/max边界；不是几个选中元素。保留file/revision与初始状态。
   在任何text helper／字体测量前分类数学公式、普通说明、RTL信号／代码、bit流／波形。矩阵／数学向量／上下标等按[数学分流](visual-content.md#数学内容分流-先认语义再选元素)创建LaTeX资源；信号和位串不误转。把数学清单关联到brief需求，保留ref→真实image/fileId→源TeX供专项验收，不新增虚构操作参数。
4. 组织简短图描述并调用 `drawing_plan(context_token, diagram)`。规划器使用真实字体/内容尺寸，负责换行、节点尺寸、分层和避障；不要按字数猜宽。
   - `kind`: flowchart/architecture/swimlane/freeform。
   - `nodes`: `id, shape, label, variant?`，shape用rectangle/ellipse/diamond；`content`支持image/latex/echarts/embeddable；其它复杂几何用实际native operations。
   - `edges`: `id, from, to, label?, fromPort?, toPort?, startArrowhead?, endArrowhead?, style?`。头型放edge顶层，显式`null`是无头，不是字符串"none"；不依赖默认arrow。端口用top/right/bottom/left；循环/回边保留，必要时`feedback:true`。箭头大小/宽箭身通过返回refs后的已有操作补充，见layout-export-animation。
   - `containers`: `id,label,members`；可見背景与表头。`groups`只是一起移动，不替代容器。
   - `lanes`: `id,label,members,color?`；实际名称swimlane，接受用户所称swimeline，别写不存在的customData.swimeline。默认竖列泳道+TB流程。
   - `layout`: direction TB/LR，nodeGap/rankGap、origin、padding可按用途覆盖；默认通常足够。`position`是scene坐标，可为负。
   - 每项logical ID唯一；缺失关系目标必须修正，不能补造用户未要求的业务节点。
5. 将返回的 `operations` **完整**传给 `drawing_apply(context_token, base_revision=plan.baseRevision, operations=plan.operations)`；不要手抄删掉绑定/标签/元数据操作。大输出可通过真实CLI或eval导入DrawingClient完成plan→apply，保留生成的plan/result文件，不写mock。
6. 记录返回的native ID/refs；再读取最终状态。现有插件可能调整容器与箭头，不能只看计划坐标。

图描述示例：

```json
{
  "diagramId": "request-review",
  "kind": "flowchart",
  "title": "访问申请流程",
  "nodes": [
    {"id": "submit", "shape": "rectangle", "label": "提交访问申请", "variant": "primary"},
    {"id": "review", "shape": "diamond", "label": "身份、权限范围和资源使用条件是否全部通过审核？"},
    {"id": "grant", "shape": "rectangle", "label": "发放凭据", "variant": "success"},
    {"id": "reject", "shape": "rectangle", "label": "拒绝并说明原因", "variant": "warning"}
  ],
  "edges": [
    {"id": "submit-review", "from": "submit", "to": "review"},
    {"id": "approved", "from": "review", "to": "grant", "label": "通过"},
    {"id": "denied", "from": "review", "to": "reject", "label": "未通过", "fromPort": "right"}
  ]
}
```

## 每轮：check → PNG → 看图 → review → 局部修正

**默认 max_rounds=5。每次当前状态的 check+PNG+视觉review计一轮，初图也计入；不是必须画五遍。** 达到要求立即结束。连续两轮问题/严重度无改善或达到上限时needs_attention，报告剩余问题，不标完成。
review新图先询问，medium只是推荐；仅明确授权默认／原图继承才省略询问。通过brief固定选择，不能在check／apply／review时降低等级；同文件／任务重绑继承轮次、expected与未解决项。[acceptance](acceptance.md)规定局部PNG证据、需求覆盖与逐项误报处理；不能只填visual_reviewed=true。

1. `drawing_check(context_token, expected=语义断言)`：断言节点存在、方向正确等。读取issues中的native IDs；结构通过不意味着业务或美观通过。
   - `expected`示例：`{"type":"label_equals","id":"实际节点或文字ID","text":"完整内容"}`、`{"type":"edge_label","from":"起点ID","to":"终点ID","text":"通过"}`；节点字段是`id`，不是`target`。
2. `drawing_preview(context_token, base_revision=check.revision, scale="auto", padding=20)`：默认预算避免大scale与包缓存内输出。除非用户明确指定外部交付路径，不传out_path，使用本机持久化artifact目录；不要把PNG写进版本化安装包。全图用于整体结构；小字/扩展内容再用ids局部PNG。`complete=false`或资源错误不能当成功。
3. **实际查看返回的PNG**。MCP返回image block；CLI输出则用当前Agent真实的图像读取工具打开out_path。没有图像查看能力就记录visual_reviewed=false并明确限制，不要求所有客户端都有名为read的工具。
4. 检查：内容与方向、长中文完整、文字是否在形状有效区域、表头/正文分离、对齐与间距、连线路径/箭头头/标签、图片/公式/图表/嵌入是否真出现、整体层级与配色。用同revision的canvasSummary识别ID和位置，再用transform.sceneOrigin/scale把PNG偏移换算为scene位移；无需从图片猜完整坐标。
   - **程序check=pass仍可能缺标签或不好看**。逐项核对用户要求的所有节点全文与分支标签；不要仅核对edge.from/to存在。普通节点内容用`label_equals`，分支标签用`edge_label`语义断言。
   - **公式源码泄漏是未完成问题**：检查所有普通text中的数学`$…$`/`$$…$$`及LaTeX命令，不把字面源码当公式。对照原文核对每个公式资源的源TeX与PNG中的根号、分式、上下标、希腊字母；转换后重新检查尺寸/行距和绑定。普通文字测量、几何check或rich_text不证明MathJax解析成功。用户要求显示源码/货币字面量不做误转换。
   - 长中文菱形不要横向撑成整张图的主视觉。优先增加合法换行与适度高度，保留至少正文内边距；检查决策宽度是否远大于同类节点、是否因此产生多余空白。
   - “通过/未通过”应贴近决策出口对应路径且左右归属明确，不贴到整张图的最外缘。可对绑定text的`labelPosition`（0–1的路径比例）作局部调整；普通两点直连默认0.5，决策/多段路径默认0.28，显式位置保留。自动LR布局按实测标签宽预留rank间距；手动position/特殊端口仍需PNG复核，不宣称所有路线自动无冲突。
   - 同层分支大小和基线一致；只为给标签空间才增间距，不能把“无重叠”做成过度疏散的大画布。初图用planner默认nodeGap/rankGap，先看PNG再有理由地覆盖。
   - 组件库端口要实际贴合路径stub，不能因绑定落在透明anchor bbox就称连接正确；按当前svgViewBox/carrier尺寸计算端点。未声明电气引脚时不以“0.28/0.72”等固定示例取代真实图形。
5. `drawing_review`提交当前revision／previewId、真实visual_checks／visual_issues，以及逐项`requirement_checks`的真实ID和覆盖说明；medium至少content/readability/occlusion，high再connections/hierarchy_style。小字或文字误报须带当前已查看可读detail_preview_ids；dispositions逐项匹配元素ID、preview_id及独立理由，文字冲突不可intentional。原生check失败不等于review一定失败，但不得把豁免后的completed说成rawCheckStatus=pass。
   - 只有实际看图后才填true。
   - 视觉问题用稳定code、elementIds、severity error/warning、reason、repair；不拿任意审美分数替代问题。
   - `completed`后调用`drawing_deliver`核验同一文件/revision/PNG再交付；`continue`按问题修正；`needs_attention`停止自动修改并报告未满足项，不规避ledger换token继续刷轮数。
   - 新会话/重绑后旧contextToken可能失效；按file重新bind是恢复路径，不是新的质量预算。保留之前review轮数与问题记录，累计至原max_rounds，不为同一任务换token规避无进展停止。
6. **修复明确问题，而不是每轮重建**：只修改问题对象、绑定文本及必要邻边。`drawing_apply`使用最新revision；局部修正后重复check和PNG。即使只改一行字也需要最终图检查。

停止标准：语义清单完整、资源完整、真实看过当前PNG，本等级阻断项已修复或对具体几何候选有当前视觉依据，review=completed；advisories/未支持几何与人工判断理由交付时披露，不称全部自动证明。工具错误、无进展或带不可读缺陷不是完成。

原生CLI路径也必须检查内容、绑定、保存结果并实际看PNG，采用相同最多5轮/无进展停止规则；没有MCP check/review时按native-cli参考记录真实评审过程和未覆盖约束，不编造check=pass、previewId或ledger。Native CLI更新后若回到MCP，重新读取它的revision并导出注册预览。

## MCP 路径：局部修正操作

先读取目标详细元素：`drawing_read(context_token, ids=[...], detail="full")`。优先这些操作，不直接改scene JSON：

- `set_text {target: body或text ID, text:完整新标签}`；长文本先`drawing_measure(..., width=目标有效宽度)`，使用返回的换行text与真实尺寸；必要时resize容器。
- `translate {targets:[ID],dx,dy,includeBoundText:true}`；同时移动容器和已包含的bound text时去重，避免二次位移。
- `resize {target,width,height,anchor:"top-left"}`：改变单个非line/arrow元素的尺寸，可重排绑定文字，但不是整组缩放、不等于字号缩放；不能只resize模板frame/外框就声称整页已适配。图片保持宽高比，复合素材用`scale_selection`；读取最终容器与邻边状态。
- `rotate {groupId:真实group ID,degrees:90}`或`rotate {targets:[ID...],degrees:90}`：相对旋转，正数顺时针，默认选区共同中心。二选一，不把各元素单独angle+=90当整组旋转。
- `scale_selection {groupId:真实group ID,factor:1.5,fromCenter:true}`或明确`targets`：复用宿主手动多选缩放，统一缩放位置、尺寸、点列和文字；不是逐个改width/height。默认中心不动；fromCenter:false固定多选边界左上角，单个已旋转元素固定其本地西北角。详见`references/layout-export-animation.md`。
- `patch_element {target,patch:{x/y/width/height/angle/points/合法样式}}`；angle是绝对**弧度**，如π/2=90°，走原生旋转维护绑定文字及相邻箭头。线的points是局部坐标，首点[0,0]，其余可负。
- `connect {from,to,start:{anchor,mode:"orbit"},end:{anchor,mode:"orbit"},waypoints:[scene点],label?,elbowed:true,style?}`。
- `rebind_arrow {arrow:箭头ID,startTarget:节点ID,endTarget:节点ID,start:{anchor,mode:"orbit"},end:{anchor,mode:"orbit"},preservePoints:true}`：更新双向绑定；另用patch_element更新局部points。不能直接patch startBinding/endBinding/boundElements。`unbind_arrow {arrow:箭头ID,end:"start"|"end"|"both"}`按实际capabilities使用。
- `patch_element {target:箭头绑定text ID,patch:{labelPosition:0.2}}`：保持原生绑定而调标签路径位置；实际PNG复核，不能只改x/y却被引擎重新居中。
- `patch_custom_data {target,merge:{安全元数据},remove:[字段路径]}`；是merge，不是patch。
- 原生交叉线：`patch_custom_data {target:line或arrow ID,merge:{lineCrossings:"arc"|"gap"|"dot"|"none"}}`；批量修改是在同一apply中为每条ID提交一项，不是targets字段。两条线需确定覆盖优先级时都设数字lineJumpPriority。详见layout-export-animation；不要用白色矩形代替gap。
- `set_feature {feature,targets:[ID],config}`用发现的spec；gradient接direction/stops，不接模型生成代码；shadow只有px字符串是像素。
- `delete {targets:[过时元素ID],cascadeBoundText:true}`：只删除明确被本次修复替代的箭头/图元，默认连带删除其绑定文字并解除相关引用。删除旧关系后核对新关系仍存在；不能为了消除交叉删除用户业务关系。

不要将反馈四舍五入的坐标整条回写。不要为了消除穿线删掉跨组关系、缩短业务内容或移用户锁定元素。REVISION_CONFLICT时重新读受影响数据，不覆盖用户新编辑。
整组选取先读取groupIds；显式targets不会自动扩展所有同组元素。绑定文字随容器且不重复变换；Frame缩放包含子元素但不能旋转。选中箭头却遗漏其绑定端点会拒绝，不静默解绑；只选节点时外部箭头跟随而外部节点不变。选区/受影响绑定文字或邻边锁定则整笔拒绝。MCP staging不触发可能写live API的afterTransformElements宿主Hook，不宣称复现泳道吞并/剥离或表格边界联动。任意角度可执行；只有90°整数倍纳入现有几何检查，其余仍unknown并需PNG。

## 扩展与边界

ECharts由真实options保留数据，泳道由真实Engine管理；customData.document/任意gradient代码不是默认接口。PNG对DOM内容需要捕获adapter；无法捕获会标incomplete，不能用边框或空白冒充正文。曲线/旋转检查若unknown，明确剩余限制或改为用户允许的可检查表达，不伪称全部校验通过。

LaTeX先看discovery中的`latex.available`：当前插件源码可能通过独立Excalidraw Extras MathJax组件加载；缺依赖会明确LATEX_PREREQUISITE_MISSING，不要等待一个无人确认的弹窗或拿公式普通文本/假图片替代。混排提取脚本也依赖此能力；它不在默认bundle/公开脚本MCP中，真实入口、删除原文字及关系恢复见[行内公式流程](visual-content.md)，不能只写“已支持LaTeX”而省掉转换。

## 原因不明时：可选 CDP 只读诊断

`read/check/PNG`无法解释错位、遮挡、字体、原生表格或资源状态时，读[cdp-readonly](cdp-readonly.md)。先`drawing_debug(status)`，未启用则向用户提供“保持关闭／开启只读”的选择；不自动改配置、启动调试宿主或SSH转发。

只读采集明确已打开的宿主vault和file：固定JS＋V8 `throwOnSideEffect`，不提供Input、任意evaluate、断点、保存/导出或写API。取到真实ID和原因线索后，使用正常入口重新read最新revision，再提交用户任务已授权的最小patch；DSL受管对象更新源/state，不能CDP直接改。用户仅授权诊断时只报告，不微调。最后仍需PNG/review；诊断fingerprint不是Bridge revision。

## 交付

给出真实vault文件、最终PNG、实际保存/校验结果、评审轮数和剩余问题。MCP交付ledger；原生-only明确没有MCPledger并列实际评审记录/检查边界。保留原生可编辑场景，以最后一次真实PNG和校验为准。
