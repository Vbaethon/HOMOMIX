"""Whole-collection and official-artwork regression tests for the identity pass."""
from pathlib import Path
import hashlib,json,unittest,xml.etree.ElementTree as E
from PIL import Image,ImageChops
import io,base64,math
R=Path(__file__).resolve().parents[1];S=R/'Sources/v4'
def read(n):return json.loads((S/n).read_text())
def sha(p):
 if str(p).startswith(str(R/'Icon/')):p=R/'Sources/v5/input-original'/p.relative_to(R)
 return hashlib.sha256(p.read_bytes()).hexdigest()
class BrandRevision(unittest.TestCase):
 def test_all_urls_preserved_and_bytes_frozen(self):
  m=read('collection-manifest.json');historical=R/'Sources/v5/input-original';actual={p.relative_to(historical).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (historical/'Icon/Color').rglob('*.png')}
  self.assertEqual(actual,m['files']);self.assertTrue(set(m['baseline_files'])<=set(actual))
  expected={p for p in actual if actual[p]!=m['baseline_files'].get(p)}
  self.assertEqual(expected,{r['path'] for r in m['changes']})
  self.assertEqual({Path(r['path']).stem for r in m['changes'] if r['kind']=='added'},{'Grok','Gemini','DeepSeek'})
 def test_official_exports_and_pairs(self):
  m=read('render-manifest.json');names=(S/'names.txt').read_text().split()
  self.assertEqual(len(m['assets']),2*len(names))
  for row in m['assets']:
   self.assertEqual(sha(R/row['path']),row['new_sha256']);self.assertEqual(sha(R/row['native_source']),row['native_source_sha256'])
   with Image.open(R/row['path']) as im:self.assertEqual(list(im.size),row['dimensions'])
   t=E.fromstring((R/row['native_source']).read_bytes())
   self.assertFalse(any(el.attrib.get('id')=='inkFinish' for el in t.iter()),'Official marks must not gain generic inner shadows')
   for el in t.iter():
    self.assertFalse(el.tag.endswith('text'))
    for k,v in el.attrib.items():
     if k.endswith('href'):self.assertTrue(v.startswith(('data:image/','#')))
 def test_distinct_balance_shapes_and_panda_anatomy(self):
  self.assertEqual(len({sha(R/'Icon/Color'/f'{n}.png') for n in ['Load_balancing','Load_balancing_2','Load_balancing_3']}),3)
  s=R/'Sources/v3/svg'
  for n in ['Panda','Panda_ai']:
   raw=(s/f'{n}.svg').read_text();self.assertIn('rotate(28 139 181)',raw);self.assertIn('rotate(-28 221 181)',raw)
   series={r['name']:r['series'] for r in json.loads((R/'Sources/v3/SERIES-49.json').read_text())['items']}
   self.assertEqual(series[n],'system_graphite')
 def test_audit_covers_every_published_png(self):
  rows=read('OFFICIAL-AUDIT.json')['items'];paths=[p for r in rows for p in r['paths']]
  self.assertEqual(len(paths),len(set(paths)))
  self.assertEqual(set(paths),{p.relative_to(R/'Sources/v5/input-original').as_posix() for p in (R/'Sources/v5/input-original/Icon/Color').rglob('*.png')})
  self.assertTrue(all(r['status'] for r in rows))
 def test_official_backgrounds_fill_circular_outline_without_white_frame(self):
  for n in ['Grok','Peacook','Disney','Scholar']:
   t=E.fromstring((S/'svg'/f'{n}.svg').read_bytes())
   self.assertFalse(any(e.tag.endswith('filter') for e in t.iter()),n)
   bg=next(e for e in t.iter() if e.attrib.get('id')=='official-background')
   self.assertEqual(bg.attrib['r'],'175')
   self.assertEqual(bg.attrib['fill'],{'Grok':'#000000','Peacook':'#181818','Disney':'#FAF9F6','Scholar':'#FFFFFF'}[n])
   with Image.open(R/'Icon/Color/Large'/f'{n}.png') as im:
    a=im.convert('RGBA').getchannel('A')
    self.assertTrue(all(a.getpixel((x,y))==0 for y in range(360) for x in range(360) if math.hypot(x+.5-180,y+.5-180)>176))
 def test_original_background_and_logo_pixels_are_untouched(self):
  for n,file in [('Grok','Grok-symbol.png'),('Peacook','Peacook.png'),('Disney','Disney-company-original.png'),('Scholar','Scholar.png')]:
   t=E.fromstring((S/'svg'/f'{n}.svg').read_bytes());node=next(e for e in t.iter() if e.tag.endswith('image'))
   data=base64.b64decode(node.attrib['href'].split(',',1)[1])
   with Image.open(io.BytesIO(data)) as embedded,Image.open(S/'official'/file) as original:
    self.assertEqual(embedded.convert('RGBA').tobytes(),original.convert('RGBA').tobytes(),n)
  with Image.open(S/'official/Grok.webp') as original,Image.open(S/'official/Grok-symbol.png') as symbol:
   diff=ImageChops.difference(original.convert('RGB'),symbol.convert('RGB')).convert('L')
   diff=ImageChops.multiply(diff,symbol.getchannel('A').point(lambda a:255 if a else 0))
   self.assertIsNone(diff.getbbox(),'Grok foreground source colors changed')
 def test_deepseek_paths_unchanged_and_optically_adjusted(self):
  source=E.fromstring((S/'official/DeepSeek.svg').read_bytes());t=E.fromstring((S/'svg/DeepSeek.svg').read_bytes())
  self.assertEqual([e.attrib['d'] for e in source.iter() if e.tag.endswith('path')],[e.attrib['d'] for e in t.iter() if e.tag.endswith('path')])
  inner=next(e for e in list(next(e for e in list(t) if e.tag.endswith('g'))) if e.tag.endswith('svg'))
  self.assertEqual((inner.attrib['x'],inner.attrib['y'],inner.attrib['width'],inner.attrib['height']),('80','90','236','181'))
if __name__=='__main__':unittest.main()
