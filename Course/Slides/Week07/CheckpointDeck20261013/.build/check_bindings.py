"""Confirm the delivered PowerPoint contains the actual checkpoint blocks."""
from pathlib import Path
import json
import sys
import zipfile
import xml.etree.ElementTree as ET

here = Path(__file__).resolve().parent
repo = here.parents[4]
sys.path.insert(0, str(repo / 'Week07UnrealPython/Content/Python'))
import week07_lessons

slides = json.loads((here.parent/'slide_sources.json').read_text(encoding='utf-8'))['slides']
bindings = json.loads((here.parent/'bindings.json').read_text(encoding='utf-8'))
ns = {'a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
pptx = here.parent/'output/Week_7_Runnable_API_Checkpoints_v8.pptx'
with zipfile.ZipFile(pptx) as z:
    for b in bindings:
        source = week07_lessons.blocks(b['id'])
        expected = '\n\n'.join(source[k] for k in b['blocks'])
        slide = slides[b['slide']-2]
        assert expected == slide['code'], b
        xml = ET.fromstring(z.read(f"ppt/slides/slide{b['slide']}.xml"))
        content = '\n'.join(t.text or '' for t in xml.findall('.//a:t',ns))
        assert ' '.join(expected.split()) in ' '.join(content.split()), b
    manifest = ET.fromstring(z.read('ppt/presentation.xml'))
    assert len(manifest.findall('.//{http://schemas.openxmlformats.org/presentationml/2006/main}sldId')) == 97
result = {'source_bound_slides':len(bindings),'checkpoint_files':len(week07_lessons.catalog()),'status':'pass'}
(here/'source-parity.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result))
