"""Build the Week 7 UX integration review from preserved notes and v15 evidence."""
from pathlib import Path
import json, re, shutil, hashlib, html, os
from lesson_detail import DETAILS

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
TMP = ROOT / 'tmp/ux_review_20261015'
VAULT = Path('C:/Users/antho/OneDrive/Desktop/Notes/anthony/personal/Duke Tech Art Course Notes/17 UI UX Design Principles')
GOLF = Path('C:/Users/antho/git/golfplus-notes')
DECK = ROOT / 'Course/Slides/Week07/DesktopIntegrated20261014'
NOTES = json.loads(((OUT/'sources/raw-note-extraction.json') if (OUT/'sources/raw-note-extraction.json').exists() else TMP/'notes.json').read_text(encoding='utf-8'))
SLIDES = json.loads(((OUT/'sources/current-slide-extraction.json') if (OUT/'sources/current-slide-extraction.json').exists() else TMP/'slides.json').read_text(encoding='utf-8'))
for name in ('notes','sources','assets','before','after'):
    (OUT/name).mkdir(exist_ok=True)

# The source lesson number remains stable even when the source's wording is repaired.
# Each tuple is: distilled principle, tool application, qualification, study prompt.
LESSONS = {
1: ('Visual design communicates purpose, relationships and available actions. Appearance participates in solving a problem.', 'Name the artist, task, intended result and protected scope before styling a tool.', 'The lecturer’s career anecdotes illustrate his perspective; they are not comparative usability studies.', 'Which decision does each visible element help the artist make?'),
2: ('Evaluate references against the audience and situation they serve. A polished layout is not evidence that it fits a different workflow.', 'Compare a marketing landing page with a repeated-use asset tool. Borrow a useful pattern, then test it in the artist’s context.', 'Adapt the warning against copying inspiration into critical reference use; do not teach a ban on references or claims about innate design ability.', 'What assumptions would change if a beginner used the same tool?'),
3: ('Appearance and behavior shape each other. A technical requirements list does not uniquely determine an understandable interface.', 'One operation can be exposed as raw parameters, a task-oriented form, or a preview-and-apply workflow.', 'The architecture and Bauhaus history is background framing, not needed to establish the Week 7 principle.', 'What can your interface explain that a function signature cannot?'),
4: ('Treat design principles as questions to investigate rather than recipes that decide a layout automatically.', 'Compare two arrangements using the same artist task and acceptance checks.', 'Nature analogies and generalizations about engineers are rhetoric, not universal laws.', 'What observation would make you revise the first layout?'),
5: ('Distinguish the implementation model, the user’s mental model, and the representation offered by the interface.', 'An artist may reason about VFX duration while the implementation manages separate spawn and kill events.', 'The notes attribute this model to Alan Cooper. Expert users can still need implementation detail; reveal it when it serves a decision.', 'Does the label describe an artist intention or an internal object?'),
6: ('The supplied source duplicates lesson 04. It does not provide a distinct explanation of this lesson.', 'Use lesson 04’s qualified principle and the recap only as a recap.', 'Do not reconstruct a missing transcript from its title. The duplicate is recorded by content hash.', 'No separate learning claim is assigned to this source.'),
7: ('Reduce unnecessary information while preserving the cues that make an action discoverable.', 'A compact tool still needs a visible target, action, status and route to useful detail.', 'Historical mobile commentary and an uncited first-impression timing claim are not current evidence of a universal effect.', 'What disappears when you make the panel smaller, and is it essential?'),
8: ('Design for the input device, context, available space and cost of repeated entry.', 'Desktop tools need keyboard focus, precise selection and resizing; a VR interface additionally needs distance, angular size and controller testing.', 'Do not convert mobile millimeter examples into universal pixel sizes or apply thumb-reach rules to desktop editors.', 'Could selection or a preset replace repeated manual path entry?'),
9: ('Balance distributes visual weight. Negative space and alignment can make relationships clear without symmetrical composition.', 'Separate task inputs, review information and actions while retaining a clear reading route.', 'A balanced appearance alone does not prove efficient operation.', 'Which group looks important, and is that the intended group?'),
10: ('Targeted changes to column widths, gutters and padding can clarify an existing interface.', 'Improve one crowded tool group before proposing a complete visual redesign.', 'The captured before/after is a design demonstration, not a measured user-study result.', 'Can a new user correctly group the same controls after the change?'),
11: ('Rhythm is the predictable recurrence of related elements and the intervals between them.', 'Repeat asset-row order, label spacing and state treatment so a user can scan successive items.', 'A repeated pattern can also repeat a poor choice; consistency must serve the task.', 'Which detail should remain stable from one row to the next?'),
12: ('Harmony comes from related visual treatments that make separate elements read as a coherent whole.', 'Use shared spacing, type roles, icon treatment and semantic state colors across related tools.', 'A visual echo communicates similarity only when the underlying meaning is also consistent.', 'Do two similar-looking controls behave similarly?'),
13: ('Alignment, spacing and emphasis can suggest a reading and action sequence.', 'Arrange source, destination, preview and commit in a route that matches the workflow.', 'Left-to-right examples reflect a reading context; localization and task structure can require a different route.', 'Where does the eye go after the most prominent element?'),
14: ('Repeated field dimensions and spacing establish a pattern; a deliberate difference can distinguish the action.', 'Use form layouts and recognizable buttons rather than hand-positioned labels and decorative action text.', 'A shorter button is not inherently more usable. Full-width buttons can be appropriate in narrow tools and are explicitly used in the GOLF+ playbook.', 'Is the action distinct while remaining consistent with the host application?'),
15: ('Dominance gives the viewer an entry point and suggests relative importance through size, contrast, position and surrounding space.', 'Emphasize the current decision. Before a valid preview, the next action is Preview rather than an unavailable Apply.', 'No single visual feature determines attention in every situation; task and familiarity also matter.', 'Does the strongest emphasis correspond to the current state?'),
16: ('Competing emphasis can obscure priorities. Reduce unnecessary competition while preserving readable secondary information.', 'Distinguish primary operations, supporting controls and reset/recovery without making any essential label illegible.', 'Claims that red/black/white is an unbeatable combination, or that a layout inevitably causes abandonment, are too absolute.', 'What can become quieter without becoming inaccessible?'),
17: ('Size, negative space and contrast interact to establish emphasis. A small isolated element can be more noticeable than a large busy one.', 'Use one intentional accent for an available task action; let decorative headings remain secondary.', 'Replace “contrast trumps size every time” with a contextual design hypothesis.', 'Would the action still be apparent without its color?'),
18: ('Consistent alignment reduces unnecessary visual paths and helps associate labels with fields.', 'Use shared label edges, logical field order and host layout managers; test the smallest supported window.', 'Do not repeat unquantified dramatic performance gains. Borders can be necessary to identify controls; removing every boundary is not the goal.', 'Which edge can align without implying an incorrect relationship?'),
20: ('Closer items tend to be perceived as related. Larger gaps can separate different tasks or information groups.', 'Keep a label, its input and its validation message together; separate global actions from per-item controls.', 'Proximity is a strong cue, not a universal winner over every other cue.', 'Does the nearest action affect that group or something elsewhere?'),
21: ('Use spacing at several scales: tight relationships inside a group and larger separation between groups.', 'Keep an asset’s name, before/after values and result associated, while separating each asset row predictably.', 'The source predicts easier scanning; it does not provide a measured time saving for our tool.', 'What grouping does a new tester perceive before you explain it?'),
23: ('Color can direct attention, carry learned meaning and support identity when used consistently.', 'Reserve semantic colors for meaningful states and pair them with text or recognizable symbols.', 'Omit the unsupported dopamine explanation and universal emotional claims. Color associations depend on context and experience.', 'Could the same hue be mistaken for a different state elsewhere?'),
24: ('Consistent color roles support continuity. Meaning must remain understandable without color alone.', 'Use labels for warning, blocked, complete and selected states; retain focus and shape cues in both light and dark hosts.', 'Do not mandate light backgrounds for all long sessions or repeat the transcript’s physiology explanation. Grayscale is not a simulation of all color-vision differences.', 'Can you understand the status when the hue cue is unavailable?'),
25: ('Evaluate color by its function: hierarchy, consistency, context and accessible communication.', 'Use palette tools for exploration, then assign roles and validate actual foreground/background pairs.', 'The lecturer’s dismissal of color theory is opinion. Art fundamentals are useful here and are explicitly retained in this adaptation.', 'What is the purpose of each accent, and does that purpose stay consistent?'),
30: ('Contrast means perceivable difference and helps distinguish boundaries and information.', 'Separate light/dark value, hue, scale, shape and spacing as different sources of visual distinction.', 'Omit the boxing anecdote and the source’s inaccurate attribution. Do not translate a metaphor into a guarantee about attention.', 'Which difference is doing the useful work in this interface?'),
31: ('Readable foreground/background differences and deliberate hierarchy help information stand out.', 'Keep all essential labels readable; use size, spacing and emphasis to distinguish importance rather than simply fading secondary text.', 'Dark versus light theme readability depends on user, environment and typography. Complementary hues do not guarantee sufficient luminance contrast.', 'Can the user read the secondary information they need to act safely?'),
32: ('Contrast can direct attention, differentiate related elements and communicate hierarchy.', 'Use these as three critique questions for the same tool, rather than three disconnected decoration rules.', '“Contrast always wins” is a memorable course mantra, not an empirical universal law.', 'Where should the strongest emphasis move when the tool changes state?'),
33: ('A grayscale check helps reveal whether hierarchy depends excessively on hue.', 'Compare the original and grayscale tool, then inspect actual contrast pairs and test focus and status cues.', 'Grayscale does not prove accessibility, simulate every color-vision deficiency, or measure WCAG ratios. Squinting is a separate coarse hierarchy check.', 'Do the target, warning and next action remain distinguishable?'),
43: ('Choose data presentation according to the question the viewer must answer. Tables support exact lookup; charts support appropriate patterns and comparisons.', 'Show affected asset, before/after, unit, status and useful next action. Let the artist inspect details behind a summary.', 'Informative graphics still encode selection and framing choices. Avoid declaring a chart bias-free or dismissing all dense views as useless.', 'Does the view answer what changed and what remains uncertain?'),
44: ('Design data for the user’s context and decisions. Reduce irrelevant decoding work while keeping needed evidence available.', 'Summarize affected, skipped and blocked items, with exact records and units available for inspection.', '“Usefulness always decreases with volume” is not universal; experts may need large structured tables. Missing, zero, untested and failed are different states.', 'Which data points let this artist choose the next action?'),
45: ('Remove redundant decoration and duplicate labels when they do not support interpretation.', 'Simplify preview tables and charts while keeping identity, units, scales, exceptions and relevant controls.', 'Do not mechanically remove every axis, border or label. Retain them when needed for comparison or correct interpretation.', 'What meaning would be lost by removing this element?'),
46: ('Simplify crowded interfaces by clarifying groups, label roles and action hierarchy.', 'Use predictable spacing and readable data; distinguish reset, preview and apply by role and current state.', 'All-caps labels, low-contrast text, text-only secondary actions and removing every container are examples, not universal prescriptions.', 'Does a quieter control remain visibly actionable and keyboard accessible?'),
47: ('Content and controls need distinct, consistent signals so users can predict what is interactive.', 'A read-only preview row should not look like an editable field. Buttons need visible labels and state cues.', 'Content may legitimately be interactive, such as asset rows that open details. The requirement is clear affordance and consistent behavior, not physical separation of all content.', 'Which elements do users expect to click, and what actually happens?'),
48: ('Differentiate primary, secondary and consequential actions without losing discoverability or familiar conventions.', 'Keep Reset away from the forward workflow; emphasize Preview until a reviewed plan allows Apply. Preserve recognizable secondary buttons.', 'Do not teach that Cancel must always be a text link, or that full-width buttons are always wrong. The final source mantra number conflicts with recap 49; use topic names.', 'Can an unfamiliar artist predict the consequence of each action?'),
49: ('The recap collects recurring principles about purpose, context, hierarchy, color, data and interaction cues.', 'Use the five Week 7 teaching mantras as a smaller, task-oriented structure; retain this recap as the source crosswalk.', 'The transcript has substantial speech-recognition errors. Its references to typography/icons do not establish completion or detailed notes for those omitted lessons.', 'Which principle explains a specific observation from the peer test?'),
}

