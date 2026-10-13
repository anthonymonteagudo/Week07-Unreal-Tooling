"""Install the tracked course skill/profile, preserving unknown existing files."""
from pathlib import Path
import hashlib
import json
import os
import re

COURSE = Path(__file__).resolve().parents[2]
VISUALS = COURSE/'Visuals'

def digest(data):
    return hashlib.sha256(data).hexdigest()

def main():
    receipt_path = VISUALS/'install_receipt.json'
    old = json.loads(receipt_path.read_text(encoding='utf-8')) if receipt_path.exists() else {}
    codex = Path(os.environ.get('CODEX_HOME', str(Path.home()/'.codex')))
    targets = {
        codex/'skills/course-visuals/SKILL.md': COURSE/'Skills/course-visuals/SKILL.md',
        Path.home()/'.diagram-design/profiles/tech-art-course.md': VISUALS/'diagram-profile.md'
    }
    for destination, source in targets.items():
        if destination.exists():
            present = digest(destination.read_bytes())
            if present != digest(source.read_bytes()) and present != old.get('installed',{}).get(str(destination)):
                raise RuntimeError(f'Preserved an unknown or externally changed file: {destination}')
    marker=COURSE/'.diagram-design'
    if marker.exists() and marker.read_text(encoding='utf-8').strip()!='profile: tech-art-course':
        raise RuntimeError(f'Preserved a different project profile marker: {marker}')
    installed={}
    # Preserve the pristine package guide as a recovery profile when available.
    pristine=codex/'skills/diagram-design/references/style-guide.md'
    default=Path.home()/'.diagram-design/profiles/default.md'
    if not default.exists() and pristine.exists():
        body=pristine.read_text(encoding='utf-8')
        checks={'paper':'#f5f5f5','paper-2':'#ececec','ink':'#2d3142','muted':'#4f5d75','soft':'#7a8399','rule':'rgba(45,49,66,0.12)','rule-solid':'#bfc0c0','accent':'#eb6c36','accent-tint':'rgba(235,108,54,0.08)','link':'#2e5aa8'}
        valid=not body.lstrip().startswith('<!-- diagram-design-profile')
        for role,value in checks.items():
            line=next((line for line in body.splitlines() if line.startswith('| `'+role+'` |')),'')
            valid=valid and value in line
        valid=valid and '| `title` | Instrument Serif |' in body and '| `node-name` | Geist (sans) |' in body
        if valid:
            default.parent.mkdir(parents=True,exist_ok=True)
            header='<!-- diagram-design-profile\nname: Default\nslug: default\nsource-url: none\ncreated: 2026-09-09\nupdated: 2026-09-09\nnotes: Pristine shipped style guide\n-->\n'
            default.write_text(header+body,encoding='utf-8')
    for destination,source in targets.items():
        destination.parent.mkdir(parents=True,exist_ok=True)
        destination.write_bytes(source.read_bytes())
        installed[str(destination)]=digest(destination.read_bytes())
    marker.write_text('profile: tech-art-course\n',encoding='utf-8')
    receipt={'installed':installed,'project_marker':'Course/.diagram-design','global_diagram_style_modified':False}
    receipt_path.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print('Installed course-visuals skill and project-scoped diagram profile. Global defaults unchanged.')

if __name__=='__main__':
    main()
