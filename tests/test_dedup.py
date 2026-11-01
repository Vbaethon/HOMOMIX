"""Compatibility aliases are downloadable, but not independently displayed."""
from pathlib import Path
import json
import sys
import unittest
import tempfile
import subprocess
from urllib.parse import unquote
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from icon_aliases import ALIASES, is_hidden_alias
from generate_catalog import build_catalog, RAW_BASE

class DedupTests(unittest.TestCase):
    def test_single_alias_table_and_no_claud(self):
        self.assertEqual(ALIASES, {'Zoho_old.png':'Zoho_new.png','Download_2.png':'Download.png',
                                  'Niche_Link.png':'Chained_2.png','Twitter.png':'X.png','Link.png':'Chained_2.png'})
        self.assertNotIn('Claud.png', ALIASES)
        for folder in ['Icon/Color', 'Icon/Color/Large']:
            self.assertFalse((ROOT/folder/'Claud.png').exists())
            self.assertTrue((ROOT/folder/'Claude.png').is_file())

    def test_all_legacy_alias_files_stay_downloadable(self):
        for folder in ['Icon/Color', 'Icon/Color/Large']:
            for alias, canonical in ALIASES.items():
                self.assertTrue((ROOT/folder/alias).is_file(), alias)
                self.assertTrue((ROOT/folder/canonical).is_file(), canonical)
                self.assertTrue(is_hidden_alias(ROOT/folder/alias))

    def test_catalog_hides_only_aliases_not_variants(self):
        paths={unquote(x['url'].removeprefix(RAW_BASE)) for x in build_catalog(ROOT)['icons']}
        for folder in ['Icon/Color', 'Icon/Color/Large']:
            for alias, canonical in ALIASES.items():
                self.assertNotIn(f'{folder}/{alias}',paths)
                self.assertIn(f'{folder}/{canonical}',paths)
        for name in ['Hugging_face','Hugging_face_g','Bilibili_blue','Bilibili_Global','Huawei','Huawei_black']:
            self.assertIn(f'Icon/Color/{name}.png',paths)

    def test_readme_hides_alias_images_explains_variants(self):
        s=(ROOT/'README.md').read_text(encoding='utf-8')
        for alias in ALIASES:
            self.assertNotIn(f'src="Icon/Color/{alias}"',s)
        self.assertNotIn('src="Icon/Color/Claud.png"',s)
        self.assertIn('src="Icon/Color/Claude.png" alt="Claude"',s)
        self.assertIn('配色变体说明',s)
        self.assertIn('不计作独立样式',s)

    def test_alias_is_directory_local_and_safe_when_canonical_missing(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t);(p/'Large').mkdir();(p/'Download_2.png').touch()
            (p/'Large/Download.png').touch()
            self.assertFalse(is_hidden_alias(p/'Download_2.png'))
            (p/'Download.png').touch()
            self.assertTrue(is_hidden_alias(p/'Download_2.png'))

if __name__=='__main__':unittest.main()
