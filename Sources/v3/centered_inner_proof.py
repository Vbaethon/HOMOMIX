from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
S=Path(__file__).resolve().parent;R=S.parents[1];font=lambda n:ImageFont.truetype(str(S/'references/Homomix-QA-CJK.otf'),n)
im=Image.new('RGB',(920,1510),'#EEF1F5');d=ImageDraw.Draw(im);d.text((20,14),'内阴影居中、柔和、淡一点',font=font(27),fill='#203049');d.text((20,55),'只调整内部边缘效果；外阴影、主体、配色与白底均不变。',font=font(17),fill='#526177');d.text((20,82),'完整导出PNG大图展示；右侧为实际60px。',font=font(15),fill='#526177')
for i,(n,label) in enumerate([('Link','连接'),('Settings','设置'),('Pig','猪'),('Network','网络')]):
 y=125+i*335
 for j,p in enumerate([S/'references/before-centered-inner'/f'{n}.png',R/'Icon/Color/Large'/f'{n}.png']):
  x=12+j*305;c=Image.open(p).convert('RGBA').resize((280,280),Image.Resampling.LANCZOS);im.paste(c,(x,y),c);d.text((x+15,y+280),['原内阴影','居中柔化内阴影'][j],font=font(19),fill='#203049')
 d.text((20,y+307),label+' '+n,font=font(15),fill='#526177')
 for k,sub in enumerate(['','Large']):
  c=Image.open(R/'Icon/Color'/sub/f'{n}.png').convert('RGBA').resize((60,60),Image.Resampling.LANCZOS)
  for z,bg in enumerate(['#FFFFFF','#E3E8EE']):
   x=655+k*140;yy=y+35+z*115;d.rectangle((x-10,yy-10,x+70,yy+70),fill=bg);im.paste(c,(x,yy),c)
 d.text((638,y+255),'默认 60px',font=font(14),fill='#526177');d.text((782,y+255),'大图 60px',font=font(14),fill='#526177')
d.text((20,1470),'内阴影无位移，模糊2.6、不透明度12%；外阴影完全不变。',font=font(15),fill='#526177')
im.save(S/'qa/centered-inner-before-after.png')
