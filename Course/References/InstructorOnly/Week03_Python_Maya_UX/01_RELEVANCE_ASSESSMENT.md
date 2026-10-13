# First-pass relevance assessment

Assessment target: the current Week 3 route

```text
Python -> PySide -> files/paths/JSON -> Maya API
       -> Lab 1 Source Art -> Lab 2 texel density
```

## Ranking

| Source | Current relevance | Best use | Main caution | Decision |
|---|---:|---|---|---|
| The Technical Artist's Guide to Python in Maya, Zeynep Fisher | Primary | Artist-centered framing, Maya layers, Script Editor, current Python basics | v0.0.2 stops at variables; a few diagrams simplify architecture | Reference thoroughly and directly |
| Introduction to Python Scripting for Maya Artists, Chad Vernon | Very high | Course sequencing, modules/packages, files, clean code, `maya.cmds`, `mayapy` | Written around Maya 2016 and Python 2 | Mine deeply now |
| The Design of Everyday Things, Don Norman | Very high | Feedback, signifiers, constraints, Undo, error prevention, systems thinking | General product design rather than DCC tooling | Mine deeply now |
| Don't Make Me Think, Steve Krug | High | Scanability, hierarchy, clear actions, low-cost usability testing | Web examples require translation to Maya tools | Mine deeply now |
| Practical Maya Programming with Python, Robert Galanakis, preview | High for instructor; medium for beginners | Composable architecture, GUI/logic separation, errors, reload cautions, host boundaries | Maya 2013, Python 2, PyMEL, and only a preview | Mine architecture, not code |
| Automate the Boring Stuff with Python, Al Sweigart | Medium-high | Beginner file/path mental model, preview-before-change, safe moves, ZIP recovery | Older `os.path`/`shutil` style; course uses `pathlib` | Mine selected chapters |
| Real Time Visual Effects for the Technical Artist, Chris Roda | Medium-low for Week 3 | TA identity, iteration, art-before-technology, later systems context | Excerpt focuses on VFX rather than Python tooling | Retain for later weeks |
| Modeling and Python Scripting in Maya for the Animation Short Style | Low | Small motivational case study about scripting repetitive Maya work | Narrow student project, dated code, limited pipeline/UI depth | Archive; do not build Week 3 from it |
| Anthony's HarvardX CS50P notes, Week 0 | Medium-high | Accessible vocabulary for functions, inputs, variables, return values, errors, and comments | Personal notes are abbreviated and contain one malformed example | Distill into Slides 3-4 and the Step 1 walkthrough |
| Simon's batch-file notes and examples | Medium for instructor; low for students | Explain repeatable launch commands and the path toward studio launchers | Hard-coded paths, destructive `taskkill`, external dependencies, and shell-specific detail | Keep as optional deployment context |

## What should influence Week 3 now

1. Frame coding as an extension of artists' visual reasoning, pattern recognition,
   decomposition, iteration, and reference comparison.
2. State that students should understand logic rather than memorize commands.
3. Reinforce the reason for automation: reduce repetitive work and human error while
   increasing useful artistic iteration.
4. Make host boundaries explicit: normal Python, `mayapy`, and interactive Maya are
   related but not interchangeable.
5. Distinguish Maya Commands (`maya.cmds`) from the Python API
   (`maya.api.OpenMaya`) instead of using “Maya API” as a generic label.
6. Teach modules and packages as the reason the course does not run one giant file.
7. Treat JSON as policy and Python as behavior.
8. Use preview, validation, constraints, feedback, and Undo as first-class tool
   requirements rather than polish added at the end.
9. Make every tool screen scannable: one goal, obvious primary action, visible state,
   and feedback adjacent to the action.
10. Test the tools by watching a beginner attempt the task, not only by proving that
   the code executes.
11. Use `input -> function -> return -> output` as the first Python data-flow model,
    while distinguishing a returned value from a printed side effect.
12. Treat batch files as one possible launcher layer, not as a connection to an
    already-open Maya process and not as a required Week 3 technology.

## What should not change yet

- Do not introduce Python 2 syntax or teach directly from old code listings.
- Do not replace `pathlib` with `os.path` in the current demonstrations.
- Do not introduce PyMEL, sockets, request-reply automation, external Maya control,
  or Maya plugin APIs in Week 3.
- Do not turn UI/UX into a long theory detour before students have used the tools.
- Do not add VFX implementation material to the current Python/Maya lesson.

## Course-placement recommendation

- Slides: use the strongest principles as short framing statements and before/after
  UI examples.
- Live code: retain the existing beginner sequence and use the Maya primer to support
  explanations of imports, packages, `maya.cmds`, and `mayapy`.
- Lab 1: foreground preview-before-change, no overwrite, validation, and visible
  feedback.
- Lab 2: foreground reference policy, constrained selection, one undoable change,
  verification, and a safe export boundary.
- Later UI lab: apply Krug and Norman explicitly after students have experienced the
  first version of the tools.
