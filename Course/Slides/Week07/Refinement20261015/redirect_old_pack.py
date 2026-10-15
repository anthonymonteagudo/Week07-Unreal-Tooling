"""Resolve old active entry points without removing the previous editions."""
from pathlib import Path
import re
OUT=Path(__file__).resolve().parent
OLD=OUT.parent/'FinalClass20261013'
destinations={'index.html':'index.html','dashboard.html':'dashboard.html','lab1.html':'lab1.html','peer-sheet.html':'peer-review.html','preparation.html':'peer-review.html','reflection.html':'peer-review.html','facilitator.html':'facilitator.html','reveal.html':'reveal.html'}
for name,target in destinations.items():
 p=OLD/name;archive=OLD/(p.stem+'-archived-20261015.html')
 if not archive.exists():archive.write_bytes(p.read_bytes())
 href='../Refinement20261015/'+target
 p.write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="0;url='+href+'"><title>Updated Week 7 material</title><body><h1>Updated Week 7 material</h1><p><a href="'+href+'">Open the current edition</a>. The timetable, three-role reviews and seven-minute timer now match the refined slide deck.</p><p><a href="'+archive.name+'">Archived previous edition</a></p></body></html>',encoding='utf-8')
p=OLD/'live-demo.html';t=p.read_text(encoding='utf-8')
archive=OLD/'live-demo-archived-20261015.html'
if not archive.exists():archive.write_text(t,encoding='utf-8')
t=re.sub(r'<h2>Keep the existing teaching slot</h2><table>.*?</table>','<h2>Keep the ten-minute instructor allocation</h2><table><tr><th>Elapsed</th><th>Sequence</th></tr><tr><td>0:00–5:00</td><td>Material prediction, Preview, Apply, protected-scope check, duplicate-name block and assignment Undo.</td></tr><tr><td>5:00–9:00</td><td>Three-anchor VFX Preview/Apply, repeat block, VFX Undo and performance boundary.</td></tr><tr><td>9:00–10:00</td><td>Questions and transition. Compare the other interface with captures rather than repeating the full demonstration.</td></tr></table><p><a href="../Refinement20261015/live-demo.html">Current run sheet and recovery guide</a></p>',t,flags=re.S)
t=t.replace('For peer review, print preparation page 1, three copies of review page 2, and synthesis page 3 per student.','For each student, print one preparation page, one review page and one reflection page. Each tool receives one observed attempt with tester and observer perspectives.')
for old,new in [('Week 7 Lab 1 Student Handout.docx','Week 7 Lab 1 Student Handout v4.docx'),('Week 7 Lab Instructor Guide.docx','Week 7 Lab Instructor Guide v4.docx'),('Week 7 Live Demo Run Sheet.docx','Week 7 Live Demo Run Sheet v4.docx'),('Week 7 Peer Review Packet v2.docx','Week 7 Peer Review Packet v3.docx')]:
 t=t.replace('Documents/'+old,'../Refinement20261015/output/'+new)
t=t.replace('The test found and fixed the UE 5.7 texture setter’s misleading return value by checking actual parameter state.','The recorded UE 5.7.4 fixture exposed a texture setter returning False even when its binding was present; the backend verifies the parameter readback.')
p.write_text(t,encoding='utf-8')
print('Updated eight legacy entry points and the recorded walkthrough; previous editions preserved.')
