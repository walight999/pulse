# PyInstaller spec — packages pulse into a single .exe for Windows
#
# Build: pyinstaller pulse.spec
# Output: dist/pulse.exe (single-file, no console window)
#
# Requires: pip install pyinstaller

from pathlib import Path

PROJECT_ROOT = Path(".").resolve()

block_cipher = None

# Data files to bundle alongside the .exe
datas = [
    # Streamlit needs its config.toml and static assets
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
    # Modules (need Python recursion)
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
    "pystray",
    "PIL",
    "PIL.Image",
    "sqlite3",
]

a = Analysis(
    ["app.py"],
    pathex=[str(PROJECT_ROOT)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "tkinter",
        "matplotlib",
        "scipy",
        "PyQt5",
        "PyQt6",
        "PySide2",
        "PySide6",
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="pulse",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,                 # no DOS box — tray-only
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(PROJECT_ROOT / "static" / "brand" / "app-icon.png"),
    version=None,
)
