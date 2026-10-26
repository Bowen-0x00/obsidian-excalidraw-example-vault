# 可信宿主脚本、Engine 与交互验证

本参考补足绘图MCP尚未适配的宿主脚本能力；不是新增的任意JS执行工具。普通图元优先MCP，已有Feature优先`set_feature`，确需本地脚本才用URI/已确认的原生CLI。

## 入口和目标

1. 读取当前目标vault、plugin manifest ID及`settings.scriptFolderPath`。绘图脚本目录可经junction共享、名称由用户配置；磁盘目录不证明当前操作哪个vault。
2. 用明确文件绑定画布。脚本正文先验证`ea.targetView.file.path`、`ea.isExcalidrawView`和API ready。不要fallback到active/first；URI中的`filepath`是画布，不是脚本。
3. 当前ymjr ScriptEngine的命令ID为`pluginID:脚本相对scriptFolderPath的路径（去掉.md）`，不是frontmatter.name。确认命令已注册后，编码参数一次：

```javascript
const uri = "obsidian://adv-uri?" + new URLSearchParams({
  vault: "实际vault名或ID",
  filepath: "Agent-Diagrams/明确目标.excalidraw.md",
  commandid: "obsidian-excalidraw-plugin-ymjr:detail/Feature-Detail-Engine"
}).toString();
```

Windows宿主可用`Start-Process '完整URI'`；macOS `open`；Linux GUI宿主`xdg-open`。无GUI远端不能在自己机器上用URI启动宿主Obsidian，应在可访问宿主的会话执行或使用已经连接的MCP。

URI只分发，不等待Action的异步工作。`x-success`/Notice不能当保存或完成回执；读取本轮新回执/实际画布验证，未知写入结果先读回，禁止盲目重发追加脚本。新脚本未注册、画布未挂载、资料不可访问都不能假装成功。常驻脚本的`:stop/:restart`只在真实注册了别名时使用。

## Engine 与面板

- Feature Engine注册EA_Core hooks；Action一般配置元数据、展示面板或调用Engine API。仅有customData不等于交互已经生效。
- 包默认bundle已有hover/shadow/gradient/swimlane/callout/checkbox/code-highlight/echarts/layer/mindmap/text-render/wavedrom/library/embeddable-export/table/特殊箭头点拖拽Engine。其他宿主绘图引擎**没有自动随本包部署/启动**，必须发现真实安装路径并按需挂载，不能凭字段假称已启用。
- 原Engine应作为手动/持久脚本启动；先核对EA_Core hook inventory或真实plugin状态，避免重复注册。不要自动改变autorun、授信配置、startupScriptPath或安装插件。
- Native CLI的一次性`script`会清理请求所属EA及资源，**不能用它启动常驻Engine/动画/面板**。CLI仅用于完全await且无持久hook的单次编辑/导出；`trusted=true`、明确脚本文件和目标，按[native-cli](native-cli.md)核对运行时能力。
- 本包Bridge保留`/v3/scripts/list/run`，但默认`ALLOWED_NAMED_SCRIPTS=[]`，也没有公开任意脚本MCP工具；不要捏造`drawing_run_script`、擅改白名单或用basename消歧同名脚本。
- Action需要UI时：有真实宿主UI控制才操作准确按钮并观察；无UI控制则读取Action核心逻辑，编写用户授权的非交互EA脚本调用同一API/字段。不得启动面板后无限等用户，也不把未来adapter写成现成工具。
- `latex/Action-Extract-Latex.md`是选中text的一次性Action，不是持久Engine或自动text渲染器。其原实现未await删除/末尾提交且会替换ID，不直接当已可靠完成的CLI脚本；选区、暂存副本、group/frame/标签关系恢复与MathJax前提按[visual-content](visual-content.md)执行。无远端脚本工具时用现有text+create_latex组合，不虚构调用。
- `text/Action-Runtime-Font-Manager.md`是宿主可选字体面板，不随本包部署，不适合通过CLI一次性script启动后留悬浮UI。需要动态字体时读[runtime-fonts](runtime-fonts.md)：获准的非交互EA调用复用registerFont等真实方法；系统／网络来源、持久化、同名覆盖与设置改动分别确认，不能把默认checkbox或trusted=true当成用户授权。

## 非交互EA编辑基本约定

使用真实安装脚本的`.md` frontmatter + `/*`/javascript fence opener/`*/`脚本体格式。输入来自已审核的请求文件或Native CLI的`utils.input`，不插值为可执行源码。操作限定实际IDs；先copyViewElementsToEAforEditing，改副本，`await ea.addElementsToView(false,true,...)`，核对返回值、读回并验证保存。`ea.clear()`只清workbench；不清用户view。任务回执最后写入新runId文件，明确部分执行/异常，不宣称原子回滚。

需要第三方扩展代码或网络图片SVG时，用户让你画图不等于允许任意JS/document/gradient运行。JSON图表使用已有受控adapter；安全metadata用`patch_custom_data {target,merge,remove}`。文档中的真实ID占位必须替换为读回/refs映射得到的native ID；对象中的root/parent/ids通常不是可自动解析的logical ref。

## 交互验证不是PNG验证

PNG证明当前静态外观；不能证明hover、Shift点击、detail展开、缩放、导航面板、动画播放或GIF多帧。

交付交互功能必须在真实view上触发：hover移入/移出、checkbox Shift+点击、detail点图标、zoom跨阈值、outline导航、thumbnail点击拖动、动画播放/暂停/停止。记录操作前后元数据/状态和真实截图/录像。只有导出PNG能力时，配置可保存，交互标为“未实测”，不说交互已通过。导出前后的hide/frame/layer状态必须说明；别为了PNG完整永久改掉用户交互状态。

来源：插件`src/shared/Scripts.ts:getScriptName/loadScript/executeScriptFile`；Advanced URI `handlers.handleCommand`；本包Bridge `ALLOWED_NAMED_SCRIPTS/runNamedScript`；各宿主绘图Feature挂载代码。外部：[Advanced URI commands](https://publish.obsidian.md/advanced-uri-doc/Actions/Commands)。
