"""Run from repo root: python Sources/v6/test_raster_pale.py"""
import json
import numpy as np
from PIL import Image
import raster_pale as m

def main():
    records=[]
    yy,xx=np.mgrid[:360,:360];rim=np.hypot(xx-179.5,yy-179.5)>177
    for name in m.available_names():
        original=np.asarray(Image.open(m.ROOT/'Sources/v5/input-large'/f'{name}.png').convert('RGBA'))
        identity=np.asarray(m.render(name,1))
        assert np.array_equal(original,identity),name+' identity'
        rendered=np.asarray(m.render(name,.85))
        assert np.array_equal(original[:,:,3],rendered[:,:,3]),name+' alpha changed'
        assert np.array_equal(original[rim],rendered[rim]),name+' rim changed'
        offset=np.asarray(m.render(name,.85,2,-1))
        assert np.array_equal(original[:,:,3],offset[:,:,3]),name+' offset alpha changed'
        records.append({'name':name,'identity_exact':True,'disc_alpha_exact':True,'rim_exact_at_85pct':True,'offset_disc_alpha_exact':True})
    for name in ['Disney','Disney_Channel','Gemini','Scholar']:
        try:m.render(name,.85)
        except ValueError:pass
        else:raise AssertionError(name+' native not rejected')
    (m.ROOT/'Sources/v6/qa/pale-tests.json').write_text(json.dumps({'passed':len(records),'native_preference':True,'tests':records},indent=2))
    print(f'{len(records)} original-scale identity, disc-alpha, rim and offset checks passed; native assets correctly rejected')

if __name__=='__main__':main()
