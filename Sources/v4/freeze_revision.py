"""Freeze reviewed official-mark renders and complete collection integrity.

Run only after optical review. Never run implicitly from an export or test.
"""
from pathlib import Path
import argparse, hashlib, json, shutil
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,data):p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def main():
    p=argparse.ArgumentParser();p.add_argument('--reviewed-render-dir',type=Path,required=True);p.add_argument('--baseline-dir',type=Path,required=True);a=p.parse_args()
    report=json.loads((a.reviewed_render_dir/'reproduction-report.json').read_text())
    for row in report['assets']:
        assert sha(a.reviewed_render_dir/row['path'])==row['new_sha256']
        assert sha(REPO/row['native_source'])==row['native_source_sha256']
        (REPO/row['path']).parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(a.reviewed_render_dir/row['path'],REPO/row['path'])
    write(ROOT/'render-manifest.json',report)
    baseline={p.relative_to(a.baseline_dir).as_posix():sha(p) for p in (a.baseline_dir/'Icon/Color').rglob('*.png')}
    actual={p.relative_to(REPO).as_posix():sha(p) for p in (REPO/'Icon/Color').rglob('*.png')}
    assert not (set(baseline)-set(actual)), 'Never delete a published URL'
    changes=[{'path':path,'before_sha256':baseline.get(path),'sha256':digest,'kind':'added' if path not in baseline else 'updated'} for path,digest in actual.items() if baseline.get(path)!=digest]
    write(ROOT/'collection-manifest.json',{'baseline_commit':'8830f6cd9ee4676d5c161e022cbefa8cd279a581','status':'reviewed candidate, not published','baseline_files':baseline,'files':actual,'changes':sorted(changes,key=lambda r:r['path'])})
    print(json.dumps({'png':len(actual),'changed_or_added_png':len(changes),'added_png':sum(r['kind']=='added' for r in changes)}))
if __name__=='__main__':main()
