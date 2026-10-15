"""Package the current student handouts and build the section guide."""
from pathlib import Path
import shutil
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'StudentMaterials'
OUT.mkdir(exist_ok=True)
source = ROOT / 'Course/Slides/Week07/LiveCleanup20261015/qa/documents'
for folder, name in [
    ('Week 7 Lab 1 Student Handout v5', 'Lab_1_Batch_Renaming.pdf'),
    ('Week 7 Peer Review Packet v4', 'Lab_2_Peer_Review.pdf'),
]:
    shutil.copy2(source / folder / 'render.pdf', OUT / name)

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='GuideTitle', fontName='Helvetica-Bold', fontSize=23, leading=28, spaceAfter=18))
styles['BodyText'].fontSize = 11
styles['BodyText'].leading = 16
styles['BodyText'].spaceAfter = 10
styles['Heading2'].fontSize = 14
styles['Heading2'].leading = 19
styles['Heading2'].spaceBefore = 14
styles['Heading2'].spaceAfter = 8
story = []
def p(text): story.append(Paragraph(text, styles['BodyText']))
def h(text): story.append(Paragraph(text, styles['Heading2']))
def title(text): story.append(Paragraph(text, styles['GuideTitle']))
base = 'https://github.com/anthonymonteagudo/Week07-Unreal-Tooling/blob/main/'
def link(label, path):
    p(f'<link href="{base}{path}" color="#225588"><u>{label}</u></link>')

title('Week 7 class guide')
p('Python in Unreal and the experience of using an artist tool. Use this guide to find each class section, run examples in the correct application, and prepare the two classroom activities.')
h('1  Set up the project')
p('Use Unreal Engine 5.7.4. Open Week07UnrealPython.uproject and the prepared map /Game/Week07/Maps/W07_MaterialVFXLab. Follow the project quick start for plugin requirements and tool setup. The native panel requires a compatible Unreal C++ toolchain if the plugin needs rebuilding.')
p('The repository uses Git LFS for large assets. Install Git LFS before cloning, then run git lfs pull in the checkout. The repository is private; sign in with an account that has access.')
link('Project quick start', 'Week07UnrealPython/README.md')
h('2  Inspect objects and assets')
p('UE01-UE03 cover the host, selected Actors and components. UE04-UE07 cover asset selection, properties, validation and paths. Predict the output, run one file, inspect the evidence, then change one input and repeat.')
p('Run Unreal files through Tools > Execute Python Script. Each file states its prerequisites. Within one file, run marked blocks in order because they share variables. Re-run setup after changing the selection.')
link('Runnable checkpoint guide', 'Week07UnrealPython/lesson_materials/week_07_api_checkpoints/README.md')
h('3  Compare Blender and Unreal')
p('BL01-BL04 cover Blender selection, Object and mesh data, evaluated geometry, and FBX export. Run Blender examples in its Text Editor. UE11-UE12 cover Unreal import tasks. These examples are host-specific: do not run a Blender example in Unreal.')
p('The optional bridge package contains its own quick start for the Maya/Blender publishing workflow. Read the included setup and recovery instructions before sending an asset.')
link('Optional bridge student package', 'Week07UnrealPython/Deliverables/Week07_Bridge_Student_Pack.zip')
story.append(PageBreak())
title('Tools and classroom activities')
h('4  Material and VFX tools')
p('Use the project quick start to prepare the scene. Open Tools > Material &amp; VFX Tools. Choose the target and inputs, Preview, inspect Before and After Apply, then Apply and check the visible result. Changing an input requires a fresh preview.')
p('Material Setup creates a material instance and assigns it to the reviewed target. VFX Placement places reviewed effects at markers. Inspect the protected crate and shared mesh as well as the changed target. Duplicate and spacing checks do not measure frame cost.')
p('Check the operation name in Edit > Undo before using it. Undoing material assignment leaves the new material asset; use a fresh unused name for another attempt. The tools do not save automatically. Practice mode uses sample data; it cannot verify Unreal behavior.')
h('5  Lab 1 and UI UX discussion')
p('Use the Lab 1 handout for the fictional batch renamer. No coding or installation is required. Fill in expected results before the instructor reveals the output. Record one discrepancy, propose one change, and describe an exact retest including the unselected asset.')
p('Discuss the five lenses: know the task; guide the eye; make actions clear; keep a shared visual language; test the whole workflow. Separate what you observed from a possible explanation.')
link('Lab 1 handout', 'StudentMaterials/Lab_1_Batch_Renaming.pdf')
h('6  Lab 2 peer review')
p('Work in a group of three and rotate owner, tester and observer through three seven-minute rounds. The owner prepares a bounded task and watches before coaching. The tester tries the task. The observer records actions, results and help needed.')
p('Use page 1 to prepare, page 2 for each tool attempt, and page 3 to review your own tool and choose one revision. Print pages 1 and 3 once per student, plus one page 2 per tool attempt. Each tool receives one observed attempt with tester and observer perspectives.')
p('Use hands-on testing, a recording, or a paper/Figma prototype. Mark engine behavior as untested when the mode cannot establish it. Finish with a specific input, action and expected result for your retest.')
link('Peer review packet', 'StudentMaterials/Lab_2_Peer_Review.pdf')
p('The separate missing-mesh Python starter remains an optional draft exercise, not a finalized or graded assignment.')

def footer(canvas, doc):
    canvas.setFont('Helvetica', 9)
    canvas.setFillColor(colors.HexColor('#555555'))
    canvas.drawString(46, 27, 'Technical Art | Week 7 | 15 October 2026')
    canvas.drawRightString(566, 27, str(doc.page))

SimpleDocTemplate(str(OUT / 'Week_7_Class_Guide.pdf'), pagesize=(612,792), leftMargin=46, rightMargin=46, topMargin=42, bottomMargin=46, title='Week 7 class guide', author='Prof. Monteagudo').build(story, onFirstPage=footer, onLaterPages=footer)
print('Packaged two existing handouts and generated the class guide.')
