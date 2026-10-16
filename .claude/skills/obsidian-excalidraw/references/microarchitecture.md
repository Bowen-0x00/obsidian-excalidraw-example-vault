# 硬件微架构：先表达部件和信号，再绘图

## 强制分流与任务边界

用户说CPU/流水线/微架构/数据通路/缓存层级/寄存器堆/阵列/互连/加速器时，**在创建图元前读取本参考**。不是普通服务架构图；不能因为主Skill有低往返路径就直接提交一列nodes+edges。速度优化只减少JSON复制和模型往返，不降低结构粒度。

先区分用途：系统/模块概览、微架构块图、详细数据通路、门级电路。用户未进一步说明“微架构”时，默认**部件级＋关键端口/信号**；不能自行降成五阶段说明或功能列表。无需追问普通视觉细节；只有ISA/流水级/分支解决位置/目标实现差异会改变结构且无依据时，问一个关键问题或明确声明保守教学假设。用户给了真实架构/RTL/论文则以真实资料为准，不补造容量、带宽、流水级或功能。

三类参考表达的要点：TPU式是存储/阵列/控制/带宽与回流，RISC式是流水边界/MUX/命名端口/旁路网络，南湖式是层次区域/队列/重复执行单元/存储层级。矩形并非错误；**把不同部件都做成同尺寸文字卡片、把信号都做成模块间关系箭头才是错误**。不是每个抽象模块都必须画门级图标，也不是强制所有架构套五级CPU。

## 创建前的硬件计划（简短表，不是新DSL）

先在Agent工作计划中确定以下内容，不要求用户手写JSON：

1. **已知事实与假设**：用途、抽象层级、ISA/时序边界、数据宽度/数量/容量的依据；未指定不猜具体型号指标。
2. **部件清单**：每个需要讨论的ALU、MUX、RF、存储、流水寄存器、队列、控制器、阵列/执行lane是独立对象；记录角色、阶段/区域和重复数量。不把关键部件仅写进阶段框的bullet。
3. **端口表**：部件的输入/输出/控制端口、数据宽度及方向；区别数据值、寄存器号/地址、选择/使能和状态。RF读/写端口、MUX数据/选择、ALU A/B/result、memory addr/wdata/rdata/we不要接成同一个中心点。
4. **信号表**：`source.port → destination.port`、数据/控制/反馈/旁路类别、时序跨哪个寄存器、必要的总线名称/位宽；一条值不能靠“数据+控制”标签代替其明确路由。可聚合明确的控制bundle，但必须在消费端拆解/标明。
5. **空间骨架**：流水级固定列/行、边界寄存器狭长条、主通路和旁路/控制通道、存储/阵列形状、主标题/图例。这不是普通有向图的拓扑rank。
6. **验收清单**：每个部件/关键端口/关系必须在画布中真实存在；哪些关系可合并为总线、哪些细节明确省略。后续报错不得偷偷改变这份清单。

计划按实际任务展开，别先生成几十个空字段的大DSL。`customData.agentDiagram`可保存logicalId/role/原文及Agent注释，但注释不是电气网表、实际绑定或新MCP参数。

## 提炼后的制作与迭代流程

流程不绑定某个模型名称或thinking档位；换更强模型不能替代清单、坐标与读回。上轮有效经验是固定阶段、独立端口、分批构图和局部补线；低效经验（源代码漫游、长JSON重抄、整图重放/回滚、越界“局部图”、check后直接completed）**不作为推荐流程**。

