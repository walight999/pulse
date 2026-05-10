# Create a Desktop shortcut for Life Tracker — right-click to "Pin to taskbar"
$ErrorActionPreference = "Stop"

$projectDir   = Split-Path -Parent $PSScriptRoot
$pythonDir    = Split-Path -Parent (Get-Command python).Source
$pythonwExe   = Join-Path $pythonDir "pythonw.exe"
if (-not (Test-Path $pythonwExe)) {
    $pythonwExe = (Get-Command python).Source
}
$appScript    = Join-Path $projectDir "app.py"

$desktop      = [Environment]::GetFolderPath("Desktop")
$shortcutPath = Join-Path $desktop "Life Tracker.lnk"

# Generate an .ico file from the app icon for the shortcut
$iconPath = Join-Path $projectDir "data\app_icon.ico"
$pyGenIcon = @"
from PIL import Image, ImageDraw

def make_icon(size):
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    pad = max(int(size * 0.06), 1)
    d.rounded_rectangle((pad, pad, size - pad, size - pad),
                        radius=int(size * 0.22), fill=(15, 23, 42, 255))
    cw, ch = size * 0.50, size * 0.30
    bx, by = size * 0.22, size * 0.36
    r = max(int(size * 0.06), 2)
    d.rounded_rectangle((bx + size*0.10, by - size*0.10,
                         bx + size*0.10 + cw, by - size*0.10 + ch),
                        radius=r, fill=(168, 85, 247, 200))
    d.rounded_rectangle((bx + size*0.05, by - size*0.05,
                         bx + size*0.05 + cw, by - size*0.05 + ch),
                        radius=r, fill=(59, 130, 246, 230))
    d.rounded_rectangle((bx, by, bx + cw, by + ch),
                        radius=r, fill=(34, 197, 94, 255))
    cx, cy = bx + cw / 2, by + ch / 2
    stroke = max(int(size * 0.07), 2)
    d.line([(cx - cw*0.22, cy + ch*0.02),
            (cx - cw*0.05, cy + ch*0.22),
            (cx + cw*0.26, cy - ch*0.22)],
           fill=(255, 255, 255, 255), width=stroke, joint='curve')
    return img

# Generate at 256, save as multi-size ICO
img = make_icon(256)
img.save(r'$iconPath', format='ICO',
         sizes=[(16,16),(32,32),(48,48),(64,64),(128,128),(256,256)])
print('icon written')
"@
& (Get-Command python).Source -c $pyGenIcon

$wsh = New-Object -ComObject WScript.Shell
$sc  = $wsh.CreateShortcut($shortcutPath)
$sc.TargetPath       = $pythonwExe
$sc.Arguments        = "`"$appScript`""
$sc.WorkingDirectory = $projectDir
$sc.IconLocation     = "$iconPath,0"
$sc.Description      = "Life Tracker - apps, subscriptions, tokens"
$sc.WindowStyle      = 7  # minimized
$sc.Save()

Write-Host "Shortcut created: $shortcutPath"
Write-Host 'To pin to taskbar: launch it once, then right-click the taskbar icon -> Pin to taskbar'
