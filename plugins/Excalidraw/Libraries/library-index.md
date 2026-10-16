# 素材库索引摘要 (Library Index)

本索引文件供绘图 Agent 进行语义检索与选库选型参考，并供用户维护与审阅。

---

## 用户偏好与业务用途说明

- **核心领域**：数字逻辑电路、计算机体系结构、CPU 微架构设计、硬件数据通路与片上互连网络。
- **业务用途**：用于绘制规范、专业、严谨的芯片体系结构框图、五级/多级 CPU 流水线、互连拓扑、存储层次与逻辑门级原理图。
- **选型倾向**：优先选用原生线条清晰、标准符合 IEEE/ANSI 规范及经典微架构教材（如 CSAPP、Patterson & Hennessy）标准的图元符号。

---

## 库：digital-circuit-components(svg).excalidrawlib

- **相对路径**：`digital-circuit-components(svg).excalidrawlib`
- **整体用途**：涵盖数字电路基础逻辑门、CMOS 晶体管、时序寄存器、算术运算单元、队列与缓存、总线互连及片上网络核心符号。
- **图元风格**：原生 SVG Path 矢量线条风格（单色黑白线框、无杂乱背景填充、专业清晰、紧凑规整）。
- **适用场景**：
  - CPU / GPU / NPU 处理器微架构框图（如流水线阶段划分、ALU、寄存器堆、旁路多路器 MUX、控制逻辑）。
  - 存储体系结构设计图（L1/L2 组相联 Cache、SRAM 多 Bank 阵列、FIFO/栈队列、TLB 快表）。
  - 片上互连与总线拓扑（NoC Router、Crossbar 交叉矩阵、Decoupled 握手流、总线分线器 Bus Tap）。
  - 基础 CMOS 电路与门级逻辑原理图（AND, OR, NOT, NAND, NOR, XOR, XNOR, PMOS, NMOS, TG, 三态门）。
- **不适用场景**：
  - 非硬件类的业务架构图、云原生微服务调用链路、常规软件 UML 图、日常办公手绘风格流程图。
- **Item 总数**：41 个（已全部完成 100% 结构化描述审阅与增补）。
- **资源与扩展特征**：纯 SVG 矢量几何路径（包含 `svgPathShape`、`svgViewBox`），无外部依赖资源，不包含可执行外部脚本或潜在不安全代码。
- **连接与编辑限制**：图元为纯几何线框与端口锚点，未绑定电气引脚或仿真网表语义；在 Excalidraw 中可直接缩放或连线，如需与信号线精准吸附建议对准端口引脚端点。

### 代表 Item 与 Exact ID

