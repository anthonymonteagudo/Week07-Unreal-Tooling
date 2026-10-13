---
updated: 2026-09-13
title: Week 3 · Python, Maya automation, and artist-facing UI
group: Weeks
order: 13
status: Preview
summary: Read a small Python operation, automate a scoped texel-density repair in Maya, and make its state, scope, and evidence understandable to an artist.
---

## The through-line

Week 2 established a manual **Get → Set → verify** texel-density repair. This week
turns that understood operation into a small tool:

1. inspect a reference and selected targets;
2. measure world-space and UV area;
3. calculate the required UV scale;
4. change only the intended UV shells;
5. measure again and report the result.

Python repeats controlled steps. It does not choose the artistic reference, decide
whether the final texture treatment is convincing, or make missing evidence true.

## What you should be able to do

By the end of class, you should be able to:

- read a short loop, condition, function call, and returned value;
- explain the difference between VS Code, a Python interpreter, `maya.cmds`, and
  PySide;
- identify the reference, targets, units, and protected scope of an operation;
- distinguish **Check** from **Apply** and successful execution from verified output;
- trace a button click through a callback into shared Maya code;
- name one artist decision that should remain outside the automation.

## Before changing a scene

State the tool contract in plain language:

- **Input:** one captured reference, one or more selected target meshes, map size,
  active UV set, and current Maya linear unit.
- **Action:** uniformly scale each existing UV shell around its own center.
- **Protected scope:** the reference and unselected meshes are not edited.
- **Evidence:** report before and after density and verify the result within tolerance.
- **Recovery:** one Apply to multiple targets is one Maya undo step.

The classroom tool does not remap, pack, cut, sew, define a UDIM policy, or change
material tiling.

## The systems-thinking layer

Treat the tool as a small system, not an isolated button:

- **Boundary:** pure Python calculates; Maya supplies and changes scene data; PySide
  communicates with the artist; the filesystem supplies code and presets.
- **State and context:** selection order, active UV set, scene unit, map size, project
  path, and Maya/Python/PySide version all affect behavior.
- **Feedback loop:** inspect → decide → change → measure again. Running Apply twice
  tests whether the system stabilizes instead of drifting.

The highest-leverage choices occur at boundaries: validate before mutation, expose
context instead of assuming it, protect scope, make the action undoable, and verify
the output. If the UI says “Done” while an invalid target was skipped, the software
ran but the system failed to communicate truthfully.

## Interactive start

Use [futurecoder](https://futurecoder.io/) for beginner Python practice and immediate
feedback. In class, the route is deliberately short: predict, run, read the feedback,
and explain one change. Students who need support can use hints or a Parsons-style
reordering problem; students who finish early should construct a counterexample to a
wrong condition.

The local [Week 3 interactive bridge](../Slides/Week03/Interactive/index.html) uses
the actual workshop data and remains available when the hosted course is not. It
connects code prediction to loop tracing, counterexamples, and UI critique.

The first checkpoint asks you to predict this result before running it:

```python
def needs_attention(name, density, minimum=9.75, maximum=10.75):
    density_is_wrong = not minimum <= density <= maximum
    name_is_wrong = not name.startswith("TD_")
    return density_is_wrong or name_is_wrong

assets = [
    ("TD_reference_cube", 10.24),
    ("TD_target_large_cube", 4.10),
    ("prop_round_mesh", 6.80),
]

print([name for name, density in assets if needs_attention(name, density)])
```

Change only one part of the condition, then construct the smallest example that shows
why the changed rule is wrong.

## Maya checkpoint sequence

The workshop is staged rather than live-typed as one large script:

1. Discover the project root and report the actual software environment.
2. Read and predict an ordinary Python loop.
3. Ask Maya for selection and polygon evidence.
4. Measure density without changing the scene.
5. Apply the reference density, verify, run twice, and undo.
6. Operate a deliberately unclear but safe UI.
7. Improve one artist-facing behavior and rerun the same test.

The supplied adapter contains the mesh API details. Introductory work stays focused on
the readable orchestration: inputs, condition, function call, result, and feedback.

## UI/UX is part of correctness

An artist should not have to guess:

- what “Value” means or what units it uses;
- which objects a button will affect;
- whether the action only checked or actually changed the scene;
- which objects changed, failed, or were skipped;
- whether the result was measured after the change;
- how to recover from an unwanted action.

The completed interface therefore names the reference and target scope, distinguishes
Check from Apply, prevents Apply until a reference is captured, reports each verified
result or skip, and names Undo as the recovery route.

## Pair lab

One person operates while the other observes silently. Before editing code, write one
expected behavior. Improve one label, validation response, callback, or report; then
run the same fixture test, Apply twice, confirm the protected control is unchanged,
and switch roles.

There is no Week 3 submission. Further practice is optional and can become evidence
for choosing a useful midterm tool idea.
