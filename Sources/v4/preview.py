"""Contact sheets made exclusively from actual exported production PNGs."""
from pathlib import Path
import math,json,hashlib
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parent;P=R.parents[1]
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
def font(n):return ImageFont.truetype(FONT,n)
def paste(im,path,x,y,size):
 a=Image.open(path).convert('RGBA');a.thumbnail((size,size),Image.Resampling.LANCZOS);im.paste(a,(round(x+(size-a.width)/2),round(y+(size-a.height)/2)),a)
def main():
 names=['Load_balancing','Load_balancing_2','Load_balancing_3','Panda','Panda_ai','Grok','Gemini','DeepSeek','AdblockPlus_2','Microsoft','Disney','Disney_plus','Disney_Channel','UBISOFT','Peacook','Scholar']
 im=Image.new('RGB',(1120,1300),'#F0F3F7');d=ImageDraw.Draw(im);d.text((24,16),'HOMOMIX · 本轮实际效果',font=font(30),fill='#172B40');d.text((24,63),'统一圆形 / 官方背景直接铺满 / 每格底部为默认 60px 实图',font=font(20),fill='#607185')
 for i,n in enumerate(names):
  x=i%4*280;y=110+i//4*295;paste(im,P/'Icon/Color/Large'/f'{n}.png',x+50,y,180);d.text((x+22,y+187),n,font=font(18),fill='#172B40');paste(im,P/'Icon/Color'/f'{n}.png',x+110,y+222,60)
 im.save(R/'qa/revision-actual-overview.png')
 rows=json.loads((R/'OFFICIAL-AUDIT.json').read_text())['items'];cw,ch=150,172;cols=12
 im=Image.new('RGB',(cols*cw,100+math.ceil(len(rows)/cols)*ch),'#F0F3F7');d=ImageDraw.Draw(im);d.text((22,16),'HOMOMIX · 全量实际图标审查',font=font(30),fill='#172B40');d.text((22,60),'177 个规范名称 + Claud 兼容别名 + 2 个 FDS 版本；官方来源未能确认项见随包清单',font=font(20),fill='#607185')
 for i,row in enumerate(rows):
  x=i%cols*cw;y=100+i//cols*ch;path=next((p for p in row['paths'] if '/Large/' in p),row['paths'][0]);paste(im,P/path,x+10,y,130);label=row['name'];label=label if len(label)<21 else label[:18]+'…';d.text((x+6,y+137),label,font=font(12),fill='#172B40')
 im.save(R/'qa/full-collection-overview.png')
 records=[]
 for row in rows:
  for p in row['paths']:records.append({'path':p,'sha256':hashlib.sha256((P/p).read_bytes()).hexdigest()})
 (R/'qa/preview-inputs.json').write_text(json.dumps(records,indent=2)+'\n')
if __name__=='__main__':main()
