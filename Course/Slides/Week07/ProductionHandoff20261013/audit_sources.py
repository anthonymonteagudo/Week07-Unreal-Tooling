from pathlib import Path
from html import unescape, escape
import json,re
P=Path(__file__).resolve().parent; W=P.parent
data=json.loads((P/'deck_handoff.json').read_text(encoding='utf-8'))
library=(W/'PrepNotes/Unreal_Tutorial_Index.html').read_text(encoding='utf-8')
items=[]
for block in re.findall(r'<article\b.*?</article>',library,re.S):
 title=re.search(r'<h3>(.*?)</h3>',block,re.S)
 if not title:continue
 title=unescape(re.sub('<[^>]+>','',title[1]))
 links=[{'title':unescape(re.sub('<[^>]+>','',t)),'url':unescape(u)} for u,t in re.findall(r'<a[^>]+href="(https?://[^"]+)"[^>]*>(.*?)</a>',block,re.S)]
 category=re.search('data-bucket="([^"]+)"',block)
 items.append({'title':title,'category':category[1] if category else 'reference','links':links,'context':unescape(re.sub('<[^>]+>',' ',block)),'status':'Preserved from the existing 10 October tutorial review; not a claim of full viewing.'})
primary=[('Epic: Python editor scripting','https://dev.epicgames.com/documentation/en-us/unreal-engine/scripting-the-unreal-editor-using-python'),('Epic: Editor Utility Widgets','https://dev.epicgames.com/documentation/en-us/unreal-engine/editor-utility-widgets-in-unreal-engine'),('Epic: editor scripting with Blueprints','https://dev.epicgames.com/documentation/en-us/unreal-engine/scripting-the-unreal-editor-using-blueprints'),('Epic: AssetImportTask, UE 5.7','https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/AssetImportTask?application_version=5.7')]
for title,url in primary:items.append({'title':title,'category':'Primary technical reference','links':[{'title':title,'url':url}],'context':'Technical reference for the refined deck. General documentation defaults to current engine; the import-task API is explicitly UE 5.7.','status':'Page inspected 13 October 2026.'})
items.append({'title':'Unreal Engine 5 C++: Create Custom Editor Tools','category':'Later / optional paid course','links':[{'title':'Vince Petrelli: custom editor tools','url':'https://www.udemy.com/course/unrealengine5-c-one-course-solution-for-extending-editor/'}],'context':'Original user-suggested C++ course; defer full implementation. Relevant editor-tool examples, but Python and a small Blueprint interface tie-in remain the Week 7 focus.','status':'Official curriculum inspected in the earlier course comparison; not completed. Restored during this audit because the earlier URL register omitted it.'})
archive=json.loads((P/'all_source_links.json').read_text(encoding='utf-8'))
known={r['url'] for r in archive}
for item in items:
 for link in item['links']:
  if link['url'] not in known:archive.append(dict(url=link['url'],title=link['title'],origin=['ProductionHandoff20261013/source_audit.json']));known.add(link['url'])
expected=['isaacoster.artstation.com/projects/qeAwqe','udemy.com/course/becoming-an-unreal-automation-expert','learning/tutorials/aVyX','udemy.com/course/unreal-engine-5-python-automation','udemy.com/course/ue4python','udemy.com/course/unrealengine5-c-one-course-solution-for-extending-editor','PLKgYiIAqG99cwlb4Y2Pu-cSb_Vw14-t0c','tutorialsearch.io/courses/unreal-engine-5-python-automation-udm63603','learning/tutorials/WBJky','udemy.com/course/unreal-5-blueprint-tools-for-artists','udemy.com/course/unreal-engine-blueprint-automation','udemy.com/course/qt-for-python-pyside6-gui-for-beginners','linkedin.com/learning/ux-design-6-paper-prototyping','qt.io/academy/course-catalog']
checks=[{'reference':s,'found':any(s in u for u in known)} for s in expected]
assert all(c['found'] for c in checks),checks
out={'date':'2026-10-13','scope':'All existing tutorial entries, curated UX/Qt/course records, prior research links, and explicitly named recent resources','explicit_reference_checks':checks,'tutorial_and_technical_groups':items,'curated_records':data['sources'],'all_links':archive,'notes':['Every source link in the three earlier research pages remains in the register.','Discovery aggregators, Spanish resources, later-week topics, and paid courses remain labelled background; they are not evidence that their full contents were reviewed.','Courses recommended in the recent conversation are retained even when not needed for the live deck.']}
local_evidence=['Week07UnrealPython/Docs/UI/README.md','Week07UnrealPython/Docs/UI/PRESENTATION_CHECKLIST.md','Week07UnrealPython/Docs/UI/MATERIAL_VFX_SCOPE.md','Week07UnrealPython/Docs/UI/UNREAL_NATIVE_UI.md','Week07UnrealPython/Content/Python/week07_tools.py','Week07UnrealPython/Content/Python/week07_tooling/ui/views.py','Course/Slides/Week07/UnrealPythonDemo/index.html']
out['local_implementation_evidence']=local_evidence
(P/'source_audit.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
body='<h1>Complete source audit · Python, Unreal, tooling, and UX</h1><p>13 October 2026. All 14 explicitly named recent reference checks passed. '+str(len(items))+' tutorial/technical groups; '+str(len(data['sources']))+' curated UX/tooling records; '+str(len(archive))+' distinct source URLs.</p><p><a href="index.html">Production handoff</a> · <a href="source_audit.json">Structured complete register</a> · <a href="../RefinedDeck20261013/index.html">Refined deck and slide sources</a></p><p>The sections below retain individual Oster episodes, Unreal supplements, and future topics. Review status is carried forward honestly; inclusion does not imply full viewing or permission to redistribute.</p>'
for item in items:
 body+='<article><h2>'+escape(item['title'])+'</h2><p>'+escape(item['category'])+'</p><p>'+escape(item['context'])+'</p><ul>'+''.join('<li><a href="'+escape(l['url'],quote=True)+'">'+escape(l['title'])+'</a></li>' for l in item['links'])+'</ul><p>'+escape(item['status'])+'</p></article>'
body+='<h2>UX, Qt, Blueprint and course references</h2>'+''.join('<article><h3><a href="'+escape(r['url'],quote=True)+'">'+escape(r['title'])+'</a></h3><p>'+escape(r['use'])+'</p><p>'+escape(r['status'])+'</p></article>' for r in data['sources'])
body+='<h2>Current local implementation evidence</h2><p>Actual course tools and documentation used for slide examples. UI captures marked offline use fictional sample data.</p><ul>'+''.join('<li><a href="../../../../'+escape(p,quote=True)+'">'+escape(p)+'</a></li>' for p in local_evidence)+'</ul>'
body+='<h2>Every preserved external link</h2><p>This includes discovery leads and later-week references as well as the prioritized material above. Inclusion is not a claim of full review.</p><details><summary>Browse all '+str(len(archive))+' source URLs</summary>'+''.join('<p><a href="'+escape(r['url'],quote=True)+'">'+escape(r.get('title') or r['url'])+'</a><br>'+escape(' · '.join(r.get('origin',[])))+'</p>' for r in archive)+'</details>'
(P/'source_audit.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Week 7 complete source audit</title><style>body{font:17px/1.6 Arial;background:#f6f5f9;color:#25222b;max-width:1100px;margin:auto;padding:28px}article{background:white;padding:20px;margin:18px 0;border:1px solid #ddd}a{color:#594396}</style>'+body+'</html>',encoding='utf-8')
print(len(items),'source groups;',len(archive),'URLs; all named-reference checks passed')
