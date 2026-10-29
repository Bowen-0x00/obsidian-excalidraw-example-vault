# 原生矢量图标：svgLayers、动态样式与本地图标库

图标适合表达实体身份、服务类别、工具／品牌或简短操作，不应代替节点标签、关系、端口和机制。先找用户现有图标库；有真实矢量图标时不要用emoji、近似矩形或整图PNG替代。新增支持复用当前原生元素和执行入口，**不是一个新的图标MCP或通用SVG无损转换器**。

只读清单先返回路径、名称／分类、源hash、viewBox和图层数，候选确定后再读d全文；不要把整个SVG目录一次塞进上下文。当前Bridge请求体预算仍为4MiB，图层、路径、文字及其他操作合计计入，不是每个icon各有4MiB。

## 1. 三类资源不能混用

| 类型 | 原生存储／编辑边界 | 推荐入口 |
| --- | --- | --- |
| `.excalidrawlib` item | 一组原生元素与资源；按exact item ID选择 | `drawing_library(list/query/get/preview/insert)`，见[library-catalog](library-catalog.md) |
| 本地SVG图标 → `svgLayers` | 一个原生rectangle承载有序path图层及源viewBox；可改整体style与图层数据，不是逐层的独立Excalidraw节点 | 审查／转换后用现有`drawing_apply create_shape`＋customData，或可信EA `addRect` |
| SVG／PNG作为image附件 | image＋fileId／附件；可改尺寸，内部stroke/fill不随元素调色板变成可编辑path | 保真优先且转换不支持时用[images-assets](images-assets.md)，明确编辑边界 |

旧`svgPathShape`是单路径line组件，见[svg-components](svg-components.md)。新`svgLayers`保留多色／多path和非零viewBox原点，优先使用矩形carrier；不要为了套旧`create_svg_path`把所有图层合并、平移或改成单色。旧单path操作的“bbox必须归零并精确等于viewBox”限制**不应套到svgLayers图标**，源viewBox可以有设计留白。

## 2. 真实前提与能力发现

源码依据：组件`95ca0df452d8411efa7d57347d8bf5551cf814af`（shape/cache/bounds/canvas/SVG导出），插件`e364fd16`（2.29.0-9及SVGLayer类型），脚本`4cb786f`的`icon/Action-Icon-Library.md`（读到1.0.0）。当前运行宿主必须实际包含这个组件；只更新Skill／MCP不会升级插件。

当前Bridge的`svg_path_shape`发现仍指旧单path，不是新图层渲染认证。**先检查实际宿主版本／配套组件证据，再在独立小样验证多层渲染与动态样式。** 旧宿主可能把carrier画成普通矩形，不能把metadata写入成功说成图标可用。

已有工具可传递安全JSON customData与style，无需新增operation。没有独立`drawing_icons`、`kind:"icon"`、SVG文件自动query/insert或通用转换MCP；不虚构这些调用。`drawing_library`只按其真实库协议工作，普通SVG文件夹不自动成为`.excalidrawlib`。

## 3. 发现与选择本地图标

1. 核对目标vault、`settings.scriptFolderPath`及已安装的`icon/Action-Icon-Library.md`。图标库根目录来自该脚本`getScriptSettings()`的`icon_library_folder`（值可能为字符串或`{value,...}`）；**缺省`Icons`不是已确认的实际用户目录**。Action初次打开可能写默认设置，不当作纯查询。
2. 读取已确认目录内的SVG清单；第一层子目录用作分类，准确记录源文件路径及内容hash。同名图标靠完整路径消歧，不只看basename。Logos／Tech／Cloud／General是本次样本分类，不是所有安装的固定目录。
3. 用需求筛少量候选，实际查看源SVG／PNG预览；品牌图标默认保留原色，通用单色图标可适配图中角色色。不要仅因有Docker图标就把普通容器节点改成Docker语义。
4. 解析前审查来源和许可。脚本MIT不自动为每个品牌标志赋予MIT或商标授权；不把用户私有图标复制进Skill或公共包。
5. 目标内容区先定尺寸与留白；默认等比例fit：factor=min(availableWidth/viewBox.width, availableHeight/viewBox.height)。不要照搬Action的48px或正方形size，使非方图标拉伸。布局位置是显式世界坐标，不采用UI滚动中心当永久源坐标。

远端Agent读取的是宿主资源；服务器上的同名路径不是宿主文件。可以用已有授权文件访问或可信EA返回小型有序图层数据；没有宿主文件读取通道时报告缺入口，不自动下载网上替代物，不扩大脚本白名单。

## 4. SVG转换范围：渲染更强，不等于解析器什么都懂

