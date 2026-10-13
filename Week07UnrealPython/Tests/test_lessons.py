"""Offline teaching contracts: expected observations, no input edits, safe dispatch."""
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "Scripts"))
import lessons


class LessonTests(unittest.TestCase):
    def test_manifest_has_unique_ids_and_existing_files(self):
        steps = lessons.sequence()
        self.assertEqual(len(steps), len({s["id"] for s in steps}))
        for step in steps:
            self.assertTrue(lessons.step_path(step).is_file())

    def test_all_offline_steps_run_from_an_unrelated_directory_without_unreal(self):
        # Blocking the import catches accidental use of real or stub Unreal APIs.
        code = (
            "import importlib.abc, json, sys; "
            f"sys.path.insert(0, {str(ROOT / 'Scripts')!r}); "
            "exec('class NoUnreal(importlib.abc.MetaPathFinder):\\n"
            " def find_spec(self, fullname, path=None, target=None):\\n"
            "  if fullname.split(\".\")[0] == \"unreal\": raise RuntimeError(\"Unreal import attempted\")'); "
            "sys.meta_path.insert(0, NoUnreal()); import lessons; "
            "print(json.dumps(lessons.run_step(sys.argv[1])))"
        )
        with tempfile.TemporaryDirectory() as directory:
            for step in lessons.sequence():
                if step["runtime"] != "python":
                    continue
                with self.subTest(step=step["id"]):
                    result = subprocess.run([sys.executable, "-c", code, step["id"]],
                                            cwd=directory, capture_output=True, text=True)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertIsNotNone(json.loads(result.stdout))

    def test_dispatch_rejects_reading_unknown_and_escaping_paths(self):
        for step_id in ("08", "99", "../../Scripts/editor/smoke_test.py"):
            with self.subTest(step=step_id), self.assertRaises(ValueError):
                lessons.run_step(step_id)
        with self.assertRaises(ValueError):
            lessons.step_path({"file": "../../Scripts/dev.py"})

    def test_scope_and_report_observations(self):
        self.assertEqual(lessons.run_step("01")["record_count"], 4)
        scope = lessons.run_step("02")
        self.assertEqual(len(scope["included"]), 3)
        self.assertEqual(scope["excluded"], ["KeyLight"])
        report = lessons.run_step("04")
        self.assertEqual(report["checked"], 3)
        self.assertCountEqual([f["issue"] for f in report["findings"]],
                              ["LABEL", "LABEL", "MISSING_MESH"])

    def test_preview_and_validation_leave_inputs_unchanged(self):
        for step_id, function in (("04", "validate"), ("05", "make_plan")):
            module = lessons.load_step(step_id)
            actors = [a for a in module["load_records"]() if "W07_DemoProp" in a["tags"]]
            original = deepcopy(actors)
            result = module[function](actors)
            self.assertTrue(result)
            self.assertEqual(actors, original)

    def test_copy_apply_rejects_stale_or_edited_plan_and_preserves_input(self):
        module = lessons.load_step("06")
        actors = [a for a in module["load_records"]() if "W07_DemoProp" in a["tags"]]
        original = deepcopy(actors)
        plan = module["make_plan"](actors)
        self.assertEqual(len(plan), 2)
        updated = module["apply_to_copy"](actors, plan)
        self.assertEqual(actors, original)
        self.assertEqual(module["make_plan"](updated), [])
        updated[0]["tags"].append("changed")
        self.assertEqual(actors, original, "Nested data must also be copied.")
        with self.assertRaises(ValueError):
            module["apply_to_copy"](updated, plan)
        tampered = deepcopy(plan)
        tampered[0]["after"] = "unreviewed_name"
        with self.assertRaises(ValueError):
            module["apply_to_copy"](actors, tampered)
        self.assertEqual(actors, original)

    def test_corrected_copy_still_reports_missing_mesh(self):
        result = lessons.run_step("06")
        self.assertEqual(result["remaining_label_changes"], [])
        self.assertEqual(result["missing_meshes_still_need_attention"], ["sample://barrel-1"])
        bridge = lessons.run_step("07")
        self.assertEqual(sum(map(len, bridge["findings_before"].values())), 6)
        self.assertEqual(bridge["findings_after_copy_update"], {
            "sample://crate-0": [], "sample://barrel-1": ["MISSING_MESH"], "sample://crate-2": []})


if __name__ == "__main__":
    unittest.main()
