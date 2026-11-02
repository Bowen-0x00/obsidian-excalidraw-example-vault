# Agent 接入与运行配置

同一份 `skills/obsidian-excalidraw/` 和同一个stdio MCP可供不同Agent使用。Skill说明流程，MCP提供工具，Obsidian负责真实执行；客户端只是安装目录、配置格式和调用名称不同。

本包当前发布的Skill正文为中文。Claude Code/Codex等支持该Skill目录格式；本文依据官方配置文档，不声称已在每种客户端运行完整绘图会话。已有真实验证包括stdio MCP及OMP绘图，客户端自身图片展示能力仍需检查。

## 通用安装

从仓库根目录执行`uv sync --frozen`。复制**整个**`skills/obsidian-excalidraw/`到Agent的Skill目录，别只复制SKILL.md。所有references/prompts相对该目录；`skill://...`只是OMP提供的访问方式，其他Agent读取相应本地文件。

配置本地stdio MCP启动命令：

```text
uv run --frozen --project /absolute/path/to/package python /absolute/path/to/package/launcher.py serve
```

参数路径使用实际绝对路径，含空格时正确引用。`serve`运行的是MCP stdio进程，不能把Bridge的`http://127.0.0.1:27124`配置成远程MCP URL；Bridge是本包内部鉴权协议，不是MCP HTTP服务。

0.9.0同时提供可选DSL，不另装服务：MCP增加drawing_dsl，CLI为`uv run --frozen python launcher.py dsl -- ...`；普通原生CLI仍是`launcher.py cli -- ...`。无LLM/MCP客户端也可用CLI调用同一真实Bridge。DSL规范/示例随包在docs和examples中；私有scene-dsl身份状态随原connection state保留，升级不删除；能力选择与命令见[scene-dsl](scene-dsl.md)。

通用JSON示例（替换路径；不要直接覆盖已有MCP配置）：

```json
{
  "mcpServers": {
    "excalidraw": {
      "command": "uv",
      "args": ["run", "--frozen", "--project", "/absolute/path/to/package", "python", "/absolute/path/to/package/launcher.py", "serve"],
      "env": {"PYTHONUTF8": "1"}
    }
  }
}
```

首次初始化前安装依赖可避免客户端较短startup timeout；绘图/导出工具允许足够调用时间（例如180秒），按该客户端实际选项配置，不复制别家的timeout字段。

## Claude Code

用户级Skill：`~/.claude/skills/obsidian-excalidraw/`；项目级：`.claude/skills/obsidian-excalidraw/`。手动调用`/obsidian-excalidraw`或自然语言请求。

```sh
claude mcp add --transport stdio --scope user excalidraw -- uv run --frozen --project "/absolute/path/to/package" python "/absolute/path/to/package/launcher.py" serve
claude mcp list
```

使用项目MCP时，可把上述JSON条目合并到项目`.mcp.json`并按客户端要求批准。仓库根`mcp.json`是OMP包配置，含`${PLUGIN_DATA}`；**不是可直接复制的Claude配置**。本仓库也提供Claude插件元数据，但本说明采用明确的Skill复制+MCP注册路径，不假设不同插件管理器会替换同一组占位变量。

