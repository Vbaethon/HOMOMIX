# Animal redraw QA

Authored native SVG geometry only, no image generation, tracing, or production overwrite.

- Source: `Sources/v5/animal_redesign.py`, compatible `adjust(name, defs, body)`.
- Preview: `before-after.png`; each pair before then after, 90px disc and actual 36px disc.
- `Fish_x` unchanged, explicitly excluded.
- Fish/Fish_b: one continuous body/tail silhouette each; 28-native eye. Fish is a horizontal plump oval with broad tail. Fish_b is a tall tropical body with swept dorsal/anal fins and shorter narrow tail; it is not a mirrored oval. Native Fish_b geometry revised after duplicate-direction feedback.
- Dolphin: continuous back, beak, flipper and tail; approximately 245-native overall width after uniform .92 fit. Eye ~22 native post-fit. Optical right/up adjustment is encoded in the same transform for body and cutout.
- Globefish: round inflated belly, short shoulder spines and side fins, no detached decorative pieces; two 28-native eye openings and 30x36 mouth. Width approximately 248 native.
- Original gradients, disk and centered-inner/offset-outer filters are byte-preserved by review renderer. Only subjectMask body is replaced and new hole mask appended.
- At36px, eyes and mouth remain open; fish tail joints are broad and continuous. Dolphin tail is deliberately simple and thick. Globefish reads rounder and less star-shaped than old.
- These are review candidates, not automatic acceptance of the user's subjective animal preference. Final visual review required before integration.
