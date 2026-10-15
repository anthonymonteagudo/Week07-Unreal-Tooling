$ErrorActionPreference='Stop'
$taskDeck = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot 'output/Week 7 - Integrated UX and Asset Workflows v6.pptx'))
$taskPpt = New-Object -ComObject PowerPoint.Application
$taskPresentation = $taskPpt.Presentations.Open($taskDeck, -1, 0, 0)
try {
    $taskShows = @()
    for($taskIndex=1; $taskIndex -le $taskPresentation.SlideShowSettings.NamedSlideShows.Count; $taskIndex++) {
        $taskShow=$taskPresentation.SlideShowSettings.NamedSlideShows.Item($taskIndex)
        $taskShows += @{name=$taskShow.Name; count=$taskShow.Count}
    }
    $taskVideos = @()
    foreach ($taskSlide in $taskPresentation.Slides) {
        foreach ($taskShape in $taskSlide.Shapes) {
            if ($taskShape.Type -eq 16) {
                $taskVideos += @{slide=$taskSlide.SlideIndex; name=$taskShape.Name; mediaType=$taskShape.MediaType}
            }
        }
    }
    $taskReceipt = @{slideCount=$taskPresentation.Slides.Count; customShows=$taskShows; media=$taskVideos; claimBoundary='PowerPoint recognizes media and the custom show; this is not a playback or live delivery rehearsal.'}
    $taskReceipt | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'qa/native-package-verification.json') -Encoding utf8
    $taskReceipt | ConvertTo-Json -Depth 4
    if(-not ($taskShows | Where-Object {$_.name -eq 'Week 7 timed class route' -and $_.count -eq 70})) {throw 'PowerPoint did not recognize the 70-slide custom show.'}
    if($taskVideos.Count -ne 9) {throw 'Expected nine native media shapes.'}
} finally {
    $taskPresentation.Close()
    [void][Runtime.InteropServices.Marshal]::ReleaseComObject($taskPresentation)
    [void][Runtime.InteropServices.Marshal]::ReleaseComObject($taskPpt)
}
