# 分级验收：先询问 review 等级，再执行质量门

验收等级是交付质量的检查深度，**不是模型effort/thinking、绘图风格、内容粒度或导出倍率**。新图先问用户选low／medium／high；medium仅为推荐项或用户明确授权默认值时的起点，不是无需询问的许可。用户选high则模型low也必须执行high。

## 1. 用户如何选择

- 先解析用户明确写出的“验收low/低等级/检查从简”“验收medium/中等级”“验收high/高等级/严格验收”。具体检查要求优先，例如“允许独立箭头，但文字不能遮挡”不改成强制所有端点绑定。
- 没有明确等级的新图必须真实ask：**low基本检查／medium可读交付（推荐）／high严格细查**；与style同轮优先询问，不为了省轮次跳过。仅给出style没有给review时，仍问review；“画好图／重试／继续”不是默认授权。
- 只有本次明确指定、原图／同套图明确继承，或用户明确授权“不问／全部默认／review你决定”才不问；任务单记录每项来源和证据。字体风格“你决定”不等于review也由Agent决定。
- 已选review通过`brief.preferences.review`持久保存；check／apply／review显式传不同等级会拒绝。重绑同文件继承同一任务的轮数、断言和未解决项。新用户请求在原任务完成后可建立新的编辑任务；不能为刷通过改task_id或换图。

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

1. 创建前记录`brief.requirements:[{id,description}]`，覆盖用户要求的对象、比较、关系、精度／时序条件和明确省略项。必要关系仍用expected；模型生成文字与自身label_equals一致，只证明复制完整，不证明用户需求／科学主张正确。
2. compose/apply可传`acceptance_level`，`inspect:true`返回当前check和PNG。单独check也可设置等级；`preview_id`可指定当前已注册PNG，以输出尺度进行可读性提示。所有参数都与模型effort独立。
3. **先实际查看PNG**，再填写visual_checks（每项pass、not_applicable或fail）与具体visual_issues；不能只复制示例pass。medium必需content/readability/occlusion，high再加connections/hierarchy_style；not_applicable仅用于本图确实不涉及的项目，不能用它跳过有文字图的可读性。
   medium／high若overview字高低于10px触发值，必须提交覆盖这些text IDs的当前可读`scope:"ids"`局部PNG，或修复布局。此值是补充阅读证据门，不是通用字形可读阈值，更不能通过无限提高全图scale解决碰撞。
4. drawing_review重新读取当前画布重算诊断；以前check中的expected会保留，不因review未带check_result丢掉。过期PNG/错误revision/改动后的图片或不属于本context的细节图均不接受。
5. 真实缺陷按ID做最小补丁，调整路由、文字位置、字号/换行或容器，保留全文与正确语义；重新保存/read/check/PNG/看图。低档不是允许删除内容，高档不是每轮全部重画。
6. review=completed后调用`drawing_deliver`，以同文件/当前revision/同一全图PNG及hash、完成评审、需求与表达契约重新核验。只有deliverable回执才进入交付；check pass、生成成功、工具报错后的自然语言“完成”均不能替代。门禁不证明Agent真的理解用户或看了图，也不限制它绕工具说假话；它提供可核验状态而非信任沙箱。

### 数学内容专项验收（所有等级）

- 内容清单中有矩阵／数学向量／转置、分式／求和／递推／成组上下标时，在brief.requirements加入对应数学表达要求，并先读[数学分流](visual-content.md#数学内容分流-先认语义再选元素)。不用新增未知API字段或全局正则猜测信号名。
- 核对实际创建了公式image/fileId、保存的源TeX与可读PNG；逐项检查矩阵行列／整体括号、上下标归属、分子分母、符号／数值和混排基线。不是只查裸`$`、反斜杠或label_equals。算术／RTL验证与数学排版分别记录。
- `requirement_checks`引用真实公式IDs并说明源与PNG观察；正文／代码／RTL信号及位串引用其原生text IDs。数学清单非空却没有公式资源、仍用空格拼矩阵／Unicode拼上标，且无明确字面显示例外时，content或readability必须fail；不能以无碰撞或resources complete放行。
- 公式内容是image，现有小text检测不能自动证明公式内部字高可读。高矩阵、分式或密集上下标按需导出当前局部PNG。能力不可用／渲染失败明确报告，不静默降级ASCII或截图；本清单仍需Agent诚实执行，不声称几何检查已自动理解数学。


调用结构示例（ID来自真实返回，示例检查结果必须由实际观察填写）：

```javascript
await drawing_check({context_token: token, acceptance_level: selectedLevel, expected: requiredRelations});
// 查看对应的真实PNG之后：
await drawing_review({
  context_token: token, revision: preview.revision, preview_id: preview.previewId,
  visual_reviewed: true,
  visual_checks: observedChecks,
  visual_issues: observedProblems,
  requirement_checks: observedRequirementCoverage,
  detail_preview_ids: actuallyViewedDetailIds
});
```

`requirement_checks`每项含`{requirement_id,outcome:"pass"|"fail",element_ids:[当前真实ID],evidence:"这些对象如何满足这项用户要求"}`，所有需求逐项覆盖；不支持用not_applicable省略用户要求。未覆盖／fail阻止completed，缺失或已删除ID会拒绝。CLI用`--requirement-checks`，DSL review观察JSON使用同名字段；模型仍需负责真实性，工具不自动验证数学／硬件精度。

## 5. 几何误报/合法叠放如何处理

不能改成容器绕检查，不能删除检测代码，也不能上传一个“ignore all”。若当前PNG证明候选确为误报/有意且不损伤阅读，可在review提交：

```json
{"issue_id":"当前issueId","element_ids":["受影响ID1","受影响ID2"],"preview_id":"当前已注册且实际查看的局部PNG ID","decision":"false_positive","reason":"具体解释这两个对象的相交区为何仅含空白，指出可辨文字与相对位置；不可复制统一理由。"}
```

每项必须匹配当前issue的完整element_ids、已查看的preview_id和独立理由，重复理由会拒绝。**TEXT_TEXT_OVERLAP／TEXT_PAINTED_OVER／LINE_THROUGH_TEXT／BORDER_THROUGH_TEXT／TEXT_OUTSIDE_CONTAINER／ARROW_LABEL_OCCLUSION不能intentional豁免**；确属误报时仅允许false_positive，并提供同revision、scope:"ids"包含全部受影响对象、字高可读的局部PNG。其它合法叠放／未知几何仍可逐项intentional说明，不删除此能力。语义、引用、资源、需求未验证不可豁免。

默认最多五轮，初图算一轮；连续两次无改善停止。账本按宿主vault＋文件＋任务保存，重绑新token不重置。重新导出同一revision只改变PNG ID，不代表已修复；原始hardIssues与rawCheckStatus始终保留。达到上限／needs_attention时保留成果报告，不新建“clean／v2”或修改state_id绕过。

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
