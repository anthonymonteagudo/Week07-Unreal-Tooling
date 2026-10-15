"""Build the one-page class guide. Does not replace exported lab PDFs."""
from pathlib import Path
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

ROOT=Path(__file__).resolve().parent
styles=getSampleStyleSheet()
styles['Title'].fontName='Helvetica-Bold'; styles['Title'].fontSize=24; styles['Title'].alignment=0
styles['BodyText'].fontSize=10.5; styles['BodyText'].leading=14; styles['BodyText'].spaceAfter=8
styles['Heading2'].fontSize=13; styles['Heading2'].spaceBefore=10; styles['Heading2'].spaceAfter=5
story=[]
def p(text,style='BodyText'):story.append(Paragraph(text,styles[style]))
p('Week 7 class guide','Title')
p('Python in Unreal and the experience of using an artist tool. Follow the examples named in class, then use evidence to investigate and review tools.')
p('Bring the classroom pack','Heading2')
p('Extract Week07_Classroom.zip and open START_HERE.md. Print or annotate the two lab PDFs. No Unreal, Python or Git installation is needed for the classroom sheets. For digital answers, use a PDF reader\'s annotation tools; the sheets are not fillable forms.')
p('Follow the class sections','Heading2')
p('<b>Unreal Python:</b> UE01-UE07 cover the host, selection, components, asset properties and validation. Read Examples/README.md. Predict, run in the named host, then inspect the result.')
p('<b>Blender and importing:</b> BL01-BL04 and UE11-UE12 compare selection, mesh data, export and import. The Maya/Blender bridge is optional. Use the prepared input and recovery notes.')
p('<b>Material and VFX tools:</b> Choose inputs, Preview, Apply, then check the target and protected objects. A changed input needs a fresh preview. Watch the native panel and optional PySide comparison demonstrated in class.')
p('<b>Lab 1:</b> Complete expected results for the fictional batch renamer. Wait for the instructor\'s reveal, record one issue, and describe an exact retest. One sheet per group.')
p('<b>UI/UX:</b> Know the task; guide the eye; make actions clear; keep a shared visual language; test the whole workflow. Separate observations from possible explanations.')
p('<b>Lab 2:</b> In a group of three, rotate owner, tester and observer through three seven-minute rounds. Use the rotation guide on page 1. Each person needs pages 1 and 3; each tool attempt needs page 2. Finish with one revision and a retest. A recording or paper/Figma prototype can test understanding; mark engine execution as untested.')
p('Optional tool setup','Heading2')
p('To try the tools yourself, download Week07_Demo_Windows_UE5.7.4.zip, extract it and follow its README. Use <b>Windows and Unreal 5.7.4</b>. Setup uses Unreal\'s Python and the included native module; no separate Python or Visual Studio installation is required. Add <b>-WithQt</b> only for the PySide comparison.')
p('The project opens W07_MaterialVFXLab. Its README covers Preview, Apply, Undo and returning to a clean fixture.')
def footer(canvas,doc):
 canvas.setFont('Helvetica',9);canvas.setFillColor(colors.HexColor('#555555'))
 canvas.drawString(44,25,'Technical Art | Week 7 | 15 October 2026')
SimpleDocTemplate(str(ROOT/'StudentMaterials/Week_7_Class_Guide.pdf'),pagesize=(612,792),leftMargin=44,rightMargin=44,topMargin=38,bottomMargin=40,title='Week 7 class guide',author='Prof. Monteagudo').build(story,onFirstPage=footer)
print('Updated one-page class guide.')
