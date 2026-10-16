# 分级验收：默认 medium，视觉可读优先

验收等级是交付质量的检查深度，**不是模型effort/thinking、绘图风格、图的内容粒度或导出倍率**。模型low也必须遵守用户选择的high验收，模型high也不能擅自增加无关硬约束。默认medium；当前实现通过MCP/runtime执行，不仅是口头承诺。

## 1. 用户如何选择

- 先解析用户明确写出的“验收low/低等级/检查从简”“验收medium/中等级”“验收high/高等级/严格验收”。具体检查要求优先，例如“允许独立箭头，但文字不能遮挡”不改成强制所有端点绑定。
- 没有明确等级的新图，在本轮真实ask选项中提供**低：快速基本检查／中：可读交付（推荐）／高：严格细查**，与视觉偏好一起问，不再追加一轮冗长问卷。最多五个问题时，颜色编码按用途默认或合入色板描述，留出验收题。已指定/同套图已选/局部改图则继承；“你决定/不要问”直接medium并简短说明。
- “high effort”“多思考”只控制模型工作方式，不自动成为high验收；“手绘”不代表low；“专业风格”也不自动成为最高等级。歧义普通情况采用medium，只有实质冲突才问。
- 将选择作为现有工具的`acceptance_level:"low"|"medium"|"high"`传给check/review或compose/apply。验收设置和已提交expected按canvas context持久保留；后续省略参数会继承，不静默回到medium。显式改等级时记录用户依据，不为刷过关降级。重新bind的新context重新明确本任务选择，不把新token当重置失败预算的手段。

## 2. 三档的实际契约

| 项目 | low | medium（默认） | high |
| --- | --- | --- | --- |
| 用户内容/方向、显式断言、已存在引用正确 | 必须 | 必须 | 必须 |
| 真实当前全图PNG、资源完整、实际查看 | 必须 | 必须 | 必须 |
| 文本互压、后画对象盖字等错误 | 修复已检测错误 | 优先修复，不能带不可读缺陷交付 | 同medium，并逐区细查 |
| 线穿文字、标签遮挡等候选警告 | 提示并在PNG判断，允许披露非阻断提示 | 默认阻断，修复或对具体误报作有证据判断 | 默认阻断，更完整检查交叉/头部/文字净空 |
| 内容与视觉检查记录 | visual_reviewed＋实际问题列表 | 必填content/readability/occlusion | 再加connections/hierarchy_style |
| 小字号/复杂曲线/旋转 | 披露限制、按需局部图 | 需要时看局部；未支持几何逐项确认 | 系统性检查必要局部/语义路径/风格与阅读层级 |
| 非关键装饰/间距瑕疵 | 可作为advisory | 不为小装饰无限修图 | 更细查，但明确cosmetic提示不强制完美主义 |
| 所有箭头必须绑定？ | **否** | **否** | **否** |

绑定的原则：有绑定就不能悬空/互相矛盾；用户要可随节点移动的关系时，才用原生绑定并验移动后行为。独立指示箭头、自由总线/示意支线等可不绑定；不把“绑定率100%”当high通用指标。用户明确要求的某条关系可用已有edge_exists/edge_label断言，不能为了验收把全部独立线硬接到最近节点。

全部等级都不允许：删业务边/文字、降成阶段文字卡片求几何pass、伪造看图结果、忽略资源不完整/真实语义错误。高等级不要求凭空提供RTL仿真、隐藏资源的全Unicode覆盖或不可得的像素级自动证明。

## 3. 判断视觉冲突，不是只判断坐标相交

**先看实际绘制顺序、填充/透明、角色、绑定关系和文字行框，再看PNG。** 当前诊断标明geometry candidate而非像素证明：

- 大矩形在下、文字在上：合法背景/容器，不因相交而移动文字。即使未额外写isContainer，内部文字不自动算冲突；边框真穿进文字则另查。
- 文字先画、后来实色矩形或图片压上：可能盖住字，不能因它名叫“背景”就忽略。透明图片、圆角和半透明区域按真实PNG判断。
- 两段正文/表格文字互压：不是合法包含；同group也不免检。字体变大、换字体、意外换行/基线变化会触发重新测量和邻域检查。
- 无关线/箭头穿过词语：文字本身通常不是整块不透明面板，线“在文字下面”仍可能破坏可读性；线宽/箭头头部包络也要看。
- 线下层＋真实不透明面板＋面板上文字：线被面板确实遮住，文字可读则合法；不能再用纯centerline交点强制拆散。
- 原生箭头自己的bound label可能有原生背景间断，这是合法的标签组织；另一条无关线穿过该label不能跟着豁免。
- 文本框之间的少量AABB相交可能只是空白/字形外接区，曲线、旋转、富文本、SVG/图片alpha也会使几何估计不精确。不要“误报就全关”，也不要“任何相交都改图”。

输出检查的`issueId/elementIds/blocking/evidence/confidence`定位修复对象。小字通过真实preview.actualScale×fontSize计算；当前10px是**检查局部可读性的触发建议**，不是跨字体硬性阈值，也不是可以一律把字号压到10的目标。需要时提供真实可读局部，并把已查看的注册ID放进detail_preview_ids。改变export scale不解决场景内文本碰撞。

