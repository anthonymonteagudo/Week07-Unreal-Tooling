"""One-time readability migration for the October 13 teaching revision."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
lessons = root / 'lesson_materials/week_07_api_checkpoints'
for file in lessons.rglob('*.py'):
    text = file.read_text(encoding='utf-8')
    text = text.replace('[a for a in assets if isinstance(a, unreal.Texture2D)]',
                        '[asset for asset in assets if isinstance(asset, unreal.Texture2D)]')
    if file.stem.startswith(('UE03', 'UE08', 'UE10')):
        text = re.sub(r'\bparts\b', 'components', text)
        text = re.sub(r'\bpart\b', 'component', text)
    if file.stem.startswith('UE08'):
        text = re.sub(r'^""".*?"""', '"""UE08: assign an existing material to the prepared target, then inspect Undo."""', text, count=1, flags=re.S)
        text = text.replace('component, material = components[0], assets[0]',
                            'component = components[0]\nmaterial = assets[0]')
        text = text.replace('        component.modify()', '        component.modify()  # Record the component for Undo.')
    if file.stem.startswith('UE06'):
        text = text.replace('_N', '_Normal').replace('checked, mismatches = 0, 0', 'checked = 0\nmismatches = 0')
        # The suffix change must not alter the Unreal enum name.
        text = text.replace('TC_NormalORMALMAP', 'TC_NORMALMAP')
    if file.stem.startswith('UE12'):
        text = re.sub(r'^""".*?"""', '"""UE12: import one new, unsaved mesh and verify its identity."""', text, count=1, flags=re.S)
    if file.stem.startswith('BL04'):
        text = re.sub(r'^""".*?"""', '"""BL04: export one selected mesh to a new temporary folder."""', text, count=1, flags=re.S)
    text = text.replace('"""\n# %% setup', '"""\n\n# %% setup')
    file.write_text(text.rstrip()+'\n', encoding='utf-8')

catalog = root/'Scripts/build_api_lesson_catalog.py'
text = catalog.read_text(encoding='utf-8').replace('The illustrative normal-map suffix is _N.', 'The prepared material tool uses the suffix _Normal.').replace('mismatching _N texture', 'mismatching _Normal texture')
catalog.write_text(text, encoding='utf-8')
tests = root/'Tests/test_api_checkpoints.py'
text = tests.read_text(encoding='utf-8')
for name in ('A_N', 'B_N', 'C_N'):
    text = text.replace('"'+name+'"', '"'+name+'ormal"')
tests.write_text(text, encoding='utf-8')
