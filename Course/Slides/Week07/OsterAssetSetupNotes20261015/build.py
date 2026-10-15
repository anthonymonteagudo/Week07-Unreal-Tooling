"""Preserve Oster sources; produce adjacent refined notes and a local reading package."""
from pathlib import Path
import json, re, shutil, hashlib, ast

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
VAULT=Path('C:/Users/antho/OneDrive/Desktop/Notes/anthony/personal/Duke Tech Art Course Notes/18 Oster Asset Setup UE Python API')
INPUT=ROOT/'tmp/oster_notes_20261015/sources.json'
for name in ['notes','sources','assets','snippets']:(OUT/name).mkdir(exist_ok=True)
frozen=OUT/'sources/source-extraction.json'
if not frozen.exists():shutil.copy2(INPUT,frozen)
RAW=json.loads(frozen.read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
manifest={'date':'2026-10-15','notes':[],'images':{},'source_scope':'Three supplied Asset Setup lessons; prerequisite import/export recap identified separately.','api_stub':str(ROOT/'Week07UnrealPython/Intermediate/PythonStub/unreal.py'),'api_stub_sha256':sha(ROOT/'Week07UnrealPython/Intermediate/PythonStub/unreal.py'),'engine_association':json.loads((ROOT/'Week07UnrealPython/Week07UnrealPython.uproject').read_text())['EngineAssociation']}
combined=['# Oster asset setup notes\n\nRefined study notes for the three supplied Asset Setup lessons, with the import/export prerequisite identified separately. Original notes, code and captures are preserved.\n']
snippets=[]
for i,raw in enumerate(RAW,1):
    source=Path(raw['path'])
    if sha(source)!=raw['sha256']:raise RuntimeError('Source changed; reconcile before rebuilding: '+str(source))
    shutil.copy2(source,OUT/'sources'/f'{i:02d}-original.md')
    content=(OUT/'authored'/f'{i:02d}.md').read_text(encoding='utf-8')
    referenced=set(re.findall(r'!\[\[([^]|]+)',content))
    captures=[]
    for j,im in enumerate(raw['images'],1):
        if len(im['matches'])!=1:raise RuntimeError('Missing or ambiguous image '+im['name'])
        p=Path(im['matches'][0]);local=f'assets/{i:02d}-{j:02d}.png'
        shutil.copy2(p,OUT/local)
        manifest['images'][im['name']]={'source':str(p),'local':local,'sha256':sha(p),'lesson':i,'original_position':j,'method':'Unmodified copy'}
        captures.append(im['name'])
    extra=[n for n in captures if n not in referenced]
    full=content+'\n\n## Additional original captures\n\n'+ ('\n\n'.join('![['+n+']]' for n in extra) if extra else 'No additional captures were embedded in this source note.')+'\n'
    full+='\n## Source note\n\n[Original '+source.name+']('+source.resolve().as_uri()+')\n'
    if i==3:full+='\n[Preserved complete source script](original-script.html)\n'
    # Obsidian version keeps existing wiki embeds and native source names.
    dest=source.with_name(source.stem+' - REFINED.md')
    vaulttext=full.replace('(original-script.html)','('+ (OUT/'original-script.html').resolve().as_uri()+')')
    vaulttext=vaulttext.replace('(../../FinalClass20261013/live-captures/rehearsal.json)','('+(OUT.parent/'FinalClass20261013/live-captures/rehearsal.json').resolve().as_uri()+')')
    dest.write_text(vaulttext,encoding='utf-8')
    def image_link(m):
        info=manifest['images'][m.group(1)]
        return f'![Original lesson {i} capture {info["original_position"]}](../{info["local"]})'
    portable=re.sub(r'!\[\[([^]|]+)\]\]',image_link,full)
    portable=portable.replace('(original-script.html)','(../original-script.html)')
    (OUT/'notes'/f'{i:02d}-refined.md').write_text(portable,encoding='utf-8')
    # Compilation keeps complete teaching text; individual notes hold all captures.
    section=re.sub(r'!\[\[([^]|]+)\]\]',lambda m:'![Original course capture]('+manifest['images'][m.group(1)]['local']+')',content)
    section=section.replace('(../../FinalClass20261013/live-captures/rehearsal.json)','(../FinalClass20261013/live-captures/rehearsal.json)')
    section=re.sub(r'^(#{1,5}) ',r'#\1 ',section,flags=re.M)
    combined.append(section+'\n\n[All original captures for this lesson](notes/'+f'{i:02d}.html'+')\n')
    for j,code in enumerate(re.findall(r'```python\s*\n(.*?)```',content,re.S),1):
        ast.parse(code)
        snippet=OUT/'snippets'/f'{i:02d}-{j:02d}.py'
        snippet.write_text(code,encoding='utf-8')
        snippets.append({'lesson':i,'file':str(snippet.relative_to(OUT)),'validation':'Python syntax checked; Unreal execution not performed'})
    manifest['notes'].append({'lesson':i,'source':str(source),'source_sha256':raw['sha256'],'refined':str(dest),'local_note':f'notes/{i:02d}-refined.md','captures':len(captures)})

code=RAW[2]['text'].split('CODE:',1)[1].lstrip('\n')
ast.parse(code)
(OUT/'sources/original-buildSelectedAssets.py').write_text(code,encoding='utf-8')
manifest['original_code']={'source_note':RAW[2]['path'],'extraction':'Text after CODE:, with line endings normalized by text reading','sha256':hashlib.sha256(code.encode('utf-8')).hexdigest(),'executed':False}
assessment=(OUT/'authored/assessment.md').read_text(encoding='utf-8')
(OUT/'assessment.md').write_text(assessment,encoding='utf-8')
(OUT/'compiled-notes.md').write_text('\n\n'.join(combined),encoding='utf-8')
(VAULT/'REFINED - Course Index.md').write_text('# Oster asset setup refined course index\n\nRefined 15 October 2026. Three Asset Setup lessons; the opening import/export recap is a prerequisite, not a separate set of supplied transcripts.\n\n[Open the illustrated compilation]('+ (OUT/'index.html').resolve().as_uri()+')\n\n'+ '\n'.join(f'- [[Asset Setup {i:02d} - REFINED|Asset Setup {i:02d} — {label}]]' for i,label in [(1,'Identify imported assets'),(2,'Material slots and instance creation'),(3,'Parent, textures, assignment and saving')])+ '\n\n[Assessment and course applications]('+ (OUT/'assessment.html').resolve().as_uri()+')\n\nOriginal notes and all 44 embedded captures remain preserved.\n',encoding='utf-8')
(OUT/'source-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'snippet-checks.json').write_text(json.dumps(snippets,indent=2),encoding='utf-8')
assert all(sha(n['source'])==n['source_sha256'] for n in manifest['notes'])
assert all(sha(OUT/im['local'])==im['sha256'] for im in manifest['images'].values())
print(json.dumps({'refined_notes':len(manifest['notes']),'preserved_images':len(manifest['images']),'syntax_checked_examples':len(snippets),'originals_unchanged':True}))
