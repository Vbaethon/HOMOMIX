from pathlib import Path
import re,subprocess,sys
from PIL import Image,ImageDraw,ImageFont
from animal_redesign import adjust,NAMES
root=Path(__file__).resolve().parents[2];out=root/'Sources/v5/animal-review';out.mkdir(exist_ok=True)
font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',14)
for n in NAMES:
 s=(root/f'Sources/v3/svg/{n}.svg').read_text()
 defs,body=adjust(n,'','')
 s=re.sub(r'<mask id="subjectMask".*?</mask>',f'<mask id="subjectMask" maskUnits="userSpaceOnUse" x="0" y="0" width="360" height="360">{body}</mask>',s,flags=re.S)
 s=s.replace('</defs>',defs+'</defs>');(out/f'{n}.svg').write_text(s)
 subprocess.run(['node',str(root/'Sources/v3/render.cjs'),str(out/f'{n}.svg'),str(out/f'{n}-master.png')],check=True)
 im=Image.open(out/f'{n}-master.png');im.resize((360,360),Image.Resampling.LANCZOS).save(out/f'{n}.png')
canvas=Image.new('RGB',(880,420),'#e8edf2');d=ImageDraw.Draw(canvas)
d.text((16,10),'每组左：修改前 ／ 右：修改后。上排90px内容盘；下排实际36px内容盘。',font=font,fill='black')
for i,n in enumerate(NAMES):
 x=20+i*215;d.text((x,45),n,font=font,fill='black')
 for j,im in enumerate([Image.open(root/f'Icon/Color/Large/{n}.png'),Image.open(out/f'{n}.png')]):
  for size,y in [(90,90),(36,230)]:
   a=im.convert('RGBA').resize((size,size),Image.Resampling.LANCZOS);canvas.paste(a,(x+j*100+(90-size)//2,y),a)
 d.text((x+15,190),'修改前',font=font,fill='black');d.text((x+115,190),'修改后',font=font,fill='black')
canvas.save(out/'before-after.png')
