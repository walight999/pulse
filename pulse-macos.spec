# PyInstaller spec — packages pulse into a macOS .app bundle
#
# Build (on macOS):
#   pip install pyinstaller pillow rumps
#   pyinstaller pulse-macos.spec
# Output: dist/pulse.app  (open with `open dist/pulse.app` or drag to /Applications)
#
# Codesigning (optional, requires Apple Developer account):
#   codesign --deep --force --options runtime --sign "Developer ID Application: White (XXXXXXXXXX)" dist/pulse.app
#   xcrun notarytool submit dist/pulse.app.zip --apple-id ... --team-id ... --password ... --wait
#
# Without codesigning, users must right-click → Open the first time (Gatekeeper warning).

from pathlib import Path

PROJECT_ROOT = Path(".").resolve()

block_cipher = None

datas = [
    (str(PROJECT_ROOT / ".streamlit"), ".streamlit"),
    (str(PROJECT_ROOT / "static"), "static"),
    (str(PROJECT_ROOT / "dashboard.py"), "."),
    (str(PROJECT_ROOT / "theme.py"), "."),
    (str(PROJECT_ROOT / "db.py"), "."),
    (str(PROJECT_ROOT / "fx.py"), "."),
    (str(PROJECT_ROOT / "quips.py"), "."),
    (str(PROJECT_ROOT / "sync_tokens.py"), "."),
    (str(PROJECT_ROOT / "tracker.py"), "."),
    (str(PROJECT_ROOT / "alerts.py"), "."),
    (str(PROJECT_ROOT / "backup.py"), "."),
    (str(PROJECT_ROOT / "notifications.py"), "."),
    (str(PROJECT_ROOT / "categories.py"), "."),
    (str(PROJECT_ROOT / "ics_export.py"), "."),
    (str(PROJECT_ROOT / "idle.py"), "."),
    (str(PROJECT_ROOT / "export.py"), "."),
    (str(PROJECT_ROOT / "platform_compat.py"), "."),
    (str(PROJECT_ROOT / "account.py"), "."),
    (str(PROJECT_ROOT / "waitlist.py"), "."),
    (str(PROJECT_ROOT / "referrals.py"), "."),
    (str(PROJECT_ROOT / "telemetry.py"), "."),
    (str(PROJECT_ROOT / "discover_subscriptions.py"), "."),
    (str(PROJECT_ROOT / "cloud"), "cloud"),
    (str(PROJECT_ROOT / "providers"), "providers"),
    (str(PROJECT_ROOT / "integrations"), "integrations"),
    (str(PROJECT_ROOT / "assistant"), "assistant"),
    (str(PROJECT_ROOT / "api"), "api"),
    (str(PROJECT_ROOT / "sdk"), "sdk"),
]

hiddenimports = [
    "streamlit",
    "streamlit.runtime",
    "streamlit.runtime.scriptrunner",
    "pandas",
    "plotly",
    "plotly.graph_objects",
    "psutil",
    "PIL",
    "PIL.Image",
    "sqlite3",
    # macOS-specific: rumps for menu-bar app (preferred over pystray on Mac)
    "rumps",
    "Foundation",
    "AppKit",
    "objc",
]

a = Analysis(
    ["app.py"],
    pathex=[str(PROJECT_ROOT)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=["tkinter", "matplotlib", "scipy"],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="pulse",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,                  # UPX breaks macOS notarization
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=True,        # required for menubar apps
    target_arch="universal2",   # both x86_64 and arm64
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    name="pulse",
)

# .app bundle wrapper
app = BUNDLE(
    coll,
    name="pulse.app",
    icon=str(PROJECT_ROOT / "static" / "brand" / "app-icon.png"),
    bundle_identifier="com.walight999.pulse",
    info_plist={
        "CFBundleName": "pulse",
        "CFBundleDisplayName": "pulse",
        "CFBundleShortVersionString": "1.5.0",
        "CFBundleVersion": "1.5.0",
        "CFBundleIdentifier": "com.walight999.pulse",
        "CFBundleExecutable": "pulse",
        "CFBundlePackageType": "APPL",
        "CFBundleSignature": "????",
        "LSMinimumSystemVersion": "12.0",
        "LSUIElement": True,         # menubar-only — no Dock icon
        "NSHighResolutionCapable": True,
        "NSHumanReadableCopyright": "Copyright (c) 2026 White. MIT Licensed.",
        "NSAppleEventsUsageDescription": "pulse uses AppleScript to detect the active app for productivity tracking.",
        "NSDesktopFolderUsageDescription": "pulse may save backups to your Desktop on request.",
    },
)
