#!/usr/bin/env python3
"""Freeze an explicitly reviewed reconstruction and optionally install its PNGs.

This authoring command changes manifests. build_all.py never changes them.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[1]


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path,data):path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')


def inventory():
    files=[p for p in ROOT.rglob('*') if p.is_file() and p.name!='source-files.json' and not {'node_modules','__pycache__'}.intersection(p.parts)]
    write(ROOT/'source-files.json',{'files':[{'path':p.relative_to(REPO).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(files)]})


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--reviewed-render-dir',type=Path)
    p.add_argument('--install',action='store_true')
    p.add_argument('--inventory-only',action='store_true')
    a=p.parse_args()
    if a.inventory_only:inventory();return
    if not a.reviewed_render_dir:p.error('--reviewed-render-dir is required')
    report=json.loads((a.reviewed_render_dir/'reproduction-report.json').read_text())
    names=(ROOT/'names.txt').read_text().split();assets=report['assets']
    expected={'Icon/Color/'+sub+n+'.png' for n in names for sub in ['', 'Large/']}
    assert len(names)==53 and len(set(names))==53
    assert {r['path'] for r in assets}==expected and len(assets)==106
    forbidden={'Google','Apple_rainbow','GOG','Twitch','Apple','Plex','Linkedin_ray','Claud','Claude'}
    assert not set(names)&forbidden
    baseline=json.loads((ROOT/'baseline-files.json').read_text());base={r['path']:r for r in baseline['files']}
    for r in assets:
        assert sha(a.reviewed_render_dir/r['path'])==r['new_sha256']
        assert sha(REPO/r['native_source'])==r['native_source_sha256']
        assert r['path'] in base and base[r['path']]['sha256']!=r['new_sha256']
        r['baseline_sha256']=base[r['path']]['sha256']
        if a.install:shutil.copy2(a.reviewed_render_dir/r['path'],REPO/r['path'])
    counts={'canonical_reviewed':174,'updated_names':53,'retained_names':121,'changed_png':106}
    spec={'status':'new reconstruction of the reviewed direction; not byte-identical to the lost package','baseline_commit':baseline['commit'],'counts':counts,'expected_dependencies':report['environment'],'assets':assets}
    write(ROOT/'render-manifest.json',spec);write(ROOT/'collection-manifest.json',spec)
    defaults=sorted([r['path'] for r in baseline['files'] if Path(r['path']).parent.as_posix()=='Icon/Color' and Path(r['path']).stem!='Claud'])
    assert len(defaults)==174
    large={Path(r['path']).name.casefold():r['path'] for r in baseline['files'] if Path(r['path']).parent.as_posix()=='Icon/Color/Large'}
    now={r['path']:r['new_sha256'] for r in assets};items=[]
    for default in defaults:
        name=Path(default).stem;paths=[default,large[Path(default).name.casefold()]];changed=[q for q in paths if q in now]
        assert len(changed) in [0,2]
        items.append({'name':name,'paths':paths,'final_disposition':'updated' if changed else 'retained','changed_paths':changed,'baseline_sha256':{q:base[q]['sha256'] for q in paths},'final_sha256':{q:now.get(q,base[q]['sha256']) for q in paths},'reason':'reconstructed from recovered source and reviewed direction; source ledger records each input' if changed else 'baseline bytes retained; outside the53 selected white/theme names'})
    write(ROOT/'all174-disposition.json',{'counts':counts,'items':items,'additional_protected_files':'Every baseline PNG outside the exact106 paths, including all FDS and both Claud aliases, is retained byte-for-byte.'})
    inventory()
    print(json.dumps({'status':'frozen','installed':a.install,'counts':counts}))


if __name__=='__main__':main()
