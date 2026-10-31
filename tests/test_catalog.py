import json
from pathlib import Path
import sys
import tempfile
import unittest
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from generate_catalog import RAW_BASE, build_catalog, write_catalog


class CatalogTests(unittest.TestCase):
    def test_missing_icon_directory_does_not_write_empty_catalog(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            with self.assertRaises(FileNotFoundError):
                write_catalog(root)
            self.assertFalse((root / 'HOMOMIX.json').exists())

    def test_repository_catalog_is_valid_and_current(self):
        saved = json.loads((ROOT / 'HOMOMIX.json').read_text(encoding='utf-8'))
        self.assertEqual(saved, build_catalog(ROOT))
        paths = [unquote(item['url'].removeprefix(RAW_BASE)) for item in saved['icons']]
        self.assertEqual(len(paths), len(set(paths)))
        for item, relative in zip(saved['icons'], paths):
            self.assertTrue(item['url'].startswith(RAW_BASE + 'Icon/Color/'))
            self.assertTrue((ROOT / relative).is_file(), relative)
            self.assertEqual(item['name'], Path(relative).name)
        for relative in ['Icon/Color/FDS/Netflix.png', 'Icon/Color/FDS/YouTube.png',
                         'Icon/Color/Claude.png', 'Icon/Color/Large/Claude.png',
                         'Icon/Color/bilibili.png', 'Icon/Color/Large/Bilibili.png']:
            self.assertIn(relative, paths)
        self.assertNotIn('Icon/Color/Claud.png', paths)
        self.assertNotIn('Icon/Color/Large/Claud.png', paths)

    def test_alias_is_excluded_only_if_canonical_exists(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            icons = root / 'Icon/Color'
            icons.mkdir(parents=True)
            (icons / 'Download_2.png').touch()
            self.assertEqual([x['name'] for x in build_catalog(root)['icons']], ['Download_2.png'])
            (icons / 'Download.png').touch()
            self.assertEqual([x['name'] for x in build_catalog(root)['icons']], ['Download.png'])

    def test_sorted_escaped_and_idempotent_output(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            icons = root / 'Icon/Color'
            icons.mkdir(parents=True)
            for name in ['z.png', 'Odd "quote".png', 'A.png']:
                (icons / name).touch()
            write_catalog(root)
            first = (root / 'HOMOMIX.json').read_bytes()
            data = json.loads(first)
            self.assertEqual([x['name'] for x in data['icons']], ['A.png', 'Odd "quote".png', 'z.png'])
            quoted = data['icons'][1]
            self.assertIn('%22quote%22', quoted['url'])
            self.assertTrue((root / unquote(quoted['url'].removeprefix(RAW_BASE))).is_file())
            write_catalog(root)
            self.assertEqual((root / 'HOMOMIX.json').read_bytes(), first)


if __name__ == '__main__':
    unittest.main()
