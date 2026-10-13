"""01: Unreal supplies the host API. Run in the Editor, not a Python terminal."""
import unreal


def run():
    context = {'engine': unreal.SystemLibrary.get_engine_version(),
               'project': unreal.Paths.project_dir()}
    unreal.log(f'Hello from Week 7 Unreal Python tooling: {context}')
    return context