| 类别 | 代表 Item | Exact ID | 视觉形态长相与几何轮廓 | 适用场景与关键差异 |
| :--- | :--- | :--- | :--- | :--- |
| **基础逻辑门** | **AND (库中名 NAND)** | `pT3wo752el-HTBSTVc-UG` | 标准 D 字形平直背线与凸半圆弧，输出尖端**无反相圆圈**，直接引出单输出引线；左侧双输入引线。 | 逻辑与运算、时钟门控、条件译码。**关键区别：库中原名保留为 NAND 但实际为 AND 与门，与带反相圈的真实 NAND 严格区分。** |
| **基础逻辑门** | **NAND** | `HGGt5kKb_OSfEu0SRZ6h_` | 标准 D 字形平直背线与凸半圆弧，输出尖端连接**反相小圆圈**；左侧双输入引线，右侧引出输出线。 | 逻辑与非门、通用门网络。与同名无圈项 (ID: `pT3wo752el-HTBSTVc-UG`) 相比，本图元输出端带有反相小圆圈。 |
| **基础逻辑门** | **OR** | `vh-zg7bNlZwUkl6zOUEFW` | 经典单凹弧背线、双凸弧相交尖端，无反相圈；左侧双输入，右侧单输出。 | 组合逻辑或门、请求合并、中断汇集。区别于 NOR 无反相圈，区别于 XOR 仅有单条输入弧。 |
| **基础逻辑门** | **NOR** | `wxZ82BQNVYOyM0VcSnI_O` | 凹弧背线、尖凸相交尖端带反相小圆圈；左侧双输入，右端带反相输出。 | 逻辑或非门、SR 锁存器、控制信号译码。 |
| **基础逻辑门** | **XOR** | `lVmFnTYPRv0bxuvR3-Klu` | 双重凹弧输入背线（独立外弧 + 主体凹弧），尖凸相交尖端无反相圈；左侧双输入。 | 半加器/全加器求和、奇偶校验、比较器。区别于 XNOR 无反相小圆圈。 |
| **基础逻辑门** | **XNOR** | `oUKEJNPRVsqiVuY-d5MDSQ` | 双重凹弧输入背线，尖凸相交尖端带有反相小圆圈；左侧双输入。 | 同或门、偶校验、位匹配比较器。 |
| **基础逻辑门** | **NOT** | `Mgy2XskpdeJJLWAEBLBKN` | 水平向右等腰三角形，右尖端带反相小圆圈；左输入右输出。 | 信号反相、低电平有效控制、时钟反相。区别于 Buffer 尖端带圈。 |
| **开关与晶体管** | **PMOS** | `VWBFtYRIIPFGl0-i2CwwD` | 垂直三端晶体管，左侧栅极引线上带反相小圆圈，接双平行极板，上下折线引出源漏极。 | CMOS 上拉网络 (PUN)、低电平导通开关。区别于 NMOS 栅极带反相圈。 |
| **开关与晶体管** | **NMOS** | `n5KyvrjjRMOAIeKfjwvnn` | 垂直三端晶体管，左侧栅极直连无圆圈，接双平行极板，上下折线引出漏源极。 | CMOS 下拉网络 (PDN)、接地放电开关、高电平导通。 |
| **运算与数据通路** | **ALU** | `adq8qLb9iMgcxqRsr78FZ` | 对称下窄上宽梯形，顶部中间带标志性倒三角 V 型凹槽（双操作数输入），底部单输出线。 | CPU 微架构执行级 (EX Stage)、算术逻辑数据通路。 |
| **运算与数据通路** | **MUX (2:1)** | `rCTopVHKcQSVdQkLpeCFo` | 立式左宽右窄梯形，左侧 2 路输入引脚，右侧 1 路输出引脚，底面 1 根选择控制引线。 | 条件二选一信号选通、操作数旁路。区别于四选一 MUX (4:1) 为紧凑 2:1 规格。 |
| **运算与数据通路** | **MUX (4:1)** | `cuxJcXzmEXhpyDqmaEEjSg` | 宽端输入 4 路数据通道 (I0..I3)，底部输入 2 位选择控制码 (S0, S1)，窄端输出选中的数据流。 | 多路操作数选择、执行单元多源旁路。 |
| **运算与数据通路** | **DEMUX (1:2)** | `_eBZGaMVW-sdqec3y6eVeg` | 梯形窄端输入单路数据，宽端引出 2 路分支数据，底端接收选择控制端。 | 单端口写总线分流、多寄存器组译码写入。 |
| **运算与数据通路** | **Adder (+)** | `Khw7U2q_Ps06zZyBVXHNGw` | 圆形符号内部标有 '+'，左侧与上方为操作数输入，右侧为求和结果。 | PC+4 递增、分支目标计算、AGU 地址生成。 |
| **运算与数据通路** | **Multiplier (×)** | `oJnyu-5n0ESgS2TWtcCVtA` | 圆形符号内部标有 '×'，输入在左/上方，乘积从右侧输出。 | 定点/浮点乘法流水线、DSP 计算与神经网络算子单元。 |
| **运算与数据通路** | **Comparator (==)** | `TmKytPU1tDnhWGJtL0ZJ9A` | 矩形框内标有双等号 '=='，左侧双比较输入 A 与 B，右侧输出单比特匹配标志。 | 分支跳转判定、TLB/Cache Tag 命中检测。 |
| **运算与数据通路** | **Shifter (>>)** | `wxTVtrwzNKqrb-E-xtbtAA` | 梯形轮廓内标有双尖括号 '>>'，宽端输入数据与位移量，窄端输出结果。 | 逻辑/算术移位器、桶形移位器。 |
| **时序与流水线** | **DFF** | `jtQi1JIy-oFo1-GHkPid1Q` | 边沿触发器符号，含 D 数据端、CLK 边沿小三角、主输出 Q 与带反相圈的 Q#。 | 时序电路基础单元、状态机状态寄存。 |
| **时序与流水线** | **Register** | `C36_q2xgNS4frrt51CE7Og` | 矩形外框内含时钟触发小三角，两端带数据输入与输出引脚。 | 通用 N 位数据寄存器、PC、临时暂存器。 |
| **时序与流水线** | **Reg (EN/RST)** | `4pzyiKX6fLXps4PZl6Ss_w` | 寄存器框带底部使能端 EN (Stall 停顿) 与顶部复位端 RST (Flush 冲刷)。 | 流水线停顿控制与异常冲刷寄存器。 |
| **时序与流水线** | **Pipeline Stage** | `tMy7DS9m6xm4qyn18Z-E7A` | 纵向细长柱体，底端带有边沿触发时钟三角标，两端引出数据线贯穿引脚。 | 在 CPU 微架构图中清晰隔离 IF, ID, EX, MEM, WB 等流水线阶段。 |
| **时序与流水线** | **Skid Buffer** | `XDlAyZsunHEgTvLa9OOFXw` | 含时钟端、前向 Data/Valid 通路与反向 Ready 反压通路，中间带双缓冲隔离切片。 | AXI4 / TileLink 解耦协议切断反压组合逻辑关键路径。 |
| **时序与流水线** | **Decoupled Handshake**| `F0zPkC4RF4v5gbJXNfvXnw` | 一对平行的相反方向箭头：正向前进 Valid 流与反向回退 Ready 反压流。 | 标注总线采用标准 Ready-Valid 解耦握手协议。 |
| **存储体系结构** | **Register File (2R1W)**| `9hKO0ptcqFyaTjixj9iNkw`| 矩形框左侧引出 RA1/RA2 读地址与 WD 写数据，右侧引出 RD1/RD2，底接时钟。 | RISC-V / ARM 标量核心通用寄存器堆 (GPR/PRF)。 |
| **存储体系结构** | **FIFO Queue** | `rlVe960STfixJBwB6DSeyQ` | 水平分槽矩形槽位，左端带入队 Push 箭头，右端带出队 Pop 箭头。 | 取指队列 (FTQ)、指令缓冲 (IBuffer)、ROB 重排序缓冲。 |
| **存储体系结构** | **Vertical Queue** | `efaCYuFhEwiBHVP1KPOM_w` | 纵向分槽存储栈，顶端入栈，底端出栈。 | 返回地址栈 (RAS)、数据深度调用栈。 |
| **存储体系结构** | **Multi-Bank SRAM** | `ctvuKRekX4jJUApFubgWbQ` | 4 个物理并列的独立访问 Bank 块，上下两端分别引出独立的读写总线接口。 | 向量寄存器堆 (VRF)、多通道共享内存。 |
| **存储体系结构** | **Cache Block** | `OwItiy5nNmT29T73gUjYGw` | 明确划分为左侧 Tag 阵列与右侧 Data 阵列，左端输入 Index/Tag，右端输出匹配结果与 Cache Line。 | I-Cache、D-Cache 及 L2 缓存体系结构。 |
| **存储体系结构** | **TLB Entry** | `0Km2Fj4mQml14lTg9Dfaaw` | 双槽位构成，分别对应虚拟页号 VPN 与物理页号 PPN，外带地址转换匹配标志。 | MMU、I-TLB、D-TLB 虚拟内存地址映射与加速。 |
| **互连与片上网络** | **2×2 CROSSBAR** | `Ef65NX4KTBYaxtVaAr-7Y` | 正方形外框，内部两条水平线通过中心对角交叉连通形成 'X' 形双通道互连。 | 紧凑型 2×2 空间交叉互连单元。区别于网格化多端口 Crossbar Switch。 |
| **互连与片上网络** | **Crossbar Switch** | `hT_hu70siErI9JrJaswEZA` | 网格化矩阵结构，行与列交点带有可配置连接圆点，实现多进多出全互连。 | 多核片上互连、向量 Lane 与 PE 间数据交换。 |
| **互连与片上网络** | **NoC Router** | `zjp92_afhxtkdIlI_qK5zw` | 中心交换矩阵，四周向外引出 Local, North, South, East, West 5 个双向链路。 | 2D Mesh 多核处理器与 AI 芯片片上网络互连架构。 |
| **互连与片上网络** | **Arbiter (RR Tree)** | `3QXGfNhKVb82sb1KmVu7Ng` | 汇聚梯形结构，下部宽端接入 Request[3:0]，顶部输出 Grant，内含优先循环指示。 | 多主设备轮询仲裁、交叉开关端口冲突解决。 |
| **总线与辅助** | **Bus Tap (Fork/Join)** | `jgdOAfaKtZBMjglYAAlB0A` | 粗主干数据线通过斜向支线分流或汇聚，支线上标有斜杠位宽符号 '/'。 | 规范化绘制总线分支拆分与位宽合并。 |
| **总线与辅助** | **Clock Source** | `kd41YTsXKka_3CIXz_l_YQ` | 方框内标有数字方波脉冲波形 '_\|^\|_'，右侧输出时钟。 | 微架构基准时钟信号源。 |
| **总线与辅助** | **VCC / VDD** | `xOLi-iAgq7aKVgPc2b1PjQ` | 垂直引线上接实心尖角箭头，指示高电平电源轨。 | 电源供电端口符号。 |
| **总线与辅助** | **GND** | `fL-fWsSIgyoUZqfi9e5WHw` | 垂直引线接三条递减的平行横向参考面，指示系统零电位参考地。 | 接地端参考地符号。 |
| **电路单元** | **Processing Element** | `bIlgfsbOWyL_QRH8-J_lKA` | 正方形单元，内部串联乘法器 (×) 与加法器 (+)，带水平激活值通道与垂直权重通道。 | Google TPU、NVIDIA Tensor Core 矩阵乘累加网格单元。 |
| **电路单元** | **Buffer** | `UMMISDc_INBTNCvZPpnQlg` | 无反相单向驱动三角形，左输入右输出。 | 信号驱动增强、时钟树缓冲分发、延迟匹配。 |
| **电路单元** | **Tri-State Buffer** | `VKcqi_nbVxWF_HiHy1CFHQ` | 驱动三角形带顶部高电平使能控制端 (EN)。 | 总线多主控隔离与共享、高阻态控制。 |
| **电路单元** | **Transmission Gate** | `uBr9CkWbeeDp8FtsMOQh6Q` | NMOS 与 PMOS 并联，两端带互补栅极控制信号 C 与 C#。 | CMOS 双向低阻模拟开关、传输门。 |

