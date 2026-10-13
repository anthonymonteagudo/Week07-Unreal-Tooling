# Deep dive: material worth mining for Week 3

Page numbers below are PDF page numbers, not necessarily printed book page numbers.
The notes paraphrase the sources and translate them to the current Maya 2027 course.

## New primary source

Zeynep Fisher's 2026 *The Technical Artist's Guide to Python in Maya* is now the
primary framing source. Its full page-to-slide and walkthrough application lives in
`Maya-Tools/course_docs/week_03/instructor/PRIMARY_BOOK_INTEGRATION.md` so those
notes remain source controlled with the course. The material below provides older
Maya, broader Python, UX, safety, and systems-thinking support around it.

## 1. Introduction to Python Scripting for Maya Artists

### High-value page route

- PDF 4-5: why Python matters to artists and what an interpreter/script is;
- PDF 9-11: running/importing scripts in Maya, search paths, and reloading;
- PDF 31-34: modules, packages, JSON, files, and directory traversal;
- PDF 41-48: PEP 8, DRY, meaningful names, side effects, small functions, early
  returns, and readable validation;
- PDF 53-57: `maya.cmds`, documentation, return values, long flag names, and
  create/query/edit modes;
- PDF 57-60: function-based Maya examples and naming automation;
- PDF 61-62: interactive Maya versus standalone `mayapy`.

### What to adopt

The source's opening rationale fits this course particularly well: technical artists
automate repetitive tasks, reduce human error, and give artists more iterations in
the feedback loop. That is a better Week 3 thesis than “learn Python syntax.” Syntax
is introduced because it enables that outcome.

The package discussion supports the current course architecture. A visible folder
tree can explain that packages group related modules and that imports expose a
stable entry point. The warning against complex work at import time supports the
current pattern:

```python
import week3_tools
week3_tools.show_source_art_lab()
```

The clean-code section maps almost one-to-one to the labs:

- use verbs for actions such as `validate`, `fix`, `measure`, and `export`;
- use question-like Boolean names such as `is_valid` or `needs_fix`;
- do not let `validate` secretly move files;
- extract nested validation into named functions with early returns;
- keep UI callbacks short and delegate work to testable functions.

The Maya command-documentation walkthrough supplies a strong live teaching method:
perform a simple action in Maya, observe Script Editor output, locate the Python
command documentation, use readable long argument names, and inspect the return
value. Create/query/edit is a useful conceptual trio before Lab 2's
measure/change/verify sequence.

The distinction between Maya and `mayapy` directly supports the current setup:

- VS Code plus `mayapy`: Python, PySide, files, tests, and batch-capable code;
- open Maya: interactive UI, scene state, selection, and Undo.

### What to modernize or omit

- Translate all Python 2 `print` statements and old exception syntax to Python 3.
- Use `importlib` or the course refresh helper instead of teaching bare `reload()`.
- Prefer Maya modules and the existing installer over editing `Maya.env` or global
  `PYTHONPATH` during class.
- Prefer `pathlib` over the source's `os.path` examples.
- Do not teach editing `.ma` files by raw string replacement.
- Keep OOP brief: students need to recognize the PySide window class, not master
  inheritance this week.

### Recommended lecture insertion

Add three concise slide ideas:

1. **Why Python for artists?** Repetition -> error risk -> automation -> more
   creative iteration.
2. **A script becomes a tool through boundaries.** Package, public function, UI,
   host adapter.
3. **Where is Python running?** Normal Python / `mayapy` / Maya GUI comparison.

## 2. Practical Maya Programming with Python preview

### High-value page route

- PDF 9-13: table of contents for composability, errors, context managers, GUI
  architecture, Maya integration, shelves, and external automation;
- PDF 17-18: the book's skills-over-recipes framing;
- PDF 25-30: `mayapy`, development roots, import paths, reload caveats, and Maya
  introspection.

### What to adopt

