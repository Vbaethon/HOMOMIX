"""Native identity fixes: distinguish balance strategies and restore panda anatomy.

White mask geometry only. Production material remains centrally defined.
"""

def panda(ai=False):
    # Large black ears, tilted orbital patches, a white muzzle and a wide nose.
    # White below denotes positive mask/ink; black is a true cutout.
    outer = '<circle cx="107" cy="108" r="34" fill="white"/><circle cx="253" cy="108" r="34" fill="white"/>'
    outer += '<path d="M180 100C119 100 79 139 79 194C79 252 125 282 180 282C235 282 281 252 281 194C281 139 241 100 180 100Z" fill="white"/>'
    outer += '<path d="M180 121C132 121 101 151 101 195C101 238 134 261 180 261C226 261 259 238 259 195C259 151 228 121 180 121Z" fill="black"/>'
    outer += '<ellipse cx="139" cy="181" rx="27" ry="35" transform="rotate(28 139 181)" fill="white"/><ellipse cx="221" cy="181" rx="27" ry="35" transform="rotate(-28 221 181)" fill="white"/>'
    outer += '<circle cx="143" cy="174" r="10" fill="black"/><circle cx="217" cy="174" r="10" fill="black"/>'
    outer += '<path d="M166 216Q180 208 194 216Q201 220 194 227L185 235Q180 240 175 235L166 227Q159 220 166 216Z" fill="white"/>'
    if ai:
        # An integrated sparkle replaces the old leafy crest (which read as an owl).
        outer += '<path d="M180 61Q184 83 201 88Q184 93 180 112Q176 93 159 88Q176 83 180 61Z" fill="white"/>'
    return '<g transform="translate(0 -7)">'+outer+'</g>'

def adjust(name, defs, body):
    if name in ('Panda', 'Panda_ai'):
        body = panda(name == 'Panda_ai')
    elif name == 'Load_balancing_2':
        # Symmetric fan-out hub, not a duplicate of the left-to-right tree.
        body = '<g fill="none" stroke="white" stroke-width="30" stroke-linecap="round" stroke-linejoin="round"><path d="M180 106V167M180 167L107 240M180 167L253 240"/></g><circle cx="180" cy="101" r="29" fill="white"/><circle cx="180" cy="170" r="31" fill="white"/><rect x="75" y="221" width="64" height="53" rx="19" fill="white"/><rect x="221" y="221" width="64" height="53" rx="19" fill="white"/>'
    elif name == 'Load_balancing_3':
        # Equal balanced loads: thick beam and two broad, rounded trays.
        body = '<g fill="none" stroke="white" stroke-width="27" stroke-linecap="round" stroke-linejoin="round"><path d="M180 95V269M113 270H247M89 132H271M108 134L81 207M108 134L135 207M252 134L225 207M252 134L279 207"/></g><path d="M64 204H152Q150 244 108 244Q66 244 64 204ZM208 204H296Q294 244 252 244Q210 244 208 204Z" fill="white"/>'
    return defs, body
