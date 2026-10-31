"""Historical v3/v4 reconstruction locks against frozen pre-optical snapshots.
Current production and approved URL deletions are tested in test_optical_revision.
"""
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import struct
import unittest
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
SOURCES=ROOT/'Sources/v3'
HISTORICAL=ROOT/'Sources/v5/input-original'


def read(name):return json.loads((SOURCES/name).read_text())
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


class ReconstructionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec=read('render-manifest.json');cls.assets=cls.spec['assets']

    def test_exact_pairs_dimensions_and_checksums(self):
        groups=defaultdict(list)
        self.assertEqual(len(self.assets),106)
        self.assertEqual(len({r['path'] for r in self.assets}),106)
        self.assertEqual(read('collection-manifest.json')['assets'],self.assets)
        for row in self.assets:
            groups[row['name']].append(row)
            path=HISTORICAL/row['path'];self.assertEqual(sha(path),row['new_sha256'])
            raw=path.read_bytes();self.assertEqual(raw[:8],b'\x89PNG\r\n\x1a\n')
            self.assertEqual(list(struct.unpack('>II',raw[16:24])),row['dimensions'])
            self.assertEqual(tuple(raw[24:26]),(8,6))
        self.assertEqual(len(groups),53)
        for name,rows in groups.items():
            self.assertEqual({tuple(r['dimensions']) for r in rows},{(300,300),(360,360)},name)
            self.assertEqual(len({r['native_source_sha256'] for r in rows}),1,name)

    def test_complete_self_contained_native_sources(self):
        source_paths={r['native_source'] for r in self.assets}
        self.assertEqual(source_paths,{p.relative_to(ROOT).as_posix() for p in (SOURCES/'svg').glob('*.svg')})
        for row in self.assets:
            source=ROOT/row['native_source'];self.assertEqual(sha(source),row['native_source_sha256'])
            tree=ET.fromstring(source.read_bytes());ids=[]
            for node in tree.iter():
                self.assertFalse(node.tag.endswith('text'),row['name']+': production font dependency')
                if 'id' in node.attrib:ids.append(node.attrib['id'])
                for key,value in node.attrib.items():
                    if key.endswith('href'):self.assertTrue(value.startswith(('data:image/','#')),row['name'])
            self.assertEqual(len(ids),len(set(ids)),row['name']+': duplicate SVG identifier')

    def test_protected_and_all_retained_png_bytes(self):
        baseline=read('baseline-files.json')['files'];changed={r['path'] for r in self.assets}
        current=json.loads((ROOT/'Sources/v4/collection-manifest.json').read_text())
        changed|={r['path'] for r in current['changes']}
        actual={p.relative_to(HISTORICAL).as_posix() for p in (HISTORICAL/'Icon/Color').rglob('*.png')}
        self.assertEqual(actual,set(current['files']),'Unexpected image URL')
        self.assertTrue({r['path'] for r in baseline}<=actual,'An original image URL was lost')
        for row in baseline:
            if row['path'] not in changed:self.assertEqual(sha(HISTORICAL/row['path']),row['sha256'],row['path'])
        forbidden={'Google','Apple_rainbow','GOG','Twitch','Apple','Plex','Linkedin_ray','Claud','Claude'}
        self.assertFalse({r['name'] for r in self.assets}&forbidden)
        self.assertFalse(any('/FDS/' in r['path'] for r in self.assets))

    def test_disposition_covers_all_174_and_matches_updates(self):
        rows=read('all174-disposition.json')['items']
        self.assertEqual(len(rows),174)
        self.assertEqual(len({r['name'] for r in rows}),174)
        self.assertEqual(sum(r['final_disposition']=='updated' for r in rows),53)
        self.assertEqual({p for r in rows for p in r['changed_paths']},{r['path'] for r in self.assets})
        for row in rows:
            self.assertEqual(len(row['paths']),2)
            for path in row['paths']:
                current=json.loads((ROOT/'Sources/v4/collection-manifest.json').read_text())
                expected=current['files'].get(path,row['final_sha256'][path])
                self.assertEqual(sha(HISTORICAL/path),expected)

    def test_source_inventory(self):
        indexed=read('source-files.json')['files'];paths=[r['path'] for r in indexed]
        self.assertEqual(len(paths),len(set(paths)))
        actual={p.relative_to(ROOT).as_posix() for p in SOURCES.rglob('*') if p.is_file() and p.name!='source-files.json' and not {'node_modules','__pycache__'}.intersection(p.parts)}
        self.assertEqual(set(paths),actual)
        for row in indexed:
            p=ROOT/row['path'];self.assertEqual(p.stat().st_size,row['bytes']);self.assertEqual(sha(p),row['sha256'],row['path'])


if __name__=='__main__':unittest.main()
