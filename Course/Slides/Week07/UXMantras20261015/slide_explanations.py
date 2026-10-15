"""15 October revision: the slides carry the explanation; live execution reinforces it."""
from pathlib import Path
import hashlib

def apply_revision(slides):
    by={p['id']:p for p in slides}
    changes={
      '40':dict(body=['UI: the labels, controls, layout and feedback an artist operates.','UX: finding the tool, preparing inputs, completing the task and checking the result.','A polished window can still hide the affected objects or make recovery difficult.','What must change, and what must remain unchanged?']),
      '41B':dict(body=['Outline the user, current workaround, starting inputs and desired result.','Map the complete task: choose → inspect scope → review → apply → check.','Include a blocked path and how the artist recovers.','Split large stories into a small useful result, not isolated backend functions.']),
      '44':dict(body=['Inputs: identify the source textures, target and material slot.','Preview: compare the intended mapping with the current assignment.','Action: apply the reviewed scope, then inspect the target and protected object.','Which information must remain beside the action?'],notes='Follow the task in this prepared capture. First identify the inputs, then the target and proposed changes, then the action. The preview supports a decision; it is not evidence that the scene has already changed. After an operation, we inspect both the intended target and an object that should remain untouched. Where would you look to confirm the material slot?'),
      '45':dict(body=['Rhythm repeats field order and spacing so the next item is predictable.','Alignment gives labels and values a shared reading edge.','Proximity uses tighter gaps within a decision and larger gaps between decisions.','Keep a validation message close to the field it explains.']),
      '47':dict(body=['The interface should identify the current state and the next useful action.','Visual emphasis follows readiness; it does not replace validation.','After Apply, inspect the result instead of treating a completion message as proof.'],notes='Read these states in sequence. Before a plan exists, Preview is the useful next action. A valid reviewed plan makes Apply available. A warning that needs acknowledgment interrupts that progression. After applying, the artist checks the intended result and protected scope. These prepared states let us discuss the behavior without depending on a successful live run. What should happen when an input changes after preview?'),
      '48':dict(body=['Input-change signals invalidate an old plan.','The interface enables Apply only when a reviewed plan is ready.','Execution still rechecks scope and limits in the session.','What if the selection changes outside this window?'],notes='This is an excerpt from the existing assistant, not a complete standalone script. The pending plan is the preview being reviewed. Apply is enabled when a plan exists and any warning has been acknowledged. That communicates readiness; the session still validates when the operation runs. The same rule can be explained from the code and state captures before we choose to demonstrate it live.',visual='Use the extracted readiness excerpt and the prepared state table. Show readable code in a wide code region, with a small matching preview crop. Keep the full method and runnable project linked in the companion.'),
      '49':dict(body=['Name the affected input and explain the problem in the artist’s terms.','Give a specific next action; retain detailed diagnostics separately.','State whether anything changed only when the operation can establish that.','A recovery message is useful when someone can continue without reading the code.']),
      '52A':dict(title='GOLF+ Course Generator: make the workflow visible',body=['Input → Parameters → Generate → optional Edit → Finalize → Integrate.','Numbered stages give the process a stable order.','Generate has the strongest emphasis in this captured state.','Collapsible groups and a labeled optional stage keep supporting detail organized.'],notes='This is the Course Generator for Paynes Valley. Read the numbered sequence from inputs through integration into the scene. The gold Generate step gives this state a strong focal point. Edit is explicitly marked optional, and the parameters can be collapsed. Now look at the warning beside Input. The icon tells us there is something to investigate, but this image does not explain its cause or whether generation should proceed. That is a useful test question, not something we can answer from appearance alone. What would you want clarified before clicking Generate?',visual='Use assets/golf-course-generator-user-20261015.png as the main image, preserving aspect ratio. Pair the full process with four brief numbered observations. Put the warning question in its own discussion caption. Keep the August overlay as a separate historical example; these are different tools.',edit='Replace the earlier proposed overlay case at 52A with the supplied Course Generator screenshot. Use its six visible stage names, not the older playbook’s shorter terminology. Retain shortcut/host context on current 52.',rationale='Uses the instructor-supplied interface to explain sequence, hierarchy and optional detail without relying on a live generation run.'),
      '53A':dict(body=['A style sheet records reusable visual and interaction decisions.','Specify type, spacing, semantic color, control states, wording and exceptions.','Tokens and components implement recurring rules; CSS/QSS implements only part of the specification.','A named owner and current examples help contributors interpret the rules consistently.']),
      '53B':dict(body=['Give the agent the current style sheet, token source and representative states.','Require existing components and deliberate, documented exceptions.','Compare the same states before and after; inspect behavior as well as appearance.','Update the shared rules when an intentional design decision changes.'],visual='Show a short student-readable instruction from the local style skill beside its corresponding action-state rule. Keep machine-specific paths out of the projected slide. Use the prepared before/after images; no live agent run is needed.'),
      '53C':dict(title='GOLF+ style rules: meaning must stay consistent',body=['Repeated type, icons and stage markers create a recognizable tool family.','Gold emphasizes Generate; muted later controls establish a different visual priority.','Color roles must distinguish emphasis, selection, completion and availability.','Do the warning and control treatments explain what the artist can do next?'],notes='The screenshot shows how shared typography, icon treatment and colors create continuity. Full-width controls fit this narrow sequential workflow; that is why we do not turn one course example into a ban on full-width buttons. But consistency also needs meaning. Muted controls could communicate several things unless the interface explains their state. The October playbook describes an earlier shorter workflow; this screenshot shows six stages with different labels. We should reconcile that difference in the style sheet rather than assume the document and implementation already match. What question would you ask about the warning beside Input?',visual='Reuse the supplied Course Generator image with a focused legend for type, stage markers and action emphasis. Keep the playbook comparison as a small editable table. Do not call muted controls programmatically disabled or filled steps completed without behavioral evidence.',edit='Replace the historical GUI image as the main visual. Preserve older feedback as process history, and explicitly reconcile the shorter playbook workflow with the six visible stages.',rationale='Teaches the style sheet as a maintained specification, including a concrete document-versus-interface discrepancy to investigate.'),
      '43':dict(body=['Paper or Figma: ask someone to explain the flow and predict each action.','Prepared state images: compare starting, reviewed, blocked and completed feedback.','Running tool: verify actual scope, changes, recovery and host behavior.','Use the least expensive prototype that answers the current question.']),
      '58':dict(body=['Record starting inputs, expected behavior, observed behavior and any help needed.','Separate the observation from your explanation of its cause.','Change one relevant feature and repeat a comparable task.','What remains uncertain, and what would you test next?']),
      '62':dict(body=['Give a goal and prepared inputs, not a sequence of clicks.','Define visible success and the object or data that must remain unchanged.','Prepare a reset; if using a storyboard, state which behavior it cannot verify.','Can a peer attempt the task without your narration?']),
    }
    for id,fields in changes.items():by[id].update(fields)
    tables={
      '41':('Outline before designing',['Part','Worked material-tool example'],[
          ['Role / context','Environment artist trying a texture set on a selected crate.'],
          ['Outcome / benefit','Compare a look while leaving other placements unchanged.'],
          ['Assumption to check','Which material slot and objects should the operation affect?']]),
      '41A':('Acceptance checks',['Situation','Observable check'],[
          ['Preview','Target, slot and texture mapping are visible; no scene edit yet.'],
          ['Apply','Only reviewed components change; protected crate stays unchanged.'],
          ['Input changes','Old plan is invalid; review a fresh preview before Apply.']]),
      '42A':('From game art to a tool',['Art principle','Interface decision'],[
          ['Balance','Distribute visual weight between inputs, preview and actions.'],
          ['Rhythm / alignment','Repeat field order and shared edges.'],
          ['Proximity','Keep each label, input and validation message together.']]),
      '45A':('Three distinct meanings',['Term','What it describes'],[
          ['Art value','How light or dark something appears.'],
          ['HSV Value','A coordinate in a particular color model.'],
          ['Relative luminance','The weighted quantity used in contrast calculations.']]),
      '45B':('Choose the check for the question',['Check','Inspect'],[
          ['Blockout','Group size, alignment, gaps and reading route.'],
          ['Grayscale','Light/dark hierarchy without hue.'],
          ['Squint / step back','The large masses that dominate attention.']]),
      '47':('Read the interface as a sequence',['State','Intended response'],[
          ['Choose inputs','Preview is emphasized; Apply is unavailable.'],
          ['Reviewed plan','Apply becomes the forward action.'],
          ['Warning','Review and acknowledge before Apply.'],
          ['Completed','Inspect the result; repeated Apply is unavailable.']]),
      '51':('Test an actual attempt',['Check','What to observe'],[
          ['Keyboard','Focus stays visible and reaches every necessary action.'],
          ['Readability','Labels remain readable at the real display size.'],
          ['State','Warning, selection and completion remain distinguishable without hue.'],
          ['Recovery','The artist can correct the problem and attempt the task again.']]),
      '53C':('Keep the specification current',['Document / capture','Workflow labels'],[
          ['Earlier playbook','Detect → Generate → Finalize → Adopt'],
          ['Supplied screenshot','Input → Parameters → Generate → Edit → Finalize → Integrate'],
          ['Maintenance question','Which labels are authoritative, and which rule changed?']]),
    }
    for id,(label,columns,rows) in tables.items():by[id]['visible_detail']={'type':'table','label':label,'columns':columns,'rows':rows}
    by['49']['visible_detail']={'type':'example','label':'Illustrative recovery message','text':'An asset named MI_Crate_Demo already exists in the destination. Choose a new instance name, then create a fresh preview.','context':'Teaching rewrite; not a claim about the exact current error wording.'}
    by['53A']['visible_detail']={'type':'example','label':'One reusable rule','text':'Forward action: emphasize Preview until a valid plan is reviewed; then emphasize Apply. Keep Reset separate. Use the same rule in each assistant.','context':'Week 7 style-sheet example; GOLF+ has its own palette and host patterns.'}
    by['53B']['visible_detail']={'type':'example','label':'A reusable instruction for the agent','text':'Read the current style sheet before changing the UI. Reuse its tokens and components. Compare matching start, warning and completion states. Report deliberate exceptions.','context':'The instruction supports consistency; the resulting UI still needs review.'}
    root=Path(__file__).resolve().parents[4]
    codepath=root/'Week07UnrealPython/Content/Python/week07_tooling/ui/assistants.py'
    lines=codepath.read_text(encoding='utf-8').splitlines()
    start=next(i for i,line in enumerate(lines) if line.strip().startswith('def update_apply('))
    excerpt='\n'.join(line[8:] for line in lines[start+1:start+4])
    by['48']['visible_detail']={'type':'code','label':'Inside AssistantWindow.update_apply','text':excerpt,'context':'Excerpt: the existing window, widgets and session are already constructed. Acknowledgment affects readiness; execution validates again.','source':str(codepath),'line':start+2,'source_sha256':hashlib.sha256(codepath.read_bytes()).hexdigest()}
    dividers={'39','42','46B','53','56'}
    for p in slides:
        p['delivery']='section transition' if p['id'] in dividers else 'prepared explanation and visual; no live execution required to teach the point'
        p['live_demo']='optional reinforcement after manual validation; preserve scheduled colleague demonstrations'
        if p['id'] not in dividers:
            p['edit']+=' Keep the definition, worked example or comparison visible in the slide; use notes for elaboration. Preserve legible type and split an overloaded composition instead of shrinking it.'
    by['45B']['visual']='Use the prepared diagnostic views of the same material screenshot. The blockout is a labeled schematic of that layout. Keep the original source image available and explain that these are hierarchy checks, not functional tests.'
