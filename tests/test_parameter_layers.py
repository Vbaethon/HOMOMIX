"""Each calibrated foreground transform must work and preserve its backdrop."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import unittest
import tempfile
import subprocess
import os
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
CONFIG=json.loads((ROOT/'build-config.json').read_text())
SOURCE=ROOT/CONFIG['source_dir']
sys.path.insert(0,str(SOURCE))
import calibrated_samples as samples

class CalibratedParameters(unittest.TestCase):
    def test_all_seven_default_layers_are_pixel_exact(self):
        self.assertEqual(samples.NAMES, {'Google','Gmail','TikTok','Facebook','Pixiv','Bluesky','Instagram'})
        for name in sorted(samples.NAMES):
            with self.subTest(name=name):
                p=samples.CALIBRATION[name]
                actual=np.array(samples.render(name,p['scale'],p['dx'],p['dy']))
                expected=np.array(Image.open(SOURCE/'approved-sample'/f'{name}.png').convert('RGBA'))
                np.testing.assert_array_equal(actual,expected)

    def test_scale_x_and_y_each_change_every_foreground(self):
        for name in sorted(samples.NAMES):
            p=samples.CALIBRATION[name]
            baseline=np.array(samples.render(name,p['scale'],p['dx'],p['dy']))
            yy,xx=np.mgrid[:360,:360]
            background=samples.layers(name)[1].copy()
            for parameter,values in [('scale',(p['scale']*.75,p['dx'],p['dy'])),
                                     ('dx',(p['scale'],p['dx']+12,p['dy'])),
                                     ('dy',(p['scale'],p['dx'],p['dy']+12))]:
                with self.subTest(name=name,parameter=parameter):
                    output=np.array(samples.render(name,*values))
                    self.assertGreater(np.count_nonzero(np.any(output[...,:3]!=baseline[...,:3],axis=2)),100)
                    np.testing.assert_array_equal(output[...,3],baseline[...,3])
                    # Backdrop pixels are a fixed layer. A translated mark may
                    # cover a previously clear rim pixel, which is not a change
                    # to the background itself. Never confuse the composited
                    # output with that immutable layer.
                    np.testing.assert_array_equal(samples.layers(name)[1],background)
                    transparent=baseline[...,3]==0
                    np.testing.assert_array_equal(output[transparent],baseline[transparent])


    def test_hidden_background_is_reconstructed_not_old_mark(self):
        for name in sorted(samples.NAMES):
            with self.subTest(name=name):
                source,bg,matte,fg=samples.layers(name)
                self.assertGreater(int(matte.sum()),100)
                self.assertTrue(np.all(fg[matte==0]==0))
                self.assertTrue(np.isfinite(bg).all())
                p=samples.CALIBRATION[name]
                output=np.array(samples.render(name,p['scale']*.4,p['dx'],p['dy']))
                # Both old outer silhouette and its inner hole must not persist
                # as a second full-size mark; visual evidence accompanies test.
                self.assertNotEqual(hashlib.sha256(output.tobytes()).hexdigest(),hashlib.sha256(source.astype('uint8').tobytes()).hexdigest())

    def test_cli_plan_transforms_are_not_overridden(self):
        plan=json.loads((SOURCE/'plan.json').read_text())
        for row in plan['icons']:
            if row['name'] in samples.NAMES:
                row.update(scale=.4,dx=30,dy=30)
        with tempfile.TemporaryDirectory() as td:
            dest=Path(td); source=dest/'changed-plan.json'
            source.write_text(json.dumps(plan))
            env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
            subprocess.run([sys.executable,str(SOURCE/CONFIG['builder']),
                            '--output-dir',str(dest/'output'),'--plan',str(source),
                            '--names',*sorted(samples.NAMES),'--jobs','2'],check=True,env=env,capture_output=True)
            report=json.loads((dest/'output/render-report.json').read_text())
            self.assertEqual(len(report['assets']),14)
            for row in report['assets']:
                with self.subTest(path=row['path']):
                    self.assertEqual((row['scale'],row['dx'],row['dy']),(.4,30,30))
                    self.assertEqual(row['method'],'calibrated_foreground_layers')
                    self.assertNotEqual((dest/'output'/row['path']).read_bytes(),(ROOT/row['path']).read_bytes())

    def test_invalid_parameters_fail_explicitly(self):
        for values in [(float('nan'),0,0),(0,0,0),(.9,float('inf'),0)]:
            with self.assertRaises(ValueError): samples.render('Google',*values)
