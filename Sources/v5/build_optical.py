#!/usr/bin/env python3
"""Deterministic optical pass. Native subject-only transforms; legacy complete
artwork uniform sampling with original white background extended only where
needed. No anisotropic stretching, recoloring or invented brand outlines.
"""
from pathlib import Path
import argparse,json,hashlib,subprocess,tempfile,sys,io,copy
import xml.etree.ElementTree as E
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent; REPO=R.parents[1]
NS='http://www.w3.org/2000/svg';E.register_namespace('',NS)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def transform(s):return f'translate(180 180) scale({s}) translate(-180 -180)'
def native(name,s):
 src=REPO/'Sources/v4/svg'/f'{name}.svg'
 if not src.exists():src=REPO/'Sources/v3/svg'/f'{name}.svg'
 if not src.exists():return None
 raw=src.read_text()
 # Optional explicit animal geometry revision, leaving material filters intact.
 if name in {'Fish','Fish_b','Dolphin','Globefish'} and (R/'animal_redesign.py').exists():
  sys.path.insert(0,str(REPO/'Sources/v3'));import author_sources
  import importlib.util
  spec=importlib.util.spec_from_file_location('animal',R/'animal_redesign.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
  original=author_sources.parts
  def parts(n):
   defs,body=original(n);return m.adjust(n,defs,body)
  author_sources.parts=parts
  raw=author_sources.svg(name);author_sources.parts=original
  s=1.0 # redesign authored directly to final optical target
 root=E.fromstring(raw)
 mask=next((e for e in root.iter() if e.attrib.get('id')=='subjectMask'),None)
 if mask is not None:
  group=E.Element(f'{{{NS}}}g',{'transform':transform(s)})
  for child in list(mask):mask.remove(child);group.append(child)
  mask.append(group) # filters do NOT scale, remain exact native 2.6/13 etc.
 else:
  fg=next((e for e in root.iter() if e.attrib.get('id')=='optical-foreground'),None)
  if fg is not None:fg.set('transform',transform(s)+' '+fg.attrib.get('transform',''))
  else:
   outer=next(e for e in list(root) if e.tag.endswith('g'))
   art=[e for e in list(outer) if not e.tag.endswith('circle')]
   group=E.Element(f'{{{NS}}}g',{'id':'optical-subject','transform':transform(s)})
   for child in art:outer.remove(child);group.append(child)
   outer.append(group)
 return E.tostring(root,encoding='unicode'),src.relative_to(REPO).as_posix()
def sample(arr,x,y):
 x=np.clip(x,0,359);y=np.clip(y,0,359);x0=x.astype(int);y0=y.astype(int);x1=np.minimum(x0+1,359);y1=np.minimum(y0+1,359);fx=(x-x0)[...,None];fy=(y-y0)[...,None]
 return arr[y0,x0]*(1-fx)*(1-fy)+arr[y0,x1]*fx*(1-fy)+arr[y1,x0]*(1-fx)*fy+arr[y1,x1]*fx*fy

def legacy(name,s):
 p=R/'input-large'/f'{name}.png'
 if not p.exists() and name=='bilibili':p=R/'input-large/Bilibili.png'
 im=Image.open(p).convert('RGBA');assert im.size==(360,360),(name,im.size)
 a=np.asarray(im,dtype=float);y,x=np.mgrid[:1440,:1440];dx=(x+.5)/4-180;dy=(y+.5)/4-180
 sx=dx/s;sy=dy/s;rad=np.hypot(sx,sy)
 # Every reviewed reducing legacy asset has a white official/common backdrop.
 # Sample the whole original subject, including near-rim pixels; never clamp
 # radius through a letter/logo (which would smear colored tips radially).
 pixels=sample(a,sx+179.5,sy+179.5)
 if s<1:
  alpha=pixels[...,3:4]/255
  pixels[...,:3]=pixels[...,:3]*alpha+255*(1-alpha)
  pixels[rad>178,:3]=255
 # All source centers are opaque. Alpha comes from fixed final outer disk.
 pixels[...,3]=np.clip((175.125-np.hypot(dx,dy))*4,0,1)*255
 return Image.fromarray(np.round(np.clip(pixels,0,255)).astype('uint8'))

def main():
 p=argparse.ArgumentParser();p.add_argument('--output-dir',type=Path,required=True);p.add_argument('--names',nargs='*');a=p.parse_args();a.output_dir.mkdir(parents=True,exist_ok=True)
 rows=json.loads((R/'optical-plan.json').read_text())['icons'];out=[]
 for row in rows:
  name=row['name']
  if a.names and name not in a.names:continue
  s=row['scale'];n=native(name,s)
  if n:
   raw,source=n;svg=R/'svg'/f'{name}.svg';svg.write_text(raw)
   with tempfile.TemporaryDirectory() as td:
    tmp=Path(td)/'hi.png';subprocess.run(['node',str(REPO/'Sources/v3/render.cjs'),str(svg),str(tmp)],check=True,capture_output=True);hi=Image.open(tmp).convert('RGBA')
   method='native_subject_transform';src='Sources/v5/svg/'+name+'.svg'
  elif s!=1:
   hi=legacy(name,s);method='legacy_uniform_artwork_sampling';src='Sources/v5/input-large/'+('Bilibili' if name=='bilibili' else name)+'.png'
  else:
   hi=None;method='reviewed_no_change';src=None
  for large in [False,True]:
   filename='Bilibili' if large and name=='bilibili' else name
   rel='Icon/Color/'+('Large/' if large else '')+filename+'.png';target=a.output_dir/rel;target.parent.mkdir(parents=True,exist_ok=True)
   if hi is None:target.write_bytes((R/'input-original'/rel).read_bytes())
   else:
    im=hi.resize((360,360) if large else (180,180),Image.Resampling.LANCZOS)
    if not large:
     canvas=Image.new('RGBA',(300,300));canvas.alpha_composite(im,(60,60));im=canvas
    arr=np.array(im);yy,xx=np.mgrid[:im.height,:im.width];c=180 if large else 150;rad=175 if large else 87.5
    # Retain native approved disk-shadow footprint (r180) except official full
    # backgrounds and resampled legacy assets with exact fixed r175 disk.
    if method=='legacy_uniform_artwork_sampling' or name in {'Grok','Peacook','Disney','Scholar'}:
     cov=np.clip(rad+.5-np.hypot(xx+.5-c,yy+.5-c),0,1)*255;arr[...,3]=np.minimum(arr[...,3],np.rint(cov).astype('uint8'))
    arr[arr[...,3]==0]=0;Image.fromarray(arr).save(target,optimize=False)
   out.append({'name':name,'path':rel,'scale':s,'method':method,'source':src,'sha256':sha(target)})
 (a.output_dir/'optical-render-report.json').write_text(json.dumps({'assets':out},indent=2)+'\n');print('Rendered',len(out),'PNGs')
if __name__=='__main__':main()
