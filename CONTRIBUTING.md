# Contributing to Pulse

Thanks for considering a contribution! Pulse aims to be the best personal-finance
dashboard for the AI era. Every line of code that gets us there is welcome.

## Code of conduct

Be kind, be specific, be useful. Discriminatory or abusive contributions are removed.

## How to contribute

### Bug reports

Open an issue with:
- What you expected
- What happened
- Steps to reproduce
- Your platform (Windows version, Python version)
- Screenshots if visual

### Feature requests

Open an issue tagged `feature` with:
- The user problem (not the solution)
- Who benefits and how
- Any prior art (links to similar features elsewhere)

### Pull requests

1. Fork the repo, create a topic branch from `main`
2. Make focused commits (one change per commit)
3. Run `python -c "import ast; ast.parse(open('dashboard.py').read())"` for syntax check
4. Update CHANGELOG.md if user-visible
5. Submit PR with description of *why* (the *what* is in the diff)

We're a small team — please keep PRs focused. Bigger refactors should be
discussed in an issue first.

## Priority contribution areas

- **macOS port** — `platform_compat.py` has scaffolding; needs real testing on a Mac
- **Linux port** — same; X11 + Wayland both ideally
- **Additional provider parsers** in `providers/` — see existing files for the pattern
- **Subscription detection heuristics** for non-English emails (TH, JP, ES, DE)
- **Theme variants** — minimal, high-contrast, system-following
- **Translations** — Streamlit doesn't natively i18n; we'd accept a layer

## Development setup

```bash
git clone https://github.com/walight999/pulse
cd pulse
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
# Optional for cloud features:
pip install -r requirements-cloud.txt

# Run dashboard (headless dev — no tray)
streamlit run dashboard.py
```

Open http://localhost:8501.

## Architecture

See `README.md` "Architecture" section for the module layout.

Key design rules:
1. **Local-first**: never require cloud for core features
2. **Theme-aware**: all CSS uses `var(--*)` from `theme.py`
3. **Cross-platform-safe**: imports of `ctypes.windll.*` only on Windows
4. **Pure functions where possible**: easier to test, easier to reason about
5. **Schema migrations**: idempotent only, never destructive (see `db.py:MIGRATIONS`)

## Testing

Pulse has no formal test suite yet (priority issue). For now:
- Manual: install, run, click around
- Syntax: `python -c "import ast; ast.parse(open('dashboard.py').read())"`
- Lint: `ruff check` if you have it

Help us add pytest coverage — high-impact starter task.

## Code style

- Python: 4-space indent, type hints encouraged, docstrings on non-trivial functions
- CSS: variables for all colors, prefer flex over float, no `!important` unless necessary
- HTML: minimal — most dynamic markup is `f-string`s in Python
- JS (browser extension): MV3, no transpilation, vanilla
- Comments: explain *why*, not *what*. The code says what.

## License

By contributing, you agree your code is released under MIT (see `LICENSE`).

## Recognition

Contributors with merged PRs get:
- Listed in CHANGELOG.md
- Free Pulse Pro for 1 year when Pro launches (Phase 2)
- A shoutout in our launch posts
