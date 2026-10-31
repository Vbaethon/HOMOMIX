"""Historical v8 optical locks against the immutable v6/input-v8 snapshot.
Catalog/alias checks remain live compatibility invariants, not v8 image locks.
"""
import hashlib,json,unittest,xml.etree.ElementTree as E
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1];S=R/'Sources/v5';H=R/'Sources/v6/input-v8'
def j(n):return json.loads((S/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
class OpticalRevision(unittest.TestCase):
 def test_historical_collection_and_explicit_delete(self):
  m=j('collection-manifest.json');actual={p.relative_to(H).as_posix():sha(p) for p in (H/'Icon/Color').rglob('*.png')}
  self.assertEqual(actual,m['files']);self.assertEqual(len(actual),356)
  self.assertEqual(set(m['baseline_files'])-set(actual),{'Icon/Color/Claud.png','Icon/Color/Large/Claud.png'})
  self.assertFalse((R/'Icon/Color/Claud.png').exists());self.assertFalse((R/'Icon/Color/Large/Claud.png').exists())
 def test_every_standard_name_reviewed_and_exact_export(self):
  rows=j('optical-plan.json')['icons'];assets=j('render-manifest.json')['assets']
  self.assertEqual(len(rows),177);self.assertEqual(len(assets),354)
  self.assertEqual({r['name'] for r in rows},{r['name'] for r in assets})
  for row in assets:
   self.assertEqual(sha(H/row['path']),row['sha256'])
   with Image.open(H/row['path']) as im:self.assertEqual(im.size,(360,360) if '/Large/' in row['path'] else (300,300))
  self.assertTrue(all(.85<=r['scale']<=1.2 for r in rows))
 def test_native_geometry_preserved_except_requested_animals(self):
  for p in (S/'svg').glob('*.svg'):
   src=R/'Sources/v4/svg'/p.name
   if not src.exists():src=R/'Sources/v3/svg'/p.name
   a=E.parse(src);b=E.parse(p)
   if p.stem not in {'Fish','Fish_b','Dolphin','Globefish'}:
    self.assertEqual([e.attrib.get('d') for e in a.iter() if e.tag.endswith('path')],[e.attrib.get('d') for e in b.iter() if e.tag.endswith('path')],p.stem)
   self.assertEqual([e.attrib for e in a.iter() if e.tag.endswith(('feGaussianBlur','feOffset','feFlood'))],[e.attrib for e in b.iter() if e.tag.endswith(('feGaussianBlur','feOffset','feFlood'))],p.stem)
   self.assertFalse(any(e.tag.endswith('text') for e in b.iter()))
 def test_actual_full_audit_paths(self):
  a=j('current-audit.json');paths=[p for r in a['items'] for p in r['paths']]
  self.assertEqual(len(paths),len(set(paths)));self.assertEqual(set(paths),set(j('collection-manifest.json')['files']))
  self.assertEqual(a['unconfirmed_names'],['bilibili','Bilibili_blue','Bilibili_Global','Omission','Onlyfans','Pornhub','Seancody','xHamster','Zune'])
 def test_no_exact_duplicate_display(self):
  from generate_catalog import build_catalog
  catalog=build_catalog(R);default=[r for r in catalog['icons'] if '/Large/' not in r['url'] and '/FDS/' not in r['url']]
  hashes=[hashlib.sha256(Image.open(R/'Icon/Color'/r['name']).convert('RGBA').tobytes()).hexdigest() for r in default]
  self.assertEqual(len(hashes),len(set(hashes)));self.assertEqual(len(hashes),172)
 def test_overview_matches_canonical_catalog(self):
  from generate_catalog import build_catalog
  names={Path(x['name']).stem for x in build_catalog(R)['icons'] if '/Large/' not in x['url'] and '/FDS/' not in x['url']}
  m=j('qa/preview-manifest.json');self.assertEqual(set(m['overview_names']),names);self.assertEqual(m['overview_count'],172)
  for x in m['input_files']:self.assertEqual(sha(H/x['path']),x['sha256'])
 def test_background_roundness_and_source_identity(self):
  for n in ['Grok','Peacook','Disney','Scholar']:
   a=E.parse(R/'Sources/v4/svg'/f'{n}.svg');b=E.parse(S/'svg'/f'{n}.svg')
   self.assertEqual([e.attrib['href'] for e in a.iter() if e.tag.endswith('image')],[e.attrib['href'] for e in b.iter() if e.tag.endswith('image')])
   bg=next(e for e in b.iter() if e.attrib.get('id')=='official-background');self.assertEqual(bg.attrib['r'],'175')
   with Image.open(H/'Icon/Color/Large'/f'{n}.png') as im:
    for pos in [(0,0),(359,0),(0,359),(359,359)]:self.assertEqual(im.getpixel(pos)[3],0)
 def test_deepseek_base_optical_center_preserved(self):
  t=E.parse(S/'svg/DeepSeek.svg');art=next(e for e in t.iter() if e.tag.endswith('svg') and 'x' in e.attrib)
  self.assertEqual((art.attrib['x'],art.attrib['y']),('80','90'))
  group=next(e for e in t.iter() if e.attrib.get('id')=='optical-subject');self.assertIn('translate(180 180)',group.attrib['transform'])
 def test_fish_shapes_not_mirrored_duplicates(self):
  f=E.parse(S/'svg/Fish.svg');b=E.parse(S/'svg/Fish_b.svg')
  self.assertNotEqual([e.attrib.get('d') for e in f.iter() if e.tag.endswith('path')],[e.attrib.get('d') for e in b.iter() if e.tag.endswith('path')])
  self.assertNotEqual(sha(H/'Icon/Color/Fish.png'),sha(H/'Icon/Color/Fish_b.png'))
if __name__=='__main__':unittest.main()
