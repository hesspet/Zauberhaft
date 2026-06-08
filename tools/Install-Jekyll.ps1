$ErrorActionPreference = "Stop"
$kleinesAe = [char]0x00E4
$kleinesOe = [char]0x00F6
$kleinesUe = [char]0x00FC

$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $projectRoot

function Add-RubyInstallerPath {
  $rubyBinPath = "C:\Ruby33-x64\bin"
  if (Test-Path -LiteralPath (Join-Path $rubyBinPath "ruby.exe")) {
    $env:Path = "$rubyBinPath;$env:Path"
  }
}

function Test-CommandAvailable {
  param([string]$CommandName)

  return $null -ne (Get-Command $CommandName -ErrorAction SilentlyContinue)
}

function Set-LocalBundlerEnvironment {
  $bundleDirectory = Join-Path $projectRoot ".bundle"
  $vendorBundleDirectory = Join-Path $projectRoot "vendor\bundle"
  $env:BUNDLE_USER_HOME = $bundleDirectory
  $env:BUNDLE_APP_CONFIG = $bundleDirectory
  $env:BUNDLE_PATH = $vendorBundleDirectory
}

Add-RubyInstallerPath
Set-LocalBundlerEnvironment

if (-not (Test-CommandAvailable -CommandName "ruby")) {
  Write-Host "Ruby ist lokal nicht verf${kleinesUe}gbar." -ForegroundColor Red
  Write-Host "Installiere RubyInstaller mit DevKit, zum Beispiel:" -ForegroundColor Yellow
  Write-Host "winget install RubyInstallerTeam.RubyWithDevKit.3.3" -ForegroundColor Yellow
  Write-Host "${kleinesOe}ffne danach ein neues Terminal und starte JekyllInstallieren.bat erneut." -ForegroundColor Yellow
  exit 1
}

Write-Host "Ruby gefunden:"
& ruby --version

if (-not (Test-CommandAvailable -CommandName "gem")) {
  Write-Host "RubyGems ist lokal nicht verf${kleinesUe}gbar. Pr${kleinesUe}fe die RubyInstaller-Installation." -ForegroundColor Red
  exit 1
}

& ruby -S bundle --version *> $null
if ($LASTEXITCODE -ne 0) {
  Write-Host "Bundler ist lokal nicht verf${kleinesUe}gbar. Bundler wird installiert."
  & ruby -S gem install bundler
  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }
}

Write-Host "Bundler gefunden:"
& ruby -S bundle --version

if (-not (Test-Path -LiteralPath (Join-Path $projectRoot "Gemfile"))) {
  Write-Host "Gemfile fehlt im Projektstamm: $projectRoot" -ForegroundColor Red
  exit 1
}

Write-Host "Lokaler Bundle-Pfad wird auf vendor/bundle gesetzt."
& ruby -S bundle config set --local path "vendor/bundle"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host "Projektabh${kleinesAe}ngigkeiten werden installiert."
& ruby -S bundle install
exit $LASTEXITCODE
