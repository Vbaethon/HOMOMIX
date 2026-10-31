from pathlib import Path
import json,math,argparse
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parent
F='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
def font(n):return ImageFont.truetype(F,n)
def paste(im,p,x,y,sz):
 a=Image.open(p).convert('RGBA').resize((sz,sz),Image.Resampling.LANCZOS);im.paste(a,(x,y),a)
def main():
 p=argparse.ArgumentParser();p.add_argument('--render',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
 rows=json.loads((R/'optical-plan.json').read_text())['icons'];aliases=json.loads((R.parents[1]/'icon_aliases.json').read_text())
 for page in range(math.ceil(len(rows)/48)):
  part=rows[page*48:(page+1)*48];im=Image.new('RGB',(1200,100+math.ceil(len(part)/6)*130),'#EFF2F6');d=ImageDraw.Draw(im);d.text((20,18),f'全套光学尺寸校准 · {page+1}/4',font=font(24),fill='#192D40');d.text((20,55),'左：调整前　右：调整后　每个圆盘实际约36像素',font=font(17),fill='#526578')
  for i,row in enumerate(part):
   n=row['name'];x=i%6*200;y=100+i//6*130
   paste(im,R/'input-original/Icon/Color'/f'{n}.png',x+25,y,60);paste(im,a.render/'Icon/Color'/f'{n}.png',x+110,y,60)
   d.text((x+8,y+65),n[:24],font=font(12),fill='#192D40');d.text((x+8,y+87),"兼容链接 · 不展示" if n+".png" in aliases else "轮廓重绘" if row.get("action")=="native_geometry_redesign" else f"主体 ×{row['scale']:.2f}",font=font(12),fill='#526578')
  im.save(a.out/f'all-before-after-{page+1}.png')
 # User overview follows the same canonical/alias policy as the catalog.
 rows=[row for row in rows if row['name']+'.png' not in aliases]
 im=Image.new('RGB',(1560,100+math.ceil(len(rows)/12)*130),'#EFF2F6');d=ImageDraw.Draw(im);d.text((20,18),'HOMOMIX · 全套光学尺寸与重复样式校准',font=font(25),fill='#192D40');d.text((20,56),'172款展示图标 · 兼容重复链接不再展示 · 官方长字标保持原有比例',font=font(17),fill='#526578')
 for i,row in enumerate(rows):
  n=row['name'];x=i%12*130;y=100+i//12*130
  p=a.render/'Icon/Color/Large'/('Bilibili.png' if n=='bilibili' else n+'.png');paste(im,p,x+20,y,90);d.text((x+3,y+96),n[:21],font=font(10),fill='#192D40')
 im.save(a.out/'full-optical-overview.png')
if __name__=='__main__':main()
