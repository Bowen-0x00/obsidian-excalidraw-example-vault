# 可选 Scene DSL：选空间表达，不替代原生能力

0.9.0起随同一个包发布。Agent把自然语言组织成精简YAML/JSON场景；编译器调用现有文字测量、布局/路由与原生事务。不是另一个渲染器，也不是要求用户学新语言；不能把DSL schema混入drawing_compose的diagram。

## 什么时候用

- 可重复生成/版本管理、嵌套row/column/grid区域、表格、命名端口结构图：优先DSL。
- 一次普通节点图：现有compose仍更直接。
- 用户库、交互/导航、动画、任意扩展、已有非受管图精确小改：保留现有native工具。
- 硬件先读microarchitecture：DSL不证明电气/RTL正确，不以形状存在代替信号清单。当前groups是可见布局区域，不是原生groupIds/frame；复合部件GUI拖动语义不自动具备。

## MCP路径

只使用真实discovery返回的`drawing_dsl`。没有此工具则更新并重启MCP，或使用已安装新版CLI，不能发明tool。

- `action:"render"`，`document:已解析的场景对象`，`font_family:当前宿主实际family`；首绘用唯一`filename`和可选`foldername`，或明确现有`file_path`。
- `state_id`默认document.id，同一源重复提交必须复用；同源另画一张用不同state_id。身份状态在客户端私有目录、按宿主/vault隔离，不放vault/Git，不包含认证token。
- `action:"plan"`只规划；需要已有state或明确file_path供真实测量，不是假字体的离线布局。
- render返回file/contextToken/revision/stateId、operationCount/diff、check、preview和实际PNG ImageContent；`visualReviewed:false`不是完成。实际看图，再用现有drawing_review记录本等级清单；需细节就真实preview局部。
- 相同源为0绘图操作；源变化按ID更新/删除自有对象，保留不受管内容。原生API改了受管文字/位置/样式/绑定/锁定就冲突，不自动adopt/强行覆盖。不要用compose整图重放或删除state绕过冲突。

## 文件/CLI路径

在真实安装包目录运行；已有EXCALIDRAW_AGENT_STATE_DIR继续选择同一连接。CLI不要求LLM或MCP客户端，但仍需要真实GUI宿主Bridge。

```sh
uv run --frozen python launcher.py dsl -- fonts
uv run --frozen python launcher.py dsl -- render examples/dsl/release-flow.yaml --font "EXACT_HOST_FAMILY" --state-id release-demo --filename "Release-Demo-Unique" --output ./output/release.json
uv run --frozen python launcher.py dsl -- plan examples/dsl/release-flow.yaml --font "EXACT_HOST_FAMILY" --state-id release-demo --output ./output/plan.json
```

EXACT_HOST_FAMILY必须替换为当前返回的实际family。改YAML后同state-id再render；报告/PNG路径属于客户端，非远端宿主路径。CLI review接收真实观察JSON（visual_checks/visual_issues及可选dispositions/detail_preview_ids），命令`launcher.py dsl -- review --report ... --checks ... --output ...`。exit0仅命令成功，render仍待视觉评审；exit1执行错误；exit2检查/资源或review未完成。

## 够用的作者层

顶层version:1、稳定id、nodes/edges、layout；可选title/style/classes/groups/acceptance。节点字符串是label简写。shape支持box/ellipse/diamond/text、原生cell表格、mux/alu/polygon和image/formula/embed/chart资源。表格内部直角、深浅表头，不把Table Engine尚未提供的功能伪造成DSL能力。

布局row/column/grid支持gap；root flow仅普通无group图；root origin和node.at允许负场景坐标。端点node、node.side、node.named_port；ports为side[:0..1]。显式via是全局轴向折点，label_at是路径比例；不能混用线元素局部points。资源size为预留区；公式用裸tex，ECharts用完整结构化options，不执行脚本。

严格拒绝重复/未知键、缺引用、重复布局、包含环、YAML alias和可执行tag。边界是512KB源描述、100逻辑节点+边、表格12列/20数据行、450初始显式操作/500增量操作；不是宿主像素或最大画布限制。改变构造/资源源内容及新增原本不存在的bound label需要新逻辑ID；表行列按序号，不是数据库行主键。

失败时查看error/path/details/committedReceipt及当前真实画布。检查/导出发生在身份状态保存之后，不能把后续失败说成未提交。一个state-id并发操作会拒绝；进程异常后先查PID/画布，再明确移除私有.lock，不自动重试未知事务。

完整公开规范与真实示例在包内`docs/scene-dsl.md`、`docs/gallery.md`、`examples/dsl/`和`examples/native/`；在线入口：[规范](https://github.com/Bowen-0x00/obsidian-excalidraw-agent-skill/blob/main/docs/scene-dsl.md)。源码、原生画布、PNG、检查/实际评审共同作为交付，不把图片输出当可编辑源或审美自动证明。
