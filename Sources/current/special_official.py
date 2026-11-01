"""Complete official Steam/Xbox/Sony LIV marks, and conservative original-art
separation for Apple/Omission. No production writes. scale relative to original
360px canvas (complete replacement artwork occupies 360px at scale1).
"""
from pathlib import Path
from functools import lru_cache
import numpy as np
from PIL import Image
from scipy.ndimage import map_coordinates,gaussian_filter1d
ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/'Sources/current/official/special'
@lru_cache(None)
def layers(name):
    a=np.array(Image.open(ROOT/'Sources/current/assets/original-raster'/f'{name}.png').convert('RGBA'),float)
    yy,xx=np.mgrid[:360,:360];x=(xx-179.5)/180;y=(yy-179.5)/180;r=np.hypot(x,y)
    if name in ('Xbox','Sony_Live','Steam'):
        fg=Image.open(DATA/f'{name}.png').convert('RGBA')
        # Full official artwork, no recropped negative-space mechanical stem.
        if name=='Xbox':bg=np.full((360,360,3),255.)
        elif name=='Sony_Live':bg=np.zeros((360,360,3))
        else:
            rgb=a[:,:,:3];mask=(r>.84)&(r<.96)&(a[:,:,3]>250)&(rgb.max(2)<210)
            row=np.full((360,3),np.nan)
            for iy in range(360):
                if mask[iy].sum()>3:row[iy]=np.median(rgb[iy][mask[iy]],axis=0)
            valid=np.isfinite(row[:,0]);row=np.stack([np.interp(np.arange(360),np.where(valid)[0],row[valid,c]) for c in range(3)],axis=1)
            row=gaussian_filter1d(row,2,axis=0);bg=np.repeat(row[:,None,:],360,axis=1)
        return a,bg,fg,None
    if name not in ('Apple','Omission','China_Taipei','South_Korea'):raise ValueError(name)
    rgb=a[:,:,:3];terms=np.stack([np.ones_like(x),x,y,x*x,x*y,y*y,x*x*x,x*x*y,x*y*y,y*y*y],axis=2)
    ring=(r>.90)&(r<.97)&(a[:,:,3]>250)
    bg=np.zeros_like(rgb);errs=[]
    for c in range(3):
        coef=np.linalg.lstsq(terms[ring],rgb[:,:,c][ring],rcond=None)[0]
        bg[:,:,c]=terms@coef;errs.append(float(np.median(np.abs(bg[:,:,c][ring]-rgb[:,:,c][ring]))))
    if max(errs)>2:raise ValueError(f'{name}: uncertain background fit {errs}')
    bg=np.clip(bg,0,255)
    diff=np.max(np.abs(rgb-bg),axis=2)
    matte=np.clip((diff-2)/8,0,1)*(a[:,:,3]/255);matte[r>.99]=0
    # Intentionally preserves integrated artwork inside the Edge sphere.
    fg=bg+(rgb-bg)/np.maximum(matte[:,:,None],1e-8)
    bg=np.where((matte<1e-8)[:,:,None],rgb,bg)
    return a,bg,fg,matte

def render(name,scale,dx=0,dy=0):
    if not .2<=scale<=1.5:raise ValueError('unsafe scale')
    a,bg,fg,matte=layers(name)
    if matte is None:
        size=round(360*scale);fg=fg.resize((size,size),Image.Resampling.LANCZOS)
        canvas=Image.fromarray(np.dstack([np.rint(bg).astype('uint8'),np.full((360,360),255,dtype='uint8')]),'RGBA')
        canvas.alpha_composite(fg,(round((360-size)/2+dx),round((360-size)/2+dy)))
        canvas.putalpha(Image.fromarray(a[:,:,3].astype('uint8')));return canvas
    if scale==1 and dx==0 and dy==0:return Image.fromarray(a.astype('uint8'),'RGBA')
    yy,xx=np.mgrid[:360,:360];co=np.array([(yy-179.5-dy)/scale+179.5,(xx-179.5-dx)/scale+179.5])
    alpha=np.clip(map_coordinates(matte,co,order=1,mode='constant'),0,1)
    premult=fg*matte[:,:,None];mov=np.stack([map_coordinates(premult[:,:,c],co,order=1,mode='constant') for c in range(3)],2)
    out=bg*(1-alpha[:,:,None])+mov
    return Image.fromarray(np.dstack([np.clip(np.rint(out),0,255).astype('uint8'),a[:,:,3].astype('uint8')]),'RGBA')
