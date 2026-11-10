# CDP 只读诊断：解释问题，不直接修图

适用：实际 PNG 不符合预期，而 `drawing_read/check` 还不能解释原因；例如字体／换行、图层遮挡、原生表格、图片资源、嵌入内容、视口和渲染异常。**不是新的绘图引擎，也不是绕过 Bridge 写入约束的后门。**

## 开关与用户选择

默认关闭。Agent 先调用 `drawing_debug(action:"status")`；这个动作只读取客户端私有配置，不探测 CDP。未启用时正常绘图、read/check/PNG/review 都不受影响。

出现难解释的问题时，向用户合并询问一次：

- **保持关闭（推荐日常默认）**：继续 Bridge 状态、几何检查和 PNG；说明无法观察的运行时缺口。
- **开启只读诊断**：用户明确指定调试端口与宿主 vault，允许读取该画布的状态；不授权 CDP 改图／点击。

不因为用户说“画好看一点”“debug一下”就自行开放调试端口。用户已明确开启则不重复询问。用户关闭后立即停止新 CDP 读取；关闭不终止宿主、不关闭其画布或调试端口。

在实际包目录，由用户运行，或在用户明确同意后代执行：

```sh
uv run --frozen python launcher.py cdp -- status
uv run --frozen python launcher.py cdp -- enable --endpoint http://127.0.0.1:19223 --vault-path "D:/Lab/MyVault"
uv run --frozen python launcher.py cdp -- inspect --file "Drawings/Example.excalidraw.md" --limit 100
uv run --frozen python launcher.py cdp -- disable
```

`--vault-path` 是**宿主的绝对路径**，远端客户端不能改填服务器自身路径。配置保存在该客户端私有 state 的 `cdp-readonly.json`，不进 vault、仓库或场景；只对这个客户端生效，不会随 remote-deploy 自动开启。`enable` 只保存选择，不启动 Obsidian、不打开端口、不验证已连接。

MCP 只提供：

```json
{"action":"status"}
{"action":"inspect","file_path":"Drawings/Example.excalidraw.md","ids":["实际elementID"],"offset":0,"limit":100}
```

没有 MCP enable、任意 expression、method、鼠标／键盘、断点或写入字段。

## 启动和目标隔离

用户或管理员显式启动 Obsidian 时增加 `--remote-debugging-port=端口`。诊断工具本身不启动／重启程序，不修改 profile、插件、授信、autorun 或主题。

优先用独立 profile **和独立 vault**验证，不能把“独立 profile”误认为自动隔离日用文件。若用户选择日用实例，也只读取明确已打开的目标。

- endpoint 只允许数字 loopback `http://127.0.0.1:PORT`／`http://[::1]:PORT`，不接受凭据、公网、URL 路径或重定向。
- HTTP discovery 与 WebSocket 必须保持同一个已选择的 loopback 主机／端口。
- 只选择 Obsidian renderer，连接后核对真实 vault 绝对路径；不靠窗口标题或焦点认定目标。
- 多个 renderer 不能猜：从该调试器的 `/json/list` 查看 ID，用户明确选择后重新 `enable ... --target-id ACTUAL_ID`。
- 目标画布必须已经唯一打开。未打开、同文件多视图、加载未就绪均拒绝，不自动 open/focus/select 或改变布局。
- 短连接每次采集后释放。关闭权限不能撤回已返回给模型的内容，也不能打断一条已经开始的短请求。

远端经用户明确配置的 SSH 隧道访问 CDP loopback；**不自动转发 CDP 端口**。已有绘图 Bridge 隧道不等于 CDP 隧道。无 X11 的远端不启动 GUI、不重连用户 vault。

## 只读的实际防线

本包不是裸 CDP 控制器：内部协议白名单只有 `Runtime.enable` 和两条固定 `Runtime.evaluate` 查询。参数是 JSON 数据，不接受模型提供的 JS。

