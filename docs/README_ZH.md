# Obsidian-Excalidraw-Eample-Vault
[English](../README.md) | [简体中文](./README_ZH.md)

这是一个打包好的开箱即用 Obsidian 示例库，包含：
- **修改版 Excalidraw 插件**：[obsidian-excalidraw-plugin-ymjr](https://github.com/Bowen-0x00/obsidian-excalidraw-plugin-ymjr)
- **丰富的自定义扩展脚本**：[obsidian-excalidraw-scripts](https://github.com/Bowen-0x00/obsidian-excalidraw-scripts)（含 140+ 常用绘图与交互脚本）
- **AI Agent 原生绘图 Skill & Bridge**：原生接入 OMP (Oh My Prompt)、Claude Desktop、Cursor 等 AI 智能体，支持代码/架构/电路/流程图的自主规划、素材调用、原生绘制与 PNG 视觉闭环。
- **矢量素材库与语义检索摘要**：内置 40+ 套 Excalidraw 矢量素材库，包含 100% 结构化描述的数字电路/微架构硬件图元库与 `library-index.md` 索引摘要。

库中放了现成的 Excalidraw 画布文件展示了一些有趣的功能与微架构图元效果，方便不熟悉插件安装和复杂配置的朋友**直接用 Obsidian 打开即刻体验**。
你可以看这个[视频](https://www.bilibili.com/video/BV1zN4y1H7Dx/?vd_source=2a4c442f72a74e8d915c1fb5f59d4ba4)以快速查看部分功能。

## 安装与使用
这是一个打包好的ob库，包含了修改后的插件和很多自定义脚本。可以直接用obsidian打开然后体验功能。

### 注意事项
请做好备份工作以保证你的重要内容不会丢失（如内存不足导致的保存异常）。

如：
- git版本控制
- onedrive云同步和版本控制
- 核心插件中的文件恢复插件
  
### 使用步骤
1. 克隆或下载压缩包后解压
2. obsidian打开库，选择这个文件夹（上一步克隆或解压后的文件夹）

## AI Agent 绘图：先启动当前库，再自动发现连接

### 1. 在真正运行 Obsidian 的电脑上启动

1. 克隆／解压本仓库，保留 `.obsidian/`，用 **Obsidian Desktop** 打开该文件夹。
2. 启用所带的 **Excalidraw-ymjr**，不是上游同名插件。脚本授权由用户审查决定；本仓库不自动修改授信或 autorun。
3. 打开一个示例画布，在 Excalidraw 脚本命令中运行 **Agent-Drawing/mcp/Start-Agent-Drawing**。

Bridge **0.13.8 及以后**从当前 Obsidian 自动取得本机和 vault 身份，在库外生成该 vault 的私有连接；复制过来的描述文件若指向其他电脑／其他库，会重建为本机连接。不要求安装本机 OMP，不要求用户填写 vault 名和 Windows 路径，也不复制 token 到剪贴板。端口被占用时发布实际可用的 loopback 端口，通知中显示宿主与 vault。

**只打开库不等于自动启动 Bridge。** 所带脚本仍为 `autorun:false`；Advanced URI 只在已安装／启用且明确启动时生效，不是必需依赖。

### 2. 安装 Agent 运行包

Skill 负责绘图规范，运行包提供 `drawing_*` MCP 工具。OMP 用户运行：

```sh
omp plugin marketplace add Bowen-0x00/obsidian-excalidraw-agent-skill
omp plugin install --scope user obsidian-excalidraw-agent-skill@obsidian-excalidraw-agent
```

重载客户端／MCP。只有一个已运行的本地候选时自动发现；存在多个候选时，按返回的连接 ID 或唯一 vault 名选择，不要求手抄路径。**Agent 的工作目录不是绘图目标选择器。**

Claude Code、Codex、克隆安装和 SSH 部署按[运行包接入指南](https://github.com/Bowen-0x00/obsidian-excalidraw-agent-skill/blob/main/skills/obsidian-excalidraw/references/agent-setup.md)操作。Bridge 的 HTTP 地址是内部鉴权协议，不能当 HTTP MCP URL 填入客户端。

### 3. 不用 Agent 也能检查状态

运行包目录可直接运行 `python launcher.py status`、`vaults`、`use 连接ID`、`doctor`；需要结构化输出时加 `--json`。SSH 安装会提供：

```sh
excalidraw status
excalidraw vaults
excalidraw use 连接ID
excalidraw doctor
```

远端显示的是**经鉴权取得的宿主 vault 清单**及已配对连接，不扫描远端文件系统冒充宿主发现，也不要求用户填写 Windows 路径。清单里未启动的库不是可写会话；先在该库的 Obsidian 启动 Bridge。多宿主保留独立记录，新增 DELL 不得悄悄覆盖原宿主的默认连接。

状态分别说明运行包、配置、Bridge 鉴权、实际宿主／库和画布是否就绪。已连接但未开画布，不应误报为鉴权失败。状态命令只读，不改图、不重启 Obsidian。

### 4. 自然语言绘图

> 帮我新建硬件微架构图，使用数字电路库中的 ALU、MUX 和寄存器堆；保留原生可编辑元素，检查最终 PNG。

素材位于 `plugins/Excalidraw/Libraries/`，配有 `library-index.md`。Agent 检索 exact item ID、原生插入、读回、检查 PNG 并取得交付回执；写入成功不等于视觉验收通过。共享 Engines 位于 `plugins/Excalidraw/Scripts/Agent-Drawing/`；表格交互由兼容宿主插件承担，不再启动已退休的脚本 Table Engine。


## 仓库自动同步

Scripts、插件产物及Skill文件由上游GitHub `main` push通知触发同步，接收工作流为[sync-scripts](../.github/workflows/sync-scripts.yml)、[sync-plugin](../.github/workflows/sync-plugin.yml)和[sync-skill](../.github/workflows/sync-skill.yml)。已取消定时检查，保留**Run workflow**手动补发；通知失败或遗漏时需手动补同步。同步范围及既有PR／合并策略不变，也不会自动pull本地vault工作目录。

## 移植功能到自己的库
部分功能是需要自定义脚本和修改后的excalidraw插件搭配使用，而也有部分功能只需要自定义脚本。

在[自定义脚本](https://github.com/Bowen-0x00/obsidian-excalidraw-scripts)的README中做了一张表格，其中列出了每个功能需要的脚本，但是还不完善，还在慢慢写。

你如果不清楚某个功能需要哪些脚本或如何配置，可以联系我。

## 问题、反馈、创意
欢迎联系我，如果：
- 遇到使用问题
- 建议与反馈
- 交流沟通有趣的想法、新的feature

沟通渠道可以是：
- github issue
- 邮件
- B站留言或私信
- 我的个人联系方式 (微信、qq)

## 赞助
如果你觉得我做的这些修改对你有所帮助，欢迎评论、留言。

你也可以赞助我一杯咖啡：
- 微信赞助码 
  <img src="../images/赞助码.jpg" width="200px">
- ko-fi
  <a href='https://ko-fi.com/G2G3SY16R' target='_blank'><img height='36' style='border:0px;height:36px;' src='https://storage.ko-fi.com/cdn/kofi2.png?v=3' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>

## 感谢
感谢[zsviczian](https://github.com/zsviczian)和[obsidian-excalidraw-plugin](https://github.com/zsviczian/obsidian-excalidraw-plugin)的其他贡献者

感谢[excalidraw](https://github.com/excalidraw/excalidraw)的贡献者
