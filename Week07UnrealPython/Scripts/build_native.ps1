param([string]$EngineRoot = 'C:\Program Files\Epic Games\UE_5.7')
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$plugin = Join-Path $projectRoot 'Plugins/Week07Tools/Week07Tools.uplugin'
$buildOutput = Join-Path $projectRoot ('Saved/NativeBuild/' + (Get-Date -Format 'yyyyMMdd_HHmmss'))
$uat = Join-Path $EngineRoot 'Engine/Build/BatchFiles/RunUAT.bat'
& $uat BuildPlugin "-Plugin=$plugin" "-Package=$buildOutput" -TargetPlatforms=Win64
if ($LASTEXITCODE -ne 0) { throw 'Native plugin build failed. Install the documented Visual Studio components.' }
$python = Join-Path $EngineRoot 'Engine/Binaries/ThirdParty/Python3/Win64/python.exe'
& $python (Join-Path $PSScriptRoot 'package_native.py') --build $buildOutput --engine-root $EngineRoot
if ($LASTEXITCODE -ne 0) { throw 'Native packaging failed.' }
