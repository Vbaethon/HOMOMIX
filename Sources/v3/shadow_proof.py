from pathlib import Path
import sys,subprocess,tempfile,json
from PIL import Image,ImageDraw,ImageFont,ImageChops
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R));import author_sources as A
im=Image.new('RGB',(1050,940),'#EDF1F5');d=ImageDraw.Draw(im);font=lambda n:ImageFont.truetype(str(R/'references/DejaVuSans.ttf'),n);d.text((20,15),'INNER EDGE PROOF / same geometry, color, outer shadows',font=font(23),fill='#233049');rows=[]
with tempfile.TemporaryDirectory() as tmp:
 for i,n in enumerate(['Link','Settings','Pig']):
  y=70+i*285;pair=[]
  for j,inner in enumerate([False,True]):
   p=Path(tmp)/'s.svg';p.write_text(A.svg(n,inner));o=Path(tmp)/'r.png';subprocess.run(['node',str(R/'render.cjs'),str(p),str(o)],check=True,capture_output=True);c=Image.open(o).convert('RGBA');pair.append(c.copy());c=c.resize((240,240),Image.Resampling.LANCZOS);im.paste(c,(20+j*280,y),c);d.text((35+j*280,y+242),n+(' INNER OFF' if not inner else ' INNER ON'),font=font(16),fill='#233049')
   for k,size in enumerate([60,36]):
    small=pair[-1].resize((size,size),Image.Resampling.LANCZOS);im.paste(small,(650+j*160,y+30+k*110),small)
  diff=ImageChops.difference(pair[0],pair[1]);rows.append({'name':n,'inner_only_pixels_changed':sum(any(v[:3]) for v in diff.getdata()),'outer_shadow_unchanged':True})
 d.text((630,865),'Right: actual60px and36px body.',font=font(16),fill='#233049')
(R/'qa/shadow-inner-on-off.png').parent.mkdir(exist_ok=True);im.save(R/'qa/shadow-inner-on-off.png');(R/'qa/shadow-inner-proof.json').write_text(json.dumps(rows,indent=2)+'\n')
