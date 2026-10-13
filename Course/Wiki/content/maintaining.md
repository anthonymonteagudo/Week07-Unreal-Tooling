---
updated: 2026-09-08
title: Maintaining the course wiki
group: Course
order: 3
status: Author guide
summary: Add a week without duplicating explanations, losing evidence, or mixing a proposal with a confirmed course requirement.
---

## Add a week

1. Copy the week template from the `templates` folder into `content`.
2. Set the title, group, order, status, summary, and updated date in the short metadata block.
3. State the connection to earlier work and the action students should be able to perform.
4. Link existing topic pages; add a new topic only when the mechanism needs its own explanation.
5. Add an example, inspection question, relevant evidence, and a focused source.
6. Build the wiki and check the new page's links.

Keep published HTML beside the Markdown source so the wiki can be read directly from the workspace. There is no server requirement for reading or searching the built pages.

## A reusable teaching structure

Begin with a visible problem or intended result. Explain the minimum mechanism needed to reason about it. Show where that mechanism can be inspected in Maya or Unreal, then ask a prediction or diagnosis question.

Use the lab to motivate the explanation. Leave a breadcrumb back to the relevant topic page, while keeping the full instructor repair key in the course's instructor materials.

Put advanced mathematics and implementation under a focused further-reading question. A later week can deepen an existing topic page rather than replacing its beginner explanation.

## Evidence and sources

Distinguish a real course capture, a publisher's example, and a proposed recording. Preserve creator credit, the source page, and useful version context. A conceptual citation does not prove that a separate image depicts the same technique or that a local repair succeeded.

Record enough context for a setting to remain meaningful after the software changes: what it controls, the importer or workflow, and the result being verified.

## Revision habits

Use the changelog to record the substantive change and reason. Preserve stable page filenames and current slide-number anchors. When a title changes, update navigation and references while retaining a clear path from the previous review.

Keep current content, proposed changes, visual design, teaching rationale, and read-aloud notes distinct in the [slide reviews](../Slides/index.html). The review is an iterative proposal until the deck is actually edited.

## Course policy and readiness

Label future weeks as planned until their teaching material is developed. Use the current Canvas brief for assignment scope, deadlines, grading, and submission. The instructor's current exhibit direction takes precedence over the older Week 2 assignment name in the syllabus snapshot.

Museum station availability comes from a rehearsed teaching build and prepared station list. A source-ready or display-only label does not establish a supported student repair task.

## Build and source control

The repository [README](README.md) documents build commands, source locations, and the dependency version. Add the Markdown, generated HTML, and referenced local assets together in Perforce so a checked-out copy remains usable. Keep caches, `node_modules`, and editor lock files out of the changelist.
