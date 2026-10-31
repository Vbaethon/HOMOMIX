from pathlib import Path
from collections import Counter
import hashlib,json,unittest,xml.etree.ElementTree as E
from PIL import Image
R=Path(__file__).resolve().parents[1];S=R/'Sources/v3';NS={'s':'http://www.w3.org/2000/svg'}
def read(n):return json.loads((S/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
class InverseFull(unittest.TestCase):
 def test_taxonomy_and_series(self):
  rows=read('TAXONOMY-174.json')['items'];self.assertEqual(Counter(x['category'] for x in rows),{'inverse_generic':49,'preserved_approved_theme_exception':4,'baseline_brand_character_flag_or_named_theme':121})
  series=read('SERIES-49.json')['items'];self.assertEqual(len({r['name'] for r in series}),49);self.assertEqual(sum(x['series']=='system_graphite' for x in series),13)
 def test_approved_theme_outputs(self):
  for row in read('references/approved-brand-exceptions/expected-outputs.json'):self.assertEqual(sha(R/row['path']),row['sha256'])
  for p in (S/'references/approved-brand-exceptions').glob('*.svg'):self.assertEqual(p.read_bytes(),(S/'svg'/p.name).read_bytes())
 def test_white_disk_and_real_inner_layers(self):
  for n in (S/'generic-names.txt').read_text().split():
   t=E.fromstring((S/'svg'/f'{n}.svg').read_bytes());self.assertEqual(t.find('s:g/s:circle',NS).attrib['fill'],'#FFFFFF')
   filt=t.find('s:defs/s:filter[@id="inkFinish"]',NS);results={x.attrib.get('result') for x in filt};self.assertTrue({'depth','light','cast'}.issubset(results));self.assertIsNotNone(t.find('s:defs/s:filter[@id="diskShadow"]',NS))
 def test_hues_and_holes(self):
  family={r['name']:r['series'] for r in read('SERIES-49.json')['items']};rows=read('qa/validation.json')['items'];self.assertEqual(len(rows),49)
  for row in rows:
   if family[row['name']]!='system_graphite':self.assertGreaterEqual(row['significant_30degree_hue_bins'],3,row['name'])
  for row in read('qa/interior-topology.json')['icons']:
   for h in row['enclosed_negative_components']:self.assertGreaterEqual(h['area_native_px'],300,row['name'])
 def test_inner_proof_and_shadow_margins(self):
  for row in read('qa/shadow-inner-proof.json'):self.assertGreater(row['inner_only_pixels_changed'],1000);self.assertTrue(row['outer_shadow_unchanged'])
  for n in (S/'generic-names.txt').read_text().split():
   with Image.open(R/'Icon/Color/Large'/f'{n}.png') as im:a=im.getchannel('A')
   for box in [(0,0,360,1),(0,359,360,360),(0,0,1,360),(359,0,360,360)]:self.assertIsNone(a.crop(box).getbbox(),n)
 def test_baseline_workflows(self):
  for row in read('WORKFLOW-BASELINE.json'):self.assertEqual(sha(R/row['path']),row['sha256'])
if __name__=='__main__':unittest.main()
