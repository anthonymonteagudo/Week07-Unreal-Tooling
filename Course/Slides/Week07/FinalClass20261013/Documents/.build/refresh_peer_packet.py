from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import html, hashlib, json, zipfile
R=Path('Course/Slides/Week07/FinalClass20261013').resolve()
B=R/'Documents/.build/peer-refresh-20261015';B.mkdir(exist_ok=True)
ref=R/'Documents/.build/reference.docx'
# Retained Week 1 reference remains unchanged; preserve its page system and package furniture.
d=Document(ref)
for e in list(d._element.body):
 if e.tag!=qn('w:sectPr'):d._element.body.remove(e)
d.styles['Normal'].font.name='Arial';d.styles['Normal'].font.size=Pt(11)
d.styles['Normal'].paragraph_format.space_after=Pt(5)
BLUE='075A9E';INK='172235'
pages=[];current=None

def para(s,bold=False,size=11):
 p=d.add_paragraph();p.paragraph_format.space_after=Pt(5)
 r=p.add_run(s);r.bold=bold;r.font.name='Arial';r.font.size=Pt(size);r.font.color.rgb=RGBColor.from_string(INK)
 current['blocks'].append(('p',s,bold));return p

def page(label,title,intro):
 global current
 if pages:d.add_page_break()
 current={'label':label,'title':title,'blocks':[]};pages.append(current)
 p=d.add_paragraph(label.upper());p.paragraph_format.space_after=Pt(4)
 for r in p.runs:r.font.size=Pt(9);r.bold=True
 t=d.add_table(rows=1,cols=1);t.autofit=False;t.columns[0].width=Inches(10.12)
 c=t.cell(0,0);pr=c._tc.get_or_add_tcPr();sh=OxmlElement('w:shd');sh.set(qn('w:fill'),BLUE);pr.append(sh)
 p=c.paragraphs[0];p.paragraph_format.space_after=Pt(5);p.paragraph_format.space_before=Pt(5)
 r=p.add_run(title);r.bold=True;r.font.name='Arial';r.font.size=Pt(20);r.font.color.rgb=RGBColor(255,255,255)
 para(intro)

def field(title,prompt,lines=2):
 p=d.add_paragraph();p.paragraph_format.space_before=Pt(6);p.paragraph_format.space_after=Pt(2)
 r=p.add_run(title+'  ');r.bold=True;r.font.name='Arial';r.font.size=Pt(11);r.font.color.rgb=RGBColor.from_string(BLUE)
 r=p.add_run(prompt);r.font.name='Arial';r.font.size=Pt(11)
 for _ in range(lines):
  p=d.add_paragraph('________________________________________________________________________________________________________')
  p.paragraph_format.space_after=Pt(2);p.paragraph_format.line_spacing=1.7
  for r in p.runs:r.font.size=Pt(10);r.font.color.rgb=RGBColor.from_string('AAB4C0')
 current['blocks'].append(('field',title,prompt,lines))

page('Lab 2 • Preparation • 4 minutes • One per author','Prepare one peer test','Give each reviewer the same task and starting state. Ask for a result; let them choose the steps.')
para('Author ____________________   Tool / version ____________________   Group ____   Letter A / B / C / D',size=10)
field('1  User and goal','Who is this for? What do they need to do, and why?',2)
field('2  Task to read aloud','Write one short task. Include the starting input and what must stay unchanged.',3)
field('3  Success','What visible result will you check?',2)
field('4  Ready to repeat','How will you reset? What will you show if the tool cannot run?',2)
para('Example task: “Try this texture set on the target crate. Leave the protected crate unchanged.”',size=10)
para('Ready check: prepared copies • same version • start state ready • reset ready',True,10)
para('Choose a mode: hands-on / recording / paper or Figma. A prototype can test understanding; it cannot verify engine behavior.',size=10)

page('Lab 2 • Peer review • One sheet per reviewer','Test a peer tool','Reviewer: try the task and say what you expect. Author: watch first. Record any help you give.')
para('Round ____   Author ____________________   Reviewer ____________________   Tool / version ____________________',size=10)
para('Mode: hands-on / recording / paper or Figma     Result: independent / helped / blocked / execution untested',size=10)
field('1  Task','What result are you trying to reach?',1)
field('2  Evidence','What did you do, expect and observe? Where did you need help?',4)
para('Use a lens that fits your observation. You do not need to answer every question.',True,10)
para('Know the task — Is the goal and scope clear?\nGuide the eye — Do grouping, spacing and contrast show what matters?\nMake actions clear — Can you tell what to click and what state it is in?\nKeep a shared visual language — Do labels, colors and controls mean the same thing?\nTest the whole workflow — Can you check the result and recover?',size=10)
field('3  Keep and improve','One observed strength. One issue or question that matters, and why.',3)
para('If no issue appeared, say so. Mark anything you could not test. Give this sheet to the author.',size=10)
para('10-minute round: task 0:00 • try 0:30 • record and share 2:30 • swap 4:00 • finish and reset 8:00',True,10)

