"""Selective native optical refinement for the approved inverse animal set.

Input is the original white subject, before the integrator applies color/shadow.
All units refer to the 360-unit SVG grid. No blanket normalization is applied.
"""
NAMES = ('Dolphin', 'Fish', 'Fish_b', 'Globefish', 'Panda', 'Panda_ai', 'Yin_Yang')
NOTES = {
 'Dolphin': 'Retained: the existing 0.94 optical fit already compacts the diagonal arch/tail without weakening its 24.44-unit effective eye. Do not normalize its long silhouette to the panda head bounding box.',
 'Fish': 'Translate down 5 native units only: the dorsal fin makes the compact oval sit high against the accepted Pig. No scaling, so the 26-unit eye and generous tail/body junction remain intact.',
 'Fish_b': 'Retained: tall sail-tail plus lower fin already balance vertically; its pointed outline intentionally differs from the compact Fish.',
 'Globefish': 'Retained: one connected plump body, sparse large spines and balanced side fins. Its 188-unit core avoids an oversized head; 26-unit eyes and 24x30-unit mouth remain unchanged.',
 'Panda': 'Retained relative to Pig: 222-unit head width versus Pig 222, with rounded ears integrated into the contour. Broad eye patches, 24-unit pupils and 20-unit meaningful surrounding gaps remain intact.',
 'Panda_ai': 'Compact only the external leaf crest: keep its base connection unchanged but lower the high leaf tips by 9 native units (roughly 0.9px at default body36). The face, ears, eye patches and 24-unit pupils are untouched; less detached-looking top accent, same nature identity.',
 'Yin_Yang': 'Retained: circular 242-unit outer diameter intentionally compensates the half-negative interior. Scaling to a filled animal head would make the 26-unit ring and 30-unit dots unnecessarily weak.',
}
_OLD_LEAF = 'M179 119C158 106 150 82 154 61Q157 53 164 60C178 71 186 84 188 98C192 80 203 69 219 65Q228 63 224 73C218 93 207 108 190 119Z'
_NEW_LEAF = 'M179 119C160 109 153 89 156 70Q159 62 166 69C179 79 186 90 188 102C193 86 203 77 218 74Q226 72 222 82C216 99 205 111 190 119Z'

def adjust(name, defs, body):
    if name == 'Fish':
        return defs, '<g transform="translate(0 5)">' + body + '</g>'
    if name == 'Panda_ai':
        if _OLD_LEAF not in body:
            raise ValueError('Panda_ai source differs from approved original leaf; refusing silent partial adjustment')
        return defs, body.replace(_OLD_LEAF, _NEW_LEAF, 1)
    return defs, body
