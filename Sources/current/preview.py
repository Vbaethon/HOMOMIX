"""Render current production only. No historical snapshots or external downloads."""
from pathlib import Path
import argparse, hashlib, json, math, textwrap
from PIL import Image, ImageDraw, ImageFont
R = Path(__file__).resolve().parent
ROOT = R.parents[1]

def font(size):
    try:
        return ImageFont.truetype('DejaVuSans.ttf', size)
    except OSError:
        return ImageFont.load_default(size=size)

def paste(canvas, path, x, y, size):
    with Image.open(path) as source:
        im = source.convert('RGBA').resize((size, size), Image.Resampling.LANCZOS)
    canvas.paste(im, (x, y), im)

def render_current(render, out):
    out.mkdir(parents=True, exist_ok=True)
    aliases = json.loads((ROOT/'icon_aliases.json').read_text())
    paths = sorted((p for p in (render/'Icon/Color').glob('*.png') if p.name not in aliases), key=lambda p: (p.stem.casefold(), p.name))
    names = [p.stem for p in paths]
    w, cell, columns = 1560, 130, 12
    im = Image.new('RGB', (w, 100 + math.ceil(len(paths)/columns)*cell), '#E9EDF2')
    draw = ImageDraw.Draw(im)
    draw.text((20, 14), 'HOMOMIX | Current icon collection', font=font(27), fill='#142739')
    draw.text((20, 55), f'{len(paths)} canonical icons | actual PNGs | aliases excluded', font=font(17), fill='#526376')
    for i, p in enumerate(paths):
        x, y = i%columns*cell, 100+i//columns*cell
        large = render/'Icon/Color/Large'/('Bilibili.png' if p.name == 'bilibili.png' else p.name)
        paste(im, large, x+20, y, 90)
        label = '\n'.join(textwrap.wrap(p.stem, 22, break_long_words=True, break_on_hyphens=False))
        draw.multiline_text((x+4, y+94), label, font=font(9), fill='#142739', spacing=1)
    im.save(out/'full-overview.png')
    # Every entry is shown at actual 60px canvas / 36px disc size; no old-version comparison.
    for page in range(math.ceil(len(paths)/48)):
        part = paths[page*48:(page+1)*48]
        sheet = Image.new('RGB', (1200, 70+math.ceil(len(part)/8)*95), '#E9EDF2')
        d = ImageDraw.Draw(sheet)
        d.text((18, 15), f'Current actual-size icons {page+1} | 36px disc', font=font(24), fill='#142739')
        for i, p in enumerate(part):
            x, y = (i%8)*150, 70+(i//8)*95
            paste(sheet, p, x+45, y, 60)
            label = '\n'.join(textwrap.wrap(p.stem, 25, break_long_words=True, break_on_hyphens=False))
            d.multiline_text((x+3, y+61), label, font=font(9), fill='#142739', spacing=1)
        sheet.save(out/f'actual-size-{page+1}.png')
    manifest = {'count': len(paths), 'names': names, 'input_files': [{'path': p.relative_to(render).as_posix(), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths]}
    (out/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    return manifest

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--render',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    args=p.parse_args();render_current(args.render,args.out)
if __name__=='__main__':main()
