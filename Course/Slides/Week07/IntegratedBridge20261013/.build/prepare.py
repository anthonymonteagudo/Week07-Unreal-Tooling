from pathlib import Path
import json
import zipfile
import xml.etree.ElementTree as ET

here=Path(__file__).resolve().parent
for name in ('build.mjs','review.mjs','guide.mjs','walkthroughs.mjs','qa.mjs','check_bindings.py'):
    p=here/name
    text=p.read_text(encoding='utf-8-sig')
    text=text.replace('Week_7_Materials_and_Walkthroughs_v9.pptx','Week_7_Integrated_Bridge_v10.pptx')
    if name=='build.mjs':
        text=text.replace('../../CheckpointDeck20261013/output/Week_7_Runnable_API_Checkpoints_v8.pptx','../../MaterialsWalkthrough20261013/output/Week_7_Materials_and_Walkthroughs_v9.pptx').replace("||'v9'","||'v10'").replace('Week_7_Materials_and_Walkthroughs_${version}','Week_7_Integrated_Bridge_${version}')
        insertion=""" if(d.parity){
  text(sl,d.tag,94,60,1100,35,20,C.purple,true);
  text(sl,d.title,94,131,1100,70,44,C.ink,true);
  text(sl,d.subtitle,94,218,1092,60,27,C.purple,true);
  const table=sl.tables.add({rows:5,columns:3,left:94,top:291,width:1092,height:285,columnWidths:[256,418,418],values:d.table});
  table.borders.assign({fill:'#D9D2E5',width:1});
  for(let r=0;r<5;r++){table.rows[r].height=57;for(let c=0;c<3;c++){const cell=table.getCell(r,c);cell.fill=r===0?'#DBEFEA':'#EFF9F6';cell.text.style={typeface:'Arial',fontSize:24,color:r===0?C.purple:C.ink,bold:r===0};}}
  text(sl,d.caption,94,596,1092,40,27,C.ink,true);
  text(sl,d.question,94,641,1092,32,23,C.purple,true);
  text(sl,'WEEK 7  /  '+d.id,94,677,850,23,15,C.muted);text(sl,String(i+2),1130,677,75,23,15,C.muted);
  sl.speakerNotes.text=d.notes+'\\n\\nFacilitation: '+d.facilitation+'\\n\\nSources:\\n'+d.local.map(f=>path.join(repo,f)).join('\\n');
  tableOwners.push(i+2);continue;
 }
"""
        text=text.replace(' if(d.transition){',insertion+' if(d.transition){',1)
    if name=='review.mjs':
        text=text.replace('../../CheckpointDeck20261013/slide_sources.json','../../MaterialsWalkthrough20261013/slide_sources.json').replace('../CheckpointDeck20261013/previews/','../MaterialsWalkthrough20261013/previews/').replace('Previous v8 slide','Previous v9 slide').replace('previous v8','previous v9')
        text=text.replace('Bridge: four-minute execution, following the API setup','Bridge: one-minute comparison, then three-minute execution')
        text=text.replace('First minute: publish baseline and identify its acknowledgement. Second minute: send the prepared revised scene under the same name. Third minute: inspect both instances, dimensions, pivot and materials. Final minute: explain recovery and take a question.', 'Use BR-PARITY for 40 seconds of explanation and 20 seconds of questions. After the API slides, spend the three-minute demo on baseline acknowledgement, the prepared revision, and verification of both instances, dimensions, pivot and materials. Use the linked walkthrough for deeper recovery details.')
        text=text.replace('<h1>Week 7: sections and Unreal Python API</h1>', '<h1>Week 7: integrated lecture deck</h1><section><h2>Bridge companion integrated</h2><p>The one-slide Maya/Blender comparison is now slide 19, stable anchor BR-PARITY, immediately after the bridge overview. The one-minute explanation comes from the existing bridge demo. Total class time remains 150 minutes. You do not need to open the separate companion PPT.</p><details><summary>Original companion slide</summary><img src="../BridgeRehearsal20261013/parity-preview.png" alt="Original Maya Blender parity companion slide"></details></section>')
    if name=='guide.mjs':text=text.replace('PowerPoint v9','PowerPoint v10')
    if name=='qa.mjs':text=text.replace('!==56','!==57')
    if name=='check_bindings.py':text=text.replace('== 101','== 102')
    p.write_text(text,encoding='utf-8')

source=here.parents[1]/'MaterialsWalkthrough20261013/output/Week_7_Materials_and_Walkthroughs_v9.pptx'
ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
with zipfile.ZipFile(source) as z:
    rows=[]
    for i in range(1,102):
        xml=ET.fromstring(z.read(f'ppt/slides/slide{i}.xml'))
        rows.append({'number':i,'text':'\n'.join(t.text or '' for t in xml.findall('.//a:t',ns))})
(here.parent/'original-text.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
