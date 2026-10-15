from zipfile import ZipFile
from lxml import etree as E
from pathlib import Path
import json,posixpath
r=Path('Course/Slides/Week07/LiveCleanup20261015'); inv=json.loads((r/'build/inventory.json').read_text()); ns={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
with ZipFile(r/'build/text-cleaned.pptx') as z:
 for num in [55,56,72,74,78,84,89,90]:
  part=inv[num-1]['part'];x=E.fromstring(z.read(part));relpart=posixpath.join(posixpath.dirname(part),'_rels',posixpath.basename(part)+'.rels'); rels={q.get('Id'):q.get('Target') for q in E.fromstring(z.read(relpart))}
  print(num,[{'name':p.find('p:nvPicPr/p:cNvPr',ns).get('name'),'asset':rels.get(p.find('p:blipFill/a:blip',ns).get('{'+ns['r']+'}embed')),'size':dict(p.find('p:spPr/a:xfrm/a:ext',ns).attrib)} for p in x.findall('.//p:pic',ns)])
