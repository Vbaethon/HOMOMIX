"""Use original official backgrounds; transparent marks use the common white disk.

Brand artwork is not recolored, redrawn, thickened or given an inner shadow.
The common disk alone retains the approved soft shadow. Grok is the official
App Store raster icon, not a fabricated vector.
"""
from pathlib import Path
import base64, io, json, sys, xml.etree.ElementTree as E
from PIL import Image
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent/'v3'))
from material import filters

PLACEMENT = {
 'Gemini': (64,64,232,232),
 'DeepSeek': (80,90,236,181),
 'Grok': (30,30,300,300),
 'UBISOFT': (68,68,224,224),
 'Peacook': (0,0,360,360),
 'AdblockPlus_2': (66,66,228,228),
 'Microsoft': (67,67,226,226),
 'Disney_Channel': (52,130,256,105),
 'Disney': (5,5,350,350),
 'Disney_plus': (64,64,232,232),
 'Scholar': (30,30,300,300),
}

def vector(name, box):
    root = E.fromstring((ROOT/'official'/(name+'.svg')).read_bytes())
    for key,val in zip(['x','y','width','height'],box):root.set(key,str(val))
    return E.tostring(root,encoding='unicode')

OFFICIAL_BACKGROUNDS={'Grok','Peacook','Disney','Scholar'}

def raster(name, box):
    source = ROOT/'official/Grok-symbol.png' if name=='Grok' else ROOT/'official/Disney-company-original.png' if name=='Disney' else next(p for p in (ROOT/'official').glob(name+'.*') if p.suffix in ('.png','.webp'))
    im=Image.open(source).convert('RGBA')
    buf=io.BytesIO();im.save(buf,format='PNG')
    data=base64.b64encode(buf.getvalue()).decode()
    x,y,w,h=box
    return f'<image x="{x}" y="{y}" width="{w}" height="{h}" href="data:image/png;base64,{data}"/>'

def main():
    for name,box in PLACEMENT.items():
        if name=='Disney_Channel':
            im=Image.open(ROOT/'official'/(name+'.png'));w=box[2];h=w*im.height/im.width;box=(box[0],180-h/2,w,h)
        art=vector(name,box) if (ROOT/'official'/(name+'.svg')).exists() else raster(name,box)
        disk_filter=filters().split('<filter id="inkFinish"')[0]
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="360" height="360" viewBox="0 0 360 360"><defs>{disk_filter}<clipPath id="outerDisk"><circle cx="180" cy="180" r="180"/></clipPath></defs><g clip-path="url(#outerDisk)"><circle cx="180" cy="180" r="175" fill="#FFFFFF" filter="url(#diskShadow)"/>{art}</g></svg>'
        if name in OFFICIAL_BACKGROUNDS:
            bg={'Grok':'#000000','Peacook':'#181818','Disney':'#FAF9F6','Scholar':'#FFFFFF'}[name]
            svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="360" height="360" viewBox="0 0 360 360"><defs><clipPath id="officialCircle"><circle cx="180" cy="180" r="175"/></clipPath></defs><g clip-path="url(#officialCircle)"><circle id="official-background" cx="180" cy="180" r="175" fill="{bg}"/>{art}</g></svg>'
        (ROOT/'svg'/(name+'.svg')).write_text(svg+'\n')
    (ROOT/'names.txt').write_text('\n'.join(PLACEMENT)+'\n')

if __name__=='__main__':main()
