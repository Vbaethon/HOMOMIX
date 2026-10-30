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
