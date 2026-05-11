# pulse — demo script

Two versions: 30-second GIF for Twitter/HN, and 90-second video for landing page.

---

## 30-second walkthrough (Twitter / HN attached GIF)

Capture with OBS Studio + ffmpeg compress to GIF, or directly via LICEcap (Mac/Win).

### Storyboard

| Time | Frame | Action | Voiceover (subtitle if silent) |
|------|-------|--------|-------------------------------|
| 0:00 | Logo splash | App tray → click "Open dashboard" | "pulse — local, fast, private" |
| 0:03 | Overview | Greeting visible, ROI hero card prominent | "Your $200 Claude plan, returning $4,127" |
| 0:08 | Hover ROI | Scroll over 5-star tier + savings number | "Legendary tier — top 1% efficiency" |
| 0:12 | Subscriptions | Click "Subscriptions" tab, show 8 subs | "Every AI sub auto-detected" |
| 0:16 | Wasted highlight | Hover the red "Wasted" badge | "Cancel idle subs, save $4,300/year" |
| 0:20 | Activity | Click "Activity", scroll Top apps list | "Where your time actually goes" |
| 0:24 | AI usage | Click "AI usage", show heatmap | "When you use AI most" |
| 0:28 | Final shot | Back to Overview with ECG line animating | "Mint for the AI era." |

### Capture settings

- Resolution: 1280×720 (Twitter native)
- Frame rate: 24 FPS (smaller file)
- Output: GIF, max 4 MB for Twitter
- Tool: OBS Studio → ffmpeg `gifski` or `gif palettegen`

### ffmpeg one-liner

```bash
ffmpeg -i demo.mp4 -vf "fps=24,scale=1280:-1:flags=lanczos,palettegen" -y palette.png
ffmpeg -i demo.mp4 -i palette.png -lavfi "fps=24,scale=1280:-1:flags=lanczos[x];[x][1:v]paletteuse" -y demo-30s.gif
```

---

## 90-second walkthrough (landing page / YouTube)

### Storyboard

| Time | Frame | Action | Voiceover |
|------|-------|--------|-----------|
| 0:00 | Black → fade to logomark | Logomark animates pulse line left-to-right | "pulse is the personal finance dashboard for the AI era." |
| 0:05 | Browser opens to pulse | Streamlit dashboard loads | "Track every AI subscription, every Claude token, every hour of focused work — in one place." |
| 0:10 | Hero card focused | Camera pushes in on Plan ROI hero | "Your $200/month Claude plan? It returned $4,127 in API equivalent value this month." |
| 0:18 | Stars animate | 5-star rating renders one by one | "Legendary tier. Top 1% efficiency. You're crushing it." |
| 0:24 | "YOU SAVED" card | Number counts up to ฿18,500 | "You saved $4,300 versus paying per-API." |
| 0:30 | Wipe to Subscriptions | Subscription list with smart status badges | "Every recurring AI service, auto-detected." |
| 0:38 | Cancel action | Right-click → Cancel link opens browser | "Cancel forgotten subs in one click. Lifetime savings tracked automatically." |
| 0:45 | Wipe to AI usage | Heatmap renders 7×24 grid | "See exactly when you use AI most." |
| 0:52 | Plan ROI bar fills | Coverage bar gradient animates | "Visualize your plan paying off in real time." |
| 0:58 | Wipe to Activity | Top apps list with green/amber bars | "Cost per hour of use — for every app, every subscription." |
| 1:05 | Streak chip glow | 47-day chip animates with pulse glow | "Hit a 30-day streak and watch your chip glow." |
| 1:10 | Settings panel | Theme switch ☾ → ☀ → ☾ smooth transition | "Light or dark. Your data, your way." |
| 1:18 | Privacy emphasis | Sidebar shows "100% local" indicator | "100% local. No account. No telemetry." |
| 1:22 | Browser ext popup | Quick shot of browser extension icon | "Browser extension captures ChatGPT, Claude.ai, Gemini, Perplexity." |
| 1:26 | End card | Logomark + "mintforai.com" + "MIT licensed" | "pulse. Mint for the AI era." |
| 1:30 | Black out | URL pulses on screen | "mintforai.com" |

### Recording setup

- 1920×1080 capture, 60 FPS
- Camtasia / DaVinci Resolve for editing
- 30 FPS final export (smaller file, smooth enough)
- Audio: instrumental track at -18 dB (royalty-free from Epidemic Sound)
- Voiceover: clean speech at -6 dB peak, normalized

### Editing notes

- Add subtle ECG line animations between scenes (matches brand)
- All cuts on the beat (sync to background music)
- End card pulses to mimic the logomark waveform
- Caption every voiceover (accessibility + sound-off viewers)

---

## Capture locations in current app

When running locally (localhost:8501):

| Section | Page | How to navigate |
|---------|------|-----------------|
| ROI hero | Overview | Top of Overview page |
| Streak chip | Overview | Next to greeting at top |
| Lifetime savings | Overview | Mid-page, green shimmer card |
| Subscriptions list | Subscriptions | Click sidebar nav |
| Wasted subscription | Subscriptions | Find sub with red badge |
| AI heatmap | AI usage → All time | 3rd tab, scroll past KPIs |
| Top apps | Activity | Click sidebar nav |
| Theme toggle | Sidebar | Top-right of sidebar |
| Browser ext popup | n/a | Capture separately from extension popup.html |

---

## Pre-capture checklist

Before recording:

- [ ] Sample data populated (run `sync_tokens.py` to have Claude logs)
- [ ] At least 5 subscriptions in DB (active + cancelled mix for variety)
- [ ] At least 30 days of activity data
- [ ] Plan budget set so ROI hero shows "Legendary" or "Excellent"
- [ ] Dark mode toggled (most users record dark mode)
- [ ] Sidebar in default collapsed state for clean main view
- [ ] Browser zoom at 100%
- [ ] OS notifications silenced
- [ ] Discord/Slack closed
- [ ] No personal info visible (real email, real names — use test data)

---

## Post-production checklist

- [ ] Length: 30s GIF + 90s video both produced
- [ ] File size: GIF < 4 MB, MP4 < 50 MB
- [ ] Captions: SRT file for video, embedded text for GIF
- [ ] Branding: logomark in corner, "mintforai.com" lower-right
- [ ] Thumbnail: hero shot at 0:15 mark
- [ ] Export: MP4 H.264 for video, GIF + WebP for animation
- [ ] Upload: YouTube unlisted first (review), then public on launch day

---

## Distribution

- 30-sec GIF → embedded in Twitter launch thread (Tweet 4 or 5)
- 30-sec GIF → README.md hero section
- 90-sec video → landing page hero
- 90-sec video → YouTube (public, link in HN post)
- Full version → Discord #showcase pinned
