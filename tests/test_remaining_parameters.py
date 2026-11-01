"""Every remaining rendering family must move only its subject, or reject edits."""
import copy,json,os,subprocess,sys,tempfile,unittest
import xml.etree.ElementTree as E
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/json.loads((ROOT/'build-config.json').read_text())['source_dir']
NAMES=['AI','Grok','Fish','Other','GOG','Disney_Mickey','Piggies','China']
class RemainingParameters(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.temp=tempfile.TemporaryDirectory();cls.base=Path(cls.temp.name)
  cls.plan=json.loads((SOURCE/'plan.json').read_text())
  cls.outputs={}
  for variant in ('default','dx','dy','compact'):
   plan=copy.deepcopy(cls.plan)
   for row in plan['icons']:
    if variant in ('dx','dy') and row['name'] in NAMES and row['name']!='China':row[variant]+=12
    if variant=='compact' and row['name']=='Other':row['compact_scale']=.75
   dest=cls.base/variant;dest.mkdir();path=dest/'plan.json';path.write_text(json.dumps(plan))
   run=subprocess.run([sys.executable,str(SOURCE/'build_unified.py'),'--output-dir',str(dest),'--plan',str(path),'--jobs','2','--names',*NAMES],capture_output=True,text=True,env={**os.environ,'OPENBLAS_NUM_THREADS':'1'})
   if run.returncode:raise AssertionError(run.stderr)
   cls.outputs[variant]=dest
 @classmethod
 def tearDownClass(cls):cls.temp.cleanup()
 def test_defaults_are_byte_identical(self):
  for name in NAMES:
   for prefix in ('Icon/Color','Icon/Color/Large'):
    rel=Path(prefix)/(name+'.png')
    with self.subTest(name=name,prefix=prefix):self.assertEqual((self.outputs['default']/rel).read_bytes(),(ROOT/rel).read_bytes())
 def test_independent_x_y_and_stationary_background(self):
  for name in NAMES[:-1]:
   before=np.array(Image.open(self.outputs['default']/f'Icon/Color/Large/{name}.png'))
   for variant in ('dx','dy'):
    with self.subTest(name=name,parameter=variant):
     after=np.array(Image.open(self.outputs[variant]/f'Icon/Color/Large/{name}.png'))
     self.assertGreater(np.count_nonzero(np.any(before!=after,axis=2)),100)
     # Moving the foreground also moves its shadow; the composited
     # rim is not a pure-background sample. Circle coverage stays fixed.
     # SVG antialias/compositing may vary a few edge alpha units
     # when a soft subject shadow reaches the clipped disc boundary.
     if name in ('AI','Grok','Fish','Other'):
      delta=np.abs(before[...,3].astype(int)-after[...,3].astype(int))
      self.assertLessEqual(int(delta.max()),2)
      self.assertLessEqual(int(np.count_nonzero(delta)),20)
     else:np.testing.assert_array_equal(before[...,3],after[...,3])
     np.testing.assert_array_equal(before[before[...,3]==0],after[before[...,3]==0])
 def test_native_background_nodes_are_not_transformed(self):
  for name in ('AI','Grok','Fish','Other'):
   trees=[]
   for variant in ('default','dx','dy'):
    tree=E.parse(self.outputs[variant]/f'Sources/current/svg/{name}.svg').getroot()
    mask=next((e for e in tree.iter() if e.attrib.get('id')=='subjectMask'),None)
    if mask is not None:
     for child in list(mask):mask.remove(child)
    else:
     foreground=next(e for e in tree.iter() if e.attrib.get('id') in {'optical-foreground','optical-subject'})
     foreground.attrib.pop('transform',None)
    trees.append(E.tostring(tree))
   self.assertEqual(trees[0],trees[1],name)
   self.assertEqual(trees[0],trees[2],name)
 def test_effective_scale_and_policy_reported(self):
  rows={x['name']:x for x in json.loads((self.outputs['default']/'render-report.json').read_text())['assets']}
  self.assertEqual(rows['Other']['scale'],.95)
  self.assertEqual(rows['Other']['scale_parameter'],'compact_scale')
  self.assertEqual(rows['China']['transform_policy'],'fixed_composition')
 def test_compact_scale_is_effective(self):
  rel='Icon/Color/Large/Other.png'
  self.assertNotEqual((self.outputs['default']/rel).read_bytes(),(self.outputs['compact']/rel).read_bytes())
  rows=json.loads((self.outputs['compact']/'render-report.json').read_text())['assets']
  self.assertTrue(all(r['scale']==.75 for r in rows if r['name']=='Other'))
 def test_unsupported_transforms_rejected(self):
  for name,key,value in [('China','dx',1),('China','dy',1),('China','scale',.9),('Other','scale',.8)]:
   with self.subTest(name=name,key=key):
    plan=copy.deepcopy(self.plan)
    for row in plan['icons']:
     if row['name']==name:row[key]=value
    path=self.base/'reject.json';path.write_text(json.dumps(plan))
    run=subprocess.run([sys.executable,str(SOURCE/'build_unified.py'),'--output-dir',str(self.base/'reject'),'--plan',str(path),'--names',name],capture_output=True,text=True)
    self.assertNotEqual(run.returncode,0)
    self.assertIn('compact_scale' if name=='Other' else 'full_composition_preserved',run.stderr)
if __name__=='__main__':unittest.main()
