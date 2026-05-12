# Install pulse

Three ways to install. Pick the path that matches your setup.

---

## 🪟 Windows — recommended (5 minutes)

### Option A: Installer (.exe wizard)

1. Go to [github.com/walight999/pulse/releases/latest](https://github.com/walight999/pulse/releases/latest)
2. Download **`pulse-setup-<version>.exe`**
3. Double-click → follow the installer
   - Choose install directory (default `C:\Program Files\pulse\`)
   - Pick whether to add a desktop shortcut
   - Choose whether to auto-launch at Windows startup
4. Click **Finish** — pulse launches automatically and appears in your system tray (lower-right of the taskbar)
5. Click the tray icon to open the dashboard in your browser

> First run: 30-second wizard asks for currency, monthly AI budget, and alert preferences. All skippable.

### Option B: Portable .zip

If you don't want to install (e.g. work computer, USB drive use):

1. Download **`pulse-<version>-windows-portable.zip`** from the same releases page
2. Unzip anywhere (e.g. `D:\pulse\`)
3. Double-click `pulse.exe`
4. (No system-tray persistence, no auto-start — runs only while you keep it open)

### Verification

- The tray icon appears 1-3 seconds after launch (small dot with mint accent)
- Dashboard opens in your default browser at `http://localhost:<random-port>`
- The first dashboard page shows "Welcome" or the demo overview

If anything doesn't work as expected, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

---

## 🍎 macOS — coming Q3 2026

The cross-platform shim (`platform_compat.py`) is already in the repo and handles macOS APIs for foreground app detection, idle time, and notifications. A native `.app` bundle (universal2 — Apple Silicon + Intel) will ship once we have:

1. Apple Developer ID certificate ($99/yr)
2. Notarization workflow
3. Beta testers on macOS 12+

Meanwhile, macOS users can run from source (see below).

[Join the macOS waitlist →](https://mintforai.com/#waitlist)

---

## 🐧 Linux — coming Q4 2026

Like macOS, the cross-platform shim handles X11 + Wayland foreground detection via `xdotool` / `wmctrl`. AppImage or Flatpak ships once we have community testers.

Run from source today.

---

## 🛠️ From source (any platform — for developers)

### Prerequisites

- **Python 3.12+** ([download](https://python.org))
- **git** ([download](https://git-scm.com))
- ~500MB free disk for dependencies

### Clone + run

```bash
git clone https://github.com/walight999/pulse
cd pulse
pip install -r requirements.txt
python app.py
```

That's it. `app.py` boots the system tray, starts the Streamlit dashboard, and opens your browser.

### Optional: cloud sync dependencies (Pro tier development)

```bash
pip install -r requirements-cloud.txt
```

Adds `supabase`, `cryptography`, `argon2-cffi` for the encrypted sync engine. Not needed for the free local app.

### Development setup

```bash
# Run tests
pytest -q tests/

# Run the Streamlit dashboard directly (without tray)
streamlit run dashboard.py

# Lint (advisory)
ruff check . --select E9,F63,F7,F82
```

### Build a Windows binary locally

```bash
pip install pyinstaller pillow
pyinstaller --clean pulse.spec
# Output: dist\pulse\pulse.exe
```

To build the installer (requires [Inno Setup](https://jrsoftware.org/isinfo.php) installed):

```bash
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" scripts\installer.iss
# Output: scripts\Output\pulse-setup-<version>.exe
```

### Build a macOS .app locally (macOS only)

```bash
chmod +x scripts/build_macos.sh
./scripts/build_macos.sh
# Output: dist/pulse.app
```

---

## 🔐 Code signing notes

The official binaries on the Releases page are signed with the project's code signing certificate once available. Windows SmartScreen builds reputation over time — first-time downloads may see a "Windows protected your PC" warning. Click **More info** → **Run anyway** to proceed. The warning disappears after enough installs.

If you build from source or use the portable .zip, your binary is unsigned and may trigger SmartScreen or Windows Defender. See [TROUBLESHOOTING.md § Windows Defender block](TROUBLESHOOTING.md#1-windows-defender-or-smartscreen-blocks-the-installer) for details.

---

## 📦 What gets installed

| Location | What |
|---|---|
| `C:\Program Files\pulse\` (default) | The `pulse.exe` binary + supporting DLLs + brand assets |
| `%USERPROFILE%\pulse\data\` | Your SQLite database, FX rate cache, waitlist + telemetry files |
| `%USERPROFILE%\pulse\logs\` | Diagnostic logs (rotated, last 30 days) |
| `%USERPROFILE%\pulse\backups\` | Auto-rotated SQLite backups (last 7 days) |
| `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` | Auto-start entry (only if you opted in) |

No registry keys outside `HKCU`. No services. No drivers. No admin install required.

---

## 🗑️ Uninstall

### Windows installer

Settings → Apps → installed apps → **pulse** → Uninstall.

The uninstaller asks: "Keep your pulse data?"
- **Yes** — removes the binary, keeps `%USERPROFILE%\pulse\` (subscriptions, AI usage, settings preserved)
- **No** — deletes everything including your local data

### Portable .zip

Delete the folder you unzipped to. Optionally also delete `%USERPROFILE%\pulse\` to remove data.

### From source

Delete the cloned repo. Optionally also delete `%USERPROFILE%\pulse\` to remove data.

---

## 🆘 Need help?

- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) — top 10 issues with fixes
- [GitHub Discussions](https://github.com/walight999/pulse/discussions) — questions
- [GitHub Issues](https://github.com/walight999/pulse/issues) — bug reports
- [hi@mintforai.com](mailto:hi@mintforai.com) — anything else
