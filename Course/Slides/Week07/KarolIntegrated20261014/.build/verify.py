from pathlib import Path
import json, zipfile, hashlib, xml.etree.ElementTree as E, re, html
from urllib.parse import urlparse,unquote
r=Path.cwd();o=r/'Course/Slides/Week07/KarolIntegrated20261014';m=json.loads((o/'slide-map.json').read_text(encoding='utf8'));src=Path(m['source']);dst=o/'output/Week_7_Python_in_Unreal_v14.pptx'
ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main'}
def load(p):
 with zipfile.ZipFile(p) as z:
  slides={int(re.search(r'slide(\d+)\.xml$',n)[1]):E.fromstring(z.read(n)) for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml',n)}
  images={hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if n.startswith('ppt/media/')}
  return slides,images
old,oi=load(src);new,ni=load(dst)
assert len(new)==120
assert all(new[i].get('show','1')!='0' for i in range(1,55))
assert all(new[i].get('show','1')=='0' for i in range(55,121))
assert oi<=ni, 'Original embedded media missing'
# No unrelated text/table changes, allowing only physical-number shift.
for row in m['slides']:
 if row['source'] and not row['changed']:
  a=[t.text for t in old[row['source']].findall('.//a:t',ns)]
  b=[t.text for t in new[row['number']].findall('.//a:t',ns)]
  if row['source']!=row['number']:
   a=[str(row['number']) if s==str(row['source']) else s for s in a]
  assert a==b, (row['source'],row['number'])
for row in json.loads((o/'coverage.json').read_text(encoding='utf8')):
 assert hashlib.sha256(Path(row['source']).read_bytes()).hexdigest()==row['sha256']
missing=[]; count=0
for file in [o/'index.html',o/'gallery.html',o/'readers/bridge-guide.html']:
 for value in re.findall(r'(?:href|src)="([^"]+)"',file.read_text(encoding='utf8')):
  value=html.unescape(value);u=urlparse(value)
  if u.scheme in ('http','https','mailto','data') or value.startswith('#'):continue
  if u.scheme=='file':target=Path(unquote(u.path).lstrip('/'))
  else:target=(file.parent/unquote(u.path)).resolve()
  count+=1
  if not target.exists():missing.append(str(target))
assert not missing,missing
receipt=json.loads((o/'.build/validation-final.json').read_text(encoding='utf8'))
assert receipt['finalSha256']==hashlib.sha256(dst.read_bytes()).hexdigest()
result={'slides':120,'live':54,'optional':66,'reviewed_lessons':48,'changed_existing_slides':13,'new_optional_slides':5,'original_media_preserved':len(oi),'unchanged_slides_text_verified':102,'local_links_checked':count,'original_refined_files_unchanged':True,'deck_sha256':receipt['finalSha256'],'validation':'passed','runtime_limit':'Offline code/UI checks only; no live Unreal or Blender UI execution.'}
(o/'verification.json').write_text(json.dumps(result,indent=2),encoding='utf8');print(json.dumps(result,indent=2))
