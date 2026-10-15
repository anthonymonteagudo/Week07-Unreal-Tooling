from pathlib import Path
from PIL import Image,ImageDraw
r=Path('Course/Slides/Week07/LiveCleanup20261015');pages=list((r/'qa/documents').rglob('page-*.png'))
s=Image.new('RGB',(2000,1500),'#b8b8b8');d=ImageDraw.Draw(s)
for i,p in enumerate(pages):
 im=Image.open(p);im.thumbnail((390,710));x=(i%5)*400;y=(i//5)*750;s.paste(im,(x,y+28));d.text((x+4,y+3),p.parent.name.replace('Week 7 ','')[:24]+' '+p.stem,fill='black')
s.save(r/'qa/document-contact.jpg')
