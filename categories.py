"""App categorization — auto-classify processes by name with manual overrides."""
from __future__ import annotations

from db import get_conn

# Default category mapping (lowercase process name substrings).
# Order matters — first match wins.
DEFAULT_RULES: list[tuple[str, str, bool]] = [
    # (substring, category, is_distraction)
    ("cursor",         "Dev tools",     False),
    ("code.exe",       "Dev tools",     False),  # VS Code
    ("vscode",         "Dev tools",     False),
    ("idea",           "Dev tools",     False),  # JetBrains IntelliJ/PyCharm/etc
    ("pycharm",        "Dev tools",     False),
    ("webstorm",       "Dev tools",     False),
    ("rider",          "Dev tools",     False),
    ("sublime",        "Dev tools",     False),
    ("notepad++",      "Dev tools",     False),
    ("windsurf",       "Dev tools",     False),
    ("zed",            "Dev tools",     False),
    ("docker",         "Dev tools",     False),
    ("git",            "Dev tools",     False),

    ("windowsterminal","Terminal",      False),
    ("powershell",     "Terminal",      False),
    ("cmd.exe",        "Terminal",      False),
    ("wsl",            "Terminal",      False),
    ("bash",           "Terminal",      False),

    ("claude",         "AI tools",      False),
    ("chatgpt",        "AI tools",      False),
    ("perplexity",     "AI tools",      False),
    ("copilot",        "AI tools",      False),

    ("chrome",         "Browser",       False),
    ("msedge",         "Browser",       False),
    ("edge.exe",       "Browser",       False),
    ("firefox",        "Browser",       False),
    ("brave",          "Browser",       False),
    ("opera",          "Browser",       False),
    ("safari",         "Browser",       False),
    ("arc.exe",        "Browser",       False),

    ("excel",          "Productivity",  False),
    ("winword",        "Productivity",  False),
    ("powerpnt",       "Productivity",  False),
    ("outlook",        "Productivity",  False),
    ("onenote",        "Productivity",  False),
    ("notion",         "Productivity",  False),
    ("obsidian",       "Productivity",  False),
    ("anki",           "Productivity",  False),

    ("slack",          "Communication", False),
    ("teams",          "Communication", False),
    ("discord",        "Communication", True),
    ("line",           "Communication", False),
    ("telegram",       "Communication", False),
    ("whatsapp",       "Communication", False),
    ("zoom",           "Communication", False),
    ("skype",          "Communication", False),

    ("photoshop",      "Creative",      False),
    ("illustrator",    "Creative",      False),
    ("premiere",       "Creative",      False),
    ("aftereffects",   "Creative",      False),
    ("blender",        "Creative",      False),
    ("figma",          "Creative",      False),
    ("canva",          "Creative",      False),

    ("steam",          "Gaming",        True),
    ("battle.net",     "Gaming",        True),
    ("epicgames",      "Gaming",        True),
    ("genshin",        "Gaming",        True),
    ("league",         "Gaming",        True),
    ("riot",           "Gaming",        True),

    ("netflix",        "Entertainment", True),
    ("spotify",        "Entertainment", False),
    ("youtube",        "Entertainment", True),
    ("vlc",            "Entertainment", False),
    ("twitch",         "Entertainment", True),

    ("explorer",       "System",        False),
    ("dwm",            "System",        False),
    ("svchost",        "System",        False),
    ("taskmgr",        "System",        False),
    ("settings",       "System",        False),
    ("searchhost",     "System",        False),
    ("textinputhost",  "System",        False),
    ("startmenuexp",   "System",        False),
    ("shellexperience","System",        False),
    ("widgets",        "System",        False),
    ("lockapp",        "System",        False),
    ("crossdevice",    "System",        False),
    ("phoneexperien",  "System",        False),
    ("runtimebroker",  "System",        False),
    ("sihost",         "System",        False),
    ("ctfmon",         "System",        False),
]


def classify(process_name: str) -> tuple[str, bool]:
    """Returns (category, is_distraction). Checks manual override first."""
    if not process_name:
        return "Other", False
    name = process_name.lower()

    # Manual override from DB
    conn = get_conn()
    row = conn.execute(
        "SELECT category, is_distraction FROM app_categories WHERE process_name = ?",
        (process_name,)
    ).fetchone()
    if row:
        return row["category"], bool(row["is_distraction"])

    # Auto rules
    for sub, cat, dist in DEFAULT_RULES:
        if sub in name:
            return cat, dist
    return "Other", False


def set_override(process_name: str, category: str, is_distraction: bool = False) -> None:
    conn = get_conn()
    conn.execute(
        "INSERT INTO app_categories (process_name, category, is_distraction) VALUES (?, ?, ?) "
        "ON CONFLICT(process_name) DO UPDATE SET "
        "category = excluded.category, is_distraction = excluded.is_distraction, "
        "updated_at = CURRENT_TIMESTAMP",
        (process_name, category, int(is_distraction))
    )
    conn.commit()


def all_categories() -> list[str]:
    cats = sorted({c for _, c, _ in DEFAULT_RULES})
    return cats + ["Other"]
