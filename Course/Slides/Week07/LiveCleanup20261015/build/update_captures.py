from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as E
from PIL import Image
import json,posixpath,hashlib
r=Path('Course/Slides/Week07/LiveCleanup20261015');inv=json.loads((r/'build/inventory.json').read_text());ns={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
with ZipFile(r/'build/text-cleaned.pptx') as z:d={n:z.read(n) for n in z.namelist()}
assets={'image47.png':'native-material-preview.png','image48.png':'material-result.png','image49.png':'native-vfx-preview.png','image50.png':'vfx-result.png','image66.png':'material-baseline.png','image67.png':'material-undo.png','fresh-62-material_preview.png':'practice/material_preview.png','image58.png':'practice/material_preview.png','fresh-65-material_complete.png':'practice/material_complete.png','refinement-20-image2.png':'practice/material_preview.png','fresh-71-vfx_warning.png':'practice/vfx_warning.png','fresh-71-vfx_blocked.png':'practice/vfx_blocked.png'}
assets.update({'image35.png':'editor-textures.png','image44.png':'material-baseline.png','image25.png':'editor-textures.png'})
for media,source in assets.items():
 assert 'ppt/media/'+media in d
 d['ppt/media/'+media]=(r/'captures'/source).read_bytes()
for item in inv:
 part=item['part'];x=E.fromstring(d[part]);relpart=posixpath.join(posixpath.dirname(part),'_rels',posixpath.basename(part)+'.rels')
 rels={q.get('Id'):q.get('Target') for q in E.fromstring(d[relpart])};changed=False
 for pic in x.findall('.//p:pic',ns):
  blip=pic.find('p:blipFill/a:blip',ns)
  if blip is None:continue
  filename=posixpath.basename(rels.get(blip.get('{'+ns['r']+'}embed'),''))
  if filename not in assets:continue
  source=assets[filename];fill=pic.find('p:blipFill',ns)
  for sr in fill.findall('a:srcRect',ns):fill.remove(sr)
  xf=pic.find('p:spPr/a:xfrm',ns);off=xf.find('a:off',ns);ext=xf.find('a:ext',ns);w,h=int(ext.get('cx')),int(ext.get('cy'))
  iw,ih=Image.open(r/'captures'/source).size
  if source=='editor-textures.png':
   left,top,right,bottom=(230,145,1434,643) if filename=='image25.png' else (433,675,1415,1045)
   sr=E.Element('{'+ns['a']+'}srcRect',l=str(round(left/iw*100000)),t=str(round(top/ih*100000)),r=str(round((iw-right)/iw*100000)),b=str(round((ih-bottom)/ih*100000)))
   fill.insert(1,sr);iw,ih=right-left,bottom-top
  if source in ('material-result.png','vfx-result.png','material-baseline.png','material-undo.png'):
   sr=E.Element('{'+ns['a']+'}srcRect',l='25000',t='27778',r='25000',b='22222');fill.insert(1,sr);iw,ih=800,450
  # Contain, center, and retain native picture aspect ratio.
  scale=min(w/iw,h/ih);nw,nh=round(iw*scale),round(ih*scale)
  off.set('x',str(int(off.get('x'))+(w-nw)//2));off.set('y',str(int(off.get('y'))+(h-nh)//2));ext.set('cx',str(nw));ext.set('cy',str(nh))
  pic.find('p:nvPicPr/p:cNvPr',ns).set('descr','Actual '+('PySide sample-data capture' if source.startswith('practice/') else 'Unreal 5.7.4 rehearsal capture')+'; 15 October 2026; cursor-free widget/viewport export. '+source)
  changed=True
 if changed:d[part]=E.tostring(x,xml_declaration=True,encoding='UTF-8',standalone=True)
# Speaker notes retain supporting explanation; replace obsolete UI words globally.
for n,b in list(d.items()):
 if n.startswith('ppt/notesSlides/') and n.endswith('.xml'):
  x=E.fromstring(b)
  for t in x.findall('.//a:t',ns):
   if t.text:t.text=t.text.replace('Apply: create 1 instance','Apply: create instance').replace('Apply reviewed changes','Apply').replace('Preview changes','Preview').replace('Applied change','Result').replace('Proposed / applied result','After Apply, then Result').replace('Tonight’s wording refinements were checked offline.','The revised interface was rehearsed live on 15 October 2026.')
  d[n]=E.tostring(x,xml_declaration=True,encoding='UTF-8',standalone=True)
with ZipFile(r/'build/candidate.pptx','w',ZIP_DEFLATED) as z:
 for n,b in d.items():z.writestr(n,b)
# Replace the two scene captures inside the run sheet, retaining its existing Word layout.
p=r/'output/Week 7 Live Demo Run Sheet v5.docx'
with ZipFile(p) as z:dd={n:z.read(n) for n in z.namelist()}
root=E.fromstring(dd['word/document.xml']);rels={q.get('Id'):q.get('Target') for q in E.fromstring(dd['word/_rels/document.xml.rels'])};blips=root.findall('.//a:blip',ns)
assert len(blips)==2
for blip,source in zip(blips,['material-result.png','vfx-result.png']):
 dd['word/'+rels[blip.get('{'+ns['r']+'}embed')]]=(r/'captures'/source).read_bytes()
with ZipFile(p,'w',ZIP_DEFLATED) as z:
 for n,b in dd.items():z.writestr(n,b)
(r/'qa/capture-manifest.json').write_text(json.dumps([{'media':m,'source':s,'sha256':hashlib.sha256((r/'captures'/s).read_bytes()).hexdigest(),'capture_method':'Qt QWidget.grab' if s.startswith('practice/') else 'Unreal Slate TakeScreenshot' if s.startswith('native-') or s=='editor-textures.png' else 'Unreal AutomationLibrary viewport screenshot','ai_cursor_overlay':False} for m,s in assets.items()],indent=2),encoding='utf-8')
print('Replaced',len(assets),'slide image assets and 2 run-sheet images.')

