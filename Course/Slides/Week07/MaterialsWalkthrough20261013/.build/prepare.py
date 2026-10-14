from pathlib import Path
import json
import zipfile
import xml.etree.ElementTree as ET

here = Path(__file__).resolve().parent
for name in ('build.mjs','guide.mjs','review.mjs','check_bindings.py','qa.mjs'):
    p=here/name
    text=p.read_text(encoding='utf-8-sig')
    text=text.replace('Week_7_Runnable_API_Checkpoints_v8.pptx','Week_7_Materials_and_Walkthroughs_v9.pptx')
    if name=='build.mjs':
        text=text.replace('../../SectionsAndAPI20261013/output/Week_7_Sections_and_Unreal_API_v7.pptx','../../CheckpointDeck20261013/output/Week_7_Runnable_API_Checkpoints_v8.pptx').replace("||'v8'","||'v9'").replace('Week_7_Runnable_API_Checkpoints_${version}', 'Week_7_Materials_and_Walkthroughs_${version}')
    if name=='review.mjs':
        text=text.replace("import {slides as sourceSlides} from '../../SectionsAndAPI20261013/.build/content.mjs';", "const sourceSlides=JSON.parse(await fs.readFile('../../CheckpointDeck20261013/slide_sources.json','utf8')).slides;")
        text=text.replace('../SectionsAndAPI20261013/previews/', '../CheckpointDeck20261013/previews/').replace('Previous v7 slide','Previous v8 slide').replace('previous v7','previous v8')
        text=text.replace('<nav><a href="output/', '<nav><a href="walkthrough.html">Manual and API walkthrough</a><a href="maya.html">Maya bridge walkthrough</a><a href="output/',1)
        text=text.replace('VFX: four-minute execution', 'VFX: 3¼-minute execution').replace('Keep the final minute for questions. Use existing captures', 'Reserve the final 15 seconds for questions. Use existing captures')
    if name=='guide.mjs':
        text=text.replace('PowerPoint v8','PowerPoint v9').replace('<nav><a href="index.html">', '<nav><a href="walkthrough.html">Manual and API walkthrough</a><a href="maya.html">Maya bridge</a><a href="index.html">',1)
    if name=='check_bindings.py':
        text=text.replace('== 97','== 101')
    if name=='qa.mjs':
        text=text.replace("'teach','checkpoints'", "'teach','checkpoints','walkthrough','maya'").replace('!==54','!==56').replace('!==43','!==45')
    p.write_text(text,encoding='utf-8')

old=here.parents[1]/'CheckpointDeck20261013/output/Week_7_Runnable_API_Checkpoints_v8.pptx'
ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
with zipfile.ZipFile(old) as z:
    rows=[]
    for i in range(1,98):
        xml=ET.fromstring(z.read(f'ppt/slides/slide{i}.xml'))
        rows.append({'number':i,'text':'\n'.join(t.text or '' for t in xml.findall('.//a:t',ns))})
(here.parent/'original-text.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