官方：[Skill安装位置](https://code.claude.com/docs/en/skills)、[MCP配置](https://code.claude.com/docs/en/mcp)。

## Codex

用户级Skill：`~/.agents/skills/obsidian-excalidraw/`；项目级：`.agents/skills/obsidian-excalidraw/`。通过`$obsidian-excalidraw`、`/skills`或自然语言选择。

```sh
codex mcp add excalidraw -- uv run --frozen --project "/absolute/path/to/package" python "/absolute/path/to/package/launcher.py" serve
codex mcp list
```

也可以合并到`~/.codex/config.toml`：

```toml
[mcp_servers.excalidraw]
command = "uv"
args = ["run", "--frozen", "--project", "/absolute/path/to/package", "python", "/absolute/path/to/package/launcher.py", "serve"]
startup_timeout_sec = 60
tool_timeout_sec = 180

[mcp_servers.excalidraw.env]
PYTHONUTF8 = "1"
```

官方：[Skill安装](https://developers.openai.com/codex/skills)、[MCP配置](https://developers.openai.com/codex/mcp)。Skill正文的相对文件路径与workflow不依赖Codex特有配置，不要用OMP的`/reload-plugins`指令代替Codex重载。

## OMP示例

```sh
omp plugin marketplace add Bowen-0x00/obsidian-excalidraw-agent-skill
omp plugin install --scope user obsidian-excalidraw-agent-skill@obsidian-excalidraw-agent
```

重启或`/reload-plugins`，`/mcp list`确认工具，再用`skill://obsidian-excalidraw`读取。OMP包内`mcp.json`通过`${PLUGIN_ROOT}`/`${PLUGIN_DATA}`定位代码和私有状态，不要求用户手抄token。

## 先区分浏览 vault 与安装 Agent 包

打开某个 vault 目录或浏览其中 Markdown，不会安装本包、注册 MCP、启动 Bridge，也不会切换绘图目标。Skill／MCP／独立 CLI 的安装属于客户端；vault 注册、插件、Bridge、字体和素材属于 GUI 宿主。cwd 只影响项目文件发现，不能作为连接选择证据。

## 自动发现、明确选择与只读状态

保持目标 Obsidian 及其 Bridge 运行。**0.13.8 bootstrap／Bridge** 会自行创建本机私有、逐 vault 的 `connections/<vault_id>.json`，记录宿主／vault 身份与连接参数；不需要把 token 复制进 Agent 配置或提示。描述文件的 vault ID 是规范化绝对路径（Windows 转小写）的 SHA-256 前 24 位，不等同于 Obsidian 自己的注册项 ID。状态与目录只显示安全摘要，不返回凭据。

宿主发现位置固定为平台默认数据目录，即使客户端另设 state：

| 宿主平台 | 自发布描述文件目录 |
| --- | --- |
| Windows | `%LOCALAPPDATA%/ObsidianExcalidrawAgent/connections/` |
| macOS | `~/Library/Application Support/ObsidianExcalidrawAgent/connections/` |
| Linux | `${XDG_DATA_HOME:-~/.local/share}/obsidian-excalidraw-agent/connections/` |

本机客户端只在没有显式连接覆盖时发现本机描述文件；唯一候选可直接使用。已有目标不会因为新增 vault、切换 cwd 或重新部署远端而被自动替换。多候选必须由用户按 ID／唯一名称选择；不默认第一项，不扫描端口，不无鉴权探测，不遍历远端磁盘。显式 `EXCALIDRAW_AGENT_CONFIG`／URL／token 等环境覆盖损坏时明确报错，不悄悄改连另一库。

在包目录运行（客户端已注册时也可用 `drawing_setup(action="status")`，其输出始终为 JSON）：

```sh
uv run --frozen python launcher.py status
uv run --frozen python launcher.py status --json
uv run --frozen python launcher.py doctor
uv run --frozen python launcher.py doctor --json
uv run --frozen python launcher.py vaults
uv run --frozen python launcher.py vaults --json
uv run --frozen python launcher.py use "VAULT_ID_OR_UNIQUE_NAME"
```

- `status`：只读报告实际 host／vault 身份、目标路径、传输／SSH、Bridge／plugin 版本、画布就绪度／打开列表、Engine、客户端 state 和选中配置位置。默认人类可读，`--json` 供自动化；不部署、启动或改选连接。
- `doctor`：同样只读；鉴权、连接、目标身份或配置故障时非零退出。`NO_CANVAS` 是已连接但尚无可用画布，不当成连接故障，不为诊断偷偷创建图。
- `vaults`：分开列出已知本机发现／已配对远端 profile，以及宿主注册 vault 目录。远端目录通过已鉴权 `GET /v3/vaults` 获取，含 pluginEnabled／running／selected。注册不代表已运行或已配对；连接目录不可用时仍保留已知 profile，并报告目录故障。
- `use SELECTOR`：明确选中已发现本机连接或已配对远端 profile；接受 ID 或唯一名称，不接受远端 Windows 路径，不启动宿主 GUI。选择只改变本客户端连接配置，不重装脚本或轮换宿主 token。显式环境覆盖仍优先，应先解决冲突覆盖再切换。

读取 `GET /v3/status` 的实时 host／vault、pluginVersion、openCanvases、engines 以核对身份；不能把 `configured:true`、旧 profile 路径或注册记录当实时服务证明。无画布时先按真实绘图需求 create 或明确 bind；不能为了让 doctor 通过而创建文件。

## 首次宿主部署与受管脚本更新

**只在 GUI 宿主**执行首次 connect／脚本更新，不在 headless 远端执行。已有匹配 Bridge 自发布连接时无需重新 connect。

```sh
uv run --frozen python launcher.py connect
# 多个已注册 vault 时选择返回的 ID／唯一名称：
uv run --frozen python launcher.py connect --vault-name "VAULT_ID_OR_UNIQUE_NAME"
```

`--vault "/实际本机路径"` 仍保留给未注册库等高级本机场景；远端不要求也不接受这种宿主文件路径。

`connect` 在本机选择明确的已注册 vault，将受管脚本部署到插件 `settings.scriptFolderPath` 下的 `Agent-Drawing/`。文档称该根目录为**绘图脚本目录**，不改用户目录名、不假设固定路径。自动 URI 启动需要 Advanced URI；否则在目标 Obsidian 手动运行 `Agent-Drawing/mcp/Start-Agent-Drawing`，新命令未索引时重载 Obsidian。匹配的 0.13.8 Start 会修复缺失或属于别的 vault 的已复制描述文件；这不是要求用户手抄凭据。

`launched:false, advanced_uri_enabled:false` 表示命令未自动发出；不要反复 start／connect 或轮换 token。`configured:true` 不等于 `connected:true`，也不证明运行中的 Bridge 已升级。更新时 Start 与 Bridge 均须为 0.13.8；仅复制 Skill 或换客户端包不会替换已运行宿主。

`Refusing to overwrite a modified or unmanaged script` 是覆盖保护，不是凭据故障。保留文件，比较真实已发布源码与既有安装记录。**禁止重新算当前文件 hash 写入 installation.json 伪造所有权**，禁止整目录覆盖或搜历史 token 绕过保护。无法安全确认时报告具体冲突，等用户选择保留／按公开版本迁移。

长驻客户端在每次请求前重新读取未显式固定的私有连接配置；显式构造参数和环境变量仍优先。旧 MCP 需 reload 以加载新代码。不做 401 重试，不重放结果未知的写操作；setup 已连接但绘图仍鉴权失败时检查旧进程、环境覆盖和实际目标，不搜历史凭据。

| 内容 | 存储位置 |
| --- | --- |
| 原生图、字体、用户素材 | GUI 宿主 vault 或用户明确选择的资源目录 |
| 宿主自发布发现描述文件 | 上述平台默认 `connections/<vault_id>.json` |
| 客户端 `connection.json`、远端 `connections/*.json`、PNG、review／DSL 身份记录 | 本客户端私有 state，status 返回实际位置 |
| 绘图脚本 | `<settings.scriptFolderPath>/Agent-Drawing/` |
| Skill 及相对参考 | Agent 安装的 `obsidian-excalidraw/` 目录 |

克隆／Claude／Codex 未覆盖时使用平台用户数据目录；OMP 使用 `${PLUGIN_DATA}/state`。保留已有 `EXCALIDRAW_AGENT_STATE_DIR`／`EXCALIDRAW_AGENT_CONFIG`，不要误建第二条连接。自发布本机描述文件使不同客户端无需各自 connect；凭据与连接配置必须在 vault／公开包之外，不能写入提示、图、Skill 或公共 MCP 配置。

## 远端独立 CLI 与绘图

Obsidian／Bridge 在 GUI 宿主；Skill、MCP 与独立 CLI 可在无 GUI 远端。图源／素材路径属于宿主，PNG 通过 MCP 返回远端，不需要 X11。远端下载路径不等于宿主附件路径。

在**已连 GUI 宿主**的包目录运行，`drawing-host` 替换为实际 SSH 别名；沿用宿主已有私有 state：

```sh
uv run --frozen python launcher.py remote-deploy --host drawing-host --remote-port 28125
uv run --frozen python launcher.py remote-tunnel --host drawing-host --remote-port 28125
```

隧道命令持续运行，仅绑定 loopback；断线后在宿主重建。部署安装 `~/.local/bin/excalidraw` 包装器，远端可以在**任意目录**直接运行，无须 Agent、MCP 会话或 GUI：

```sh
~/.local/bin/excalidraw status
~/.local/bin/excalidraw status --json
~/.local/bin/excalidraw doctor --json
~/.local/bin/excalidraw vaults
~/.local/bin/excalidraw use "PAIRED_PROFILE_ID_OR_UNIQUE_NAME"
```

远端 profile 保存在远端私有 `state/connections/*.json`。新配对不得覆盖已有不同宿主／vault 的默认目标；部署后需要时运行 `use ID` 明确选择。status 只通过所选 profile 的鉴权 loopback 隧道读宿主实时状态，**不读取远端机器自己的默认目录来冒充 Windows 宿主**。vaults 的注册目录来自所选宿主，不代表每个注册 vault 都能远端执行；尚未运行／配对的 vault 必须在 GUI 宿主完成部署、启动及配对后才可选择。不能传 Windows 路径给远端 connect，也不能在远端 start／reload 宿主。

远端需要 Python 3.11+、pip、SSH；便捷部署同时处理 OMP Skill／MCP 注册并保留其他配置，OMP 不是独立 CLI 的运行前提。其他 Agent 按自己的目录与 stdio 命令注册同一远端运行时，不假设命令会安装 Claude／Codex。更新远端包后重载原有 MCP；正常 status 不重装、不重启任何宿主。

配对通过加密 SCP 将 `0600` 临时 JSON 放入远端 `0700` 事务目录，执行后删除；不在命令参数／日志放 token，不把本机状态文件直接复制进 vault。已安装依赖先离线核对，避免每次配对重新联网。`remote-tunnel` 是前台常驻命令：保留窗口或由用户自己的服务管理器运行；status 不负责悄悄启动它。

## 多 Agent 共用连接

先由协调者配置并启动一次Bridge，Agent分别create/bind不同文件并保存各自contextToken/revision；子Agent不重复connect/start。客户端可并发请求，但Bridge的原生执行/导出共享串行队列；慢任务只阻塞等待，不应串文件。不要共享输出路径或同文件写作权。

同文件竞争使用乐观revision，旧写入返回REVISION_CONFLICT。Bridge0.13.1撤销按文件最近事务隔离，仍有revision与全局20笔历史边界。默认drawing_read给全画布两位小数摘要/世界min-max边界，PNG同时携带同revision的canvasSummary与像素→场景transform。完整约定见SKILL的“多 Agent 并发”和“完整摘要与 PNG 坐标反馈”。

## 更新与卸载

- 克隆安装：关闭本包MCP进程，`git pull`→`uv sync --frozen`→同步已复制Skill→重启客户端MCP。
- OMP：先在使用本包的会话中关闭/断开旧MCP，避免Windows安装缓存被锁，再更新：

```sh
omp plugin marketplace update obsidian-excalidraw-agent
omp plugin upgrade --scope user obsidian-excalidraw-agent-skill@obsidian-excalidraw-agent
```

- 重新connect同一vault更新受管脚本；Engine变更后重启Obsidian。自定义脚本被拒绝覆盖时先备份和解决差异，不force覆盖用户改动。
- 只更新`.excalidrawlib`不需要升级Skill；重新query/get/preview当前库，必要时刷新用户描述/摘要。库文件不上传到Skill仓库。
- 卸载只删除本客户端的Skill/MCP注册和不再需要的安装包；不自动删用户图、素材、私有state或其他绘图脚本。OMP命令：`omp plugin uninstall --scope user obsidian-excalidraw-agent-skill@obsidian-excalidraw-agent`。

## 常见问题

| 现象 | 检查 |
| --- | --- |
| 找到Skill却没有工具 | Skill与MCP是两次配置；核对stdio命令、实际路径、uv/Python及客户端权限 |
| MCP工具出现但未连Obsidian | drawing_setup(status)，检查GUI宿主Bridge、目标vault和私有配置 |
| connected=true但ready=false | 已连服务但无目标画布；显式create或bind |
| 在 Example vault 目录启动却连接旧库 | 浏览目录不等于安装／选库；先 status／vaults，再 use 明确 ID／唯一名称 |
| SELECTION_REQUIRED | 多个候选不能猜，vaults 后按 ID／唯一名称 use |
| BRIDGE_UPDATE_REQUIRED | 在 GUI 宿主部署并运行配套 0.13.8 Start／Bridge，不复制 token |
| 远端目录出现某 vault 但 use 不可选 | 注册不代表已配对；先在 GUI 宿主部署、运行并配对，再远端按 profile ID 选择 |
| configured=true但launched=false/connected=false | 配置与实际服务不同；缺Advanced URI时需用户手动启动，不当作已连接 |
| setup已连接但drawing_context鉴权失败 | 旧进程可能缓存凭据；加载本次客户端修复／reload MCP，检查显式环境覆盖，不扫描历史token |
| Claude/Codex无法读skill:// | 该URI是OMP功能；读取安装目录下对应相对文件 |
| PNG已生成但无法查看 | 核对客户端/模型图片能力，不能记录视觉通过 |
| 更新被Windows EPERM阻止 | 停止占用旧安装包的本包MCP进程后更新；不关闭其他应用/删用户state |

运行时验证先`launcher.py doctor`，固定诊断图用`launcher.py smoke --font "当前已发现的精确family" --filename 唯一测试名`；此命令显式采用已声明的专业诊断风格／medium，仅创建原生图和PNG，不虚构视觉验收。开发回归：`uv run --frozen python -m unittest discover -s runtime/tests -v`。
