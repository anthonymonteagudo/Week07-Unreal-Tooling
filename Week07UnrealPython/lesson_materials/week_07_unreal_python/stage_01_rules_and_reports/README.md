# Stage 01 · Rules and reports

Run `Scripts/lessons.py run 03`, then `run 04` using the project interpreter.

| Step | Open | Expect | Try |
| --- | --- | --- | --- |
| 03 | `step_03_naming_rule.py` | Expected names `W07_Crate_01`, `W07_Barrel_02`, `W07_Crate_03`. | Step into the function; explain `+ 1` and `:02d`. |
| 04 | `step_04_validation_report.py` | Three findings: two `LABEL`, one `MISSING_MESH`. | Which findings can a rename operation actually fix? |

The third prop already has the right name. A report counts issues, not necessarily
unique objects: the barrel has two problems. Neither step changes the input.
