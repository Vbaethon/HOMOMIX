"""Subject-only scaling of existing multicolored raster marks. No geometry tracing.
Background fitting is an explicitly approximate reconstruction beneath the mark.
The original background remains fixed at all observed, unoccluded pixels.
"""
from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageFilter,ImageDraw
from scipy.ndimage import binary_fill_holes, binary_opening, label, gaussian_filter, distance_transform_edt
R=Path(__file__).resolve().parent
NAMES=['Apple_TV','Douyin','Hugging_face_g','Hulu','Jellyfin','MLB','NBA','Netflix','Niconico_Manga','PayPal','Peacook','Plex','Pornhub','Spotify','Twitch','Vimeo','Xianyu']
_CACHE={}
def _layers(name):
 if name not in NAMES:raise KeyError(name)
 if name in _CACHE:return _CACHE[name]
 p=R/'assets/original-raster'/f'{name}.png';orig=np.asarray(Image.open(p).convert('RGBA')).astype(float);rgb=orig[:,:,:3]
 yy,xx=np.mgrid[:360,:360];x=(xx-179.5)/180;y=(yy-179.5)/180;rr=np.hypot(x,y)
 # Low-order smooth backdrop, robust against peripheral logo contamination.
 basis=np.stack([np.ones_like(x),x,y,x*x,x*y,y*y],axis=-1)
 ring_inner=.90 if name in {'Niconico_Manga','Spotify'} else .76
 ring_outer=.95 if name in {'Niconico_Manga','Spotify'} else .91
 valid=(rr>ring_inner)&(rr<ring_outer)&(orig[:,:,3]>250)
 for _ in range(8):
  coef=np.linalg.lstsq(basis[valid],rgb[valid],rcond=None)[0];pred=np.clip(basis@coef,0,255)
  err=np.max(np.abs(rgb-pred),axis=2);vals=err[valid];cut=max(2.,float(np.quantile(vals,.80))*1.8)
  valid=(rr>ring_inner)&(rr<ring_outer)&(orig[:,:,3]>250)&(err<cut)
 delta=np.max(np.abs(rgb-pred),axis=2)
 support=(delta>9)&(rr<.985)&(orig[:,:,3]>250)
 # Component filtering removes isolated JPEG/raster artifacts, never erodes glyphs.
 labs,count=label(support);sizes=np.bincount(labs.ravel());support=support&(sizes[labs]>=5)
 support=binary_fill_holes(support)
 # Include all soft edge pixels adjoining known geometry; no manual logo outlines.
 dist=distance_transform_edt(~support);alpha=np.clip(1.5-dist,0,1);alpha[support]=1
 alpha[rr>.995]=0
 # Matte edge carries original antialiasing pixels; RGB never whitened/recolored.
 bg=rgb.copy();bg[alpha>0]=pred[alpha>0]
 rgba=np.dstack([rgb,np.rint(alpha*255)]).astype('uint8')
 meta={'name':name,'background_recovery':'robust quadratic RGB fit from original visible ring; approximate only under removed foreground','fit_ring_median_error':float(np.median(np.max(np.abs(rgb-pred),axis=2)[valid])),'foreground_bbox':Image.fromarray((alpha*255).astype('uint8')).getbbox(),'warning':'No claim of lossless recovery of hidden background. Inspect QA for halos, clipped geometry and dark detail preservation.'}
 _CACHE[name]=(Image.fromarray(rgba),bg,orig,meta)
 return _CACHE[name]
def render(name,scale,dx=0,dy=0):
 fg,bg,orig,meta=_layers(name)
 # Resize only the foreground. Background and circular alpha never scale.
 s=float(scale);sz=max(1,round(360*s));mark=fg.resize((sz,sz),Image.Resampling.LANCZOS)
 out=Image.fromarray(np.dstack([np.rint(bg),np.full((360,360),255)]).clip(0,255).astype('uint8'))
 out.alpha_composite(mark,(round((360-sz)/2+dx),round((360-sz)/2+dy)))
 a=np.array(out);a[:,:,3]=orig[:,:,3].astype('uint8');a[a[:,:,3]==0]=0
 return Image.fromarray(a)
def qa():
 out=R/'qa/colored';out.mkdir(parents=True,exist_ok=True);rows=[]
 sheet=Image.new('RGB',(1200,180*((len(NAMES)+3)//4)),'#dfe3e8');d=ImageDraw.Draw(sheet)
 for i,n in enumerate(NAMES):
  fg,bg,orig,meta=_layers(n);im=render(n,.88);im.save(out/f'{n}.png');fg.save(out/f'{n}-matte.png');rows.append(meta)
  x=i%4*300;y=i//4*180;d.text((x+5,y+5),n+'  original / subject .88',fill='black')
  for j,src in enumerate([Image.fromarray(orig.astype('uint8')),im]):
   thumb=src.resize((120,120),Image.Resampling.LANCZOS);sheet.paste(thumb,(x+5+j*145,y+25),thumb)
   small=src.resize((36,36),Image.Resampling.LANCZOS);sheet.paste(small,(x+45+j*145,y+145),small)
 sheet.save(out/'before-after.png');(out/'report.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
if __name__=='__main__':qa()
