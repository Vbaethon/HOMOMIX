# 当前自动验收覆盖与历史测试迁移

## 计数与运行方式

基线 `beb4b28fede0d4f8a93056113c276d0fc332c0e4` 的 `tests/test_*.py` 共 **48 个测试方法 / 7 个文件**；当前为 **46 个测试方法 / 9 个文件**。这里统计 `test_*` 方法，不把参数化 `subTest` 算作独立方法，不把 cold build 或手工视觉检查冒充单元测试。测试数量减少不等于逐断言完全等价；下面明确区分迁移、退休与未自动保证的性质。

```sh
python -m unittest discover -s tests -v
python scripts/validate_icons.py --tests --generated --cold --jobs 2
```

第二条另检查 README/catalog 重新生成一致性、177 个名称共 354 张当前渲染 PNG 的 cold rebuild SHA 与 manifest、生产文件三方一致。两张未完成 FDS 系列 PNG 不属于渲染器重建输出，由当前 collection manifest 保护。CI 的 build 作业运行全部 unittest 和 cold；独立 gallery/catalog 作业检查 generated，一律只读，无 commit/push。

## 旧 48 项逐 suite 对照

| 基线 suite（方法数） | 当前替代与有意退休的范围 |
|---|---|
| `test_catalog.py`（4） | 保留四项：目录缺失不写空目录；catalog 与当前生产一致；仅 canonical 存在才隐藏 alias；排序、转义、幂等。名称和链接新增由 metadata suite 检查。 |
| `test_dedup.py`（5） | 保留五项：单一 alias 表且无 Claud；旧 alias URL 可下载；只隐藏 alias 不误删变体；README 说明；目录内安全解析。 |
| `test_unified_revision.py`（8） | 保留八项当前约束、路径迁至 current：完整 collection/hash/count、354 PNG 的 RGBA/尺寸/hash、172 唯一展示及 alias 像素一致、14 款官方几何、23 款紧凑主体及阴影/圆边/留白、Bitcoin 背景、Crypto 背景、背景来源 hash。官方几何 fixture 改为 current 路径，不继续依赖旧目录。 |
| `test_v3_assets.py`（5） | `exact_pairs_dimensions_and_checksums` → 当前 unified 的尺寸/hash/成对输出；`complete_self_contained_native_sources` → current_sources 的资源 href 自包含检查、generic 无字体与 cold 重建；`protected_and_all_retained_png_bytes` → 当前 collection/alias 与本次发布前后 diff；`disposition_covers_all_174_and_matches_updates` → 当前 audit 覆盖所有现存生产路径；`source_inventory` → 单 current 结构、来源 hash、许可证与 cold 闭包。旧 106 个导出、174 项历史 disposition、旧源清单逐文件 hash 和全量 SVG ID 唯一断言不再保留为同等自动断言。 |
| `test_brand_revision.py`（7） | `all_urls_preserved_and_bytes_frozen`、`official_exports_and_pairs` → 当前 collection/exports/aliases、官方几何及 live official 无通用 finish；`distinct_balance_shapes_and_panda_anatomy` → live 负载均衡哈希互异，熊猫辨识仍需人工；`audit_covers_every_published_png` → current audit；`official_backgrounds_fill_circular_outline_without_white_frame` → 当前品牌几何锁、透明边界与默认 PNG hash；`original_background_and_logo_pixels_are_untouched` → 原始下载 hash 与当前 native 几何/嵌入 payload 锁；`deepseek_paths_unchanged_and_optically_adjusted` → live DeepSeek path 和 (80,90) 定位。旧版新增名单/旧 palette/熊猫两条 rotate 字符串及旧下载图逐像素对比不再单独执行。 |
| `test_optical_revision.py`（9） | `historical_collection_and_explicit_delete`、`every_standard_name_reviewed_and_exact_export` → 当前 collection/render、无 Claud；`native_geometry_preserved_except_requested_animals` → 当前14款官方几何锁与 generic finish；`actual_full_audit_paths` → current audit；`no_exact_duplicate_display` → 当前172展示哈希唯一；`overview_matches_canonical_catalog` → live preview manifest 名单/输入 hash；`background_roundness_and_source_identity` → 当前 source/geometry、透明边界与 cold；`deepseek_base_optical_center_preserved` → live DeepSeek；`fish_shapes_not_mirrored_duplicates` → 当前 Fish/Fish_b 输出哈希互异。旧 v8 字节/旧 scale 范围和历史任意非动物 path 对照不再冻结；哈希不同不证明不是镜像或艺术质量合格。 |
| `test_inverse_full.py`（10） | `taxonomy_and_series` → live49名单与series；`approved_theme_outputs` → 当前统一 hash/cold，而非旧主题快照；`white_disk_and_real_inner_layers` → live 白底/finish；`hues_and_holes` → live gradient ≥3 distinct stops，**不等价于像素色相分桶或孔洞面积**；`inner_proof_and_shadow_margins` → live透明边缘、finish结构，旧 inner-only 像素证明退休；`broad_gaussian_outer_not_tight_contact_layer` → live cast blur13、offset(7,11)、disk blur2.5/opacity.035；`preview_uses_exact_actual_exports` → live preview 输入 hash；`v5_geometry_locked_except_reviewed_identity_fixes` → 当前官方几何锁，不再冻结全部旧generic图形；`centered_symmetric_inner_effect` → live SourceAlpha/无内阴影 offset/模糊参数，旧反射对称性数值报告不再重验；`baseline_workflows` → 改为 current CI 全触发、只读、依赖 pin 等正向约束，**有意移除旧 workflow 字节冻结**。 |

