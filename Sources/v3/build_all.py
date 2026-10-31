#!/usr/bin/env python3
"""Offline export from self-contained SVGs; writes only --output-dir.

python3 Sources/v3/build_all.py --output-dir /tmp/homomix-rebuild --verify
Requires Python 3.10+, Pillow 11.3.0, Node.js and npm ci in Sources/v3.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import io
import json
import math
from pathlib import Path
import platform
import subprocess
import tempfile
import xml.etree.ElementTree as ET

from PIL import Image

ROOT=Path(__file__).resolve().parent


def sha(raw):return hashlib.sha256(raw).hexdigest()


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output-dir',required=True,type=Path)
    p.add_argument('--verify',action='store_true')
    p.add_argument('--jobs',type=int,default=2)
    a=p.parse_args()
    if not 1<=a.jobs<=8:raise ValueError('jobs must be 1..8')
    names=(ROOT/'names.txt').read_text().split()
    expected={}
    if a.verify:
        expected={r['path']:r for r in json.loads((ROOT/'render-manifest.json').read_text())['assets']}
        if len(expected)!=len(names)*2:raise ValueError('Incomplete expected manifest')
    a.output_dir.mkdir(exist_ok=True,parents=True)
    def render(name):
        source=ROOT/'svg'/(name+'.svg');raw=source.read_bytes();digest=sha(raw)
        for el in ET.fromstring(raw).iter():
            if el.tag.endswith('text'):raise ValueError(name+': production font dependency')
            for k,v in el.attrib.items():
                if k.endswith('href') and not v.startswith(('data:image/','#')):raise ValueError(name+': external SVG dependency')
        rows=[]
        with tempfile.TemporaryDirectory(prefix='homomix-render-') as tmp:
            master=Path(tmp)/'master.png'
            subprocess.run(['node',str(ROOT/'render.cjs'),str(source),str(master)],check=True,capture_output=True)
            hi=Image.open(master).convert('RGBA');hi.info={}
            if hi.size!=(1440,1440):raise ValueError(name+': wrong master size')
            for large in [False,True]:
                if large:im=hi.resize((360,360),Image.Resampling.LANCZOS)
                else:
                    im=Image.new('RGBA',(300,300));im.alpha_composite(hi.resize((180,180),Image.Resampling.LANCZOS),(60,60))
                # Do not keep invisible RGB noise at fully transparent pixels.
                pixels=im.load()
                center=180 if large else 150
                radius=180 if large else 90
                for y in range(im.height):
                    for x in range(im.width):
                        red,green,blue,alpha=pixels[x,y]
                        # Lanczos can create faint disconnected rings outside an
                        # otherwise exact circle. Limit alpha to its analytic
                        # one-pixel coverage rather than retaining those specks.
                        coverage=max(0,min(1,radius+.5-math.hypot(x+.5-center,y+.5-center)))
                        alpha=min(alpha,round(coverage*255))
                        pixels[x,y]=(red,green,blue,alpha) if alpha else (0,0,0,0)
                im.info={};buf=io.BytesIO();im.save(buf,format='PNG',optimize=False)
                data=buf.getvalue();rel='Icon/Color/'+('Large/' if large else '')+name+'.png'
                row={'name':name,'path':rel,'new_sha256':sha(data),'native_source':'Sources/v3/svg/'+name+'.svg','native_source_sha256':digest,'master':[1440,1440],'dimensions':list(im.size),'body':[360,360] if large else [180,180],'offset':[0,0] if large else [60,60],'alpha_bbox':list(im.getchannel('A').getbbox()),'bytes':len(data)}
                if a.verify:
                    ex=expected[rel]
                    for key in ['new_sha256','native_source_sha256','dimensions','alpha_bbox']:
                        if row[key]!=ex[key]:raise ValueError(rel+': '+key+' differs from frozen reconstruction')
                target=a.output_dir/rel;target.parent.mkdir(exist_ok=True,parents=True);target.write_bytes(data);rows.append(row)
        return rows
    with ThreadPoolExecutor(max_workers=a.jobs) as pool:
        assets=[r for group in pool.map(render,names) for r in group]
    report={'status':'pass','verified':a.verify,'names':len(names),'png':len(assets),'environment':{'python':platform.python_version(),'pillow':Image.__version__,'resvg-js':'2.6.2','node':subprocess.check_output(['node','--version'],text=True).strip()},'assets':sorted(assets,key=lambda r:r['path'])}
    (a.output_dir/'reproduction-report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='assets'}))


if __name__=='__main__':main()
