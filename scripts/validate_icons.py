#!/usr/bin/env python3
"""Read-only full regression gate. Production assets and sources are never written."""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]

def run(command, cwd=ROOT):
    env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
    subprocess.run(command, cwd=cwd, env=env, check=True)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def validate_generated():
    # Generators see a temporary copy of only their public input; no git writes,
    # no production overwrite even if generated data is stale or fails midway.
    with tempfile.TemporaryDirectory(prefix='homomix-generated-') as temp:
        target = Path(temp)
        shutil.copytree(ROOT/'Icon', target/'Icon')
        for p in ROOT.glob('*.py'):
            shutil.copy2(p, target/p.name)
        for p in ROOT.glob('*.json'):
            shutil.copy2(p, target/p.name)
        shutil.copy2(ROOT/'README.md', target/'README.md')
        for script, output in [('generate_catalog.py', 'HOMOMIX.json'), ('generate_readme.py', 'README.md')]:
            run([sys.executable, script], target)
            if (target/output).read_bytes() != (ROOT/output).read_bytes():
                raise SystemExit(f'{output} is stale; run {script} and commit its result.')
    print('Generated catalog and README are up to date.')

def validate_cold(config, jobs):
    source = ROOT/config['source_dir']
    manifest = json.loads((source/config['manifest']).read_text())
    with tempfile.TemporaryDirectory(prefix='homomix-cold-') as temp:
        target = Path(temp)
        run([sys.executable, str(source/config['builder']), '--output-dir', str(target), '--jobs', str(jobs)])
        expected = {row['path']: row['sha256'] for row in manifest['assets']}
        actual = {p.relative_to(target).as_posix(): sha(p) for p in (target/'Icon').rglob('*.png')}
        if actual != expected:
            changed = sorted(set(actual)^set(expected) | {p for p in actual.keys() & expected.keys() if actual[p] != expected[p]})
            raise SystemExit('Cold rebuild mismatch: ' + ', '.join(changed))
        for path, digest in expected.items():
            if sha(ROOT/path) != digest:
                raise SystemExit('Production PNG differs from render manifest: ' + path)
    print(f'Cold rebuild: all {len(expected)} PNG hashes match source manifest and production.')

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--tests', action='store_true')
    p.add_argument('--generated', action='store_true')
    p.add_argument('--cold', action='store_true')
    p.add_argument('--jobs', type=int, default=2)
    args = p.parse_args()
    config = json.loads((ROOT/'build-config.json').read_text())
    if not any((args.tests, args.generated, args.cold)):
        args.tests = args.generated = args.cold = True
    if args.tests:
        run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v'])
    if args.generated:
        validate_generated()
    if args.cold:
        validate_cold(config, args.jobs)

if __name__ == '__main__':
    main()
