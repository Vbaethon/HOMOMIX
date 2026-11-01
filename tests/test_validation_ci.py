from pathlib import Path
import json
import unittest
ROOT=Path(__file__).resolve().parents[1]
class ValidationContract(unittest.TestCase):
    def test_build_config_and_pinned_dependencies(self):
        c=json.loads((ROOT/'build-config.json').read_text())
        for path in [ROOT/c['source_dir']/c['builder'],ROOT/c['source_dir']/c['manifest'],ROOT/c['source_dir']/'requirements.txt',ROOT/c['renderer_dir']/'package-lock.json']:
            self.assertTrue(path.is_file(),str(path))
        dependencies=[line.strip() for line in (ROOT/c['source_dir']/'requirements.txt').read_text().splitlines() if line.strip() and not line.startswith('#')]
        self.assertTrue(all('==' in line for line in dependencies))
    def test_workflows_validate_all_changes_without_push(self):
        build=(ROOT/'.github/workflows/build.yml').read_text()
        gallery=(ROOT/'.github/workflows/iconpreview.yml').read_text()
        self.assertIn('scripts/validate_icons.py --tests --cold',build)
        self.assertIn('scripts/validate_icons.py --generated',gallery)
        for text in (build,gallery):
            self.assertIn('pull_request:',text)
            self.assertIn('contents: read',text)
            self.assertNotIn('paths:',text)
            self.assertNotIn('git push',text)
            self.assertNotIn('|| true',text)
            self.assertIn('persist-credentials: false',text)