当前Action的`SVGIconParser.parse/extractStyle`是受限正则提取器：提取path、circle、rect、polygon，处理每个标签上的fill/stroke/stroke-width及部分inline style。**以下不能默认保留**：

- 根／group的继承样式、CSS/class、currentColor的完整级联；nested transform／use／defs。
- path/circle/rect等混排的文档绘制顺序：原解析器按类型批量收集，可能重排覆盖关系。
- rect的rx/ry、ellipse、line/polyline、text、image、clipPath/mask、gradient/filter及animation。
- fill-rule/evenodd、stroke-linecap/linejoin／dash、group opacity等；SVGLayer类型列出opacity不表示当前renderer已消费它。
- viewBox正则并非完整数字／单位语法；科学计数法、百分比尺寸、异常／空文档不能靠默认24×24假装解析成功。

先检查源中是否存在这些特征。简单样本可复用已核对的有限提取方法；需要一般SVG时用真实DOM／成熟解析与路径变换工具保留继承、transform与顺序，**不能把正则升级宣传为通用parser**。只把已展开且renderer可表达的path和style交给svgLayers；无法表达的效果说明差异、询问是否接受简化，或保留为image。不能静默丢掉文字／圆角／剪裁仍称忠实矢量导入。

SVG审查先于任何预览或DOM挂载：拒绝script、on*事件、foreignObject、外链资源与url(...) paint、未知可执行内容。路径字符串只是d数据，不接受整份SVG XML。网络下载／素材安装、写库或修改图标目录设置不是普通画图授权自动包含的副作用；见[脚本边界](script-execution.md)和[资源安全](images-assets.md)。

## 5. 原生数据与真实调用

当前插件类型：

```typescript
// 这是customData结构，不是新增工具schema。
type SVGLayer = {
  d: string;
  fill?: string;
  stroke?: string;
  strokeWidth?: number;
  fillStyle?: "solid" | "hachure" | "cross-hatch" | "dots" | "zigzag";
  roughness?: number;
  opacity?: number;
};
// svgViewBox: {x?:number,y?:number,width:number,height:number}
```

必须保持图层数组顺序、正的viewBox宽高、有限数值和源d。`scaleX/scaleY`用于源坐标翻转，常规用1／-1；元素width/height是目标显示尺寸。坐标转换为`(source-viewBoxOrigin)*target/viewBoxSize`，非零原点无需破坏源路径去强行归零。

以下是完整可执行的**合成双色矢量小样**操作，非品牌图标、非用户库事实。应用到已绑定、已获准的测试画布，用返回refs取得真实ID：

```json
{
  "op":"create_shape","ref":"vector-icon","type":"rectangle",
  "x":80,"y":100,"width":96,"height":96,
  "style":{
    "strokeColor":"transparent","backgroundColor":"transparent",
    "strokeWidth":1,"fillStyle":"solid","roughness":0,"roundness":null
  },
  "customData":{
    "svgLayers":[
      {"d":"M2 2H22V22H2Z","fill":"#3b82f6","stroke":"none","strokeWidth":1},
      {"d":"M6 6H18V18H6Z","fill":"#fbbf24","stroke":"none","strokeWidth":1}
    ],
    "svgViewBox":{"x":0,"y":0,"width":24,"height":24},
    "scaleX":1,"scaleY":1,
    "agentDiagram":{"logicalId":"vector-icon","role":"icon"}
  }
}
```

真实图标替换成审查后的有序layers／源viewBox，并用安全metadata记录源路径/hash；不手填原生ID／version／versionNonce／index。新建icon载体不带普通节点label；需要说明则单独原生text并group，避免文字压在图标中央。矩形carrier可作为实际绑定目标，连接的是整个图标bbox，不是内部path孔洞／端口；真正硬件网络仍需部件／端口契约。

改整体样式：

```json
{"op":"patch_element","target":"实际iconID","patch":{"strokeColor":"#0f766e","backgroundColor":"#d1fae5","strokeWidth":2,"roughness":0}}
```

恢复源多色模式：把strokeColor、backgroundColor都改回`transparent`，strokeWidth回到约定基准1；原svgLayers不变。需要只改某个图层时，先读完整当前数组，再以`patch_custom_data {target, merge:{svgLayers:完整新数组}}`替换；不要假设数组merge会按索引保留未返回成员。carrier不重建，源图标文件不自动改写。

可信EA复用Action核心：`addRect`→取得element→设置上述style/customData→`await addElementsToView(false,true,true)`→精确读回。**原Action未await末尾提交**，其Notice／弹窗关闭不能当可靠保存回执；不直接开面板等待用户来冒充Agent插入完成。

## 6. 动态样式的优先级与容易误解的行为

