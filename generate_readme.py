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
GROUPS_PER_ROW = 4


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


def display_name(name):
    # Keep every character, but bound unbroken text so long names cannot widen a group.
    lines = []
    while len(name) > 18:
        split = name.rfind('_', 0, 18) + 1
        if split < 9:
            split = 18
        lines.append(escape(name[:split]))
        name = name[split:]
    lines.append(escape(name))
    return '<br>'.join(lines)


def pair_preview_sizes(pair):
    # Measure the complete visible icon, including its white disk or backing.
    # Ignore faint cast-shadow pixels, never crop or alter the source image.
    from PIL import Image, ImageChops
    metrics = {}
    for version, path in pair.items():
        with Image.open(path) as image:
            alpha = image.convert('RGBA').getchannel('A')
            bbox = alpha.point(lambda value: 255 if value >= 128 else 0).getbbox()
            if bbox is None:
                raise ValueError(f'Empty gallery icon: {path.name}')
            if version == 'Large' and path.stem not in {'Apple_Music', 'Amazon', 'Apple'}:
                # On GitHub's light page a plain white disk is not a visible edge.
                # Measure the recognizable colored/dark artwork, but retain the
                # entire source canvas (including the disk) in the linked image.
                rgb = image.convert('RGB')
                red, green, blue = rgb.split()
                low = ImageChops.darker(ImageChops.darker(red, green), blue)
                high = ImageChops.lighter(ImageChops.lighter(red, green), blue)
                chroma = ImageChops.subtract(high, low)
                ink = ImageChops.lighter(low.point(lambda v: 255 if v < 190 else 0),
                                        chroma.point(lambda v: 255 if v > 25 else 0))
                ink = ImageChops.multiply(ink, alpha.point(lambda v: 255 if v >= 128 else 0))
                bbox = ink.getbbox() or bbox
            x0, y0, x1, y1 = bbox
            metrics[version] = (image.width, image.height, x1-x0, y1-y0)
    # Match optical footprint rather than forcing a wide wordmark and a disk
    # to have the same height. Independent aspect caps keep both recognizable.
    sizes = {}
    for version, (w, h, bw, bh) in metrics.items():
        scale = min(56.0 / (bw * bh) ** 0.5, 76.0 / bw, 64.0 / bh,
                    144.0 / w, 108.0 / h)
        sizes[version] = max(1, round(w * scale))
    return sizes



def gallery_table(pairs):
    # One flat table: each filename spans its two fixed side-by-side versions.
    # Table cells, rather than CSS or inline images, prevent version wrapping.
    rows = ['<table>']
    for start in range(0, len(pairs), GROUPS_PER_ROW):
        group = pairs[start:start + GROUPS_PER_ROW]
        rows.append('<tr>')
        for pair in group:
            path = pair.get('Large') or pair['FDS']
            rows.append(f'<td colspan="2" width="320" align="center"><strong title="{escape(path.name, quote=True)}">{display_name(path.stem)}</strong></td>')
        rows.append('</tr>')
        rows.append('<tr>')
        for pair in group:
            sizes = pair_preview_sizes(pair)
            for version in ('Large', 'FDS'):
                if version not in pair:
                    rows.append('<td width="160"></td>')
                    continue
                target = pair[version]
                relative = escape(target.relative_to(ROOT).as_posix(), quote=True)
                title = escape(f'{target.name} ({version})', quote=True)
                rows.append(f'<td width="160" align="center" valign="middle"><a href="{relative}" title="{title}"><img src="{relative}" alt="{title}" width="{sizes[version]}"></a></td>')
        rows.append('</tr>')
    rows.append('</table>')
    return '\n'.join(rows)


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