每条查询都设置 V8 `throwOnSideEffect:true`、短超时、`disableBreaks:true`。V8 判断可能有副作用、宿主 API 不兼容或返回异常，就报 `CDP_READ_REJECTED`；**禁止去掉保护重试**。

不调用：

- `Input.*`、`Page.navigate/reload`、`Debugger.pause`／断点／单步；
- `Runtime.callFunctionOn`、任意 evaluate、插件 CLI create/apply/script/export；
- `updateScene`、`mutateElement`、`TableManager` 修改、保存、撤销、导出；
- 页面点击、拖拽、键盘、打开文件、换焦点、切主题、加载资源或插件重载。

**CDP 协议本身不是只读，也不是安全沙箱。** 只读保证的范围是本包诊断器允许发送的固定受保护操作；其他调试客户端仍可能任意执行。只信任受控宿主和本机用户，不把端口暴露到公网。浏览器工具也能接入 Electron，但本模式不能用它的 raw evaluate/点击绕过白名单。

## 返回哪些反馈

| 证据 | 能定位的问题 | 不能声称 |
| --- | --- | --- |
| 原生元素顺序、坐标、style、透明度 | 背景盖字、尺寸／配色未生效 | 属性正确就一定视觉正确 |
| 显示文字／源文字摘要、fontFamily、行高、绑定 | 换行、省略、容器错位 | 已证明全部字形无 fallback |
| 原生 table 角色、行列、主题、边框、列宽 | 新旧表格路径混用、主题未落地 | 已验证拖拽／撤销／所有交互 |
| fileId、imageStatus、资源注册情况 | 引用缺失或资源尚未就绪 | 已证明图片解码或 PNG 像素正确 |
| canvas 像素尺寸、viewport、zoom、scroll、字体集状态 | 视口缩放与成图尺寸混淆 | 自动计算已经覆盖所有装饰包络 |
| console error／exception **计数** | renderer 存在异常线索 | 计数属于当前画布或包含完整历史 |

不读取插件设置、凭据、任意 vault 文件、完整 console 参数、任意 iframe 内容或图片数据 URL。Console／exception 只记录连接时缓存及采集期间事件计数，不返回可能包含无关文档／秘密的文本或对象。

元素按 `offset/limit` 分页（最多200），可按最多100个真实ID筛选。`coverage/count/truncated`说明范围；文本摘要240字符，标记截断，不能当作全文证据。坐标原精度仅用于诊断，不反向覆盖画布。

`sceneFingerprint` 来自同一次同步读取前后核对的原生身份／版本列表；**不是 Bridge revision**，不能传给 `drawing_apply`。用户在两个页面之间修改图时，比较 fingerprint，必要时重新读取，不能拼成假一致快照。

## debug → 正常微调 → 再验收

1. 保存问题描述与当前PNG／check，定位可能相关的真实element IDs。
2. 检查只读开关；未开启时解释收益与读取范围，请用户选择，不自动启用。
3. `drawing_debug(inspect)` 读取同一宿主／文件的相关元素及运行时状态。受保护读取被拒绝就报告缺口，不改用任意脚本。
4. 把反馈拆成**已观察事实**、**原因假设**、**最小修法**。不要把console计数、资源注册或字体状态当成根因证明。
5. 微调只能走用户原任务授权的 Bridge/API：重新 `drawing_read` 取得当前file/context/revision，用实际ID局部修改；DSL受管内容按DSL源/state更新，不能CDP改后绕过所有权。
6. 超出原任务的修改另问用户。只允许诊断的会话不提交任何修复。
7. 修改后仍要正常 check、真实 PNG、实际查看和 review。CDP状态不能替代最终视觉验收。

本模式的“debug”是**无暂停、无写入的状态排查**；不是修改变量、交互回放或通过CDP微调画布。需要这些开发操作必须另立明确授权的隔离测试任务，不扩大本开关含义。
