# Pulse

**Your money & time, in rhythm.**

Pulse is a local-first desktop app that tracks your subscriptions, AI-tool usage,
and computer time — and helps you save money by catching unused subscriptions
before they auto-renew.

- 100% local — your data never leaves your computer
- No account, no login, no telemetry by default
- Free forever for personal use

## Features

### Subscriptions
- Track every recurring service in one place
- Auto-detect status: active monthly / late payment / probably yearly / likely cancelled
- Renewal alerts via Windows toast notifications
- Calendar export (.ics) — see all renewals in Google/Apple Calendar
- Cost-per-hour-of-use ROI for app-linked subs

### AI usage
- Imports Claude Code logs from `~/.claude/projects/`
- Today / This month / All time views with hourly heatmap
- Per-model + per-project cost breakdown
- Plan ROI vs API equivalent ("$200 plan returning $4,000 in token value")
- Daily/monthly budgets with spike alerts

### Activity
- Foreground app tracking, idle-aware (pauses after N min of no input)
- Auto-categorized (Dev / Browser / Communication / Entertainment / etc.)
- Distraction-time ratio
- Top-apps and by-category breakdown

### System
- Background tray app — runs at login automatically
- Auto-backup of database (last 7 daily snapshots)
- Auto-vacuum + log rotation
- Multi-currency (~30 currencies), live FX rates from frankfurter.dev (ECB)

## Quick start

### Requirements
- Windows 10 / 11
- Python 3.11 or later

### Install (developer mode)
```powershell
git clone https://github.com/your-org/pulse
cd pulse
pip install -r requirements.txt
powershell -File scripts\install_task.ps1
powershell -File scripts\create_shortcut.ps1
Start-ScheduledTask -TaskName LifeTracker
```

The system tray will start a small Pulse icon. Click it → "Show dashboard" to
open `http://localhost:8501`.

### Install (standalone .exe — recommended for end users)
```powershell
powershell -File scripts\build_exe.ps1
# Distribute the dist\Pulse\ folder
```

End users double-click `Pulse.exe` — no Python needed.

## Pulse Pro (coming soon)

Pulse stays free for local single-device use forever. **Pro** ($9/mo) adds:
- Cloud sync + mobile companion
- AI assistant ("Ask Pulse")
- Cross-provider AI tracking (OpenAI, Gemini, Cursor)
- Bank/credit card auto-import
- Email digest + push notifications
- Receipt OCR

[Join the waitlist](pulse://settings#waitlist) inside the app for early access.

## Privacy

- All data is stored locally in `data/tracker.db` (SQLite)
- No accounts, no telemetry, no internet connection required
- Foreground app titles are tracked locally — *delete `data/tracker.db` to wipe*
- FX rates are fetched from frankfurter.dev (no personal data sent)

See [PRIVACY.md](PRIVACY.md).

## Documentation

- [ROADMAP.md](ROADMAP.md) — what's coming next, architecture for cloud/mobile
- [PRIVACY.md](PRIVACY.md) — what data is stored where
- [TERMS.md](TERMS.md) — terms of use

## License

To be decided. Currently: source-available, no commercial redistribution.

---

Made with care in Bangkok.
