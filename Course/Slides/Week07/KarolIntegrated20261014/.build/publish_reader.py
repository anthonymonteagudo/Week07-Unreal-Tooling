from pathlib import Path
import re, os, shutil, json
r=Path.cwd();o=r/'Course/Slides/Week07/KarolIntegrated20261014';stage=o/'.build/reader-stage';dest=o/'readers';dest.mkdir(exist_ok=True)
source=stage/'Course/Readers/readme-78ab53f5.html'; target=dest/'bridge-guide.html'
s=source.read_text(encoding='utf8')
def remap(m):
    attr,value=m.groups()
    if value.startswith(('#','http:','https:','mailto:','data:')):return m[0]
    parts=value.split('#',1); local=(source.parent/parts[0]).resolve()
    try: relative=local.relative_to(stage)
    except ValueError:return m[0]
    real=r/relative
    if real.name=='reader.css':value='reader.css'
    elif real==r/'Course/Readers/index.html':value='../index.html'
    else:value=os.path.relpath(real,target.parent).replace('\\','/')+('#'+parts[1] if len(parts)>1 else '')
    return f'{attr}="{value}"'
s=re.sub(r'(href|src)="([^"]+)"',remap,s)
target.write_text(s,encoding='utf8');shutil.copyfile(stage/'Course/Readers/reader.css',dest/'reader.css')
p=o/'index.html';s=p.read_text(encoding='utf8').replace('../../../../Week07UnrealPython/Docs/Bridge/README.md','readers/bridge-guide.html');p.write_text(s,encoding='utf8')
print('Published readable bridge guide')