MANTRAS = [
 ('M1','Know the task','User, context, goal, benefit and observable success; story to testable workflow.'),
 ('M2','Guide the eye','Balance, rhythm, alignment, proximity, value and contrast; compare art and tool composition.'),
 ('M3','Make actions clear','Content versus controls, state, scope, feedback, recovery and a small implementation bridge.'),
 ('M4','Keep a shared visual language','A maintained style sheet, semantic tokens, reusable patterns and AI-assisted consistency.'),
 ('M5','Test the whole workflow','Prototype at the needed fidelity, observe behavior, inspect results and retest a targeted change.'),
]

SOURCES = {
 'stories':('Atlassian: user stories','https://www.atlassian.com/agile/project-management/user-stories','Role, desired outcome and benefit; a story supports conversation rather than replacing acceptance checks.'),
 'mapping':('NN/g: story mapping','https://www.nngroup.com/articles/user-story-mapping/','Activities, steps and details; use a small vertical slice of the artist workflow.'),
 'tasks':('NN/g: test scenarios','https://www.nngroup.com/articles/task-scenarios-usability-testing/','Give a goal and context without teaching the interface’s click sequence.'),
 'art':('Getty: elements of art','https://www.getty.edu/education/teachers/building_lessons/formal_analysis.html','Value as lightness/darkness; distinguish it from a software HSV coordinate.'),
 'principles':('Getty: principles of design','https://www.getty.edu/education/teachers/building_lessons/formal_analysis2.html','Balance, emphasis, movement, rhythm and unity provide an art vocabulary for UI critique.'),
 'contrast':('W3C: text contrast','https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html','Use measured contrast as a practical desktop UI benchmark; this is not a claim of full WCAG conformance.'),
 'color':('W3C: use of color','https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html','Meaning must not depend on color alone.'),
 'figma':('Figma: prototyping','https://help.figma.com/hc/en-us/articles/360040314193-Guide-to-prototyping-in-Figma','Connected frames and interactions for flow testing; not evidence that engine operations work.'),
 'system':('Figma: design systems','https://www.figma.com/design-systems/','Shared styles, variables and component libraries support consistency across teams.'),
 'qt':('Qt: layout management','https://doc.qt.io/qtforpython-6.8/overviews/qtwidgets-layout.html','Layout managers express relationships and respond to sizing changes; check installed-version behavior.'),
 'euw':('Epic: Editor Utility Widgets','https://dev.epicgames.com/documentation/en-us/unreal-engine/editor-utility-widgets-in-unreal-engine','UMG-based editor tools; distinct from the project’s existing C++ Slate panel and an external PySide window.'),
 'coolors':('Coolors palette generator','https://coolors.co/generate','User-requested exploration link. Automated fetch returned 403; current UI/features were not inspected.'),
 'coolors-contrast':('Coolors contrast checker','https://coolors.co/contrast-checker','User-requested tool pointer; validate actual foreground/background pairs. Automated fetch returned 403.'),
}