| 属性／模式 | 当前renderer行为 | 使用建议 |
| --- | --- | --- |
| stroke/bg都transparent | 保留各layer的原fill/stroke；未定义stroke时无描边 | 多色Logo原色模式，不是图标不可见 |
| 非透明strokeColor | 覆盖layer描边；对单色、fill-only图层还将fill改为strokeColor；也可能给原本填充图层加轮廓 | 单色整体改色有用；多色标志不自动统一填充，谨慎加轮廓 |
| 非透明backgroundColor | 对图层统一应用填充，**包括原fill=none图层** | 会改变轮廓／孔洞外观，不是carrier背后的底板；底板另建独立rectangle |
| strokeWidth | 有原stroke时通常为layer.strokeWidth×元素strokeWidth；新加轮廓可能直接用元素宽度 | 保留源宽度与整体倍率概念；0在当前实现被`||1`当1，不用0作隐藏描边开关 |
| fillStyle / roughness | 元素级值通常优先于层级值；sharp用roughness0，rough可按用户偏好 | 不承诺为每个图层独立切换同样效果 |
| opacity | 使用元素整体opacity；layer.opacity虽有类型声明，当前主分支未应用 | 不声称保留逐层透明度；需要时另行转换／披露 |

`currentColor`在当前Action中算一个颜色token，不是执行完整SVG/CSS级联。轮廓图标应给carrier明确非透明strokeColor；多色分类由不同fill/stroke token数决定，不是Agent认定的艺术分类。

源路径缩放与stroke宽度不是同一计算：当前实现缩放Rough path坐标，不能假设显示尺寸翻倍就自动把描边翻倍；改变尺寸后按目标用途检查线宽。暗色主题经过宿主dark-mode filter；品牌精确颜色需实际查看主题下的PNG，不能只看输入hex。

## 7. 保存、缓存、检查与增量修改

- svgLayers序列化在元素customData里。无外部image/fileId时，源SVG文件是来源依据，已插入图标不应被宣传成实时链接原文件；源库改了不会自动更新画布。保存后重开要检查layers、viewBox、style和native ID。
- 新组件ShapeCache用versionNonce识别style变化；**通过当前原生mutation API／Bridge patch操作触发更新，不手动随机nonce、直接改live对象或清全缓存掩盖问题**。保存属性不变但PNG不刷新时记录差异，用正常读回／预览／具体诊断处理。
- 当前Bridge摘要／feature发现并不完整识别svgLayers；可按ID完整read，核对层数、源色、viewBox、尺寸、原生type与style。不要凭“摘要没有svgLayers标记”认定丢失。
- 通用几何检查主要按carrier bbox和文本关系，不证明path可见性、孔洞／clip、图标识别或品牌忠实；透明元素style也不表示多色layer不可见。实际PNG必须检查。
- 验证至少覆盖：多色原色保留、单色stroke换色、bg填充覆盖、strokeWidth改变、同ID局部更新、源数据与无关元素保留、保存重开、完整PNG及必要细节；有SVG导出需求再独立验SVG，不拿PNG替代所有输出证据。
- 错误只修受影响ID／源转换，保留用户未要求改的其他对象、布局与样式。未支持的SVG特性或旧宿主应明确报差距，不能删图层或改成图片后仍说原生多色样式通过。

本地实测（2026-10-29，授权升级的演示库2.29.0-9）：用4个实际SVG源样本及合成viewBox样本创建8个rectangle图标，共28个原生元素、0个image。Google/Python原色、Heart描边／填充／线宽、单色Star跟随描边色、非零原点、同ID改色恢复均通过真实PNG和读回；改两个目标时其余26元素完全不变。隔离scratch经原生mutateElement后nonce变化，旧缓存被拒绝且新shape样式正确；真实保存关闭重开保留ID／源层／几何／style，PNG哈希一致。SVG导出已查看图标层；PNG检查零问题、High review及delivery通过。未实测任意SVG转换、图标面板交互、暗色主题或所有逐层效果；SVG文本字体在独立查看器中的可移植性不由图标层测试证明。

## 8. 选用策略

“云架构需要数据库图标”：先选准确本地图标，按服务节点内容区fit，标签仍独立；不把图标当数据库模型。

“把这三个单色图标统一为主题色”：保留源layers与ID，按实际单／多色判断只改carrier style；不要同时改品牌多色Logo。

“保持品牌色，但把线加粗”：说明多色fill与新描边的不同作用，小样看图确认，不假设strokeColor会替换所有fill。

无需为了展示能力给每个节点加icon。只有能降低识别成本、帮助层级或满足用户指定时使用；图标库只是语义和视觉资源，不替代本次图形表达与验收计划。
