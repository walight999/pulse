# Troubleshooting pulse

Top 10 issues with fixes. If your problem isn't here, search [GitHub Issues](https://github.com/walight999/pulse/issues) or open a new one.

---

## 1. Windows Defender or SmartScreen blocks the installer

**Symptom:** "Windows protected your PC" dialog when running `pulse-setup-<version>.exe`, OR Defender quarantines the file immediately.

**Why:** New Windows apps need to build SmartScreen reputation. Even signed apps see this warning until they accumulate ~3,000 installs.

**Fix:**
1. Click **More info** in the dialog
2. Click **Run anyway**
3. (If quarantined) Windows Security → Virus & threat protection → Protection history → find `pulse-setup-<version>.exe` → **Allow on device**

**Bonus:** If you want to verify the binary before running:
- Compare its SHA-256 against the hash published in the GitHub Release notes
- Or check the digital signature: right-click the `.exe` → Properties → Digital Signatures tab

---

## 2. Tray icon missing after launch

**Symptom:** pulse appears to start (no error window), but the system-tray icon never shows up. Or dashboard opens but tray is gone.

**Common causes + fixes:**

- **Tray collapsed into "hidden icons"** — click the `^` chevron in the taskbar to expand. Drag the pulse icon out to the visible tray.
- **pulse.exe died after launching** — open Task Manager (Ctrl+Shift+Esc) → Details tab → search `pulse.exe`. If it's not there, check `%USERPROFILE%\pulse\logs\` for the latest log.
- **Port conflict** — another app is using Streamlit's port. See issue #5 below.
- **First-launch indexing** — on very large `~/.claude/projects/` directories (10K+ files), the first scan can take 30+ seconds before the tray shows up. Wait, or check the log file.

**Verify the process is healthy:**

```powershell
Get-Process pulse -ErrorAction SilentlyContinue
```

If the process exists but no tray icon → likely Windows tray bug. Restart Windows Explorer:

```powershell
Stop-Process -Name explorer -Force; Start-Process explorer
```

---

## 3. "No Claude data found" — Claude usage tab is empty

**Symptom:** AI usage page shows zero tokens / no projects despite using Claude Code regularly.

**Why:** pulse reads `~/.claude/projects/*.jsonl` (one folder per project). On Windows that path is `%USERPROFILE%\.claude\projects\`. If you've never used Claude Code OR your install put logs elsewhere, the directory is empty.

**Fix:**

```powershell
# Verify Claude Code logs exist
Test-Path "$env:USERPROFILE\.claude\projects"
# Expected: True

# List recent log activity
Get-ChildItem "$env:USERPROFILE\.claude\projects" -Recurse -Filter *.jsonl |
  Sort-Object LastWriteTime -Descending |
  Select-Object -First 5 FullName, LastWriteTime, Length
```

If `False` or empty:
- Install [Claude Code](https://docs.anthropic.com/claude/code) and use it for at least one session
- Or run pulse with sample data — Settings → "Show me pulse with sample data" toggle (coming v1.0.1)

If you store Claude logs elsewhere, you can override the path in Settings → Preferences → "Claude log directory".

---

## 4. FX rates show as "—" or stuck on yesterday's value

**Symptom:** Multi-currency conversions broken, or rates haven't updated in over 24 hours.

**Why:** pulse calls `https://api.frankfurter.dev/v1/latest` once per 24h. If the call fails (network down, frankfurter outage, firewall block), pulse falls back to the cached `data/fx_cache.json`.

**Fix:**

```powershell
# Test connection
Invoke-WebRequest https://api.frankfurter.dev/v1/latest | Select-Object StatusCode

# Force a fresh fetch (delete cache)
Remove-Item "$env:USERPROFILE\pulse\data\fx_cache.json" -ErrorAction SilentlyContinue
```

Then restart pulse. The first dashboard load will hit `frankfurter.dev` and cache a fresh rate.

If your network blocks `api.frankfurter.dev`:
- Set a different FX source (Settings → Preferences → "FX provider" — coming v1.1)
- Or disable currency conversion (Settings → set display currency to your local currency only)

---

## 5. "Address already in use" — Streamlit port conflict

**Symptom:** Tray icon shows but clicking it doesn't open the dashboard. Or error in `%USERPROFILE%\pulse\logs\` mentions port 8501 / 8502.

**Why:** Another Streamlit app or local server is using pulse's port.

**Fix:**

```powershell
# Find what's on port 8501
Get-NetTCPConnection -LocalPort 8501 -ErrorAction SilentlyContinue |
  Select-Object LocalAddress, LocalPort, OwningProcess
# Optionally kill it
Stop-Process -Id <PID-from-above> -Force
```

Or change pulse's port via env var:

```powershell
$env:PULSE_PORT = "8590"
& "C:\Program Files\pulse\pulse.exe"
```

To make it permanent: System Properties → Environment Variables → User → New → Variable name `PULSE_PORT`, value `8590`.

---

## 6. SQLite locked / "database is locked" error

**Symptom:** Saving subscriptions fails, or dashboard hangs with `OperationalError: database is locked` in the logs.

**Why:** Two pulse processes are running at once and fighting over `tracker.db`. (Pulse uses a single-instance socket lock but on rare crashes it can be bypassed.)

