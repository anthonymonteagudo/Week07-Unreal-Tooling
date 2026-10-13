from PIL import Image,ImageChops
from pathlib import Path
import json
old=Path('../../TeachingDeck20261013/previews');new=Path('../previews');changed=[]
for p in sorted(new.glob('slide-*.png')):
 a=Image.open(old/p.name).convert('RGB');b=Image.open(p).convert('RGB')
 if a.size!=b.size or ImageChops.difference(a,b).getbbox():changed.append(p.name)
Path('pixel-review.json').write_text(json.dumps({'changed':changed,'identical':71-len(changed)},indent=2));print(changed)
