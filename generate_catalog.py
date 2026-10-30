"""Build a deterministic, valid JSON catalog using only the Python standard library."""
import json
from pathlib import Path
from urllib.parse import quote

RAW_BASE = 'https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/'
ALIASES = {'Claud.png': 'Claude.png'}


def build_catalog(repo_root=Path('.')):
    root = Path(repo_root)
    icon_root = root / 'Icon/Color'
    if not icon_root.is_dir():
        raise FileNotFoundError(f'Icon directory not found: {icon_root}')
    files = sorted(icon_root.rglob('*'), key=lambda path: (path.as_posix().lower(), path.as_posix()))
    icons = []
    for path in files:
        if not path.is_file():
            continue
        canonical = ALIASES.get(path.name)
        if canonical and path.with_name(canonical).is_file():
            continue
        relative = path.relative_to(root).as_posix()
        icons.append({'name': path.name, 'url': RAW_BASE + quote(relative, safe='/')})
    return {'name': 'HOMOMIX', 'icons': icons, 'description': '适用于mihomo - MetacubeX面板的Icon'}


def write_catalog(repo_root=Path('.')):
    data = build_catalog(repo_root)
    target = Path(repo_root) / 'HOMOMIX.json'
    target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return data


if __name__ == '__main__':
    catalog = write_catalog()
    print(f'HOMOMIX.json: {len(catalog["icons"])} icons')