page('Lab 2 • Reflection • Final 5 minutes • One per author','Choose one revision','Compare your reviews. Preserve a strength, choose one change, and plan a test.')
para('Author ____________________   Distinct reviewers ____   Modes used ____________________',size=10)
field('1  Keep','Which strength did a reviewer observe?',2)
field('2  Prioritize','Which issue or uncertainty matters most? Cite a peer’s observation and its consequence.',3)
field('3  Revise','What specific change will you make or investigate?',2)
field('4  Retest','State the input, action and expected result. Include what must stay unchanged.',3)
field('5  Reflect','What changed or strengthened your judgment? What is still untested?',2)
para('A serious failure can matter even if only one reviewer sees it. Record the reviews you actually received.',size=10)

for i,sec in enumerate(d.sections):
 for p in sec.footer.paragraphs:
  p.text='Week 7  |  Technical Art  |  Peer review  |  Updated 15 October 2026'
  for r in p.runs:r.font.name='Arial';r.font.size=Pt(8)
d.core_properties.title='Week 7 Peer Review Packet';d.core_properties.author='Prof. Monteagudo'
out=R/'Documents/Week 7 Peer Review Packet v2.docx';d.save(out)
# Preserve all opaque reference package parts exactly; only the rewritten body, footer and metadata are intentional edits.
with zipfile.ZipFile(ref) as a,zipfile.ZipFile(out) as b:
 changes=[n for n in a.namelist() if n not in b.namelist() or a.read(n)!=b.read(n)]
(B/'package-diff.json').write_text(json.dumps(changes,indent=2))
(B/'artifact.md').write_text('Reference: '+str(ref)+'\nSHA256: '+hashlib.sha256(ref.read_bytes()).hexdigest()+'\nWeek 1 landscape Letter geometry, Arial and blue title retained. Body replaced with three purpose-specific forms. User requested simpler organization and shorter text: removed five-color matrix, duplicate task fields and long qualifiers. Increased body text to 11 pt, retained 10 pt compact directions. Page 2 maps the five new teaching mantras to optional observation prompts. Existing v15 slides 61–68 govern timing and review roles. New UXMantras material is a proposal, not an edited deck. All original source documents retained. Footer update and body/style metadata changes are intentional.\n',encoding='utf-8')
css='''*{box-sizing:border-box}body{margin:0;background:#eef1f5;color:#172235;font:16px/1.4 Arial}nav{max-width:1056px;margin:20px auto}a{color:#075a9e}.page{background:white;max-width:1056px;margin:20px auto;padding:28px 40px;min-height:816px}.label{font-size:12px;font-weight:bold;text-transform:uppercase}h1{background:#075a9e;color:white;font-size:27px;padding:9px 12px;margin:8px 0 10px}p{margin:7px 0;white-space:pre-line}.small{font-size:14px}.field{margin-top:14px}.field b{color:#075a9e}.line{border-bottom:1px solid #aab4c0;height:26px}button{padding:8px 14px;font:inherit}footer{font-size:11px;margin-top:20px}@page{size:Letter landscape;margin:.28in .42in}@media print{nav{display:none}body{background:white;font-size:11pt}.page{margin:0;padding:0;min-height:0;break-after:page}h1{font-size:20pt;print-color-adjust:exact}.small{font-size:10pt}.field{margin-top:8px}.line{height:20px}footer{font-size:8pt}}'''
def markup(pg):
 s='<section class="page"><div class="label">'+html.escape(pg['label'])+'</div><h1>'+html.escape(pg['title'])+'</h1>'
 for b in pg['blocks']:
  if b[0]=='p':s+='<p class="small">'+('<strong>' if b[2] else '')+html.escape(b[1])+('</strong>' if b[2] else '')+'</p>'
  else:s+='<div class="field"><b>'+html.escape(b[1])+'</b> '+html.escape(b[2])+''.join('<div class="line"></div>' for _ in range(b[3]))+'</div>'
 return s+'<footer>Week 7 | Technical Art | Updated 15 October 2026</footer></section>'
for name,pg in zip(['preparation.html','peer-sheet.html','reflection.html'],pages):
 original=R/name
 backup=B/(name+'.original');backup.exists() or backup.write_bytes(original.read_bytes())
 original.write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+pg['title']+'</title><style>'+css+'</style></head><body><nav><a href="index.html">Class pack</a> · <a href="Documents/Week%207%20Peer%20Review%20Packet%20v2.docx">Word packet</a> · <a href="preparation.html">Prepare</a> · <a href="peer-sheet.html">Review</a> · <a href="reflection.html">Reflect</a><p><button onclick="window.print()">Print this sheet</button> Write on paper or in your own notes. Responses are not saved here.</p></nav>'+markup(pg)+'</body></html>',encoding='utf-8')
# Point existing handout links at the refreshed packet; retain v1 on disk.
for f in R.glob('*.html'):
 s=f.read_text(encoding='utf-8');n=s.replace('Documents/Week 7 Peer Review Packet.docx','Documents/Week 7 Peer Review Packet v2.docx')
 if s!=n:f.write_text(n,encoding='utf-8')
(B/'content.json').write_text(json.dumps(pages,indent=2),encoding='utf-8')
print(out)
print('Changed package parts:',changes)
print('New words:',sum(len(str(x).split()) for p in pages for x in p['blocks']))


