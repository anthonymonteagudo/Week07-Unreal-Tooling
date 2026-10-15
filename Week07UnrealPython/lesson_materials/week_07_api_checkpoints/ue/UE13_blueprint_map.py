"""Optional: Execute Python Script node output unreal_map; Config is Map<String,Integer>.
Run inside an editor utility Blueprint. Inspect a=1, b=2; change b and rerun.
No scene edits. The execution-success Boolean is separate from the data.
"""
import unreal
my_dict = {"a": 1, "b": 2}
unreal_map = unreal.Map.cast(str, int, my_dict)
