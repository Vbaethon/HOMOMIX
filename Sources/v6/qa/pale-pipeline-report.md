# Legacy pale-background subject pipeline

## Result
`Sources/v6/raster_pale.py`: `render(name, scale, dx=0, dy=0)` returns RGBA 360×360. Scale is relative to the original `Sources/v5/input-large/{name}.png`; offsets are original-canvas pixels. It uniformly resamples the foreground, not the disc. Original alpha and circle boundary remain fixed. No Icon production outputs were edited.

46 legacy pale-background names supported. Existing v3/v4 SVGs are refused (Disney, Disney_Channel, Gemini, Scholar): the caller must use native transforms. Case-sensitive canonical names are read directly from classification, including `Bilibili_Global`.

## Separation
Bilateral outer-ring samples establish the neutral background. Most are flat white or a linear vertical pale-gray ramp. BT_Bittorrent is a confirmed non-linear vertical ramp with a bottom plateau: it uses smoothed observed row medians instead of an invented solid background. A soft difference matte separates colored/dark geometry; opaque subject colors are resampled directly without hue changes or unequal-axis stretch. Very faint background-level differences (<=2/255) are treated as quantization noise. Pale details near that threshold cannot be promised bit-exact after scaling; no stronger losslessness claim is made.

The original PNG background samples are retained wherever the matte is zero; removed subject areas reveal the reconstructed same-tone ramp, not white. Low-opacity edge contributions are separated by difference unpremultiplication. This is a raster matte pipeline, not new vector artwork or an exact recovered original authoring layer. Existing baked subject shading is retained; no new inner/outer shadow is injected here.

## QA
- `pale-before.jpg`: original 50-class contact sheet including four native exclusions.
- `pale-separation-representatives.png`: original vs foreground85% Amazon, Zoho_new, Adguard, Outlook, EPIC, xHamster, plus true36px examples. Viewed directly.
- `pale-all-after.png`: all46 rendered at85%, 92px and true36px. Viewed directly; no added white rims or pasted-disc seams observed.
- `pale-*.png`: individual360px diagnostic outputs at85%, **not final production scale decisions**.
- `pale-separation-stats.json`: every name, fit error, estimated background top/bottom, matte extent.
- `pale-tests.json`:46 passes for original identity at scale1, exact unchanged circle alpha, exact outer-ring pixels at85%, and unchanged alpha under dx/dy.
- `python Sources/v6/test_raster_pale.py` reproduces checks.

Caller still owns final per-name optical scales and final all-icon comparison. Google/Gmail/TikTok should follow the approved16-sample caller override. Zoho_old is a compatibility alias, not a separately advertised style.
