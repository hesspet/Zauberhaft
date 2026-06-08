param(
  [switch]$WhatIfMode
)

$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
$articleDirectory = Join-Path $projectRoot "_artikel"

if (-not (Test-Path -LiteralPath $articleDirectory)) {
  Write-Host "Artikelordner nicht gefunden: $articleDirectory"
  exit 1
}

$dateRegex = '^(\s*date:\s*)(\d{4}-\d{2}-\d{2})(\s*)$'
$updatedRegex = '^(\s*updated:\s*)(\d{4}-\d{2}-\d{2})(\s*)$'
$hasTimeRegex = '\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}'

$changedCount = 0
$skippedCount = 0
$errorCount = 0

$articleFiles = Get-ChildItem -LiteralPath $articleDirectory -Filter "*.md" -File

foreach ($file in $articleFiles) {
  $lines = Get-Content -LiteralPath $file.FullName -Encoding UTF8
  $changed = $false
  $newLines = @()

  foreach ($line in $lines) {
    $newLine = $line

    if ($line -match $dateRegex) {
      $currentValue = $matches[2]
      if ($currentValue -notmatch $hasTimeRegex) {
        $newValue = "$currentValue 00:00"
        $newLine = "$($matches[1])$newValue$($matches[3])"
        Write-Host "$($file.Name): date '$currentValue' -> '$newValue'"
        $changed = $true
      }
    }
    elseif ($line -match $updatedRegex) {
      $currentValue = $matches[2]
      if ($currentValue -notmatch $hasTimeRegex) {
        $newValue = "$currentValue 00:00"
        $newLine = "$($matches[1])$newValue$($matches[3])"
        Write-Host "$($file.Name): updated '$currentValue' -> '$newValue'"
        $changed = $true
      }
    }

    $newLines += $newLine
  }

  if ($changed) {
    if (-not $WhatIfMode) {
      try {
        $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
        [System.IO.File]::WriteAllLines($file.FullName, $newLines, $utf8NoBom)
        $changedCount++
      }
      catch {
        Write-Error "Fehler beim Schreiben von $($file.Name): $_"
        $errorCount++
      }
    }
    else {
      Write-Host "[WhatIf] Wuerde $($file.Name) aktualisieren."
      $changedCount++
    }
  }
  else {
    $skippedCount++
  }
}

Write-Host ""
Write-Host "============================================"
Write-Host "Migration abgeschlossen."
Write-Host "  Geaendert: $changedCount"
Write-Host "  Uebersprungen (bereits mit Uhrzeit): $skippedCount"
if ($errorCount -gt 0) {
  Write-Host "  Fehler: $errorCount"
}
if ($WhatIfMode) {
  Write-Host "  (WhatIf-Modus - keine Aenderungen geschrieben)"
}
Write-Host "============================================"
