@echo off
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0tools\Install-Jekyll.ps1"
exit /b %ERRORLEVEL%
