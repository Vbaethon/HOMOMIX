"""Experimental original Sony raster separation; Xbox explicitly not separable.
No production writes. Inpainted hidden Sony background is approximate, not official.
"""
from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import binary_dilation,binary_fill_holes,label
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve
R=Path(__file__).resolve().parent

def sony_layers():
 a=np.asarray(Image.open(R.parent/'v5/input-large/Sony_Live.png').convert('RGBA'));rgb=a[:,:,:3].astype(float);r,g,b=rgb.transpose(2,0,1);y,x=np.mgrid[:360,:360]
 white=(y<120)&(r>170)&(g>170)&(b>170)
 yellow=(y>215)&(y<341)&(x>85)&(x<280)&(r>150)&(g>80)&((b<r*.72)|(g>r*.85))
 core=white|yellow
 labs,num=label(core);sizes=np.bincount(labs.ravel());core=core&(sizes[labs]>8)
 mask=binary_dilation(core,iterations=2);mask=binary_fill_holes(mask)
 # Restore actual letter holes (O, etc.) rather than painting hole colors as strokes.
 # For scaling the complete glyph group, original interior colors stay with glyph.
 # Solve Laplace interpolation only in removed letter support; visible flow unchanged.
 points=np.argwhere(mask);ids=np.full((360,360),-1,int);ids[mask]=np.arange(len(points));mat=lil_matrix((len(points),len(points)));rhs=np.zeros((len(points),3))
 for i,(yy,xx) in enumerate(points):
  mat[i,i]=4
  for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)):
   ny,nx=yy+dy,xx+dx
   if mask[ny,nx]:mat[i,ids[ny,nx]]=-1
   else:rhs[i]+=rgb[ny,nx]
 bg=rgb.copy();bg[mask]=spsolve(mat.tocsr(),rhs)
 fg=np.dstack([rgb,mask*255]).astype('uint8')
 return a,bg,Image.fromarray(fg)

def render(name,scale,dx=0,dy=0):
 if name=='Xbox':raise ValueError('Xbox is an intact transparent official sphere foreground. Use special_official.render to scale the whole sphere on the standard white circle; do not separate or fabricate its X grooves.')
 if name!='Sony_Live':raise KeyError(name)
 orig,bg,fg=sony_layers();s=round(360*scale);fg=fg.resize((s,s),Image.Resampling.LANCZOS)
 out=Image.fromarray(np.dstack([np.rint(bg),np.full((360,360),255)]).clip(0,255).astype('uint8'));out.alpha_composite(fg,(round((360-s)/2+dx),round((360-s)/2+dy)));arr=np.array(out);arr[:,:,3]=orig[:,:,3];arr[arr[:,:,3]==0]=0;return Image.fromarray(arr)

def main():
 out=R/'qa/separate-special';out.mkdir(parents=True,exist_ok=True);orig,bg,fg=sony_layers();im=render('Sony_Live',.88);im.save(out/'Sony_Live-candidate.png');fg.save(out/'Sony_Live-matte.png');Image.fromarray(np.dstack([bg,orig[:,:,3]]).clip(0,255).astype('uint8')).save(out/'Sony_Live-reconstructed-background.png')
 c=Image.new('RGB',(900,410),'#dfe3e8');d=ImageDraw.Draw(c)
 for i,(n,src) in enumerate([('Original',Image.fromarray(orig)),('Candidate .88',im),('Recovered background',Image.open(out/'Sony_Live-reconstructed-background.png'))]):
  src=src.resize((280,280),Image.Resampling.LANCZOS);c.paste(src,(i*300+10,25),src);d.text((i*300+10,5),n,fill='black');sm=src.resize((36,36),Image.Resampling.LANCZOS);c.paste(sm,(i*300+120,325),sm)
 c.save(out/'Sony_Live-before-after.png')
 provenance=json.load(open(R/'official-special/provenance.json'));xbox=next(x for x in provenance if x['name']=='Xbox');x=Image.open(R/'official-special/Xbox.png').convert('RGBA')
 # Keep curated provenance decisions; preview regeneration must not revert approved source interpretation.
 report=json.loads((out/'report.json').read_text())
 (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
