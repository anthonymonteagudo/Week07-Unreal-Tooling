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
import zipfile
import hashlib

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


def install_native(engine):
    """Install only a module built for this exact installed engine."""
    package = ROOT / 'Support/Week07Tools_Win64.zip'
    if not package.is_file():
        raise RuntimeError('Missing native package. Run git lfs pull or download the complete demo ZIP.')
    with zipfile.ZipFile(package) as archive:
        metadata = json.loads(archive.read('build.json'))
        engine_id = json.loads((engine / 'Engine/Binaries/Win64/UnrealEditor.modules').read_text())['BuildId']
        if metadata['engine_build_id'] != engine_id:
            raise RuntimeError('Native plugin does not match this engine build. Use Unreal 5.7.4 from Epic Games Launcher, or follow Instructor/README.md to rebuild.')
        for name in ('UnrealEditor-Week07Tools.dll', 'UnrealEditor.modules'):
            data = archive.read(name)
            if hashlib.sha256(data).hexdigest() != metadata['sha256'][name]:
                raise RuntimeError('Native package checksum failed: ' + name)
            target = ROOT / 'Plugins/Week07Tools/Binaries/Win64' / name
            target.parent.mkdir(parents=True, exist_ok=True)
            if not target.exists() or target.read_bytes() != data:
                target.write_bytes(data)


def setup(override, ui=False):
    engine = engine_root(override)
    python = engine / 'Engine/Binaries/ThirdParty/Python3/Win64/python.exe'
    local_python = ROOT / '.venv/Scripts/python.exe'
    if not local_python.exists():
        subprocess.run([str(python), '-m', 'venv', str(ROOT / '.venv')], check=True)
    # Repair environments created by the older --without-pip setup.
    subprocess.run([str(local_python), '-m', 'ensurepip', '--upgrade'], check=True)
    LOCAL.parent.mkdir(exist_ok=True)
    LOCAL.write_text(json.dumps({'engine_root': str(engine)}, indent=2) + '\n', encoding='utf-8')
    install_native(engine)
    if ui:
        subprocess.run([str(local_python), '-m', 'pip', 'install', '--upgrade',
                        '--target', str(ROOT / '.deps/ui'), '-r', str(ROOT / 'requirements-ui.txt')], check=True)
    print('Setup complete. Open Week07UnrealPython.uproject; the Material/VFX map opens automatically.')
    print('Optional PySide installed.' if ui else 'Native tools ready. Add -WithQt to Setup.ps1 only if you want the PySide comparison.')


def check():
    count = 0
    for folder in ('Content/Python', 'Scripts', 'Tests', 'lesson_materials'):
        for path in (ROOT / folder).rglob('*.py'):
            ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
            count += 1
    print(f'Syntax OK: {count} Python files.')


def editor_run(script):
    """A separate full editor process; never connects to the live classroom session."""
    if not (ROOT / 'Scripts/editor' / script).exists():
        raise RuntimeError('This authoring command requires the full repository. For the small demo, follow README.md to run the Material/VFX tools.')
    if script == 'smoke_test.py' and not (ROOT / 'Content/Northwood').exists():
        raise RuntimeError('The legacy prop smoke test requires the archived Northwood assets. Use the Material/VFX checks in README.md for the small checkout.')
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
    checks['native_plugin_exists'] = (ROOT / 'Plugins/Week07Tools/Binaries/Win64/UnrealEditor-Week07Tools.dll').exists()
    print(json.dumps(checks, indent=2))
    if not checks['local_python_exists'] or not checks['native_plugin_exists']:
        raise RuntimeError('Run Setup.ps1 first. Autocomplete stubs are optional.')
    print('Ready. Autocomplete stubs are optional; they are not needed to run the tools.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['setup', 'check', 'test', 'doctor', 'editor-test', 'stubs'])
    parser.add_argument('--engine-root')
    parser.add_argument('--ui', action='store_true', help='Also install the optional PySide comparison UI.')
    args = parser.parse_args()
    if args.command == 'setup':
        setup(args.engine_root, args.ui)
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