| 阶段 | 实际输入/产出 | 进入下一阶段的条件 |
| --- | --- | --- |
| 1. 需求与结构契约 | 明确抽象层级/教学假设；部件、端口、信号/选择码、必需通路清单 | 不可把“存在于说明文字”算独立部件，不补造用户未给的实现指标 |
| 2. 空间与素材准备 | 固定流水列/区域、寄存器边界、端口朝向、数据/控制/反馈通道；发现/测量真实素材 | 真实尺寸和端口stub能放入区域，首末线段沿端口法向引出 |
| 3. 先放部件及端口 | 一批创建节点/轮廓/端口/标签，API生成ID，用ref→实际ID和原生group维护身份 | read核对朝向、尺寸、独立对象和端口坐标，尚未布线不称完成 |
| 4. 按网络分批布线 | 先主数据、再选择/使能、再外围写回/分支/旁路；复用同一端点表计算waypoints | 各段正交、网络/输入数/选择码对应；不是复制模块中心线 |
| 5. 保存后审计 | 读回同file/revision；核对原ID/组件、信号端点、逐段轴向、遮挡和已有expected | 先确定性检查再PNG，错误保留ID并建立issue列表，不删关系求pass |
| 6. overview＋有效局部 | 全图判断空间/角色/轨道；阶段及端口局部判断信号、字高、箭头头和交点 | 必须实际看图；局部bounds/scale确有放大，未读到的部分不称已审 |
| 7. 最小补丁与再审 | 问题→native IDs/原因/修法；只patch points/尺寸/端口/必要邻边 | 每次修改后重读审计及PNG；同一轮记录真实改动、剩余问题与进度 |
| 8. 交付或停止 | 源文件、refs/清单、当前PNG、check和review证据 | 内容/视觉都满足才completed；上限或无进展则保留图、报告needs_attention |

清单/端点表/issue列表可暂存在Agent工作文件或用户允许的元数据中，不是新的服务端DSL。一个协调者拥有画布revision；部件、数据边、控制边可在代码内批量传递，避免每条边单独一轮模型。没有必要先读插件大量源码，已有tool schema/Skill/API可回答的先复用。

每轮开始先核对最新revision，外部编辑则重新读受影响对象。补丁必须附前后不变量：全部原部件/边ID集合、信号from/to、绑定、标签/样式、锁定及frame/group保持，除非这轮明确要求改变。原生属性能维护的关系不手填JSON。若只修正交路由，不能顺手移动硬件、改选择码、改颜色或宣布此前未完成的硬件评审已完成。

## 从硬件DSL成图吸收的制作规则

`hwdiagram/1`的named-grid数据通路实验说明：好看不只因为语法，而是**真实符号/端口＋主体对齐＋独立走线通道＋按用途重新测量**。下列规则可直接用于现有MCP/EA，不要求用户写DSL，也不把实验schema塞进drawing_compose。

