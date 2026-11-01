"""Update the original README gallery or catalog from the current icon files."""
import argparse
from html import escape
import json
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
START, END = '<!--start-icons-->', '<!--end-icons-->'
RAW = 'https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/'
# Existing URLs remain available, but identical compatibility names are not shown twice.
ALIASES = {'Download_2.png':'Download.png',
           'Niche_Link.png':'Chained_2.png', 'Link.png':'Chained_2.png'}
MAX_LABEL_LENGTH = 12


def icon_files():
    return sorted((p for p in (ROOT/'Icon/Color').rglob('*')
                   if p.is_file() and p.suffix.lower() in {'.png','.jpg','.jpeg','.svg'}
                   and 'FDS' not in p.relative_to(ROOT/'Icon/Color').parts
                   and not (p.name in ALIASES and p.with_name(ALIASES[p.name]).exists())),
                  key=lambda p: (p.as_posix().lower(), p.as_posix()))


def catalog_rows():
    # Preserve metadata already attached to the public catalog and update links.
    old = json.loads((ROOT/'HOMOMIX.json').read_text(encoding='utf-8'))
    known = {row['url']: row for row in old['icons']}
    rows = []
    for path in icon_files():
        url = RAW + quote(path.relative_to(ROOT).as_posix(), safe='/')
        row = dict(known.get(url, {}))
        row.update(name=path.name, url=url)
        rows.append(row)
    return rows


def gallery_pairs():
    # Match case-only filename differences while preserving exact link paths.
    pairs = {}
    large_files = [p for p in icon_files() if p.parent == ROOT/'Icon/Color/Large']
    fds_files = sorted((p for p in (ROOT/'Icon/Color/FDS').rglob('*')
                        if p.is_file() and p.suffix.lower() in {'.png','.jpg','.jpeg','.svg'}),
                       key=lambda p: (p.as_posix().lower(), p.as_posix()))
    for version, files in (('Large', large_files), ('FDS', fds_files)):
        for path in files:
            key = path.name.casefold()
            pair = pairs.setdefault(key, {})
            if version in pair:
                raise ValueError(f'Ambiguous {version} gallery filename: {path.name}')
            pair[version] = path
    return [pairs[key] for key in sorted(pairs)]


def gallery_table(pairs):
    cells = ['<table>']
    for i, pair in enumerate(pairs):
        if i % 4 == 0:
            cells.append('<tr>')
        path = pair.get('Large') or pair['FDS']
        full_name = escape(path.name, quote=True)
        label = path.stem
        if len(label) > MAX_LABEL_LENGTH:
            label = label[:MAX_LABEL_LENGTH-3] + '...'
        versions = []
        for version, width, height in (('Large', 64, 64), ('FDS', 100, 72)):
            if version not in pair:
                continue
            target = pair[version]
            relative = escape(target.relative_to(ROOT).as_posix(), quote=True)
            title = escape(f'{target.name} ({version})', quote=True)
            versions.append(f'<td align="center"><a href="{relative}" title="{title}"><img src="{relative}" alt="{title}" width="{width}" height="{height}"></a><br><a href="{relative}" title="{title}">{version}</a></td>')
        cells.append(f'<td align="center"><table><tr>{"".join(versions)}</tr></table><strong title="{full_name}">{escape(label)}</strong></td>')
        if i % 4 == 3 or i == len(pairs)-1:
            cells.append('</tr>')
    cells.append('</table>')
    return '\n'.join(cells)


def update_readme():
    gallery = gallery_table(gallery_pairs())
    path = ROOT/'README.md'
    text = path.read_text(encoding='utf-8')
    if text.count(START) != 1 or text.count(END) != 1:
        raise ValueError('README must contain one original icon gallery marker pair.')
    start = text.index(START) + len(START)
    end = text.index(END, start)
    path.write_text(text[:start] + '\n\n' + gallery + '\n\n' + text[end:], encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--catalog', action='store_true')
    args = parser.parse_args()
    if args.catalog:
        data = {'name':'HOMOMIX', 'icons':catalog_rows(),
                'description':'适用于mihomo - MetacubeX面板的Icon'}
        (ROOT/'HOMOMIX.json').write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    else:
        update_readme()
