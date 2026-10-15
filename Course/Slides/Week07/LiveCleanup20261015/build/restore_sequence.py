"""Restore complete lesson chains and give both PowerPoint shows one sequence."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from copy import deepcopy
from lxml import etree as E
import json,hashlib,uuid,shutil,ast

R=Path(__file__).resolve().parents[1]
source=R/'output/Week 7 - Direct Copy v8.pptx'
snapshot=R/'build/source-v8.pptx'
if not snapshot.exists():shutil.copy2(source,snapshot)
assert source.read_bytes()==snapshot.read_bytes()
ip=R/'build/pre-sequence-inventory.json'
if not ip.exists():shutil.copy2(R/'qa/final-slide-inventory.json',ip)
inv=json.loads(ip.read_text())
with ZipFile(source) as z:d={n:z.read(n) for n in z.namelist()}
NS={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships','p14':'http://schemas.microsoft.com/office/powerpoint/2010/main'}
restored=[7,8,16,18,21,25,30,49]
hidden={5:'Duplicate host check. UE01 on slide 11 retains the complete example and expected output.',41:'Standalone script-editor case study.',44:'Optional Remote Control example.',45:'Standalone AYON pipeline case study.',58:'Second independent Project Titan tool case.',69:'Additional workflow-scope example; user stories and acceptance criteria remain visible.',70:'Additional mental-model example; the user story remains visible.',85:'Task-feedback summary; state, preview, warning and Undo examples remain visible.',95:'Second naming-consistency example; the style-sheet lesson remains visible.',100:'Optional telemetry comparison; direct observation and useful feedback remain visible.'}
sections=[(1,'Introduction'),(3,'Unreal Setup'),(9,'Python in Unreal'),(11,'UE01: Engine and Project'),(13,'UE02: Actor Selection'),(19,'UE03: Components and Meshes'),(24,'UE04: Content Browser Selection'),(26,'UE05: Texture Properties'),(32,'UE06: Validation'),(35,'UE07: Paths'),(36,'Asset Workflows'),(47,'Blender to Unreal'),(52,'Tool Demos'),(60,'Colleague Demos'),(62,'Break'),(63,'UI/UX and Lab 1'),(66,'Know the Task'),(71,'Guide the Eye'),(80,'Make Actions Clear'),(92,'Keep It Consistent'),(96,'Test the Workflow'),(102,'Peer Review Lab')]
replacements={16:{'Running a Python File':'UE02: Run a Python File','Save the complete UE02 example as Content/Python/selection_demo.py.':'Choose Tools > Execute Python Script.','In Unreal, choose Tools > Execute Python Script and select that file.':'Open UE02_level_selection.py from the project’s lesson_materials folder.'},18:{'UE02: Actor Selection':'UE02: Selection in Unreal'},19:{'UE03: Actor Selection':'UE03: Components and Meshes','UE03 uses this selection to read components and their mesh assets.':'Run UE03_components.py with a mesh Actor selected.'},21:{'UE03: Components and Meshes':'UE03: Output in Unreal'},31:{'UE04–05: Texture Properties':'UE05: Output in Unreal'}}
copy_changes=[]
def text(x):return ''.join(x.xpath('.//a:t/text()',namespaces=NS))
def set_text(p,value):
 ts=p.findall('.//a:t',NS);assert ts
 ts[0].text=value
 for t in ts[1:]:t.text=''
 for br in p.findall('a:br',NS):p.remove(br)
for s in inv:
 n=s['number'];part=s['part'];x=E.fromstring(d[part]);before=text(x)
 if n in hidden:x.set('show','0')
 else:x.attrib.pop('show',None)
 edits=dict(replacements.get(n,{}))
 for p in x.findall('.//a:p',NS):
  old=text(p)
  if old in edits:set_text(p,edits.pop(old))
 assert not edits,(n,edits)
 if n==19:
  # Show the actual complete UE03 checkpoint, not the repeated UE02 selection.
  path=R.parents[3]/'Week07UnrealPython/lesson_materials/week_07_api_checkpoints/ue/UE03_components.py'
  lines=[line for line in path.read_text().splitlines() if line.strip() and not line.startswith(('"""','#'))]
  ast.parse('\n'.join(lines))
  code=next(sp for sp in x.findall('.//p:sp',NS) if 'import unreal' in text(sp))
  body=code.find('p:txBody',NS);template=deepcopy(body.find('a:p',NS))
  for p in list(body.findall('a:p',NS)):body.remove(p)
  for line in lines:
   p=deepcopy(template);set_text(p,line)
   pp=p.find('a:pPr',NS)
   if pp is None:pp=E.Element('{'+NS['a']+'}pPr');p.insert(0,pp)
   for v in list(pp):
    if E.QName(v).localname in ('lnSpc','spcBef','spcAft'):pp.remove(v)
   ls=E.Element('{'+NS['a']+'}lnSpc');E.SubElement(ls,'{'+NS['a']+'}spcPts',val='2200');pp.insert(0,ls)
   for at,tag in enumerate(('spcBef','spcAft'),1):
    v=E.Element('{'+NS['a']+'}'+tag);E.SubElement(v,'{'+NS['a']+'}spcPts',val='0');pp.insert(at,v)
   body.append(p)
  xf=code.find('p:spPr/a:xfrm',NS);xf.find('a:off',NS).set('y','1905000');xf.find('a:ext',NS).set('cy','3683000')
  title=next(sp for sp in x.findall('.//p:sp',NS) if text(sp)=='UE03: Components and Meshes')
  title.find('p:spPr/a:xfrm/a:off',NS).set('y','1206500')
  caption=next(sp for sp in x.findall('.//p:sp',NS) if text(sp).startswith('Run UE03_components'))
  caption.find('p:spPr/a:xfrm/a:off',NS).set('y','5816600')
 if before!=text(x):copy_changes.append({'slide':n,'before':before,'after':text(x)})
 d[part]=E.tostring(x,xml_declaration=True,encoding='UTF-8',standalone=True)
