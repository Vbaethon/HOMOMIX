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
import native as previous
import author_sources
import compact_originals,raster_white,raster_colored,raster_pale,special_official,calibrated_samples
# Compatibility-only legacy scale values. Compact artwork is authored at its
# target size; only compact_scale controls its actual geometric scale. Keep
# this immutable so editing plan.json cannot silently redefine validation.
COMPACT_LEGACY_SCALE={'AI_Tree': 1.07, 'AI_voice': 1.176, 'Auto_Link': 1.1648, 'Chained': 1.155, 'Chained_2': 1.1025, 'Consistent_Hashing': 1.1025, 'DIRECT': 1.176, 'Download': 1.08, 'Download_2': 1.15344, 'Failover': 1.09, 'GFW': 1.0735, 'Load_balancing': 1.06, 'Load_balancing_2': 1.1, 'Load_balancing_3': 1.177, 'Magic_Timer': 1.134, 'Network': 1.02, 'Other': 1.265, 'Round_Robin': 1.089, 'SNS': 1.07, 'Server': 1.064, 'Stream': 1.008, 'Tick_2': 0.95, 'Transfer': 1.12}
NS='http://www.w3.org/2000/svg';E.register_namespace('',NS)
ALIASES={Path(a).stem:Path(b).stem for a,b in json.loads((ROOT/'icon_aliases.json').read_text()).items()}
FISH='M58 182C66 132 101 99 146 99C180 99 210 125 231 155C247 144 264 129 286 121Q301 116 298 132L288 181L298 230Q301 246 286 241C264 234 247 219 231 208C209 245 180 265 146 265C101 265 66 232 58 182Z'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def translate_foreground(raw,dx,dy):
 if not dx and not dy:return raw
 tree=E.fromstring(raw)
 node=next((e for e in tree.iter() if e.attrib.get('id')=='subjectMask'),None)
 if node is not None:
  group=E.Element(f'{{{NS}}}g',{'transform':f'translate({dx} {dy})'})
  for child in list(node):node.remove(child);group.append(child)
  node.append(group)
 else:
  node=next((e for e in tree.iter() if e.attrib.get('id') in {'optical-foreground','optical-subject'}),None)
  if node is None:raise ValueError('Native SVG has no independently transformable foreground')
  node.set('transform',f'translate({dx} {dy}) '+node.attrib.get('transform',''))
 return E.tostring(tree,encoding='unicode')

def svg(name,scale,compact_scale=1.,dx=0,dy=0):
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
  return translate_foreground(raw,dx,dy),'concentrated_original',compact_scale
 result=previous.native(canonical,scale)
 if result is None:return None
 raw,src=result
 if canonical in {'Fish','Fish_b','Dolphin','Globefish'}:
  t=E.fromstring(raw);mask=next(e for e in t.iter() if e.attrib.get('id')=='subjectMask');list(mask)[0].set('transform',previous.transform(scale));raw=E.tostring(t,encoding='unicode')
 if canonical=='Fish':
  import animal_redesign
  raw=raw.replace(animal_redesign.SHAPES['Fish'][0],FISH)
 return translate_foreground(raw,dx,dy),'native_foreground',scale

