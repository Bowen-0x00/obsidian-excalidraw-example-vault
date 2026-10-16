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

## 连接、状态与文件

保持Obsidian运行，目标vault已启用ymjr插件。已注册MCP可调用`drawing_setup`的status/connect/start；没有客户端工具列表时，仓库目录可运行：

```sh
uv run --frozen python launcher.py status
uv run --frozen python launcher.py connect --vault "/actual/vault/path"
uv run --frozen python launcher.py doctor
```

`connect`部署受管脚本到插件`settings.scriptFolderPath`下的`Agent-Drawing/`。文档统一称这个根目录为**绘图脚本目录**（drawing script directory），实际名称由用户配置决定；不重命名磁盘目录、不假设固定路径。自动URI启动需要Advanced URI；否则打开目标画布并手动运行`Agent-Drawing/mcp/Start-Agent-Drawing`。

| 内容 | 存储位置 |
| --- | --- |
| 原生图、用户素材 | 宿主vault或用户明确指定的资源目录 |
| `connection.json`、PNG、review记录 | MCP私有状态目录，`launcher.py status`/drawing_setup返回实际路径 |
| 绘图脚本 | `<settings.scriptFolderPath>/Agent-Drawing/` |
| Skill及相对参考 | Agent安装的`obsidian-excalidraw/`目录 |

不设环境变量时，克隆/Claude/Codex使用平台用户数据目录；OMP插件使用`${PLUGIN_DATA}/state`。需要多个客户端控制同一Bridge时，给它们明确设置**同一个**`EXCALIDRAW_AGENT_STATE_DIR`或`EXCALIDRAW_AGENT_CONFIG`，同时让宿主描述文件指向该连接配置。配置必须在vault和安装包之外；不能无意各自connect轮换宿主凭据。不要把token放在提示、图、Skill或公共MCP配置里。

## 远端绘图

通用拓扑：Obsidian与Bridge在GUI宿主；Skill和MCP客户端可以在远端。原图/源素材属于宿主，PNG通过MCP返回远端，模型无需X11。不能把远端下载路径误当宿主附件路径。

**当前`remote-deploy`便捷命令具体面向OMP**，自动写OMP用户Skill/MCP注册；这不表示远端模式只支持OMP，也不表示它自动安装Claude Code/Codex。其他Agent需要按自己的目录和stdio配置注册同一远端运行时。

已有OMP远端环境时，在已连接的GUI宿主包目录运行（`drawing-host`换成真实SSH别名）：

```sh
uv run --frozen python launcher.py remote-deploy --host drawing-host --remote-port 28125
uv run --frozen python launcher.py remote-tunnel --host drawing-host --remote-port 28125
```

使用与宿主MCP相同的私有状态目录。远端需要Python 3.11+、pip、SSH与OMP；部署保留其模型/其他服务器配置。隧道命令持续运行，只绑定loopback，隔离无关转发/X11。断线后重启；换宿主vault后重新部署并重启远端MCP。remote setup中选vault/启动Bridge必须在GUI宿主完成。

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
| Claude/Codex无法读skill:// | 该URI是OMP功能；读取安装目录下对应相对文件 |
| PNG已生成但无法查看 | 核对客户端/模型图片能力，不能记录视觉通过 |
| 更新被Windows EPERM阻止 | 停止占用旧安装包的本包MCP进程后更新；不关闭其他应用/删用户state |

运行时验证用`launcher.py doctor/smoke`；smoke创建独立画布和PNG但不会虚构视觉检查。开发回归：`uv run --frozen python -m unittest discover -s runtime/tests -v`。
