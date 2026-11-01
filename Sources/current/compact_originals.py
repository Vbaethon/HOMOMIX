"""Compact, filled native originals. Geometry-only adjust interface.
No gradients, filters, official identities, or production files are altered.
Coordinates directly target ~240–250 native span inside fixed360 disk.
"""
NAMES=('Load_balancing','Load_balancing_2','Load_balancing_3','AI_Tree','AI_voice','Network','Round_Robin','Chained_2')
SHAPES={
'Load_balancing':('''<rect x="60" y="78" width="240" height="204" rx="48" fill="white"/>''','''<path d="M96 164H128V141Q128 133 136 138L178 172Q187 180 178 188L136 222Q128 227 128 219V196H96Q87 196 87 187V173Q87 164 96 164Z" fill="black"/><rect x="211" y="118" width="50" height="42" rx="12" fill="black"/><rect x="211" y="200" width="50" height="42" rx="12" fill="black"/>'''),
'Load_balancing_2':('''<path d="M103 104Q103 81 126 81H234Q257 81 257 104V133H280Q301 133 301 154V249Q301 278 272 278H88Q59 278 59 249V154Q59 133 80 133H103Z" fill="white"/>''','''<rect x="142" y="117" width="76" height="41" rx="12" fill="black"/><rect x="96" y="198" width="62" height="43" rx="12" fill="black"/><rect x="202" y="198" width="62" height="43" rx="12" fill="black"/>'''),
'Load_balancing_3':('''<path d="M159 111Q159 90 180 90Q201 90 201 111V132H283Q301 132 300 150L296 182Q292 222 248 227H201V248H254Q273 248 273 267Q273 283 254 283H106Q87 283 87 267Q87 248 106 248H159V227H112Q68 222 64 182L60 150Q59 132 77 132H159Z" fill="white"/>''','''<path d="M93 162H150L143 187Q138 199 122 199Q106 199 101 187Z" fill="black"/><path d="M210 162H267L259 187Q254 199 238 199Q222 199 217 187Z" fill="black"/>'''),
'AI_Tree':('''<path d="M180 81C160 63 126 73 118 97C88 94 67 119 73 147C50 169 54 203 76 218C69 247 95 271 122 267C134 293 163 294 180 277C197 294 226 293 238 267C265 271 291 247 284 218C306 203 310 169 287 147C293 119 272 94 242 97C234 73 200 63 180 81Z" fill="white"/>''','''<rect x="166" y="110" width="28" height="143" rx="14" fill="black"/><path d="M114 129Q121 123 128 129L151 152Q157 160 150 168Q142 174 135 167L112 145Q106 137 114 129ZM246 129Q239 123 232 129L209 152Q203 160 210 168Q218 174 225 167L248 145Q254 137 246 129ZM108 208Q108 195 121 195H144Q157 195 157 208Q157 221 144 221H121Q108 221 108 208ZM203 208Q203 195 216 195H239Q252 195 252 208Q252 221 239 221H216Q203 221 203 208Z" fill="black"/>'''),
'AI_voice':('''<path d="M105 81H255Q300 81 300 126V220Q300 265 255 265H149L113 287Q103 293 103 280V264Q60 261 60 220V126Q60 81 105 81Z" fill="white"/>''','''<rect x="100" y="151" width="28" height="50" rx="14" fill="black"/><rect x="144" y="125" width="28" height="102" rx="14" fill="black"/><rect x="188" y="112" width="28" height="128" rx="14" fill="black"/><rect x="232" y="144" width="28" height="64" rx="14" fill="black"/>'''),
'Network':('''<circle cx="180" cy="180" r="121" fill="white"/>''','''<path d="M167 94C146 109 135 133 132 162H94C99 129 128 102 167 94ZM193 94C214 109 225 133 228 162H266C261 129 232 102 193 94ZM94 198H132C135 227 146 251 167 266C128 258 99 231 94 198ZM228 198H266C261 231 232 258 193 266C214 251 225 227 228 198Z" fill="black"/>'''),
'Round_Robin':('''<path d="M249 90L277 65Q287 56 290 70L307 145Q310 158 296 159L218 161Q204 161 213 150L237 124C218 107 197 101 174 105C137 111 111 143 111 180C111 221 142 253 181 253C207 253 229 240 243 219Q251 207 263 213L283 223Q294 230 287 242C265 278 226 299 181 299C113 299 61 247 61 180C61 113 109 61 175 59C203 58 230 69 249 90Z" fill="white"/>''',''),
'Chained_2':('''<g transform="rotate(-40 180 180)"><rect x="56" y="107" width="248" height="146" rx="70" fill="white"/></g>''','''<g transform="rotate(-40 180 180)"><rect x="91" y="148" width="60" height="64" rx="27" fill="black"/><rect x="209" y="148" width="60" height="64" rx="27" fill="black"/></g>''')
}

