#!/usr/bin/env bash
# ============================================================================
# Build pulse for macOS (.app bundle)
# Run on macOS only. Apple Silicon + Intel both supported (universal2).
# ============================================================================
set -euo pipefail

cd "$(dirname "$0")/.."

# Verify we're on macOS
if [[ "$(uname -s)" != "Darwin" ]]; then
    echo "build_macos.sh must run on macOS"
    exit 1
fi

# Verify Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
if [[ "$PYTHON_VERSION" < "3.12" ]]; then
    echo "Python 3.12+ required, got $PYTHON_VERSION"
    exit 1
fi

echo "==> Installing dependencies"
pip install -r requirements.txt pyinstaller pillow rumps

echo "==> Building pulse.app"
pyinstaller --clean pulse-macos.spec

if [[ ! -d "dist/pulse.app" ]]; then
    echo "Build failed — dist/pulse.app not found"
    exit 1
fi

echo "==> Codesign (optional — if Apple Developer ID configured)"
if [[ -n "${APPLE_DEVELOPER_ID:-}" ]]; then
    codesign --deep --force --options runtime \
        --sign "Developer ID Application: $APPLE_DEVELOPER_ID" \
        dist/pulse.app
    echo "Codesigned with $APPLE_DEVELOPER_ID"
else
    echo "(skipping codesign — set APPLE_DEVELOPER_ID env var to enable)"
fi

echo "==> Creating .zip for distribution"
cd dist
ditto -c -k --keepParent pulse.app pulse-macos-1.5.0.zip
cd ..

echo
echo "============================================================================"
echo "Done."
echo "  App:  dist/pulse.app"
echo "  Zip:  dist/pulse-macos-1.5.0.zip"
echo
echo "Test: open dist/pulse.app"
echo
echo "Notarize (requires Apple Developer account):"
echo "  xcrun notarytool submit dist/pulse-macos-1.5.0.zip \\"
echo "    --apple-id YOUR_APPLE_ID --team-id YOUR_TEAM_ID \\"
echo "    --password YOUR_APP_SPECIFIC_PASSWORD --wait"
echo "============================================================================"
