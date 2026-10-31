"""Production v6 integrity and structural safety, not a visual-quality proof.

Historical v8 pixel hashes are checked separately against input-v8. These tests
cannot certify equal perceived size, artistic quality, or every raster matte.
"""
import hashlib
import json
from pathlib import Path
import sys
import unittest
import xml.etree.ElementTree as E
import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
S=ROOT/'Sources/v6'
sys.path.insert(0,str(ROOT))
from generate_catalog import build_catalog
from icon_aliases import ALIASES
COMPACT={'AI_Tree','AI_voice','Auto_Link','Chained','Chained_2','Consistent_Hashing','DIRECT','Download','Download_2','Failover','GFW','Load_balancing','Load_balancing_2','Load_balancing_3','Magic_Timer','Network','Other','Round_Robin','SNS','Server','Stream','Tick_2','Transfer'}
EXPECTED_ALIASES={'Zoho_old.png':'Zoho_new.png','Download_2.png':'Download.png','Niche_Link.png':'Chained_2.png','Twitter.png':'X.png','Link.png':'Chained_2.png'}
def read(path): return json.loads(path.read_text())
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def localtag(e):return e.tag.rsplit('}',1)[-1]
def brand_geometry(tree):
    # SVG container/subject transforms may change. The actual source shape and
    # embedded bitmap payload must not. Background geometry is included too.
    keys={'path':('d','fill','fill-rule','stroke','stroke-width'),
          'polygon':('points','fill','stroke'),
          'polyline':('points','fill','stroke'),
          'image':('href','{http://www.w3.org/1999/xlink}href')}
    return [(localtag(e),[(k,e.get(k)) for k in keys[localtag(e)]]) for e in tree.iter() if localtag(e) in keys]

