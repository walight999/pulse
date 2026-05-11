# Pulse Cloud — Phase 2

Production-ready code for opt-in cloud sync. Activated when a Supabase project
is provisioned and `SUPABASE_URL` + `SUPABASE_ANON_KEY` env vars are set.

## Modules

| File | What |
|------|------|
| `auth.py` | Supabase Auth magic-link signup/signin + JWT cache |
| `crypto.py` | AES-256-GCM + Argon2id key derivation (audited libs) |
| `sync.py` | Encrypted delta sync with last-write-wins conflict resolution |
| `leaderboard.py` | 5-category ranking computation (Best ROI / Streak / Token wizard / Power day / Project depth) |
| `teams.py` | Multi-user team workspaces + role-based access |
| `sso.py` | SAML/OIDC scaffolding (Enterprise tier) |
| `billing.py` | Stripe Checkout integration |
| `supabase_schema.sql` | Postgres schema + RLS + RPC functions |

## Deploy steps (when activating Cloud)

### 1. Create Supabase project

1. Sign up at https://supabase.com → New Project
2. Project name: `pulse-prod` (or `-staging` for testing)
3. Database password: generate strong, save in 1Password
4. Region: closest to your users (e.g. ap-southeast-1 for SEA)
5. Wait ~2 min for provisioning

### 2. Apply schema

```bash
# Option A — Supabase Dashboard → SQL Editor → paste entire file → Run
cat cloud/supabase_schema.sql | xclip -selection clipboard

# Option B — psql (if you exposed direct connection)
psql "postgres://postgres:[PASSWORD]@db.[PROJECT_REF].supabase.co:5432/postgres" \
  -f cloud/supabase_schema.sql
```

### 3. Install auth.users trigger (manual, requires admin)

In Supabase Dashboard → SQL Editor, run:

```sql
CREATE TRIGGER trg_on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION on_auth_user_created();
```

This auto-creates a `pulse_profiles` row when someone signs up.

### 4. Configure email

Supabase Dashboard → Authentication → Email Templates:

- Enable email confirmations
- Customize magic link template with Pulse branding (use `operations/welcome-email.html`)
- Set sender to `hi@pulse.app` (requires custom SMTP)

### 5. Set env vars in desktop app

Create `.env` in the project root (gitignored):

```bash
SUPABASE_URL=https://[PROJECT_REF].supabase.co
SUPABASE_ANON_KEY=eyJhb...
```

Or via Settings → Cloud → "Connect cloud" UI (TODO: wire UI).

### 6. Install Python deps

```bash
pip install -r requirements-cloud.txt
```

### 7. Test round trip

```python
from cloud import auth, sync, crypto
# Sign up
auth.signup_with_magic_link("test@example.com", "local-pulse-id-uuid")
# User clicks link → exchanges token for session
# Run sync
master_key = crypto.derive_master_key("test-password", crypto.new_salt())
hmac_secret = b"hmac-secret-bytes-32"
sync.sync_once(master_key, hmac_secret)
```

## Schema overview

```
auth.users (Supabase built-in)
   │
   ├── pulse_profiles (1:1)
   │     plan, pro_until, stripe_customer_id, referral_code
   │
   ├── pulse_deltas (1:N)
   │     encrypted blobs for subscriptions / token_usage / app_activity
   │
   ├── leaderboard_entries (1:N — by window)
   │     metrics JSONB, visibility, display_name
   │
   ├── friendships (M:N self)
   │     canonical user_a < user_b ordering
   │
   ├── teams (1:N as owner) ◀──── team_members (M:N)
   │                                   ┌── teams ──┐
   │                                   └──── team_invites
   │
   └── audit_log (1:N)
         action, target, details JSONB
```

## RLS policies in plain English

- **pulse_deltas**: only the workspace owner can read/write their rows
- **pulse_profiles**: only the user can read/update their own profile
- **leaderboard_entries**: user can write their own; friends can read friends-scoped; everyone can read public
- **friendships**: both sides can read; either side can delete
- **teams**: members can read; only admins can update
- **team_invites**: admins manage; invited email can see their own
- **audit_log**: owner read-only

## RPC functions

| Function | Caller | Purpose |
|----------|--------|---------|
| `pulse_push_deltas(workspace_id, deltas[])` | desktop | Bulk upsert encrypted changes (last-write-wins) |
| `pulse_pull_deltas(workspace_id, since)` | desktop | Fetch newer-than-since changes |
| `pulse_leaderboard(category, window, scope, limit)` | desktop / mobile | Friend/public rankings |
| `pulse_my_teams(user_id)` | desktop | List teams user is in |
| `pulse_team_dashboard(team_id, window)` | desktop | Aggregate team metrics |
| `pulse_accept_team_invite(code, user_id)` | mobile / desktop | Redeem invite code |

## Cost estimates

Supabase Pro tier ($25/mo) covers:
- 8 GB database storage (millions of encrypted rows)
- 50 GB bandwidth
- 100K monthly active users
- Custom domain (api.pulse.app)
- SOC 2 Type II compliance (parent platform)

For first 1,000 Pulse Pro users, free tier ($0) suffices:
- 500 MB database
- 2 GB bandwidth
- 50K monthly active users

Scale up to Pro when MRR > $500.

## Self-hosted alternative

For users who don't trust hosted Supabase:

```yaml
# docker-compose.yml (simplified)
services:
  db:
    image: supabase/postgres:15
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - ./pgdata:/var/lib/postgresql/data
      - ./cloud/supabase_schema.sql:/docker-entrypoint-initdb.d/01-schema.sql
  api:
    image: supabase/postgrest:latest
    environment:
      PGRST_DB_URI: postgres://postgres:${DB_PASSWORD}@db:5432/postgres
      PGRST_DB_ANON_ROLE: anon
      PGRST_JWT_SECRET: ${JWT_SECRET}
    depends_on:
      - db
```

Full Docker setup ships with Pulse Team self-hosted (v3.0).
