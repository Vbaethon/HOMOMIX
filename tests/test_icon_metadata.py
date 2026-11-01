import json
from pathlib import Path
import re
import sys
import unittest
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from generate_catalog import build_catalog, RAW_BASE
from generate_readme import build_gallery
from icon_metadata import metadata_for

class DisplayMetadataTests(unittest.TestCase):
    def test_stable_catalog_ids_and_dimensions(self):
        rows = build_catalog(ROOT)['icons']
        self.assertEqual(len({r['id'] for r in rows}), len(rows))
        for row in rows:
            self.assertEqual(set(row['size']), {'width', 'height'})
            self.assertGreater(row['size']['width'], 0)
            self.assertIn(row['variant'], {'default', 'large'})
            relative = unquote(row['url'].removeprefix(RAW_BASE))
            self.assertEqual(row['name'], Path(relative).name)
            self.assertTrue((ROOT / relative).is_file())
        self.assertEqual(len({r['id'] for r in rows if r['canonical_name']=='Netflix'}), 2)

    def test_full_labels_unique_clickable_latest_production(self):
        gallery = build_gallery(ROOT)
        labels = re.findall(r'<strong>(.*?)</strong>', gallery)
        self.assertEqual(len(labels), 172)
        self.assertEqual(len(set(labels)), len(labels))
        self.assertNotIn('...', ''.join(labels))
        self.assertNotIn('…', ''.join(labels))
        images = re.findall(r'<a href="([^"]+)"><img src="([^"]+)"', gallery)
        self.assertEqual(len(images), 172)
        for href, src in images:
            self.assertEqual(href, src)
            self.assertTrue(src.startswith('Icon/Color/'))
            self.assertNotIn('Sources/', src)
            self.assertNotIn('/FDS/', src)
            self.assertTrue((ROOT/src).is_file())
        self.assertEqual(gallery, build_gallery(ROOT))

    def test_accurate_names_keep_legacy_paths(self):
        expected = {'F2C':'FC2', 'Cloud':'SoundCloud', 'Adobe':'Adobe Creative Cloud',
                    'Omission':'Microsoft Edge（Omission 策略）'}
        for filename, display in expected.items():
            self.assertEqual(metadata_for(filename)['display_name'], display)
            self.assertTrue((ROOT/'Icon/Color'/f'{filename}.png').exists())
        self.assertEqual(len({metadata_for(n)['display_name'] for n in
                              ['Load_balancing','Load_balancing_2','Load_balancing_3']}), 3)

    def test_long_brand_limit_is_not_hidden(self):
        for name in ['Disney_Channel','Olympics']:
            self.assertTrue(metadata_for(name)['small_size_note'])
            self.assertTrue(metadata_for(name)['official_reference'].startswith('https://'))
        self.assertIn('细标：建议配合标签', build_gallery(ROOT))
