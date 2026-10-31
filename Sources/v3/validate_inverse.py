from pathlib import Path
import json,subprocess,tempfile,xml.etree.ElementTree as ET
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent;NS={'s':'http://www.w3.org/2000/svg'};rows=[]
with tempfile.TemporaryDirectory() as tmp:
 for n in (R/'generic-names.txt').read_text().split():
  t=ET.fromstring((R/'svg'/f'{n}.svg').read_bytes());disk=t.find('s:g/s:circle',NS);assert disk.attrib['fill']=='#FFFFFF';t.find('s:g',NS).remove(disk);fg=t.find('s:g/s:g',NS);fg.attrib.pop('filter');src=Path(tmp)/'f.svg';src.write_bytes(ET.tostring(t));out=Path(tmp)/'f.png';subprocess.run(['node',str(R/'render.cjs'),str(src),str(out)],check=True,capture_output=True)
  im=Image.open(out).convert('RGBA');a=np.array(im);hsv=np.array(im.convert('RGB').convert('HSV'));valid=a[:,:,3]>250;bins=np.bincount(hsv[:,:,0][valid].astype(int)*12//256,minlength=12);strong=int(np.count_nonzero(bins>valid.sum()*.035))
  rgb=a[valid,:3]/255;linear=np.where(rgb<=.04045,rgb/12.92,((rgb+.055)/1.055)**2.4);lum=linear@np.array([.2126,.7152,.0722]);contrast=1.05/(lum+.05)
  rows.append({'name':n,'significant_30degree_hue_bins':strong,'hue_bin_percent':[round(float(v)/valid.sum()*100,2) for v in bins],'subject_pixels_contrast3_on_white_percent':round(float((contrast>=3).mean()*100),2),'subject_pixels_contrast2_on_white_percent':round(float((contrast>=2).mean()*100),2),'disk_fill':'#FFFFFF'})
 (R/'qa/validation.json').write_text(json.dumps({'status':'pass','items':rows},indent=2)+'\n')
 print(json.dumps(rows))
