# 原生 Excalidraw CLI

这是插件自带的执行入口，不是本包的 `launcher.py cli`。它适合明确文件的读取、简单创建、局部编辑和导出；自动布局、复杂图元、素材组合、几何诊断和远端 PNG 反馈仍优先用 `drawing_*` MCP。

## 选择入口

| 当前环境 | 使用方式 |
| --- | --- |
| 已连接本包 MCP，尤其 `mode=remote` | 继续用 `drawing_*`；不要在无GUI远端调用不存在的宿主 Obsidian 可执行文件 |
| 在运行 Obsidian 的本机，有插件原生 CLI | 简单文件操作可直接调用原生命令，先读取 `status`、`help`、`schema` |
| 在可信 EA 脚本中，插件有 `ea.executeCLI` | 调用同一 JSON 协议；它不是一个终端程序，也不是远程监听服务 |
| 没有原生 CLI，也没有可用 MCP | 明确报告前提缺失；不能直接拼完整场景 JSON 冒充可靠执行 |

一次编辑保持一个入口：Native CLI 的 `expectedRevision` 与 Bridge 的 `baseRevision/contextToken` 不可互换。切换入口后重新读取目标身份与版本。

## 能力发现和正确命令前缀

终端入口要求：Obsidian Desktop 正在运行、API 1.12.2+、CLI 已启用、插件包含 Native CLI handler、`registerCliHandler` 在运行时存在。Windows 捕获 stdout 使用实际 `Obsidian.com`，不要把图形入口 `Obsidian.exe` 当成可保证返回 JSON 的 console launcher。

ymjr 安装的 manifest ID 是 `obsidian-excalidraw-plugin-ymjr`，所以示例前缀如下。原版文档可能使用 `obsidian-excalidraw-plugin`；必须按实际插件 ID/帮助输出确认，不能照搬前缀。

```sh
obsidian vault="目标vault" obsidian-excalidraw-plugin-ymjr:status
obsidian vault="目标vault" obsidian-excalidraw-plugin-ymjr:help
obsidian vault="目标vault" obsidian-excalidraw-plugin-ymjr:schema action=create
obsidian vault="目标vault" obsidian-excalidraw-plugin-ymjr:api surface=ea name=measureText
```

`vault` 放在命令之前。检查 `data.vault`、`data.ready` 和 `data.nativeCLI`，不能把进程退出码 0 当成功。CLI 的 `status` 反映被命令选中的 vault，不代表所有 Obsidian 窗口中获得焦点的那个。

进程内入口不依赖终端 CLI 设置或 1.12.2 的注册 API，但要求已安装的插件版本实际提供该方法：

```js
if (typeof ea.executeCLI !== "function") {
  throw new Error("当前插件没有 executeCLI；请使用可用 MCP 或更新插件");
}
const status = await ea.executeCLI({ apiVersion: 1, command: "status" });
if (!status.ok || !status.data.ready) throw new Error("插件尚未就绪");
```

不要通过 CLI 的一次性 `script` 命令启动常驻 Bridge/Engine：该命令结束会清理请求所属 EA 与注册资源，不能把它当成服务管理入口。

## 请求与回执

- 所有 JSON 请求包含 `apiVersion:1`；进程内请求必须有 `command`。
- 所有写操作（`create/apply/export/script`）必须有唯一 `requestId`：1–80 个字母、数字、`_`、`.`、`-`。
- 相同有效请求和相同 ID 可恢复已有回执；不同内容不能复用 ID。丢失 stdout/超时后先 `result requestId=...`，不要用新 ID 重发未知写操作。
- 回执仅在插件会话中保存，最多 128 项、完成后 15 分钟过期；重载或未知结果后先读回目标。
- 写入成功检查 `ok=true`、`mutation` 与 `persistence`。`applied + unsaved/unknown` 表示可能已变更但尚未可靠保存；先检查/保存原图，不清空重建。
- 大请求放在可见的 vault 相对 UTF-8 JSON 文件，通过 `input=...` 传入；小请求可用 `json`。两者不能同时使用；flags 和 JSON 字段必须一致。

## 创建与编辑

先用真实 EA/MCP 文字测量和明确布局组织内容。Native CLI 只接收精简 skeleton，不会根据业务描述自动布局。

示例请求存为 `CLI/create.json`；这是输入例子，不是用户事实：

```json
{
  "apiVersion": 1,
  "command": "create",
  "requestId": "flow-create-1",
  "path": "Drawings/Flow.excalidraw.md",
  "elements": [
    {"id":"start","type":"rectangle","x":0,"y":0,"width":220,"height":90,"label":{"text":"提交申请"}},
    {"id":"end","type":"rectangle","x":360,"y":0,"width":220,"height":90,"label":{"text":"完成处理"}},
    {"id":"edge","type":"arrow","x":220,"y":45,"start":{"id":"start"},"end":{"id":"end"},"endArrowhead":"arrow"}
  ]
}
```

