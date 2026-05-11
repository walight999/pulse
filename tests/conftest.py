"""pytest config — fixtures + path setup so tests can import Pulse modules.

Run with: pytest -q tests/

These tests are intentionally minimal and CI-tolerant. The goal is to catch
regressions in pure-Python logic without requiring a Streamlit session or a
live SQLite DB on disk.
"""
import sys
from pathlib import Path

# Make project root importable as if running from repo root
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
