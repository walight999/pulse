# Start the background tracker (foreground console — closes on Ctrl+C)
$projectDir = Split-Path -Parent $PSScriptRoot
Set-Location $projectDir
python tracker.py
