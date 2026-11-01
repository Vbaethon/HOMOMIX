"""Foreground-only resampling for legacy white/pale-disc assets.

Input is original 360px v5/input-large, never a previously scaled deliverable.
The original disc alpha and sampled vertical background stay fixed. A conservative
soft difference matte separates the subject from the neutral pale background;
opaque subject colors are resampled directly, without recoloring or distortion.
Not for colored/integrated-art backgrounds or existing native SVG assets.
"""
from pathlib import Path
from functools import lru_cache
import json
import numpy as np
from PIL import Image
from scipy.ndimage import map_coordinates, median_filter, gaussian_filter1d
ROOT = Path(__file__).resolve().parents[2]
STRATEGIES = json.loads((ROOT/'Sources/current/background-strategies.json').read_text())
PALE_NAMES = {r['name'] for r in STRATEGIES['icons'] if r['classification']=='white_or_pale_disc_raster'}

def native_source(name):
    p=ROOT/'Sources/current/assets/native-baseline'/f'{name}.svg'
    return p if p.exists() else None

def available_names():
    return sorted(n for n in PALE_NAMES if not native_source(n))

@lru_cache(maxsize=64)
def separate(name):
    if name not in PALE_NAMES: raise ValueError(f'{name}: not classified pale raster')
    if native_source(name): raise ValueError(f'{name}: use existing native source {native_source(name)}')
    p=ROOT/'Sources/current/assets/original-raster'/f'{name}.png'
    a=np.asarray(Image.open(p).convert('RGBA'),dtype=np.float64)
    if a.shape != (360,360,4): raise ValueError(f'{name}: expected original 360px RGBA')
    rgb=a[:,:,:3]; yy,xx=np.mgrid[:360,:360]; r=np.hypot(xx-179.5,yy-179.5)
    # Original antialiased edge is excluded from estimation. Pale disc backgrounds
    # in this group are neutral vertical gradients. Both sides are sampled.
    ring=(r>164)&(r<175)&(a[:,:,3]>250)&(np.ptp(rgb,axis=2)<3)&(rgb.mean(2)>195)
    values=np.full(360,np.nan)
    for y in range(360):
        row=rgb[y][ring[y]]
        if len(row)>=4: values[y]=np.median(row)
    valid=np.isfinite(values)
    if valid.sum()<240: raise ValueError(f'{name}: insufficient clean background evidence')
    # Linear fit handles the known pale gradients. Iterated rejection prevents
    # isolated subject pixels touching the sampling ring from biasing the fit.
    y=np.arange(360)
    keep=valid.copy()
    for _ in range(4):
        coeff=np.polyfit(y[keep],values[keep],1)
        pred=np.polyval(coeff,y)
        keep=valid&(np.abs(values-pred)<2.0)
    profile=np.clip(pred,0,255)
    if name == 'BT_Bittorrent':
        # Verified non-linear vertical ramp, plateauing at gray226 below y260.
        # Use observed bilateral row medians, not an assumed white background.
        profile=gaussian_filter1d(median_filter(np.interp(y,y[valid],values[valid]),size=9),sigma=3)
        keep=valid & (np.abs(values-profile)<2)
    error=float(np.median(np.abs(values[keep]-profile[keep])))
    if error>1.2 or np.sum(keep)<230:
        raise ValueError(f'{name}: background cannot be safely reconstructed (error={error:.2f})')
    bg=np.repeat(profile[:,None,None],360,axis=1);bg=np.repeat(bg,3,axis=2)
    diff=np.max(np.abs(rgb-bg),axis=2)
    # 2px quantization/jpg-like noise is background, not a fake giant foreground.
    # Alpha reaches one for true colored/dark subject; light edge contributions
    # are preserved by unpremultiplying the observed difference.
    matte=np.clip((diff-2)/6,0,1)*(a[:,:,3]/255)
    matte[r>177]=0
    fg=bg+(rgb-bg)/np.maximum(matte[:,:,None],1e-8)
    # Retain exact original background samples where the matte is absent. This
    # preserves original circle perimeter and avoids white rims or pasted discs.
    background=np.where((matte<1e-8)[:,:,None],rgb,bg)
    stats={'name':name,'background_fit_median_error':error,'background_top':float(profile[0]),'background_bottom':float(profile[-1]),'ring_samples':int(keep.sum()),'matte_extent':[int(z) for z in [np.where(matte>.5)[1].min(),np.where(matte>.5)[0].min(),np.where(matte>.5)[1].max(),np.where(matte>.5)[0].max()]]}
    return a,background,matte,fg,stats

def render(name, scale, dx=0, dy=0):
    """Return RGBA360; uniform scale relative to original subject, offsets in px."""
    if not np.isfinite(scale) or not 0.2<=scale<=1.5: raise ValueError('scale outside safe range .2–1.5')
    a,bg,matte,fg,_=separate(name)
    if scale==1 and dx==0 and dy==0: return Image.fromarray(a.astype('uint8'),'RGBA')
    yy,xx=np.mgrid[:360,:360]
    coords=np.array([(yy-179.5-dy)/scale+179.5,(xx-179.5-dx)/scale+179.5])
    alpha=np.clip(map_coordinates(matte,coords,order=1,mode='constant',cval=0),0,1)
    premult=fg*matte[:,:,None]
    moved=np.stack([map_coordinates(premult[:,:,c],coords,order=1,mode='constant',cval=0) for c in range(3)],axis=2)
    out=bg*(1-alpha[:,:,None])+moved
    return Image.fromarray(np.dstack([np.clip(np.rint(out),0,255).astype('uint8'),a[:,:,3].astype('uint8')]),'RGBA')
