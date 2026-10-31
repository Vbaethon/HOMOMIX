#!/usr/bin/env python3
"""Fixed-circle foreground normalization and concentrated original silhouettes.
Run --output-dir elsewhere; does not write production Icon directory.
"""
from pathlib import Path
import sys,json,hashlib,subprocess,tempfile,xml.etree.ElementTree as E
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent;ROOT=R.parents[1]
sys.path.insert(0,str(R.parent/'v5'));import build_optical as previous
sys.path.insert(0,str(R.parent/'v3'));import author_sources
import compact_originals,raster_white,raster_colored,raster_pale,special_official
NS='http://www.w3.org/2000/svg';E.register_namespace('',NS)
ALIASES={Path(a).stem:Path(b).stem for a,b in json.loads((ROOT/'icon_aliases.json').read_text()).items()}
FISH='M58 182C66 132 101 99 146 99C180 99 210 125 231 155C247 144 264 129 286 121Q301 116 298 132L288 181L298 230Q301 246 286 241C264 234 247 219 231 208C209 245 180 265 146 265C101 265 66 232 58 182Z'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def svg(name,scale,compact_scale=1.):
 canonical=ALIASES.get(name,name)
 if canonical in compact_originals.SHAPES:
  original=author_sources.parts
  def compact_parts(n):
   defs,body=original(n);return compact_originals.adjust(n,defs,body)
  author_sources.parts=compact_parts
  try:raw=author_sources.svg(canonical)
  finally:author_sources.parts=original
  if compact_scale!=1:
   t=E.fromstring(raw);mask=next(e for e in t.iter() if e.attrib.get('id')=='subjectMask');group=E.Element(f'{{{NS}}}g',{'transform':previous.transform(compact_scale)})
   for child in list(mask):mask.remove(child);group.append(child)
   mask.append(group);raw=E.tostring(t,encoding='unicode')
  return raw,'concentrated_original',compact_scale
 result=previous.native(canonical,scale)
 if result is None:return None
 raw,src=result
 if canonical in {'Fish','Fish_b','Dolphin','Globefish'}:
  t=E.fromstring(raw);mask=next(e for e in t.iter() if e.attrib.get('id')=='subjectMask');list(mask)[0].set('transform',previous.transform(scale));raw=E.tostring(t,encoding='unicode')
 if canonical=='Fish':
  import animal_redesign
  raw=raw.replace(animal_redesign.SHAPES['Fish'][0],FISH)
 return raw,'native_foreground',scale

