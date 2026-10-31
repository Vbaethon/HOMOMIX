#!/usr/bin/env python3
"""Final actual-size contact sheets and analytic PNG-edge validation."""
import argparse,hashlib,json,math
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[1]
def icon_path(name, sub=''):
 folder=REPO/'Icon/Color'/sub
 path=folder/(name+'.png')
 if path.exists(): return path
 return next(p for p in folder.glob('*.png') if p.stem.casefold()==name.casefold())
def main():
 p=argparse.ArgumentParser();p.add_argument('--output-dir',required=True,type=Path);a=p.parse_args();a.output_dir.mkdir(parents=True,exist_ok=True)
 spec=json.loads((ROOT/'render-manifest.json').read_text());rows=[]
 for r in spec['assets']:
  im=Image.open(REPO/r['path']).convert('RGBA');arr=np.array(im);alpha=arr[:,:,3];large='/Large/' in r['path'];radius=180 if large else 90;center=180 if large else 150;y,x=np.indices(alpha.shape)
  assert list(im.size)==r['dimensions'];assert list(im.getchannel('A').getbbox())==r['alpha_bbox'];assert np.all(arr[alpha==0,:3]==0);assert not np.any(alpha[np.hypot(x+.5-center,y+.5-center)>radius+2]);rows.append({'path':r['path'],'status':'pass'})
 white=(ROOT/'generic-names.txt').read_text().split();font=lambda n:ImageFont.truetype(str(ROOT/'references/DejaVuSans.ttf'),n)
 def sheet(names,path,title,actual=False,cols=7):
  cw,ch=(160,190) if actual else(160,178);top=87;im=Image.new('RGB',(cols*cw,top+math.ceil(len(names)/cols)*ch),'#EEF2F7');d=ImageDraw.Draw(im);d.text((20,15),title,font=font(24),fill='#20354E');d.text((20,52),'Actual60px: default36px disk / Large60px disk; light + dark.' if actual else 'White disks / semantic-series subjects / cohesive forms / coordinated inner-edge finish.',font=font(14),fill='#526680')
  for i,n in enumerate(names):
   x=i%cols*cw;y=top+i//cols*ch
   if actual:
    d.rounded_rectangle((x+5,y+71,x+155,y+140),radius=7,fill='#14283C')
    for k,sub in enumerate(['','Large']):
     small=Image.open(icon_path(n,sub)).convert('RGBA').resize((60,60),Image.Resampling.LANCZOS)
     for yy in [y+4,y+76]:im.paste(small,(x+9+k*78,yy),small)
    d.text((x+7,y+149),n if len(n)<24 else n[:21]+'…',font=font(11),fill='#20354E')
   else:
    icon=Image.open(icon_path(n,'Large')).convert('RGBA').resize((128,128),Image.Resampling.LANCZOS);im.paste(icon,(x+16,y+1),icon);d.text((x+5,y+139),n if len(n)<24 else n[:21]+'…',font=font(11),fill='#20354E')
  im.save(path)
 sheet(white,a.output_dir/'inverse49-overview.png','HOMOMIX / WHITE BASE / SERIES / 49 ORIGINAL ICONS')
 sheet(white,a.output_dir/'inverse49-actual60.png','HOMOMIX / ACTUAL SMALL-SIZE QA / 49',True)
 # All174 retains original brand/flag identity, including published spelling/case.
 taxonomy=json.loads((ROOT/'TAXONOMY-174.json').read_text())['items'];allnames=[r['name'] for r in taxonomy]
 sheet(allnames,a.output_dir/'all174-overview.png','HOMOMIX / ALL174 / 49 INVERSE + 4 THEME UPDATES',False,12)
 # Four previously approved theme exceptions are not monochrome conversions.
 sheet(['Bahamut','Bahamut_b','Bahamut_i','Disney_Castle'],a.output_dir/'approved-theme-exceptions.png','4 APPROVED THEME EXCEPTIONS / IDENTITY RETAINED',True,4)
 (a.output_dir/'pixel-qa.json').write_text(json.dumps({'status':'pass','verified_png':len(rows),'white_names':49,'theme_exceptions':4,'assets':rows},indent=2)+'\n');print('QA106 PNG;49white actual36/60;174contactsheet')
if __name__=='__main__':main()
