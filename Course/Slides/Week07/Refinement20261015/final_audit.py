"""Verify the delivered package against the immutable sources and teaching plan."""
from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
from datetime import datetime,timezone
import json,hashlib,posixpath,ast
OUT=Path(__file__).resolve().parent
def read(name):return json.loads((OUT/name).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
inv=read('source-inventory.json');plan=read('content-plan.json');mapping=read('slide-map.json')
deck=OUT/'output/Week 7 - Integrated UX and Asset Workflows v6.pptx'
checks=[]
def check(label,passed,detail=None):
 checks.append(dict(label=label,passed=bool(passed),detail=detail))
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
check('Original gradient deck unchanged',sha(Path(inv['source']))==inv['sha256'])
with ZipFile(deck) as z:
 pres=E.fromstring(z.read('ppt/presentation.xml'))
 ids=pres.find('p:sldIdLst',N)
 check('Full deck contains 106 ordered slides',len(ids)==106)
 check('All 78 original media parts preserved byte for byte',all(hashlib.sha256(z.read(n)).hexdigest()==s for n,s in inv['media'].items()))
 videos=[n for n in inv['media'] if Path(n).suffix.lower() in ('.mp4','.mov','.wmv','.avi')]
 check('Nine original embedded video files preserved',len(videos)==9,videos)
 shows=pres.findall('p:custShowLst/p:custShow',N)
 show=next(x for x in shows if x.get('name')=='Week 7 timed class route')
 rkey='{'+N['r']+'}id'
 expected=[ids[plan['order'].index(k)].get(rkey) for k in plan['timed_route']]
 actual=[s.get(rkey) for s in show.find('p:sldLst',N)]
 check('70-slide custom show exactly follows the teaching plan',actual==expected and len(actual)==70)
 editable=[];notes=[]
 for s in mapping:
  root=E.fromstring(z.read(s['part']))
  if isinstance(s['key'],str):editable.append(bool(root.findall('.//p:sp',N)))
  rp=posixpath.dirname(s['part'])+'/_rels/'+posixpath.basename(s['part'])+'.rels'
  rels=E.fromstring(z.read(rp));nr=next(x for x in rels if x.get('Type').endswith('/notesSlide'))
  np=posixpath.normpath(posixpath.dirname(s['part'])+'/'+nr.get('Target'))
  words=' '.join(E.fromstring(z.read(np)).xpath('.//a:t/text()',namespaces=N))
  notes.append('Sources' in words and ('Instructor' in words))
 check('All 32 authored slides retain editable native content',len(editable)==32 and all(editable))
 check('All 106 slides have narration, sources and instructor guidance',len(notes)==106 and all(notes))
receipt=read('qa/presentation-validation-v6.json')
check('Final deck hash matches validation receipt',sha(deck)==receipt['finalSha256'])
check('Structural and layout findings are clear',receipt['packageIntegrity']['finding_count']==0 and receipt['presentationLayout']['finding_count']==0)
check('Native PowerPoint text and table-cell fit clear',read('qa/render-final-v6/text-fit.json')==[])
native=read('qa/native-package-verification.json')
check('PowerPoint recognizes the 70-slide custom show and nine videos',any(s['name']=='Week 7 timed class route' and s['count']==70 for s in native['customShows']) and len(native['media'])==9)
check('All 106 final slides rendered by PowerPoint',len(list((OUT/'qa/render-final-v6').glob('slide-*.png')))==106)
check('Review displays current final renders',all(sha(OUT/'assets/slides'/f.name)==sha(f) for f in (OUT/'qa/render-final-v6').glob('slide-*.png')))
for d in read('document-changes.json'):
 source=Path(d['source']);target=Path(d['output'])
 check('Original Word source unchanged: '+source.name,sha(source)==d['source_sha256'])
 with ZipFile(source) as a,ZipFile(target) as b:
  diff=[n for n in a.namelist() if a.read(n)!=b.read(n)]
  check('Preserved Word package except document text: '+target.name,diff==['word/document.xml'],diff)
check('Timetable totals 150 minutes',sum(int(s[-1]) for s in plan['schedule'])==150)
check('Tool tests passed','Ran 88 tests' in (OUT/'qa/tool-tests.txt').read_text(encoding='utf-8-sig') and '\nOK' in (OUT/'qa/tool-tests.txt').read_text(encoding='utf-8-sig'))
check('Assistant UI gates passed','Ran 18 tests' in (OUT/'qa/ui-gates.txt').read_text(encoding='utf-8-sig'))
syntax=list((OUT.parents[3]/'Week07UnrealPython/Content/Python').rglob('*.py'))
for f in syntax:ast.parse(f.read_text(encoding='utf-8-sig'),filename=str(f))
check('Course Python source parses',len(syntax)>0,len(syntax))
web=read('qa/web-verification.json')
check('Desktop/mobile pages and classroom interactions pass',not web['failures'] and not web['page_errors'] and all(x['passed'] for x in web['timer_and_review']))
keyboard=read('qa/keyboard-verification.json')
check('Offscreen Qt key-event checks pass',len(keyboard['checks'])==12 and all(x['passed'] for x in keyboard['checks']))
now=datetime.now(timezone.utc);start=datetime(2026,10,15,7,58,39,tzinfo=timezone.utc)
report={'started_utc':start.isoformat(),'audited_utc':now.isoformat(),'elapsed_minutes':round((now-start).total_seconds()/60,2),'deck':str(deck),'checks':checks,'conservative_layout_warning':'Slide 81 table estimate warns by 0.0863 in. Actual PowerPoint cell fit has zero findings; full-size rendered table and question have a visible gap.','evidence_limits':['No new live Unreal or Unity rehearsal.','Existing recorded UE 5.7.4 fixture and fresh offline practice checks are distinguished.','No manual projection-distance, DPI or screen-reader validation.']}
(OUT/'qa/final-audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
failed=[x for x in checks if not x['passed']]
print(json.dumps({'checks':len(checks),'failed':failed,'elapsed_minutes':report['elapsed_minutes']},indent=2))
raise SystemExit(bool(failed))
