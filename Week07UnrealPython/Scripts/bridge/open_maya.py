"""Run this saved file in Maya's Python Script Editor using runpy.run_path."""
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[2]
python_root = str(root / 'Content' / 'Python')
if python_root not in sys.path:
    sys.path.insert(0, python_root)
from week07_bridge import maya_ui
maya_ui.show()
