# v6：固定背景、主体光学校准与原创图形整理

本目录记录当前制作方案。`plan.json` 和实际渲染产物是执行依据；早期 QA 候选、分类提案与下载素材并不自动代表最终采用方案。

## 当前采用的特殊图形

- **Sony_Live**：使用 `Sources/v5/input-large/Sony_Live.png` 的原始白色 SONY、金色 liv 像素分离主体，保持原满圆紫色流光背景。`separate_special_rasters.py` 仅对被原文字遮挡的背景做 Laplace 插值恢复；这是近似修复，不是声称取得官方分层底图。不采用内嵌方卡替代。
- **Steam**：保留原图正型白色机械连杆与既有蓝色背景；采用 `build_unified.py` 的 `steam_existing_positive` 分支。`official-special/Steam.svg` 是官方来源研究资料，其负空间替代造型未用于当前生产。
- **Xbox**：采用 `official-special/Xbox.png` 中官方透明完整立体球标，作为整体主体以 **0.70** 缩放置于固定白底。按透明官方球体作为主体的规则；旧 QA 中“保持原满圆”的建议已被此决定取代。球片之间的 X 是透明负空间，不能另行编造小白 X 或球面沟槽。

## 数量、兼容与展示

- 49 个原创名称：23 项集中重绘、2 项兼容别名、24 项保留。
- 177 个现存名称，默认/Large 共 **354 张标准 PNG**；默认展示 **172 项**。
- 5 个兼容别名由仓库根目录 `icon_aliases.json` 统一维护：Zoho_old → Zoho_new、Download_2 → Download、Niche_Link → Chained_2、Twitter → X、Link → Chained_2。旧文件 URL 保留，展示不重复计数。
- 拼写错误 `Claud` 已删除，不属于兼容别名；规范名称是 `Claude`。
- 同主体配色保留为配色变体，不冒称独立造型。

## 依赖与复现

验证环境使用 Python 3.12、Pillow 13.0.0、NumPy 2.3.5、SciPy 1.17.0；依赖精确版本列于 `requirements.txt`。SVG 使用 Node.js 的 `@resvg/resvg-js` **2.6.2**，锁定信息位于 `Sources/v3/package.json` 与 `package-lock.json`。

在仓库根目录运行：

```sh
python -m pip install -r Sources/v6/requirements.txt
npm ci --prefix Sources/v3
python Sources/v6/build_unified.py --output-dir ./build-v6-check --jobs 4
```

输出到独立目录，审查后才替换生产。构建还会更新本目录 `svg/` 中间文件，故它不是完全只读命令。`Sources/v6` 不是可脱离仓库单独运行的包：保留 `Sources/v3` 原创源/renderer、`Sources/v4` 官方源、`Sources/v5` 原始输入与复用模块，以及根目录别名表。不要删除这些前序版本依赖，也不要通过修改前序历史文件改变基线。

`raster_colored.py`、`raster_white.py`、`raster_pale.py` 将主体与固定背景分开；不使用旧版整图缩小补白圈。未知的遮挡底色只能近似恢复，应查看实际 36px 和放大 QA，不能只凭 bbox 或圆盘面积宣称一致。满幅旗帜等按计划列构图例外。

## 源与 QA 状态

- `official-special/provenance.json` 明确区分下载研究素材和当前生产来源。
- `qa/separate-special/report.json` 记录 Sony 分离证据及 Xbox 决策更新。
- `qa/` 中早期实验图仅作为追踪证据；当前模式以 `plan.json` 为准。
- JSON 文件引用采用仓库相对路径或官方 HTTPS URL，不应含本机绝对 workspace 路径。

## 验证结果与边界

当前全套 48 项测试通过；354 张标准 PNG 已从最终源冷重建。主展示 172 项没有像素重复；5 个兼容别名仍可下载。完整官方来源审计沿用 `current-audit.json`，9 项无法完整确认的品牌身份仍明确保留不确定状态，不将全路径检查冒充全部官方核验通过。

23 项集中重绘统计包含 Download_2 兼容别名；规范造型数不把别名重复计入。链路三款是同族胶囊与不同负形，不宣称完全不同外轮廓。长字标不拉伸或人为加粗，形状导致的阅读限制仍存在。Sony 等扁平位图分离中被旧字形遮挡的背景采用近似恢复；已审实际小尺寸，不声称获得不存在的官方分层源。

## 最后定点背景校核

Bitcoin 的橙色改为满圆背景、白 B 独立调尺寸，是用户要求的套系布局适配；官方原资源仍是完整币标，不能将此改排称作官方新logo。Crypto采用已核实官方App深蓝底与完整白六角狮头，去掉旧项目青绿配色。GOG采用官网紫色字形白底，移除未证实的旧黑紫方卡。Reddit、Messenger 的彩色气泡和YouTube的红色播放板属于标识本体，保留完整几何，不机械拆除。
