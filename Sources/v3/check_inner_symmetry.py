from pathlib import Path
import tempfile,subprocess,json,xml.etree.ElementTree as E
import numpy as np
from PIL import Image
from material import filters
R=Path(__file__).resolve().parent;NS={'s':'http://www.w3.org/2000/svg'}
raw=f'<svg xmlns="http://www.w3.org/2000/svg" width="360" height="360"><defs>{filters()}</defs><circle cx="180" cy="180" r="110" fill="white" filter="url(#inkFinish)"/></svg>'
t=E.fromstring(raw);f=t.find('s:defs/s:filter[@id="inkFinish"]',NS);m=f.find('s:feMerge',NS)
for child in list(m):
 if child.attrib.get('in') not in ['depth','light']:m.remove(child)
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp)/'fixture.svg';p.write_bytes(E.tostring(t));o=Path(tmp)/'fixture.png';subprocess.run(['node',str(R/'render.cjs'),str(p),str(o)],check=True,capture_output=True);a=np.array(Image.open(o).convert('RGBA'))[:,:,3].astype(int)
 dx=int(np.abs(a-a[:,::-1]).max());dy=int(np.abs(a-a[::-1,:]).max());yy,xx=np.indices(a.shape);cx=float((a*xx).sum()/a.sum());cy=float((a*yy).sum()/a.sum());hx=float(np.abs(a-a[:,::-1]).sum()/a.sum());hy=float(np.abs(a-a[::-1,:]).sum()/a.sum());assert abs(cx-719.5)/4<.05 and abs(cy-719.5)/4<.05;assert hx<.005 and hy<.005
 yy,xx=np.indices(a.shape);outside=np.hypot((xx+.5)/4-180,(yy+.5)/4-180)>111;assert int(a[outside].max())==0
 report={'status':'pass','fixture':'centered circle native360 rendered1440; onlyinnerdepth/highlight merged','horizontal_reflection_max_alpha_delta':dx,'vertical_reflection_max_alpha_delta':dy,'outside_subject_alpha_max':int(a[outside].max()),'inner_max_alpha':int(a.max()),'centroid_offset_native':[(cx-719.5)/4,(cy-719.5)/4],'reflection_alpha_relative_L1':[hx,hy],'raster_note':'Local edge quantization can differ by a few alpha levels; normalized reflection error and centroid establish no meaningful directional shift.','inner_has_spatial_offset':False,'outer_shadow_excluded_only_for_diagnostic':True};(R/'qa/inner-symmetry.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
