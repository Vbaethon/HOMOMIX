"""Separate existing white marks from fixed colored backdrops.
Only observed white foreground is moved; hidden backdrop is harmonic interpolation,
not a claimed original layered official source. Transparent exterior is excluded
from the interpolation, avoiding black halos at the circular boundary.
"""
from pathlib import Path
from functools import lru_cache
import json
import numpy as np
from PIL import Image
from scipy.ndimage import binary_dilation, distance_transform_edt
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import cg
R=Path(__file__).resolve().parent
STRATEGIES=json.loads((R/'background-strategies.json').read_text())
NAMES={x['name'] for x in STRATEGIES['icons'] if x['classification'] in {'white_mark_flat_color_background','white_mark_gradient_background'}}-{'Steam'}
@lru_cache(None)
def layers(name):
 if name not in NAMES:raise ValueError(name)
 p=R.parent/'v5/input-large'/('Bilibili.png' if name=='bilibili' else name+'.png')
 if name=='Crypto':p=R/'official-special/Crypto-360.png'
 a=np.asarray(Image.open(p).convert('RGBA'),float);rgb=a[...,:3];valid=a[...,3]>200
 white=rgb.min(2)>190
 support=white&valid
 if name=='Crypto':
  yy,xx=np.mgrid[:360,:360];support&=(yy>30)&(yy<330)&(xx>35)&(xx<325)
 # Preserve source RGB including subtle shading; sample original AA boundary.
 dist=distance_transform_edt(~support);alpha=np.clip(2.0-dist,0,1);alpha[~valid]=0
 erased=binary_dilation(support,iterations=4)&valid
 bg=rgb.copy();coords=np.argwhere(erased);n=len(coords);ids=np.full((360,360),-1,int);ids[erased]=np.arange(n)
 rr=[];cc=[];dd=[];rhs=np.zeros((n,3));degree=np.zeros(n)
 for dy,dx in [(-1,0),(1,0),(0,-1),(0,1)]:
  yy=coords[:,0]+dy;xx=coords[:,1]+dx;ok=(yy>=0)&(yy<360)&(xx>=0)&(xx<360);ii=np.where(ok)[0];yy=yy[ok];xx=xx[ok];ok2=valid[yy,xx];ii=ii[ok2];yy=yy[ok2];xx=xx[ok2];degree[ii]+=1
  dest=ids[yy,xx];unknown=dest>=0
  rr.extend(ii[unknown]);cc.extend(dest[unknown]);dd.extend(np.full(unknown.sum(),-1.))
  rhs[ii[~unknown]]+=rgb[yy[~unknown],xx[~unknown]]
 rr.extend(np.arange(n));cc.extend(np.arange(n));dd.extend(degree)
 mat=csr_matrix((dd,(rr,cc)),shape=(n,n))
 for channel in range(3):
  val,info=cg(mat,rhs[:,channel],rtol=2e-6,maxiter=1400)
  if info!=0:raise RuntimeError(f'{name}: backdrop interpolation did not converge ({info})')
  bg[...,channel][erased]=np.clip(val,0,255)
 fg=Image.fromarray(np.dstack([rgb,np.rint(alpha*255)]).astype('uint8'))
 return a,bg,fg,{'name':name,'source':'Sources/v5/input-large/'+p.name,'background':'observed pixels fixed; harmonic reconstruction only under original white mark + AA margin','foreground_bbox':fg.getchannel('A').getbbox(),'no_transparent_rgb_in_interpolation':True}
def render(name,scale,dx=0,dy=0):
 a,bg,fg,meta=layers(name)
 if scale==1 and dx==0 and dy==0:return Image.fromarray(a.astype('uint8'))
 size=round(360*scale);mark=fg.resize((size,size),Image.Resampling.LANCZOS)
 out=Image.fromarray(np.dstack([np.rint(bg),np.full((360,360),255)]).clip(0,255).astype('uint8'));out.alpha_composite(mark,(round((360-size)/2+dx),round((360-size)/2+dy)))
 arr=np.asarray(out).copy();arr[...,3]=a[...,3].astype('uint8');arr[arr[...,3]==0]=0
 return Image.fromarray(arr)
