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

## AI Agent 开箱即用绘图

本仓库已预先配置好面向 AI 智能体的完整闭环绘图能力：

### 1. 架构与组成
- **Skill 规则与参考手册**：放置于 `skills/obsidian-excalidraw`、`.omp/skills/` 与 `.claude/skills/`，向 AI Agent 提供微架构/流程图/布局/字体与素材库选型规则。
- **Agent-Drawing 桥接引擎**：放置于 `plugins/Excalidraw/Scripts/Agent-Drawing/`，包含 `mcp/Start-Agent-Drawing.md`、`mcp/Engine-Agent-Bridge.md` 及 16 个原生特性引擎（Hover、Shadow、Gradient、Swimlane、ECharts、Mindmap、Table、WaveDrom 等）。
- **自启动 Bridge 服务**：Excalidraw 插件启动时会自动运行 `Start-Agent-Drawing.md`，在本地环回端口 `27124` 启动轻量安全的 Bridge 服务，无须手动执行任何命令。
- **结构化素材库**：位于 `plugins/Excalidraw/Libraries/`，配有 `library-index.md` 摘要。AI Agent 可以根据语义先读摘要初筛，再通过关键词 query 精准获取图元（如 ALU、MUX、NOR、寄存器堆、NoC Router 等），并按精确比例原生注入画布。

### 2. 使用方法
1. **打开示例库**：用 Obsidian 打开本仓库文件夹。
2. **配置 AI 客户端**：
   - 若使用 **OMP (Oh My Prompt)**：OMP 会自动识别 `.omp/skills/obsidian-excalidraw`；配置 Excalidraw MCP 服务后即可直接对话。
   - 若使用 **Claude Desktop / Cursor**：将 `skills/obsidian-excalidraw` 挂载为 Skill，或配置 MCP server。
3. **自然语言绘图**：
   在 Agent 对话框中发送指令，例如：
   > “帮我新建一个硬件微架构图，使用数字电路素材库中的 ALU、MUX 和通用寄存器堆，画一个两阶段运算数据通路。”
   Agent 会自动执行：发现库 -> 读取摘要 -> 检索图元 Exact ID -> 原生注入画布 -> 查看渲染 PNG 闭环验证。

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
