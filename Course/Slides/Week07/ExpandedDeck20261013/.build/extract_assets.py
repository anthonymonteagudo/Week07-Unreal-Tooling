from pathlib import Path
from pypdf import PdfReader
from PIL import Image
import subprocess,json,hashlib
root=Path(__file__).resolve().parents[1]; assets=root/'assets'
sources={
'guerrilla':('Dan Sumaili and Sander van der Steen / Guerrilla, GDC 2017','https://d3d3g8mu99pzk9.cloudfront.net/DanSumaili/GDC2017_Sumaili_VanDerSteen_CreatingAToolsPipelineForHorizonZeroDawn.pdf'),
'vicarious':('Jeff Stewart / Vicarious Visions, GDC 2018','https://media.gdcvault.com/gdc2018/presentations/Stewart_Jeff_BuildGreatTools.pdf'),
'mission':('Etienne Palmer-Campbell / NetherRealm Studios, GDC 2025','https://media.gdcvault.com/gdc2025/Slides/Palmer-Campbell_Etienne_MissionKontrolRevolutionizing.pdf')}
records=[]
# Rectangles are in PDF points from the top-left. Notes below the figures are excluded.
figures=[('guerrilla',23,None,'horizon-editor'),('guerrilla',25,None,'horizon-dialogue'),('guerrilla',31,None,'horizon-prototype'),('guerrilla',33,None,'horizon-node-editor'),('vicarious',9,(90,54,450,324),'vv-world-builder'),('vicarious',13,(90,54,450,324),'vv-survey'),('vicarious',24,(90,54,450,324),'vv-findability'),('vicarious',35,(90,54,450,324),'vv-content-model'),('mission',26,(30,54,510,324),'mk-architecture'),('mission',34,(30,54,510,324),'mk-reflector'),('mission',46,(30,54,510,324),'mk-first'),('mission',47,(30,54,510,324),'mk-feedback'),('mission',49,(30,54,510,324),'mk-sequence'),('mission',51,(30,54,510,324),'mk-share'),('mission',55,(30,54,510,324),'mk-lifecycle')]
for source,n,box,id in figures:
 prefix=root/'.build'/id
 subprocess.run(['pdftoppm','-scale-to','2880','-png','-singlefile','-f',str(n),'-l',str(n),str(assets/(source+'.pdf')),str(prefix)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 im=Image.open(str(prefix)+'.png'); pg=PdfReader(assets/(source+'.pdf')).pages[n-1]
 if box:
  sx=im.width/float(pg.mediabox.width);sy=im.height/float(pg.mediabox.height)
  crop=tuple(round(v*(sx if i%2==0 else sy)) for i,v in enumerate(box));im=im.crop(crop)
 else:crop=None
 im.save(assets/(id+'.png'))
 records.append(dict(id=id,file=id+'.png',source=sources[source][1]+'#page='+str(n),credit=sources[source][0],pdf_page=n,crop_pdf_points=box,crop_render_pixels=crop,method='Rasterized published PDF figure; original pixels and proportions retained',rights='Third-party presentation excerpt with attribution. Public access is not a redistribution license.',use='Teaching analysis of production tooling',sha256=hashlib.sha256((assets/(id+'.png')).read_bytes()).hexdigest()))
(assets/'visual_sources.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
print('Prepared',len(records),'credited source figures')
