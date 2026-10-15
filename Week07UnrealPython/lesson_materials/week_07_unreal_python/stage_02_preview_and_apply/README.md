# Stage 02 · Preview and apply

Run `Scripts/lessons.py run 05`, then `run 06` using the project interpreter.

| Step | Open | Expect | Try |
| --- | --- | --- | --- |
| 05 | `step_05_change_plan.py` | Two before/after records; original labels still unchanged. | Compare a finding to a proposed change. What extra information is needed? |
| 06 | `step_06_apply_to_copy.py` | Corrected labels in a copy; original unchanged; no remaining renames; barrel still missing its mesh. | At a breakpoint after preview, change `actors[0]['label']`. Apply should reject the stale plan. |

Repeated runs start from the same sample. Inside Step 06, a fresh plan made from the
corrected copy is empty; the second pass needs no renames. Applying the old plan
again is a stale-plan error. Neither behavior writes to disk or touches Unreal.

The copy makes this experiment disposable. It does not teach or provide engine
Undo, world identity checks, collision detection or protection against every kind
of changed record. Those responsibilities belong to the existing adapter.
