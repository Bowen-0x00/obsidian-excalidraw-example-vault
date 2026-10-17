# Obsidian-Excalidraw-Eample-Vault

[English](./README.md) | [简体中文](docs/README_ZH.md)

This is a packaged, out-of-the-box Obsidian vault that includes:
- **[Modified Excalidraw Plugin](https://github.com/Bowen-0x00/obsidian-excalidraw-plugin-ymjr)**: Enhanced with native engines, hooks, and REST bridge integration.
- **[Custom Scripts Suite](https://github.com/Bowen-0x00/obsidian-excalidraw-scripts)**: 140+ practical drawing, formatting, and interactive scripts.
- **AI Agent Native Drawing Skill & Bridge**: Out-of-the-box integration with OMP (Oh My Prompt), Claude Desktop, Cursor, and other AI agents for autonomous planning, native symbol insertion, and visual PNG verification.
- **Curated Excalidraw Libraries & Semantic Index**: 40+ vector component libraries (`plugins/Excalidraw/Libraries/`), including a 100% structured digital circuit & microarchitecture library and `library-index.md` catalog for AI semantic retrieval.

Pre-made Excalidraw canvas files are provided to showcase features and components, allowing anyone to **open with Obsidian and experiment immediately without manual setup**.
You can watch this [video](https://www.bilibili.com/video/BV1zN4y1H7Dx/?vd_source=2a4c442f72a74e8d915c1fb5f59d4ba4) to quickly see some of the features: Video.

## Installation and Usage
This is a packaged obsidian vault that includes the modified plugin and many custom scripts. You can directly open it with Obsidian and experience the features.

### Precautions
Please make sure to backup your work to ensure that your important content is not lost (such as saving abnormalities caused by insufficient memory).

For example:

- Use git version control.
- Utilize onedrive for cloud synchronization and version control.
- Enable file recovery plugins in the core plugins.
### Steps to Follow

1. Clone or download the compressed package and extract it.
2. Open Obsidian and select this folder (the folder you cloned or extracted in the previous step).
## AI Agent Out-of-the-Box Drawing

This repository comes pre-configured for end-to-end autonomous AI diagramming:

### 1. Architecture & Components
- **Skill Rules & Reference Docs**: Located in `skills/obsidian-excalidraw`, `.omp/skills/`, and `.claude/skills/`. Provides agents with domain rules for microarchitecture, flowcharts, typography, and library component selection.
- **Agent-Drawing Bridge & Engines**: Located in `plugins/Excalidraw/Scripts/Agent-Drawing/`. Includes `mcp/Start-Agent-Drawing.md`, `mcp/Engine-Agent-Bridge.md`, and 16 native feature engines (Hover, Shadow, Gradient, Swimlane, ECharts, Mindmap, Table, WaveDrom, etc.).
- **Auto-Starting Local Bridge**: When Obsidian opens this vault, the Excalidraw plugin automatically launches `Start-Agent-Drawing.md` and hosts a local loopback REST Bridge on port `27124`.
- **Structured Symbol Libraries**: Stored in `plugins/Excalidraw/Libraries/` with `library-index.md`. AI Agents can read catalog summaries, query exact item IDs (e.g., ALU, MUX, NOR, Register File, NoC Router), and insert them with precise scaling directly onto the canvas.

### 2. How to Use with AI Agents
1. **Open Vault**: Open this folder in Obsidian.
2. **Configure AI Client**:
   - **OMP (Oh My Prompt)**: OMP automatically discovers `.omp/skills/obsidian-excalidraw`. Connect your Excalidraw MCP server and start chatting.
   - **Claude Desktop / Cursor**: Point to `skills/obsidian-excalidraw` as a skill or configure the MCP server.
3. **Draw with Natural Language**:
   Send a prompt to your agent, such as:
   > "Create a CPU datapath diagram using the ALU, MUX, and Register File from the digital circuit library."
   The agent will discover the library, read the index, retrieve exact item IDs, natively insert elements into the canvas, and inspect the rendered PNG to verify layout.


## Automatic Repository Synchronization

Scripts, plugin artifacts and Skill files are synchronized by upstream GitHub `main` push notifications. The receivers are [sync-scripts](.github/workflows/sync-scripts.yml), [sync-plugin](.github/workflows/sync-plugin.yml) and [sync-skill](.github/workflows/sync-skill.yml). Periodic checks are disabled; **Run workflow** remains available for manual catch-up if a notification fails or is missed. Existing synchronization scope and PR/merge behavior are unchanged; this automation does not pull updates into a local vault checkout.

## Porting Features to Your Own vault
Some features require a combination of custom scripts and the modified excalidraw plugin, while others only require custom scripts.

In the README of the [custom scripts](https://github.com/Bowen-0x00/obsidian-excalidraw-scripts), a table is provided listing the scripts required for each feature, but it is not yet complete and is still being written.

If you are unsure about which scripts are needed for a specific feature or how to configure them, you can contact me.

## Feedback, questions, ideas, problems
Feel free to contact me if:

- You have any issues or questions regarding usage.
- You have suggestions or feedback.
- You want to discuss interesting ideas or new features.

Communication channels can be:
- GitHub issues.
- Email.
- Bilibili comments or private messages.
- My personal contact information (WeChat, QQ).


## Say Thank You
If you find the modifications I made helpful to you, feel free to leave comments and messages.

You can also sponsor me a cup of coffee:
- WeChat sponsorship code.
<img src="images/赞助码.jpg" width="200px">
- ko-fi
  <a href='https://ko-fi.com/G2G3SY16R' target='_blank'><img height='36' style='border:0px;height:36px;' src='https://storage.ko-fi.com/cdn/kofi2.png?v=3' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>

## Thanks
Thanks to [zsviczian](https://github.com/zsviczian) and other contributors of [obsidian-excalidraw-plugin](https://github.com/zsviczian/obsidian-excalidraw-plugin).

Thanks to contributors of [excalidraw](https://github.com/excalidraw/excalidraw).