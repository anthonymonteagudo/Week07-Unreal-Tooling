param(
    [string]$EngineRoot = 'C:\Program Files\Epic Games\UE_5.7',
    [switch]$WithQt
)
$ErrorActionPreference = 'Stop'
$python = Join-Path $EngineRoot 'Engine/Binaries/ThirdParty/Python3/Win64/python.exe'
if (!(Test-Path -LiteralPath $python)) {
    throw 'Unreal Python was not found. Install Unreal 5.7.4 or pass -EngineRoot with your UE_5.7 folder.'
}
$version = Get-Content -LiteralPath (Join-Path $EngineRoot 'Engine/Build/Build.version') -Raw | ConvertFrom-Json
if ($version.MajorVersion -ne 5 -or $version.MinorVersion -ne 7 -or $version.PatchVersion -ne 4) {
    throw 'This teaching package is verified for Unreal 5.7.4. Install that version before setup.'
}
$setupArgs = @((Join-Path $PSScriptRoot 'Scripts/dev.py'), 'setup', '--engine-root', $EngineRoot)
if ($WithQt) { $setupArgs += '--ui' }
& $python @setupArgs
if ($LASTEXITCODE -ne 0) { throw 'Setup did not finish. See the error above.' }