def main():
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--output-dir',required=True,type=Path);p.add_argument('--jobs',type=int,default=4);p.add_argument('--names',nargs='*');args=p.parse_args();args.output_dir.mkdir(parents=True,exist_ok=True)
 rows=json.loads((R/'plan.json').read_text())['icons'];byname={x['name']:x for x in rows};jobs=[]
 for row in rows:
  n=row['name']
  if args.names and n not in args.names:continue
  canonical=ALIASES.get(n,n);settings=dict(byname[canonical]);settings['name']=n;settings['canonical']=canonical
  if settings['mode']=='native':
   result=svg(n,settings['scale'],settings.get('compact_scale',1.));raw,method,effective=result;path=R/'svg'/f'{n}.svg';path.write_text(raw);settings.update(svg=path,method=method,effective_scale=effective)
  else:settings.update(method=settings['mode'],effective_scale=settings['scale'])
  jobs.append(settings)
 def render(row):
  name=row['name'];n=row['canonical'];s=row['effective_scale'];dx=row['dx'];dy=row['dy'];mode=row['mode'];im=None
  if 'svg' in row:
   with tempfile.TemporaryDirectory() as td:
    dest=Path(td)/'hi.png';subprocess.run(['node',str(R.parent/'v3/render.cjs'),str(row['svg']),str(dest)],check=True,capture_output=True);hi=Image.open(dest).convert('RGBA');im=hi.resize((360,360),Image.Resampling.LANCZOS)
  elif mode=='special':im=special_official.render(n,s,dx,dy)
  elif mode=='gog_official_white':
   src=Image.open(R/'official-special/GOG.png').convert('RGBA');a=np.array(src).astype(float);rgb=a[...,:3];alpha=1-rgb.min(2)/255
   color=np.where(alpha[...,None]>1e-5,(rgb-255*(1-alpha[...,None]))/np.maximum(alpha[...,None],1e-5),0)
   fg=Image.fromarray(np.dstack([np.clip(color,0,255),np.rint(alpha*255)]).astype('uint8'));fg=fg.crop(fg.getchannel('A').getbbox());sz=(round(fg.width*s),round(fg.height*s));fg=fg.resize(sz,Image.Resampling.LANCZOS)
   im=Image.new('RGBA',(360,360),'white');im.alpha_composite(fg,((360-sz[0])//2,(360-sz[1])//2))
  elif mode=='bitcoin_adapted_background':
   src=np.array(Image.open(R.parent/'v5/input-large/Bitcoin.png').convert('RGBA')).astype(float);rgb=src[...,:3];yy,xx=np.mgrid[:360,:360];inside=np.hypot(xx-180,yy-180)<115
   orange=np.array([247.,147.,26.]);direction=255-orange
   alpha=np.clip(np.sum((rgb-orange)*direction,axis=2)/np.sum(direction*direction),0,1)*inside
   fg=Image.fromarray(np.dstack([np.full((360,360,3),255),np.rint(alpha*255)]).astype('uint8'));sz=round(360*s)
   im=Image.new('RGBA',(360,360),tuple(orange.astype(int))+(255,));im.alpha_composite(fg.resize((sz,sz),Image.Resampling.LANCZOS),(round((360-sz)/2+dx),round((360-sz)/2+dy)))
  elif mode=='sony_original':
   import separate_special_rasters
   im=separate_special_rasters.render(n,s,dx,dy)
  elif mode=='steam_existing_positive':
   original,bg,_,_=special_official.layers('Steam');rgb=original[...,:3];direction=255-bg
   alpha=np.clip(np.sum((rgb-bg)*direction,axis=2)/np.maximum(np.sum(direction*direction,axis=2),1),0,1);alpha[alpha<.015]=0;alpha*=original[...,3]/255
   fg=Image.fromarray(np.dstack([np.full((360,360,3),255),np.rint(alpha*255)]).astype('uint8'));sz=round(360*s)
   im=Image.fromarray(np.dstack([np.rint(bg),np.full((360,360),255)]).astype('uint8'));im.alpha_composite(fg.resize((sz,sz),Image.Resampling.LANCZOS),(round((360-sz)/2+dx),round((360-sz)/2+dy)));im.putalpha(Image.fromarray(original[...,3].astype('uint8')))
  elif mode.startswith('white_mark_'):
   raster_white.NAMES.add(n);im=raster_white.render(n,s,dx,dy)
  elif mode in {'colored_mark_dark_background','colored_mark_bright_background','dark_mark_bright_background'}:im=raster_colored.render(n,s,dx,dy)
  elif mode=='white_or_pale_disc_raster':im=raster_pale.render(n,s,dx,dy)
  elif mode=='illustration_pale':
   raster_pale.PALE_NAMES.add(n);im=raster_pale.render(n,s,dx,dy)
  elif mode=='character_on_flat_background':
   from scipy.ndimage import binary_fill_holes,distance_transform_edt
   source=Image.open(R.parent/'v5/input-large'/f'{n}.png').convert('RGBA');a=np.array(source).astype(float);rgb=a[...,:3];valid=a[...,3]>250
   bins=(rgb[valid]//8).astype(int);keys=bins[:,0]*1024+bins[:,1]*32+bins[:,2];key=int(np.bincount(keys).argmax());color=np.array([key//1024,(key//32)%32,key%32])*8+4;color=np.median(rgb[valid][keys==key],axis=0)
   support=(np.max(abs(rgb-color),axis=2)>12)&valid;support=binary_fill_holes(support);dist=distance_transform_edt(~support);alpha=np.clip(1.5-dist,0,1)*valid
   fg=Image.fromarray(np.dstack([rgb,np.rint(alpha*255)]).astype('uint8'));im=Image.new('RGBA',(360,360),tuple(np.rint(color).astype(int))+(255,));sz=round(360*s);im.alpha_composite(fg.resize((sz,sz),Image.Resampling.LANCZOS),((360-sz)//2,(360-sz)//2));im.putalpha(source.getchannel('A'))
  elif mode=='transparent_character':
   source=Image.open(R.parent/'v5/input-large'/f'{n}.png').convert('RGBA');im=Image.new('RGBA',(360,360),'white');sz=round(360*s);im.alpha_composite(source.resize((sz,sz),Image.Resampling.LANCZOS),((360-sz)//2,(360-sz)//2))
  elif mode=='full_composition_preserved':im=Image.open(R/'input-v8/Icon/Color/Large'/f'{n}.png').convert('RGBA')
  else:raise ValueError((name,mode))
  # Match actual approved raster examples, not a subtly different second matte.
  if n in {'Google','Gmail','TikTok','Facebook','Pixiv','Bluesky','Instagram'}:
   im=Image.open(R/'approved-sample'/f'{n}.png').convert('RGBA');row['method']='approved_sample_exact'
  arr=np.array(im);yy,xx=np.mgrid[:360,:360];coverage=np.clip(175.5-np.hypot(xx+.5-180,yy+.5-180),0,1)*255
  # Circle is fixed and independent of foreground size. Never add a white frame.
  arr[...,3]=np.minimum(arr[...,3],np.rint(coverage).astype('uint8'));arr[arr[...,3]==0]=0;im=Image.fromarray(arr)
  assets=[]
  for large in (False,True):
   filename='Bilibili' if name=='bilibili' and large else name
   rel='Icon/Color/'+('Large/' if large else '')+filename+'.png';target=args.output_dir/rel;target.parent.mkdir(parents=True,exist_ok=True)
   if large:out=im
   else:out=Image.new('RGBA',(300,300));out.alpha_composite(im.resize((180,180),Image.Resampling.LANCZOS),(60,60))
   out.save(target,optimize=False);assets.append({'name':name,'canonical':n,'path':rel,'sha256':sha(target),'scale':s,'dx':dx,'dy':dy,'method':row['method'],'source_svg':row['svg'].relative_to(ROOT).as_posix() if 'svg' in row else None})
  return assets
 with ThreadPoolExecutor(max_workers=args.jobs) as pool:assets=[a for result in pool.map(render,jobs) for a in result]
 (args.output_dir/'render-report.json').write_text(json.dumps({'assets':assets,'names':len(jobs),'png':len(assets)},indent=2)+'\n');print('Rendered',len(assets),'PNG')
if __name__=='__main__':main()