- **网络和图面分开。**工作计划记录component、port方向/已知位宽、同一net的全部目的；控制器只有select/enable职责，不因为名字相似就接成数据源。语义归属不强迫可见大框，显示区域也不冒充电气模块。未知位宽保持未知；总线bits不是箭身宽度。
- **按主体/端口对齐，不按带caption的总bbox对齐。**区分body outline、label safe region、pin/stub、用于排版的allocation box。寄存器窄高、MUX/ALU保留原始长宽比，文字过长先外置caption或扩大留白，不把所有符号撑成同尺寸卡片。寄存器D/Q、时钟标记和MUX输入0/1增加辨识；不能为装饰虚构时钟连接。
- **素材先有几何契约。**记录真实item ID、自然尺寸、命名anchor/fixedPoint、出线normal、文字安全区及可否缩放/换色。源库MUX的底部select要求caption移到上方；另一个ALU同名素材可能输出朝下，不能沿用左右引脚。保留用户库原样式，只有声明可替换槽才改色。
- **主通路优先，控制/反馈分轨。**常用左→右主体骨架，控制器放独立上方区域，写回/反馈走外围下方；先为首末stub、位宽短标签、分叉和跨线留空间。caption避开实际引脚，位宽标签贴本信号清晰段，不让控制线穿过名称。少量语义色＋一个重点单元足够，不默认逐阶段彩虹背景。
- **同网fanout不是两条独立业务关系。**可用有身份的原生junction/主干与分支表示，保留源→全部目的的映射及绑定。跨越不同net用原生lineCrossings的arc/gap；dot仅用于真实同网连接，不能用白底遮罩、假弧或把两独立driver画成相连。
- **paper/presentation不是只放大PNG。**换字体/字号、线身/箭头、符号或留白会改变包络，需重新measure/layout/route；语义和网表保持。不要照抄该实验的Helvetica、pt×2、固定节点名或特定库ID为通用默认。队列/寄存器表采用[直角分层表格](capability-map.md#表格清晰表头与连续网格)。
- **保留严格边界。**该adapter实际只实现一个指定7资源数据通路，其他构造fail closed；复杂array/domain/多视图/ELK/Visio不能因schema写了就称已实现。一次Result移动绑定随动，只证明该路径，不证明全部GUI编辑能回写DSL；本地独立DSL的身份/冲突保护也不能被一次性生成器取代。

来源：`hardware-dsl-design/specification.md`的model/view/style/SymbolContract，以及`excalidraw_adapter.mjs:compile/connectionOperations/decorations`、`check_design.py:validate`。指定Presentation画布已实际只读导出检查：46元素、9箭头，仍含4个历史跨线辅助line；新版adapter虽已改原生跨线，**既有画布尚未迁移，不把当前PNG当新版跨线验证**。不擅自修改用户喜欢的原图。

## 现有接口的能力与限制

- `kind:"microarchitecture"`只是已有planner接受的分类，**没有自动硬件符号/阶段列/多端口/bus布线语义**。单纯改kind不能把服务架构图变成数据通路。
- 普通planner按有向边最长路径分层；控制边会影响rank。`containers`是节点排完后的包围框，不会把所有EX单元固定在EX列。需要硬件骨架时用显式`nodes[].position`/实际尺寸、原生create/apply分批构图或库insert，然后显式connect路由。
- compose仍可在代码内完整plan→apply，inspect仍可合并check/PNG；但只在它能保留本计划的硬件拓扑、尺寸和位置时使用。复杂固定列图可以先创建全部部件再一次批量连接，不要求每条线等一个模型响应。
- planner字段是`layout.nodeGap/rankGap`，不是nodeSpacing/rankSpacing；容器成员是`members`，不是children；节点style用strokeColor/backgroundColor。当前容器的逐项style不是通用承诺，使用profile.container/实际region.color或按native refs patch，**输入字段写了不等于生效**。
- 不同节点输入size/position要按当前真实schema；原生图元x/y是scene左上角，线points是局部点且可负，connect.waypoints是scene点。只让API维护ID/version/index与双向绑定。
- 创建时优先省略`id`让API生成原生ID，用`ref`保存长logical名称；后续用refs/read回实际ID。已实测某宿主保存会把新建长text ID规范化为8字符，导致revision/preview过期；不能手填`text_rf_wdata_label`之类ID后假称身份稳定。**先保存并重新read，再check/PNG/review**；若ID改变，按实际映射重建非持久回执和断言，不对旧ID继续操作，也不改用户原生版本机制。

## 符号、尺寸和素材

- **先发现/查询真实用户库**，确认当前可用ALU/MUX/寄存器/队列等，get/preview后按实际轮廓、朝向、viewBox与stub确定尺寸。用户指定库必须优先使用；名称相同用exact item ID。不预设个人路径、item数量或所有库引脚相同。
- 库中只有line/SVG carrier时，用insert返回的anchorElementId建立关系，保留完整instance/group与sourceIdMap；不直接把不支持的line当绑定目标。需要调整朝向/大小时对完整实例rotate/scale_selection，再按**变换后的**几何重算端口。
- 找不到/不适合现有素材时，ALU用原生闭合多边形凹口、MUX用多边形梯形＋明确数据/选择端、流水寄存器用狭长条并显示时钟/字段分段；这些是静态可编辑形状，不是用PNG替代。已有create_linear(polygon/closed)/create_svg_path及EA原生构造即可，不造第二个renderer。必要的透明anchor只服务绑定且与符号编组，不夸成已存在电子引脚。
  **不能把“查到库”当已使用符号**：若最终MUX仍是写着“MUX”的普通矩形且无可辨输入/选择端，或ALU/RF端口仅在正文中列名字，验收不通过。原生构造可用`{"op":"create_linear","kind":"line","x":100,"y":100,"points":[[0,0],[60,12],[60,88],[0,100]],"polygon":true,"closed":true,"style":{"strokeColor":"#1d4ed8","backgroundColor":"#eff6ff","fillStyle":"solid","roughness":0}}`创建MUX梯形轮廓（坐标仅示意）；端口/anchor/文字需按真实输入数另建并编组，不能直接把line轮廓当可绑定节点。
- RF/memory/queue/cache可以用矩形，但使用不同长宽比、端口、内部区划/entries或bank示意表达角色；阵列用适量重复格/网格＋数量标注，不为显示64k单元生成64k对象。stacked memory用真实层叠原生元素，合法包含/叠放有construction unit，不让诊断忽略所有重叠。
- 流水边界不是220×72文字卡片；以阶段间的窄高条贯穿所需数据/控制高度，字段标签简洁。计算块、memory、RF、controller尺寸由功能/端口密度和阅读尺度共同决定，不用统一最小220宽覆盖所有硬件。
- 配色按硬件角色和信号类别，不默认一阶段一种彩虹色。常用深蓝/黑实线数据、细红/橙虚线控制；灰度方案用线型/粗细/标签冗余。图例必须与实际元素颜色/虚实线一致，不能只写“红色控制”却仍画普通实线。

## 端口、总线和路由

- 对每条关键连接显式选source/destination的side/fixedPoint；多个RF输出或MUX输入必须分离。可在原生部件上加命名小端口/短stub；这些是实际图元，不把“Read Data1/2”写进说明就当已建端口。
- connect的`from/to`用真实部件/anchor ID，`start/end`的anchor、fixedPoint、mode按实际API传，维护start/endBinding及目标boundElements。命名端口标签与正确fixedPoint结合；只有命名metadata没有几何连接不算完成。
  按[分级验收](acceptance.md)区分真实网络关系与独立示意线：需随部件移动的关键连接使用原生绑定；自由总线/装饰指示箭头可不绑定，即使high也不强制100%绑定率。有绑定须一致、端口/语义须清楚；不能为提高绑定率把线接到错误对象。
- 每个MUX须列出**每一路数据输入源和选择源**，逐项对应实际独立边；3:1旁路MUX不能只有ID/EX数据＋一根ForwardA虚线。Forwarding Unit只产生选择码，不产生旁路数据；EX/MEM.ALUResult与MEM/WB.WBData要分别到FwdA/FwdB数据端。load的EX/MEM值是地址而非读回数据，禁止当load value旁路。
- ALUSrc的立即数、store write data、WB的rd地址与RegWrite、PC的branch target与PCSrc是不同信号。BEQ判决由Branch控制与比较结果形成；branch target加法器结果不是AND门的逻辑输入。图中只连接其中一部分时必须标未完成，不能用RF/ALU框内一句“所有端口”冒充完整连接。
- 选择码必须与每个MUX输入编号一致（如MemtoReg=1是否选load，ForwardA的00/01/10各选何源）；不能只验“有三条入边”。信号表里写明选择映射，图内标号、控制输出说明、实际连接三者对照；如果采用非惯例编码，明确说明而非混用常见含义。
- 主数据从左到右/上到下，反馈/写回走外围通道，控制带在上或下；对跨多个流水级的旁路留独立track。控制器/Hazard/Forwarding常应在局部控制区域而不串进主数据链导致拉长rank。
- 可将同一真实网络以主干＋分支表示；每个fanout落在真实信号，分叉点dot仅用于语义连通，独立交叉用arc/gap。不能随便把各独立arrow的中点绑定在一起宣称电气总线。没有net对象的接口就保留明确端点列表和可验证分支，不假称完整网表验证。
- 短局部线不需要长段论文文字；用端口名、`rs1`/`rd`/`32b`/`MemWrite`等短标签，完整说明放旁边注释。跨级bundle可以有简短总线名，不能每条边都加“[数据通路]”把间距撑大。
- 自动LR的最长标签会扩大所有rank间距，不能靠无限增大rankGap消除拥挤。固定列时手动分配bus/label净空与折点，标签避开头部/节点。需要复杂精确路由就用显式waypoints，不假设通用避障器理解阶段列/控制网。

### 微架构信号默认必须正交

**信号线只允许水平/竖直直连或正交折线/原生elbow**，数据、控制、旁路和反馈同样适用。仅用户明确要求斜线/曲线、或图型本身确有需要时才逐线例外并记录原因；不能因为两端不对齐就直接斜接。此规则针对信号线/arrow，不针对MUX/ALU多边形的斜边、时钟三角或端口符号轮廓。

- 两点线仅当`abs(dx)<=epsilon`或`abs(dy)<=epsilon`时可用；两方向都非零就必须增加正交拐点。**整体element.angle=0不代表线是水平的**，2点也不是天然水平/竖直；arrowhead、roughness、roundness都不会把斜直线变成正交线。
- 低层`connect`未传`elbowed`会按false处理；没有waypoints就直连端点，且不调用通用避障router。创建时显式选择**保留拐点的正交polyline**（`elbowed:false`＋轴向waypoints/points，硬拐点用`roundness:null`），或需要原生自动调整时用`elbowed:true`/primitive `routing:"orthogonal"`。**elbowed是编辑/路由模式，不是最终几何证据**：false也可有正确的四点正交折线；true也可能被宿主重路由到错误侧，必须读回逐段检查。
- 端点未对齐时，水平出/入端口常用H–V–H（中间track x固定），垂直出/入常用V–H–V；不同法向用L形或外围track。先留短法向stub，再避开部件/标签/其它信号。不要一律在中点加一个L拐点导致从错误侧穿进符号；同网分支与不相关交叉仍按真实语义处理。
- 小偏差如1.5/5画布单位也会形成斜线，不靠视觉忽略。原图端口可合法对齐且用户允许时，移动端口/重新计算所有相关边；否则保持端口不动，保留小正交折线。不要snap箭头端点坐标去“修直”却让它脱离原绑定端口。
- 修改已有线优先`patch_element {target,patch:{points:局部点列,elbowed:所选模式,roundness:所选转角}}`，保留同一箭头ID/绑定/头型/标签；点列首点[0,0]，waypoints则是scene坐标，不混用。先读原angle/局部坐标；不能为了正交只写angle=0，或把负local points截为正数。原生elbow硬角用`{type:2,value:0}`，手工正交polyline用`roundness:null`保持折点而不变样条。

例如端点scene `(100,200)→(240,260)`，左右端口的一个无障碍候选是`[(100,200),(170,200),(170,260),(240,260)]`：create/connect的waypoints仅传中间两个scene点；若已有arrow起点为(100,200)、angle0，patch.points为`[[0,0],[70,0],[70,60],[140,60]]`。这只是候选，不是通用避障答案，应用前核对实际障碍与端口方向。

**真实修复教训**：在使用2×2中心小锚点的CPU图上，直接把7条斜线设置`elbowed:true`，宿主重新推断出入方向，其中3条绕入寄存器，check报ARROW_CROSSES_NODE。最终保留原绑定和端点，使用显式四点H–V–H、elbowed=false、roundness=null，才同时满足正交与不穿节点。遇到这种情况先修受影响route，不删除端口、不强行全部elbow、不假称原输入waypoints已被原生模式原样保留。若选原生自动elbow，须准备正确的端口朝向并再次核对实际路径。

#### 正交审计是独立质量门

从**完整精确read**取实际点列，按线元素旋转变换为世界坐标；逐相邻点计算dx/dy，若两者绝对值均大于epsilon则报告`箭头ID/段索引/端点/dx/dy`。epsilon可取0.01画布单位处理浮点误差，不是以几像素容忍有意斜线；不要用四舍五入摘要来审计。还要排除零长段、重复折点/回头stub，确认首末段方向和端口法向一致。

现有通用drawing_check没有“微架构全网正交”的内建保证，也没有可凭空传入的orthogonal assertion type。Agent须用真实客户端脚本/现有执行环境实现以上逐段审计，或逐ID核对，不能把check=pass当全线正交。曲线/旋转例外明确列出，不能偷偷跳过。应用→保存→read后**重新审计所有信号线**，因为绑定/宿主可能调整点列；接着同revision check→PNG→实际看图→review，几何审计不替代穿线/标签和视觉判断。

每条问题只修自己的route及确实受影响的端口/邻边。不对整图强制转换曲线、拆线、白色遮罩，不修改用户业务语义；全部线已正交仍不意味着网络完整或图达到专业质量。

## 五级 CPU 的可执行规划范式

这是**无指定型号时的教学范式**，不是对任意CPU或用户RTL的事实断言。可采用单发射RV32I教学数据通路（ALU/load/store/BEQ；分支EX决策、静态不取、独立I/D存储），并在图中写清简化边界；用户指定MIPS/RV64/其它branch阶段则按实际改，不能混称“MIPS/RISC-V都完全一样”。未实现JAL/CSR/中断/乘除等不宣称完整RV32I实现。

- 五列IF、ID、EX、MEM、WB；四个边界IF/ID、ID/EX、EX/MEM、MEM/WB。边界显示数据及必要EX/MEM/WB控制bundle的跨拍保存，不能把Stage仅做成一个大框。
- IF：PC、Next-PC MUX、PC+4加法器、I-memory；两条next-PC值输入来自顺序值和branch target，select是独立控制端。PC+4和instruction进入IF/ID，PC或必要PC基值继续流向branch加法器。
- ID：RF至少两个读端口和rd/wdata/we写端；ImmGen、Decoder/Control、Load-use Hazard。指令字段分别到读地址/立即数/控制；读数据、立即数、rd和必要控制进入ID/EX。不要用一条“操作数+全部控制”边隐藏端口。
- EX：两路operand forwarding MUX、ALUSrc MUX、ALU、branch target加法器及比较/branch逻辑；Forwarding控制来自EX/MEM、MEM/WB的rd/RegWrite和ID/EX的rs1/rs2。操作数A/B、select、ALUCtrl及Zero/compare结果按端口分开。
- MEM：D-memory的addr/wdata/rdata/MemRead/MemWrite；ALU result/rd/control继续流入MEM/WB，store value应来自正确的寄存/旁路路径。可把存储和ALU结果并行直通画出，不让所有指令看起来都必须读memory。
- WB：result MUX在ALU result和load data间选择，输出writeback data/rd/RegWrite回RF；写回总线也参与forward。EX/MEM和MEM/WB旁路信号分别到对应operand MUX，而不只是写一段“Forwarding Unit”。
- Hazard输出PCWrite、IF/IDWrite、ID/EX bubble/flush等明确到消费部件；branch redirect/flush到正确PC选择和需清空的边界。简化设计采用哪些停顿/前递规则须写清，不把load尚未返回的数据错误地从EX/MEM当load value前递。

一次完整图可以用overview＋各区域局部PNG评审，不为了挤进1600宽删除这些对象。若具体细节会让图过密，可以按用户允许拆成“主数据通路”“控制/冒险/前递”两张互相对应的详细图，但不能把其中一张省掉，或偷偷降成阶段概要。

## 错误恢复：绝不靠降粒度通过

- 先读错误receipt和当前revision。compose有提交而check=fail时，图已经存在：**不再次compose整份diagram**，不换diagramId让重复创建保护失效。按错误native IDs修节点/端口/route/label；成功对象和全部业务关系保持。
- 若确需整体替换，仅对本轮明确创建的IDs做可追踪切换并保留原图/回执；不clear、不删除用户原内容，不在新文件重复画一个更简单图然后宣布原任务完成。
- 不把ALU/RF/MUX等独立部件收进“IF阶段：…列表”，不删除反馈/控制/旁路线，不缩短业务内容，不随便把冲突节点标isContainer以躲检查。需要改变抽象层级/省略内容必须征得用户同意。
- `expected`要非空并覆盖部件与关键关系，既有node_exists/edge_exists/label_equals/edge_label可用；它们只能证明确切已建对象/边，不自动验证电气时序。额外端口/阶段检查由执行代码或Agent按读回精确元素核对，不能传虚构assertion type。
- 第一次发现问题就记录review visual_issues及相关IDs；每轮计入同一预算，不把多次PNG后最终第一次review伪称只花一轮。达到上限或无进展报告needs_attention，不用新token/新文件刷过关。
- 不允许把程序异常用`except: pass`当作成功，也不对未知状态无条件revert再重新apply整图。先读状态/receipt，只撤销明确属于本轮且确需回退的事务；已通过部分保持，修复用最新revision按ID局部提交。批量客户端参数取当前安装包路径和`EXCALIDRAW_AGENT_STATE_DIR`，不猜Python包名或导入工作区旧原型；耗时源代码搜索不是绘图前提。

## 必须逐项验收

1. **结构粒度**：计划中所有硬件部件仍是独立图元/组件；关键端口有实际信号连接，不仅标签。阶段概要不能替代微架构。
2. **硬件逻辑**：沿“取指→读操作数→执行→访存/直通→写回”追踪一条ALU、一条load、一条store和一条branch；核对Forwarding/load-use/flush的输入与消费端，哪些示例不在任务范围则按实际检查。检查数据与select/enable未混接。
3. **时序/空间**：阶段列和边界清楚，同级功能并列而不是按普通rank排成十几列；数据/控制/反馈track有组织、没有无意穿过部件；具体容量/带宽/位宽有来源或教学假设。
4. **检查证据**：check只验证了已提交的对象；expected为空时不得称“语义100%通过”。绑定引用存在不是端口正确，更不是电气/时序网表通过；frame/group存在不是硬件层次正确。
5. **可读性**：按`preview.actualScale × text.fontSize`计算输出中的有效字高。若overview正文约6px、图细长到只剩一条线，必须调整布局/尺度或提供并实际查看每个必要区域的局部图，不能把complete=true当可读。约12–14px可作为overview正文设计起点而非通用硬上限；复杂图细节以局部图证明，最终用途决定尺度。
   局部预览不能把某个区域内对象的所有boundElements（尤其跨全图的箭头）无条件加入选区；否则被长线撑成另一张缩略全图。ids仅含目标区域及其绑定文字、**局部需要**的完整边；跨区网络用单独网络预览或真实区域裁剪。读取返回bounds/actualScale确认真的放大；若使用已有PNG裁剪，记录其原PNG/revision/区域且不冒充新注册preview。不改场景裁切用户内容，不将跨区线删掉来获得局部图。
6. **真实视觉**：看整个PNG和必要局部（所有流水级、符号端口、旁路交叉、长标签）。符号未显示/端口错位/文字糊或遗漏必须修，不能visual_issues=[]。参考图的逻辑角色、空间层级和线网组织应可辨认，不强求像素临摹。
   中高等级提交content/readability/occlusion的实际visual_checks，高级再提交connections/hierarchy_style。背景容器上的清晰文字是合法包含；线穿字、字互压、后画对象盖字优先修。几何候选若被当前PNG证实是空白相交或合法叠放，逐issueId记录dispositions，不全局关闭检查；未支持几何审查后披露限制，不要求凭空证明每根示意线都绑定。
7. **交付诚实**：保存原生源、全图＋必要局部PNG、结构/语义清单及剩余限制。review只是Agent对真实PNG作出的评审记录，不是自动专业质量证明；未满足本任务硬件验收就不得标completed。
   绘图任务默认要求可追踪的逻辑/端口/时序假设，不要求凭空提供RTL仿真；没有RTL不是单独的视觉错误，也不能声称已仿真。发现具体缺线、选择码不一致、时序矛盾才列硬件问题；“未经独立RTL验证”作为明确范围限制，避免用泛泛免责声明替代逐条检查。达到本轮实际自动修复上限时，即使ledger因漏记前轮仍返回continue，也停止并报告needs_attention；不得把账本轮数当已经执行次数。

## 实测范围与未满足项

本参考基于真实五级CPU运行修订，不把通用三节点图当能力证明。首轮Gemini/high实际建立独立部件和流水边界，但依然用了矩形MUX/ALU、漏掉部分旁路值连接，局部预览被长边撑大；其completed声明被独立评审拒绝。后续按原图ID局部修复，保留原始113个元素及48条原有箭头，增加7个原生polygon轮廓、命名端点、旁路/控制网络和有效1.6x局部PNG；最终351元素、73条记录信号、227条既有断言类型通过几何/绑定检查。

这轮**不宣传为全自动专业微架构验收完成**：整体反馈线仍拥挤，细节依赖局部图，选择码/时序仍需按具体实现审查；实际ledger最后是continue，自动修复已停止。证据证明已有API可以保留硬件对象和端口并显式报告问题，不证明仅更新Skill即可让任意模型稳定达到参考论文图水准。后续任务同样按上面的质量门执行，不复用本次completed/continue或轮数作为新图结论。

## 能力定位

这是Skill工作流与已有原生/库/路由API的组合，不宣称新增硬件自动布局器、通用电气端口DSL或RTL验证器。优先使用现有模块；如真实运行暴露某工具不能保持所需结构，应报告具体缺口并切换到现有更低层API，不拿文字卡片掩盖缺口。high可以辅助硬件规划，但不是正确表达层和验收的替代品。
