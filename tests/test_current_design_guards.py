"""Live design invariants replacing archived QA/snapshot assertions."""
import hashlib
import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as E
ROOT=Path(__file__).resolve().parents[1]
S=ROOT/'Sources/current'
def tag(e):return e.tag.rsplit('}',1)[-1]

class CurrentDesignGuards(unittest.TestCase):
    def test_live_generic_palette_and_centered_inner_layer(self):
        rows=json.loads((S/'SERIES-49.json').read_text())['items']
        for row in rows:
            with self.subTest(name=row['name']):
                tree=E.parse(S/'svg'/f"{row['name']}.svg")
                ink=next(e for e in tree.iter() if e.get('id')=='ink')
                colors={e.get('stop-color') for e in ink if tag(e)=='stop'}
                self.assertGreaterEqual(len(colors),3)
                filt=next(e for e in tree.iter() if e.get('id')=='inkFinish')
                depth=next(e for e in filt if e.get('result')=='depthBlur')
                self.assertEqual(depth.get('in'),'SourceAlpha')
                edges={e.get('result'):e for e in filt if e.get('result') in {'depthEdge','lightEdge'}}
                for edge in edges.values():
                    self.assertEqual(edge.get('in'),'SourceAlpha');self.assertEqual(edge.get('operator'),'out')
                disk=next(e for e in tree.iter() if e.get('id')=='diskShadow')
                shadow=next(e for e in disk if tag(e)=='feDropShadow')
                self.assertEqual(float(shadow.get('stdDeviation')),2.5)
                self.assertEqual(float(shadow.get('flood-opacity')),.035)

    def test_live_official_native_paths_and_no_generic_finish(self):
        lock=json.loads((ROOT/'tests/fixtures/current-native-brand-geometry.json').read_text())['items']
        for row in lock:
            with self.subTest(name=row['name']):
                tree=E.parse(ROOT/row['output'])
                self.assertFalse(any(e.get('id')=='inkFinish' for e in tree.iter()))
        a=E.parse(S/'official/native/DeepSeek.svg')
        b=E.parse(S/'svg/DeepSeek.svg')
        self.assertEqual([e.get('d') for e in a.iter() if tag(e)=='path'],[e.get('d') for e in b.iter() if tag(e)=='path'])
        nested=next(e for e in b.iter() if tag(e)=='svg' and 'x' in e.attrib)
        self.assertEqual((nested.get('x'),nested.get('y')),('80','90'))

    def test_preview_manifest_tracks_current_actual_exports(self):
        m=json.loads((S/'qa/final/manifest.json').read_text())
        from generate_catalog import build_catalog
        names={Path(r['name']).stem for r in build_catalog(ROOT)['icons'] if r['variant']=='default'}
        self.assertEqual(set(m['names']),names);self.assertEqual(m['count'],172)
        for row in m['input_files']:
            self.assertEqual(hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest(),row['sha256'])
        self.assertFalse(any((S/'qa/final').glob('cross-before-after*')))
