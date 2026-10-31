> 当前整套候选由 `Sources/v4/README.md` 和 v4 全量清单统领。下述53项是通用图形/主题作者流程；品牌修订、新增AI及全量审核见v4，旧版“全套/不变”描述仅指当时范围。

# HOMOMIX · 白底通用图形源（v3）

当前更新53个名称／106张PNG：49项原创通用图形使用白圆底、按功能系列统一的渐变或近黑主体、协调内缘层次与柔和外阴影；另完整保留已确认的Bahamut三款龙形简化与Disney_Castle比例修正。当前为按最终方向新作，不冒称此前丢失源包原件。

174个规范名称全部分类：53更新、121保留。原352个PNG路径和Claud兼容文件保留，范围外246个PNG与基线`efe70aec5ee7da492609be67a53c6a9dde78c3a2`字节一致。官方品牌、FDS、Google、Apple_rainbow、GOG、Twitch、Apple、Plex、Linkedin_ray、Claude/Claud均未改。既有工作流字节不变。

## 内容

- `svg/`：53个自包含母版。49通用项原生矢量；四项主题例外含来源保真内嵌位图，不宣称全套纯矢量。
- `author_sources.py`、`material.py`、`adjustments/`：完整作者流程、统一材料效果及逐项紧凑度／光学微调。
- `references/original-white-geometry/`：49项前版原生形状输入，仅作作者几何来源，不是当前生产配色。
- `SERIES-49.json`、`SERIES-PALETTES.json`、`SOURCE-LEDGER.json`：最终功能系列、色值和逐项来源。
- `DESIGN-STANDARD.md`：原生单位、视觉尺寸、负形、阴影与小尺寸限制。
- `TAXONOMY-174.json`、`all174-disposition.json`：全目录更新／保留理由。
- `render-manifest.json`、`collection-manifest.json`：106个输出与53个原生源的SHA-256、尺寸、偏移。
- `qa/inverse49-overview.png`、`qa/inverse49-actual60.png`：49项大图与真实60px默认／Large浅深底。
- `qa/shadow-inner-on-off.png`：仅开关内缘光影，其他几何、颜色、外阴影相同的证明。
- `qa/all174-overview.png`、`qa/approved-theme-exceptions.png`：完整目录及四项例外。

## 复现

首次安装需要网络：

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r Sources/v3/requirements.txt
npm ci --prefix Sources/v3 --ignore-scripts
```

安装后离线导出，只写显式目录：

```sh
.venv/bin/python Sources/v3/build_all.py --output-dir /tmp/homomix-final --verify
.venv/bin/python -m unittest discover -s tests -v
```

resvg-js2.6.2在1440px渲染，Pillow11.3.0 Lanczos缩放。Large360；默认300画布、180内容盒、偏移(60,60)。49项白盘半径175原生单位，给淡外影留5单位边缘；默认60px显示时内容盒36px、白盘35px。四项主题例外保持原有输出字节。生产不依赖字体或网络。

`author_sources.py`可重建全部母版。设计变更后须人工复核并显式冻结摘要，不能为通过测试直接篡改期望值。固定环境可核验106个PNG SHA；跨平台压缩库不同可能改变文件摘要而不改变解码像素。

## 来源与限制

49项形状为本项目原生构造，地理轮廓使用随包Natural Earth公有领域数据；没有新增第三方图标路径。QA使用附许可证的DejaVu字体。Apple Music官方商店图仅作为近黑主体和细微层次的视觉参考，未复制音符或打包Apple素材。品牌、角色与原项目素材权利归各自权利人，适配不构成官方新标，不重新许可为CC0。

默认60px画布内的36px内容盒以识别和内轮廓可读为主；内缘效果刻意保持轻微，在36px可能极细微，不宣称所有尺寸都有同等立体感。亮黄绿局部对比低于蓝紫或近黑，已按实际小尺寸检查，不冒称每个渐变像素达到统一无障碍阈值。




## 历史 V5：仅居中、淡化内阴影（已在 8830f6c 发布）

只替换内部深色／微光层，保留外投影(7,11)、blur13、11.5%与白盘外影原字节。主体几何、渐变、布局和白盘大小全部不变，四项主题和所有保护项不变。该历史修订已发布；本轮身份修订候选尚未同步。

`qa/centered-inner-before-after.png`为实际完整导出PNG的旧／新内缘对比和真实60px；`references/NON-INNER-LOCK.json`验证除内缘过滤块外全部53个SVG原文一致。`qa/inner-symmetry.json`用对称圆形检验效果自身：内缘无offset，横／纵归一化反射差异约0.15%／0.13%，重心偏移小于0.006原生单位；局部边缘可有几个alpha级的栅格量化误差，不虚称逐像素数学完全对称。该诊断与原图形本身是否对称无关。

## 本轮身份修订

Panda/Panda_ai 改为黑白熊猫解剖特征（圆耳、斜向眼斑、宽鼻），两项归入 graphite 系列。Load_balancing 保留分流树，_2 改中心分发，_3 改平衡秤概念变体；后者不是网络拓扑示意。通用主体阴影参数保持不变。
