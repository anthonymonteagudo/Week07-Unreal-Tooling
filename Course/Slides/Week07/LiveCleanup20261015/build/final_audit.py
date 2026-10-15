from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
import hashlib,json,ast
root=Path(__file__).resolve().parents[1]
workspace=root.parents[3]
ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main','w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
deck=root/'output/Week 7 - Rehearsed and Refined v7.pptx'
with ZipFile(root/'build/source-v6.pptx') as source,ZipFile(deck) as current:
 current_xml=[E.fromstring(current.read(n)) for n in current.namelist() if n.endswith('.xml') and n.startswith(('ppt/slides/','ppt/notesSlides/','ppt/slideMasters/','ppt/slideLayouts/'))]
 texts=[t for x in current_xml for t in x.xpath('.//a:t/text()',namespaces=ns)]
 assert not any('\u2014' in t or '\ufffd' in t for t in texts)
 footers=[]
 for x in current_xml:
  for sp in x.findall('.//p:sp',ns):
   if sp.find('.//p:ph[@type="ftr"]',ns) is None:continue
   value=''.join(sp.xpath('.//a:t/text()',namespaces=ns)).strip()
   if not value or value.upper() in ('FOOTER','SAMPLE FOOTER TEXT','CLICK TO EDIT MASTER FOOTER STYLE'):footers.append(value)
 assert not footers
 video=[n for n in source.namelist() if n.startswith('ppt/media/') and n.lower().endswith(('.mp4','.wmv','.mov','.m4v'))]
 assert len(video)==9 and all(source.read(n)==current.read(n) for n in video)
 media=json.loads((root/'qa/capture-manifest.json').read_text())
 assert all(hashlib.sha256(current.read('ppt/media/'+m['media'])).hexdigest()==m['sha256'] for m in media)
docs=[]
for p in (root/'output').glob('*.docx'):
 with ZipFile(p) as z:
  t=' '.join(E.fromstring(z.read('word/document.xml')).xpath('.//w:t/text()',namespaces=ns))
  assert '\u2014' not in t and '\ufffd' not in t
  docs.append({'name':p.name,'words':len(t.split()),'pages':len(list((root/'qa/documents'/p.stem).glob('page-*.png')))})
project=workspace/'Week07UnrealPython'
assert project.exists() and not (project/'Docs').exists() and not (project/'START_HERE.txt').exists()
authored=[p for folder in ['Content/Python/week07_tooling','Scripts'] for p in (project/folder).rglob('*.py')]
for p in authored:ast.parse(p.read_text(encoding='utf-8-sig'),filename=str(p))
ui=[p for p in (project/'Content/Python/week07_tooling').rglob('*.py')]+list((project/'Plugins/Week07Tools/Source').rglob('*.cpp'))
assert not any('\u2014' in p.read_text(encoding='utf-8-sig') or 'Proposed / applied' in p.read_text(encoding='utf-8-sig') for p in ui)
with ZipFile(project/'Deliverables/Week07_Bridge_Student_Pack.zip') as z:
 assert z.testzip() is None
 assert not any(n.startswith('Docs/') for n in z.namelist())
 zip_files=len(z.namelist())
summary=json.loads((root/'qa/package-summary.json').read_text())
assert not json.loads((root/'qa/render-final/text-fit.json').read_text(encoding='utf-8-sig'))
report={**summary,'deck_sha256':hashlib.sha256(deck.read_bytes()).hexdigest(),'empty_or_default_footer_placeholders':len(footers),'em_dashes_or_garbled_characters':0,'unchanged_embedded_videos':len(video),'capture_hashes_match':True,'documents':docs,'python_files_parsed':len(authored),'bridge_pack_files':zip_files,'student_supplementary_docs_removed':True,'live_rehearsal':'qa/live-rehearsal.json'}
(root/'qa/final-audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
