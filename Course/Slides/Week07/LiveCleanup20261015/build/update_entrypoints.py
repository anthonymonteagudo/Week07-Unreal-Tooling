from pathlib import Path
root=Path('Course')
paths=[root/'index.html',root/'Slides/index.html',root/'Slides/Week07/UXMantras20261015/index.html',root/'Slides/Week07/OsterAssetSetupNotes20261015/index.html']
legacy=root/'Slides/Week07/FinalClass20261013'
for p in legacy.glob('*.html'):
 text=p.read_text(encoding='utf-8')
 if 'http-equiv="refresh"' in text and 'Refinement20261015' in text:paths.append(p)
for p in paths:
 text=p.read_text(encoding='utf-8').replace('Refinement20261015/index.html','LiveCleanup20261015/index.html')
 if p.parent==legacy:text=text.replace('../Refinement20261015/','../LiveCleanup20261015/')
 if p==root/'Slides/index.html':text=text.replace('70-slide timed route','61-slide live route and 88 visible slides').replace('Latest · Week 7 integrated teaching pack','Latest · Week 7 rehearsed teaching pack')
 p.write_text(text,encoding='utf-8')
# Preserve the prior capture walkthrough as an archive and route the live shortcut to current captures.
p=legacy/'live-demo.html'
archive=legacy/'live-demo-archived-20261015.html'
if not archive.exists():archive.write_bytes(p.read_bytes())
p.write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="0;url=../LiveCleanup20261015/walkthrough.html"><title>Current demo captures</title><body><h1>Current demo captures</h1><p><a href="../LiveCleanup20261015/walkthrough.html">Open the rehearsed Material and VFX walkthrough</a>.</p><p><a href="live-demo-archived-20261015.html">Archived earlier captures</a></p></body></html>',encoding='utf-8')
print('Updated',len(paths)+1,'entry points; prior walkthrough archived.')
