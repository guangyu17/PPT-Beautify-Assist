#!/usr/bin/env python3
"""Create source-adjacent, resumable asset workspace without moving originals."""
import argparse
import hashlib
import json
from pathlib import Path
from _common import utf8_stdio

DIRECTORIES = ('extracted', 'backgrounds/generated', 'backgrounds/derived', 'foregrounds/original',
               'foregrounds/cutouts', 'foregrounds/derived', 'ornaments/generated', 'ornaments/derived',
               'fonts/downloaded', 'fonts/licenses', 'fonts/previews', 'downloads/images', 'downloads/references',
               'prompts', 'layouts', 'previews', 'output', 'logs')


def initialize(source=None, parent=None, name=None):
    source = Path(source).resolve() if source else None
    if source and not source.is_file():
        raise FileNotFoundError(source)
    if not source and (not parent or not name):
        raise ValueError('Outline-only projects require --parent and --name')
    base = Path(parent).resolve() if parent else source.parent
    stem = name or source.stem
    if stem in ('.', '..') or any(c in stem for c in '\\/:*?"<>|') or not stem.strip() or stem != stem.rstrip('. '):
        raise ValueError('Project name must be a safe folder name')
    root = (base / (stem + '_beautify')).resolve()
    if not root.is_relative_to(base):
        raise ValueError('Workspace escapes chosen parent')
    record = root / 'logs/workspace.json'
    identity = str(source) if source else None
    if record.exists():
        previous = json.loads(record.read_text(encoding='utf-8'))
        if previous['source'] != identity:
            raise ValueError('Existing workspace belongs to a different source; choose --name')
    elif root.exists() and any(root.iterdir()):
        raise ValueError('Existing unregistered workspace: preserve it; choose a distinct --name or review migration first')
    for relative in DIRECTORIES:
        target = (root / relative).resolve()
        if not target.is_relative_to(root):
            raise ValueError('Unsafe existing directory link')
        target.mkdir(parents=True, exist_ok=True)
    if not record.exists():
        result = {'schema_version': 1, 'source': identity, 'source_sha256_at_creation':
                  hashlib.sha256(source.read_bytes()).hexdigest() if source else None,
                  'workspace': str(root), 'directories': list(DIRECTORIES)}
        record.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    return json.loads(record.read_text(encoding='utf-8'))


def main():
    utf8_stdio()
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('source', nargs='?', type=Path)
    p.add_argument('--parent', type=Path)
    p.add_argument('--name')
    a = p.parse_args()
    print(json.dumps(initialize(a.source, a.parent, a.name), ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
