"""AI provider adapters — Phase 2+.

Each module implements `sync()` / `parse_*()` functions that return a list
of normalized TokenUsageRow dicts ready to insert into the `token_usage` table.

The Anthropic Claude Code adapter lives in `sync_tokens.py` (production).

Phase 2 providers (stub modules — implementation begins when Cloud sync ships):
- openai_parser  — ChatGPT Plus / API / Team
- cursor_parser  — Cursor IDE local state
- gemini_parser  — Google AI Studio + Gemini app
- copilot_parser — GitHub Copilot (flat subscription + GraphQL audit)

Future providers:
- perplexity_parser
- replit_parser
- v0_parser
- lovable_parser
- mistral_parser
"""
