"""04: An edit has explicit scope and an Undo boundary."""
from week07_tooling.editor import demo


def run(plan):
    # w7.run_example('04_apply_reviewed_plan', plan=plan)
    changed = demo.apply(plan)
    demo.check()
    return changed
