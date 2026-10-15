"""Offline checkpoint behavior with explicit host doubles, not engine validation."""
import contextlib
import io
from pathlib import Path
import sys
from types import SimpleNamespace as NS
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "Content/Python"))
import week07_lessons as lessons


class Texture:
    def __init__(self, name, compression="DEFAULT"):
        self.name, self.compression = name, compression
    def get_name(self): return self.name
    def get_path_name(self): return "/Game/" + self.name
    def get_editor_property(self, key):
        return {"compression_settings": self.compression, "srgb": True}[key]


class Material:
    pass


class Component:
    def __init__(self):
        self.material = Material()
        self.edits = 0
    def get_num_materials(self): return 1
    def get_material(self, slot): return self.material
    def modify(self): pass
    def set_material(self, slot, material):
        self.edits += 1
        self.material = material


class Actor:
    def __init__(self, tag="W07_MaterialTarget"):
        self.tags = [tag]
        self.part = Component()
    def get_components_by_class(self, cls): return [self.part]


class AssignmentHost:
    def __init__(self):
        self.actor, self.material = Actor(), Material()
        self.selected_actors, self.selected_assets = [self.actor], [self.material]
        self.pie, self.transactions = False, 0
        self.map_path = "/Game/Week07/Maps/W07_MaterialVFXLab.Map"
        self.EditorActorSubsystem, self.LevelEditorSubsystem = object(), object()
        self.UnrealEditorSubsystem, self.StaticMeshComponent = object(), object()
        self.MaterialInterface = Material
        self.EditorUtilityLibrary = NS(get_selected_assets=lambda: self.selected_assets)
    def get_editor_subsystem(self, cls):
        if cls is self.EditorActorSubsystem:
            return NS(get_selected_level_actors=lambda: self.selected_actors)
        if cls is self.LevelEditorSubsystem:
            return NS(is_in_play_in_editor=lambda: self.pie)
        return NS(get_editor_world=lambda: NS(get_path_name=lambda: self.map_path))
    @contextlib.contextmanager
    def ScopedEditorTransaction(self, label):
        self.transactions += 1
        yield


class ImportTask:
    def __init__(self): self.imported_object_paths = []
    def set_editor_property(self, name, value): setattr(self, name, value)
    def get_editor_property(self, name): return getattr(self, name)


class Mesh:
    def get_bounding_box(self): return "120 x 60 x 180 cm (test double)"


class ImportHost:
    def __init__(self):
        self.AssetImportTask = self.FbxImportUI = ImportTask
        self.FbxFactory, self.StaticMesh = object, Mesh
        self.FBXImportType = NS(FBXIT_STATIC_MESH="STATIC")
        self.Paths = NS(project_dir=lambda: str(ROOT))
        self.LevelEditorSubsystem = object()
        self.exists, self.pie, self.fail, self.good_path = False, False, False, True
        self.commands, self.calls = [], 0
        self.EditorAssetLibrary = NS(does_asset_exist=lambda p: self.exists)
        self.SystemLibrary = NS(get_console_variable_int_value=lambda f: 1,
                                execute_console_command=lambda world, text: self.commands.append(text))
        self.AssetToolsHelpers = NS(get_asset_tools=lambda: NS(import_asset_tasks=self.import_tasks))
    def get_editor_subsystem(self, cls): return NS(is_in_play_in_editor=lambda: self.pie)
    def load_asset(self, path): return Mesh()
    def import_tasks(self, tasks):
        self.calls += 1
        if self.fail: raise RuntimeError("Importer failure")
        task = tasks[0]
        task.imported_object_paths = [task.destination_path + "/" + task.destination_name + "." + task.destination_name] if self.good_path else []


def execute(step, module=None, host="unreal"):
    output = io.StringIO()
    with patch.dict(sys.modules, {host: module}), contextlib.redirect_stdout(output):
        namespace = {"__name__": "__main__"}
        exec(compile(lessons.source(step), step, "exec"), namespace)
    return output.getvalue(), namespace


