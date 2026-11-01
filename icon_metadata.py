"""Display metadata supplements stable download filenames; never renames URLs."""
import json
import struct
from pathlib import Path

METADATA = json.loads(Path(__file__).with_suffix('.json').read_text(encoding='utf-8'))

def canonical_key(stem):
    return 'bilibili' if stem.lower() == 'bilibili' else stem

def metadata_for(stem):
    key = canonical_key(stem)
    return {'display_name': key.replace('_', ' '), **METADATA.get(key, {})}

def image_dimensions(path):
    """Read PNG IHDR without a third-party image dependency. Unknown = None."""
    with Path(path).open('rb') as stream:
        header = stream.read(24)
    if len(header) == 24 and header[:8] == b'\x89PNG\r\n\x1a\n' and header[12:16] == b'IHDR':
        width, height = struct.unpack('>II', header[16:24])
        return {'width': width, 'height': height}
    return None

def catalog_metadata(path, icon_root):
    path = Path(path)
    relative = path.relative_to(icon_root)
    variant = 'default' if len(relative.parts) == 1 else '/'.join(relative.parts[:-1]).lower()
    canonical = canonical_key(path.stem)
    return {
        'id': f'color/{variant}/{canonical}',
        'canonical_name': canonical,
        'variant': variant,
        'size': image_dimensions(path),
        **metadata_for(canonical),
    }