class UnifiedRevision(unittest.TestCase):
    def test_current_collection_manifest_and_counts(self):
        m=read(S/'collection-manifest.json')
        actual={p.relative_to(ROOT).as_posix():sha(p) for p in (ROOT/'Icon/Color').rglob('*.png')}
        self.assertEqual(actual,m['files']);self.assertEqual(len(actual),356)
        self.assertEqual(set(m['baseline_files'])-set(actual),{'Icon/Color/Claud.png','Icon/Color/Large/Claud.png'})
        self.assertEqual(len(list((ROOT/'Icon/Color').glob('*.png'))),177)
        self.assertEqual(len(list((ROOT/'Icon/Color/Large').glob('*.png'))),177)
        self.assertEqual({p.name for p in (ROOT/'Icon/Color/FDS').glob('*.png')},{'Netflix.png','YouTube.png'})
        self.assertFalse(any(p.stem=='Claud' for p in (ROOT/'Icon/Color').rglob('*.png')))

    def test_production_render_hashes_and_exact_dimensions(self):
        rows=read(S/'render-manifest.json')['assets']
        self.assertEqual(len(rows),354);self.assertEqual(len({r['path'] for r in rows}),354)
        self.assertEqual(len({r['name'] for r in rows}),177)
        actual={p.relative_to(ROOT).as_posix() for d in [ROOT/'Icon/Color',ROOT/'Icon/Color/Large'] for p in d.glob('*.png')}
        self.assertEqual({r['path'] for r in rows},actual)
        for r in rows:
            with self.subTest(name=r['name'],path=r['path']):
                self.assertEqual(sha(ROOT/r['path']),r['sha256'])
                with Image.open(ROOT/r['path']) as im:
                    self.assertEqual(im.mode,'RGBA')
                    self.assertEqual(im.size,(360,360) if '/Large/' in r['path'] else (300,300))

    def test_aliases_exact_pixels_and_172_unique_display_items(self):
        self.assertEqual(ALIASES,EXPECTED_ALIASES)
        for folder in ['Icon/Color','Icon/Color/Large']:
            for alias,canonical in ALIASES.items():
                with Image.open(ROOT/folder/alias) as a,Image.open(ROOT/folder/canonical) as b:
                    self.assertEqual(a.convert('RGBA').tobytes(),b.convert('RGBA').tobytes(),alias)
        rows=[r for r in build_catalog(ROOT)['icons'] if '/Large/' not in r['url'] and '/FDS/' not in r['url']]
        self.assertEqual(len(rows),172)
        self.assertFalse({r['name'] for r in rows}&set(ALIASES))
        hashes=[]
        for r in rows:
            with Image.open(ROOT/'Icon/Color'/r['name']) as im:hashes.append(hashlib.sha256(im.convert('RGBA').tobytes()).hexdigest())
        self.assertEqual(len(hashes),len(set(hashes)))

    def test_native_brand_geometry_is_preserved(self):
        lock=read(ROOT/'tests/fixtures/v6-native-brand-geometry.json')
        self.assertEqual(len(lock['items']),14)
        for r in lock['items']:
            with self.subTest(name=r['name']):
                self.assertEqual(sha(ROOT/r['source']),r['source_sha256'])
                self.assertEqual(brand_geometry(E.parse(ROOT/r['source'])),brand_geometry(E.parse(ROOT/r['output'])))

    def test_compact23_set_shadow_parameters_and_circle(self):
        m=read(S/'render-manifest.json')
        self.assertEqual(set(m['compact_originals']),COMPACT)
        self.assertEqual(len(m['compact_originals']),23)
        for name in sorted(COMPACT):
            with self.subTest(name=name):
                tree=E.parse(S/'svg'/f'{name}.svg')
                finish=next(e for e in tree.iter() if e.get('id')=='inkFinish')
                blur={e.get('result'):float(e.get('stdDeviation')) for e in finish if localtag(e)=='feGaussianBlur'}
                self.assertEqual(blur,{'castBlur':13.,'depthBlur':2.6,'lightBlur':1.1})
                offsets=[e for e in finish if localtag(e)=='feOffset']
                self.assertEqual(len(offsets),1)
                self.assertEqual((offsets[0].get('in'),float(offsets[0].get('dx')),float(offsets[0].get('dy'))),('castBlur',7.,11.))
                floods=[float(e.get('flood-opacity')) for e in finish if localtag(e)=='feFlood']
                self.assertEqual(floods,[.115,.12,.03])
                for result,inp in [('depthEdge','depthBlur'),('lightEdge','lightBlur')]:
                    edge=next(e for e in finish if e.get('result')==result)
                    self.assertEqual((edge.get('in'),edge.get('in2'),edge.get('operator')),('SourceAlpha',inp,'out'))
                self.assertFalse(any(localtag(e)=='text' for e in tree.iter()))
                mask=next(e for e in tree.iter() if e.get('id')=='subjectMask')
                self.assertGreater(len(list(mask)),0)
                with Image.open(ROOT/'Icon/Color/Large'/f'{name}.png') as im:a=np.asarray(im.convert('RGBA'))
                yy,xx=np.mgrid[:360,:360];distance=np.hypot(xx+.5-180,yy+.5-180)
                self.assertEqual(int(a[distance>176,3].max()),0,'disc spills beyond fixed boundary')
                self.assertEqual(int(a[180,180,3]),255)
                # Strong chroma/darkness only: faint soft shadows are not a hard
                # subject silhouette. This is a clipping guard, not optical QA.
                significant=(a[:,:,:3].min(2)<210)&(a[:,:,3]>250)
                ys,xs=np.where(significant)
                self.assertGreater(len(xs),100)
                self.assertGreaterEqual(min(xs.min(),ys.min()),18)
                self.assertLessEqual(max(xs.max(),ys.max()),341)


class AdaptiveBackgroundPolicy(unittest.TestCase):
    def test_bitcoin_color_fills_disc_not_white_ring(self):
        im=Image.open(ROOT/'Icon/Color/Large/Bitcoin.png').convert('RGBA')
        for xy in [(180,15),(15,180),(345,180),(180,345)]:
            r,g,b,a=im.getpixel(xy);self.assertEqual(a,255);self.assertGreater(r,220);self.assertTrue(100<g<180);self.assertLess(b,60)
    def test_crypto_official_blue_fills_disc(self):
        im=Image.open(ROOT/'Icon/Color/Large/Crypto.png').convert('RGBA')
        for xy in [(180,15),(15,180),(345,180),(180,345)]:
            r,g,b,a=im.getpixel(xy);self.assertEqual(a,255);self.assertGreater(b,r+25);self.assertLess(g,150)
    def test_background_source_provenance_bytes(self):
        rows=json.loads((S/'official-special/provenance.json').read_text())
        for n in ['Bitcoin','Crypto','GOG']:
            row=next(x for x in rows if x['name']==n)
            self.assertEqual(hashlib.sha256((ROOT/row['local_source']).read_bytes()).hexdigest(),row['sha256'])

if __name__=='__main__':unittest.main()
