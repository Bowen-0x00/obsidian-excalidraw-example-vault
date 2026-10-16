---
name: Start Agent Drawing
description: Bootstrap script to initialize Excalidraw Agent engines and bridge.
author: local
version: 0.13.3
autorun: false
---
/*
```javascript
*/

const BOOTSTRAP_VERSION = "0.13.3";

const obsidianApp =
  ea.plugin?.app || (typeof app !== "undefined" ? app : null);
const scriptEngine = ea.plugin?.scriptEngine;
const { Notice } = ea.obsidian || {};

if (!obsidianApp || !scriptEngine) {
  const msg = "Excalidraw ScriptEngine or Obsidian App is unavailable.";
  if (Notice) new Notice(`[Start-Agent-Drawing] ${msg}`, 8000);
  throw new Error(msg);
}

if (typeof window.EA_Core?.registerHook !== "function") {
  throw new Error("Excalidraw-ymjr EA_Core is unavailable. Enable a compatible plugin before starting Agent Drawing.");
}

// 1. Derive bundle root directory from utils.scriptFile.path
let bundleRoot = null;
if (utils?.scriptFile?.path) {
  // utils.scriptFile.path: e.g. "plugins/Excalidraw/Scripts2/Agent-Drawing/mcp/Start-Agent-Drawing.md"
  const mcpDir = utils.scriptFile.path.substring(
    0,
    utils.scriptFile.path.lastIndexOf("/"),
  );
  bundleRoot = mcpDir.substring(0, mcpDir.lastIndexOf("/"));
}

if (!bundleRoot) {
  const configuredFolder = String(
    ea.plugin?.settings?.scriptFolderPath || "plugins/Excalidraw/Scripts2",
  ).replace(/\/+$/, "");
  bundleRoot = `${configuredFolder}/Agent-Drawing`;
}

// 2. Validate bundle root contains bridge
const bridgeRel = "mcp/Engine-Agent-Bridge.md";
const bridgeFile = obsidianApp.vault.getFileByPath(`${bundleRoot}/${bridgeRel}`);
if (!bridgeFile) {
  const msg = `[Start-Agent-Drawing] Bridge script not found at ${bundleRoot}/${bridgeRel}. Check bundle deployment.`;
  if (Notice) new Notice(msg, 8000);
  throw new Error(msg);
}

// 3. Define bundled feature engines in strict dependency order
const ENGINES = [
  {
    id: "hover",
    name: "Hover Interaction Engine",
    path: "hover/Feature-Hover-Engine.md",
    scriptId: "ymjr.feature.hover-engine",
    properties: ["_ymjr_HoverState"],
  },
  {
    id: "shadow",
    name: "Shadow Visual Engine",
    path: "shadow/Feature-Shadow-Engine.md",
    scriptId: "ymjr.feature.shadow-engine",
    properties: ["_ymjr_shadow", "_ymjr_shadow_engine"],
  },
  {
    id: "gradient",
    name: "Gradient Rendering Engine",
    path: "gradient/Feature-Gradient-Engine.md",
    scriptId: "ymjr.feature.gradient-engine",
    properties: ["_ymjr_gradient", "_ymjr_gradient_engine"],
  },
  {
    id: "swimlane",
    name: "Swimlane Container Engine",
    path: "swimlane/Feature-Swimlane-Engine.md",
    scriptId: "ymjr.feature.swimlane-engine",
    properties: ["_ymjr_swimlane", "_ymjr_swimlane_engine"],
  },
  {
    id: "callout",
    name: "Callout Annotation Engine",
    path: "callout/Feature-Callout-Engine.md",
    scriptId: "ymjr.feature.callout-engine",
    properties: ["_ymjr_callout", "_ymjr_callout_engine"],
  },
  {
    id: "checkbox",
    name: "Checkbox Interactive Engine",
    path: "checkbox/Feature-Checkbox-Engine.md",
    scriptId: "ymjr.feature.checkbox-engine",
    properties: ["_ymjr_checkbox", "_ymjr_checkbox_state", "_ymjr_checkbox_engine"],
  },
  {
    id: "code_highlight",
    name: "Code Highlight Engine",
    path: "code-highlight/Feature-Code-Highlight-Engine.md",
    scriptId: "ymjr.feature.codehighlight",
    properties: ["_ymjr_code_highlight", "_ymjr_codeHighlight", "_ymjr_code_highlight_engine", "_ymjr_codeMap"],
  },
  {
    id: "echarts",
    name: "Apache ECharts Diagram Engine",
    path: "echarts/Feature-Echarts-Engine.md",
    scriptId: "ymjr.feature.echarts-engine",
    properties: ["_ymjr_echarts", "_ymjr_echarts_engine"],
  },
  {
    id: "layer",
    name: "Layer Management Engine",
    path: "layer/Feature-Layer-Engine.md",
    scriptId: "ymjr.feature.layer-engine",
    properties: ["_ymjr_layer_engine", "_ymjr_layer"],
  },
  {
    id: "mindmap",
    name: "Mindmap Diagram Engine",
    path: "mindmap/Feature-Mindmap-Engine.md",
    scriptId: "ymjr.feature.mindmap-engine",
    properties: ["_ymjr_mindmap", "_ymjr_mindmap_engine", "MindmapAPI"],
  },
  {
    id: "text_render",
    name: "Rich Text Rendering Engine",
    path: "text/Feature-Text-Render-Engine.md",
    scriptId: "ymjr.feature.text-render-engine",
    properties: ["_ymjr_text_render", "_ymjr_textRender", "_ymjr_text_render_engine"],
  },
  {
    id: "wavedrom",
    name: "WaveDrom Timing Diagram Engine",
    path: "wave-drom/Feature-Wavedrom-Engine.md",
    scriptId: "ymjr.feature.wavedrom-engine",
    properties: ["_ymjr_wavedrom", "_ymjr_wavedrom_engine", "WaveDrom"],
  },
  {
    id: "library",
    name: "Library Engine & Image Hydration",
    path: "library/Feature-Library-Engine.md",
    scriptId: "ymjr.feature.library-engine",
    properties: ["_ymjr_customLibraryImageCache"],
  },
  {
    id: "export_embeddable",
    name: "Embeddable SVG Export Engine",
    path: "export/Feature-Export-Embeddable.md",
    scriptId: "ymjr.feature.export-embeddable-svg",
    properties: ["_ymjr_mdCacheMap", "html2canvas"],
  },
  {
    id: "arrow_head_resize",
    name: "Arrowhead Resizer Engine",
    path: "arrow/Feature-Arrow-Head-Resize-Engine.md",
    scriptId: "ymjr.feature.arrowhead-resize-engine",
    properties: [],
  },
];

