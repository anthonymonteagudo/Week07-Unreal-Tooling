from pathlib import Path
from PIL import Image,ImageDraw
import pypdfium2 as pdf
r=Path('Course/Slides/Week07/LiveCleanup20261015')
for batch in range(6):
 nums=list(range(1+batch*18,min(107,19+batch*18)))
 sheet=Image.new('RGB',(1600,6*255),'#252525');draw=ImageDraw.Draw(sheet)
 for j,n in enumerate(nums):
  im=Image.open(r/f'qa/render-1/slide-{n:03}.png');im.thumbnail((520,230));x=(j%3)*533;y=(j//3)*255;sheet.paste(im,(x,y+23));draw.text((x+8,y+4),str(n),fill='white')
 sheet.save(r/f'qa/contact-{batch+1}.jpg')
for p in (r/'qa/documents').rglob('render.pdf'):
 doc=pdf.PdfDocument(p)
 for i,page in enumerate(doc):page.render(scale=1.25).to_pil().save(p.parent/f'page-{i+1}.png')
print('Slide contact sheets and all 10 document pages rendered.')