```sh
obsidian vault="目标vault" obsidian-excalidraw-plugin-ymjr:create input="CLI/create.json"
obsidian vault="目标vault" obsidian-excalidraw-plugin-ymjr:open path="Drawings/Flow.excalidraw.md"
obsidian vault="目标vault" obsidian-excalidraw-plugin-ymjr:read path="Drawings/Flow.excalidraw.md" source=live detail=elements limit=200
```

`create` 使用精确路径并拒绝覆盖，不自动改名。`data.idMap` 将输入局部 ID 映射到实际 ID；绑定文字的 ID 从 `createdIds` 和读回元素中获取。多 view 时传实际 `viewId` 对应的 `view`。

原生 CLI 与 Bridge schema 不同：

- Skeleton 样式是顶层字段，容器文字用 `label`；不是 Bridge operation 的 `style` 对象。
- Native CLI只接受其当前schema声明的fontFamily类型/范围；此前安装版本实测为数字ID 1–10，这不是跨宿主保证，也不证明这些ID对应哪些字体。先按[typography](typography.md)发现实际family，再用本机已验证映射；不能把MCP支持的字符串或另一版本的编号表硬传入受限接口。无法映射时使用已发现的可信EA/MCP入口，不绕过拒绝规则。
- 受支持的基础类型为 rectangle、ellipse、diamond、text、arrow、line、frame、stickynote。frames 不嵌套，children 引用同批 ID。
- `apply` 使用 `operations:[{op:"update",id:"实际ID",set:{...}}]`，不是 `patch_element/target/patch`。
- 改标签更新实际 bound text ID。identity/version/binding/frame/资源内部字段及任意 `customData` 不在普通 update 接口中；不要绕过拒绝规则。
- image 操作使用宿主 vault 的真实资源；latex 需要已启用且兼容的 Extras MathJax。复杂扩展优先用现有 MCP Feature adapter，而非未经授权执行脚本。

每次编辑先重新 `read source=live`，取 `data.revision` 作为 `expectedRevision`。发生 `STALE_REVISION` 则刷新，不复用旧 revision；`BUSY` 也先核对状态再决定是否重试。

## 全图读取与 PNG 评审

`read` 默认 summary 只有计数、类型和版本，**不是所有元素的简略列表**。需要元素时用 `detail=elements`：默认 50、最多 200 个/页，按 `nextOffset` 遍历，后续页使用同一 `revision`；遍历中版本变化从第一页重新读取。可由执行脚本将这些元素压缩为 id/type/geometry/text/bindings 摘要；不要把反馈四舍五入坐标反向覆盖原图。

```sh
obsidian vault="目标vault" obsidian-excalidraw-plugin-ymjr:export path="Drawings/Flow.excalidraw.md" source=live out="Drawings/Flow.png" requestId=preview-1 scale=1 padding=20
```

- PNG 写到明确的宿主 vault `out`，并返回 `data.path/width/height/bytes/revision/source`。它不返回 MCP ImageContent，也不会自动把文件传给远端Agent；远端继续用 `drawing_preview`。
- 已有输出必须明确 `overwrite=true`；不能替换图、请求文件或源资源。live export 不会隐式保存 drawing。
- Native PNG scale 0.1–4；当前原生导出预算为 1600 万像素、每边 16384 像素。这是该接口的代码限制，不是所有 Excalidraw/Bridge 渲染器的通用上限。先 scale=1，按 bounds 和返回尺寸控制，必要时用 `area` 做局部图。
- 真正读取 PNG 检查中文全文、文字容器、方向、分支标签、交叉、资源和颜色；成功回执不等于视觉通过。
- Native CLI 没有本包的 `drawing_check` 或 `drawing_review` ledger。若走原生-only，必须记录相同的最多5轮检查/修复过程，并交付真实输出路径、保存结果、已执行检查和仍未覆盖的几何约束；不能伪造 `check=pass`、`previewId` 或 ledger。
- 如已使用 Native CLI 更新一个 MCP 绑定图，重新读取 MCP 当前状态后走其 check/preview/review，不能将 Native PNG 冒充已注册的 MCP 预览。

## 可信脚本边界

`script` 仅用于用户明确授权的既有本地脚本，要求 `trusted=true`；参数通过 `utils.input`，不要插值进源码。`utils.excalidrawLib` 是真实运行时，`api surface=lib` 是有意提供的帮助子集，不证明所有 exports 都已公开给 CLI。

脚本不是沙箱、事务或可强制撤销的任务。await 所有变更与保存，不保留 timers/hooks。utility prompts 会报 `INTERACTION_REQUIRED`；其他交互 API 仍可能弹 UI，因此不能用脚本掩盖缺依赖/授权。

源码依据：插件 `docs/CLI.md`、`src/core/managers/ExcalidrawCLI.ts`、`src/core/cli/cliCommands.ts`、`cliElements.ts`、`cliExport.ts`，以及 `src/shared/ExcalidrawAutomate.ts:executeCLI`。公共入口以安装版本的 `help/schema/status` 为准。
