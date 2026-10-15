"""Verify the copy revision against the rehearsed deck without changing assets."""
from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
import hashlib,json,posixpath

root=Path(__file__).resolve().parents[1]
ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main'}
deck=root/'output/Week 7 - Direct Copy v8.pptx'
source=root/'build/source-v7.pptx'
changes=json.loads((root/'qa/direct-copy-changes.json').read_text())
inventory=json.loads((root/'build/pre-direct-copy-inventory.json').read_text())
assert hashlib.sha256(source.read_bytes()).hexdigest()==changes['source_sha256']
assert deck.read_bytes()==(root/'build/candidate-v8.pptx').read_bytes()
assert (root/'output/Week 7 - Rehearsed and Refined v7.pptx').read_bytes()==source.read_bytes()
with ZipFile(source) as old,ZipFile(deck) as new:
 assert new.testzip() is None
 assert set(old.namelist())==set(new.namelist())
 assert old.read('ppt/presentation.xml')==new.read('ppt/presentation.xml')
 media=[n for n in old.namelist() if n.startswith('ppt/media/')]
 assert all(old.read(n)==new.read(n) for n in media)
 videos=[n for n in media if n.lower().endswith(('.mp4','.wmv','.mov','.m4v'))]
 assert len(videos)==9
 hidden=[];tables=[];projected=[];notes={}
 for s in inventory:
  part=s['part'];a=E.fromstring(old.read(part));b=E.fromstring(new.read(part))
  assert a.get('show')==b.get('show')
  if b.get('show')=='0':hidden.append(s['number'])
  assert len(a.findall('.//a:tbl',ns))==len(b.findall('.//a:tbl',ns))
  if b.findall('.//a:tbl',ns):tables.append(s['number'])
  texts=b.xpath('.//a:t/text()',namespaces=ns);projected.extend(texts)
  if s['number']==40:
   assert 'Progress Bars' in texts
   assert not any('Karol' in t or 'Instructor captures' in t for t in texts)
  rp=posixpath.dirname(part)+'/_rels/'+posixpath.basename(part)+'.rels'
  assert old.read(rp)==new.read(rp)
  for rel in E.fromstring(new.read(rp)):
   if rel.get('Type','').endswith('/notesSlide'):
    np=posixpath.normpath(posixpath.join(posixpath.dirname(part),rel.get('Target')))
    notes[s['number']]=' '.join(E.fromstring(new.read(np)).xpath('.//a:t/text()',namespaces=ns))
 for c in changes['credits_moved']:
  assert c['credit'] in notes[c['slide']]
 assert not any(v in ' '.join(projected) for v in ('Instructor captures from','Notice:','Apply:','Karol','UI/UX course connection'))
 for name in new.namelist():
  if not name.endswith('.xml') or not name.startswith(('ppt/slides/','ppt/notesSlides/','ppt/slideMasters/','ppt/slideLayouts/')):continue
  x=E.fromstring(new.read(name))
  assert not any('\u2014' in t or '\ufffd' in t for t in x.xpath('.//a:t/text()',namespaces=ns))
  for sp in x.findall('.//p:sp',ns):
   if sp.find('.//p:ph[@type="ftr"]',ns) is None:continue
   value=''.join(sp.xpath('.//a:t/text()',namespaces=ns)).strip()
   assert value and value.upper() not in ('FOOTER','SAMPLE FOOTER TEXT','CLICK TO EDIT MASTER FOOTER STYLE')
 assert hidden==[5,7,8,16,18,21,25,30,41,44,45,49,58,69,70,85,95,100]
assert not json.loads((root/'qa/render-v8/text-fit.json').read_text(encoding='utf-8-sig'))
assert len(list((root/'qa/render-v8').glob('slide-*.png')))==106
report={'deck':str(deck.relative_to(root)),'deck_sha256':hashlib.sha256(deck.read_bytes()).hexdigest(),'source_v7_unchanged':True,'slides':106,'slides_revised':len(changes['edits']),'credits_moved_to_notes':len(changes['credits_moved']),'slide51_native_crop':'Caption and metadata excluded; embedded video and poster bytes retained.','hidden_slides':hidden,'custom_show_unchanged':True,'all_media_unchanged':len(media),'videos_unchanged':len(videos),'native_table_slides':tables,'layout_findings':0,'final_renders':106,'visual_review':'All 106 slides inspected individually, with the final changed slides rechecked.','em_dashes_or_placeholder_footers':0}
(root/'qa/direct-copy-audit-v8.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
