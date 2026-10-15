param([string]$Deck = '', [string]$Destination = 'qa/render-1')
$ErrorActionPreference = 'Stop'
$taskRoot = $PSScriptRoot
if (-not $Deck) { $Deck = Join-Path $taskRoot 'build/candidate.pptx' }
$Deck = [IO.Path]::GetFullPath($Deck)
if (-not (Test-Path -LiteralPath $Deck)) { throw "Missing deck: $Deck" }
$taskOutput = Join-Path $taskRoot $Destination
New-Item -ItemType Directory -Force -Path $taskOutput | Out-Null
$presentationApp = New-Object -ComObject PowerPoint.Application
$deckObject = $presentationApp.Presentations.Open($Deck, -1, 0, 0)
$findings = @()
try {
    for ($slideIndex = 1; $slideIndex -le $deckObject.Slides.Count; $slideIndex++) {
        $slide = $deckObject.Slides.Item($slideIndex)
        $slide.Export((Join-Path $taskOutput ('slide-{0:d3}.png' -f $slideIndex)), 'PNG', 1600, 900)
        foreach ($shape in $slide.Shapes) {
            if ($shape.HasTable) {
                for ($rowIndex = 1; $rowIndex -le $shape.Table.Rows.Count; $rowIndex++) {
                    for ($colIndex = 1; $colIndex -le $shape.Table.Columns.Count; $colIndex++) {
                        $cellShape = $shape.Table.Cell($rowIndex, $colIndex).Shape
                        $cellText = $cellShape.TextFrame2.TextRange
                        $cellAvailable = $cellShape.Height - $cellShape.TextFrame2.MarginTop - $cellShape.TextFrame2.MarginBottom
                        if ($cellText.BoundHeight -gt ($cellAvailable + 2)) {
                            $findings += @{slide=$slideIndex; shape=$shape.Name; row=$rowIndex; column=$colIndex; height=$cellShape.Height; boundHeight=$cellText.BoundHeight; text=$cellText.Text}
                        }
                    }
                }
            }
            if ($shape.HasTextFrame -and $shape.TextFrame.HasText) {
                $textRange = $shape.TextFrame2.TextRange
                $availableHeight = $shape.Height - $shape.TextFrame2.MarginTop - $shape.TextFrame2.MarginBottom
                if ($textRange.BoundHeight -gt ($availableHeight + 2)) {
                    $findings += @{slide=$slideIndex; shape=$shape.Name; height=$shape.Height; boundHeight=$textRange.BoundHeight; text=$textRange.Text}
                }
            }
        }
    }
    ConvertTo-Json -InputObject @($findings) -Depth 5 | Set-Content -LiteralPath (Join-Path $taskOutput 'text-fit.json') -Encoding utf8
    Write-Output ('Rendered {0} slides; {1} text-fit findings.' -f $deckObject.Slides.Count, $findings.Count)
} finally {
    $deckObject.Close()
    [void][Runtime.InteropServices.Marshal]::ReleaseComObject($deckObject)
    [void][Runtime.InteropServices.Marshal]::ReleaseComObject($presentationApp)
}