---

## 库：presentation-bundle.excalidrawlib

- **相对路径**：`presentation-bundle.excalidrawlib`
- **整体用途**：专用于多页演示幻灯片（Presentation Slides）的纯原生 Frame 画布模板库，供 `drawing_present` 原生演示工具调用。
- **图元风格**：基于 Excalidraw 原生 Frame 画框，预设了标题栏、主干结构框、内容要点占位符和配色风格。
- **适用场景**：
  - 使用 `drawing_present` 创建多页架构评审、技术汇报、产品发布或课程讲义演示画板。
  - 包含 7 种主流风格套系（Simplicity、Pacman、Tetris、Graph、Creativity、Circles、Excalidraw 原生手绘风）及其配对的 Intro 封面页与 Slides 正文页。
  - 包含标准画框比例辅助模板：16:9, 4:3, 3:2, 1:1, 21:9 等。
- **不适用场景**：
  - 严谨的硬件微架构、逻辑门原理图或细粒度流程图（此类请使用 `digital-circuit-components(svg).excalidrawlib`）。
- **Item 总数**：20 个（全部 100% 结构化描述审阅与增补）。

### 代表 Item 与 Exact ID

| 套系 / 类别 | 代表 Item | Exact ID | 视觉形态长相与几何轮廓 | 适用场景与配对关系 |
| :--- | :--- | :--- | :--- | :--- |
| **Simplicity 极简风** | **Simplicity (intro)** | `UEan54xVVGzUsV1OnrGf4` | 纯白底色，内嵌一层带对角透视引导线的虚线矩形画框，居中双行大标题与副标题/作者。 | 正式演讲、技术方案发布封面。与 `Simplicity (slides)` 配对。 |
| **Simplicity 极简风** | **Simplicity (slides)** | `7cNv6q_ipH1AdnUjJj56u` | 纯白底色，包裹双层极细浅灰手绘虚线边框，左上角标有 Slide title，带两个空心圆列表点。 | 高管汇报、咨询复盘、学术讲座正文页。与 `Simplicity (intro)` 配对。 |
| **Pacman 街机风** | **Pacman (intro)** | `WNzbsU3oHCQQOfWFPclIj` | 纯黑背景，环绕青色街机迷宫走廊与黄色吃豆圆点，点缀彩色像素小幽灵与吃豆人，中心为亮青色卡片加粗标题。 | 技术沙龙、黑客松、游戏研发、开源项目演讲封面。与 `Pacman (slides)` 配对。 |
| **Pacman 街机风** | **Pacman (slides)** | `bHRAac4ZwcsSAAD4_0fnz` | 纯黑边框深底，青色标题栏与黄色点状序号，底部横贯黄色吃豆轨道与吃豆人图标，右下标有页码。 | 极客技术分享、趣味开发讲座正文页。与 `Pacman (intro)` 配对。 |
| **Tetris 积木风** | **Tetris (intro)** | `fNkw95y4OvDFPTIf5b0Pj` | 浅灰方格网格底纹，底部铺满整齐的马卡龙色系像素方块墙（青橙紫粉黄绿），中心醒目蓝色主标题。 | 系统架构搭建、技术底座重构、工程化演讲封面。与 `Tetris (slides)` 配对。 |
| **Tetris 积木风** | **Tetris (slides)** | `L2TQOZXaU3Zzryu9I_OIH` | 浅灰细网格底纹，左上角深蓝序号标题与蓝色方块点，下缘与两侧堆叠柔和像素方块。 | 微服务架构拆解、模块化设计、敏捷迭代正文页。与 `Tetris (intro)` 配对。 |
| **Graph 折线风** | **Graph (intro)** | `7YIAj8e77fLE6mxKSnk0-` | 下半部为多彩折线图山峦景观（青蓝深紫折线、黄色多边形、排线阴影），左上浅粉阴影圆，右下作者与日期。 | 商业计划书 (BP)、数据增长、宏观经济分析封面。与 `Graph (slides)` 配对。 |
| **Graph 折线风** | **Graph (slides)** | `U6DnMjQKFIK05ZV7PUcUP` | 温暖淡奶油底色，左上角珊瑚红标题与右向双尖角符号 '>>'，下半部衬有起伏平缓的浅粉与浅黄波浪山峦。 | 业务增长分析、数据科学分享、指标回顾正文页。与 `Graph (intro)` 配对。 |
| **Creativity 艺术风** | **Creativity (intro)**| `_d7jpKB8SC_O2zk0jBODs`| 底板铺陈多层半透明莫兰迪水彩圆形与有机色块叠印交织，正中深紫色艺术字体主标题。 | 设计分享、创意提案、品牌故事、用户研究封面。与 `Creativity (slides)` 配对。 |
| **Creativity 艺术风** | **Creativity (slides)**| `5IPbx8M4pFB5x29KbQ_pq`| 米白底色，背景带极细相交大圆弧几何曲线，左上角圆角矩形紫色胶囊标题栏与菱形列表符。 | 产品体验评审、UI/UX 方案、设计系统正文页。与 `Creativity (intro)` 配对。 |
| **Circles 水彩风** | **Circles (intro)** | `WYkBaBoWaC7x80m75wRPJ` | 柔和多彩水彩圆斑叠放，中央浮置圆角矩形浅米色保护卡片，居中排列主标题与作者名。 | 培训课件、团队文化宣讲、温馨亲和型演讲封面。与 `Circles (slides)` 配对。 |
| **Circles 水彩风** | **Circles (slides)** | `e5lLzFCnIhi4UMBn1lkkO` | 背景晕染半透明马卡龙彩色圆形气泡斑块，左上淡紫圆角标签标有 Slide title，配备菱形列表。 | 教育培训、产品故事、团队敏捷回顾正文页。与 `Circles (intro)` 配对。 |
| **Excalidraw 手绘风** | **Excalidraw (intro)** | `jz7XG5gfC3LYApo-o6bCm` | 充满白板脑暴手绘涂鸦：弯曲虚线箭头、黄色荧光笔涂抹刷、紫色排线小柱状图、手绘圆圈重点批注。 | 创意脑暴开场、敏捷工作坊、架构草案探讨封面。与 `Excalidraw (slide)` 配对。 |
| **Excalidraw 手绘风** | **Excalidraw (slide)** | `PBNZbUig71hoHRfUAwZm_` | 纯净手绘白底，左上角手绘紫色圆角便签标题块，下方为手绘菱形项目符号列表内容。 | 技术方案脑暴、架构草图、黑板教学演示正文页。与 `Excalidraw (intro)` 配对。 |
| **排版辅助** | **Bullets** | `lRlViQw8fIKKA6vrcehgZ` | 纵向单列 25 个独立手绘排版指示图标集：圆圈、三角、方框、箭头、勾号、叉号等。 | 为任何演示页、流程图卡片或看板列表增补高亮图标与列表符号。 |
| **画框比例** | **16:9** | `cnvqDbvFP09TxaCBpPNEP` | 细黑线条矩形框，横纵比例严格为 16:9 现代主流宽屏比例，居中标注 '16:9'。 | 现代显示器、高清投影、视频封面通用排版基准框。 |
| **画框比例** | **4:3** | `oXGMSKE4T6CD1s0TXC21I` | 细黑线条矩形框，横纵比例严格为 4:3 传统屏幕比例，居中标注 '4:3'。 | 传统投影仪演示、A4/Letter 文档版面适配基准框。 |
| **画框比例** | **3:2** | `uTxnzRVh1OXKBP_cMpPgG` | 细黑线条矩形框，横纵比例严格为 3:2 经典比例，居中标注 '3:2'。 | 平板电脑 (iPad/Surface) 与经典画幅排版参考框。 |
| **画框比例** | **1:1** | `2InZI5FWOHMN94iMJ8AgX` | 细黑线条正方形框，横纵比例严格为 1:1 正方形比例，居中标注 '1:1'。 | 正方形插图、社交媒体分享图、头像卡片参考框。 |
| **画框比例** | **21:9** | `WlAUqIaToANOTangKgZhx` | 细黑线条矩形框，横纵比例严格为 21:9 超宽屏比例，居中标注 '21:9'。 | 带鱼屏全景长图、影视比例演示或超宽架构全景图参考框。 |