// Helper to check if an engine is already registered in the runtime
function isEngineAlreadyRegistered(engineDef) {
  const plugin = ea.plugin || window.ExcalidrawAutomate?.plugin;

  // 1. Check disable function on plugin
  if (engineDef.scriptId && typeof plugin?.[`disable_${engineDef.scriptId}`] === "function") {
    return true;
  }

  // Use the public hook inventory, not library globals that may exist without hooks.
  const hooks = window.EA_Core?.listHooks?.() || {};
  if (Object.values(hooks).some((list) => list.some((hook) => hook.id === engineDef.scriptId))) {
    return true;
  }

  return false;
}

// 4. Resolve active target view if available
let targetView;
try {
  ea.setView("active");
  if (ea.targetView && ea.isExcalidrawView(ea.targetView)) {
    targetView = ea.targetView;
  }
} catch {
  targetView = undefined;
}

// 5. Execute bundled engines sequentially in dependency order
let registeredCount = 0;
let skippedCount = 0;

for (const engine of ENGINES) {
  if (isEngineAlreadyRegistered(engine)) {
    console.log(`[Start-Agent-Drawing] Engine ${engine.name} already active; skipping.`);
    skippedCount++;
    continue;
  }

  const enginePath = `${bundleRoot}/${engine.path}`;
  const engineFile = obsidianApp.vault.getFileByPath(enginePath);
  if (!engineFile) {
    const msg = `[Start-Agent-Drawing] Required engine file missing: ${enginePath}`;
    if (Notice) new Notice(msg, 8000);
    throw new Error(msg);
  }

  const rawSource = await obsidianApp.vault.adapter.read(engineFile.path);
  const scriptName =
    scriptEngine.getScriptName?.(engineFile) ||
    engineFile.path.replace(/\.md$/, "");

  try {
    await scriptEngine.executeScript(
      targetView,
      rawSource,
      scriptName,
      engineFile,
    );
    if (!isEngineAlreadyRegistered(engine)) {
      throw new Error(`Engine did not register its native hooks: ${engine.path}`);
    }
    registeredCount++;
    console.log(`[Start-Agent-Drawing] Mounted engine: ${engine.name} (${engine.scriptId})`);
  } catch (err) {
    const msg = `[Start-Agent-Drawing] Failed to execute engine ${engine.name}: ${err?.message || err}`;
    console.error(msg, err);
    if (Notice) new Notice(msg, 8000);
    throw new Error(msg);
  }
}

// 6. Finally, execute Bridge
const bridgeSource = await obsidianApp.vault.adapter.read(bridgeFile.path);
const bridgeScriptName =
  scriptEngine.getScriptName?.(bridgeFile) ||
  bridgeFile.path.replace(/\.md$/, "");

try {
  await scriptEngine.executeScript(
    targetView,
    bridgeSource,
    bridgeScriptName,
    bridgeFile,
  );
  const server = window.__EXCALIDRAW_AGENT_BRIDGE__?.server;
  if (!server) throw new Error("Bridge execution returned without a server.");
  if (!server.listening) {
    await new Promise((resolve, reject) => {
      const timer = setTimeout(() => reject(new Error("Bridge did not listen within 5 seconds.")), 5000);
      server.once("listening", () => { clearTimeout(timer); resolve(); });
      server.once("error", (error) => { clearTimeout(timer); reject(error); });
    });
  }
  console.log(`[Start-Agent-Drawing] Bridge started: ${bridgeScriptName}`);
} catch (err) {
  const msg = `[Start-Agent-Drawing] Failed to start Bridge: ${err?.message || err}`;
  console.error(msg, err);
  if (Notice) new Notice(msg, 8000);
  throw new Error(msg);
}

const summary = `Excalidraw Agent ready (${registeredCount} engines registered, ${skippedCount} existing, bridge running).`;
console.log(`[Start-Agent-Drawing] ${summary}`);
if (Notice) new Notice(summary, 5000);
