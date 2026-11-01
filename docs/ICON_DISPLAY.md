# 图标显示名称与小尺寸适用性

## 当前规范链接

主目录 `HOMOMIX.json` 和 README 图廊均指向当前生产 `Icon/Color` 文件。旧文件名仍是稳定下载地址，显示名称由根目录 `icon_metadata.json` 维护，不为纠正品牌名而破坏既有 URL。

- `F2C.png` 显示 **FC2**。
- `Cloud.png` 显示 **SoundCloud**。
- `Adobe.png` 显示 **Adobe Creative Cloud**。
- `Omission.png` 显示 **Microsoft Edge（Omission 策略）**：图形身份与原策略用途分开说明。
- 三款负载均衡各有完整语义名称；不再用共同的 `Load_balan...` 标签。

目录保留原 `name`、`url` 字段，另提供唯一 `id`、`canonical_name`、`variant`、`size`（PNG文件宽高，非感知主体面积）、`display_name`。名称不应用作跨尺寸主键。主目录只包含当前默认及 Large 两种尺寸，共344条；172款默认图在 README 展示。FDS 是第三个未完成系列，保留独立 [分类入口](../Icon/Color/FDS/README.md) 与现有两文件；不混入344条完整系列目录。全部图片链接都引用生产路径，不引用候选或历史源码中的PNG。

## 横向官方标识：保持真实，不假造紧凑版

2026-11-01 对官方来源补查：

- [Disney 官方媒体素材页](https://newsroom.disney.fr/photos/logo-disney-channel-png-7dd4-dc71f.html)提供 Disney Channel 字标。未找到可核实、可直接替换当前字标的独立紧凑 Channel 标识；Disney 的 D 与 Disney+ 的 D 不能冒充 Disney Channel。
- [IOC 官方五环介绍](https://www.olympics.com/ioc/olympic-rings)定义五环关系、比例和颜色版本。它不是可以为增加视觉分量随意重排、描粗的装饰图案。

这两款保持现有官方几何与像素，不夸大宣称36px时已与实心图标拥有相同视觉分量。README显式标记细标限制、保留完整品牌文字并提供Large链接；消费方应在小尺寸使用时显示名称，或选择较大展示。`small_size_note`随目录提供，便于面板作提示。此处是适用性处理，不是假称发现不存在的官方compact资源。

## 链路原创的定点修复

`Chained`、`Chained_2`、`Auto_Link`改为有明确穿插/开口的厚链环，不再用单个打孔胶囊表示链路。三环、双环、自动链接闪电各保留独立语义；统一渐变、阴影、圆盘不变，默认/大尺寸及兼容别名同步导出。几何只改这三款原创，不更改官方商标。
