# Complex/special official mark handling

Implementation: `Sources/v6/special_official.py`, `render(name,scale,dx=0,dy=0)` -> PIL RGBA360.

## Provenance and extraction
See `Sources/v6/official-special/provenance.json` for exact official URLs and strategies.
- Steam: use three exact official SVG symbol paths as one complete circular emblem; do not invent an extension to the legacy cropped arm. Original light-gray fill preserved. The symbol is an official negative-space design and differs from the legacy positive white mechanical arm.
- Xbox: exact2000px transparent bitmap decoded from official favicon SVG. The SVG wrapper has a tiling pattern that can show duplicate slivers, so use its original embedded bitmap rather than wrapper. Complete source sphere preserved.
- Sony_Live: complete official rounded-square lockup, not separated lettering. Integrated background is part of the official asset. Place full artwork on a fixed black disc; do not clip SONY or cut away the colored sweep. It remains a complete-artwork exception, not a dishonest claim of independently scaling the internal letters.
- Apple: supplied official source is a flat gray mark on an opaque white social card, not the existing shaded black Apple. Preserve existing mark and recover background from clean outer ring instead. No replacement geometry or colors fabricated.
- Omission: original Edge-like sphere retained complete; identity semantics remain uncertain. No official source for this custom illuminated sphere was established. Recover original dark backing from outer ring and scale complete sphere, never split its internal blue swirls.

## Scale semantics
For Apple/Omission, scale applies relative to original360px input. For Steam/Xbox/Sony_Live official replacements, the complete asset occupies360×scale pixels at original aspect ratio. Current QA uses .86 for original-art marks and .72 for official replacements; these are demonstrations, not final optical scale decisions.

## QA and limits
`special-before.png` and `special-after.png` were directly viewed; after includes real36px versions. No original circle-edge clipping remains for the Xbox/Steam complete marks. Sony full wordmark/lockup is intact. Apple/Omission backing stays fixed while foreground shrinks. Five exact circle-alpha checks and two original-art identity checks passed (`special-tests.json`).

For Apple/Omission, fitting and matte are approximate raster recovery. No claim of recovering exact original layers; low-contrast differences<=2/255 are treated as noise. No added shadows. No production Icon files changed.
