from pathlib import Path
from lxml import etree as E
from zipfile import ZipFile
import json
r=Path('Course/Slides/Week07/LiveCleanup20261015'); inv=json.loads((r/'build/inventory.json').read_text())
with ZipFile(r/'build/source-v6.pptx') as z:
 for num in [55,56,72,74,75,76,77,78,79,81,82,83,84,89,90,93,94,97,99,103,105]:
  x=E.fromstring(z.read(inv[num-1]['part']));ns={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
  print('\nSLIDE',num)
  print(json.dumps([''.join(p.itertext()) for p in x.findall('.//a:t',ns)],ensure_ascii=False))
