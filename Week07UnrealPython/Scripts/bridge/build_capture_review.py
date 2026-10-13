"""Package actual UI screenshots for slides. No synthesized application imagery."""
from pathlib import Path
import hashlib
import json
import shutil
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / 'Docs/Bridge/UI-Rehearsal'
OUT = ROOT.parent / 'Course/Slides/Week07/BridgeRehearsal20261013'
ASSETS = OUT / 'assets'
ASSETS.mkdir(parents=True, exist_ok=True)
font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 28)
small = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 20)
steps = [
    ('01-blender-baseline.png', '1  Blender baseline: one mesh, 180 cm tall'),
    ('03-unreal-before.png', '2  Publish & Send: two blue placements share the same mesh'),
    ('04-roof-vertices-selected.png', '3  Edit Mode: select all four roof vertices with X-ray'),
    ('05-roof-plus-40cm.png', '4  Move the roof +40 cm on Z; keep the floor pivot'),
    ('06-revision-sent.png', '5  Object Mode: Publish & Send the revised FBX + JSON'),
    ('07-unreal-both-updated.png', '6  Both blue placements update to 220 cm; orange Maya props stay 180 cm'),
]
frames = []
for filename, title in steps:
    img = Image.open(RAW/filename).convert('RGB')
    img.thumbnail((1440, 844), Image.Resampling.LANCZOS)
    frame = Image.new('RGB', (1440, 930), '#151a22')
    frame.paste(img, ((1440-img.width)//2, 60+(844-img.height)//2))
    draw = ImageDraw.Draw(frame)
    draw.text((24,16), title, font=font, fill='white')
    draw.text((24,903), 'Actual UI rehearsal stills • Blender 5.1.1 / Unreal 5.7.4 • 13 October 2026', font=small, fill='#b9c8d8')
    frames.append(frame)
frames[0].save(ASSETS/'ui-walkthrough.gif', save_all=True, append_images=frames[1:], duration=[3500,4500,3500,4000,3500,6000], loop=0)

canvas = Image.new('RGB', (1920,1080), '#151a22')
draw = ImageDraw.Draw(canvas)
titlefont = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 44)
draw.text((54,40),'One Blender edit updates both Unreal instances',font=titlefont,fill='white')
for x, filename, title in [(50,'03-unreal-before.png','BEFORE  ·  Blue mesh: 180 cm'),(980,'07-unreal-both-updated.png','AFTER  ·  Blue mesh: 220 cm')]:
    im = Image.open(RAW/filename).convert('RGB')
    # Crop exactly the same viewport rectangle in both raw captures.
    im = im.crop((185,137,959,686))
    im.thumbnail((890,770), Image.Resampling.LANCZOS)
    canvas.paste(im,(x+15,210))
    draw.text((x+15,145),title,font=font,fill='#55c6ed')
draw.text((65,850),'Both placements retain the same mesh asset reference.',font=font,fill='white')
draw.text((65,900),'Orange Maya comparison meshes remain 180 cm. The blue roof moves +40 cm.',font=font,fill='white')
draw.text((65,1008),'Cropped actual editor captures • same camera and lighting • raw screenshots included',font=small,fill='#b9c8d8')
canvas.save(ASSETS/'before-after.png')
for path in RAW.glob('*.png'):
    shutil.copy2(path,ASSETS/path.name)
shutil.copy2(RAW/'verification.json',OUT/'verification.json')
manifest = dict(date='2026-10-13',capture_method='Windows Computer Use window screenshots during native UI rehearsal',
               animation='Timed slideshow of actual captured stills, not continuous screen recording',
               composite_crop=[185,137,959,686],raw=[dict(file=p.name,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(RAW.glob('*.png'))])
(OUT/'capture-provenance.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
print(OUT)
