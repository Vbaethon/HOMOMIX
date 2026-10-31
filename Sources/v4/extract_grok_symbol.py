from pathlib import Path
from PIL import Image,ImageFilter
import numpy as np
from collections import deque
R=Path(__file__).resolve().parent/'official';im=Image.open(R/'Grok.webp').convert('RGBA');a=np.array(im);m=(a[:,:,:3].mean(2)>30)&(a[:,:,3]>50);seen=np.zeros(m.shape,bool);parts=[]
for y,x in zip(*np.where(m)):
 if seen[y,x]:continue
 q=deque([(y,x)]);seen[y,x]=1;pts=[]
 while q:
  yy,xx=q.popleft();pts.append((yy,xx))
  for Y,X in [(yy-1,xx),(yy+1,xx),(yy,xx-1),(yy,xx+1)]:
   if 0<=X<im.width and 0<=Y<im.height and m[Y,X] and not seen[Y,X]:seen[Y,X]=1;q.append((Y,X))
 if len(pts)>5000:parts.append(pts)
assert len(parts)==2
mask=np.zeros(m.shape,dtype=np.uint8)
for pts in parts:
 for y,x in pts:mask[y,x]=255
# Include all anti-aliased dark fringe around the two unchanged silver components.
mask=np.array(Image.fromarray(mask).filter(ImageFilter.MaxFilter(9)))>0
out=a.copy();out[:,:,3]=np.where(mask,a[:,:,3],0);out[~mask,:3]=0
Image.fromarray(out).save(R/'Grok-symbol.png')
assert np.array_equal(out[mask,:3],a[mask,:3])
print('selected components',list(map(len,parts)),'source color pixels unchanged')
