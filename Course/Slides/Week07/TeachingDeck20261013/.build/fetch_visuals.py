import urllib.request,json,hashlib
from pathlib import Path
r=Path('../assets'); rows=[]
for name,url,context in [
('nng-testing-photo.png','https://media.nngroup.com/media/editor/2019/11/11/usabilitytesting101-29.png','https://www.nngroup.com/articles/usability-testing-101/'),
('nng-testing-flow.png','https://media.nngroup.com/media/editor/2019/11/11/usabilitytesting101_final1.png','https://www.nngroup.com/articles/usability-testing-101/'),
('parallel-prototyping.pdf','https://hci.stanford.edu/publications/2010/parallel-prototyping/ParallelPrototyping2010-submitted.pdf','https://hci.stanford.edu/publications/2010/parallel-prototyping/ParallelPrototyping2010-submitted.pdf')]:
 data=urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"}),timeout=40).read();(r/name).write_bytes(data); rows.append(dict(file=name,source=url,context=context,sha256=hashlib.sha256(data).hexdigest(),method='Unmodified source download',rights='Third-party source excerpt, attributed. No open license asserted.'))
(r/'new_visual_provenance.json').write_text(json.dumps(rows,indent=2))
print([(x['file'],(r/x['file']).stat().st_size) for x in rows])

