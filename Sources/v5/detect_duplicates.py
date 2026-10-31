#!/usr/bin/env python3
"""Read-only production PNG duplicate audit. Writes only JSON and QA contact sheet.
Default glob is nonrecursive: Large/FDS pairs are intentionally excluded.
Dependencies: Pillow, numpy. Thresholds propose candidates, never auto-delete.
"""
from pathlib import Path
import argparse,hashlib,json,itertools
from PIL import Image,ImageDraw
import numpy as np

def feature(path):
 im=Image.open(path).convert('RGBA'); bg=Image.new('RGBA',im.size,'white');bg.alpha_composite(im);rgb=np.asarray(bg.convert('RGB')).astype(float)/255
 y,x=np.indices(rgb.shape[:2]);h,w=rgb.shape[:2];mx=rgb.max(2);mn=rgb.min(2)
 # Ignore white disc and neutral soft outer shadow; restrict to central mark area.
 mask=(((mx-mn)>.20)|(mx<.62))&(((x-w/2)/(w*.43))**2+((y-h/2)/(h*.43))**2<1)
 yy,xx=np.where(mask);box=(int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)) if len(xx) else (0,0,w,h)
 m=Image.fromarray((mask*255).astype('uint8')).crop(box).resize((36,36),Image.Resampling.LANCZOS)
 shape=np.asarray(m)/255
 small=bg.convert('RGB').resize((36,36),Image.Resampling.LANCZOS)
 crop=bg.convert('RGB').crop(box).resize((36,36),Image.Resampling.LANCZOS)
 arr=np.asarray(crop).astype(float)/255
 dx=np.max(np.abs(np.diff(arr,axis=1,prepend=arr[:,:1])),axis=2)
 dy=np.max(np.abs(np.diff(arr,axis=0,prepend=arr[:1,:])),axis=2)
 edge=np.sqrt(dx*dx+dy*dy);edge[:2]=0;edge[-2:]=0;edge[:,:2]=0;edge[:,-2:]=0
 edge=edge/max(float(np.linalg.norm(edge)),1e-9)
 return im,shape,np.asarray(small).astype(float)/255,box,edge

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[2]);ap.add_argument('--output',type=Path);args=ap.parse_args();root=args.root;out=args.output or Path(__file__).with_name('duplicate-audit.json');out.parent.mkdir(parents=True,exist_ok=True)
 paths=sorted((root/'Icon/Color').glob('*.png'));data={p.stem:feature(p) for p in paths};groups={}
 for n,(im,*_) in data.items():groups.setdefault(hashlib.sha256(str(im.size).encode()+im.tobytes()).hexdigest(),[]).append(n)
 exact=[v for v in groups.values() if len(v)>1];pairs=[]
 for a,b in itertools.combinations(data,2):
  _,ma,ca,_,ea=data[a];_,mb,cb,_,eb=data[b];iou=float(np.minimum(ma,mb).sum()/max(np.maximum(ma,mb).sum(),1));mad=float(np.abs(ca-cb).mean());shape_mae=float(np.abs(ma-mb).mean())
  edge_cos=float((ea*eb).sum())
  if (iou>.77 and edge_cos>.80) or (mad<.018 and iou>.40):pairs.append(dict(names=[a,b],edge_cos=round(edge_cos,4),foreground_iou=round(iou,4),shape_mae=round(shape_mae,4),rgb36_mae=round(mad,4)))
 pairs.sort(key=lambda p:-p['foreground_iou']);report=dict(method='Decoded RGBA exact hash; 36px RGB MAE plus white-disc-excluding foreground-mask IoU and normalized internal RGB-edge cosine. Candidate if (IoU > .77 and edge cosine > .80) or (RGB MAE < .018 and IoU > .40). Mask bbox normalized independently; candidates require visual review.',default_count=len(paths),excluded='Nonrecursive glob excludes Icon/Color/Large and FDS; no Default/Large size-pair false matches.',exact_pixel_groups=exact,candidate_pairs=pairs,limitations='Bbox normalization can overmatch generic circles. Pale/white details may be omitted. Perceptual thresholds are candidates, not a complete mathematical proof of nonduplication.',files=[dict(name=n,foreground_bbox=data[n][3]) for n in data]);out.write_text(json.dumps(report,ensure_ascii=False,indent=2))
 # Pair-by-pair rendered production pixels, enlarged only for inspection.
 cw,ch=360,150;sheet=Image.new('RGB',(cw*3,ch*((len(pairs)+2)//3)),'#dedede');d=ImageDraw.Draw(sheet)
 for i,p in enumerate(pairs):
  x=i%3*cw;y=i//3*ch;d.text((x+5,y+3),f"{i}: IoU={p['foreground_iou']} MAE={p['rgb36_mae']}",fill='black')
  for j,n in enumerate(p['names']):
   im=data[n][0].copy();im.thumbnail((110,110));sheet.paste(im,(x+15+j*170,y+18),im);d.text((x+5+j*170,y+130),n,fill='black')
 sheet.save(out.with_suffix('.png'));print(json.dumps(dict(default_count=len(paths),exact=exact,candidates=len(pairs),output=str(out))))
if __name__=='__main__':main()
