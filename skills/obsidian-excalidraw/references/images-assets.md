# 图片获取、插入和资源保留

图片是重要内容类型，不要因原生shape优先就忽略。用户要照片/截图/产品图/图标时，先找合适真实来源，再原生`image`插入；不能画近似矩形代替，也不能把整张架构图栅格化。

## 从网上到画布

1. 按用户语义搜索图片，优先官方/开放授权来源。记录来源网页、直接资源URL、作者/许可（不确定就说明），不是把搜索缩略图当原始资源。不要绕过登录/付费/站点访问限制。
2. 获取实际图片字节，确认HTTP响应、Content-Type、解码尺寸与真实内容；网页HTML/反爬提示不是图片。下载使用Agent已有HTTP/浏览器工具或宿主可信EA `ea.obsidian.requestUrl`，不要在绘图工具不存在下载API时编造调用。
3. 默认保存真实附件到宿主vault可见目录，用唯一文件名或内容hash，避免覆盖现有附件。远端Agent下载的文件不是宿主路径：可通过下面的data:image入口传实际字节，或SSH/SCP/可信宿主`vault.createBinary`保存附件；不能直接把远端绝对路径传给宿主。
4. SVG要检查脚本、事件属性、foreignObject、外部资源，来源不明时优先可信PNG/JPEG/WebP版本；无授权不执行其代码。保留原始来源说明，不把嵌入图片当可修改的矢量子元素。
5. 用真实API插入，保留`fileId`/附件来源。尺寸按自然比例缩放，考虑布局边距；明确裁剪用户所需内容，不默认拉伸。
6. 读回image元素/资源就绪，保存后再导出PNG并实际看图；背景透明、EXIF旋转、远端解码、丢资源都可能导致画面与预期不同。

## 三种真实入口

### 绘图MCP

已有Bridge操作，不是新增tool：

```json
{"op":"create_image","ref":"logo","x":40,"y":60,"source":"https://实际直接图片URL","scale":true,"anchor":false,"width":240,"height":160,"customData":{"assetSource":{"page":"实际来源网页","credit":"实际作者/许可"}}}
```

`source`由`ea.addImage`解析，支持真实直接URL、插件支持的引用及data:image；`scale`是布尔的插件尺寸缩放开关，不是数值倍率。width/height必须一起按比例计算；不确定自然尺寸就先插入并read后等比例resize。URI/dataURL直接插入可能保持外部链接/嵌入数据，不代表已生成稳定本地附件。默认附件策略用下面的EA TFile路径，再回到MCP重新bind/read做PNG闭环。

### 远端已有PNG：通过MCP传字节，不传远端路径

没有独立`upload(local_path)`工具；已有`create_image.source`接受data URL。在已连接的远端执行器中读取用户指定PNG，经程序编码再调用现有MCP或DrawingClient；不要把长base64打印给模型手抄。下面是已取得真实`client/token/revision/png_path`后的核心片段，width/height先按自然比例和目标内容区计算：

```python
import base64
source = "data:image/png;base64," + base64.b64encode(png_path.read_bytes()).decode("ascii")
result = client.apply(token, revision, [{
    "op": "create_image", "ref": "photo", "x": x, "y": y,
    "source": source, "scale": False, "anchor": False,
    "width": width, "height": height
}])
```

Bridge当前JSON请求体上限4MiB，base64约膨胀为4/3，须把本次**全部**图片、文本及操作字段一起计入；不是每张PNG可用4MiB。多图可分批保留revision，单图超限先按展示需求合理缩小/压缩，或走宿主附件路径；不无限重试、不临时公开用户图片。`create_image.scale`是布尔，`drawing_library.scale`与选区factor才是数值倍率。

本轮真实Redhat 0.8.6 → 宿主ymjr/Bridge 0.13.2验证：两个远端PNG通过stdio MCP组合为1 frame、2 image、7原生text；宿主保存成两个附件，字节SHA256与远端原件一致，最终PNG实际查看、check=pass、review完成。不同宿主版本仍须读回fileId、保存后的Embedded Files/附件和PNG，不根据缺省status字段断言资源失败。

页面可同时包含多张独立image与原生文字；图片内部像素不变成可编辑矢量。先适配页面底板再排图文，参见[尺寸适配](layout-export-animation.md)。这里只生成Excalidraw演示页，不声称生成PPTX。

### 可信宿主EA脚本：先保存附件再插入

读取[script-execution](script-execution.md)绑定明确view和运行授权；下面是核心API片段，不是自动执行任务：

```javascript
const response = await ea.obsidian.requestUrl({url: input.url});
if (response.status !== 200 || !response.headers["content-type"]?.startsWith("image/")) {
  throw new Error("Expected a real image response");
}
// input.asset是审核后的vault相对新路径；父目录先按vault API创建，不覆盖已有文件。
if (await ea.plugin.app.vault.adapter.exists(input.asset)) throw new Error("Attachment exists");
const file = await ea.plugin.app.vault.createBinary(input.asset, response.arrayBuffer);
const id = await ea.addImage(input.x, input.y, file, true, false);
if (!id) throw new Error("Image decoding/insertion failed");
if (!await ea.addElementsToView(false, true)) throw new Error("Image scene commit failed");
```

requestUrl参数来自可信数据，不是任意JS。保存前应检查字节/解码与SVG安全；片段没有代替这些检查。TFile与字符串语义不同：`addImage(...,file)`保存插件附件引用；URL字符串是链接，dataURL可嵌入。`fileId/imagesDict/EmbeddedFile`由EA管理，不手填base64或invent ID。别对未经确认的外网URL自动补Bearer/cookie或发送用户文件。

### 插件原生CLI

已安装Native CLI并通过status/schema确认时：`apply.operations:[{"op":"image","asset":"Attachments/真实文件.png","x":40,"y":60,"scale":true}]`。asset是**宿主vault**准确路径，不是互联网URL/本机绝对路径。持久化与requestId按[native-cli](native-cli.md)；导出之后真看PNG。

## GIF、公式和Markdown图片

GIF单张PNG只能显示一帧，多帧控制见[special-diagrams](special-diagrams.md)。LaTeX是含源公式的image资源，不拿普通文字或截图假装公式；先确认Extras MathJax。**普通text中的`$…$`不会自动渲染**，文字混排按[visual-content](visual-content.md)复用`latex/Action-Extract-Latex.md`或现有text+create_latex组合，转换后检查源TeX、分组/frame/绑定和PNG。Markdown/PDF/SVG链接可能触发插件专用loader和远端访问，先读真实API/资源条件，不能把页面占位当正文。插入图片不会天然生成点击导航/hover，按需另设原生link或已确认的交互metadata。

来源：插件`ExcalidrawAutomate.addImage`/`EmbeddedFilesLoader`、本包Bridge`createImage`与Native CLI`image`操作；网络获取是Agent或可信宿主HTTP能力，不是独立的绘图下载引擎。
