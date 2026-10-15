"""Local development commands. Uses only the Python standard library.

The Unreal import stub is never added to the runtime Python path.
"""
import argparse
import ast
from datetime import datetime
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / 'Week07UnrealPython.uproject'
LOCAL = ROOT / '.vscode/unreal.local.json'


def engine_root(override=None):
    if override:
        candidate = Path(override)
    elif LOCAL.exists():
        candidate = Path(json.loads(LOCAL.read_text(encoding='utf-8'))['engine_root'])
    else:
        version = json.loads(PROJECT.read_text(encoding='utf-8-sig'))['EngineAssociation']
        candidate = Path(os.environ.get('ProgramFiles', 'C:/Program Files')) / 'Epic Games' / f'UE_{version}'
    if not (candidate / 'Engine/Binaries/Win64/UnrealEditor-Cmd.exe').is_file():
        raise RuntimeError('Engine not found. Run dev.py setup --engine-root "path to UE_5.7".')
    return candidate.resolve()


def setup(override):
    engine = engine_root(override)
    python = engine / 'Engine/Binaries/ThirdParty/Python3/Win64/python.exe'
    local_python = ROOT / '.venv/Scripts/python.exe'
    if not local_python.exists():
        subprocess.run([str(python), '-m', 'venv', '--without-pip', str(ROOT / '.venv')], check=True)
    LOCAL.parent.mkdir(exist_ok=True)
    LOCAL.write_text(json.dumps({'engine_root': str(engine)}, indent=2) + '\n', encoding='utf-8')
    print('Local Python environment ready (no third-party packages needed).')
    print('Next: open Week07PythonTools.code-workspace; run dev.py stubs if autocomplete is missing.')


def check():
    count = 0
    for folder in ('Content/Python', 'Scripts', 'Tests', 'lesson_materials'):
        for path in (ROOT / folder).rglob('*.py'):
            ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
            count += 1
    print(f'Syntax OK: {count} Python files.')


def editor_run(script):
    """A separate full editor process; never connects to the live classroom session."""
    engine = engine_root()
    run_dir = ROOT / 'Saved/Tooling/Checks' / datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    run_dir.mkdir(parents=True)
    result_path = run_dir / 'result.json'
    command = [str(engine / 'Engine/Binaries/Win64/UnrealEditor-Cmd.exe'), str(PROJECT),
               '/Engine/Maps/Entry', f'-ExecutePythonScript={ROOT / "Scripts/editor" / script}',
               '-unattended', '-nosplash', '-RenderOffscreen', '-nosound', '-nop4',
               '-stdout', '-FullStdOutLogOutput']
    environment = dict(os.environ, WEEK07_RESULT_PATH=str(result_path))
    print(f'Running separate Unreal session. Log: {run_dir / "editor.log"}', flush=True)
    with (run_dir / 'editor.log').open('w', encoding='utf-8') as log:
        completed = subprocess.run(command, cwd=ROOT, env=environment, stdout=log,
                                   stderr=subprocess.STDOUT, timeout=300)
    if completed.returncode or not result_path.exists():
        raise RuntimeError(f'Editor test did not complete. Read {run_dir / "editor.log"}')
    result = json.loads(result_path.read_text(encoding='utf-8'))
    print(json.dumps(result, indent=2))
    if result.get('status') != 'PASS':
        raise RuntimeError(f'Editor check failed: {result_path}')


def doctor():
    engine = engine_root()
    stub = ROOT / 'Intermediate/PythonStub/unreal.py'
    checks = {'engine': str(engine), 'local_python': str(ROOT / '.venv/Scripts/python.exe'),
              'local_python_exists': (ROOT / '.venv/Scripts/python.exe').exists(),
              'unreal_autocomplete_exists': stub.exists(),
              'python': sys.version.split()[0]}
    print(json.dumps(checks, indent=2))
    if not checks['local_python_exists'] or not checks['unreal_autocomplete_exists']:
        raise RuntimeError('Run setup and stubs to finish development setup.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['setup', 'check', 'test', 'doctor', 'editor-test', 'stubs'])
    parser.add_argument('--engine-root')
    args = parser.parse_args()
    if args.command == 'setup':
        setup(args.engine_root)
    elif args.command == 'check':
        check()
    elif args.command == 'test':
        subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', 'Tests', '-v'], cwd=ROOT, check=True)
    elif args.command == 'doctor':
        doctor()
    else:
        editor_run('smoke_test.py' if args.command == 'editor-test' else 'generate_stubs.py')


if __name__ == '__main__':
    main()
