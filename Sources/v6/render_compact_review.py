from pathlib import Path
import re,subprocess
from PIL import Image,ImageDraw,ImageFont
from compact_originals import adjust,NAMES
NAMES=NAMES[:8]
R=Path(__file__).resolve().parents[2];out=R/'Sources/v6/compact-review';out.mkdir(exist_ok=True)
f=lambda n:ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',n)
for name in NAMES:
 src=R/'Sources/v4/svg'/f'{name}.svg'
 if not src.exists():src=R/'Sources/v3/svg'/f'{name}.svg'
 s=src.read_text();defs,body=adjust(name,'','')
 s=re.sub(r'<mask id="subjectMask".*?</mask>',f'<mask id="subjectMask" maskUnits="userSpaceOnUse" x="0" y="0" width="360" height="360">{body}</mask>',s,flags=re.S).replace('</defs>',defs+'</defs>')
 (out/f'{name}.svg').write_text(s)
 subprocess.run(['node',str(R/'Sources/v3/render.cjs'),str(out/f'{name}.svg'),str(out/f'{name}-hi.png')],check=True,capture_output=True)
 Image.open(out/f'{name}-hi.png').resize((360,360),Image.Resampling.LANCZOS).save(out/f'{name}.png')
im=Image.new('RGB',(1040,650),'#e9edf2');d=ImageDraw.Draw(im);d.text((18,12),'集中块面样板 · 每组左旧 / 右新；90px检查 + 实际36px',font=f(22),fill='#142739')
for i,name in enumerate(NAMES):
 x=i%4*260;y=65+i//4*285;d.text((x+12,y),name,font=f(17),fill='#142739')
 for j,path in enumerate([R/'Icon/Color/Large'/f'{name}.png',out/f'{name}.png']):
  a=Image.open(path).convert('RGBA')
  for size,dy in [(90,35),(36,175)]:
   b=a.resize((size,size),Image.Resampling.LANCZOS);im.paste(b,(x+20+j*125+(90-size)//2,y+dy),b)
  d.text((x+38+j*125,y+137),'修改前' if j==0 else '集中版',font=f(14),fill='#526376')
im.save(out/'集中块面_前后对照.png')
