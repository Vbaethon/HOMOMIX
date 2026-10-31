"""Final inverse collection: semantic-family gradients, cohesive native silhouettes, three-layer finish."""
from pathlib import Path
import json,re,hashlib,importlib.util
from material import filters
ROOT=Path(__file__).resolve().parent
SERIES={r['name']:r['series'] for r in json.loads((ROOT/'SERIES-49.json').read_text())['items']}
PALETTES={
'system_graphite':['#292C31','#151719','#050607'],
'network_blue_cyan':['#00B89C','#00A9CD','#137EDD','#493ACF'],
'transfer_orange_red':['#FFAC17','#FF7B13','#F34428','#DE245B'],
'entertainment_purple_pink':['#F56470','#DE31A9','#A62ACD','#6331D2'],
'animal_green_yellow':['#FFB41B','#E2D91A','#6CD12A','#00B576','#009EAE'],
'intelligence_rose_violet':['#F77A25','#ED3A83','#B52BC5','#6433D4'],
'location_emerald_teal':['#46CB52','#00B68D','#00A4C4','#2768D2']}

def parts(n):
 raw=(ROOT/'references/original-white-geometry'/f'{n}.svg').read_text();defs=re.search(r'<defs>(.*?)</defs>',raw,re.S)[1];defs=re.sub(r'<(?:radial|linear)Gradient.*?</(?:radial|linear)Gradient>','',defs,flags=re.S);defs=re.sub(r'<filter.*?</filter>','',defs,flags=re.S)
 body=re.search(r'<g id="white-foreground"[^>]*>(.*)</g></g></svg>',raw,re.S)[1]
 for module in sorted((ROOT/'adjustments').glob('*.py')):
  spec=importlib.util.spec_from_file_location(module.stem,module);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);defs,body=m.adjust(n,defs,body)
 # Accepted sample line-weight improvements extend only to their direct variants.
 if n in ['Link','Chained_2','Niche_Link']:body=body.replace('stroke-width="29"','stroke-width="34"').replace('r="16"','r="18"')
 if n in ['Load_balancing','Load_balancing_2','Load_balancing_3']:body=body.replace('stroke-width="28"','stroke-width="33"')
 if n in ['Download','Download_2']:body=body.replace('stroke-width="29"','stroke-width="34"')
 return defs,body

def gradient(n):
 family=SERIES[n];colors=PALETTES[family]
 if family=='system_graphite':return '<linearGradient id="ink" gradientUnits="userSpaceOnUse" x1="80" y1="60" x2="270" y2="300">'+''.join(f'<stop offset="{i/(len(colors)-1):.3f}" stop-color="{c}"/>' for i,c in enumerate(colors))+'</linearGradient>'
 cx,cy={'network_blue_cyan':(90,180),'transfer_orange_red':(260,270),'entertainment_purple_pink':(260,100),'animal_green_yellow':(180,300),'intelligence_rose_violet':(85,100),'location_emerald_teal':(100,265)}[family]
 if n=='Link':cx,cy=265,100
 if n=='Load_balancing_2':cx,cy=85,245
 if n=='Network':cx,cy=85,85
 # Same series shares colors; family coherence outranks random palette diversity.
 stops=[0,.28,.53,.76,1] if len(colors)==5 else [0,.34,.68,1]
 radius={'Consistent_Hashing':210,'DIRECT':180,'Location':210,'Load_balancing_2':210}.get(n,255)
 return f'<radialGradient id="ink" gradientUnits="userSpaceOnUse" cx="{cx}" cy="{cy}" r="{radius}">'+''.join(f'<stop offset="{o}" stop-color="{c}"/>' for o,c in zip(stops,colors))+'</radialGradient>'

def svg(n,inner=True):
 defs,body=parts(n);defs+='<mask id="subjectMask" maskUnits="userSpaceOnUse" x="0" y="0" width="360" height="360">'+body+'</mask>'
 return f'<svg xmlns="http://www.w3.org/2000/svg" width="360" height="360" viewBox="0 0 360 360"><defs>{defs}{gradient(n)}{filters(SERIES[n]=="system_graphite",inner)}</defs><g clip-path="url(#disk)"><circle id="white-base" cx="180" cy="180" r="175" fill="#FFFFFF" filter="url(#diskShadow)"/><g id="gradient-subject" filter="url(#inkFinish)"><rect width="360" height="360" fill="url(#ink)" mask="url(#subjectMask)"/></g></g></svg>\n'

def main():
 rows=[]
 for n in (ROOT/'names.txt').read_text().split():
  if n in SERIES:raw=svg(n);category='inverse_generic';family=SERIES[n]
  else:raw=(ROOT/'references/approved-brand-exceptions'/f'{n}.svg').read_text();category='preserved_approved_theme_exception';family='approved_original_theme'
  (ROOT/'svg'/f'{n}.svg').write_text(raw);rows.append({'name':n,'category':category,'series':family,'native_source':f'Sources/v3/svg/{n}.svg','source_sha256':hashlib.sha256(raw.encode()).hexdigest(),'third_party_new_paths':False})
 (ROOT/'SOURCE-LEDGER.json').write_text(json.dumps({'revision':'final-inverse-series','counts':{'inverse_generic':49,'preserved_theme_exception':4},'items':rows},indent=2)+'\n')
 (ROOT/'SERIES-PALETTES.json').write_text(json.dumps(PALETTES,indent=2)+'\n')
 print('Authored49 inverse +4 preserved themes')
if __name__=='__main__':main()
