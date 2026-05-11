# Pulse — Browser extension

Captures your ChatGPT / Claude.ai / Gemini / Perplexity web sessions and sends
them to the Pulse desktop app for unified analytics.

## What it captures

- **Provider name** (openai, anthropic-web, google-gemini-web, perplexity)
- **Model name** when exposed by the API response
- **Timestamp**
- **Approximate character count** of response (for token estimation)

**Never captured**: message text, conversation content, personal information.

## Install (dev mode)

1. Chrome / Edge → Extensions → Enable Developer mode → "Load unpacked"
2. Select the `browser-ext/` folder
3. Visit chat.openai.com or claude.ai and chat normally
4. Open the extension popup → see buffered events

The buffer is flushed every 5 minutes to `http://localhost:8000/v1/ingest/web-session`
(your local Pulse desktop). If the desktop is offline, events buffer locally up to 1000.

## Permissions justification

- `storage` — buffer events while desktop offline
- `alarms` — periodic sync every 5 minutes
- Host permissions on AI sites — needed to inject the fetch wrapper

## Publishing

Submit to:
- Chrome Web Store ($5 one-time fee)
- Microsoft Edge Add-ons (free)
- Firefox Add-ons (free, but requires Manifest V2 fork)

## Roadmap

- v0.2 — Cluely, Mistral, Lovable, v0
- v0.3 — Background token estimation via tiktoken in worker
- v0.4 — Direct cloud sync (skip desktop) for Pulse Pro users
