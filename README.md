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
## AI Agent drawing: one host, one discovered connection

### 1. Start in the actual Obsidian vault

1. Clone/download this repository, including `.obsidian/`, and open the folder as a vault in **Obsidian Desktop**.
2. Enable the bundled **Excalidraw-ymjr** plugin, not the upstream Excalidraw plugin. Review and approve script execution yourself; this repository does not grant trust or enable autorun.
3. Open an example drawing. Run **Agent-Drawing/mcp/Start-Agent-Drawing** using Excalidraw's script command.

Bridge **0.13.8+** derives the current vault and machine from Obsidian, creates a private per-vault connection outside the vault, and repairs a copied descriptor that references another computer or vault. Credentials are never copied to the clipboard or committed. If a port is occupied, the Bridge publishes its actual loopback port. A startup notice identifies the host and vault.

**Opening the vault alone does not promise an automatically started Bridge.** The supplied startup script is `autorun:false`. Advanced URI may start an explicitly configured vault when installed/enabled, but it is optional.

### 2. Install the Agent runtime once

The Skill explains how to draw; the separate runtime supplies `drawing_*` MCP tools. For OMP:

```sh
omp plugin marketplace add Bowen-0x00/obsidian-excalidraw-agent-skill
omp plugin install --scope user obsidian-excalidraw-agent-skill@obsidian-excalidraw-agent
```

Reload the client/MCP. A single live local connection is discovered automatically; if there is more than one, select a returned connection ID or unique vault name. The Agent working directory is not a vault selector.

For Claude Code, Codex, a repository install, and SSH deployment, use the [runtime setup guide](https://github.com/Bowen-0x00/obsidian-excalidraw-agent-skill/blob/main/skills/obsidian-excalidraw/references/agent-setup.md). Do not configure the internal Bridge URL as an HTTP MCP endpoint.

### 3. Check without asking an Agent

In the installed runtime directory use `python launcher.py status`, `vaults`, `use CONNECTION_ID`, or `doctor`; add `--json` for machine-readable output. SSH installations provide:

```sh
excalidraw status
excalidraw vaults
excalidraw use CONNECTION_ID
excalidraw doctor
```

The remote client lists **authenticated host vaults** and paired connections; it never needs a user to transcribe a Windows vault path. A listed but unstarted host vault is not a writable session. Start its Bridge in Obsidian first. Multiple hosts remain separate profiles; adding DELL must not silently replace an existing host.

The status distinguishes installed runtime, configuration, authenticated Bridge, observed host/vault and open canvas. `connected` with no open canvas is not an authentication failure. Status does not edit a drawing or restart Obsidian.

### 4. Ask for a drawing

> Create a CPU datapath using the ALU, MUX and Register File from the digital circuit library. Keep native editable elements and inspect the resulting PNG.

The library lives under `plugins/Excalidraw/Libraries/` with `library-index.md`. The Agent selects exact item IDs, edits native elements, checks the current PNG and reports a delivery receipt—not merely a successful write. Shared Engines are bundled under `plugins/Excalidraw/Scripts/Agent-Drawing/`; table interaction belongs to a compatible host plugin, not the retired script Table Engine.


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