**Fix:**

```powershell
# Kill all pulse processes
Get-Process pulse -ErrorAction SilentlyContinue | Stop-Process -Force

# Restart cleanly
& "C:\Program Files\pulse\pulse.exe"
```

If the lock persists after restart:

```powershell
# Check no stale lock file
Remove-Item "$env:USERPROFILE\pulse\data\tracker.db-shm" -ErrorAction SilentlyContinue
Remove-Item "$env:USERPROFILE\pulse\data\tracker.db-wal" -ErrorAction SilentlyContinue
```

If your DB is corrupted (very rare), restore from `%USERPROFILE%\pulse\backups\` — there are up to 7 daily snapshots.

---

## 7. Backup not created — `backups/` folder is empty

**Symptom:** No `.db.gz` files in `%USERPROFILE%\pulse\backups\` after multiple days of use.

**Why:** Either pulse can't write to that folder (permissions), or you've never hit the 24h backup interval (background daemon runs once a day).

**Fix:**

```powershell
# Verify permissions
$path = "$env:USERPROFILE\pulse\backups"
icacls $path
# You should see "Allow" for your user with "(F)" full control

# Manually trigger a backup (Settings → Data & backup → "Backup now")
```

If permissions are wrong: right-click the folder → Properties → Security → grant your user Full Control.

---

## 8. Activity tracking stuck on "idle" or single app

**Symptom:** App usage list never updates. Always shows one app or all "Idle".

**Why:** pulse uses Win32 API `GetForegroundWindow` + `GetLastInputInfo`. Some PC management software (corporate antivirus, kiosk mode, screen recorders) blocks these APIs.

**Fix:**

```powershell
# Check pulse is allowed to read foreground state
# (this requires admin in some setups)
Get-WinEvent -LogName Security -MaxEvents 10 |
  Where-Object { $_.Message -like "*pulse*" }
```

If you're in a corporate environment, ask IT to allow `pulse.exe` to read foreground window state. There's no escalation involved — it's the same API Task Manager uses.

For users on Focus Assist / Do Not Disturb mode: foreground tracking still works, but pulse's notifications won't fire until you exit DnD.

---

## 9. Theme not switching, or stuck in dark mode

**Symptom:** Sidebar theme toggle does nothing, or the dashboard renders half-light / half-dark.

**Why:** Streamlit caches CSS. Switching themes flushes the cache, but some browsers (Edge in particular) cache CSS at the network layer too.

**Fix:**

1. Hit **Ctrl+Shift+R** (hard refresh) on the dashboard tab
2. Or close the tab and re-open via tray icon
3. Or restart pulse entirely

If the issue persists:

```powershell
# Clear Streamlit cache
Remove-Item "$env:USERPROFILE\.streamlit\config.toml" -ErrorAction SilentlyContinue

# Restart pulse
Get-Process pulse | Stop-Process -Force
& "C:\Program Files\pulse\pulse.exe"
```

---

## 10. Update failed / can't upgrade

**Symptom:** Auto-update notification appeared, but the new version doesn't install. Or running the new installer over the old one fails.

**Why:** Either the old `pulse.exe` is still running (file lock), or a permission issue blocks the installer.

**Fix:**

1. Right-click the tray icon → **Quit pulse**
2. Verify in Task Manager that no `pulse.exe` process remains
3. Re-run the new installer

If the installer still fails:

```powershell
# Uninstall the old version cleanly
$uninst = "C:\Program Files\pulse\unins000.exe"
Start-Process $uninst -ArgumentList "/SILENT" -Wait

# Install fresh
Start-Process "pulse-setup-<new-version>.exe"
```

Your data in `%USERPROFILE%\pulse\` is preserved across uninstall + reinstall (only the binary is replaced).

---

## Still stuck?

1. Check `%USERPROFILE%\pulse\logs\pulse-<date>.log` for the actual error
2. Search [GitHub Issues](https://github.com/walight999/pulse/issues?q=is%3Aissue) for similar reports
3. Open a [new bug report](https://github.com/walight999/pulse/issues/new?template=bug_report.md) with:
   - Your Windows version (`winver`)
   - The exact error from the log
   - Steps to reproduce
   - Screenshots if UI-related
4. For security issues: **do not file a public issue** — email [security@mintforai.com](mailto:security@mintforai.com) instead

---

## Reset everything

If pulse is broken beyond repair and you want a fresh start:

```powershell
# 1. Kill pulse
Get-Process pulse -ErrorAction SilentlyContinue | Stop-Process -Force

# 2. Backup your data (optional but recommended)
Compress-Archive -Path "$env:USERPROFILE\pulse" -DestinationPath "$env:USERPROFILE\pulse-backup-$(Get-Date -Format yyyy-MM-dd).zip"

# 3. Nuke everything
Remove-Item "$env:USERPROFILE\pulse" -Recurse -Force
Remove-Item "$env:USERPROFILE\.streamlit" -Recurse -Force -ErrorAction SilentlyContinue

# 4. Reinstall + start fresh
Start-Process "pulse-setup-<version>.exe"
```

Your subscription list, AI usage history, and settings will all be reset — but you have a `.zip` backup if you change your mind.
