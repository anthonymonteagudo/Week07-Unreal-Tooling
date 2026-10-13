from pathlib import Path
import json, zipfile, xml.etree.ElementTree as ET, hashlib
root=Path(__file__).resolve().parents[5]
work=Path(__file__).resolve().parent.parent
prior=work.parent/'FinalClass20261013'
text=(prior/'.build/build.mjs').read_text(encoding='utf-8-sig')
text=text.replace("import {S,slides} from './content.mjs';", "import {S,slides,sections,timing} from './content.mjs';")
text=text.replace("../../PacedDeck20261013/output/Week_7_Paced_150_Minutes_v1.pptx","../../FinalClass20261013/output/Week_7_Final_Class_v3.pptx")
text=text.replace("p.slides.keep([0]);","await fs.writeFile('source-layout.json',JSON.stringify(await p.inspect({kind:'layout',maxChars:100000})));p.slides.keep([0]);")
text=text.replace("const sl=p.slides.add", "const palette=sections[d.section]; C.purple=palette.color;C.light=palette.tint;\n const sl=p.slides.add")
text=text.replace("sl.background.fill='#FFFFFF'", "sl.background.fill=d.transition?palette.color:palette.tint")
start=text.index(" text(sl,d.tag||")
end=text.index(" if(d.divider){",start)
text=text[:start]+''' if(d.transition){
  text(sl,d.tag,94,65,1080,38,24,'#FFFFFF',true);
  text(sl,d.title,94,190,1080,190,76,'#FFFFFF',true);
  text(sl,d.subtitle,94,433,1080,90,32,'#FFFFFF');
  text(sl,d.next,94,576,1080,65,26,'#FFFFFF');
  text(sl,`WEEK 7   /   ${i+2}`,94,677,1080,23,16,'#FFFFFF');
  sl.speakerNotes.text=d.notes+'\\n\\nFacilitation: '+d.facilitation;
  continue;
 }
 text(sl,d.tag,94,60,1100,35,20,C.purple,true);
 text(sl,d.title,94,125,1100,95,46,C.ink,true);
 text(sl,'WEEK 7  /  '+d.id,94,677,850,23,15,C.muted);
 text(sl,String(i+2),1130,677,75,23,15,C.muted);
 if(d.api){
  const t=text(sl,d.code,94,239,830,335,24,C.ink);
  t.text.style={typeface:'Consolas',fontSize:24,color:C.ink};
  text(sl,d.explain,943,240,250,346,24,C.purple);
 }else''' +text[end:]
text=text.replace("}else if(d.divider){", "}else if(d.divider){")
text=text.replace("path.join(repo,f)","path.isAbsolute(f)?f:path.join(repo,f)")
text=text.replace("Week_7_Final_Class_${version}.pptx", "Week_7_Sections_and_Unreal_API_${version}.pptx")
text=text.replace("process.env.DECK_VERSION||'v1'", "process.env.DECK_VERSION||'v4'")
text=text.replace("fontPolicy:{basis:'reference',families:['Arial'],referencePath:source,referenceSha256:crypto.createHash('sha256').update(await fs.readFile(source)).digest('hex')}", "fontPolicy:{basis:'design',families:['Arial','Consolas']}")
text=text.replace("{sourceDeck:source,sourceKeys:S,slides}","{sourceDeck:source,sourceKeys:S,slides,timing,sections}")
text += "\nawait fs.writeFile('../timing.json',JSON.stringify(timing,null,2));\n"
(work/'.build/build.mjs').write_text(text,encoding='utf-8')
(work/'output').mkdir(exist_ok=True)
# Extract exact original text directly from v3, preserving the physical slide numbers.
ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
z=zipfile.ZipFile(prior/'output/Week_7_Final_Class_v3.pptx')
records=[]
for i in range(1,72):
    xml=ET.fromstring(z.read(f'ppt/slides/slide{i}.xml'))
    records.append({'number':i,'text':'\n'.join(''.join(p.itertext()) for p in xml.findall('.//a:t',ns))})
(work/'original-text.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
downloads=Path('C:/Users/antho/Downloads')
inventory=[]
for name in ['Python.zip','UE5_2_project.zip','VP_Demo_UE53_starting_point.zip','ExamplePlugin_FixTextureCompression.zip','Files.zip']:
    with zipfile.ZipFile(downloads/name) as archive:
        names=archive.namelist()
        inventory.append({'archive':name,'entries':len(names),'relevant_files':[n for n in names if n.endswith(('.py','.uproject','.uplugin'))]})
(work/'downloads-inventory.json').write_text(json.dumps(inventory,indent=2),encoding='utf-8')
print('Prepared revision builder and source records')
