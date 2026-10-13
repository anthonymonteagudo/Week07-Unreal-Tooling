param([string]$EngineRoot = 'C:\Program Files\Epic Games\UE_5.7')
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$projectFile = Join-Path $projectRoot 'Week07UnrealPython.uproject'
$editor = Join-Path $EngineRoot 'Engine\Binaries\Win64\UnrealEditor.exe'
if (!(Test-Path -LiteralPath $editor)) { throw 'Unreal 5.7 editor not found. Pass -EngineRoot with its installation folder.' }
$running = Get-CimInstance Win32_Process -Filter "Name='UnrealEditor.exe'" | Where-Object { $_.CommandLine -like '*Week07UnrealPython.uproject*' }
if ($running) { throw 'This project is already open. Use Tools > Material & VFX Tools in that editor.' }
$startScript = Join-Path $projectRoot 'Scripts\editor\start_live_demo.py'
$startupCode = [Convert]::ToBase64String([IO.File]::ReadAllBytes($startScript))
$startupCommand = '-ExecCmds="py exec(__import__(''base64'').b64decode(''' + $startupCode + '''))"'
# The user requested a visible, interactive teaching editor.
Start-Process -FilePath $editor -ArgumentList @(('"'+$projectFile+'"'), '/Game/Week07/Maps/W07_MaterialVFXLab', $startupCommand, '-nosplash', '-nop4', '-windowed', '-ResX=1600', '-ResY=1000')

