import io,urllib.request,zipfile,json
from pathlib import Path
URL='https://d3d3g8mu99pzk9.cloudfront.net/DanSumaili/GDC2017_Sumaili_VanDerSteen_CreatingAToolsPipelineForHorizonZeroDawn.pptx'
class RemoteZip(io.RawIOBase):
 def __init__(self):self.pos=0;self.size=552032678
 def seekable(self):return True
 def readable(self):return True
 def tell(self):return self.pos
 def seek(self,n,w=0):
  self.pos=n if w==0 else self.pos+n if w==1 else self.size+n
  return self.pos
 def read(self,n=-1):
  if n<0:n=self.size-self.pos
  if not n:return b''
  start=self.pos;end=min(self.size,start+n)-1
  req=urllib.request.Request(URL,headers={'User-Agent':'Mozilla/5.0','Range':f'bytes={start}-{end}'})
  with urllib.request.urlopen(req,timeout=30) as r:
   if r.status!=206:raise RuntimeError('Range unsupported; refusing full download')
   b=r.read()
  self.pos+=len(b);return b
with zipfile.ZipFile(RemoteZip()) as z:
 media=[{'name':x.filename,'bytes':x.file_size} for x in z.infolist() if x.filename.endswith(('.mp4','.wmv','.avi'))]
 print(json.dumps(media))
 root=Path(__file__).resolve().parent
 (root/'remote_media_inventory.json').write_text(json.dumps(media,indent=2))
 # Record movie references for selected editor demonstrations.
 for n in [23,24,25,31,33,46]:
  name=f'ppt/slides/_rels/slide{n}.xml.rels'
  if name in z.namelist():print(n,z.read(name).decode())
