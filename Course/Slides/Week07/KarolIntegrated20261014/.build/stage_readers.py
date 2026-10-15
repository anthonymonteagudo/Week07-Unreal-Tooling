from pathlib import Path
import shutil
r=Path.cwd(); o=r/'Course/Slides/Week07/KarolIntegrated20261014'; m=o/'.build/reader-stage'
for folder in ['Course/Tools','Course/Wiki','Course/Slides/Week07/KarolIntegrated20261014','Week07UnrealPython/Docs/Bridge']:(m/folder).mkdir(parents=True,exist_ok=True)
shutil.copyfile(r/'Course/Tools/build_readers.mjs',m/'Course/Tools/build_readers.mjs')
shutil.copyfile(o/'index.html',m/'Course/Slides/Week07/KarolIntegrated20261014/index.html')
shutil.copyfile(r/'Week07UnrealPython/Docs/Bridge/README.md',m/'Week07UnrealPython/Docs/Bridge/README.md')
