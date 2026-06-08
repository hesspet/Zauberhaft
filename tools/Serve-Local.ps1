$ErrorActionPreference = "Stop"
$kleinesAe = [char]0x00E4
$kleinesUe = [char]0x00FC

function Add-RubyInstallerPath {
  $rubyBinPath = "C:\Ruby33-x64\bin"
  if (Test-Path -LiteralPath (Join-Path $rubyBinPath "ruby.exe")) {
    $env:Path = "$rubyBinPath;$env:Path"
  }
}

function Test-BundlerAvailable {
  & ruby -S bundle --version *> $null
  return $LASTEXITCODE -eq 0
}

function Set-LocalBundlerEnvironment {
  $bundleDirectory = Join-Path $projectRoot ".bundle"
  $vendorBundleDirectory = Join-Path $projectRoot "vendor\bundle"
  $env:BUNDLE_USER_HOME = $bundleDirectory
  $env:BUNDLE_APP_CONFIG = $bundleDirectory
  $env:BUNDLE_PATH = $vendorBundleDirectory
}

$projectRoot = Split-Path -Parent $PSScriptRoot
& (Join-Path $PSScriptRoot "Validate-Articles.ps1")

Set-Location -LiteralPath $projectRoot
Add-RubyInstallerPath
Set-LocalBundlerEnvironment

if ((Test-Path -LiteralPath (Join-Path $projectRoot "Gemfile")) -and (Get-Command "ruby" -ErrorAction SilentlyContinue) -and (Test-BundlerAvailable)) {
  Write-Host "Lokale Vorschau startet unter http://127.0.0.1:4000/Zauberhaft/"
  & ruby -S bundle exec jekyll serve --livereload --host 127.0.0.1 --port 4000
  exit $LASTEXITCODE
}

Write-Host "Jekyll ist lokal nicht verf${kleinesUe}gbar." -ForegroundColor Red
Write-Host "Installiere zuerst Ruby, Bundler und die Projektabh${kleinesAe}ngigkeiten mit JekyllInstallieren.bat." -ForegroundColor Yellow
Write-Host "Danach kann die lokale Vorschau mit WebStarten.bat erneut gestartet werden." -ForegroundColor Yellow
exit 1
