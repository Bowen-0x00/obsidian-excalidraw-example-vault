# 多场景演示与手动GIF录制

以下prompt用于在你自己的vault重新生成并录制过程，不是固定坐标脚本，也不要求OMP。可用Claude Code/Codex/OMP等支持真实MCP与图像查看的Agent。本轮实际调用OMP加载Skill生成了这些场景、查看PNG并局部修复；你手动录制时用相同的短prompt即可。

包内真实画廊见`docs/gallery.md`或[在线画廊](https://github.com/Bowen-0x00/obsidian-excalidraw-agent-skill/blob/main/docs/gallery.md)。六组`examples/dsl/`展示流程、分区、硬件反馈、表格/ECharts、Tomasulo与资源；新增三组复杂五级RISC-V、分布式推理、4×4矩阵阵列来自`examples/builders/advanced_showcase.py`的Agent编写Python／原生API，**不是DSL自动布局**。源码、原生画布、全图／可读局部和验证边界均单独标明；不是全ISA、RTL仿真或生产性能证明。DSL按[scene-dsl](scene-dsl.md)，自然语言／原生路径继续用本文。

## 一次只跑一个场景

共通要求：使用obsidian-excalidraw Skill，先status确认连接，在`Agent-Diagrams/Showcase`新建独立画布；真实测量/布局→apply→全图read/check→PNG→实际看图→局部修复→review，最多5轮，保留原生元素与用户素材，不修改源库。

| 场景 | 风格/能力 | 已运行证据 |
|---|---|---|
| 服务器开发、本地绘图架构 | Visio三分区、正交前向/反馈关系 | 过扁长原稿改为三列内竖排；29个ID和7条关系保留，1200×669最终PNG |
| 访问申请审批 | Rough.js handdrawn、长中文菱形、分支标签 | 真实roughness/hachure、18个原生元素，全文和通过/未通过关系保留 |
| 订单领域模型 | Visio UML类图三分区、composition | Customer/Order/LineItem属性/方法、Order端实心diamond，23个元素 |
| 发布职责分工 | professional、真实泳道Engine | 开发/CI/运维，失败→修复→测试完整回路，27个元素 |
| 微架构数据通路 | blueprint、用户SVG库、anchor绑定 | MUX/ALU/CROSSBAR原生导入；按真实stub修输入端点，21个ID不变 |
| 数据反馈循环 | Rough.js形状/箭头、Callout | 采集→清洗→分析→报告→采集；完整中文说明，16个元素 |
| 白板手画笔迹 | native freedraw，而非Rough.js profile | 3个freedraw含points/pressures，原生text/arrow与透明anchor，12个元素 |
| 可编辑图形与视觉反馈演示页 | presentation、frame、WaveDrom/code/callout | 1200×760frame、21个子元素；波形JSON/代码源保留，最终PNG实测 |

数字电路库是用户依赖：若你没有同名库，指定自己的实际库并query/get/preview核对；不能声称示例一定预装。WaveDrom/Callout/code需要当前宿主Engine可用。

## 可复制的短prompt

### 1. Visio分区架构

> 使用obsidian-excalidraw Skill，画“服务器开发，本地绘图”：服务器区有项目源码和Agent+Skill；安全连接区有MCP客户端和SSH反向隧道；本地工作站有Bridge、Obsidian Excalidraw和可编辑画布。按这条链连接，并从画布返回Agent一条“PNG视觉反馈”外侧回边。Visio严谨分区，三列区内竖排、紧凑可读。保留原生元素，导出PNG并实际检查。

### 2. Rough.js审批流程

> 画访问申请：提交→判断“身份、权限范围和资源条件是否全部符合？”；通过→发放凭据，未通过→拒绝并说明原因，两路到结束。使用handdrawn/Rough.js风格，保留完整中文，标签贴近正确出口，检查PNG并局部修正。

### 3. UML分割

> Visio风格画订单UML：Customer有id/name、placeOrder()；Order有id/status、total()；LineItem有sku/quantity、subtotal()。每类严格三分区。Customer关联多个Order；Order组合多个LineItem，实心diamond在Order端。用真实原生图元，查看PNG。

### 4. 泳道

> 三条竖向泳道“开发/CI/运维”，发布流程：提交变更→运行测试→判断测试是否通过；通过→部署上线→观察指标，未通过→修复反馈→运行测试。professional风格，保留失败回路、泳道表头和正文分离，真实PNG检查。

### 5. SVG库微架构

> 从我指定的当前数字电路库查询并原生插入MUX、ALU、CROSSBAR。A/B→MUX→ALU→CROSSBAR→结果，blueprint风格，保留库源外观。输入箭头按真实svgViewBox/carrier/stub对齐，透明anchor维护绑定，不把0.28/0.72等示例当真实端口。检查PNG，不改源库。

### 6. 手绘数据循环

> handdrawn风格画“采集→清洗→分析→报告→采集”，外侧回流清楚。加一个原生Callout说明反馈和数据质量控制，文字完整可读。不要用图片模拟手绘，导出PNG检查。

### 7. Native手画白板

> 用原生freedraw制作“想法/原型/反馈”三个不规则笔迹区域，用原生text和可绑定arrow表达想法→原型→反馈→想法。不是roughness矩形，不是图片，保留点列和压力。真实check、PNG、视觉迭代。

### 8. 扩展演示页

> presentation风格制作1200×760原生frame页“可编辑图形+真实视觉反馈”：四区分别是需求→绘图→PNG→修正小流程、clk与A/B/C data的真实WaveDrom、Python源码高亮、Callout“可继续编辑”。保存真实源和frame成员，首次PNG就等待资源，实际看图后review。

### 9. 已有组的旋转与缩放

> 打开我指定的已有画布，读取元素groupIds，找到“组件A、组件B和它们的内部箭头”所在组。用原生选区变换绕共同中心顺时针旋转90°，再保持中心放大1.5倍；节点文字与箭头标签同步缩放，保留ID和双向绑定。外部节点不动，跨组连接正确跟随。读取最终状态，导出PNG并实际检查；不要逐项angle/width/height拼装变换，不清空重建。

该补充场景由当前Agent直接调用真实Bridge完成，不是前八张的独立OMP生成会话。真实PNG与可编辑画布作为本地验证产物保留；Frame不能旋转，表格/泳道特殊手势Hook不作为MCP几何变换承诺。

## 录GIF步骤

1. 先打开Obsidian目标vault和Agent窗口，确认Skill/MCP已连接；开始录屏时不要展示connection.json、token或用户私有目录。
2. 选择上面一个短prompt，展示自然语言输入，不需要把完整底层JSON作为用户操作。
3. 展示原生元素在Obsidian中生成，随后Agent读取摘要/check并看到PNG。
4. 有问题时保留初稿，录下针对ID/关系的局部修复；不要每轮清空重建。
5. 最后在Obsidian中点选/拖动/改一行字/移动节点，证明仍可编辑；重新PNG复核改动，不以录屏效果替代质量检查。
6. 结束当前片段，换下一个独立画布；GIF只是README展示，交付仍保留原图和最终PNG。

建议录三个短片：Visio架构（体现严谨/服务器拓扑）、Rough.js与freedraw对比（体现多风格）、SVG/WaveDrom/源码（体现修改版扩展）。不要把三者叫成不同文件格式或假设所有交互都会进入静态PNG。

## 本轮条件与限制

实际OMP会话与PNG在独立真实Obsidian/vault中执行，未修改用户原素材库或图。上游模型网络错误曾中断扩展页，在核对未创建后重试完成。当前服务器SSH的直接/代理/本地隧道路由未连通，因此本轮新图由本机OMP控制独立本地宿主生成；服务器→宿主拓扑是已实现的远端模式，不把架构示意图当成本轮服务器连通证据。