# Keep every slide ID and order. Both show modes include the same visible slides.
pres=E.fromstring(d['ppt/presentation.xml']);ids=pres.findall('p:sldIdLst/p:sldId',NS)
show=pres.find('p:custShowLst/p:custShow',NS);lst=show.find('p:sldLst',NS)
for v in list(lst):lst.remove(v)
visible=[n for n in range(1,107) if n not in hidden]
for n in visible:E.SubElement(lst,'{'+NS['p']+'}sld',{'{'+NS['r']+'}id':ids[n-1].get('{'+NS['r']+'}id')})
# Native PowerPoint sections make the complete blocks navigable in edit view.
exts=pres.find('p:extLst',NS)
for ext in list(exts):
 if ext.find('p14:sectionLst',NS) is not None:exts.remove(ext)
ext=E.SubElement(exts,'{'+NS['p']+'}ext',uri='{521415D9-36F7-43E2-AB2F-B90AF26B5E84}')
sl=E.SubElement(ext,'{'+NS['p14']+'}sectionLst',nsmap={'p14':NS['p14']})
for i,(start,name) in enumerate(sections):
 end=sections[i+1][0]-1 if i+1<len(sections) else 106
 sec=E.SubElement(sl,'{'+NS['p14']+'}section',name=name,id='{'+str(uuid.uuid5(uuid.NAMESPACE_URL,'week07-v9/'+name)).upper()+'}')
 il=E.SubElement(sec,'{'+NS['p14']+'}sldIdLst')
 for n in range(start,end+1):E.SubElement(il,'{'+NS['p14']+'}sldId',id=ids[n-1].get('id'))
d['ppt/presentation.xml']=E.tostring(pres,xml_declaration=True,encoding='UTF-8',standalone=True)
with ZipFile(R/'build/candidate-v9.pptx','w',ZIP_DEFLATED) as z:
 for n,b in d.items():z.writestr(n,b)
report={'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'restored':restored,'hidden':hidden,'visible':visible,'custom_show':visible,'sections':[{'start':n,'name':t} for n,t in sections],'copy_changes':copy_changes,'lesson_blocks':{'UE01':[11,12],'UE02':list(range(13,19)),'UE03':list(range(19,24)),'UE04':[24,25],'UE05':list(range(26,32)),'UE06':[32,33,34],'UE07':[35],'Blender':list(range(47,52))}}
(R/'qa/sequence-changes-v9.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({'restored':restored,'visible':len(visible),'hidden':len(hidden),'native_sections':len(sections),'copy_slides':[c['slide'] for c in copy_changes]}))
