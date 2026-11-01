# HOMOMIX 当前审计修复验收

基线：GitHub main `beb4b28fede0d4f8a93056113c276d0fc332c0e4`。本报告记录本地修复与验收；远端同步、远端 CI 状态由发布记录另行确认。

## 已修复

- Google、Gmail、TikTok、Facebook、Pixiv、Bluesky、Instagram 不再用整张固定PNG覆盖调整。背景/主体分层，默认7款两规格共14张像素不变，21个scale/dx/dy独立变化有回归；命令行自定义plan同样验证。
- Native及GOG、Mickey、Piggies等分支补齐位移；compact明确使用compact_scale，修改不生效的旧scale会报错；六个完整构图明确拒绝非默认变换，而非谎报可调。
- CI改为所有main变更及PR触发，只读验证；Python3.12与精确固定Python依赖、Node22与npm锁文件；全unittest、生成目录检查和全354张冷构建，不再只运行4个catalog tests。
- README 172个完整唯一名称；主目录344条唯一id。FC2、SoundCloud、Creative Cloud、Edge显示身份更准确，下载文件名兼容保留。
- Chained、Chained_2、Auto_Link改为能辨识穿插的厚链环。连同Link、Niche_Link兼容别名，两规格仅10张PNG改变，其他生产PNG不变。
- 当前源码只留Sources/current。解除旧版本目录依赖，保留必要原始官方素材、提取输入、许可和溯源；旧版本快照、候选QA和重复包退出当前分发，Git历史可回退。
- 图标库只保留原三类入口：等高Color、放大Large、未完成FDS。实测等高177张为300×300（180图案居中留白），Large177张为360×360（图案近满画布），FDS两张125×90；和发布基线一致，不改原功能。主目录排除5个兼容别名和未完成FDS，后者保留独立清晰入口。

## 验收证据

- 本地统一验收命令 `python scripts/validate_icons.py --tests --generated --cold --jobs 4` 已通过（2026-11-01）；354张cold哈希全部与manifest及生产一致。
- 全测试46个方法；不是以方法数量冒充全覆盖，旧48项与现行检查的逐类映射见TEST_COVERAGE.md。
- 默认生产路径集合未增删；仅10张链路PNG像素变更。现行生成图清单354张；FDS不由当前完整系列重建。
- 全套当前实际小尺寸图与总览位于Sources/current/qa/final；manifest逐图记录生产输入哈希。
- 新增变换回归允许SVG主体位移后极少边缘像素的抗锯齿差异：max alpha差2、非零像素最多20；实测Fish各轴10像素差1–2。背景节点结构严格不变，默认输出逐字节一致。

## 仍需如实保留的限制

- Disney Channel长字标、Olympic细线五环在36px视觉仍偏弱；没有核实到可用官方compact替代，不重排/描粗/拉伸官方标。目录提示配合标签或大尺寸，而非宣称视觉分量已等同实心图案。
- 九项此前身份来源不确定性未凭空消除；官方身份识别也不等于获得再分发或商用许可。
- 遮挡背景重建来自现存像素推断，非恢复官方原始图层。六个fixed composition需进一步层拆才能独立编辑。
- 自动测试验证结构、像素、参数、尺寸与重建确定性，不能证明所有形状在人的视觉上完全等重。
