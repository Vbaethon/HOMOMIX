"""Hole topology diagnostics, native pixel references; never automatic optical alignment."""
from pathlib import Path
from collections import deque
import json,tempfile,subprocess,xml.etree.ElementTree as E
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent;NS={'s':'http://www.w3.org/2000/svg'};E.register_namespace('',NS['s'])
def enclosed_holes(raw):
 t=E.fromstring(raw);b=t.find('s:g',NS);fg=b.find('s:g',NS)
 for el in list(b):
  if el is not fg:b.remove(el)
 fg.attrib.pop('filter',None)
 with tempfile.TemporaryDirectory() as temp:
  p=Path(temp)/'fg.svg';p.write_bytes(E.tostring(t));o=Path(temp)/'fg.png';subprocess.run(['node',str(R/'render.cjs'),str(p),str(o)],check=True,capture_output=True)
  im=Image.open(o).convert('RGBA').resize((360,360),Image.Resampling.LANCZOS);white=np.array(im)[:,:,3]>=128
 visited=np.zeros((360,360),bool);holes=[]
 for y in range(360):
  for x in range(360):
   if white[y,x] or visited[y,x]:continue
   q=deque([(y,x)]);visited[y,x]=True;points=[];edge=False
   while q:
    yy,xx=q.popleft();points.append((yy,xx));edge|=yy in [0,359] or xx in [0,359]
    for ry,rx in [(yy-1,xx),(yy+1,xx),(yy,xx-1),(yy,xx+1)]:
     if 0<=ry<360 and 0<=rx<360 and not white[ry,rx] and not visited[ry,rx]:visited[ry,rx]=True;q.append((ry,rx))
   if not edge:
    ys,xs=zip(*points);holes.append({'area_native_px':len(points),'bbox':[min(xs),min(ys),max(xs)+1,max(ys)+1]})
 return holes
if __name__=='__main__':
 rows=[]
 for n in (R/'generic-names.txt').read_text().split():
  holes=enclosed_holes((R/'svg'/f'{n}.svg').read_bytes());rows.append({'name':n,'enclosed_negative_components':holes});print(n,holes)
 (R/'qa/interior-topology.json').write_text(json.dumps({'note':'Connected-component diagnostic is not a replacement for optical/small-size review. Curved shape tips may taper naturally; intentional feature dimensions are specified separately.','icons':rows},indent=2)+'\n')
