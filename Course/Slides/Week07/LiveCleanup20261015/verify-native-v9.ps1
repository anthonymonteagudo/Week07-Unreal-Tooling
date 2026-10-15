$ErrorActionPreference='Stop'
$taskDeck = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot 'output/Week 7 - Ordered Lessons v9.1.pptx'))
$taskPpt = New-Object -ComObject PowerPoint.Application
$taskPresentation = $taskPpt.Presentations.Open($taskDeck, -1, 0, 0)
try {
    $taskShows = @()
    for($taskIndex=1; $taskIndex -le $taskPresentation.SlideShowSettings.NamedSlideShows.Count; $taskIndex++) {
        $taskShow=$taskPresentation.SlideShowSettings.NamedSlideShows.Item($taskIndex)
        # PowerPoint's COM array includes an unused zero slot before the slide IDs.
        $taskShows += @{name=$taskShow.Name; count=$taskShow.Count; slideIds=@($taskShow.SlideIDs | Where-Object {$_ -gt 0})}
    }
    $taskVideos = @()
    foreach ($taskSlide in $taskPresentation.Slides) {
        foreach ($taskShape in $taskSlide.Shapes) {
            if ($taskShape.Type -eq 16) {
                $taskVideos += @{slide=$taskSlide.SlideIndex; name=$taskShape.Name; mediaType=$taskShape.MediaType}
            }
        }
    }
    $taskVisibleIds = @()
    foreach ($taskSlide in $taskPresentation.Slides) {
        if ($taskSlide.SlideShowTransition.Hidden -eq 0) { $taskVisibleIds += $taskSlide.SlideID }
    }
    $taskLive = $taskShows | Where-Object {$_.name -eq 'Week 7 live route'}
    if (($taskVisibleIds -join ',') -ne ($taskLive.slideIds -join ',')) {throw 'Normal show and custom show differ.'}
    $taskSections = @()
    for($taskIndex=1; $taskIndex -le $taskPresentation.SectionProperties.Count; $taskIndex++) {
        $taskSections += @{name=$taskPresentation.SectionProperties.Name($taskIndex); start=$taskPresentation.SectionProperties.FirstSlide($taskIndex); count=$taskPresentation.SectionProperties.SlidesCount($taskIndex)}
    }
    $taskExpected = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'qa/sequence-changes-v9.json') -Raw | ConvertFrom-Json
    if ($taskSections.Count -ne $taskExpected.sections.Count) {throw 'Native section count differs.'}
    for($taskIndex=0; $taskIndex -lt $taskSections.Count; $taskIndex++) {
        if ($taskSections[$taskIndex].name -ne $taskExpected.sections[$taskIndex].name -or $taskSections[$taskIndex].start -ne $taskExpected.sections[$taskIndex].start) {throw 'Native section differs from the intended lesson order.'}
    }
    $taskReceipt = @{slideCount=$taskPresentation.Slides.Count; customShows=$taskShows; normalShowMatchesCustomShow=$true; sections=$taskSections; media=$taskVideos; claimBoundary='PowerPoint recognizes media, ordered sections and matching show routes; this is not a new live engine rehearsal.'}
    $taskReceipt | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'qa/native-package-verification-v9.json') -Encoding utf8
    $taskReceipt | ConvertTo-Json -Depth 4
    if(-not ($taskShows | Where-Object {$_.name -eq 'Week 7 live route' -and $_.count -eq 96})) {throw 'PowerPoint did not recognize the 96-slide custom show.'}
    if($taskVideos.Count -ne 9) {throw 'Expected nine native media shapes.'}
} finally {
    $taskPresentation.Close()
    [void][Runtime.InteropServices.Marshal]::ReleaseComObject($taskPresentation)
    [void][Runtime.InteropServices.Marshal]::ReleaseComObject($taskPpt)
}

