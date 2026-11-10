# 原生表格：主题、边框模板与稳定语义

优先使用宿主自己的 `TableManager`，不要逐格模拟表头色、条纹、三线表或阴影。本包提供 **`drawing_table(create|style)`**，Python 对应 `DrawingClient.table(...)`；不是把新字段偷偷塞进旧 `create_table`。

## 先发现真实宿主能力

`drawing_context(action="discover")` 的 `capabilities.nativeTable` 包含 `callable`、`schemaVersion:2`、`themes`、`borders` 和 endpoint。只有 `callable:true` 才使用新接口。

配套原生表格／外观构建目前是开发检查点，**不是本包安装后自动具备的公开宿主插件能力**。本轮在隔离测试库实际运行并导出；未替换日用 vault 的插件。旧宿主调用新接口返回 `TABLE_RUNTIME_REQUIRED`，不伪造主题效果。旧 `drawing_apply(create_table)` 和 DSL 表格保持原有契约；不会自动获得新主题。

## 已确认的目录

主题 ID：`light-blue`、`light-mint`、`dark-slate`、`dark-ink`、`morandi-sage`、`morandi-rose`、`academic`、`sketch`。

边框 ID：`grid`、`framed`、`dashed`、`three-line`、`none`。主题和边框可组合。实际颜色、逐边绘制、条纹与原生表格纸张阴影均由宿主实现；Agent 不复制色板或额外画线。新目录项仍需相应 Bridge 版本支持，不凭菜单截图猜接口 ID。

## 创建与修改

```json
{
  "context_token":"绑定目标得到的token",
  "base_revision":"最新read得到的revision",
  "action":"create",
  "ref":"results",
  "theme":"academic",
  "border":"three-line",
  "options":{
    "x":80,"y":220,"rows":3,"cols":3,
    "cellWidth":180,"cellHeight":64,
    "columnWidths":[260,180,180],
    "cells":[["Treatment","Moisture (%)","Biomass (g)"],["Control","18.2","42.0"],["Mulch","23.6","47.8"]],
    "style":{"fontFamily":"实际发现的family","fontSize":20}
  }
}
```

`options.cells` 必须是对应行列数的字符串矩阵。每格最小宽40、高32；一个请求最多500格。先按实际字体测量长标签，再给出列宽；不要压小字号掩盖容量不足。

回执含 rootId、cellIds、`refs.results`、`refs.results:r:c` 和非空 bound text 的 `:label` refs、当前 revision、原生 table 元数据及保存状态。

换外观：`action:"style", target:真实root或cellID, theme:"morandi-sage", border:"framed"`。只改 border 时省略 theme，保留既有颜色和手工填充。不要把空 target 当作“当前选中表格”。

## 所有权和事务边界

原生 schema-v2 table 使用 root/cell/content 角色、稳定 rowIds/colIds、columnWidths、行高策略和双向文字绑定。创建、主题和尺寸分别调用现有宿主方法；`atomic:false`，不是跨步骤原子事务，也不进入 `drawing_revert` 的 Bridge 历史。发生提交后错误会保留 root/ref/当前 revision 和 committed 标志；先读回，不盲目重新创建。

原生宿主的交互 API还包括 `setRowMode`、`setColumnWidth`、`setPadding`、图片／组内容挂载和插入删除行列；本 MCP 工具**只暴露创建、创建时列宽与主题／边框修改**，不要把其它 manager 方法当作新增 MCP 参数。复杂内容编辑继续按已验证的宿主 UI／可信原生脚本入口执行。

## 已运行证据与边界

- 甘特页：`light-mint + grid`，15格，列宽250/120/160；任务条与表格行对齐。
- 生态学页：`academic + three-line`，12格，列宽260/205/205；三条横线由原生 renderer 输出，没有模拟线条。
- 全图PNG、保存后的 schema/角色、完整文字和 containerId 已核对；主题／边框换肤保持 ID、内容与尺寸另有真实接口 smoke。
- 表格纸张必须位于自己的单元格／文字下，整体表格必须高于页面背景。创建入口使用原生 `newElementsOnTop:true`，不是靠白色遮罩修图。
- 源码依据：宿主 `src/view/managers/TableManager.ts`、`src/shared/table/tableAppearance.ts`；组件 `packages/element/src/tableText.ts` 与 `tableVisual.ts`。源代码存在、开发构建实测、正式发布是三个不同状态。
