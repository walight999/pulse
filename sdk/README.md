# Pulse SDK

Programmatic access to your own Pulse data.

## Python

```bash
pip install requests
# (proper PyPI package coming in v1.2)
```

```python
from sdk.python.pulse_client import PulseClient

client = PulseClient(api_key="pk_live_...")

# Your profile + plan
print(client.me())

# Active subscriptions
for s in client.subscriptions(active_only=True):
    print(f"{s['name']}: {s['cost']} {s['currency']}/{s['billing_cycle']}")

# AI usage this month
from datetime import date
month_start = date.today().replace(day=1).isoformat()
usage = client.token_usage(since=month_start)
total_cost = sum(u["cost_usd"] for u in usage)
print(f"Spent ${total_cost:.2f} on AI this month")

# Friend leaderboard
top = client.leaderboard("best_roi", window="monthly", scope="friends")
for entry in top[:3]:
    print(f"#{entry['rank']}: {entry['display_name']} — {entry['value']:.1f}x")
```

## JavaScript / TypeScript

Coming in v1.2. Will support browser + Node.

## Authentication

Generate an API key in Pulse Settings → Developer → API keys.

Keys are scoped to your own data only. Team-tier keys can read team data
if your role has `admin` or `member` permission.

## Rate limits

- Free: 60 req/min
- Pro: 300 req/min
- Team: 1000 req/min per seat
- Enterprise: custom (default 5000 req/min)

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET    | /v1/me | Your profile + plan tier |
| GET    | /v1/subscriptions | List subscriptions (filter active_only) |
| GET    | /v1/token_usage | AI usage rows (paginated) |
| GET    | /v1/stats/monthly | Aggregated monthly stats |
| GET    | /v1/leaderboard/{category} | Friend rankings (opt-in) |
| POST   | /v1/export | Generate CSV / PDF export |

See `api/server.py` for the full OpenAPI spec.
