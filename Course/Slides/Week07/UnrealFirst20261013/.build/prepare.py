from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET
import json

here=Path(__file__).resolve().parent
for name in ['build.mjs','guide.mjs','walkthroughs.mjs','review.mjs','check.py']:
    p=here/name
    t=p.read_text(encoding='utf8')
    t=t.replace('Week_7_Unreal_Foundations_v12.pptx','Week_7_Python_in_Unreal_v13.pptx')
    if name=='build.mjs':
        t=t.replace('../../StudentFacing20261013/output/Week_7_Student_Facing_v11.pptx','../../UnrealFoundations20261013/output/Week_7_Unreal_Foundations_v12.pptx')
        t=t.replace("||'v12'","||'v13'").replace('Week_7_Unreal_Foundations_${version}','Week_7_Python_in_Unreal_${version}')
        t=t.replace('if(d.question)text', "if(d.resource){const t=text(sl,d.resourceLabel,94,599,1092,27,18,C.purple,true);t.text=[[{run:d.resourceLabel,link:{uri:S[d.resource],isExternal:true},style:{typeface:'Arial',color:C.purple}}]];}\n if(d.question)text")
    if name=='review.mjs':
        t=t.replace('../../StudentFacing20261013/slide_sources.json','../../UnrealFoundations20261013/slide_sources.json').replace('../StudentFacing20261013/previews/','../UnrealFoundations20261013/previews/').replace('Previous v11','Previous v12')
        t=t.replace('Week 7: Unreal foundations','Week 7: Python in Unreal')
        t=t.replace('Unreal documentation, VS Code autocomplete, explained calls and expected input/result examples now precede the Blender comparison. The original live topics remain available. The class schedule is unchanged; slide depth is flexible, with no new per-slide time budget.', 'The instructor opening focuses on Python in Unreal, with production and public-tool examples between concepts. A brief Blender API example and Blender bridge demo close the opening immediately before colleague demonstrations. Detailed material tools and Maya bridging remain available in the appendix. The schedule is unchanged.')
        t=t.replace('v11, matching the blue/orange deck in the supplied screenshot. This is a separate v12 file','v12. This is a separate v13 file')
        t=t.replace('Unreal setup and readiness activity → documentation and VS Code → short selection/property examples → material and VFX tools → Blender comparison → Maya/Blender bridge → remaining class activities.', 'Python in Unreal: setup, documentation, VS Code, selection, objects, properties and validation, with production examples throughout. Then brief Blender API → Blender bridge → colleagues’ material and Maya demonstrations.')
        t=t.replace('s.subtitle,s.next,s.caption,s.question','s.subtitle,s.next,s.caption,s.question,s.resourceLabel,s.resource?S[s.resource]:null')
        t=t.replace("${esc(action)}</p>","${esc(action)} ${s.hidden&&!prev?.hidden?'Move to optional references to avoid duplicating colleague coverage.':''}</p>")
        cut=t.index("await fs.writeFile('../teach.html'")
        t=t[:cut]+'''await fs.writeFile('../teach.html',page('Teaching this revision',`<h1>Python in Unreal, then a brief Blender bridge</h1><nav><a href="index.html">Slide review</a><a href="${deck}">PowerPoint</a><a href="../LiveTesting20261013/index.html">Exact tests and reset steps</a></nav><section><h2>Schedule</h2><p>The existing schedule is unchanged. Content depth is flexible; no new per-slide budget is imposed.</p><h2>Instructor opening</h2><p>Focus on Unreal's Python host, API documentation, VS Code, objects, selections, properties and validation. Retain short texture-property examples as API examples. Leave the full material assistant and Maya publisher walkthrough to the colleagues' demonstrations.</p><h2>Production examples between concepts</h2><p>After readiness: Unit 2 Games and Crayta. After saved scripts: Unreal Script Editor. After asset selection: M2 Animation shot setup. After validation: AYON's artist tools. These are linked primary-source showcases; no third-party tool was installed or tested in this revision.</p><h2>Final instructor demo</h2><p>Use the Blender divider, BL01 selection example and the prepared Blender bridge. Publish the baseline, revise the roof, republish the same asset name, inspect the two blue Unreal instances, and restore the baseline. Then hand over. Detailed FBX options and Maya/Blender parity remain in the appendix.</p><h2>Live-demo limitation</h2><p>The prior receiver.json access-denied issue still needs a successful bridge rehearsal. The clean Material/VFX preflight did not validate the bridge. If it remains blocked, use the linked recorded Blender UI evidence and label it as recorded.</p><h2>Source preview cues</h2><p>Crayta: asset import and conditioning. M2 Animation: automatic shot management and the MRQ custom UI. Script Editor: README UI preview and Features checklist. AYON: Meet AYON Tools, Loading AYON Products and Publishing Products. These are topic pointers, not verified video timecodes.</p></section>`));
await fs.writeFile('../audit.html',page('Production and tool sources',`<h1>Production examples and available tools</h1><nav><a href="index.html">Review</a><a href="../UnrealFoundations20261013/audit.html">Prior Karol and API audit</a></nav><section><h2>Production talks</h2><p>Both selected cases are Unreal Fest sessions, not GDC sessions. They explicitly identify Python use. Unit 2 Games describes importing and conditioning assets for Crayta; M2 Animation describes shot/sequence creation and a rendering interface. Classroom connections are explanatory interpretations, not claims that the teaching code reproduces studio implementations.</p>${['crayta','craytaVideo','m2'].map(k=>`<p><a href="${esc(S[k])}">${esc(k)}</a></p>`).join('')}<h2>Public tools</h2><p>Unreal Script Editor is a Python/Qt tool. Its README lists autocomplete as unfinished. AYON provides a Python integration plus an Unreal plugin and requires a configured AYON environment. Epic PythonSamples supplies scripts, not a packaged tool. Availability and source were checked; UE 5.7 compatibility was not tested.</p>${['scriptEditor','scriptEditorFork','ayon','ayonCode','ayonPython','samples'].map(k=>`<p><a href="${esc(S[k])}">${esc(k)}</a></p>`).join('')}<h2>Scope and provenance</h2><p>Keep Isaac Oster / Northwood attribution for the original project and Karol / Tech Art Corner for supplemental pedagogy. No engine was launched and no current bridge success is claimed. Existing Blender captures are credited as recorded rehearsal evidence. Material and Maya details were moved to references because colleagues cover those topics, not to force the slides into an estimated time budget.</p></section>`));
console.log('Wrote v13 review and source guide');
'''
    if name=='check.py':
        t=t.replace('StudentFacing20261013/slide_sources.json','UnrealFoundations20261013/slide_sources.json')
        t=t.replace("s['id']==p['id'] and s.get('hidden',False)==p.get('hidden',False)","s['id']==p['id']")
        t=t.replace("assert [s['id'] for s in slides].index('SB') > [s['id'] for s in slides].index('09D')", "live=[s['id'] for s in slides if not s.get('hidden')]; assert live[live.index('SB'):live.index('11')+1]==['SB','BL01','10D','11']; assert all(next(s for s in slides if s['id']==i)['hidden'] for i in ['09','BR-PARITY','10','MAT2'])")
        t=t.replace('all_previous_live_topics_retained','all_previous_topics_preserved')
    p.write_text(t,encoding='utf8')
source=here.parents[1]/'UnrealFoundations20261013/output/Week_7_Unreal_Foundations_v12.pptx'
with ZipFile(source) as z:
    rows=[]
    for i in range(1,111):
        xml=ET.fromstring(z.read(f'ppt/slides/slide{i}.xml'))
        rows.append({'number':i,'text':'\n'.join(x.text or '' for x in xml.findall('.//{http://schemas.openxmlformats.org/drawingml/2006/main}t'))})
(here.parent/'original-text.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
