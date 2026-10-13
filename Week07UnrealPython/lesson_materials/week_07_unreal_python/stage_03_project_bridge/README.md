# Stage 03 · Connect the example to the project

Run `Scripts/lessons.py run 07` using the project interpreter. Open
`step_07_reusable_rules.py` alongside `Content/Python/week07_tooling/rules.py`.
The latter path is relative to the project root.

Expect six findings before the copy update: two label issues, three placement
issues, and one missing mesh. Afterwards, only the barrel's missing mesh remains.
The returned production plan contains all three props. Location units are centimeters.

Then read [Step 08 · Editor boundary](step_08_editor_boundary.md). It is deliberately
not executable through the offline runner. No Unreal rehearsal is required to work
on these files.
