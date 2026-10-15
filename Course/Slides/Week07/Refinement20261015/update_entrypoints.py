"""Point course navigation at the integrated edition; keep earlier research visible."""
from pathlib import Path
import re
OUT=Path(__file__).resolve().parent
course=OUT.parents[2]
link='Slides/Week07/Refinement20261015/index.html'
p=course/'index.html';s=p.read_text(encoding='utf-8')
item='<li id="week07-current"><a href="'+link+'">Week 7: refined deck, demos, labs and peer review</a></li>'
if 'id="week07-current"' not in s:s=s.replace('<ul>','<ul>'+item,1)
p.write_text(s,encoding='utf-8')
p=course/'Slides/index.html';s=p.read_text(encoding='utf-8')
section='<section id="week07-current"><h2>Latest · Week 7 integrated teaching pack · 15 October 2026</h2><p><a href="Week07/Refinement20261015/index.html">Refined gradient PowerPoint, actual before/after review, aligned handouts and demo fallback</a>. Includes the 70-slide timed route, five UX mantras, Oster asset setup, GOLF+ examples and classroom timer.</p></section>\n'
if 'id="week07-current"' not in s:s=s.replace('<h2>Latest · Week 2',section+'<h2>Week 2',1)
s=s.replace('Reviews are iterative proposals; source PowerPoints remain separate.','Each package identifies its delivered deck or proposed changes; original source files are preserved.')
p.write_text(s,encoding='utf-8')
p=course/'README.md';s=p.read_text(encoding='utf-8')
if 'Refinement20261015/index.html' not in s:
 s=s.replace('- [Slides section]', '- [Current Week 7 teaching pack](Slides/Week07/Refinement20261015/index.html): integrated gradient deck, timed route, refined demos, lab documents and verification.\n- [Slides section]',1)
p.write_text(s,encoding='utf-8')
for folder in ('UXMantras20261015','OsterAssetSetupNotes20261015'):
 p=OUT.parent/folder/'index.html';s=p.read_text(encoding='utf-8')
 banner='<div class="notice" id="integrated-edition"><strong>Integration completed:</strong> <a href="../Refinement20261015/index.html">Open the current Week 7 deck and class pack</a>. This page preserves the earlier notes/review context; its source slide numbers and preparation status describe that earlier pass. Use the integrated pack for the current timetable and teaching materials.</div>'
 if 'id="integrated-edition"' not in s:s=re.sub(r'(</h1>)',r'\1'+banner,s,count=1)
 p.write_text(s,encoding='utf-8')
print('Course navigation and earlier research entry points now identify the integrated edition.')
