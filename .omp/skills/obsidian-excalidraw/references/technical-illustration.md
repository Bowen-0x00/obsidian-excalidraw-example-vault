# 技术插图：投影、剖面、层叠与标注

先读[视觉设计层](visual-design.md)，再按任务选组件。复用 drawing_primitives → 原生operations → check/PNG/review/deliver，不新增渲染引擎。这些kind及托管render需要0.10.3或更新运行包；0.10.2只有原有cuboid等。先核对工具schema/运行版本，不能只复制本文假装API已升级。

## 坐标与投影

局部物理坐标为u/v/z；z向上。斜投影 `p(u,v,z)=(x+u+vx*v, y+vy*v-z)`，当前支持右上深度轴vx>0、vy<0。默认projection=[0.65,-0.45]。x/y是共同模型原点，不是投影bbox左上；可负。一个视图内使用共同x/y/projection，几何规划返回实际bounds和world anchors。二维投影不是可旋转三维模型或CAD。

## 确定性组件

通过 `drawing_primitives(items,style)` 规划，style中的fontFamily必须来自当前宿主发现。原生操作仍由[现有执行层](native-features.md)构造。

```json
[
  {"kind":"projected_box","id":"logic-oblique","objectId":"logic","viewId":"oblique","x":100,"y":500,"u":80,"v":30,"z":60,"width":180,"depth":100,"height":30,"faceColors":{"top":"#81b99a","front":"#589b78","side":"#3b7457"}},
  {"kind":"layer_stack","id":"package-section","viewId":"section","x":800,"y":500,"width":440,"depth":200,"layers":[{"id":"substrate","height":45,"color":"#64748b"},{"id":"interposer","height":20,"color":"#de9f92"}]},
  {"kind":"grid_array","id":"bumps","objectId":"bumps","viewId":"section","x":810,"y":510,"rows":1,"cols":12,"pitch":[32,20],"size":[10,10],"shape":"ellipse"},
  {"kind":"leader","id":"interposer-leader","viewId":"section","points":[[1350,470],[1280,470],[1240,470]],"target":[1240,470],"targetObject":"interposer"}
]
```

- projected_box：三张闭合原生line多边形，独立面色，保留共同模型和anchors。width/depth/height>0。
- layer_stack：layers自底向上，每层唯一id、height，gap>=0；view=section（默认）或oblique。稳定ref含层id，不按当前数组序号重命名。
- grid_array：正整数rows/cols，pitch与size为正；实际投影后的cell也不允许互压，最多200格。数量属于示意或实数必须注明。
- leader：world points，末点须命中target（1 scene单位）；可斜线，不套电气正交门。targetObject用于专项目标检查，不虚构startBinding/endBinding。
- text：`{kind:"text",id,x,y,text,width,style,objectId?,viewId?}`，按当前字体测量换行；objectId/viewId让同名对象跨视图核对label。默认外部文字不随便压在斜投影面上。

多个组件总批次最多500 operations，超出明确拆区域，不静默丢弃内容。plan返回anchors/manifests/measuredBounds；不能把返回bounds坐标当模型origin反写。

## 可编辑增量

`drawing_primitives(action:"render",state_id:"固定任务身份",base_revision:当前版本,context_token,items,style)`复用已有Scene reconciler，技术kind和text支持同state_id增量。返回真实PNG和check，不自动视觉批准。默认action=plan不写画布。CLI走同名primitives JSON入口。

同一画布的原生ID、外部改动指纹、状态锁和错误提交回执沿用既有机制。复用state_id，不重放原图。跨资源/类型替换不假装同ID，必要时用新逻辑对象明确替换。

局部验证至少：HBM层数5→7时原有层ref/ID保留，只加新层；移动logic同时更新其标注；增interposer厚度时上层抬升、下层不动。观察实际PNG和逐对象diff，不能只证明元素变多。

## 封装双视图示例规则

- 左侧：同面芯粒+中介层+基板的斜投影；RF/MEMS可位于右侧剖切面外，明确说明。
- 右侧：Logic/GPU与HBM剖面、Interposer、Package Substrate、PCB、可选Heat Spreader；截面只表达穿过的对象，不要求投影图每个芯粒都出现在截面。
- Logic绿色、Memory/HBM暖色、Interposer粉色、Substrate灰、PCB绿；同一物体跨视图用相同语义色，参考颜色不是精确材质。
- 重复HBM层/凸点/TSV均标“示意，数量及厚度不按比例”；不从低清截图推断工艺层数、材料、热/电性能。
- Interposer可为硅/重布线等实现，不能画一种颜色就宣称一定是硅；术语不清在说明中披露，不伪装制造模型。

## 专项质量门

visual_plan声明的对象在各视图需有真实body；标签需一致。检查supported_by/contains、模型体积穿插、保存后的投影几何是否仍与构造一致；合法投影重叠只按未变的具体模型体积判断，不免除跨物体碰撞，也不免除文字碰撞。

引出线检查当前末点与目标部件范围；可见面的实际命中、遮挡、厚度易读、视图对应仍需PNG检查。复杂材质/照片不自动转原生分层。详见[字体](typography.md)、[验收](acceptance.md)、[完整交付](workflow-details.md)。

引出线可经过其目标和按共同模型原点／投影／足迹／接触高度证明的承载背景；无关实体和所有文字仍检查。新层默认按新增元素绘制顺序进入场景，不承诺任意插层自动修复所有遮挡；务必查看增量PNG，优先把标签放在可增长结构之外。实际案例的新增HBM顶面曾盖住旧引出箭头，已通过局部移动标签修复，不能把几何pass说成可见性证明。
