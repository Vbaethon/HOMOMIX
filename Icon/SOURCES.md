# 图标来源与项目适配记录

本台账记录已核实的素材来源和实际改动，核查日期为 **2026-10-30**。
未列出的图标不代表已经核实官方来源；本项目 PNG 也不自动等同于品牌官方提供的成品图标。

来源分类：
- **官方几何 + 项目适配**：轮廓来自官方材料，背景、配色或排版由项目适配。
- **既有素材衍生**：基于仓库已有图形优化，如实保留来源不确定性。
- **项目自绘**：仅在确实采用自绘图形时明确记录，不冒称官方品牌素材。

## Bilibili 三个变体

适用文件：
- `Color/bilibili.png` 与 `Color/Large/Bilibili.png`
- `Color/Bilibili_blue.png` 与 `Color/Large/Bilibili_blue.png`
- `Color/Bilibili_Global.png` 与 `Color/Large/Bilibili_Global.png`

**分类：官方几何 + 项目配色适配。**

来源为国际 Bstar CDN 托管的 [Bilibili Brand Identity Guidebook v1.03，第 9 页](https://p.bstarstatic.com/fe-lib/images/web/Brand%20Guidelines.pdf)。
采用 PDF 中原生矢量路径，保留路径与比例，不手绘或描摹；用小电视主体替换小尺寸下难辨认的字标与淡色水印。
三个变体保留项目原有的粉色、蓝色、白色底板及白色/粉色主体关系，并保持原有圆形和渐变风格。

这属于项目选择的统一可读性适配，不声称国际版指南是国内版的强制品牌规范，也不声称这些配色 PNG 是未经修改的官方成品。

- 官方 PDF SHA-256：`1f6ca5e9026ed3e4b171c78b0d9adcdc9529801659dc3981d5cd895460858e43`
- 提取 SVG SHA-256：`4eae2d0c7c77acfcde5359a0fd6ff3f55467e5f08af10ed6f5e9e9b5e7ffa79e`
- 官方品牌资料为专有素材，**不是 CC0**；未将第三方图标库许可套用到该素材，也不宣称另行取得了品牌授权。

## OnlyFans

适用文件：`Color/Onlyfans.png` 与 `Color/Large/Onlyfans.png`。

**分类：既有仓库素材衍生，非本轮取得的官方矢量。**

保留[基线仓库中已有的双色 OF 标志](https://github.com/Vbaethon/HOMOMIX/blob/ec81d9930c50538b0f8bbd4e385faedc193b7db1/Icon/Color/Large/Onlyfans.png)，去掉微小字标，将主体等比放大，并向右下微调视觉重心；不凭空重画品牌轮廓。
相对第一版可读性预览，Large 向右 16 px、向下 8 px，默认版向右 8 px、向下 4 px。

[Simple Icons 的固定版本轮廓](https://github.com/simple-icons/simple-icons/blob/90646e4bf7f3b89df6c37e65baf3e7bc759a517c/icons/onlyfans.svg)仅用于辅助核对标志身份，并不是本次渲染的双色源素材。
本轮找到的官方品牌资源地址未返回可用素材，因此不把当前图标称为已下载并核实的官方矢量；原仓库素材的完整授权来源仍未独立确认。

- 基线源图 SHA-256：`55f6ad3c0ebac0a0e17adf4bf0cfba8a231cbbde9de707864450a802077fac26`
- 不将 Simple Icons 的 CC0 许可归给该既有双色 PNG。

品牌名称与商标权归相应权利人所有；本项目适配不代表品牌官方出品、授权或背书。

## 第二批小尺寸主体优化

以下五个名称均同时适用于 `Color/` 和 `Color/Large/`；保留各自原有背景形状、配色风格与透明轮廓，不统一替换外壳。
本批继续区分「官方原生矢量」「官方位图的项目矢量衍生」和「非品牌功能图形自绘」，不把后两者冒称官方 SVG。

### Disney

- [Disney 官网](https://www.disney.com/)实际链接的 [D 字 favicon](https://static-mh.content.disney.io/matterhorn/assets/favicon-94e3862e7fb9.ico)，最大原图为 64×64。
- 取该 Disney.com 图形的实际轮廓并作平滑矢量衍生，原尺寸轮廓重叠 IoU 为 0.97576；**不是下载到的官方 SVG**，也没有拿 Disney+ 的几何替代通用 Disney。
- 保留项目白色主体及原底板；默认版原有圆角方形、Large 原有圆形分别保留。
- 源文件 SHA-256：`a600974287c84ec71850184d929a9d718fa5c189f951a677ae027bb1810e61fa`。

### Disney_plus

- [Disney+ 官网](https://www.disneyplus.com/)实际链接的[官方浏览器 mask-icon SVG](https://static-assets.bamgrid.com/product/disneyplus/favicons/mask-icon-aurora.86b2f302cf50180b25ddd8835041b1c3.svg)。
- 保留原生 D 矢量路径、等比缩放并适配项目原有白色主体；没有另造加号或拼接新的标志组合。
- 源文件 SHA-256：`0bc31ff0134ca63f2b31a6d2633dd965a2279ef451337b7646918914e2e086ba`。

### Zoho_new

- 使用 Zoho 官方静态资源域上的[四色 favicon](https://www.zohowebstatic.com/sites/zweb/images/favicon.ico)，最大原图为 48×48；与[官方视觉指南](https://www.zoho.com/branding/visual-guidelines.html)中的完整字标区别记录。
- 按实际四个色区忠实矢量化，保留四色与项目原有灰白背景；没有自造 Z 或从完整公司字标任意裁切。此为**项目衍生矢量，不是官方 SVG 下载**。
- 已核实素材由官方域托管；本轮官网页面读取受限，未重新核实当前首页的 `rel=icon` 引用，也未取得相同四色环的官方高分辨率矢量。
- 源文件 SHA-256：`578688454641bfca876d506e911b1ad9e6a0521a773e9dabe18a1adaa1a0a013`。

### AI_voice 与 AI_Tree

- **AI_voice：项目自定功能图形。** 保留原紫色渐变与透明轮廓，去掉被截断的小字，将 13 条细波形简化为 7 条较粗波形，改善 32 px 显示。
- **AI_Tree：项目自定功能图形。** 保留黑白配色、中央环与放射神经节点概念，简化为 8 个主要连接节点，去掉小尺寸下混成一团的细枝。
- 两者不是品牌官方素材，不宣称第三方官方来源。

以上品牌素材未核实开放源代码许可，不套用 CC0；品牌与商标权仍归相应权利人。所有最终 PNG 都包含项目布局/配色适配，不是官方未经修改的成品下载。
