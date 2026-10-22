# 教学配图：先决定用什么可视结构解释

本模块需要0.10.4及更新运行包。不要把全文摘要拆成s1/s2/s3然后自动套nodes+edges；统一配色不等于统一图法。矩形可以表示token/内存块/计算单元，错误是让每个矩形只表示一段话。

## 绘制前的表达选择关口

1. 提出本图唯一的学习目标：读者应看见什么对象、关系或变化？
2. 提供2–3个适合该目标的候选。每个说明画面会出现什么、解释什么、有什么取舍，并推荐一个。
3. 用客户端真实ask给用户选择，**不是只问手绘／配色**。记录用户指定／answer／明确授权delegated／已有方案inherited及真实证据。
4. 同一套多图先列逐章图法清单，可一轮确认若干图或先确认代表图；其余明确沿用同类设计，不为省事把15章都做文字流程图。用户明确说“你决定”才跳过选择UI；生成候选不等于获得授权。
5. 根据所选方法构造，再检查实际PNG。局部修改保留原确认设计，除非用户要求改图法。

`drawing_begin(action:"prepare",request,design:提案)`返回`design_options`，含question/options/recommended/candidate_ids；Agent应把它交给实际ask。工具不能代替客户端弹窗，也不能验证Agent引用的对话真伪。create/bind需要`brief.teaching_plan`中的selected/choice。没有选择时停止在准备阶段，不先创建用户图。

## 任务单（Agent编写，不让用户填JSON）

```json
{
  "objective":"看懂哪些历史token会被保留",
  "candidates":[
    {"id":"mask","label":"序列＋掩码","approach":"mechanism","description":"token保留布局与注意力格子对应；最直接解释可见范围"},
    {"id":"steps","label":"时间步对照","approach":"mechanism","description":"并排状态解释下一步发生什么；不着重完整注意力矩阵"}
  ],
  "recommended":"mask",
  "selected":"mask",
  "reason":"本章要说明可见范围，不只是叙述步骤",
  "choice":{"source":"answer","evidence":"用户在真实选项中选择序列＋掩码"},
  "goals":[{"id":"visible","requirement_id":"R1","question":"不读长段正文能否看出保留与丢弃？","method":"sequence_window","components":["window"]}]
}
```

放在已有brief的teaching_plan字段，requirements仍逐项保留。教学／学习／图解／示意／机制／画出类新任务不能用general跳过计划。真实物理/逻辑图仍分别用既有专用契约，不能互相冒充。

## 根据学习目标选方法

- 序列、滑窗、sink：sequence_window，token保留状态及行Query×列Key掩码。
- 量化粒度：matrix_groups，同一矩阵按row/column分组，离群值独立可见。
- 存储位宽：bitwidth_compare，**相同数值数量**的等尺度位格长度；这不证明精度或性能。
- 分页/间接寻址：memory_map，逻辑块→映射表→物理池的真实几何连接。
- 重算与复用、窗口移动：time_steps，横向对象、纵向状态；新算/复用/未涉及分别编码。
- 过程、总览、速查：可以选择process/overview/reference及flow/comparison_table，但必须说明为什么适合。选择mechanism/comparison时不能仅用flow/table段落替代。不是强制每张图做立体或更换形状。

这些都是drawing_primitives的kind，支持默认plan或托管render＋state_id/base_revision，同一既有reconciler维护原生ID和外部修改冲突，不增另一种渲染DSL。每个组件使用稳定id；goals.components指向该id。当前自动编码检查覆盖上述五类，不宣称通用语义理解或所有教学题材自动布局。

## 原生输入示例

```json
[
 {"kind":"sequence_window","id":"window","x":60,"y":160,"tokens":["0","1","2","3","4","5"],"window":3,"sinks":1,"step":5,"show_mask":true},
 {"kind":"matrix_groups","id":"keys","x":500,"y":180,"values":[[1,12,2],[2,15,1],[1,11,3]],"group_by":"column","outlier_threshold":8},
 {"kind":"bitwidth_compare","id":"bits","x":60,"y":700,"count":3,"bits":[16,4]},
 {"kind":"memory_map","id":"pages","x":60,"y":1000,"mapping":[4,1,6],"physical_count":8,"block_tokens":4},
 {"kind":"time_steps","id":"decode","x":1000,"y":180,"tokens":["A","B","C"],"steps":[{"id":"t1","active":[0,1],"reused":[]},{"id":"t2","active":[2],"reused":[0,1]}]}
]
```

style.fontFamily从宿主发现。所有文字经真实measure，颜色/位置表示离散状态或等尺度，不猜测实际模型性能。内存块/token数为小例子，必须标示示意；不要混淆示例大小与真实产品配置。

## 验收分两层

**自动层**：按保存的组件source重建期望编码，核对实际非文本cells/blocks/links、位置/尺寸/状态填色、分组、映射端点、数值标签；缺矩阵、缺token、误接物理块、保留状态错误都阻断。不是按矩形比例打审美分，也不是看metadata声明就通过。只写“对角带”“Block Table”的段落没有编码证据。所有TEACHING_*硬错误不可用intentional/false_positive豁免。

**视觉层**：实际查看PNG后，为每个goal提交expression_checks：

```json
[{"goal_id":"visible","outcome":"pass","element_ids":["实际非文本编码ID"],"observation":"看到了前缀保留格与最右侧窗口格，中间格为丢弃状态","without_prose":"无需读段落，位置和色块就能区分保留范围"}]
```

同时完成原来的requirement_checks与本等级visual_checks；只有all-pass布尔值不够。观察必须具体，不能把“文本中提到了”写成“图中画出了”；失败就局部改图，不改写目标为已完成。表达观察仍是Agent自述，工具不冒充独立语义裁判。必要时另一个审阅者只看问题/PNG/实际对象核对，不让作者的总结代替图形证据。

几何失败修坐标／路由；表达失败应重选图法或补真正的对象，不为了check过关删掉机制。无需修改remote已有交付图来试验，使用独立QA画布。
