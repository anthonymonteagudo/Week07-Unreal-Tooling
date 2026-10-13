from pathlib import Path
f=Path('diagrams.mjs')
s=f.read_text(encoding="utf-8").replace("'Repeat a task after a targeted change','16B'","'Repeat a task after a targeted change','16E'").replace('These describe relationships, not a captured tool execution.','These describe relationships, not a captured tool execution. Use these ink-colored diagrams on white or light backgrounds; the purple preview is supplied by the page, not baked into the PNG.').replace('<html><meta','<html lang="en"><meta').replace('<img src="${d.png}">','<img src="${d.png}" alt="${d.title}">')
f.write_text(s,encoding="utf-8")
f=Path('companion.mjs')
s=f.read_text(encoding="utf-8").replace('media:d.mediaPath||null','displayCrop:d.crop||null,media:d.mediaPath||null').replace("credit:'Dan Sumaili", "sha256:(await import('node:crypto')).createHash('sha256').update(await fs.readFile('../assets/guerrilla-source-demo.mov')).digest('hex'),credit:'Dan Sumaili")
f.write_text(s,encoding="utf-8")

