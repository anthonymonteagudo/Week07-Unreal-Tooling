# Lab starter: scope pending

This optional starter is separate from the worked checkpoints, following the
starter/example distinction in the SimonDev reference. It is not a finalized lab
or graded assignment.

Open `starter_missing_mesh_report.py`. Implement `missing_mesh_paths(records)` so it
returns only tagged demo props whose `has_mesh` flag is false. Use a breakpoint or
ordinary Python to inspect the return value. This file is self-contained and may
be run directly. The expected output is `['sample://barrel-1']`.

Stretch discussion: return structured findings instead of strings; explain why the
tool should report a missing mesh rather than guess which asset to assign. Keep
automatic mesh assignment, editor UI and importing outside this draft exercise.
