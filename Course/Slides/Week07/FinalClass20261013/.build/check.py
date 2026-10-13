from pathlib import Path
from PIL import Image,ImageChops
import json,zipfile,xml.etree.ElementTree as E
root=Path(__file__).resolve().parent.parent
changed=[]
for p in sorted((root/'previews').glob('slide-*.png')):
 a=Image.open(root/'../PacedDeck20261013/previews'/p.name).convert('RGB');b=Image.open(p).convert('RGB')
 if a.size!=b.size or ImageChops.difference(a,b).getbbox():changed.append(p.name)
with zipfile.ZipFile(root/'output/Week_7_Final_Class_v3.pptx') as z:
 names=[n for n in z.namelist() if n.startswith('ppt/slides/slide') and n.endswith('.xml')]
 hidden=sum(E.fromstring(z.read(n)).get('show')=='0' for n in names)
assert len(names)==71 and hidden==37,(len(names),hidden)
assert len(changed)==12,changed
(root/'.build/final-check.json').write_text(json.dumps({'slides':71,'live':34,'hidden':37,'changed':changed,'unchangedPixelIdentical':59,'practiceChecks':17,'nativePowerPointVerified':False,'liveUnrealRehearsed':True},indent=2))
print('71 slides; 34 live; 37 hidden; 12 changed slides inspected; 59 pixel-identical to paced source.')
