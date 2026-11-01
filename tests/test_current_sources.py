"""Latest-only source closure, source authenticity and present release invariants.
Historical PNG snapshots are intentionally not fixtures: current manifest and a
cold rebuild validate the current output, while Git preserves past versions.
"""
import hashlib
import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as E
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
S=ROOT/'Sources/current'
def j(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def tag(e):return e.tag.rsplit('}',1)[-1]

class CurrentSources(unittest.TestCase):
    def test_only_current_source_tree(self):
        self.assertEqual({p.name for p in (ROOT/'Sources').iterdir() if p.is_dir() and p.name!='__pycache__'},{'current'})
        self.assertTrue((S/'build_unified.py').is_file())
        self.assertFalse((S/'input-v8').exists())
        self.assertFalse((S/'input-original').exists())
        self.assertFalse((S/'compact-review').exists())

    def test_current_names_and_families(self):
        generic=set((S/'generic-names.txt').read_text().split())
        rows=j(S/'SERIES-49.json')['items']
        self.assertEqual(len(generic),49)
        self.assertEqual(generic,{r['name'] for r in rows})
        plan={r['name']:r for r in j(S/'plan.json')['icons']}
        self.assertTrue(generic<=set(plan))
        self.assertTrue(all(plan[n]['mode']=='native' for n in generic))
        self.assertTrue(all((S/'assets/original-geometry'/f'{n}.svg').is_file() for n in generic))

    def test_all_generic_finishes_and_white_base_are_current(self):
        for n in (S/'generic-names.txt').read_text().split():
            with self.subTest(name=n):
                t=E.parse(S/'svg'/f'{n}.svg')
                base=next(e for e in t.iter() if e.get('id')=='white-base')
                self.assertEqual(base.get('fill'),'#FFFFFF')
                f=next(e for e in t.iter() if e.get('id')=='inkFinish')
                b={e.get('result'):e for e in f if tag(e)=='feGaussianBlur'}
                self.assertEqual(float(b['castBlur'].get('stdDeviation')),13)
                self.assertEqual(float(b['depthBlur'].get('stdDeviation')),2.6)
                self.assertEqual(float(b['lightBlur'].get('stdDeviation')),1.1)
                self.assertEqual([e.get('result') for e in f if tag(e)=='feOffset'],['castOffset'])
                off=next(e for e in f if tag(e)=='feOffset')
                self.assertEqual((float(off.get('dx')),float(off.get('dy'))),(7.,11.))
                self.assertFalse(any(tag(e)=='text' for e in t.iter()))

    def test_svg_no_remote_or_machine_resource_dependencies(self):
        for p in list((S/'svg').glob('*.svg'))+list((S/'assets/native-baseline').glob('*.svg')):
            with self.subTest(path=p.name):
                for e in E.parse(p).iter():
                    for k,v in e.attrib.items():
                        if k.endswith('href'):
                            self.assertTrue(v.startswith(('data:image/','#')),f'{p.name}: {v[:80]}')

    def test_audit_covers_present_files_only(self):
        rows=j(S/'current-audit.json')['items'];paths=[p for r in rows for p in r['paths']]
        expected={p.relative_to(ROOT).as_posix() for p in (ROOT/'Icon/Color').rglob('*.png')}
        self.assertEqual(set(paths),expected)
        self.assertEqual(len(paths),len(set(paths)))
        self.assertTrue(all(r['status'] for r in rows))

    def test_official_download_hashes_are_retained(self):
        base=S/'official/native';rows=j(base/'provenance.json')['items']
        for row in rows:
            with self.subTest(name=row['name']):
                self.assertEqual(sha(base/row['file']),row['sha256'])
                if row.get('original_file'):
                    self.assertEqual(sha(base/row['original_file']),row['original_sha256'])
        for row in j(S/'official/special/provenance.json'):
            if row.get('local_source') and row.get('sha256'):
                with self.subTest(name=row['name']):self.assertEqual(sha(ROOT/row['local_source']),row['sha256'])

    def test_all_production_corners_and_outer_edges_clear(self):
        for p in (ROOT/'Icon/Color/Large').glob('*.png'):
            with self.subTest(name=p.stem),Image.open(p) as im:
                a=im.getchannel('A')
                for b in [(0,0,360,1),(0,359,360,360),(0,0,1,360),(359,0,360,360)]:
                    self.assertLessEqual(a.crop(b).getextrema()[1],1)

    def test_chain_balance_animals_distinct(self):
        for group in [('Load_balancing','Load_balancing_2','Load_balancing_3'),('Fish','Fish_b'),('Chained','Chained_2','Auto_Link')]:
            self.assertEqual(len({sha(ROOT/'Icon/Color'/f'{n}.png') for n in group}),len(group))

    def test_current_provenance_and_licenses_present(self):
        self.assertTrue((S/'current-audit.json').is_file())
        self.assertTrue((S/'official/native/provenance.json').is_file())
        self.assertTrue((S/'official/special/provenance.json').is_file())
        self.assertGreaterEqual(len(list((S/'licenses').glob('*'))),2)

if __name__=='__main__':unittest.main()