旧 suite 共 48 = 4 + 5 + 8 + 5 + 7 + 9 + 10。历史源快照按“只保留最新版”的要求从工作树移除，过去版本可从 Git 历史取回；不是把旧 snapshot 测试换路径后假装仍验证历史设计。

## 当前 46 项清单

| 当前 suite | 方法数 | 主要 live 证据 |
|---|---:|---|
| `test_catalog.py` | 4 | catalog 安全生成/一致性 |
| `test_dedup.py` | 5 | 兼容 alias、Claude 拼写及变体 |
| `test_unified_revision.py` | 8 | 当前 PNG/几何/compact/背景来源 |
| `test_current_sources.py` | 9 | current-only、49 generic、live finish、自包含资源、当前 audit、下载 hash、外边缘透明、定点互异、许可证 |
| `test_current_design_guards.py` | 3 | live 渐变/内阴影/外阴影、官方几何/DeepSeek、当前预览输入 |
| `test_icon_metadata.py` | 4 | 344 stable IDs/尺寸、172完整唯一显示名和最新链接、准确名称兼容旧路径、长品牌限制说明 |
| `test_parameter_layers.py` | 5 | 七款默认像素精确；逐款 scale/dx/dy；背景重建基本安全；CLI 不覆盖参数；非法参数拒绝 |
| `test_remaining_parameters.py` | 6 | 8种代表图默认字节、7种可动图 dx/dy、native背景节点不动、实际scale/policy、compact_scale、拒绝不支持的编辑 |
| `test_validation_ci.py` | 2 | 配置/固定依赖，全部变更触发、完整测试/cold、无push |
| **合计** | **46** | `subTest` 为各方法内多个样本，不另外加数 |

### 参数测试的边界

七款指 Google、Gmail、TikTok、Facebook、Pixiv、Bluesky、Instagram。每款均检查默认 RGBA 与批准输入相同，以及独立 scale、dx、dy 的像素响应；不再固定成品覆盖参数。背景不可见区域是重建估计，不是凭空恢复官方原始分层；“hidden background”哈希断言本身不能证明没有任何残影，仍须查实际变换预览。

其他分支以 AI、Grok、Fish、Other、GOG、Disney_Mickey、Piggies、China 为代表，不意味着每个名称/每个极端参数都被穷举。完整 composition 明确拒绝非默认变换；紧凑图使用 compact_scale 并拒绝误用旧 scale，报告记录实际策略。SVG 抗锯齿/软阴影在圆边可能引起极少 alpha 量化差；具体容差以测试代码为准，不应把容差通过写成逐像素完全固定。

## 非自动质量保证与剩余限制

- 哈希/cold 相同证明重建稳定，不证明视觉大小完全统一、视觉中心完美或造型艺术质量。必须看真实导出和小尺寸预览。
- ≥3 个 gradient stops 不证明跨色系跨度足够，也不替代实际像素 hue-bin 检查；当前不自动测所有内部孔洞最小面积、全套镜像相似度、阴影反射对称性。
- Disney_Channel / Olympics 的官方细长/细线标识，小尺寸仍有辨识限制；不以拉伸/描粗伪造官方 compact 版本，目录提供 Large 与说明。
- 官方来源 hash/几何锁证明当前记录的来源未被改写，不证明所有品牌身份都已核实；审计中的未确认身份仍是未确认。
- CI 文件可执行性/本地通过不等于 GitHub 已运行成功；发布后须另记录远端 run 状态。
- 本次独立比较生产 PNG 路径集合未变，仅 Chained、Chained_2、Auto_Link、Link、Niche_Link 的两个尺寸共10张不同；这是发布前 diff 证据，不是让未来所有合理修改都失败的永久测试。
