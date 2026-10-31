# 全量光学尺寸独立QA

人工独立视觉QA：全量overview + 178张300×300默认PNG以60×60显示，实际内容盘约36px。建议值是相对当前主体的等比倍率，不是背景圆盘倍率；需在v5输出后复核。不是像素面积自动评分。

## 必须处理
- Zoho_new / Zoho_old当前同样式：必须分离正确官方来源，不能以尺寸差异冒充新旧版本。
- 不对官方圆形背景、国旗和全幅构图机械套用同一主体面积目标。
- 先缩放主体，维持锁定背景、阴影、原色与几何；横向字标不可改字或拉伸。
- 表中1.00表示已审查且当前适中，不代表漏项。用户要求全量适配时也应允许保持合理项目。

## 分类逐项建议

| 名称 | 分类 | 判断 | 主体倍率 |
|---|---|---|---|
| AI | 实心 | 偏小 | 1.05 |
| AI_Tree | 线形 | 适中 | 1.00 |
| AI_bot | 实心 | 偏小 | 1.05 |
| AI_voice | 线形 | 偏小 | 1.12 |
| ASIA | 线形 | 偏小 | 1.05 |
| Adblock | 实心 | 偏小 | 1.08 |
| AdblockPlus | 线形 | 适中 | 1.00 |
| AdblockPlus_2 | 实心 | 偏小 | 1.05 |
| Adguard | 实心 | 偏大 | 0.95 |
| Adobe | 实心 | 适中 | 1.00 |
| Amazon | 字标 | 适中 | 1.00 |
| Apple | 实心 | 适中 | 1.00 |
| Apple_TV | 字标 | 偏小 | 1.10 |
| Apple_black | 实心 | 适中 | 1.00 |
| Apple_rainbow | 实心 | 适中 | 1.00 |
| Auto_Link | 线形 | 偏小 | 1.12 |
| BT_Bittorrent | 线形 | 适中 | 1.00 |
| Bahamut | 线形 | 偏小 | 1.12 |
| Bahamut_b | 线形 | 偏小 | 1.12 |
| Bahamut_i | 线形 | 偏小 | 1.12 |
| Bilibili_Global | 线形 | 偏小 | 1.08 |
| Bilibili_blue | 线形 | 适中 | 1.00 |
| Binance | 实心 | 适中 | 1.00 |
| Bing | 实心 | 偏小 | 1.05 |
| Bitcoin | 实心 | 适中 | 1.00 |
| Bluesky | 实心 | 适中 | 1.00 |
| Bytedance | 实心 | 适中 | 1.00 |
| Calcifer | 实心 | 偏小 | 1.05 |
| Chained | 线形 | 偏小 | 1.05 |
| Chained_2 | 线形 | 偏小 | 1.05 |
| ChatGPT | 线形 | 适中 | 1.00 |
| China | 实心 | 适中 | 1.00 |
| China_Taipei | 线形 | 适中 | 1.00 |
| Claud | 实心 | 偏大 | 0.95 |
| Claude | 实心 | 偏大 | 0.95 |
| Cloud | 实心 | 偏小 | 1.08 |
| CloudFlare | 实心 | 偏小 | 1.10 |
| Consistent_Hashing | 线形 | 偏小 | 1.05 |
| Crypto | 线形 | 偏小 | 1.05 |
| DIRECT | 线形 | 偏小 | 1.12 |
| DeepSeek | 线形 | 偏小 | 1.12 |
| Discord | 实心 | 适中 | 1.00 |
| Disney | 线形 | 偏小 | 1.10 |
| Disney_Castle | 实心 | 适中 | 1.00 |
| Disney_Channel | 字标 | 偏小 | 1.15 |
| Disney_Mickey | 实心 | 适中 | 1.00 |
| Disney_plus | 线形 | 偏小 | 1.10 |
| Dolphin | 线形 | 偏小 | 1.05 |
| Douyin | 实心 | 适中 | 1.00 |
| Download | 线形 | 偏小 | 1.08 |
| Download_2 | 线形 | 偏小 | 1.08 |
| EPIC | 实心 | 适中 | 1.00 |
| Emby | 实心 | 偏小 | 1.05 |
| European_Union | 实心 | 适中 | 1.00 |
| F2C | 线形 | 适中 | 1.00 |
| FCM_Firebase_Cloud_Messaging | 实心 | 适中 | 1.00 |
| Facebook | 实心 | 适中 | 1.00 |
| Failover | 线形 | 适中 | 1.00 |
| Fast | 字标 | 偏小 | 1.10 |
| Fish | 实心 | 偏小 | 1.08 |
| Fish_b | 实心 | 偏小 | 1.05 |
| Fish_x | 实心 | 适中 | 1.00 |
| Flight | 线形 | 偏小 | 1.05 |
| Forbidden | 线形 | 适中 | 1.00 |
| GFW | 实心 | 偏大 | 0.95 |
| GOG | 字标 | 偏小 | 1.05 |
| Game | 实心 | 偏小 | 1.10 |
| Gemini | 线形 | 适中 | 1.00 |
| GitHub | 实心 | 适中 | 1.00 |
| Global | 线形 | 适中 | 1.00 |
| Globefish | 实心 | 偏小 | 1.08 |
| Gmail | 实心 | 偏大 | 0.92 |
| Google | 实心 | 偏大 | 0.97 |
| Grok | 线形 | 适中 | 1.00 |
| HBO_MAX | 字标 | 适中 | 1.00 |
| Home | 实心 | 偏小 | 1.08 |
| Hong_Kong | 实心 | 偏小 | 1.10 |
| Huawei | 实心 | 偏小 | 1.10 |
| Huawei_black | 实心 | 偏小 | 1.10 |
| Huawei_white | 实心 | 偏小 | 1.10 |
| Hugging_face | 实心 | 偏小 | 1.05 |
| Hugging_face_g | 实心 | 偏小 | 1.05 |
| Hulu | 字标 | 偏小 | 1.15 |
| Infuse | 线形 | 偏小 | 1.05 |
| Instagram | 线形 | 适中 | 1.00 |
| Japan | 实心 | 偏小 | 1.08 |
| Jellyfin | 线形 | 适中 | 1.00 |
| Link | 线形 | 偏小 | 1.05 |
| Linkedin | 实心 | 适中 | 1.00 |
| Linkedin_ray | 实心 | 适中 | 1.00 |
| Load_balancing | 线形 | 适中 | 1.00 |
| Load_balancing_2 | 线形 | 偏小 | 1.08 |
| Load_balancing_3 | 线形 | 偏小 | 1.10 |
| Location | 实心 | 偏小 | 1.05 |
| MLB | 实心 | 偏小 | 1.10 |
| Magic_Timer | 线形 | 偏小 | 1.05 |
| Mail | 实心 | 偏小 | 1.08 |
| Messenger | 实心 | 适中 | 1.00 |
| Meta_1 | 线形 | 适中 | 1.00 |
| Microsoft | 实心 | 偏大 | 0.97 |
| Microsoft_365 | 实心 | 偏小 | 1.05 |
| Microsoft_Copilot | 实心 | 适中 | 1.00 |
| NBA | 实心 | 偏小 | 1.08 |
| Netflix | 实心 | 适中 | 1.00 |
| Netflix_b | 实心 | 适中 | 1.00 |
| Network | 线形 | 适中 | 1.00 |
| Network_2 | 线形 | 适中 | 1.00 |
| Niche_Link | 线形 | 偏小 | 1.05 |
| Niconico | 线形 | 偏大 | 0.95 |
| Niconico_Live | 线形 | 偏小 | 1.05 |
| Niconico_Manga | 实心 | 适中 | 1.00 |
| Olympics | 线形 | 偏小 | 1.15 |
| Omission | 实心 | 适中 | 1.00 |
| OneDrive | 实心 | 适中 | 1.00 |
| Onlyfans | 线形 | 偏小 | 1.05 |
| Other | 实心 | 偏小 | 1.15 |
| Outlook | 实心 | 偏大 | 0.95 |
| Palestine | 实心 | 适中 | 1.00 |
| Panda | 线形 | 偏小 | 1.08 |
| Panda_WWF | 实心 | 偏小 | 1.05 |
| Panda_ai | 线形 | 偏小 | 1.08 |
| PayPal | 实心 | 适中 | 1.00 |
| PayPal_business | 实心 | 偏小 | 1.05 |
| Peacook | 实心 | 适中 | 1.00 |
| Perplexity | 线形 | 适中 | 1.00 |
| Pig | 实心 | 偏小 | 1.08 |
| Piggies | 实心 | 适中 | 1.00 |
| Piggies_b | 实心 | 适中 | 1.00 |
| Pixiv | 实心 | 适中 | 1.00 |
| Playstation | 实心 | 偏小 | 1.10 |
| Playstation_30th | 实心 | 偏小 | 1.05 |
| Playstation_remote | 线形 | 适中 | 1.00 |
| Plex | 实心 | 偏小 | 1.08 |
| Pornhub | 字标 | 适中 | 1.00 |
| Prime | 字标 | 偏小 | 1.15 |
| Qoura | 实心 | 适中 | 1.00 |
| Reddit | 实心 | 偏小 | 1.05 |
| Remote | 实心 | 适中 | 1.00 |
| Round_Robin | 线形 | 偏小 | 1.10 |
| SNS | 实心 | 适中 | 1.00 |
| Scholar | 实心 | 偏小 | 1.05 |
| Seancody | 字标 | 偏小 | 1.15 |
| Server | 实心 | 偏大 | 0.95 |
| Settings | 实心 | 偏小 | 1.08 |
| Signal_Light | 实心 | 偏小 | 1.12 |
| Singapore | 实心 | 适中 | 1.00 |
| Sony_Live | 字标 | 适中 | 1.00 |
| South_Korea | 实心 | 适中 | 1.00 |
| SpeedTest | 线形 | 适中 | 1.00 |
| Spotify | 实心 | 适中 | 1.00 |
| Steam | 实心 | 适中 | 1.00 |
| Stream | 线形 | 偏小 | 1.05 |
| Taiwan_Province | 线形 | 适中 | 1.00 |
| Telegram | 实心 | 适中 | 1.00 |
| Threads | 线形 | 适中 | 1.00 |
| Tick | 线形 | 适中 | 1.00 |
| Tick_2 | 线形 | 适中 | 1.00 |
| TikTok | 实心 | 偏小 | 1.05 |
| Transfer | 线形 | 适中 | 1.00 |
| Twitch | 实心 | 适中 | 1.00 |
| Twitter | 线形 | 适中 | 1.00 |
| UBISOFT | 线形 | 偏小 | 1.10 |
| UK | 实心 | 适中 | 1.00 |
| USA | 实心 | 适中 | 1.00 |
| Video_Vimeo | 实心 | 适中 | 1.00 |
| Vimeo | 实心 | 适中 | 1.00 |
| Weibo | 线形 | 适中 | 1.00 |
| WhatsApp | 线形 | 适中 | 1.00 |
| X | 线形 | 适中 | 1.00 |
| Xbox | 实心 | 适中 | 1.00 |
| Xianyu | 字标 | 偏小 | 1.15 |
| Yin_Yang | 线形 | 偏小 | 1.08 |
| YouTube | 实心 | 适中 | 1.00 |
| Zoho_new | 实心 | 偏小 | 1.05 |
| Zoho_old | 实心 | 偏小 | 1.05 |
| Zune | 线形 | 偏大 | 0.92 |
| bilibili | 线形 | 适中 | 1.00 |
| xHamster | 线形 | 偏小 | 1.05 |

## 实施复核
- 批量倍率是第一轮建议，非精密测量；输出后需再看实际36px主体。
- 放大超过1.10的横向图应优先检查左右安全距；若官方几何可能裁切，降低倍率而非裁图。
- 放大前后需保持DeepSeek已校正中心，不按几何bbox重新归中。
- 圆形底图与前景不能分离的官方素材，保留原构图或重新选择合规适配方式，不能直接把整个圆盘放大裁边。