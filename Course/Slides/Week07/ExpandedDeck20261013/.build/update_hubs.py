from pathlib import Path
root=Path(r'C:/Users/antho/Perforce/anthony.monteagudo_TechArt/anthony.monteagudo/Course')
f=root/'Slides/Week07/PrepNotes/Week07_Prep_Context.md'
s=f.read_text(encoding='utf-8')
s=s.replace('This is the current deck-production result; earlier drafts below remain research history.','This is the preceding deck-production pass; the expanded visual lecture above is current.')
s=s.replace('# Week 7 preparation · start here\n','# Week 7 preparation · start here\n\n**Expanded visual lecture · current:** [Review the 65-slide deck](../ExpandedDeck20261013/index.html): 43 live slides and 22 optional slides, with actual old/new comparisons, read-aloud notes, six new editable diagrams, AAA GDC production examples, and a playable 16-second Guerrilla clip. [Complete source and visual register](../ExpandedDeck20261013/sources.html) preserves all earlier collected sources; [motion companion](../ExpandedDeck20261013/media.html) contains the clip and course comparison GIF. Rehearse the classroom route and Maya → Unreal bridge before teaching.\n',1)
f.write_text(s,encoding='utf-8')
f=root/'Visuals/Source/build_visuals.mjs'
s=f.read_text(encoding='utf-8')
s=s.replace("fs.writeFileSync(path.join(root,'manifest.json'),", "manifest.collections=[{id:'week07',title:'Week 7: Python tooling and UX',html:'Week07/index.html',manifest:'Week07/manifest.json',count:6}];\nfs.writeFileSync(path.join(root,'manifest.json'),",1)
s=s.replace('<h2>Week 1 reference</h2>','<h2>Week 7 · tooling and UX</h2><p><a href="Week07/index.html">Six editable diagrams: shared assets, DCC handoff, preview states, interface/backend, layout sketches, and the testing loop.</a> Transparent PNGs and SVG masters have their own provenance register.</p><h2>Week 1 reference</h2>',1)
f.write_text(s,encoding='utf-8')
