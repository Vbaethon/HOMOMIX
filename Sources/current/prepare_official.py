"""Reproduce transparent-background extraction and component crops.

No new logo geometry is drawn. Original downloaded assets remain beside the
derived components. Disney company mark: solve the original uniform warm
paper/black antialias blend, retaining the original #121212 foreground.
"""
from pathlib import Path
import xml.etree.ElementTree as E
import numpy as np
from PIL import Image,ImageChops
R=Path(__file__).resolve().parent/'official/native'

def main():
    a=np.array(Image.open(R/'Disney-company-original.png').convert('RGB')).astype(float)
    paper=np.array([250,249,246.]);ink=np.array([18,18,18.]);v=paper-ink
    alpha=np.clip(((paper-a)*v).sum(2)/(v*v).sum(),0,1)
    out=np.empty((*alpha.shape,4),dtype=np.uint8);out[:,:,:3]=18
    out[:,:,3]=np.round(alpha*255).astype('uint8');out[out[:,:,3]==0,:3]=0
    im=Image.fromarray(out);im.crop(im.getchannel('A').getbbox()).save(R/'Disney.png')
    raw=Image.open(R/'Disney-channel-plus-original.png').convert('RGBA')
    crop=raw.crop((0,0,480,260))
    mask=ImageChops.difference(crop.convert('RGB'),Image.new('RGB',crop.size,'white')).convert('L').point(lambda p:255 if p>30 else 0)
    mask=ImageChops.multiply(mask,crop.getchannel('A'))
    crop.crop(mask.getbbox()).save(R/'Disney_Channel.png')
    tree=E.fromstring((R/'AdblockPlus-lockup-original.svg').read_bytes())
    # First six untouched paths are the official octagon and its ABP letters.
    assert len(tree)==7
    tree.remove(list(tree)[6]);tree.set('viewBox','0 0 33 33');tree.set('width','33');tree.set('height','33')
    (R/'AdblockPlus_2.svg').write_bytes(E.tostring(tree))

if __name__=='__main__':main()
