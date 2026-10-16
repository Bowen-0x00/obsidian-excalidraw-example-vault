# next-ai-draw-io 可借鉴点

参考项目：[DayuanJiang/next-ai-draw-io](https://github.com/DayuanJiang/next-ai-draw-io)；其MCP文档：[packages/mcp-server/README.md](https://github.com/DayuanJiang/next-ai-draw-io/blob/main/packages/mcp-server/README.md)。这是外部参考，不是本项目的依赖或已移植代码。

## 适合借鉴

### 1. Canvas-first，而不是只返回代码

它把真实draw.io编辑器作为持续预览面，Agent通过MCP修改，用户仍可以手动编辑。适合本项目的对应做法是：

- Obsidian Excalidraw保持真实打开画布；
- Bridge/MCP只绑定明确画布；
- 每轮返回当前revision、PNG和可回读的原生元素；
- 不把“生成JSON/计划”当成完成。

本项目还有更强的原生编辑性约束：元素、文本、绑定、SVG path carrier和素材源都保留，不能为了预览把整图变成PNG。

### 2. 首次上下文 + 增量编辑

next-ai-draw-io要求先`start_session`，随后读当前图，再用`edit_diagram`对现有cell做小修改；没有上下文或状态陈旧时拒绝编辑。这个原则与本项目的`drawing_context(bind)`、`drawing_read`、`baseRevision`/`REVISION_CONFLICT`一致。

可借鉴的交互规则：

1. 创建/绑定后先读状态；
2. 修改时只传逻辑上受影响的节点/边；
3. 用户手动改过后重新读取，不覆盖未知修改；
4. 大重建和局部编辑使用不同路径。

### 3. 内容级编辑门，而不是时间超时

其`edit-gate.ts`不依赖“30秒内没有变化”，而是对模型最后看过的图和当前图做结构指纹比较，忽略编辑器自动重排的非语义属性；发现用户编辑则拒绝陈旧更新。

本项目已有revision和文件/视图身份检查。后续可借鉴其更细粒度的内容指纹思路：对元素ID、业务字段、绑定、组/frame和资源引用做语义快照，忽略Excalidraw会重新生成的version/nonce等内部字段。不能直接把draw.io XML指纹算法复制到Excalidraw。

### 4. 全有或全无的增量操作

它的`edit_diagram`先验证全部操作，任何操作失败都不写入；本项目Bridge已有事务准备、验证与交易记录，但批量操作的原子边界必须以实际响应为准，不应假称所有跨阶段`compose/present/library insert`完全原子。

借鉴结论：每轮结果应明确：

- 计划操作数；
- 实际已执行的阶段和native IDs；
- 失败阶段与原因；
- 是否可通过`drawing_revert`回退；
- 当前revision和下一步读取要求。

### 5. 版本卡片、缩略图和恢复

它保存最近20个版本并为版本提供缩略图，支持比较、恢复和撤销。当前本项目有transaction history和review ledger，但两者职责不同：

- transaction/revert：执行层的操作回退；
- preview/review ledger：视觉检查证据与停止条件；
- 用户vault保存的图：真实长期编辑状态。

可借鉴新增一个面向Agent的“变更摘要 + PNG + revision”展示层，但不要把私有artifact或整个历史自动写入vault。恢复必须基于真实revision/transaction，不能用模型记忆重建。

### 6. 小而明确的工具面

其MCP工具围绕会话、创建、编辑、读取、选择、截图、版本、页面和导出组织，不把每个XML属性拆成独立工具。这个边界适合本项目：`drawing_context/read/plan/apply/check/preview/review/revert`覆盖主闭环；特殊能力通过受控`set_feature`、`drawing_primitives`和`drawing_library`扩展，而不是暴露完整scene JSON让模型随意改内部字段。

## 代码证据

- [drawing-guide.ts](https://github.com/DayuanJiang/next-ai-draw-io/blob/main/packages/mcp-server/src/drawing-guide.ts)：真实工具流程、当前选择、复杂修改后截图、局部编辑规则；不能把其“clear重建”默认带入用户已有画布。
- [compact-cells.ts](https://github.com/DayuanJiang/next-ai-draw-io/blob/main/packages/mcp-server/src/compact-cells.ts)：expand/fold轻量mxCell表示，自动补几何与结构字段；本项目已由EA负责内部字段，不需要另造XML层。
- [edit-gate.ts](https://github.com/DayuanJiang/next-ai-draw-io/blob/main/packages/mcp-server/src/edit-gate.ts)：基于canonical内容指纹拒绝no-context/stale，而不是时间窗口。
- [edit-diagram.ts](https://github.com/DayuanJiang/next-ai-draw-io/blob/main/packages/mcp-server/src/edit-diagram.ts)：验证全部操作后才应用，错误按cell/操作回报。
- [history.ts](https://github.com/DayuanJiang/next-ai-draw-io/blob/main/packages/mcp-server/src/history.ts)：20条快照、稳定entry ID与内容去重，浏览器用户修改/restore来源分别记录。

本轮依据公开源码研究，未运行它的服务，也未将其Apache-2.0代码移植进本项目。更值得马上借鉴的是演示“真实可编辑画布→截图→局部修复”的产品流程，而不是堆更多DSL或替换现有Obsidian执行层。

## 不直接照搬

- draw.io XML不是Excalidraw元素模型，不能用mxCell compact DSL替换当前原生API。
- draw.io的真实浏览器编辑器与Obsidian插件的Canvas/EA/Engine生命周期不同，不能把浏览器session当作宿主view绑定。
- 它的图标库是项目内可控库；本项目的数字电路/微架构库由用户维护，必须实时list/query/get/preview，不把本地库打包到公开Skill。
- 它的服务器可以直接让预览页面在浏览器显示；本项目需要Obsidian Desktop宿主，服务器/远端Agent通过Bridge或SSH隧道控制宿主，服务器本身不能凭空访问vault或渲染窗口。
- draw.io支持多页XML；本项目的frame/presentation保留原生frame与元素，不能声称已经提供PPTX导出。

## 对本项目的具体改进方向

1. 为每次绘图生成轻量的`change receipt`：base revision、affected logical/native IDs、PNG、check、review和剩余问题。
2. 为复杂图新增内容级snapshot摘要，比较元素语义而不是内部version/nonce。
3. 让Agent在服务端绘图时明确“服务器负责模型与MCP，桌面宿主负责Obsidian渲染/文件/资源”；PNG通过MCP ImageContent返回服务器模型。
4. 为常见图型补充短drawing guide和shape/library catalog，不把所有规则塞进一个巨大prompt。

这些改进与当前Skill的PNG闭环、原生元素约束、revision保护和用户素材库规则兼容。
