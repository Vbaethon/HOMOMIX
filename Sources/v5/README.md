# v5 光学尺寸与重复样式修订

本层使用完整的 v6 候选源包作为输入，**不是只调整新添加的图标**。逐项检查177个现存默认名称及其Large配对；FDS历史小矩形版本独立保留。规范目录将四组同像素及一组微小色差兼容别名隐藏；Claud是明确授权删除的错误拼写。

## 光学规范

- 实际使用检视：默认300px画布显示为60px，其中圆盘约36px；同时看90px大图排查边缘。
- 一致的是感知主体尺寸，不是要求每个标识具有相同bbox或像素面积。
- 紧凑实心主体以约23–26px主要轮廓为起点；开放线形、细结构与不规则动物允许约24–28px；横向字标约27–30px宽。大面积圆形、方形、长字标分别校准；这是人工目标区间，不宣称所有指标机械落同一数值。
- 全套第一轮独立审查记录在`qa/independent-optical-review.json`。适中项目明确保留，不为凑“全部改动”无故重采样。
- 全部只等比缩放；不横向拉伸、不自造品牌几何、不靠加粗官方标志填面积。DeepSeek围绕已修正的视觉中心缩放，保留其官方路径与右移18的基础位置。
- 官方有色背景铺圆，无额外白圈。Grok只缩完整官方主体，黑底仍铺满圆盘。
- 泛用矢量图仅变换subjectMask内几何，内阴影2.6/12%、高光1.1/3%、外阴影dx7/dy11/blur13/11.5%均保持原生绝对值，不随主体缩放。
- 鱼、热带鱼、海豚、河豚四款重绘使用连续饱满轮廓；Fish_x为角色例外，不擅改。

## 输入与渲染

`input-original`为前一候选包生产图片的冻结回归快照，不是可选目录；其中历史Claud仅用于证明删除/旧包回归，生产目录已删除。`input-large`为传统PNG的原始360px采样源。v3/v4原生SVG与原始品牌资源不被覆盖。`svg`是新光学输出的自包含SVG。

- 有原生层的64项使用主体变换，底盘不变。
- 传统PNG没有原始分层向量：不伪称已恢复矢量。均匀采样原始整体内部图像；仅当缩小白底标识时在原图外部延续原有白色背景，圆盘位置/尺寸不变。主体像素保持原色、形状与比例；最终实际像素需独立逐张审查，不能凭指标自动通过。
- `measure_optical.py`的主体面积/质心是诊断，不等于美感分数。对复杂渐变、旗帜、满幅图的启发式分割明确低置信，不用于机械归一化。

重建：在安装v3依赖和Python Pillow/numpy后执行：
```
python Sources/v5/build_optical.py --output-dir /tmp/homomix-optical-rebuild
python Sources/v5/measure_optical.py --repo . --icon-root /tmp/homomix-optical-rebuild --output-dir /tmp/homomix-optical-metrics
```
旧v3/v4测试现在检查不可变前版本PNG快照；当前生产输出由`test_optical_revision.py`、全路径manifest、冷重建比对及独立视觉checklist验证。不能把历史snapshot测试当作当前渲染通过。

## 重复与兼容

五组重复/微差样式保留URL但不双重展示：Zoho_old→Zoho_new、Download_2→Download、Niche_Link→Chained_2、Twitter→X、Link→Chained_2。

Zoho的两个旧文件是同一个官方favicon，未发现可靠不同历史版本；不能以翻转、微调色彩假造“新旧”。明确不同官方底色/配色保留为配色变体，不声称几何造型不同。Claud默认/Large两个错名删除，Claude两个合法尺寸保留。

官方来源审计沿用v4的逐项证据及9项未完全确认限制；覆盖所有路径不等于所有品牌获得官方许可或完美像素溯源。
