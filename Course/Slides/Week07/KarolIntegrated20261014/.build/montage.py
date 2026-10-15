from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import json
p=Path('Course/Slides/Week07/KarolIntegrated20261014'); data=json.loads((p/'slide-map.json').read_text(encoding='utf8'))
for start in range(0,120,20):
    sheet=Image.new('RGB',(1600,1000),'white'); d=ImageDraw.Draw(sheet)
    for j in range(20):
        n=start+j+1; im=Image.open(p/f'previews/slide-{n:03}.png');im.thumbnail((390,220));x=(j%4)*400;y=(j//4)*200;im.thumbnail((350,175));sheet.paste(im,(x,y+20));d.text((x+8,y+3),str(n),fill='black')
    sheet.save(p/f'.build/montage-{start+1}.jpg')
