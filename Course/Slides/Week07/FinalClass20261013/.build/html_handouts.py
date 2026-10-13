from pathlib import Path
from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.oxml.ns import qn
import html
root=Path(__file__).resolve().parents[1];docs=root/'Documents';esc=html.escape
css='''*{box-sizing:border-box}body{margin:0;background:#eef1f5;color:#172235;font-family:Arial}.screen{max-width:1100px;margin:20px auto;font-size:16px}.page{background:white;width:1056px;min-height:816px;margin:20px auto;padding:27px 40px 30px;font:13px/1.2 Arial}.page p{margin:0 0 6px;white-space:pre-wrap}table{border-collapse:collapse;table-layout:fixed;width:100%;margin-bottom:12px}td{padding:5px 6px;vertical-align:top}td p{margin:0!important}.title td{background:#075a9e;color:white;font-size:25px;font-weight:bold}.page>p:first-child{font-size:11px;font-weight:bold}a{color:#075a9e}button{font:inherit;padding:8px 14px}@page{size:Letter landscape;margin:0}@media print{body{background:white}.screen{display:none}.page{width:11in;min-height:8.5in;margin:0;padding:.28in .42in;break-after:page}.page:last-child{break-after:auto}}@media screen and (max-width:1080px){.page{width:calc(100% - 24px);min-height:0;padding:22px}.screen{padding:12px}}'''
def para(p):
 return '<p>'+''.join(('<strong>' if r.bold else '')+esc(r.text).replace('\n','<br>')+('</strong>' if r.bold else '') for r in p.runs)+'</p>'
def pages(file):
 d=Document(file);result=['']
 for e in d.element.body:
  if e.tag==qn('w:p'):
   if e.xpath('.//w:br[@w:type="page"]'):result.append('');continue
   result[-1]+=para(Paragraph(e,d))
  elif e.tag==qn('w:tbl'):
   t=Table(e,d);widths=[c.width for c in t.columns];total=sum(widths)
   body='<table'+(' class="title"' if len(t.rows)==1 and len(t.columns)==1 else '')+'><colgroup>'+''.join(f'<col style="width:{w/total*100:.3f}%">' for w in widths)+'</colgroup>'
   for row in t.rows:
    body+='<tr>'
    for cell in row.cells:
     sh=cell._tc.xpath('./w:tcPr/w:shd');bg=sh[-1].get(qn('w:fill')) if sh else 'FFFFFF';dark=bg in ['0A2D62','075A9E','168A86','397B35','C66C0A'];body+=f'<td style="background:#{bg};color:{"white" if dark else "#172235"}">'+''.join(para(p) for p in cell.paragraphs)+'</td>'
    body+='</tr>'
   result[-1]+=body+'</table>'
 return result
mapping=[('lab1','Week 7 Lab 1 Student Handout.docx',0),('preparation','Week 7 Peer Review Packet.docx',0),('peer-sheet','Week 7 Peer Review Packet.docx',1),('reflection','Week 7 Peer Review Packet.docx',2)]
for name,file,index in mapping:
 body=pages(docs/file)[index];(root/(name+'.html')).write_text(f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(file[:-5])}</title><style>{css}</style><div class="screen"><a href="index.html">Class pack</a> · <a href="live-demo.html#handouts">All Word handouts</a> · <a href="Documents/{esc(file)}">Editable Word version</a><p><button onclick="window.print()">Print landscape Letter</button> Write on paper or in your own notes. This page does not save responses.</p></div><section class="page">{body}</section></html>',encoding='utf-8')
p=root/'index.html';s=p.read_text(encoding='utf-8');links=''.join(f'<li><a href="Documents/{esc(x.name)}">{esc(x.stem)}</a></li>' for x in sorted(docs.glob('*.docx')));s=s.replace('<h1>','<section><h2>Live demo and Week 1 style handouts</h2><p><a href="live-demo.html">Rehearsed Unreal demo, recovery and offline fallback</a></p><ul>'+links+'</ul><p>The Peer Review Packet has preparation, review and synthesis pages. Print page 2 three times per student.</p></section><h1>',1);p.write_text(s,encoding='utf-8')
print('Updated HTML handouts from checked DOCX sources')
