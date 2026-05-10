# Build a standalone Pulse.exe so end users don't need Python installed.
# Run once on a machine with Python + pip + PyInstaller.
# Output: dist/Pulse/Pulse.exe (with all deps bundled)

$ErrorActionPreference = "Stop"
$projectDir = Split-Path -Parent $PSScriptRoot
Set-Location $projectDir

Write-Host "Installing PyInstaller..."
pip install --quiet pyinstaller

Write-Host "Cleaning previous build..."
Remove-Item -Recurse -Force build, dist -ErrorAction SilentlyContinue
Remove-Item -Force *.spec -ErrorAction SilentlyContinue

Write-Host "Building Pulse.exe..."
# --onedir is more reliable than --onefile for Streamlit (data files, multiprocess)
# --noconsole hides the console window (we use system tray instead)
# --add-data includes Streamlit assets and our static files
pyinstaller `
    --name Pulse `
    --noconsole `
    --add-data "data;data" `
    --add-data ".streamlit;.streamlit" `
    --hidden-import streamlit.runtime.scriptrunner.magic_funcs `
    --hidden-import streamlit.web.cli `
    --hidden-import psutil `
    --hidden-import pystray._win32 `
    --collect-data streamlit `
    --collect-data plotly `
    app.py

if (Test-Path "dist\Pulse\Pulse.exe") {
    Write-Host ""
    Write-Host "Built: dist\Pulse\Pulse.exe"
    Write-Host "Size: $([Math]::Round((Get-ChildItem dist\Pulse -Recurse | Measure-Object Length -Sum).Sum / 1MB, 1)) MB"
    Write-Host ""
    Write-Host "Distribute the entire dist\Pulse\ folder. Users double-click Pulse.exe — no Python needed."
} else {
    Write-Host "Build failed — see PyInstaller output above"
    exit 1
}
