"""Minimal, optically judged compactness refinements on the native 360 grid.
No backgrounds/shadows or global scaling. Unknown and retained names pass through.
Foreground remains white for the integrator's final inverse treatment.
"""
import math

NAMES = 'AI AI_Tree AI_bot AI_voice Adblock Consistent_Hashing DIRECT Failover Forbidden GFW Home Location Magic_Timer Mail Other Remote Round_Robin SNS'.split()

def _circle(x,y,r):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFFFFF"/>'

def _rect(x,y,w,h,r):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="#FFFFFF"/>'

def adjust(name, defs, body):
    if name == 'AI_Tree':
        # Keep existing 24-diameter central mask opening and 22-unit white ring.
        branches = []
        for angle in [-90,-30,30,90,150,210]:
            x=180+86*math.cos(math.radians(angle))
            y=180+86*math.sin(math.radians(angle))
            branches.append(f'<path d="M180 180L{x:.3f} {y:.3f}" fill="none" stroke="#FFFFFF" stroke-width="26" stroke-linecap="round"/>')
            branches.append(_circle(f'{x:.3f}',f'{y:.3f}',24))
        body=f'<g mask="url(#AI_Tree_interior)">'+''.join(branches)+_circle(180,180,34)+'</g>'
    elif name == 'AI_voice':
        # Same five-bar identity and 28-unit widths; gaps 22 -> 20, not scaling.
        body=''.join(_rect(x-14,180-h/2,28,h,14) for x,h in [(84,52),(132,100),(180,156),(228,100),(276,52)])
    elif name == 'SNS':
        # Outer figures move inward six; bodies narrow four, preserving 22 gaps.
        body=_circle(180,108,28)+_circle(90,137,23)+_circle(270,137,23)
        body+=_rect(142,161,76,116,30)+_rect(60,184,60,66,24)+_rect(240,184,60,66,24)
        body='<g transform="translate(0 -7)">'+body+'</g>'
    elif name == 'Other':
        # Short ellipsis is deliberately not inflated to square-icon height.
        body=''.join(_circle(x,180,27) for x in [100,180,260])
    return defs,body

NOTES={
'AI_Tree':'Refine: terminal radius 22→24; spoke length 96→86 and width 24→26. Overall diameter 236→220; stronger hub cohesion. Central 24-unit hole and 22-unit white ring preserved. No global scale.',
'AI_voice':'Refine: five 28-wide bars retained; gaps 22→20; total width 228→220. Heights 54/108/164/108/54→52/100/156/100/52. Compact rhythm without shrinking width or losing minimum gaps.',
'SNS':'Refine: side centers 84/276→90/270; side widths 64→60, central width 84→76. Overall width 256→240. Body gaps stay 22; head-to-body gaps 24/25 retained; optical upward 7 retained.',
'Other':'Refine: dot centers 92/180/268→100/180/260; diameter 54 unchanged. Gaps 34→26; total width 230→214. Intentional wide/short ellipsis optical exception: no giant dots or enclosure.',
'AI':'Retain: connected head, ear and antenna mass is already cohesive; eye openings 28×44 remain robust.',
'AI_bot':'Retain: one rounded speech mass, 28×46 eyes; existing optical downward 5.',
'Adblock':'Retain: single compact shield, generous 100×28 negative minus.',
'Consistent_Hashing':'Retain: cohesive stopwatch ring/crown, 32 stroke; separated hand is essential and spacious.',
'DIRECT':'Retain: input node merges into arrow shaft; intentional horizontal optical exception.',
'Failover':'Retain: U-route is connected; cross is meaningful failure indicator, not decorative scatter.',
'Forbidden':'Retain: balanced continuous ring and diagonal, 32 width.',
'GFW':'Retain: regular 2×3 wall blocks already have only 20/24-unit gaps; further packing would compromise negative spaces. Arrow is essential directional modifier.',
'Home':'Retain: substantial connected silhouette with 48-wide open doorway.',
'Location':'Retain: single pin mass with 68-diameter opening; no packing needed.',
'Magic_Timer':'Retain: compact crown/ring, interior lightning remains separated to preserve legibility.',
'Mail':'Retain: single envelope mass, broad 24-wide negative chevron.',
'Remote':'Retain: four directional heads form one tight symmetric cluster with purposeful central negative space.',
'Round_Robin':'Retain: continuous circular route and substantial head, existing optical left 6.'
}