def h(s): return html.escape(str(s),quote=True)
def href(p): return Path(p).resolve().as_uri()
def copy_asset(p,name):
    p=Path(p); target=OUT/'assets'/name
    if p.exists(): shutil.copy2(p,target); return 'assets/'+name
    return None

def build_notes():
    manifest=[]; images={}; blocks=[]
    personal=VAULT.parent.parent
    lookup={p.name:p for p in personal.rglob('Pasted image *.png')}
    for n in NOTES:
        num=int(n['name'][:2]); principle,apply,qualify,prompt=LESSONS[num]
        source=Path(n['path']); embeds=re.findall(r'!\[\[([^]|]+)',n['text'])
        image_links=[]
        for name in embeds:
            p=lookup.get(name)
            if p:
                short=f'note-{num:02d}-{len(image_links)+1:02d}.png'
                # One physical file per original image; a cross-lesson reference reuses it.
                if name not in images:
                    copy_asset(p,short); images[name]={'source':str(p),'local':'assets/'+short,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
                image_links.append(images[name]['local'])
        raw_target=OUT/'sources'/f'{num:02d}-original.md'
        raw_target.write_text(n['text'],encoding='utf-8')
        refined=f'# {num:02d} · {n["name"][3:]}\n\nRefined 15 October 2026 from the supplied Joe Natoli course notes. Original wording and captures remain preserved.\n\n## Core principle\n\n{principle}\n\n## Application to game tools\n\n{apply}\n\n## Assessment and qualification\n\n{qualify}\n\n## Try it\n\n{prompt}\n\nSource: [{source.name}]({source.as_uri()})\n\n'
        detail_md='## Study detail and teaching translation\n\n'+'\n\n'.join('- '+x for x in DETAILS[num])+'\n\n'
        refined+=detail_md
        refined+='## Original captures\n\n'+('\n\n'.join(f'![Course capture {i+1}](../{u})' for i,u in enumerate(image_links)) if image_links else 'No embedded capture is present in this source.')+'\n'
        (OUT/'notes'/f'{num:02d}-refined.md').write_text(refined,encoding='utf-8')
        # Match the instructor's Karol-note workflow: adjacent refined notes, original untouched.
        vault_refined=refined[:refined.index('## Original captures')]+ '## Original captures\n\n'+'\n\n'.join('![['+x+']]' for x in embeds)+'\n'
        (source.parent/(source.stem+' - REFINED.md')).write_text(vault_refined,encoding='utf-8')
        manifest.append({'lesson':num,'source':str(source),'sha256':n['sha256'],'refined':str(source.parent/(source.stem+' - REFINED.md')),'captures':image_links,'missing_captures':[x for x in embeds if x not in lookup]})
        gallery=''.join(f'<a href="../{u}"><img loading="lazy" src="../{u}" alt="Original course capture for lesson {num}"></a>' for u in image_links)
        notehtml=f'<h1>{num:02d} · {h(n["name"][3:])}</h1><p class="meta">Refined source notes · Joe Natoli · teaching adaptation is identified separately</p><h2>Core principle</h2><p>{h(principle)}</p><h2>Application to game tools</h2><p>{h(apply)}</p><h2>Assessment and qualification</h2><p>{h(qualify)}</p><h2>Try it</h2><p>{h(prompt)}</p><p><a href="{href(source)}">Original note</a> · <a href="{num:02d}-refined.md">Editable refined note</a></p><h2>Source captures</h2><div class="gallery">{gallery or "No embedded capture in this source."}</div>'
        notehtml=notehtml.replace('<h2>Source captures</h2>','<h2>Study detail and teaching translation</h2><ul>'+''.join('<li>'+h(x)+'</li>' for x in DETAILS[num])+'</ul><h2>Source captures</h2>')
        (OUT/'notes'/f'{num:02d}.html').write_text(page(notehtml,css='../review.css',nav='../index.html'),encoding='utf-8')
        blocks.append(f'## {num:02d} · {n["name"][3:]}\n\n{principle}\n\n**Tool application:** {apply}\n\n**Qualification:** {qualify}\n\n**Review prompt:** {prompt}\n\n'+detail_md+f'[Refined note and captures](notes/{num:02d}.html)\n')
    (OUT/'source-manifest.json').write_text(json.dumps({'notes':manifest,'images':images,'deck':str(DECK/'output/Week_7_Python_in_Unreal_v15.pptx'),'deck_sha256':hashlib.sha256((DECK/'output/Week_7_Python_in_Unreal_v15.pptx').read_bytes()).hexdigest(),'duplicate':[4,6],'not_supplied':[19,22,26,27,28,29,34,35,36,37,38,39,40,41,42]},ensure_ascii=False,indent=2),encoding='utf-8')
    (OUT/'compiled-notes.md').write_text('# UI/UX principles for game tools\n\n'+str(len(NOTES))+' supplied lesson files, with one duplicate (04/06). This is the selected-course compilation, not a claim that all 49 lessons were studied. The earlier ten-note compilation is superseded.\n\n'+'\n'.join(blocks),encoding='utf-8')
    index=VAULT/'REFINED - Course Index.md'
    if index.exists() and not (OUT/'sources/previous-course-index.md').exists(): shutil.copy2(index,OUT/'sources/previous-course-index.md')
    index.write_text('# UI/UX Design Principles — refined course index\n\nUpdated 15 October 2026. '+str(len(NOTES))+' supplied lesson files, including duplicate 04/06. Original notes remain unchanged.\n\n[Open the illustrated integration review]('+href(OUT/'index.html')+')\n\n'+ '\n'.join(f'- [{n["name"]}]({href(Path(n["path"]).parent/(Path(n["path"]).stem+" - REFINED.md"))})' for n in NOTES)+'\n',encoding='utf-8')
    return manifest

def page(body,css='review.css',nav='index.html'):
    return '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Week 7 UX integration review</title><link rel="stylesheet" href="'+css+'"><body><main><nav><a href="'+nav+'">Week 7 UX review</a></nav>'+body+'</main></body></html>'

if __name__=='__main__':
    build_notes()
    print(f'Refined {len(NOTES)} source notes and copied their available captures.')
