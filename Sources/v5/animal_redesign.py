"""V5 native animal geometry. White mask only; palette and filters untouched.
Compatible with v3 adjust(name, defs, body). No image tracing or raster inputs.
"""
NAMES = ('Fish', 'Fish_b', 'Dolphin', 'Globefish')
SHAPES = {
 'Fish': ('M58 182C66 142 101 119 146 119C180 119 210 133 231 155C247 144 264 129 286 121Q301 116 298 132L288 181L298 230Q301 246 286 241C264 234 247 219 231 208C209 231 180 245 146 245C101 245 66 222 58 182Z', '<circle cx="106" cy="170" r="14" fill="black"/>'),
 'Fish_b': ('M300 181C291 148 270 123 240 111C224 88 203 75 182 77Q167 79 176 91L185 104C156 110 136 129 122 155L79 137Q61 130 65 149L73 181L65 213Q61 232 79 225L122 207C135 234 157 252 185 258L176 270Q167 283 183 284C207 284 230 267 245 246C273 231 291 207 300 181Z', '<circle cx="250" cy="169" r="14" fill="black"/>'),
 'Dolphin': ('M64 222C69 172 101 129 145 111C151 96 164 83 180 80Q192 78 188 90L184 104C218 104 246 119 263 140L291 151Q306 157 297 167Q293 172 280 170L261 168C253 181 239 192 224 199C215 208 211 222 208 239Q206 251 196 246C182 237 177 224 178 209C143 206 113 220 96 244C100 259 98 276 90 286Q83 295 77 284L67 263L44 270Q31 274 34 262C39 244 49 231 64 222Z', '<circle cx="244" cy="145" r="12" fill="black"/>'),
 'Globefish': ('M180 88C202 88 223 96 240 111L250 105Q262 99 260 113L258 133C269 147 276 163 278 180L294 184Q310 189 298 200L278 213C271 246 232 277 180 277C128 277 89 246 82 213L62 200Q50 189 66 184L82 180C84 163 91 147 102 133L100 113Q98 99 110 105L120 111C137 96 158 88 180 88Z', '<circle cx="143" cy="173" r="14" fill="black"/><circle cx="217" cy="173" r="14" fill="black"/><ellipse cx="180" cy="220" rx="15" ry="18" fill="black"/>')
}

def adjust(name, defs, body):
    if name not in SHAPES:
        return defs, body
    path, holes = SHAPES[name]
    # Dolphin's authored sweep is optically shifted right/up relative to its tail.
    transform=' transform="translate(20.4 11.4) scale(.92)"' if name=='Dolphin' else ''
    mask=f'{name}_v5_animal_mask'
    defs+=f'<mask id="{mask}" maskUnits="userSpaceOnUse" x="0" y="0" width="360" height="360"><rect width="360" height="360" fill="white"/><g{transform}>{holes}</g></mask>'
    body=f'<g mask="url(#{mask})"><path d="{path}" fill="white"{transform}/></g>'
    return defs, body

NOTES = {
 'Fish':'One continuous plump oval and softly rounded tail; no detached dorsal shard, one 28-unit eye.',
 'Fish_b':'High-bodied tropical fish: deep disc body, swept integrated dorsal/anal fins, short narrow tail; not a mirrored oval. One 28-unit eye.',
 'Dolphin':'Single curved back, integrated dorsal fin, rounded beak and broad flipper/tail; one 24-unit eye.',
 'Globefish':'Inflated rounded body with two short rounded shoulder spines and broad side fins; two 28-unit eyes and 30x36 mouth, no scattered dots.'
}