def main():
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--output-dir',required=True,type=Path);p.add_argument('--jobs',type=int,default=4);p.add_argument('--names',nargs='*');p.add_argument('--plan',type=Path,default=R/'plan.json');args=p.parse_args();
 if args.output_dir.resolve()==ROOT.resolve():p.error('--output-dir must be outside the production repository root')
 args.output_dir.mkdir(parents=True,exist_ok=True)
 rows=json.loads(args.plan.read_text())['icons'];byname={x['name']:x for x in rows};jobs=[]
 for row in rows:
  n=row['name']
  if args.names and n not in args.names:continue
  canonical=ALIASES.get(n,n);settings=dict(byname[canonical]);settings['name']=n;settings['canonical']=canonical
  if not all(np.isfinite(settings[k]) for k in ('scale','dx','dy')) or settings['scale']<=0:
   raise ValueError(f'{n}: scale must be positive and transforms finite')
  if settings['mode']=='full_composition_preserved' and (settings['scale'],settings['dx'],settings['dy'])!=(1.,0,0):
   raise ValueError(f'{n}: full_composition_preserved only accepts scale=1, dx=dy=0')
  if settings['mode']=='native' and canonical in compact_originals.SHAPES:
   if settings['scale']!=COMPACT_LEGACY_SCALE[canonical]:
    raise ValueError(f'{n}: concentrated_original uses compact_scale; legacy scale is not an editable transform')
   if not np.isfinite(settings.get('compact_scale',1.)) or settings.get('compact_scale',1.)<=0:
    raise ValueError(f'{n}: compact_scale must be finite and positive')
  if canonical in calibrated_samples.NAMES:
   settings.update(method='calibrated_foreground_layers',effective_scale=settings['scale'])
  elif settings['mode']=='native':
   result=svg(n,settings['scale'],settings.get('compact_scale',1.),settings['dx'],settings['dy']);raw,method,effective=result;path=args.output_dir/'Sources/current/svg'/f'{n}.svg';path.parent.mkdir(parents=True,exist_ok=True);path.write_text(raw);settings.update(svg=path,method=method,effective_scale=effective)
  else:settings.update(method=settings['mode'],effective_scale=settings['scale'])
  jobs.append(settings)
 def render(row):
  name=row['name'];n=row['canonical'];s=row['effective_scale'];dx=row['dx'];dy=row['dy'];mode=row['mode'];im=None
  if n in calibrated_samples.NAMES:im=calibrated_samples.render(n,s,dx,dy)
  elif 'svg' in row:
   with tempfile.TemporaryDirectory() as td:
    dest=Path(td)/'hi.png';subprocess.run(['node',str(R/'render.cjs'),str(row['svg']),str(dest)],check=True,capture_output=True);hi=Image.open(dest).convert('RGBA');im=hi.resize((360,360),Image.Resampling.LANCZOS)
  elif mode=='special':im=special_official.render(n,s,dx,dy)
  elif mode=='gog_official_white':
   src=Image.open(R/'official/special/GOG.png').convert('RGBA');a=np.array(src).astype(float);rgb=a[...,:3];alpha=1-rgb.min(2)/255
   color=np.where(alpha[...,None]>1e-5,(rgb-255*(1-alpha[...,None]))/np.maximum(alpha[...,None],1e-5),0)
   fg=Image.fromarray(np.dstack([np.clip(color,0,255),np.rint(alpha*255)]).astype('uint8'));fg=fg.crop(fg.getchannel('A').getbbox());sz=(round(fg.width*s),round(fg.height*s));fg=fg.resize(sz,Image.Resampling.LANCZOS)
   im=Image.new('RGBA',(360,360),'white');im.alpha_composite(fg,((360-sz[0])//2+round(dx),(360-sz[1])//2+round(dy)))
  elif mode=='bitcoin_adapted_background':
   src=np.array(Image.open(R/'assets/original-raster/Bitcoin.png').convert('RGBA')).astype(float);rgb=src[...,:3];yy,xx=np.mgrid[:360,:360];inside=np.hypot(xx-180,yy-180)<115
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
   source=Image.open(R/'assets/original-raster'/f'{n}.png').convert('RGBA');a=np.array(source).astype(float);rgb=a[...,:3];valid=a[...,3]>250
   bins=(rgb[valid]//8).astype(int);keys=bins[:,0]*1024+bins[:,1]*32+bins[:,2];key=int(np.bincount(keys).argmax());color=np.array([key//1024,(key//32)%32,key%32])*8+4;color=np.median(rgb[valid][keys==key],axis=0)
   support=(np.max(abs(rgb-color),axis=2)>12)&valid;support=binary_fill_holes(support);dist=distance_transform_edt(~support);alpha=np.clip(1.5-dist,0,1)*valid
   fg=Image.fromarray(np.dstack([rgb,np.rint(alpha*255)]).astype('uint8'));im=Image.new('RGBA',(360,360),tuple(np.rint(color).astype(int))+(255,));sz=round(360*s);im.alpha_composite(fg.resize((sz,sz),Image.Resampling.LANCZOS),((360-sz)//2+round(dx),(360-sz)//2+round(dy)));im.putalpha(source.getchannel('A'))
  elif mode=='transparent_character':
   source=Image.open(R/'assets/original-raster'/f'{n}.png').convert('RGBA');im=Image.new('RGBA',(360,360),'white');sz=round(360*s);im.alpha_composite(source.resize((sz,sz),Image.Resampling.LANCZOS),((360-sz)//2+round(dx),(360-sz)//2+round(dy)))
  elif mode=='full_composition_preserved':im=Image.open(R/'assets/composition'/f'{n}.png').convert('RGBA')
  else:raise ValueError((name,mode))
  arr=np.array(im);yy,xx=np.mgrid[:360,:360];coverage=np.clip(175.5-np.hypot(xx+.5-180,yy+.5-180),0,1)*255
  # Circle is fixed and independent of foreground size. Never add a white frame.
  arr[...,3]=np.minimum(arr[...,3],np.rint(coverage).astype('uint8'));arr[arr[...,3]==0]=0;im=Image.fromarray(arr)
  assets=[]
  for large in (False,True):
   filename='Bilibili' if name=='bilibili' and large else name
   rel='Icon/Color/'+('Large/' if large else '')+filename+'.png';target=args.output_dir/rel;target.parent.mkdir(parents=True,exist_ok=True)
   if large:out=im
   else:out=Image.new('RGBA',(300,300));out.alpha_composite(im.resize((180,180),Image.Resampling.LANCZOS),(60,60))
   out.save(target,optimize=False);assets.append({'name':name,'canonical':n,'path':rel,'sha256':sha(target),'scale':s,'scale_parameter':('compact_scale' if row['method']=='concentrated_original' else 'scale'),'transform_policy':('fixed_composition' if mode=='full_composition_preserved' else 'foreground_only'),'dx':dx,'dy':dy,'method':row['method'],'source_svg':('Sources/current/svg/'+name+'.svg') if 'svg' in row else None})
  return assets
 with ThreadPoolExecutor(max_workers=args.jobs) as pool:assets=[a for result in pool.map(render,jobs) for a in result]
 (args.output_dir/'render-report.json').write_text(json.dumps({'assets':assets,'names':len(jobs),'png':len(assets)},indent=2)+'\n');print('Rendered',len(assets),'PNG')
if __name__=='__main__':main()
