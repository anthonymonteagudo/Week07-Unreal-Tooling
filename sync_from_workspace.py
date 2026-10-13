"""Explicit, non-destructive snapshot update from the Perforce authoring workspace.

Usage: python sync_from_workspace.py C:/path/to/anthony.monteagudo
Review git diff, then commit/push. This script never deletes or publishes files.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import shutil

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('workspace', type=Path)
args = parser.parse_args()
source = args.workspace.resolve()
target = Path(__file__).resolve().parent
if source == target or not (source/'Week07UnrealPython/Week07UnrealPython.uproject').is_file():
    raise SystemExit('Expected the authoring workspace containing Week07UnrealPython.')
roots = ['Week07UnrealPython', 'Course/Slides/Week07', 'Course/Readers', 'Course/Tools',
         'Course/Visuals', 'Course/Skills', 'Course/Wiki', 'Course/References']
excluded_dirs = {'.git', '.venv', '.deps', 'node_modules', 'Saved', 'Intermediate',
                 'DerivedDataCache', 'Binaries', '__pycache__'}
records, omitted = [], []
for root in roots:
    for path in (source/root).rglob('*'):
        if not path.is_file():
            continue
        rel = path.relative_to(source)
        if any(part in excluded_dirs for part in rel.parts):
            continue
        if path.name.startswith('~$') or path.suffix in {'.pyc', '.log', '.blend1', '.tmp'} or path.name == 'unreal.local.json':
            continue
        if '.build' in rel.parts:
            authored = path.suffix in {'.mjs', '.js', '.py', '.html', '.css'}
            small_data = path.suffix == '.json' and path.name != 'deck.json' and path.stat().st_size < 1_000_000
            if not (authored or small_data):
                omitted.append(rel.as_posix())
                continue
        dest = target/rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        if path.suffix == '.ini':
            data = path.read_bytes()
            data = re.sub(rb'(?m)^SecurityToken=[^\r\n]*', b'SecurityToken=', data)
            if not dest.exists() or dest.read_bytes() != data:
                dest.write_bytes(data)
        elif not dest.exists() or path.stat().st_size != dest.stat().st_size or path.stat().st_mtime_ns != dest.stat().st_mtime_ns:
            shutil.copy2(path, dest)
        records.append(dict(path=rel.as_posix(), bytes=dest.stat().st_size))
for rel in ['Course/AGENTS.md', 'Course/Slides/REVIEW_FORMAT_PREFERENCES.md']:
    dest = target/rel
    dest.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(source/rel,dest)
(target/'snapshot-inventory.json').write_text(json.dumps(dict(
    scope=roots, files=records, omitted_intermediate_slide_outputs=omitted,
    excluded_directory_names=sorted(excluded_dirs),
    secret_handling='Android File Server SecurityToken blanked in copied INI files',
    source_remains='Perforce workspace; this script does not modify it'),indent=2)+'\n',encoding='utf8')
print(f'Snapshotted {len(records)} project and teaching files. Review git diff before committing.')
