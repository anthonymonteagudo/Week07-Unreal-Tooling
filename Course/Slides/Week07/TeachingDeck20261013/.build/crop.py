from PIL import Image
from pathlib import Path
root=Path('../../../../..');dest=Path('../assets')
for src,name,box in [('Course/Slides/Week07/UnrealPythonDemo/Captures/04_undo_transaction.png','undo-detail.png',(102,30,467,165)),('Week07UnrealPython/Docs/UI/captures/stage_3_empty.png','apply-detail.png',(755,760,1088,820))]:
 im=Image.open(root/src);im.crop(box).save(dest/name)
