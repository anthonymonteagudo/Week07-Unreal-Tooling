# Week 7 instructor setup

Use **Windows and Epic Games Launcher Unreal 5.7.4**. The prepared native plugin avoids a Visual Studio installation. Download the demo ZIP from the root README for the quickest setup, or use the small Git checkout below to edit and pull updates.

## Pull a small working checkout

Install Git with Git LFS and obtain access to this private repository. In PowerShell:

```powershell
git lfs install
$env:GIT_LFS_SKIP_SMUDGE = '1'
git clone --no-checkout --depth 1 https://github.com/anthonymonteagudo/Week07-Unreal-Tooling.git
cd Week07-Unreal-Tooling
git sparse-checkout set --no-cone '/*' '!/Course/' '!/Releases/' '!/Week07UnrealPython/Content/Northwood/' '!/Week07UnrealPython/Content/Week07/Maps/W07_PythonLab.umap' '!/Week07UnrealPython/Reference/' '!/Week07UnrealPython/Deliverables/'
git checkout main
git config --local lfs.fetchinclude 'Week07UnrealPython/Content/Week07/LiveDemo/**,Week07UnrealPython/Content/Week07/Bridge/**,Week07UnrealPython/Content/Week07/Maps/W07_MaterialVFXLab.umap,Week07UnrealPython/Samples/Bridge/**,Week07UnrealPython/Source/LiveDemo/**,Instructor/**'
git lfs pull
Remove-Item Env:GIT_LFS_SKIP_SMUDGE
cd Week07UnrealPython
powershell -ExecutionPolicy Bypass -File .\Setup.ps1 -WithQt
```

For a nondefault Unreal installation, add `-EngineRoot 'D:\Epic Games\UE_5.7'`. Setup uses Unreal's Python 3.11, creates a local environment with pip, installs the matching native module and optionally downloads PySide. It does not open Unreal. No system Python changes are needed.

If GitHub reports "Repository not found", sign in with the GitHub account that has access to this private repository. The URL above is correct. Avoid adding `--filter=blob:none`: with this archive, Git LFS can then make thousands of extra requests to inspect the omitted asset pointers.

Open `Week07UnrealPython.uproject`, then follow [the demo quick start](../Week07UnrealPython/README.md). To update later, run `git pull --ff-only`, `git lfs pull`, then rerun `Setup.ps1 -WithQt`. Preserve or commit your local edits before pulling.

The sparse checkout omits older course materials. For slides or the full archive, use a separate full clone; do not expand it during classroom setup. The working project opens the prepared Material/VFX map and does not require Northwood assets.

For this snapshot, Git still downloads about 354 MiB of repository objects plus 26 MiB of selected LFS files. Use the demo ZIP (under 1 MB) when you only need to run the demonstration. Unreal and the optional PySide install are separate from these download sizes.

## Check the setup

From `Week07UnrealPython`:

```powershell
.\.venv\Scripts\python.exe Scripts/dev.py doctor
.\.venv\Scripts\python.exe Scripts/dev.py test
.\.venv\Scripts\python.exe Scripts/ui_quality.py --stage 3
```

The UI check requires `-WithQt`. Autocomplete stubs are optional. The native panel and external PySide window are separate interfaces over the same tools. Use the project README's reset guidance; importing an asset is not a general Undo transaction.

## Rebuild the native plugin only when needed

If you change C++ or use a different engine build, install Visual Studio 2022 (17.14 recommended), Game development with C++, MSVC v143 14.44 and a Windows SDK (10.0.22621 or newer recommended). Follow [Epic's Unreal 5.7 toolchain instructions](https://dev.epicgames.com/documentation/en-us/unreal-engine/setting-up-visual-studio-development-environment-for-cplusplus-projects-in-unreal-engine?application_version=5.7) for the full component list.

Close this project's editor before replacing its module. From `Week07UnrealPython`:

```powershell
powershell -ExecutionPolicy Bypass -File Scripts/build_native.ps1
powershell -ExecutionPolicy Bypass -File Setup.ps1 -WithQt
```

The build command records the engine build ID, source hashes and module checksums in `Support/Week07Tools_Win64.zip`. Setup refuses a mismatched binary. The provided release is tested on 5.7.4; a different engine requires its own verification.

## Maintain the teaching release

`Instructor/HandoutSources` contains the editable handouts. Re-export their PDFs to `StudentMaterials` after edits. `build_student_materials.py` creates the short class guide; `build_release.py` packages the two downloads without the instructor archive, caches, installed dependencies or Northwood environment. Neither script edits slides. See [verification.json](verification.json) for this release's checks.

The existing Perforce workspace remains the original authoring location. Sync narrowly and review changes before committing. Do not run the historical broad snapshot sync merely to refresh a handout: it also copies the instructor archive. The Northwood provenance and third-party licenses remain in the archive; the student demo contains only the prepared Week 7 fixtures and their engine/plugin dependencies.