## 4. 工具流程与验收输入

1. 简短记录本次内容/关系清单、视觉偏好和等级，不要求用户写坐标。必要语义关系使用已支持的expected断言，原生check不理解全部领域语义。
2. compose/apply可传`acceptance_level`，`inspect:true`返回当前check和PNG。单独check也可设置等级；`preview_id`可指定当前已注册PNG，以输出尺度进行可读性提示。所有参数都与模型effort独立。
3. **先实际查看PNG**，再填写visual_checks（每项pass、not_applicable或fail）与具体visual_issues；不能只复制示例pass。medium必需content/readability/occlusion，high再加connections/hierarchy_style；not_applicable仅用于本图确实不涉及的项目，不能用它跳过有文字图的可读性。
4. drawing_review重新读取当前画布重算诊断；以前check中的expected会保留，不因review未带check_result丢掉。过期PNG/错误revision/改动后的图片或不属于本context的细节图均不接受。
5. 真实缺陷按ID做最小补丁，调整路由、文字位置、字号/换行或容器，保留全文与正确语义；重新保存/read/check/PNG/看图。低档不是允许删除内容，高档不是每轮全部重画。

调用结构示例（ID来自真实返回，示例检查结果必须由实际观察填写）：

```javascript
await drawing_check({context_token: token, acceptance_level: selectedLevel, expected: requiredRelations});
// 查看对应的真实PNG之后：
await drawing_review({
  context_token: token, revision: preview.revision, preview_id: preview.previewId,
  visual_reviewed: true,
  visual_checks: observedChecks,
  visual_issues: observedProblems,
  detail_preview_ids: actuallyViewedDetailIds
});
```

上面是现有工具调用的示意变量，不是另一个DSL；真实客户端前缀/schema以discovery为准。Python客户端对应check(...,acceptance_level=...)、review(...,visual_checks=...)；CLI check/review有`--acceptance-level`，review有`--visual-checks/--dispositions/--detail-preview-ids`，JSON为参数值，不混入命令文本。

## 5. 几何误报/合法叠放如何处理

不能改成容器绕检查，不能删除检测代码，也不能上传一个“ignore all”。若当前PNG证明候选确为误报/有意且不损伤阅读，可在review提交：

```json
{"issue_id":"当前check返回的issueId","decision":"false_positive","reason":"实际查看此revision的PNG后，确认相交区只有字框空白，没有字形被盖；正文完整可读。"}
```

放在`dispositions:[...]`中，decision也可为intentional（必须说明有意构图和为什么仍可读）。仅对当前具体几何候选生效，不跨revision自动沿用；原问题、理由和advisory都会保留。引用损坏、显式内容/关系断言失败、未看图、资源缺失、未做必需视觉检查不能这样豁免。未知几何须按unsupportedChecks生成的issueId逐项检查，review最终返回unresolvedIssues和advisories；不把“带限制接受”伪装成全部自动几何已证明。

默认最多五轮，初图算一轮，连续两次无进展停止。只计算阻断问题的进度，不因不重要装饰提示无限修；有未解决阻断项到上限则needs_attention，保留成果并具体报告。高等级只是更完整的验收，不是无限迭代授权。

## 6. 外部调研：采用机制，不照抄局部假设

| 实际来源 | 借鉴 | 不照搬 |
| --- | --- | --- |
| [coleam00 Excalidraw Skill](https://github.com/coleam00/excalidraw-diagram-skill/blob/main/SKILL.md) | 结构承载含义、层级/多尺度、render-view-fix | 手写完整原生JSON、按模型输出长度一律禁止生成器，不适合本项目现有API |
| [jgraph draw.io Skill](https://github.com/jgraph/drawio-mcp/blob/main/plugins/claude-code/skills/drawio/SKILL.md) | 按图型选自动布局/精准布局、导出前repair pass | 不能推断本项目有ELK/libavoid；自动layout也不证明文字可读 |
| [softaworks draw-io](https://github.com/softaworks/agent-toolkit/blob/main/skills/draw-io/SKILL.md) | 背景/内边距、标签位置、导出后查穿字 | 固定字体、字符数估宽、所有线必须后置、固定2x不能当通用保证 |
| [rnjn Excalidraw Skill](https://github.com/rnjn/cc-excalidraw-skill/blob/main/SKILL.md) | 统一视觉、明确关系与可编辑元素 | 旧字体数字ID/手填版本绑定、仅JSON正确不等于可读 |
| [Anthropic PPTX QA](https://github.com/anthropics/skills/blob/main/skills/pptx/SKILL.md#qa-required) | 内容/结构/视觉分开验收，优先溢出穿字、修后重新渲染 | 不照搬特定Office字体/英寸/装饰偏好，不把模板自带问题当本次新增问题 |
| [Graphviz overlap](https://graphviz.org/docs/attrs/overlap/) | 确定性布局帮助减少节点冲突，保留阅读次序 | 节点overlap removal不等于字形、标签、层级、厚箭包络的视觉验收 |

以上是设计借鉴和接口边界；不声称这些来源本身已经实现本项目的三级验收或自动美学评分。几何诊断只是定位，视觉清晰和用户语义仍需要Agent查看真实PNG并负责。
