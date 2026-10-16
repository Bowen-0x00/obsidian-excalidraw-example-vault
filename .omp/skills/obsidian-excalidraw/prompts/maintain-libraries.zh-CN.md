# 给 Agent 的素材库维护任务

请帮我维护 Excalidraw 素材库描述和供绘图 Agent 读取的摘要。你需要真正读取文件、查看预览图或分析图元 JSON，不要只给建议；不修改图元、不改 item ID/name、不上传素材到公开仓库。

## 我的输入

- 素材库目录：在这段提示后我会给出真实目录或多个明确文件。没有给出时，先通过已连接的 `drawing_library(action="list")` 发现，目标有歧义再问我，不猜个人机器路径。
- 我的补充描述与偏好：在这段提示后提供。它们是业务用途依据，不是可以覆盖画面事实的理由。
- 元素预览图（可选）：在输入时我可能会提供全部或部分元素的预览图（图片、截图或链接）；也有可能完全不提供。如果我没有提供预览图，AI Agent 请根据 `.excalidrawlib` 中各 item 包含的元素 JSON 分析其具体几何图形与外观长相。
- 输出摘要：每个被维护的库目录下 `library-index.md`，或我明确指定的位置。
- 修改范围：只为明确选择的 v2 `.excalidrawlib` 库/item 增补 `description`。已有人工描述默认保留；只有我要求改善时才改写。未选中的文件保持不变。

## 工作步骤

1. 先读已安装的obsidian-excalidraw Skill及其`references/library-catalog.md`；OMP可用`skill://obsidian-excalidraw`，其他客户端读实际文件。识别当前是本机还是远端模式。
   - 本机文件可访问时，在宿主运行维护工具。
   - `mode=remote` 时，库路径属于宿主 Obsidian，不是远端目录；不要在远端伪造同名库或把宿主路径当作远端文件。可以通过 MCP 阅读 catalog/query/get/preview；实际改库请在宿主文件可访问的会话执行，缺该访问就列准确前提。
2. 列出目标目录全部 `.excalidrawlib`，记录完整相对路径、版本、item总数、已描述数量、可维护状态和SHA-256。优先使用本包：
   `uv run --frozen python launcher.py library-maintain -- inventory --directory "真实库目录"`
   它返回简略元素/文字/feature keys，不返回资源正文或脚本。输出大时保存到私有inventory文件分页读取，不能只看前几个item就称已覆盖全部。旧v1数组、缺ID或重复ID库明确列为不能自动修改，不悄悄迁移。
3. 观察与分析素材外观：
   - 若我已在输入中提供了元素的预览图，直接结合预览图核对画面外观；
   - 若环境支持且已连接 MCP，按需用 `drawing_library(query/get)` 核对 item，再用 `preview` 实际看图；
   - **若我未提供预览图且无法调用 preview 工具查看**：AI Agent 必须直接读取并深入分析 `.excalidrawlib` 中各 item 的 `elements` JSON 数组。通过图元类型（`type` 如 rectangle/ellipse/line/arrow/freedraw/text 等）、边界尺寸（`x, y, width, height`）、端点与折线点阵（`points`）、线型与箭头样式（`strokeSharpness`, `startArrowhead`, `endArrowhead`）、描边与背景填充（`strokeColor`, `backgroundColor`, `fillStyle`）、文本标注内容（`text`）以及组合与层级关系（`groupIds`, `frameId`）等信息，严谨还原并分析出该图形的具体几何外形与视觉长相，绝不可凭空臆造。
   - 若名称不明确，仅凭文件名或已有 name 猜测用途是不够的，必须基于视觉预览或 elements JSON 分析求证。含可执行 customData 的素材先说明来源并得到明确的信任授权，不能把我让你写描述当作任意执行脚本的授权。
