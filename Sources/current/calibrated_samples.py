"""Editable calibrated raster layers for the seven approved reference images.

The reference is an immutable calibration input, not an output override. Foreground
and background are separated once and every plan transform acts on foreground
only. At the recorded calibration transform, composing the two layers preserves
all original pixels. Hidden backgrounds are harmonic reconstructions; moving a
flattened raster cannot recover an unavailable official layered original.
"""
from functools import lru_cache
from pathlib import Path
import json
import numpy as np
from PIL import Image
from scipy.ndimage import binary_dilation, binary_fill_holes, map_coordinates
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import cg

R = Path(__file__).resolve().parent
CALIBRATION = json.loads((R / 'sample-calibration.json').read_text())['icons']
NAMES = frozenset(CALIBRATION)


def _restore_background(rgb, region, valid):
    """Keep observed backdrop exact; solve only the foreground occlusion."""
    bg = rgb.copy()
    coords = np.argwhere(region)
    ids = np.full(region.shape, -1, int)
    ids[region] = np.arange(len(coords))
    row, col, values = [], [], []
    rhs = np.zeros((len(coords), 3))
    degree = np.zeros(len(coords))
    for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        yy, xx = coords[:, 0] + dy, coords[:, 1] + dx
        ok = (yy >= 0) & (yy < 360) & (xx >= 0) & (xx < 360)
        ii = np.flatnonzero(ok)
        yy, xx = yy[ok], xx[ok]
        ok = valid[yy, xx]
        ii, yy, xx = ii[ok], yy[ok], xx[ok]
        degree[ii] += 1
        dest = ids[yy, xx]
        unknown = dest >= 0
        row.extend(ii[unknown]); col.extend(dest[unknown])
        values.extend(np.full(unknown.sum(), -1.0))
        rhs[ii[~unknown]] += rgb[yy[~unknown], xx[~unknown]]
    row.extend(range(len(coords))); col.extend(range(len(coords))); values.extend(degree)
    matrix = csr_matrix((values, (row, col)), shape=(len(coords), len(coords)))
    for c in range(3):
        solution, status = cg(matrix, rhs[:, c], rtol=1e-9, maxiter=2400)
        if status != 0:
            raise RuntimeError(f'calibrated backdrop reconstruction failed: {status}')
        bg[..., c][region] = np.clip(solution, 0, 255)
    return bg


@lru_cache(maxsize=7)
def layers(name):
    if name not in NAMES:
        raise ValueError(f'not a calibrated sample: {name}')
    source = np.asarray(Image.open(R / 'approved-sample' / f'{name}.png').convert('RGBA'), float)
    rgb = source[..., :3]
    yy, xx = np.mgrid[:360, :360]
    radius = np.hypot(xx + .5 - 180, yy + .5 - 180)
    valid = (source[..., 3] > 250) & (radius < 174)
    if CALIBRATION[name]['foreground'] == 'white':
        support = (rgb.min(2) > 190) & valid
        # Include original edge antialiasing and soft shadow, not just white ink.
        region = binary_dilation(binary_fill_holes(support), iterations=24 if name == 'Bluesky' else 7) & valid
    else:
        # These three use a neutral, pale vertical backdrop. Fit observed outer
        # samples and reject colored/black foreground, never the circle itself.
        clean = valid & (radius < 160) & (np.ptp(rgb, axis=2) < 3) & (rgb.mean(2) > 210)
        profile = np.full(360, np.nan)
        for y in range(360):
            values = rgb[y].mean(1)[clean[y]]
            if len(values) >= 8:
                profile[y] = np.median(values)
        rows = np.arange(360)
        known = np.isfinite(profile)
        if known.sum() < 220:
            raise ValueError(f'{name}: insufficient observed pale backdrop')
        profile = np.interp(rows, rows[known], profile[known])
        estimate = profile[:, None]
        support = (np.max(abs(rgb - estimate[..., None]), axis=2) > 3) & valid & (radius < 160)
        region = binary_dilation(binary_fill_holes(support), iterations=4) & valid
    if not region.any() or region.sum() > .7 * valid.sum():
        raise ValueError(f'{name}: implausible foreground separation')
    if CALIBRATION[name]['foreground'] == 'pale':
        background = np.where(region[..., None], np.repeat(estimate[..., None], 3, axis=2), rgb)
    else:
        background = _restore_background(rgb, region, valid)
    # Solve the smallest alpha that can represent each observed RGB above the
    # reconstructed backdrop with a valid [0,255] foreground. Unlike an opaque
    # RGB cutout, this never transports a band of old gradient with the mark.
    delta = rgb - background
    positive = np.maximum(delta, 0) / np.maximum(255 - background, 1e-9)
    negative = np.maximum(-delta, 0) / np.maximum(background, 1e-9)
    matte = np.clip(np.maximum(positive, negative).max(axis=2), 0, 1)
    matte *= region
    premult = rgb - background * (1 - matte[..., None])
    premult[matte == 0] = 0
    return source, background, matte, premult



def render(name, scale, dx=0, dy=0):
    if not all(np.isfinite(v) for v in (scale, dx, dy)) or not .2 <= scale <= 1.5:
        raise ValueError('finite transform required, with scale in .2–1.5')
    source, background, matte, premult = layers(name)
    calibration = CALIBRATION[name]
    ratio = scale / calibration['scale']
    yy, xx = np.mgrid[:360, :360]
    coords = np.array([(yy - 179.5 - dy) / ratio + 179.5 + calibration['dy'],
                       (xx - 179.5 - dx) / ratio + 179.5 + calibration['dx']])
    alpha = np.clip(map_coordinates(matte, coords, order=1, mode='constant', cval=0), 0, 1)
    moved = np.stack([map_coordinates(premult[..., c], coords, order=1,
                                     mode='constant', cval=0) for c in range(3)], axis=2)
    rgb = np.rint(background * (1 - alpha[..., None]) + moved).clip(0, 255).astype('uint8')
    rgb[source[..., 3] == 0] = source[..., :3][source[..., 3] == 0].astype('uint8')
    return Image.fromarray(np.dstack([rgb, source[..., 3].astype('uint8')]))
