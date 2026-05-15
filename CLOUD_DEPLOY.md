# Deploying the pulse cloud server

The pulse desktop app runs entirely locally. **You don't need this server unless you want Pro features** (cross-device sync, mobile PWA, multi-user team workspaces). Everything in this repo is MIT-licensed — self-host the server with zero rate limit.

---

## What this gets you

- REST API at `https://api.your-domain.com/v1/*` for the SDK / mobile / 3rd-party integrations
- Encrypted sync endpoint at `/sync/push` + `/sync/pull` for cross-device subscription + AI usage sharing
- WebSocket bridge for the browser extension to push live capture
- Optional Stripe billing webhooks (`/v1/webhooks/stripe`) when you're ready to charge

The server is stateless — auth + storage are delegated to Supabase. You can replace Supabase with any Postgres + JWT provider; the abstraction lives in `cloud/auth.py`.

---

## Local dev (no Supabase needed)

For hacking on the API locally:

```bash
pip install -r requirements-cloud.txt
python -m api.server --dev --port 8000
```

The `--dev` flag bypasses JWT signature verification — every request with `Authorization: Bearer <anything>` is accepted and the user_id is derived from a sha1 of the token. **Never expose this to the public internet.**

Then hit it:

```bash
curl http://localhost:8000/healthz
curl -H "Authorization: Bearer dev" http://localhost:8000/v1/subscriptions
```

The local SQLite at `data/tracker.db` is read directly — same data the Streamlit dashboard uses. Changes via the API are visible in the dashboard immediately.

---

## Production deploy — Supabase + Fly.io (recommended)

### 1. Create the Supabase project

1. Sign up at [supabase.com](https://supabase.com) (free tier: 500 MB database, 50k MAU — covers most pulse deployments)
2. Project Settings → API → copy:
   - `Project URL` (e.g. `https://xxxxx.supabase.co`)
   - `service_role` key (NOT anon — the server needs full access)
   - `JWT Secret` from Project Settings → API → JWT Settings
3. SQL Editor → run the schema from `ROADMAP.md` § 1.2 (the `accounts` / `workspaces` / `subscriptions_enc` / `audit_log` tables)

### 2. Create a Fly.io app

```bash
fly launch --name pulse-api --no-deploy
```

Edit the generated `fly.toml`:

```toml
app = "pulse-api"
primary_region = "iad"

[build]
  dockerfile = "Dockerfile.api"

[http_service]
  internal_port = 8000
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0

[checks]
  [checks.api]
    grace_period = "10s"
    interval = "30s"
    method = "get"
    path = "/healthz"
    port = 8000
    timeout = "5s"
    type = "http"
```

### 3. Set the secrets

```bash
fly secrets set \
  SUPABASE_URL=https://xxxxx.supabase.co \
  SUPABASE_SERVICE_ROLE_KEY=eyJhbGc... \
  SUPABASE_JWT_SECRET=your-jwt-secret \
  SUPABASE_JWT_AUDIENCE=authenticated
```

### 4. Deploy

```bash
fly deploy
```

Confirm with:

```bash
curl https://pulse-api.fly.dev/healthz
```

The response should show `"supabase_configured": true` and `"dev_mode": false`.

---

## Alternative deploys

| Platform | Pros | Cons |
|---|---|---|
| Fly.io | Cheap (<$5/mo), great Postgres integration | Less popular than Vercel |
| Render | One-click Postgres + Web Service | $7/mo minimum for non-free tier |
| Railway | Generous free tier, slick UI | $5/mo minimum once you exceed free |
| Cloudflare Workers | Free tier huge, edge-deployed | Need to port FastAPI → Hono (significant work) |
| Self-host on a VPS | Full control, fixed cost | You own the uptime |

The server is plain FastAPI + uvicorn. Any Python-friendly platform works.

---

## Required environment variables

| Variable | Required for | Default |
|---|---|---|
| `SUPABASE_URL` | Supabase calls | — |
| `SUPABASE_SERVICE_ROLE_KEY` | DB inserts (bypasses RLS) | — |
| `SUPABASE_JWT_SECRET` | JWT verification | — |
| `SUPABASE_JWT_AUDIENCE` | JWT verification | `authenticated` |
| `PULSE_API_DEV_MODE` | Local dev bypass | unset (= prod mode) |

If neither `SUPABASE_JWT_SECRET` nor `PULSE_API_DEV_MODE=1` is set, every authenticated request returns HTTP 500 with a clear message.

---

## Dockerfile

```dockerfile
# Dockerfile.api
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt requirements-cloud.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r requirements-cloud.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "api.server:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Testing the deployment

```bash
# 1. Health check (no auth required)
curl https://api.your-domain.com/healthz

# 2. Try an authenticated request (should return 401 without a real Supabase JWT)
curl https://api.your-domain.com/v1/me
# {"detail":"missing_bearer_token"}

# 3. With a malformed token (should return 401)
curl -H "Authorization: Bearer bad" https://api.your-domain.com/v1/me
# {"detail":"malformed_token"}

# 4. With a real Supabase-issued JWT (returns the user's profile)
curl -H "Authorization: Bearer eyJhbGc..." https://api.your-domain.com/v1/me
# {"user_id":"abc-123","email":"...","plan":"pro","currency":"USD",...}
```

---

## Costs at typical scale

| Tier | Users | Supabase | Fly.io | Total |
|---|---|---|---|---|
| Dev | 1 (you) | free | free | $0 |
| Personal | <50 | free | free | $0 |
| Small team | <500 | free | free–$5/mo | $0–5/mo |
| Growing | <5k | $25/mo (Pro) | $5/mo | ~$30/mo |
| Production | 50k+ | $25–100/mo | $20–50/mo | $45–150/mo |

Pulse is structurally cheap at the cloud tier because the actual data lives on user machines — the cloud is a thin sync layer holding encrypted blobs + metadata.

---

## Security baseline

The server enforces:

1. JWT signature verification on every `/v1/*` endpoint
2. CORS — currently `*` for dev; **change `allow_origins` in `api/server.py:46` to your real domain(s) before production**
3. No password storage — Supabase Auth handles login (magic links or OAuth)
4. Row-Level Security via Supabase policies — see `ROADMAP.md` § 1.2

Things you must do before exposing to the internet:

- [ ] Tighten CORS `allow_origins`
- [ ] Move `SUPABASE_*` env vars out of `fly.toml` into `fly secrets set`
- [ ] Enable rate limiting (Cloudflare in front + Supabase rate limits)
- [ ] Set up Sentry or similar for error tracking
- [ ] Configure backups (Supabase has automatic Point-In-Time Recovery on Pro)
- [ ] Run the audit log query (`SELECT * FROM audit_log ORDER BY at DESC LIMIT 100`) at least weekly

---

## Self-host vs Pulse-hosted

This is the same MIT-licensed code that powers the eventual Pulse Pro hosted service. The paid Pro tier ($9/mo when it launches Q3 2026) is hosting + maintenance + the mobile PWA — never a feature lock.

If you self-host: you own the server, you own the data, you pay your own infra bill (often $0).
If you use Pulse-hosted: we run it for you. Same software, same encryption, same source code.
