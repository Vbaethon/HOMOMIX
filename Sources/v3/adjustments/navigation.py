"""Selective optical refinements; 360-native-unit coordinates, no palette changes.
Input is the approved white-V2 defs/body. Unknown names are unchanged.
No run-time assets, raster edits, or global rescaling.
"""
NOTES = {
 'Network': 'Outer ring and equator 28→32, meridian 26→30 native units. Fullness increases without changing the globe envelope or adding fine grids.',
 'Signal_Light': 'Pill height 104→116, y128→122, radius52→58; width and three 44-unit holes stay fixed. Adds 6 units of white above/below holes, avoiding a skinny horizontal capsule at 36px.',
 'Stream': 'Enclosing ring 28→32 only. Play triangle and generous negative clearance retained; no blind enlargement.',
 'Tick': 'Open check stroke34→38. Adds perceived weight to this sparse subject without scaling its span or disturbing the rounded join.',
 'Transfer': 'Arrow strokes30→32; top shaft y127→133 and bottom y233→227, including both arrowheads. Pair is 12 units more compact vertically while retaining a 27-unit arrowhead-to-opposite-shaft gap and a 62-unit shaft gap.',
 'Tick_2': 'Retained. Existing 28-unit ring/check balance leaves roughly20-unit critical inner clearance; thickening would sacrifice that clearance for little gain.',
 'Flight': 'Retained. Already cohesive broad rocket with one42-unit window. Separate flame clearance was explicitly repaired in V2 and remains readable; moving it inward risks fusion at36px.',
 'ASIA': 'Retained. Existing land/rim union is a single cohesive generalized silhouette; additional thickening would close ocean features.',
 'Global': 'Retained. Existing land/rim union is a single cohesive generalized silhouette, with broad ocean cutout; no fine islands or grids.',
 'Network_2': 'Retained. Existing Americas/rim union has two generous ocean cutouts; do not compress these or equalize geographic mass by blind scaling.'
}

def adjust(name, defs, body):
    if name == 'Network':
        body = body.replace('stroke-width="28"', 'stroke-width="32"').replace('stroke-width="26"', 'stroke-width="30"')
    elif name == 'Signal_Light':
        body = body.replace('x="57" y="128" width="246" height="104" rx="52"', 'x="57" y="122" width="246" height="116" rx="58"')
    elif name == 'Stream':
        body = body.replace('stroke-width="28"', 'stroke-width="32"')
    elif name == 'Tick':
        body = body.replace('stroke-width="34"', 'stroke-width="38"')
    elif name == 'Transfer':
        body = body.replace('M84 127H274M239 92L275 127L239 162', 'M84 133H274M239 98L275 133L239 168')
        body = body.replace('M276 233H86M121 198L85 233L121 268', 'M276 227H86M121 192L85 227L121 262')
        body = body.replace('stroke-width="30"', 'stroke-width="32"')
    return defs, body
