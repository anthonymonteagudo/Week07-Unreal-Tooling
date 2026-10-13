# Stage 00 · Data and scope

Run `Scripts/lessons.py run 01`, then `run 02` using the project interpreter.

| Step | Open | Expect | Try |
| --- | --- | --- | --- |
| 01 | `step_01_read_records.py` | Four records; first path `sample://crate-0`, label `crate_old`. | Inspect `first` at a breakpoint. Which field remains useful after renaming? |
| 02 | `step_02_choose_scope.py` | Three included labels; `KeyLight` excluded. | Remove a tag from your local data copy and see which list changes. |

These dictionaries stand in for data a future adapter can collect. They are not
Actor objects. This checkpoint filters exclusions; the existing Unreal Apply path
rejects mixed selections, a stricter policy discussed in Stage 03.
