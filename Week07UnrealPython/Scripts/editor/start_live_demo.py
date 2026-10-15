"""Explicit classroom launch only; no map clearing, asset deletion or automatic save."""
import unreal
from week07_tooling.editor import live_demo
unreal.log(live_demo.preflight())
unreal.Week07EditorLibrary.open_tools()