def adjust(name, defs, body):
    if name not in SHAPES:return defs,body
    ink,holes=SHAPES[name]
    # Brain compensates broad lobes; all foreground is compactly centered.
    trans='translate(7.2 7.2) scale(.96)' if name=='AI_Tree' else 'translate(0 -6)' if name=='Load_balancing_3' else 'translate(0 -4)' if name=='AI_voice' else ''
    mask=name+'_compact_v6'
    defs+=f'<mask id="{mask}" maskUnits="userSpaceOnUse" x="0" y="0" width="360" height="360"><rect width="360" height="360" fill="white"/>{holes}</mask>'
    body=f'<g transform="{trans}"><g mask="url(#{mask})">{ink}</g></g>'
    return defs,body

# Second batch: semantic consolidated silhouettes, not universal square badges.
BATCH2=('Auto_Link','Chained','DIRECT','Transfer','Failover','SNS','Other','Server','Download','Download_2','GFW','Consistent_Hashing')
SHAPES.update({
'Auto_Link':('''<g transform="rotate(-38 180 180)"><rect x="57" y="111" width="246" height="138" rx="65" fill="white"/></g>''','''<g transform="rotate(-38 180 180)"><ellipse cx="112" cy="180" rx="20" ry="26" fill="black"/><ellipse cx="248" cy="180" rx="20" ry="26" fill="black"/><path d="M183 133L157 184Q154 191 162 191H176L172 226L204 175Q208 169 199 169H184L192 136Q193 130 183 133Z" fill="black"/></g>'''),
'Chained':('''<g transform="rotate(-40 180 180)"><rect x="55" y="114" width="250" height="132" rx="62" fill="white"/></g>''','''<g transform="rotate(-40 180 180)"><rect x="87" y="157" width="42" height="46" rx="19" fill="black"/><rect x="159" y="157" width="42" height="46" rx="19" fill="black"/><rect x="231" y="157" width="42" height="46" rx="19" fill="black"/></g>'''),
'DIRECT':('''<path d="M78 137H180V106Q180 91 192 100L294 170Q307 180 294 190L192 260Q180 269 180 254V223H78Q59 223 59 204V156Q59 137 78 137Z" fill="white"/>''',''),
'Transfer':('''<path d="M80 110H218V88Q218 77 228 84L294 130Q305 138 294 146L228 192Q218 199 218 188V166H80Q60 166 60 138Q60 110 80 110Z" fill="white"/><path d="M280 194H142V172Q142 161 132 168L66 214Q55 222 66 230L132 276Q142 283 142 272V250H280Q300 250 300 222Q300 194 280 194Z" fill="white"/><rect x="142" y="149" width="76" height="62" fill="white"/>''',''),
'Failover':('''<path d="M180 66Q232 95 282 101Q299 103 297 121L287 198Q278 257 180 295Q82 257 73 198L63 121Q61 103 78 101Q128 95 180 66Z" fill="white"/>''','''<path d="M112 143V197Q112 224 139 224H221Q248 224 248 197V153" fill="none" stroke="black" stroke-width="28" stroke-linecap="round"/><path d="M214 163L240 127Q248 116 256 127L282 163Q288 173 277 173H219Q208 173 214 163Z" fill="black"/><path d="M101 113L123 135M123 113L101 135" stroke="black" stroke-width="15" stroke-linecap="round"/>'''),
'SNS':('''<circle cx="180" cy="108" r="32" fill="white"/><circle cx="109" cy="139" r="27" fill="white"/><circle cx="251" cy="139" r="27" fill="white"/><rect x="151" y="129" width="58" height="80" rx="20" fill="white"/><rect x="87" y="157" width="44" height="57" rx="15" fill="white"/><rect x="229" y="157" width="44" height="57" rx="15" fill="white"/><rect x="60" y="182" width="240" height="93" rx="36" fill="white"/>''','''<rect x="133" y="188" width="22" height="55" rx="11" fill="black"/><rect x="205" y="188" width="22" height="55" rx="11" fill="black"/>'''),
'Other':('''<path d="M180 76C111 76 59 119 59 174C59 216 88 248 130 263L115 284Q109 294 122 291L174 273C244 276 301 231 301 174C301 119 249 76 180 76Z" fill="white"/>''','''<circle cx="113" cy="174" r="18" fill="black"/><circle cx="180" cy="174" r="18" fill="black"/><circle cx="247" cy="174" r="18" fill="black"/>'''),
'Server':('''<rect x="71" y="60" width="218" height="240" rx="42" fill="white"/>''','''<rect x="108" y="105" width="144" height="28" rx="14" fill="black"/><rect x="108" y="166" width="144" height="28" rx="14" fill="black"/><rect x="108" y="227" width="144" height="28" rx="14" fill="black"/>'''),
'Download':('''<path d="M164 64H196Q211 64 211 79V157H242Q254 157 246 167L192 230Q180 244 168 230L114 167Q106 157 118 157H149V79Q149 64 164 64Z" fill="white"/><path d="M77 204Q59 204 59 222V265Q59 294 88 294H272Q301 294 301 265V222Q301 204 283 204Q265 204 265 222V252H198V227H162V252H95V222Q95 204 77 204Z" fill="white"/>''',''),
'Download_2':('''<path d="M164 64H196Q211 64 211 79V157H242Q254 157 246 167L192 230Q180 244 168 230L114 167Q106 157 118 157H149V79Q149 64 164 64Z" fill="white"/><path d="M77 204Q59 204 59 222V265Q59 294 88 294H272Q301 294 301 265V222Q301 204 283 204Q265 204 265 222V252H198V227H162V252H95V222Q95 204 77 204Z" fill="white"/>''',''),
'GFW':('''<path d="M75 82H115Q126 82 126 93V120H151V93Q151 82 162 82H198Q209 82 209 93V120H234V93Q234 82 245 82H285Q296 82 296 93V260Q296 282 274 282H86Q64 282 64 260V93Q64 82 75 82Z" fill="white"/>''','''<path d="M103 176H171V153Q171 144 180 150L232 191Q240 198 232 205L180 246Q171 252 171 243V220H103Q93 220 93 210V186Q93 176 103 176Z" fill="black"/>'''),
'Consistent_Hashing':('''<circle cx="180" cy="180" r="120" fill="white"/>''','''<path d="M159 116L140 244M220 116L201 244M119 151H246M111 209H238" fill="none" stroke="black" stroke-width="26" stroke-linecap="round" stroke-linejoin="round"/>''')
})
NAMES=NAMES+BATCH2

