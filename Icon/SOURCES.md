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

## 2026-10-30 — Current marks, retained project themes and circular containers (revision 2)

Baseline `638ecb4df92a43ba8938023c538d36764e38a07b`. **59 PNG paths / 34 ordinary icon names**. All sources below were checked on **2026-10-30**. Official geometry and project adaptations are distinguished; these PNGs are not presented as unmodified official deliverables. Trademark and copyright rights remain with their respective owners.

### Official technology sources

- **Google.png** — [source page](https://blog.google/image-library/); [asset/package](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/GoogleG_FullColor_White_RGB.original.jpg). Source SHA-256 `4d19bb8c9e422f5ab65e206a11b73b24d8f793541fbeefe8304334a121372459`. Official high-resolution gradient G raster; only white margins cropped. Native colors retained.
- **Gmail.png** — [source page](https://workspace.google.com/products/gmail/); [asset/package](https://www.gstatic.com/images/branding/productlogos/gmail_2026/v2/web/192px.svg). Source SHA-256 `0a242131424b796a26247a8edd41d66fa294da6d177897526a19b7e81aedfdb8`. Native geometry and colors uniformly scaled on a project circular base.
- **Outlook.png** — [source page](https://www.microsoft.com/en-us/microsoft-365/onedrive/online-cloud-storage); [asset/package](https://www.microsoft.com/content/dam/microsoft/bade/images/icons/en-us/m365-app-icons-fy26/Outlook-Icon-FY26.svg). Source SHA-256 `d67b8bb4bb8d7afe8e71e066112452d5d681ea7991fa1ec7c37df962246b2c31`. Native geometry and colors uniformly scaled on a project circular base.
- **OneDrive.png** — [source page](https://www.microsoft.com/en-us/microsoft-365/onedrive/online-cloud-storage); [asset/package](https://www.microsoft.com/content/dam/microsoft/bade/images/icons/en-us/m365-app-icons-fy26/OneDrive-Icon-FY26.svg). Source SHA-256 `9f72ac359c7e03ca4723ce1a3b60f932a0bc5d2ce72dbdce365e83223142f6bc`. Native geometry and colors uniformly scaled on a project circular base.
- **Microsoft_Copilot.png** — [source page](https://www.microsoft.com/en-us/microsoft-365/onedrive/online-cloud-storage); [asset/package](https://www.microsoft.com/content/dam/microsoft/bade/images/icons/en-us/m365-app-icons-fy26/Copilot-Icon-FY26.svg). Source SHA-256 `f16fdf8123d9dc4597561bfc62cebf5bc43262a1301d9acd470c4914e6dd1e1f`. Native geometry and colors uniformly scaled on a project circular base.
- **Messenger.png** — [source page](https://www.meta.com/brand/resources/facebook/messenger-icon/); Messenger Icon Pack downloaded from the source page. Source SHA-256 `0278c863f568da118d80547ceee6ad0b75381111e72d7c69cdd8859467c7889b`. Native geometry and colors uniformly scaled on a project circular base.
- **Reddit.png** — [source page](https://redditinc.com/brand); [asset/package](https://redditinc.com/hubfs/Reddit%20Inc/Content/Brand%20Page/Reddit_Logo.png). Source SHA-256 `b0944f3d873c71965cd657a009d3c9b336c66858eb49d255739ade244501b15f`. Native geometry and colors uniformly scaled on a project circular base.
- **GitHub.png** — [source page](https://brand.github.com/foundations/logo); [asset/package](https://brand.github.com/GitHub_Logos.zip). Source SHA-256 `ccd84c89b1056345608fc3489357f8acc7397e49a3cdc2d418b6c8016911d47b`. Current official white inverse mark, including native negative-space structure, on clean black project circle.
- **Adguard.png** — [source page](https://adguard.com/en/media-materials.html); [asset/package](https://cdn.adguardcdn.com/website/adguard.com/media-kits/logos/AdGuard_Ad_Blocker_logos_and_icons.zip). Source SHA-256 `cf5b41f5aa80899ecce63962395a7ab50e3efeeea65b45de117847eb88455e18`. Native geometry and colors uniformly scaled on a project circular base.
- **PayPal_business.png** — [source page](https://www.paypal.com/us/home); [asset/package](https://www.paypalobjects.com/marketing/web/logos/paypal-mark-color_new.svg). Source SHA-256 `8766a4211434d2c318fbfa412ea9633b385ecf1cab6119f8894019d91ed7e027`. Current official full-color P retained on light project base; distinct from the PayPal inverse theme.
- **ChatGPT.png** — [source page](https://openai.com/brand/); [asset/package](https://cdn.openai.com/brand/OpenAI-Logos-2025.zip). Source SHA-256 `7be72f1fea831d3ba81a545cee79b7e0ae69449d5d7837c9571ccbfb4aa1e00b`. Downloaded asset is officially named OpenAI monoblossom, used as the project ChatGPT identifier; current geometry retained.
- **Apple_TV.png** — [source page](https://www.apple.com/tv-pr/about/); [asset/package](https://www.apple.com/tv-pr/about-assets/images/logo/Apple_TV_Logo.zip). Source SHA-256 `a088da3efd0b723c9b75df64ec2dc87fef0c6251d2e0ad001efb078fe8bc6985`. Apple TV streaming-service press hero; only blank margins cropped before uniform scaling, no recoloring.
- **PayPal.png** — [source page](https://www.paypal.com/us/home); [asset/package](https://www.paypalobjects.com/marketing/web/logos/paypal-mark-color_new.svg). Source SHA-256 `8766a4211434d2c318fbfa412ea9633b385ecf1cab6119f8894019d91ed7e027`. Current native three-path P geometry; original project deep-blue/pale-white inverse theme retained. This adapted colorway is not claimed to be an official supplied inverse asset.

### Official media sources

- **HBO_MAX.png** — [source page](https://brand.hbomax.com/quick-downloads). Source SHA-256 `0816ebf9c87c9f4556996067f341542b9283a00e2fabc082a6d955a0366d3c0a`. Current downloadable stacked HBO/max logo, corroborated by current app artwork; conflicting older small-size website illustrations were not reconstructed.
- **Peacook.png** — [source page](https://apps.apple.com/us/app/peacock-tv-stream-tv-movies/id1508186374); [asset/package](https://is1-ssl.mzstatic.com/image/thumb/Purple211/v4/02/50/8f/02508fc6-59f4-fa16-893a-98d93f74af0a/AppIcon-0-0-1x_U007epad-0-1-0-85-220.png/512x512bb.jpg). Source SHA-256 `3003783eea993e2dade26254fc26978150eaf1e2c5d5ce216416ed421c066194`. Official current app P plus five gradient dots; spelling of the existing project URL retained. Old website favicon was not used.
- **Vimeo.png** — [source page](https://vimeo.com/press/media-kit); [asset/package](https://drive.google.com/uc?export=download&id=1gN9dRDamlsqXLfO3c0a3Ank2IgbA6VKY). Source SHA-256 `d7e143eb0e2d9e3cd33973e0eb35f60758574fedff9b1fd481daee25b50a6495`. Current official black V and official blue background family retained.
- **Video_Vimeo.png** — [source page](https://vimeo.com/press/media-kit); [asset/package](https://drive.google.com/uc?export=download&id=1eGJGw65ArkdbJPA2uR0Uzsal48zKFyNI). Source SHA-256 `5e7b8fdce2466c1883a73c461ebc0bf6adeaa0cad60f2874a24d52092c59f568`. Current official white V geometry on the original project orange/yellow/pink gradient; this theme remains distinct from main Vimeo blue.
- **YouTube.png** — [source page](https://brand.youtube/color/); [asset/package](https://www.gstatic.com/marketing-cms/78/29/3e68a1414bb28d0b7e47b44c3c91/youtube-icon.zip). Source SHA-256 `1027b1b0517727adb9697155a270744381c3ce9b047b1c8bd8a9389dc7d07a83`. Current digital red #FF0033 mark. This entry applies only to ordinary default/Large assets, not FDS.
- **Pixiv.png** — [source page](https://www.pixiv.co.jp/news/press-kit/); [asset/package](https://pixiv1.app.box.com/index.php?rm=box_download_shared_file&shared_name=yj9ymvhbnpcbj22vfkkzctugzv46cnos&file_id=f_1775154925561). Source SHA-256 `e8d77cf0712750580c5ad836aa6ea729fa57f7a400ed62aed209fe3f4ec23002`. Current service p icon, not the separate corporate wordmark. Native p path and blue retained; square source container adapted to circle.
- **Xbox.png** — [source page](https://www.xbox.com/); [asset/package](https://cms-assets.xboxservices.com/assets/bf/a7/bfa78b03-47f1-4113-94a0-0094e615a81a.svg?n=Favicon.svg). Source SHA-256 `eaa4f917a26b1287845f40d2ed34517cf753db2ad1a1c3f56563bb4a9a956d92`. Exact official 2000 px PNG extracted losslessly from the SVG container. Its dimensional appearance is current brand art, not a project glass redesign.

### Identity mapping and accepted lockup

- **X.png / Twitter.png:** [official X guidelines](https://about.x.com/content/dam/about-twitter/x/brand-toolkit/x-brand-guidelines.pdf), page 3 embedded 2004×2048 raster plus native alpha (not falsely called a vector extraction). Clean black/white project circle; obsolete Twitter URL maps to current X identity.
- **Bitcoin.png:** [Bitcoin.org](https://bitcoin.org/en/), [current header SVG](https://bitcoin.org/img/icons/logotop.svg?1792398050). Exact orange-disc/tilted-B paths separated from the lockup. This corrects the repository’s explicitly named Bitcoin identity; it is not a dated rebrand or a central trademark-authority claim.
- **Zoho_old.png → Zoho_new.png:** current accepted project compact mark, previously faithfully traced from the [official Zoho favicon](https://www.zohowebstatic.com/sites/zweb/images/favicon.ico). URL retained; not described as an official SVG download.
- **Prime.png:** [official whole prime + smile asset](https://m.media-amazon.com/images/G/01/digital/video/merch/subs/benefit-id/m-r/Prime/logos/channels-logo-white.png), source SHA-256 `8c4b0313ad4e42c709b4a542589d6a70af43dd6893491c4a752a874eecd4768a`. This is the Prime membership/benefit mark used by Prime Video, not the complete Prime Video wordmark. User accepted that scope; whole geometry, original blue base and optical placement retained. Rejected play triangle excluded.

### Original-theme protection and exclusions

- **Apple_rainbow.png:** both baseline files are byte-identical and excluded from this patch. Its original angular rainbow layout is user-created artwork, not an outdated-brand alias. The existing Apple silhouette matches current [Apple navigation](https://www.apple.com/) geometry (normalized mask overlap 0.99029); no needless re-render or background reconstruction.
- **Video_Vimeo / PayPal:** their original gradient and inverse-color themes are preserved as explicit project adaptations of current official geometry. Named themes are not collapsed into the canonical colorway.
- **FDS:** the entire 125×90 series is outside this round and remains byte-identical. No centering, circle conversion, recoloring, resizing or brand-update claim applies to it. Earlier FDS candidates are superseded, not deliverables.
- **Playstation_30th:** expressly named commemorative artwork remains distinct from the ordinary current corporate mark. Other named colorways, characters, service identities and functional variants remain distinct.

### Container-only and optical checks

- Nine noncircular ordinary defaults reuse their existing circular Large counterparts at 180px within 300px with 60px padding: Disney, Disney_Mickey, European_Union, Round_Robin, Yin_Yang, Flight, Auto_Link, Netflix_b and Failover. Twitter/Copilot intersections resolve to the current-brand outputs above.
- All 35 candidate or verified-original entries were inspected at actual 16/24/32/48 default-canvas sizes on light and dark plus native context. Geometry is uniformly scaled, never stretched to a common square. Long lockups retain complete identity and safe margins.
- PayPal inverse-color placement is adjusted separately from the business full-color version: 5px left and 7px up at Large relative to the prior candidate, accounting for the different contrast weight.
- At 16px default canvas the body is only 9.6px. Dense wordmark letters and fine details cannot be guaranteed readable; no generic unrelated symbol replaces the brand merely to claim clarity.

### Limits of source verification

- All 174 canonical pairs were visually audited. Unchanged preexisting artwork outside verified source coverage is not retrospectively labeled official or latest.
- Amazon 2025 refresh is confirmed but an appropriate verified compact asset was not finalized; the existing file is retained and not certified current. Microsoft_365 suite/app scope and Disney_Channel regional compact identity remain unresolved. No invented “official” substitutes.
- This is raster/source QA, not an interactive client-runtime test or a trademark-license grant.

Third-party brand assets are not relicensed as CC0. No open redistribution license covering all listed brands was verified; repository licensing does not confer third-party trademark rights.