This source is most valuable as an instructor architecture check. Its chapter order
supports four principles already present in the course:

1. reusable/composable code before a large tool;
2. deliberate error handling rather than silent failure;
3. UI separated from application logic;
4. Maya treated as one host/adapter, not the location of every responsibility.

Its warning about reload is particularly useful: refresh accelerates development,
but a tool still needs a clean-session test before being considered finished. Keep
the current refresh helper for instructor iteration, then test the final lab in a
fresh Maya session.

The GUI chapter headings support the current split among application, UI, and Maya
layers. The later request-reply and external automation chapters are useful studio
awareness, but they validate leaving external Maya control out of this beginner
lesson.

### What to modernize or omit

- The examples target Maya 2013, Python 2, and PyMEL.
- Do not reproduce the source's install paths or environment-variable setup.
- Do not introduce PyMEL alongside `maya.cmds` in the same beginner class.
- Do not add ZeroMQ, sockets, `exec`, remote evaluation, or plugin-node material.
- Because this is only a preview, use its architecture headings as prompts, not as a
  complete implementation reference.

### Recommended instructor use

Use the chapter list as a checklist when reviewing Lab 2:

```text
Can the math run without Maya?
Can the Maya adapter run without the UI?
Does the UI state the action and result?
Are failures actionable?
Can one change be undone?
Does it work after a fresh Maya restart?
```

## 3. Automate the Boring Stuff with Python

### High-value page route

- PDF 198-205: folder hierarchy, relative versus absolute paths, joining paths,
  existence checks, and file reading;
- PDF 222-229: copying, moving, renaming, recursive traversal, and ZIP files;
- PDF 234-237: incremental backup, avoiding self-inclusion, previewing dangerous
  operations, and recovery.

### What to adopt

The strongest contribution is not syntax; it is the safety mindset around file
automation. The source repeatedly demonstrates that moving or deleting files can do
something other than what the programmer intended, and recommends printing or
previewing targets before performing destructive operations.

That maps directly to Lab 1:

```text
discover -> validate -> preview planned moves -> confirm -> change -> validate again
```

It also supports the lab ZIP as a recovery artifact without mentioning ZIP mechanics
inside the student-facing tool. A recovery copy belongs to deployment; the tool's
normal UI should focus on the actual Source Art state.

### What to modernize or omit

- Teach `Path` objects rather than strings plus `os.path.join`.
- Use `Path.exists`, `is_file`, `is_dir`, `iterdir`, and `rglob` where appropriate.
- Use context managers for file access.
- Never demonstrate recursive deletion in this beginner lab.
- The current validator should remain constrained to declared assets instead of
  walking and mutating an arbitrary tree.

### Recommended live comparison

Show one unsafe-looking operation and then the course pattern:

```python
# Too much trust: mutation is the first visible action.
shutil.move(source, destination)

# Course pattern: resolve, validate, display the plan, confirm, then move.
planned_change = {"source": source, "destination": destination}
```

Do not actually perform the unsafe version. The comparison exists to motivate the
validator's staged design.

## 4. Don't Make Me Think

### High-value page route

- PDF 37-41: self-evident versus self-explanatory interfaces and user scanning;
- PDF 58-65: visual hierarchy, defined regions, obvious controls, noise reduction,
  and scannable text;
- PDF 183-189: prioritizing the essential and preserving obvious routes;
- PDF 218-226: fix broad confusion first and observe real users attempting tasks.

### Translation from web pages to Maya tools

Artists open a utility to complete a task, not to study its interface. Assume they
scan for the action matching their immediate goal. A Maya dialog should therefore
answer these questions almost immediately:

1. What is this tool for?
2. What should I select or choose?
3. What is the primary next action?
4. What changed or why can I not continue?
5. How do I recover?

This argues for the current staged Lab 1 flow and against a toolbar full of vaguely
related choices. Button labels should describe the result, not an implementation:
**Validate**, **Fix Naming + Structure**, **Import Organized Assets**.

