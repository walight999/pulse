# Install Life Tracker as a Windows Scheduled Task — runs at user logon.
# Launches app.py (system tray) which manages tracker.py + dashboard internally.
$ErrorActionPreference = "Stop"

$taskName     = "LifeTracker"
$projectDir   = Split-Path -Parent $PSScriptRoot
$pythonDir    = Split-Path -Parent (Get-Command python).Source
$pythonwExe   = Join-Path $pythonDir "pythonw.exe"
if (-not (Test-Path $pythonwExe)) {
    $pythonwExe = (Get-Command python).Source
}
$appScript = Join-Path $projectDir "app.py"

$action    = New-ScheduledTaskAction -Execute $pythonwExe -Argument "`"$appScript`"" -WorkingDirectory $projectDir
$trigger   = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME
# Small delay so the desktop is ready when the tray icon appears
$trigger.Delay = "PT15S"
$settings  = New-ScheduledTaskSettingsSet `
                -StartWhenAvailable `
                -DontStopOnIdleEnd `
                -ExecutionTimeLimit (New-TimeSpan -Days 0) `
                -RestartCount 3 `
                -RestartInterval (New-TimeSpan -Minutes 5) `
                -MultipleInstances IgnoreNew
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited

Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Description "Life Tracker — system tray app + background tracker" | Out-Null

Write-Host "Installed scheduled task: $taskName"
Write-Host "Auto-starts at next logon (15s delay). To start now:"
Write-Host "  Start-ScheduledTask -TaskName LifeTracker"
Write-Host "To stop:"
Write-Host "  Stop-ScheduledTask -TaskName LifeTracker"
Write-Host "To remove:"
Write-Host '  Unregister-ScheduledTask -TaskName LifeTracker -Confirm:$false'
