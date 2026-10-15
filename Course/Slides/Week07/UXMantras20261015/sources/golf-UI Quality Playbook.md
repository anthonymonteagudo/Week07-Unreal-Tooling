# UI Quality Playbook (editor tools)

2026-10-08. Distilled from the in-project rules (Spline Suite `ui-style-guide.md`, Course Tools `DESIGN.md`, Spline Suite `ui-intent.md` / `ui-design-pipeline.md`), Ben's feedback, and outside guidelines that suit dense pro tools. First applied to the Course Generator (PR #1160).

## Ben's brief, as rules

1. The 80-90% path is a few clear buttons, in order, with icons and numbers. Course Generator: **Detect from Scene → Generate → Finalize → Adopt**.
2. Everything else sits behind one labelled fold per step (the gear), never a second level.
3. One visual wrapper shared by every GOLF+ tool, in step with the installer and Mesh Studio.

## Text

- Labels are short nouns (`Splines`, not `Spline Root (Curvy)`). Qualifiers ("0 = off", units of meaning) go in the tooltip. [JetBrains, Spline Suite guide]
- Buttons are a verb + object, 3 words or fewer. "…" only when more input follows. [Unity Foundations, GNOME]
- Cut the implied verbs ("Use", "Enable", "Specify") and the words a header already says. [JetBrains, Blender]
- No prose on screen. One-line state notices; the detail is in the tooltip. A disabled control's tooltip says why. [Unity Foundations]
- Errors name the value and the fix, never "Invalid" or "Failed". [JetBrains, Polaris, Atlassian]
- One glossary across tools: Workable, Finalize, Adopt, Section heights, Exclusions. Never two names for one thing. [Apple HIG]

## Layout

- One row height (22 px), 2 px between rows, 8 px between groups. Space before containers. [Unity Foundations, 8-pt grid]
- Main buttons full width and tall (32 px); never put a high-traffic control in a fold. [Unity Foundations, memory: workflow prominence]
- Group with a gold title and hairline, not grey panels. Headers only for groups of 3+ controls. [Spline Suite guide, JetBrains]
- Most-used at the top, rarely used at the bottom or folded. [Blender]
- Shared margins, no control touching the window edge, no horizontal scroll at minimum width. [Unity Foundations]

## Colour

- 95% neutral ground; colour is meaning. Gold = the next step / commit. Green = done. Clay = destructive. Amber dot = attention. [Course Tools DESIGN.md, Material dark]
- One primary (gold) button per section at most. [Polaris, JetBrains]
- Never colour alone: pair with an icon or text. Text 4.5:1, icons and borders 3:1. [WCAG]
- Every colour from one token file (`SplineSuiteStyle`); no hex in tool code.

## Sequencing

- Number steps only when the order is real; show done / next / waiting on each. Name the next action ("NEXT · FINALIZE"), not "Next". [NN/g wizards]
- Disable rather than hide a step's button until it can run. [Unity Foundations]
- Sensible defaults, remembered per course; presets for the rest. [NN/g defaults]
- Inline validation at the right moment, never a modal for it. [JetBrains]

## Icons

- One set (Tabler via `CourseToolsIcons`), one meaning per icon across tools. Pick with the Glyph Browser. [Course Tools DESIGN.md]
- Main buttons pair icon + label. Icon-only for toolbars, and their tooltip leads with the name. [NN/g icon usability, JetBrains]
- 14-16 px, monochrome; colour only when it means something. [JetBrains, Unity Foundations]

## How to push it further (ranked)

1. **One shared GOLF+ editor kit.** Promote `CourseGenStyle` + the step framework (`CourseGenSteps`) into Course Tools Suite (a `GPEditorUI` class) and move Road Builder, Spline Suite panels and Mesh Studio onto it. Consistency across tools is the biggest jump in perceived quality, and it's Ben's ask.
2. **Settle the brand tokens once.** The editor palette is Spline Suite's dark green + gold; the installer is dark slate + bright green + gold; the game's design system is slate + teal/blue. Pick one ground and one accent for all tools and put them in the token file. Brand type is decided: TeeLine Extra Bold Italic for titles (`Assets/Resource Data/Fonts`).
3. **Watch Ben use it.** Time to first bake, click count, and every place he hesitates. Fix the top three, repeat. Tools get simpler fastest this way.
4. **Non-default markers + reset.** A gold dot on any value changed from the preset, and "reset section". This is how Unreal and Unity make dense panels safe.
5. **Screenshot review per PR.** The window can be captured without focus (GUIView.GrabPixels through the bridge). Before/after shots catch spacing and colour drift a diff never shows.
6. **A word budget.** Each step: a 1-word state, 1-3 word buttons, notices of one line. Read every string aloud once per PR.
7. **Empty states that teach.** "Select a generated piece to edit it" beats a disabled button.
8. **UI Toolkit later.** For cards, transitions and hover art like Mesh Studio's, port the shell to UI Toolkit with IMGUI bodies inside (the middle path in the TODO list).

## Sources

- JetBrains IntelliJ UI guidelines: https://plugins.jetbrains.com/docs/intellij/ui-guidelines-welcome.html (Markdown in JetBrains/intellij-sdk-docs)
- Unity Editor Foundations: https://www.foundations.unity.com
- Blender HIG: https://developer.blender.org/docs/features/interface/human_interface_guidelines/
- GNOME writing style: https://developer.gnome.org/hig/guidelines/writing-style.html
- Microsoft style tips: https://learn.microsoft.com/en-us/style-guide/top-10-tips-style-voice
- Apple HIG writing (JSON): https://developer.apple.com/tutorials/data/design/human-interface-guidelines/writing.json
- Atlassian content standards: https://atlassian.design/llms-content.txt
- NN/g: progressive disclosure, wizards, icon usability, defaults (nngroup.com/articles/...)
- Laws of UX: https://lawsofux.com/hicks-law/index.md (each law as Markdown)
- Radix colour scales: https://www.radix-ui.com/colors/docs/palette-composition/understanding-the-scale
- WCAG contrast: https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
- In project: `Spline Tool Suite/Docs/ui-style-guide.md`, `Course Tools Suite/DESIGN.md`, `Spline Tool Suite/Docs/ui-intent.md`, `C:\Users\antho\Downloads\design.md` (the game's design system)