Visual hierarchy should follow task hierarchy. Primary action, status, and result
belong together. Documentation and optional material should not compete visually
with the action. This directly validates splitting the Python and Maya Learning Hubs
instead of presenting one large link matrix.

### Low-cost usability test for the later UI lab

Observe three beginners individually. Do not explain the interface first. Ask each
student to:

1. state what they believe the tool does;
2. identify the first action;
3. validate the supplied problem;
4. explain the feedback;
5. predict what Fix will change;
6. recover from one intentionally missing prerequisite.

Record hesitation, wrong clicks, questions, and misunderstood labels. Revise the
largest repeated problem, then test again. The goal is not preference polling; it is
evidence of whether users can complete the intended task.

## 5. The Design of Everyday Things

### High-value page route

- PDF 28-33: affordances, signifiers, mappings, feedback, and system image;
- PDF 84-92: execution/evaluation gap and feedback that helps users understand
  state;
- PDF 142-165: constraints, interlocks, lock-ins, lockouts, and conventions;
- PDF 189-214: slips, mistakes, checklists, error reporting, prevention, and
  detection.

### What to adopt

Norman supplies the systems-thinking bridge for Week 3. A student does not interact
only with a button. They form an understanding from the tool's visible interface,
its feedback, the folder they can inspect, the Maya scene result, and the recovery
path. Together these form the system image.

Translate the key concepts this way:

| Design concept | Week 3 implementation |
|---|---|
| Signifier | A concrete label such as **Open SourceArt** or **Validate** |
| Mapping | Buttons appear in the same order as the workflow |
| Feedback | Validation log names the issue and planned result |
| Constraint | Import stays unavailable until organization validates |
| Interlock | Export refuses invalid selection, path, or overwrite |
| Reversibility | Maya change is one Undo; supplied files have a recovery copy |
| Error detection | Re-measure and validate after changing state |
| Knowledge in the world | JSON rules, visible paths, status, and walkthroughs |

The most important error principle is to avoid blaming the artist. “User error” is
often evidence that a system allowed a plausible mistake and failed to expose enough
state. An actionable message should name what is missing, where the tool looked, and
what the user can do next.

Constraints should protect the task without becoming so annoying that users bypass
them. For example, disabling Import until validation succeeds is proportional.
Forcing a dozen modal confirmations for harmless checks would not be.

### Systems-thinking mini-lesson

Use one five-minute loop after students operate Lab 1:

```text
artist goal
  -> visible UI choice
  -> Python decision
  -> JSON policy
  -> filesystem change
  -> Maya import
  -> visible verification
  -> artist trust and next action
```

Ask: “If the final result is wrong, at which boundary could the system have failed?”
This introduces inputs, policy, transformation, feedback, and recovery without a
separate abstract systems-theory lecture.

## 6. Lower-priority sources

### Real Time Visual Effects for the Technical Artist

The supplied excerpt is most useful for later framing: real-time work serves an
experience, effects should remain art-directable, iteration matters, and technology
should support the art rather than become the point. For Week 3, mine only a short
statement connecting automation to iteration. Save its VFX rules and real-time
examples for later rendering/effects weeks.

### Modeling and Python Scripting in Maya for the Animation Short Style

This is a small project report rather than a pipeline or teaching reference. It can
support the general claim that scripting removes repeated work and enables procedural
experimentation, but its examples and scope should not guide the current code,
architecture, UI, or lab sequence.

## Recommended next application pass

When revising slides and demos, apply these changes in this order:

1. add the automation/iteration thesis near the opening;
2. add the three-host diagram before setup;
3. add modules/packages and public entry points before Maya;
4. annotate Lab 1 with preview, constraint, feedback, and validation;
5. annotate Lab 2 with reference policy, Undo, verification, and error detection;
6. reserve the explicit Krug/Norman UI critique for the later UI cleanup exercise;
7. run the three-person usability observation before finalizing the tool UI.
