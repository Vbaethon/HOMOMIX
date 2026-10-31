"""Single source of compatibility aliases shared by catalog and README.
Alias files stay downloadable; hide them only when same-directory canonical exists.
Claud is a removed typo, not a supported alias.
"""
import json
from pathlib import Path
ALIASES = json.loads(Path(__file__).with_suffix('.json').read_text(encoding='utf-8'))

def is_hidden_alias(path):
    path = Path(path)
    canonical = ALIASES.get(path.name)
    return bool(canonical and path.with_name(canonical).is_file())
