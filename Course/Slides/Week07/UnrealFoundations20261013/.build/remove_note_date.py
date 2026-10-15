"""Remove inherited Notes Master date placeholders; preserve slide content."""
from pathlib import Path
from zipfile import ZipFile
from lxml import etree

source=Path(__file__).parent/'candidate.pptx'
temp=source.with_name('without-notes-date.pptx')
ns={'p':'http://schemas.openxmlformats.org/presentationml/2006/main'}
removed=0
with ZipFile(source) as zin, ZipFile(temp,'w') as zout:
    for entry in zin.infolist():
        data=zin.read(entry.filename)
        if entry.filename.startswith(('ppt/notesMasters/','ppt/notesSlides/')) and entry.filename.endswith('.xml'):
            root=etree.fromstring(data)
            for shape in root.xpath('.//p:sp[p:nvSpPr/p:nvPr/p:ph[@type="dt"]]',namespaces=ns):
                shape.getparent().remove(shape)
                removed+=1
            for header in root.xpath('.//p:hf',namespaces=ns):
                header.set('dt','0')
            data=etree.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
        zout.writestr(entry,data)
temp.replace(source)
print(f'Removed {removed} Notes Master date placeholder(s).')