class ApiCheckpointTests(unittest.TestCase):
    def test_all_blocks_compile_and_every_file_has_its_own_imports(self):
        ids = [s["id"] for s in lessons.catalog()]
        self.assertEqual(len(ids), len(set(ids)))
        for step in lessons.catalog():
            source = lessons.source(step["id"])
            compile(source, step["file"], "exec")
            self.assertEqual(list(lessons.blocks(step["id"])), step["blocks"])
            if step["host"] != "python":
                self.assertIn("import " + {"unreal": "unreal", "blender": "bpy"}[step["host"]], source)
            for name, block in lessons.blocks(step["id"]).items():
                compile(block, step["id"] + "." + name, "exec")

    def test_selection_reports_empty_without_index_error(self):
        host = NS(EditorActorSubsystem=object(), get_editor_subsystem=lambda cls:
                  NS(get_selected_level_actors=lambda: []))
        for ident in ["UE02", "UE03", "UE10"]:
            if ident == "UE10": host.NiagaraComponent = object()
            if ident == "UE03": host.StaticMeshComponent = object()
            output, _ = execute(ident, host)
            self.assertIn("0", output)

    def test_validation_reports_all_mismatches_and_never_edits(self):
        assets = [Texture("A_Normal"), Texture("B_Normal"),
                  Texture("C_Normal", "NORMAL"), Texture("Legacy_N"),
                  Texture("D_Base"), object()]
        host = NS(Texture2D=Texture, TextureCompressionSettings=NS(TC_NORMALMAP="NORMAL"),
                  EditorUtilityLibrary=NS(get_selected_assets=lambda: assets))
        output, ns = execute("UE06", host)
        self.assertEqual((ns["checked"], ns["mismatches"]), (3, 2))
        self.assertIn("A_Normal", output)
        self.assertIn("B_Normal", output)
        self.assertEqual(assets[0].compression, "DEFAULT")

    def test_zero_eligible_textures_is_not_a_pass(self):
        host = NS(Texture2D=Texture, TextureCompressionSettings=NS(TC_NORMALMAP="NORMAL"),
                  EditorUtilityLibrary=NS(get_selected_assets=lambda: []))
        output, _ = execute("UE06", host)
        self.assertIn("not a passing validation", output)

    def test_material_eligibility_blocks_before_editing(self):
        for bad in ["protected", "empty", "multi", "no_material", "wrong_material", "PIE", "map"]:
            with self.subTest(case=bad):
                host = AssignmentHost()
                if bad == "protected": host.actor.tags = ["W07_Protected"]
                if bad == "empty": host.selected_actors = []
                if bad == "multi": host.selected_actors *= 2
                if bad == "no_material": host.selected_assets = []
                if bad == "wrong_material": host.selected_assets = [object()]
                if bad == "PIE": host.pie = True
                if bad == "map": host.map_path = "/Game/Other.Other"
                with self.assertRaises(RuntimeError): execute("UE08", host)
                self.assertEqual(host.actor.part.edits, 0)
                self.assertEqual(host.transactions, 0)

    def test_assignment_and_repeat_noop(self):
        host = AssignmentHost()
        execute("UE08", host)
        self.assertIs(host.actor.part.material, host.material)
        output, _ = execute("UE08", host)
        self.assertEqual((host.actor.part.edits, host.transactions), (1, 1))
        self.assertIn("no new Undo entry", output)

    def test_task_preparation_does_not_import(self):
        host = ImportHost()
        _, ns = execute("UE11", host)
        self.assertEqual(host.calls, 0)
        self.assertFalse(ns["task"].replace_existing)
        self.assertFalse(ns["task"].save)

    def test_import_checks_result_and_restores_importer_flag(self):
        for failure in [False, True]:
            host = ImportHost()
            host.fail = failure
            if failure:
                with self.assertRaises(RuntimeError): execute("UE12", host)
            else: execute("UE12", host)
            self.assertEqual(host.commands, ["Interchange.FeatureFlags.Import.FBX 0", "Interchange.FeatureFlags.Import.FBX 1"])
        host = ImportHost()
        host.good_path = False
        with self.assertRaisesRegex(RuntimeError, "Expected mesh missing"): execute("UE12", host)

    def test_existing_destination_and_pie_never_invoke_import(self):
        for field in ["exists", "pie"]:
            host = ImportHost()
            setattr(host, field, True)
            with self.assertRaises(RuntimeError): execute("UE12", host)
            self.assertEqual((host.calls, host.commands), (0, []))

    def test_evaluated_mesh_releases_on_read_failure(self):
        class Broken:
            @property
            def polygons(self): raise RuntimeError("Read failed")
        cleared = []
        evaluated = NS(to_mesh=lambda: Broken(), to_mesh_clear=lambda: cleared.append(True))
        obj = NS(type="MESH", data=NS(polygons=[1]), evaluated_get=lambda g: evaluated)
        host = NS(context=NS(mode="OBJECT", selected_objects=[obj], evaluated_depsgraph_get=lambda: object()))
        with self.assertRaisesRegex(RuntimeError, "Read failed"): execute("BL03", host, "bpy")
        self.assertEqual(cleared, [True])

    def test_blender_wrong_mode_and_empty_selection_stop(self):
        for step in ["BL03", "BL04"]:
            for mode, objects in [("OBJECT", []), ("EDIT_MESH", [NS(type="MESH")])]:
                host = NS(context=NS(mode=mode, selected_objects=objects))
                with self.assertRaises(RuntimeError): execute(step, host, "bpy")

    def test_plain_python_snapshot_has_no_host_dependency(self):
        output, _ = execute("PY01")
        self.assertIn("BLOCKED", output)

    def test_launcher_rejects_unknown_id_and_wrong_host(self):
        with self.assertRaises(ValueError): lessons.resolve("../../something.py")
        with patch.dict(sys.modules, {"unreal": None}):
            with self.assertRaisesRegex(RuntimeError, "inside Unreal"): lessons.run("UE02")
        with patch.dict(sys.modules, {"bpy": None}):
            with self.assertRaisesRegex(RuntimeError, "inside Blender"): lessons.run("BL01")


if __name__ == "__main__":
    unittest.main()
