from pathlib import Path
root=Path(__file__).resolve().parent
source=(root/'../../TeachingDeck20261013/.build/build.mjs').resolve().read_text(encoding='utf-8')
source=source[source.index("import fs from"):]
source=source[:source.index('let body=')]
source=source.replace('../../ExpandedDeck20261013/output/Week_7_Expanded_Visual_Lecture_v3.pptx','../../PacedDeck20261013/output/Week_7_Paced_150_Minutes_v1.pptx')
source=source.replace('Week_7_Teaching_Revision_${version}.pptx','Week_7_Final_Class_${version}.pptx')
source=source.replace("const sl=p.slides.add", "const sl=p.slides.add")
(root/'build.mjs').write_text(source,encoding='utf-8')
