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
ALIASES = {'Zoho_old.png':'Zoho_new.png', 'Download_2.png':'Download.png',
           'Niche_Link.png':'Chained_2.png', 'Twitter.png':'X.png', 'Link.png':'Chained_2.png'}


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


def update_readme():
    names = {row['url']: row.get('display_name') for row in catalog_rows()}
    cells = ['<table>']
    files = [p for p in icon_files() if p.parent == ROOT/'Icon/Color']
    for i, path in enumerate(files):
        if i % 5 == 0:
            cells.append('<tr>')
        relative = path.relative_to(ROOT).as_posix()
        label = names.get(RAW + quote(relative, safe='/')) or path.stem
        cells.append(f'<td align="center"><a href="{escape(relative, quote=True)}"><img src="{escape(relative, quote=True)}" alt="{escape(label, quote=True)}" width="60" height="60"></a><br><strong>{escape(label)}</strong></td>')
        if i % 5 == 4 or i == len(files)-1:
            cells.append('</tr>')
    cells.append('</table>')
    path = ROOT/'README.md'
    text = path.read_text(encoding='utf-8')
    if text.count(START) != 1 or text.count(END) != 1:
        raise ValueError('README must contain one original icon gallery marker pair.')
    start = text.index(START) + len(START)
    end = text.index(END, start)
    path.write_text(text[:start] + '\n\n' + '\n'.join(cells) + '\n\n' + text[end:], encoding='utf-8')


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
