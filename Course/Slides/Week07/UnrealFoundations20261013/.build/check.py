import ast
import json
import sys
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET

here=Path(__file__).resolve().parent
sys.path.insert(0,str(here.parents[4]/'Week07UnrealPython/Content/Python'))
import week07_lessons
data=json.loads((here.parent/'slide_sources.json').read_text(encoding='utf8'))
prior=json.loads((here.parents[1]/'StudentFacing20261013/slide_sources.json').read_text(encoding='utf8'))
slides=data['slides']
assert data['timing']==prior['timing'], 'Schedule changed'
assert all(any(s['id']==p['id'] and s.get('hidden',False)==p.get('hidden',False) for s in slides) for p in prior['slides'])
assert [s['id'] for s in slides].index('SB') > [s['id'] for s in slides].index('09D')
count=0
with ZipFile(here.parent/'output/Week_7_Unreal_Foundations_v12.pptx') as z:
    for i,s in enumerate(slides,2):
        if s.get('checkpoint'):
            c=s['checkpoint']; blocks=week07_lessons.blocks(c['id'])
            expected='\n\n'.join(blocks[k] for k in c['blocks'])
            assert expected==s['code'],s['id']
            xml=ET.fromstring(z.read(f'ppt/slides/slide{i}.xml'))
            text=' '.join(t.text or '' for t in xml.findall('.//{http://schemas.openxmlformats.org/drawingml/2006/main}t'))
            assert ' '.join(expected.split()) in ' '.join(text.split()),s['id']
            count+=1
        if s['id']=='VSC2': json.loads(s['code'])
for c in week07_lessons.catalog():
    ast.parse((here.parents[4]/'Week07UnrealPython/lesson_materials/week_07_api_checkpoints'/c['file']).read_text(encoding='utf8'))
result={'source_bound_slides':count,'total_slides':len(slides)+1,'schedule_unchanged':True,'all_previous_live_topics_retained':True,'status':'pass'}
(here/'content-check.json').write_text(json.dumps(result,indent=2),encoding='utf8')
print(result)
