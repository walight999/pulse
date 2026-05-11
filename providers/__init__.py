"""AI provider adapters — multi-provider usage tracking.

Each module implements `sync()` / `parse_*()` / `sync_from_*()` functions
that return TokenUsageRow dicts ready to insert into the `token_usage` table.

The Anthropic Claude Code adapter lives in `sync_tokens.py` (production).

Production-ready providers:
- openai_parser     — ChatGPT API (/v1/usage) + ChatGPT export archive parser
- cursor_parser     — Cursor IDE local state.vscdb reader (read-only)

Scaffolded (Phase 2 wiring needed):
- gemini_parser     — Google AI Studio + Gemini app
- copilot_parser    — GitHub Copilot flat + GraphQL audit
- gmail_usage_parser — Gmail invoice scanner across all providers

Stub (flat-rate-only, defer to gmail_usage_parser for invoices):
- perplexity_parser — Perplexity Pro + sonar API
- replit_parser     — Replit Core/Teams/Enterprise
- v0_parser         — v0.dev (Vercel)
- lovable_parser    — Lovable
- mistral_parser    — Mistral La Plateforme + Le Chat
"""