---

## 审阅与维护记录

- **维护日期**：2026-10-16
- **维护模式**：本地宿主工具维护（Local Host Mode）
- **源文件原字节备份**：`digital-circuit-components(svg).excalidrawlib.e6e82dc22909.metadata-backup`
- **原文件 SHA-256**：`e6e82dc2290922053d5475c2f6279b11864fc92d68deb23dafb9b6368387da9a`
- **维护后 SHA-256**：`d71dd717278f6ea5bc067570b31d4e8227ffe0a1549a55e1767a3919ef627d57`
- **已审查覆盖范围**：全库共 41 个 item 已全部完成 100% 视觉比对、要素审查与描述补全：
  - 本次全新增补描述：11 个 item（ID: `Ef65NX4KTBYaxtVaAr-7Y`, `adq8qLb9iMgcxqRsr78FZ`, `rCTopVHKcQSVdQkLpeCFo`, `wxZ82BQNVYOyM0VcSnI_O`, `HGGt5kKb_OSfEu0SRZ6h_`, `lVmFnTYPRv0bxuvR3-Klu`, `vh-zg7bNlZwUkl6zOUEFW`, `pT3wo752el-HTBSTVc-UG`, `Mgy2XskpdeJJLWAEBLBKN`, `VWBFtYRIIPFGl0-i2CwwD`, `n5KyvrjjRMOAIeKfjwvnn`）
  - 保留并核验已有人工描述：30 个 item（ID: `oUKEJNPRVsqiVuY-d5MDSQ` 至 `jgdOAfaKtZBMjglYAAlB0A`）
  - **presentation-bundle.excalidrawlib**：全库共 20 个 item 已全部完成 100% 结构化描述增补（包含 7 套配对演示页与 6 个画框/排版辅助工具，SHA-256: `2ee1dfac17bb60f80943812236deb7934181dc317dc2fb580b2358e6c3abf2ba`）。
- **未确认项 / 遗留注意事项**：
  - Item 8（ID: `pT3wo752el-HTBSTVc-UG`）在原始库中的 `name` 标记为 `NAND`，但图元几何形状无反相输出圈，实为标准 `AND` 门。按照维护规范保持原 `name` 不变，但在 `description` 和摘要中均做了明确警示与区分。
