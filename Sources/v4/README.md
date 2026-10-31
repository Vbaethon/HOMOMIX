> 历史身份修订层：当前生产光学尺寸与目录去重以 [v5](../v5/README.md) 为准。此处原始官方素材和历史测试输入保留，用于来源与重建溯源。

# HOMOMIX · 官方标识与辨识度修订

**构建记录：本包已验证；发布状态以 GitHub main 的实际提交为准。** 基线为 `8830f6cd9ee4676d5c161e022cbefa8cd279a581`。

## 本轮结果

- 更新12个既有名称、24张PNG；新增Grok、Gemini、DeepSeek共6张PNG。总计30张变更/新增，原目录无删除。
- 原创修正4项：Load_balancing_2、Load_balancing_3、Panda、Panda_ai。第一款Load_balancing分流树保留，预览中展示它只是比较三种样式。
- 官方错标/非旧版命名过时标修正6项：AdblockPlus_2、Microsoft、Disney_Channel、UBISOFT、Peacook、Scholar。
- 官方compact忠实重采样2项：Disney、Disney_plus。**单独D本身有官方依据，不是因为缺完整字标或加号而错误。**
- 所有既有URL、Claud兼容别名和FDS图片保留。共177规范名称、178个默认路径（含别名）、178个Large路径、2个FDS路径，即358个PNG。

## 设计约束

原创图形使用白圆盘、功能系列配色；熊猫用黑白耳斑、白脸、宽鼻，避免旧版猫头鹰感。负载均衡为分流树、中心分发、平衡秤三种概念；平衡秤不是网络拓扑示意。

原创图形内阴影仍为居中零偏移、blur2.6、12%；高光居中blur1.1、3%；外影(7,11)、blur13、11.5%。没有为本轮重做阴影。

官方前景保持其几何、颜色和宽高比，不强加自定义渐变、内阴影或描粗；通过等比缩放和光学位置统一。有官方自带背景的Grok、Peacock、Disney公司标、Scholar使用官方背景铺满统一圆形，不再外套白圈，不新增阴影；完整保留主体，圆裁不能切到标识；透明标识才使用统一白盘。Disney公司暖白背景铺满圆形，不再使用之前试版的背景提取结果。Grok移除原App方框反光边，保留两个官方银色主体组件的原始RGB/抗锯齿，按300原生宽度居中放在官方纯黑圆底，斜线两端不被裁切。DeepSeek保持官方路径，整体右移18原生单位，按实际视觉重心校正，垂直和尺寸不变。Disney+使用官方compact SVG。Disney Channel未找到可确证独立compact标，保留完整官方字标，小尺寸细节较弱，不冒用DisneyNow红D。

## 全量审查与限制

`OFFICIAL-AUDIT.json` / `.md` 覆盖180项（包含别名与FDS），对应全部358路径。**路径全覆盖不等于全部官方来源确认。** 各项“正确”指身份和基本几何匹配，不代表原始压缩字节溯源一致，也不授予商标许可。

9项未完全确认，逐项保留现状和原因：bilibili、Bilibili_blue、Bilibili_Global、Omission、Onlyfans、Pornhub、Seancody、xHamster、Zune。部分官网受限，部分为历史/子品牌或命名含义不明；不凭印象重画或冒充官方。

新品牌母版中6个为官方矢量，5个使用真实官方栅格资产（Grok、Disney、Disney_Channel、Peacook、Scholar）。后者不宣称原生矢量或无限分辨率。Large尺寸可能显现栅格源柔化，默认60px展示对应36px内容盒。

完整仓库输出均随包保存。v3的53项与v4的11项可从自包含母版再生成128张PNG，其余230张历史PNG保留原字节；没有伪造这些历史文件的矢量源。

## 再生成

依赖使用 `Sources/v3/requirements.txt` 与 `Sources/v3/package-lock.json`，固定Pillow11.3.0、resvg-js2.6.2。首次安装：

```sh
python3 -m venv .venv
.venv/bin/pip install -r Sources/v3/requirements.txt
npm ci --prefix Sources/v3 --ignore-scripts
```

离线验证导出（不写生产文件、不自动改变期望摘要）：

```sh
.venv/bin/python Sources/v3/build_all.py --output-dir /tmp/homomix-generic --verify
.venv/bin/python Sources/v4/build_brands.py --output-dir /tmp/homomix-brands --verify
.venv/bin/python -m unittest discover -s tests -v
```

`prepare_official.py`保留组件裁取和早期试版背景提取过程（当前Disney使用完整原图，不使用该提取结果）；`author_brands.py`重建官方母版；`author_sources.py`重建原创母版。预览仅从实际生产PNG读取，中文联系表额外需要Noto Sans CJK字体；生产图标不依赖字体或网络。

`freeze_revision.py`是人工审查后的显式冻结工具，不应为通过测试盲目更新摘要。`collection-manifest.json`锁定全部358文件和基线差异，`render-manifest.json`锁定品牌导出，`qa/preview-inputs.json`记录预览输入。

商标、角色与原项目素材权利属于各权利人。官网素材用于用户请求的图标适配，未声称官方授权、未重新许可为CC0。工作流文件未修改。
