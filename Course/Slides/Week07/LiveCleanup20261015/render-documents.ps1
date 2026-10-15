$ErrorActionPreference = 'Stop'
$taskRoot = $PSScriptRoot
$wordApp = New-Object -ComObject Word.Application
$wordApp.Visible = $false
$wordApp.DisplayAlerts = 0
try {
    foreach ($file in Get-ChildItem -LiteralPath (Join-Path $taskRoot 'output') -Filter '*.docx') {
        $taskDirectory = Join-Path $taskRoot ('qa/documents/' + $file.BaseName)
        New-Item -ItemType Directory -Force -Path $taskDirectory | Out-Null
        $document = $wordApp.Documents.Open($file.FullName, $false, $true, $false)
        try {
            $document.Repaginate()
            $document.ExportAsFixedFormat((Join-Path $taskDirectory 'render.pdf'), 17)
            Write-Output ($file.Name + ': ' + $document.ComputeStatistics(2) + ' pages')
        } finally { $document.Close(0) }
    }
} finally { $wordApp.Quit(0) }
