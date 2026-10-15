from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as E
import json
r=Path('Course/Slides/Week07/LiveCleanup20261015'); src=r.parent/'Refinement20261015/output'
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
changes={
'Tonight’s wording refinements were checked offline.':'The simplified UI was rebuilt and rehearsed live on 15 October 2026.',
'Choose VFX Placement, classroom fountain, scale 1.0.':'Choose VFX Placement, scale 1.0. The native tab uses the prepared classroom fountain.',
'Two plain cubes, three empty pedestals, no placed effects.':'Two plain cubes, three empty pedestals and no effects on a dark stage.',
'Preview. Read the destination, parent, three texture mappings and one target.':'Preview. Read After Apply: destination, parent, three texture mappings and one target. Hover names for full paths.',
'Apply once. Show the near blue cube and far plain cube.':'Click Apply: create instance. The table becomes Result. Show the blue target and plain protected cube.',
'Use Edit > Undo only when its label identifies the material assignment.':'Check Edit > Undo: Week 7: assign prepared material instance. Camera piloting adds a separate Undo entry.',
'Preview: three anchors, three effects, their positions and rotations. Apply once.':'Preview: three anchors, three effects, positions and rotations. Click Apply: place 3 effects.',
'New instance cleanup is separate: inspect references before deleting only your rehearsal asset.':'New instance cleanup is separate. Use a fresh name or discard only the unsaved rehearsal asset when closing.',
'Preset review: one lightweight GPU sprite emitter, 90 particles/second, lifetime 1.4–1.75 seconds, sprite size 6–12 cm, default Niagara sprite material. Three new effects maximum; scale 0.25–1; anchors at least 100 cm apart. Effect Type: 5000 cm distance, maximum 4 instances per system and 8 overall. This classroom review does not certify packaged-game performance.':'The prepared fountain uses a reviewed Niagara preset. Maximum three new effects; scale 0.25–1; markers at least 100 cm apart. Count and spacing checks do not establish runtime performance.',
}
report=[]
for name in ['Week 7 Lab 1 Student Handout v4.docx','Week 7 Peer Review Packet v3.docx','Week 7 Lab Instructor Guide v4.docx','Week 7 Live Demo Run Sheet v4.docx']:
 with ZipFile(src/name) as z:d={n:z.read(n) for n in z.namelist()}
 changed=0
 for part,b in list(d.items()):
  if part.startswith('word/') and part.endswith('.xml'):
   x=E.fromstring(b)
   for t in x.findall('.//w:t',ns):
    if t.text:
     old=t.text;new=old.replace(' — ',': ').replace('—','; ')
     if 'Run Sheet' in name:
      for a,b in changes.items():new=new.replace(a,b)
     if new!=old:changed+=1;t.text=new
   d[part]=E.tostring(x,xml_declaration=True,encoding='UTF-8',standalone=True)
 newname=name.replace(' v4',' v5').replace('Packet v3','Packet v4')
 with ZipFile(r/'output'/newname,'w',ZIP_DEFLATED) as z:
  for n,b in d.items():z.writestr(n,b)
 report.append({'file':newname,'changed_text_runs':changed})
(r/'qa/document-changes.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(report)
