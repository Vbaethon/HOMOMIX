from pathlib import Path
import json,math,argparse
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parent;ROOT=R.parents[1];F='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
def font(n):return ImageFont.truetype(F,n)
def paste(c,p,x,y,size):
 im=Image.open(p).convert('RGBA').resize((size,size),Image.Resampling.LANCZOS);c.paste(im,(x,y),im)
def main():
 p=argparse.ArgumentParser();p.add_argument('--render',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(exist_ok=True,parents=True)
 aliases=json.loads((ROOT/'icon_aliases.json').read_text());names=sorted([p.stem for p in (a.render/'Icon/Color').glob('*.png') if p.name not in aliases],key=str.casefold)
 im=Image.new('RGB',(1560,100+math.ceil(len(names)/12)*130),'#E9EDF2');d=ImageDraw.Draw(im);d.text((20,15),'HOMOMIX · 集中主体与统一留白 · 实际全套',font=font(26),fill='#142739');d.text((20,56),f'{len(names)}款规范展示 / 圆背景固定 / 原创块面化 / 官方保持身份',font=font(17),fill='#526376')
 for i,n in enumerate(names):
  x=i%12*130;y=100+i//12*130;f='Bilibili' if n=='bilibili' else n;paste(im,a.render/'Icon/Color/Large'/f'{f}.png',x+20,y,90);d.text((x+4,y+97),n[:21],font=font(10),fill='#142739')
 im.save(a.out/'full-overview.png')
 generic=set((ROOT/'Sources/v3/generic-names.txt').read_text().split());g=[n for n in names if n in generic];b=[n for n in names if n not in generic];mixed=[]
 while g or b:
  if b:mixed.append(b.pop(0))
  if g:mixed.append(g.pop(0))
 for page in range(math.ceil(len(mixed)/48)):
  part=mixed[page*48:(page+1)*48];im=Image.new('RGB',(1200,100+math.ceil(len(part)/6)*125),'#E9EDF2');d=ImageDraw.Draw(im);d.text((18,12),f'跨类别主体对照 {page+1}/4 · 圆盘实际36px',font=font(25),fill='#142739');d.text((18,52),'每格左为v8旧版，右为集中/统一版；官方与原创相邻检查',font=font(17),fill='#526376')
  for i,n in enumerate(part):
   x=i%6*200;y=100+i//6*125;f='Bilibili' if n=='bilibili' else n
   paste(im,R/'input-v8/Icon/Color/Large'/f'{f}.png',x+35,y+5,36);paste(im,a.render/'Icon/Color/Large'/f'{f}.png',x+125,y+5,36)
   paste(im,a.render/'Icon/Color/Large'/f'{f}.png',x+75,y+50,52);d.text((x+5,y+105),n[:24],font=font(11),fill='#142739')
  im.save(a.out/f'cross-before-after-{page+1}.png')
 (a.out/'manifest.json').write_text(json.dumps({'names':names,'cross_order':mixed,'count':len(names)},indent=2))
if __name__=='__main__':main()
