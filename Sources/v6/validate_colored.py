import sys,json
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
r=Path(__file__).resolve().parent;sys.path.insert(0,str(r));import raster_colored as m
old={x['name']:x['scale'] for x in json.load(open(r.parent/'v5/optical-plan.json'))['icons']};new={x['name']:x['relative_to_v8_scale'] for x in json.load(open(r/'full-optical-review.json'))['icons']}
results=[];sheet=Image.new('RGB',(1200,180*5),'#dfe3e8');d=ImageDraw.Draw(sheet)
for i,n in enumerate(m.NAMES):
 fg,bg,orig,meta=m._layers(n);scale=old[n]*new[n];one=np.asarray(m.render(n,1)).astype(float);im=m.render(n,scale);out=np.asarray(im);alpha=np.asarray(fg)[:,:,3]
 y,x=np.mgrid[:360,:360];ring=(np.hypot(x-179.5,y-179.5)>170)&(orig[:,:,3]>250)
 result={'name':n,'candidate_source_scale':scale,'alpha_identical':bool(np.array_equal(out[:,:,3],orig[:,:,3])),'identity_rgb_max_error_opaque':float(abs(one[:,:,:3]-orig[:,:,:3])[orig[:,:,3]>250].max()),'unchanged_visible_background_max_error':float(abs(out[:,:,:3].astype(float)-orig[:,:,:3])[ring&(alpha==0)].max()),'note':'target scale is old v5 scale times visual relative proposal, not final approval'};results.append(result)
 assert result['alpha_identical'];assert result['unchanged_visible_background_max_error']<=1
 im.save(r/'qa/colored'/f'{n}-target.png');xx=i%4*300;yy=i//4*180;d.text((xx+5,yy+5),n+f'  original / target {scale:.3f}',fill='black')
 for j,src in enumerate([Image.fromarray(orig.astype('uint8')),im]):
  thumb=src.resize((120,120),Image.Resampling.LANCZOS);sheet.paste(thumb,(xx+5+j*145,yy+25),thumb);sm=src.resize((36,36),Image.Resampling.LANCZOS);sheet.paste(sm,(xx+45+j*145,yy+145),sm)
sheet.save(r/'qa/colored/target-before-after.png');(r/'qa/colored/validation.json').write_text(json.dumps(results,indent=2));print('17 alpha and fixed outer backdrop tests passed');print('max identity error',max(x['identity_rgb_max_error_opaque'] for x in results))
