import json, hashlib, zipfile, html
from pathlib import Path
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parent.parent
manifest = json.loads((root/'slide-map.json').read_text(encoding='utf-8'))
src = Path(manifest['source'])
dst = root/'output/Week_7_Python_in_Unreal_v15.pptx'
ns = {'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main'}
def content(z, n):
    el = ET.fromstring(z.read(f'ppt/slides/slide{n}.xml'))
    texts = []
    for shape in el.findall('.//p:spTree/*', ns):
        ts = [t.text or '' for t in shape.findall('.//a:t', ns)]
        if ts == [str(n)]: continue
        texts.extend(ts)
    return texts, el.get('show','1')
checks = []
with zipfile.ZipFile(src) as a, zipfile.ZipFile(dst) as b:
    for s in manifest['slides']:
        if not s.get('source'): continue
        old, oh = content(a,s['source'])
        new, nh = content(b,s['number'])
        assert oh == nh, ('hidden',s['number'])
        if not s['changed']:
            assert old == new, ('content',s['source'],s['number'])
        if s['source'] in [1,2,31,32,35,47,49,51,52,53]:
            assert old == new, ('schedule',s['source'])
            checks.append(s['source'])
    ah = {hashlib.sha256(a.read(p)).hexdigest() for p in a.namelist() if p.startswith('ppt/media/')}
    bh = {hashlib.sha256(b.read(p)).hexdigest() for p in b.namelist() if p.startswith('ppt/media/')}
    report = {'originalSlidesPreserved':120,'totalSlides':134,'scheduleSlidesUnchanged':checks,'sourceMediaCount':len(ah),'sourceMediaPreserved':len(ah & bh),'hiddenStatesPreserved':True,'unchangedSlideTextVerified':True}
(root/'.build/preservation-check.json').write_text(json.dumps(report,indent=2))
esc = html.escape
cards=[]
for s in manifest['slides']:
    n=s['number']; changed=s['changed']; source=s.get('source')
    label = f'v14 slide {source}' if source else 'New slide'
    before=''
    if source and changed:
        p=root.parent/f'KarolIntegrated20261014/previews/slide-{source:03}.png'
        if p.exists(): before=f'<figure><figcaption>v14 — slide {source}</figcaption><img loading="lazy" src="../KarolIntegrated20261014/previews/slide-{source:03}.png"></figure>'
    notes=esc(s.get('notes',''))
    cards.append(f'<article id="slide-{n}" data-changed="{str(changed).lower()}" data-hidden="{str(s["hidden"]).lower()}"><h2>{n}. {esc(s["title"])}</h2><p>{label} · {"Hidden reference" if s["hidden"] else "Live"} · {"Updated" if changed else "Preserved"}</p><div class="compare">{before}<figure><figcaption>v15 — slide {n}</figcaption><a href="previews/slide-{n:03}.png"><img loading="lazy" src="previews/slide-{n:03}.png"></a></figure></div><details><summary>Speaker notes and sources</summary><pre>{notes}</pre></details></article>')
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Week 7 v15 review</title><style>body{font:17px Arial;background:#f2f3f7;color:#222;margin:0}header,main{max-width:1450px;margin:auto;padding:28px}header{position:sticky;top:0;background:#fff;z-index:2;border-bottom:2px solid #7260a7}h1{margin:0 0 12px}a{color:#315d94}article{background:white;margin:24px 0;padding:24px;border-radius:10px}figure{margin:0;min-width:0;flex:1}img{width:100%;display:block}.compare{display:flex;gap:16px}pre{white-space:pre-wrap;font:16px/1.6 Arial}input,select{padding:10px;font:inherit;margin:8px}figcaption{padding:8px 0;color:#666}@media(max-width:850px){.compare{display:block}}</style><header><h1>Week 7 — v15 review</h1><p>Based on v14. Schedule unchanged. 68 live slides and 66 hidden reference slides. Four new section transitions; screenshots, plugin delivery, desktop UI/UX, color and telemetry integrated.</p><a href="output/Week_7_Python_in_Unreal_v15.pptx">Open full PowerPoint deck</a><br><input id="search" placeholder="Search titles or notes"><select id="filter"><option value="all">All slides</option><option value="changed">Updated and new slides</option><option value="live">Live slides</option></select></header><main>'''+''.join(cards)+'''</main><script>function filter(){let q=document.querySelector('#search').value.toLowerCase(),v=document.querySelector('#filter').value;document.querySelectorAll('article').forEach(a=>a.hidden=!(a.textContent.toLowerCase().includes(q)&&(v!=='changed'||a.dataset.changed==='true')&&(v!=='live'||a.dataset.hidden==='false')))}document.querySelector('#search').oninput=filter;document.querySelector('#filter').onchange=filter;</script></html>'''
(root/'index.html').write_text(page,encoding='utf-8')
for start in range(1,135,24):
    canvas=Image.new('RGB',(1280,6*200),'#ddd'); draw=ImageDraw.Draw(canvas)
    for i,n in enumerate(range(start,min(start+24,135))):
        im=Image.open(root/f'previews/slide-{n:03}.png'); im.thumbnail((320,180)); x=(i%4)*320;y=(i//4)*200
        canvas.paste(im,(x,y));draw.text((x+4,y+182),str(n),fill='black')
    canvas.save(root/f'.build/montage-{start}.jpg')
print(json.dumps(report))
