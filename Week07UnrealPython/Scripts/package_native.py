"""Record native module provenance and package only the two runtime files."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
p = argparse.ArgumentParser()
p.add_argument('--build', type=Path, required=True)
p.add_argument('--engine-root', type=Path, required=True)
a = p.parse_args()
files = {n: (a.build / 'Binaries/Win64' / n).read_bytes()
         for n in ['UnrealEditor-Week07Tools.dll', 'UnrealEditor.modules']}
engine_id = json.loads((a.engine_root / 'Engine/Binaries/Win64/UnrealEditor.modules').read_text())['BuildId']
module = json.loads(files['UnrealEditor.modules'])
assert module['BuildId'] == engine_id, 'BuildPlugin generated a module for a different engine.'
meta = {'engine': json.loads((a.engine_root / 'Engine/Build/Build.version').read_text()),
        'engine_build_id': engine_id,
        'sha256': {n: hashlib.sha256(data).hexdigest() for n, data in files.items()},
        'source_sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in (ROOT / 'Plugins/Week07Tools/Source').rglob('*') if p.is_file()}}
out = ROOT / 'Support/Week07Tools_Win64.zip'
out.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    for n, data in files.items(): z.writestr(n, data)
    z.writestr('build.json', json.dumps(meta, indent=2))
print(out, out.stat().st_size, 'bytes')
