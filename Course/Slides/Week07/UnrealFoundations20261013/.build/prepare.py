from pathlib import Path
from zipfile import ZipFile
import json
import xml.etree.ElementTree as ET

here = Path(__file__).resolve().parent
p = here / 'build.mjs'
t = p.read_text(encoding='utf-8-sig')
t = t.replace('../../IntegratedBridge20261013/output/Week_7_Integrated_Bridge_v10.pptx', '../../StudentFacing20261013/output/Week_7_Student_Facing_v11.pptx')
t = t.replace("||'v11'", "||'v12'").replace('Week_7_Student_Facing_${version}', 'Week_7_Unreal_Foundations_${version}')
t = t.replace('if(d.api){', '''if(d.showcase){
  text(sl,'INPUT',94,231,1092,30,20,C.purple,true);
  text(sl,d.input,94,270,1092,75,26);
  const output=text(sl,d.output,94,352,1092,165,24,C.ink);
  output.text.style={typeface:'Consolas',fontSize:24,color:C.ink};
  text(sl,d.result,94,527,1092,65,24,C.purple);
  text(sl,d.experiment,94,608,1092,58,21,C.ink);
 }else if(d.api){''')
p.write_text(t, encoding='utf-8')
for name in ['guide.mjs','walkthroughs.mjs']:
    p=here/name
    t=p.read_text(encoding='utf-8-sig').replace('Week_7_Student_Facing_v11.pptx','Week_7_Unreal_Foundations_v12.pptx').replace('PowerPoint v11','PowerPoint v12')
    p.write_text(t,encoding='utf-8')
source=here.parents[1]/'StudentFacing20261013/output/Week_7_Student_Facing_v11.pptx'
with ZipFile(source) as z:
    rows=[]
    for i in range(1,103):
        xml=ET.fromstring(z.read(f'ppt/slides/slide{i}.xml'))
        rows.append({'number':i,'text':'\n'.join(x.text or '' for x in xml.findall('.//{http://schemas.openxmlformats.org/drawingml/2006/main}t'))})
(here.parent/'original-text.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
