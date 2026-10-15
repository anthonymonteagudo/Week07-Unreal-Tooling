"""Offline verification only; never imports unreal or executes editor snippets."""
from pathlib import Path
import ast
import hashlib
import json
from PIL import Image

root = Path(__file__).resolve().parent
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
manifest = json.loads((root / "source-manifest.json").read_text(encoding="utf-8"))
for note in manifest["notes"]:
    assert sha(note["source"]) == note["source_sha256"]
    assert sha(root / "sources" / f'{note["lesson"]:02d}-original.md') == note["source_sha256"]
    assert Path(note["refined"]).is_file()
for entry in manifest["images"].values():
    assert sha(entry["source"]) == sha(root / entry["local"]) == entry["sha256"]
    with Image.open(root / entry["local"]) as im:
        assert min(im.size) > 0
        im.verify()
snippets = sorted((root / "snippets").glob("*.py"))
for snippet in snippets:
    ast.parse(snippet.read_text(encoding="utf-8"))
code = (root / "sources/original-buildSelectedAssets.py").read_text(encoding="utf-8")
raw = json.loads((root / "sources/source-extraction.json").read_text(encoding="utf-8"))
assert code == raw[2]["text"].split("CODE:", 1)[1].lstrip("\n")
ast.parse(code)

# Extract and execute only the ordinary-Python name parser, with no Unreal code.
tree = ast.parse((root / "snippets/03-01.py").read_text(encoding="utf-8"))
parser = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "texture_identity")
namespace = {}
exec(compile(ast.Module(body=[parser], type_ignores=[]), "texture_identity", "exec"), namespace)
parse = namespace["texture_identity"]
valid = {
    "T_AirConditioning_01_BC": ("AirConditioning_01", "BC"),
    "T_Air_Conditioning_01_N": ("Air_Conditioning_01", "N"),
    "T_Pipe_02_ORM": ("Pipe_02", "ORM"),
}
for name, expected in valid.items():
    assert parse(name) == expected
invalid = ["SM_AirConditioning_01_BC", "T__BC", "T_AirConditioning_01", "T_AirConditioning_01_Roughness", "T_AirConditioning_01_bc"]
for name in invalid:
    try:
        parse(name)
    except ValueError:
        pass
    else:
        raise AssertionError(name)
assert parse("T_AirConditioning_010_BC")[0] != "AirConditioning_01"
assert parse("T_AirConditioning_01_Variant_BC")[0] != "AirConditioning_01"
result = {
    "original_notes_unchanged": len(manifest["notes"]),
    "image_hashes_and_decoding_passed": len(manifest["images"]),
    "refined_snippets_syntax_passed": len(snippets),
    "original_script_preserved_and_syntax_checked": True,
    "pure_python_name_cases_passed": len(valid) + len(invalid) + 2,
    "unreal_code_executed": False,
    "deck_or_teaching_tool_code_modified": False,
}
(root / "verification.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps(result))
