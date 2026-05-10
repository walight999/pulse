"""AI provider adapters — Phase 3.

Each module implements a `sync()` function that returns a list of normalized
TokenUsageRow dicts ready to insert into the `token_usage` table.

The Anthropic Claude Code adapter already lives in `sync_tokens.py` — this
folder is for future providers (OpenAI, Gemini, Cursor, etc.).
"""
