from PIL import Image,ImageOps,ImageDraw
from pathlib import Path
p=Path('../previews'); files=sorted(p.glob('slide-*.png'))
for start in range(0,len(files),12):
 out=Image.new('RGB',(1280,4*205),'#ddd');d=ImageDraw.Draw(out)
 for j,f in enumerate(files[start:start+12]):
  im=Image.open(f);im.thumbnail((416,175));x=(j%3)*426;y=(j//3)*205;out.paste(im,(x,y+24));d.text((x+8,y+5),f.stem,fill='black')
 out.save(f'montage-{start//12}.jpg')