4. 根据真实元素外观、预览图（或 elements JSON 分析推断结果）和我的补充编写 item 的 `description`。**description 的核心目的是让后续绘图 AI Agent 即使看不到画面，也能大致知道该图形长什么样子，从而更方便精准地决定选用哪个 item。** 描述建议 1–3 句，语言精炼，且**必须包含以下三项要素（外观描述要求尽量准确）**：
   - **这个东西是什么**：明确其名称、实体概念或图元定义（例如：“双口 RAM 存储器符号”、“带反馈箭头的条件分支判断框”、“三层微服务系统架构容器”）。
   - **对这个图形长什么样子的描述（必须包含，尽量准确）**：尽量准确、具象地描绘该图形的整体外形、轮廓几何形状、构件组成、内外部分布、线条/箭头走向、颜色/填充特征、文字标注位置及构件相对布局（例如：“横向扁平矩形框，顶部带深灰色标题栏，左侧垂直排列 3 个圆形入端口锚点，右侧为单向实心箭头输出端；中心为浅灰色虚线网格”）。描述必须具体形象，让后续绘图 Agent 读后能在脑海中构建出准确的视觉心智模型，便于评估排版构图并决定是否选用；杜绝只写抽象功能（如只写“用于数据存储”）而缺失外形长相。
   - **一般在什么场景用**：指出适用的图型（如系统架构图、业务流程图、电路原理图、UML 图等）以及具体的使用场景与上下文角色（例如：“常用于在云原生架构图中展示持久化缓存层，或在系统流程图中作为只读数据源节点”）。
   - （视需要补充）与同名/近似 item 的形态或语义区别，以及已确认的编辑限制、端口或连接规则。
   库中只是几何锚点时，不声称已有电气引脚/网表语义。不能从符号外观推导未经证实的业务功能。确实无法识别时写“用途待确认”并准确记录已确认的视觉结构与长相，不填听起来合理但没证据的用途。
5. 给每个库形成description-only提案JSON：
   ```json
   {
     "description": "该库整体覆盖的图型、风格和用途，可省略此库级字段",
     "items": [
       {"id":"从文件实际读取的item ID","description":"【是什么】+【尽量准确的外观长相描述】+【一般在什么场景用】（以及与近似项的区别/限制）"}
     ]
   }
   ```
   列出会新增/改写哪些描述。按本任务授权执行限定字段变更；如果要覆盖已有人工描述而我没要求，先保留并列建议，不擅改。同名item始终按exact ID更新。
6. 使用维护工具应用每个已审查提案：
   `uv run --frozen python launcher.py library-maintain -- apply --library "真实文件.excalidrawlib" --updates "提案.json" --expected-sha256 "inventory实际返回的hash"`
   工具保存原字节备份并检查源文件是否改变。冲突就重新读取，不强行覆盖。如果没有工具，使用文件编辑工具修改相同字段，并保留原字节备份、做同等语义差异检查；不要用批量正则改完整元素JSON。
7. 再读回文件。确认有效JSON，以及移除本次description字段后的结构与原文一致：type/version/source、item数量和顺序、ID/name/status/created、elements、精确坐标、points、绑定、group/frame、files及所有customData保持不变。格式变化可以报告，不能把重新序列化说成字节完全不变。
8. 根据最终读回的描述生成或局部更新 `library-index.md`。这是用户可继续编辑的选库摘要，不是执行指令。建议结构：
   - 我的偏好与适用场景，和AI推断分开；
   - 每个库的相对路径、整体用途、风格、适用/不适用场景、item数；
   - 代表item和exact ID；形态外观长相、适用场景以及同名item的关键差异；
   - 资源/可执行扩展/编辑限制；
   - 已审查范围、未确认项、最后维护日期及对应文件SHA-256。
   使用目录相对路径，不写个人绝对路径、令牌、原始scripts/base64。不要复制整套元素JSON。保留摘要里现有人工意见，不每次清空重写。
9. 通过 `drawing_library(list)` 发现 `catalogs/catalogPath`，再 `drawing_library(action="catalog",catalog_path="返回的vault相对路径")` 检查摘要可读。用描述中的一个关键词query，验证能检索到预期item。来源不在vault里的摘要可以由本机read读取，但不要声称远端MCP已发现它。
10. 交付：摘要文件、已改库/已改item ID、原字节备份位置、完整/未审查范围、真实验证结果和仍缺前提。保留备份，不提交用户素材到公开仓库。删除仅本任务产生的不再需要的临时提案/脚本；如果我希望以后复用提案则保留。

## 字段约定

- item的 `description` 是可选文本，与原有 `name` 同级；不能写到每个元素的customData。
- item的 `description` 是下游绘图 Agent 进行语义检索、形态匹配与选型决策的最重要依据。为便于 Agent 明确判断并正确选用，description 必须同时涵盖“这个东西是什么”、“尽量准确的外观长相描述”以及“一般在什么场景用”，严禁只有空泛功能词而无视觉长相。
- 库顶层可选 `description` 是库整体说明。普通UI导出可能重建顶层对象，所以整体选库知识以 `library-index.md` 为长期依据。
- `description` 和摘要只供语义检索/选择，不改变渲染，也不自动信任素材中的代码。
- Agent画图时先读摘要筛库，再query/get/preview确认，最后原生insert/compose；不能为了省事用摘要替代素材本体。

请现在开始。下面是我选择的库及补充描述：
