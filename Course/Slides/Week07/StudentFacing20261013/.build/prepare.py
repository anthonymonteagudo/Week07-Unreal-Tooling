from pathlib import Path
from zipfile import ZipFile
import json
import xml.etree.ElementTree as ET

here=Path(__file__).resolve().parent
for name in ('build.mjs','review.mjs','guide.mjs','walkthroughs.mjs','qa.mjs','check_bindings.py'):
    p=here/name
    t=p.read_text(encoding='utf-8-sig').replace('Week_7_Integrated_Bridge_v10.pptx','Week_7_Student_Facing_v11.pptx')
    if name=='build.mjs':
        t=t.replace("import fs from 'node:fs/promises';", "import fs from 'node:fs/promises';\nimport {execFileSync} from 'node:child_process';")
        t=t.replace('../../MaterialsWalkthrough20261013/output/Week_7_Materials_and_Walkthroughs_v9.pptx','../../IntegratedBridge20261013/output/Week_7_Integrated_Bridge_v10.pptx').replace("||'v10'","||'v11'").replace('Week_7_Integrated_Bridge_${version}','Week_7_Student_Facing_${version}')
        t=t.replace("join(' Â· ')", "join('. ')")
        start=t.index('if(d.caption||d.credit){')
        end=t.index('\n if(d.mediaPath)',start)
        t=t[:start]+"if(d.caption||d.credit)text(sl,d.credit||d.caption,94,599,d.mediaPath?815:1092,27,16,C.muted);"+t[end:]
        t=t.replace('const {finalizePresentation}=', "execFileSync('C:/Users/antho/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe',['remove_note_date.py'],{stdio:'inherit'});\nconst {finalizePresentation}=")
    if name=='review.mjs':
        t=t.replace('../../MaterialsWalkthrough20261013/slide_sources.json','../../IntegratedBridge20261013/slide_sources.json').replace('../MaterialsWalkthrough20261013/previews/','../IntegratedBridge20261013/previews/').replace('Previous v9 slide','Previous v10 slide').replace('previous v9','previous v10')
        t=t.replace('<h1>Week 7: integrated lecture deck</h1>','<h1>Week 7: student-facing cleanup</h1><section><p>Corrected the garbled separator, moved the historical-capture reminder to instructor preparation, replaced technical code footers with plain run instructions, removed their machine-local hyperlinks, and removed the inherited Notes Master date placeholder.</p></section>')
    if name=='guide.mjs':t=t.replace('PowerPoint v10','PowerPoint v11')
    p.write_text(t,encoding='utf-8')
source=here.parents[1]/'IntegratedBridge20261013/output/Week_7_Integrated_Bridge_v10.pptx'
ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
with ZipFile(source) as z:
    rows=[]
    for i in range(1,103):
        r=ET.fromstring(z.read(f'ppt/slides/slide{i}.xml'))
        rows.append({'number':i,'text':'\n'.join(t.text or '' for t in r.findall('.//a:t',ns))})
(here.parent/'original-text.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
