"""Run this saved file from Blender's Text Editor (Alt+P). No auto-install needed."""
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[2]
python_root = str(root / 'Content' / 'Python')
if python_root not in sys.path:
    sys.path.insert(0, python_root)
from week07_bridge import blender_ui
blender_ui.register()
print('Week 7 publisher: 3D View > N sidebar > Week 7')