BATCH3=('Magic_Timer','Stream','Tick_2')
SHAPES.update({
'Magic_Timer':('''<rect x="150" y="58" width="60" height="46" rx="18" fill="white"/><circle cx="180" cy="190" r="108" fill="white"/>''','''<path d="M187 110L134 191Q126 202 141 202H171L162 258Q160 269 170 258L229 174Q237 163 223 163H191L199 116Q201 104 187 110Z" fill="black"/>'''),
'Stream':('''<circle cx="180" cy="180" r="121" fill="white"/>''','''<path d="M151 117Q139 110 139 124V236Q139 250 151 243L238 192Q252 184 238 176Z" fill="black"/>'''),
'Tick_2':('''<circle cx="180" cy="180" r="121" fill="white"/>''','''<path d="M118 178L162 222L245 137" fill="none" stroke="black" stroke-width="34" stroke-linecap="round" stroke-linejoin="round"/>''')
})
NAMES=NAMES+BATCH3

# Audit refinement: retain thick connected silhouettes, but show real interlocking
# link openings rather than a single filled capsule perforated with round holes.
SHAPES.update({
    'Chained_2': ('''<g transform="translate(60 60) scale(10)" fill="none" stroke="white" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07L11.75 5.18"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></g>''', ''),
    'Chained': ('''<g transform="rotate(-35 180 180)" fill="none" stroke="white" stroke-width="32" stroke-linecap="round" stroke-linejoin="round"><path d="M130 132H106a48 48 0 0 0 0 96h24"/><path d="M230 132h24a48 48 0 0 1 0 96h-24"/><rect x="130" y="132" width="100" height="96" rx="48"/><path d="M112 180h38M210 180h38"/></g>''', ''),
    'Auto_Link': ('''<g transform="translate(60 60) scale(10)" fill="none" stroke="white" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"><path d="M8.2 15.8l-1.1 1.1a3.7 3.7 0 0 1-5.2-5.2l4.2-4.2a3.7 3.7 0 0 1 5.2 0"/><path d="M15.8 8.2l1.1-1.1a3.7 3.7 0 0 1 5.2 5.2l-4.2 4.2a3.7 3.7 0 0 1-5.2 0"/></g><path d="M190 109L139 181Q132 191 146 191H174L164 248Q162 257 172 248L222 176Q229 166 215 166H188L198 114Q200 105 190 109Z" fill="white"/>''', '')
})
