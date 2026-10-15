"""Narrow OOXML edits retain the Week 1-derived handout styles and page geometry."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as E
import hashlib,json

OUT=Path(__file__).resolve().parent
SOURCE=OUT.parent/'FinalClass20261013/Documents'
W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS={'w':W}
def text(p):return ''.join(p.xpath('.//w:t/text()',namespaces=NS))
def replace(p,value):
    ts=p.findall('.//w:t',NS)
    if not ts:
        r=E.SubElement(p,'{'+W+'}r');ts=[E.SubElement(r,'{'+W+'}t')]
    ts[0].text=value
    ts[0].set('{http://www.w3.org/XML/1998/namespace}space','preserve')
    for t in ts[1:]:t.text=''
def cell(t,row,col,value):
    c=t.findall('w:tr',NS)[row].findall('w:tc',NS)[col]
    ps=c.findall('w:p',NS)
    replace(ps[0],value)
    for p in ps[1:]:replace(p,'')

reports=[]
def edit(source,name,changes,table_edits=None):
    src=SOURCE/source
    with ZipFile(src) as z:data={n:z.read(n) for n in z.namelist()}
    root=E.fromstring(data['word/document.xml']);applied=[]
    for p in root.findall('.//w:p',NS):
        old=text(p)
        if old in changes:replace(p,changes[old]);applied.append(old)
    missing=set(changes)-set(applied)
    if missing:raise ValueError((source,missing))
    if table_edits:
        tables=root.findall('w:body/w:tbl',NS)
        for ti,ri,ci,value in table_edits:cell(tables[ti],ri,ci,value)
    before=data['word/document.xml'];data['word/document.xml']=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
    dst=OUT/'output'/name
    with ZipFile(dst,'w',ZIP_DEFLATED) as z:
        for n,b in data.items():z.writestr(n,b)
    with ZipFile(src) as a,ZipFile(dst) as b:
        assert all(a.read(n)==b.read(n) for n in a.namelist() if n!='word/document.xml')
        old=E.fromstring(before)
        assert [E.tostring(x) for x in old.findall('.//w:sectPr',NS)]==[E.tostring(x) for x in root.findall('.//w:sectPr',NS)]
    reports.append({'source':str(src),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'output':str(dst),'changed_paragraphs':len(applied),'changed_cells':len(table_edits or []),'styles_and_page_geometry_preserved':True})

edit('Week 7 Lab 1 Student Handout.docx','Week 7 Lab 1 Student Handout v4.docx',{
 'LAB 1 STUDENT HANDOUT   8 MINUTES   FICTIONAL CASE':'LAB 1 STUDENT HANDOUT   5:10–5:18 PM   FICTIONAL CASE',
 'Prepare one 20-second finding. Keep your first judgment; revisit it during the UX discussion.':'Prepare one 20-second finding. Revisit it using the five UI/UX mantras. Keep observation separate from a proposed cause.',
})
edit('Week 7 Peer Review Packet v2.docx','Week 7 Peer Review Packet v3.docx',{
 'LAB 2 • PREPARATION • 4 MINUTES • ONE PER AUTHOR':'LAB 2 • TASK SETUP • FIRST 2 MINUTES • ONE PER OWNER',
 'Author ____________________   Tool / version ____________________   Group ____   Letter A / B / C / D':'Owner ____________________   Tool / version ____________________   Group ____   Letter A / B / C',
 'Give each reviewer the same task and starting state. Ask for a result; let them choose the steps.':'Prepare one bounded task and a starting state. Ask for a result; let the tester choose the steps.',
 'LAB 2 • PEER REVIEW • ONE SHEET PER REVIEWER':'LAB 2 • PEER REVIEW • ONE SHEET PER TOOL ATTEMPT',
 'Reviewer: try the task and say what you expect. Author: watch first. Record any help you give.':'Tester: try the task. Observer: record evidence and help. Owner: watch before coaching.',
 'Round ____   Author ____________________   Reviewer ____________________   Tool / version ____________________':'Round ____   Owner __________________   Tester __________________   Observer __________________',
 'If no issue appeared, say so. Mark anything you could not test. Give this sheet to the author.':'If no issue appeared, say so. Mark what you could not test. Give this sheet to the owner.',
 '10-minute round: task 0:00 • try 0:30 • record and share 2:30 • swap 4:00 • finish and reset 8:00':'7-minute round: task 0:00 • attempt 0:45 • compare evidence 3:45 • finding 5:15 • retest and reset 6:15',
 'LAB 2 • REFLECTION • FINAL 5 MINUTES • ONE PER AUTHOR':'LAB 2 • SELF REVIEW AND REVISION • FINAL 7 MINUTES • ONE PER OWNER',
 'Compare your reviews. Preserve a strength, choose one change, and plan a test.':'Review your own tool for 4 minutes. Use the final 3 minutes to choose a revision and a retest.',
 'Author ____________________   Distinct reviewers ____   Modes used ____________________':'Owner ____________________   Observed attempts ____   Review mode ____________________',
 'A serious failure can matter even if only one reviewer sees it. Record the reviews you actually received.':'One serious failure can matter. Each tool receives one observed attempt with tester and observer perspectives.',
})

instructor_changes={
 'Protect task preparation and complete attempts. Form groups of four, assign A–D, and keep tools on their prepared machines. Each pair tests in both directions. The later letter tests the earlier letter’s tool first.':'Protect the 30-minute lab. Form groups of three, assign A–C, and keep tools on prepared machines. Rotate owner, tester and observer so each tool gets one observed attempt.',
 'Call every round: 0:00 state task; 0:30 attempt; 2:30 record; 3:30 explain; 4:00 swap; 4:30 attempt; 6:30 record; 7:30 explain; 8:00 finish and reset; 10:00 switch.':'Call each 7-minute round: 0:00 state task; 0:45 attempt; 3:45 compare evidence; 5:15 keep and improve; 6:15 write the retest, reset and rotate.',
}
edits=[]
# Existing table 5 is the page-two title; table 6 is the schedule.
edits.append((4,0,0,'Facilitate three-role peer reviews'))
schedule=[('5:30–5:32','Confirm one task, prepared inputs and fallback. Assign owner, tester and observer.'),
 ('5:32–5:39','Round 1: owner A, tester B, observer C.'),('5:39–5:46','Round 2: owner B, tester C, observer A.'),
 ('5:46–5:53','Round 3: owner C, tester A, observer B.'),('Within each round','Reset and rotate during the last 45 seconds. No extra transition minute.'),
 ('5:53–5:57','Apply the same lenses to your own tool.'),('5:57–6:00','Record one strength, one revision and its retest.'),
 ('Evidence count','One observed attempt per tool, with two peer perspectives. Do not call this three independent reviews.')]
for i,row in enumerate(schedule,1):
 for j,value in enumerate(row):edits.append((5,i,j,value))
for i,value in enumerate([
 'Per student: one preparation page, one peer-review page and one reflection page. One Lab 1 sheet per group. Display the revised seven-minute timer. No installation during rounds.',
 'Ask what the tester expected, what happened and why it matters. Record help. A strength needs evidence too. If no fault appeared, record a useful uncertainty instead of inventing one.',
 'Allow one brief recovery attempt, then label the task blocked and use a recording or prototype. A walkthrough tests understanding; engine execution remains untested.',
 'Prefer triads. A fourth person can share observation. A pair alternates owner/tester and uses the remaining round for a retest. Record the actual people and attempts; do not inflate coverage.',
 'End concepts at 5:30. Protect the 5:53 self review and 5:57 revision. If late, state the reduced attempt time honestly. The Lab 1 investigation runs 5:10–5:18 within the UI/UX block.',
]):edits.append((6,i,1,value))
edit('Week 7 Lab Instructor Guide.docx','Week 7 Lab Instructor Guide v4.docx',instructor_changes,edits)

demo_changes={
 'LIVE UNREAL RUN SHEET   2 OF 4   MATERIAL   3:49–3:56':'LIVE UNREAL RUN SHEET   2 OF 4   MATERIAL   FIRST 5 MINUTES',
 'LIVE UNREAL RUN SHEET   3 OF 4   VFX   3:58–4:02':'LIVE UNREAL RUN SHEET   3 OF 4   VFX   NEXT 4 MINUTES',
 '3:56–3:58 UI comparison: native Slate belongs to the editor tab system; PySide offers the current staged interface. Both call the same workflow. Use existing Stage 1/2/3 practice captures for the brief visual comparison; do not repeat the whole operation.':'Reserve the last minute for questions and transition. Native Slate is an editor tab; PySide is a separate window. Use the prepared comparison instead of repeating both UIs. Keep the complete demo within its 10-minute allocation.',
}
demo_edits=[]
elapsed=['0:00–0:30','0:30–1:30','1:30–2:30','2:30–3:00','3:00–4:00','4:00–5:00']
for i,value in enumerate(elapsed,1):demo_edits.append((3,i,0,value))
demo_edits.append((5,5,1,'Ask what has been verified and what remains unmeasured. Placement and recovery were checked for this fixture; target-hardware performance remains unmeasured. Keep one minute for questions and transition.'))
demo_edits.append((8,1,1,'Recorded UE 5.7.4 rehearsal: material creation and texture readback; protected cube/shared mesh unchanged; assignment Undo with asset retained; exactly three VFX placements; duplicate block; VFX Undo; invalid/missing/stale selections; live PySide and native Slate Preview/Apply. Tonight’s wording refinements were checked offline.'))
edit('Week 7 Live Demo Run Sheet.docx','Week 7 Live Demo Run Sheet v4.docx',demo_changes,demo_edits)
(OUT/'document-changes.json').write_text(json.dumps(reports,indent=2),encoding='utf-8')
print(json.dumps({'updated_documents':len(reports),'source_files_unchanged':True,'page_geometry_and_styles_preserved':True}))
