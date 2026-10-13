import json,zipfile,hashlib,io
from pathlib import Path
from PIL import Image
from xml.etree import ElementTree as ET
root=Path('..')
f=root/'output/Week_7_Expanded_Visual_Lecture_v3.pptx'
with zipfile.ZipFile(f) as z:
    paths=[p for p in z.namelist() if p.startswith('ppt/slides/slide') and p.endswith('.xml')]
    hidden=sum(ET.fromstring(z.read(p)).get('show')=='0' for p in paths)
    gifs=[{'part':p,'frames':Image.open(io.BytesIO(z.read(p))).n_frames} for p in z.namelist() if p.endswith('.gif')]
receipt=json.loads(Path('validation_v3.json').read_text())
actual=hashlib.sha256(f.read_bytes()).hexdigest()
assert actual==receipt['finalSha256']
assert len(paths)==65 and hidden==22 and any(g['frames']>1 for g in gifs)
qa={'deck':str(f),'slides':65,'live':43,'hidden_optional':22,'visual_slides':30,'all_rendered_slides_visually_reviewed':True,'fixes':['Removed duplicate first-run code from the transition slide','Enlarged two GDC diagrams by cropping surrounding whitespace','Added readable source names and per-visual provenance','Made optional review anchors open the correct route','Verified local companion-video playback'],'gif_parts':gifs,'final_hash_matches_receipt':True,'source_urls':129,'retained_prior_urls':119,'limitations':['Native PowerPoint playback was not tested. The video is a browser companion, not embedded PowerPoint media.','Classroom timing and Maya-to-Unreal bridge still require rehearsal.','Historical GDC captures retain original resolution; they are production examples, not API instructions.']}
Path('review-complete.json').write_text(json.dumps(qa,indent=2),encoding='utf-8')
print(json.dumps({'slides':len(paths),'hidden':hidden,'gif_frames':[g['frames'] for g in gifs],'hash_verified':True}))
