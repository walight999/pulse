-- ============================================================================
-- Pulse Cloud — Supabase Postgres schema (v2.0)
--
-- Run in order on a fresh Supabase project:
--   1. Tables + indexes
--   2. Row Level Security policies
--   3. RPC functions
--   4. Triggers for updated_at
--
-- Apply via Supabase Dashboard → SQL Editor, or psql:
--   psql "$(supabase status | grep DB | cut -d= -f2)" -f cloud/supabase_schema.sql
--
-- The `auth.users(id)` references are Supabase Auth's built-in users table.
-- All app data is encrypted client-side (cloud/crypto.py) before reaching here.
-- Server stores only ciphertext + HMAC-SHA256 searchable indexes.
-- ============================================================================

-- ────────────────── 1. TABLES ──────────────────

-- Encrypted sync deltas — last-write-wins by updated_at.
CREATE TABLE IF NOT EXISTS pulse_deltas (
    id BIGSERIAL PRIMARY KEY,
    workspace_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    table_name TEXT NOT NULL CHECK (table_name IN ('subscriptions', 'token_usage', 'app_activity')),
    row_id TEXT NOT NULL,
    ciphertext BYTEA NOT NULL,
    nonce BYTEA NOT NULL,
    searchable_index JSONB DEFAULT '{}'::jsonb,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    deleted BOOLEAN DEFAULT false,
    UNIQUE (workspace_id, table_name, row_id)
);
CREATE INDEX IF NOT EXISTS idx_pulse_deltas_workspace_updated
    ON pulse_deltas (workspace_id, updated_at DESC);
CREATE INDEX IF NOT EXISTS idx_pulse_deltas_searchable
    ON pulse_deltas USING GIN (searchable_index);

-- Per-user profile (extends auth.users with Pulse-specific fields)
CREATE TABLE IF NOT EXISTS pulse_profiles (
    user_id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    plan TEXT DEFAULT 'free' CHECK (plan IN ('free', 'pro', 'team', 'enterprise')),
    pro_until TIMESTAMPTZ,
    stripe_customer_id TEXT UNIQUE,
    display_name TEXT,
    referral_code TEXT UNIQUE,
    referred_by TEXT REFERENCES pulse_profiles(referral_code) ON DELETE SET NULL,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Leaderboard opt-in metrics — aggregate only, never raw token data
CREATE TABLE IF NOT EXISTS leaderboard_entries (
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    window TEXT NOT NULL CHECK (window IN ('weekly', 'monthly', 'all_time')),
    visibility TEXT NOT NULL DEFAULT 'friends' CHECK (visibility IN ('off', 'friends', 'public')),
    display_name TEXT NOT NULL,
    metrics JSONB NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT now(),
    PRIMARY KEY (user_id, window)
);
CREATE INDEX IF NOT EXISTS idx_leaderboard_visibility ON leaderboard_entries (visibility);

-- Friend graph — for leaderboard scoping
CREATE TABLE IF NOT EXISTS friendships (
    user_a UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    user_b UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT now(),
    PRIMARY KEY (user_a, user_b),
    CHECK (user_a < user_b)   -- canonical ordering, prevents duplicate pairs
);
CREATE INDEX IF NOT EXISTS idx_friendships_a ON friendships (user_a);
CREATE INDEX IF NOT EXISTS idx_friendships_b ON friendships (user_b);

-- Teams (Pulse Team tier)
CREATE TABLE IF NOT EXISTS teams (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    owner_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE RESTRICT,
    plan TEXT DEFAULT 'team' CHECK (plan IN ('team', 'enterprise')),
    seat_count INT DEFAULT 1,
    stripe_subscription_id TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS team_members (
    team_id UUID NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    role TEXT NOT NULL CHECK (role IN ('admin', 'member', 'viewer')),
    joined_at TIMESTAMPTZ DEFAULT now(),
    PRIMARY KEY (team_id, user_id)
);
CREATE INDEX IF NOT EXISTS idx_team_members_user ON team_members (user_id);

CREATE TABLE IF NOT EXISTS team_invites (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    team_id UUID NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
    email TEXT NOT NULL,
    code TEXT UNIQUE NOT NULL,
    role TEXT NOT NULL DEFAULT 'member',
    invited_by UUID NOT NULL REFERENCES auth.users(id),
    invited_at TIMESTAMPTZ DEFAULT now(),
    used_by UUID REFERENCES auth.users(id),
    used_at TIMESTAMPTZ,
    expires_at TIMESTAMPTZ DEFAULT (now() + interval '7 days')
);
CREATE INDEX IF NOT EXISTS idx_team_invites_code ON team_invites (code);

-- Server-side audit log (mirrors client audit_log table)
CREATE TABLE IF NOT EXISTS audit_log (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
    action TEXT NOT NULL,
    target TEXT,
    details JSONB DEFAULT '{}'::jsonb,
    ip INET,
    user_agent TEXT,
    timestamp TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_audit_user_ts ON audit_log (user_id, timestamp DESC);


-- ────────────────── 2. ROW LEVEL SECURITY ──────────────────

ALTER TABLE pulse_deltas         ENABLE ROW LEVEL SECURITY;
ALTER TABLE pulse_profiles       ENABLE ROW LEVEL SECURITY;
ALTER TABLE leaderboard_entries  ENABLE ROW LEVEL SECURITY;
ALTER TABLE friendships          ENABLE ROW LEVEL SECURITY;
ALTER TABLE teams                ENABLE ROW LEVEL SECURITY;
ALTER TABLE team_members         ENABLE ROW LEVEL SECURITY;
ALTER TABLE team_invites         ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_log            ENABLE ROW LEVEL SECURITY;

-- pulse_deltas: only owner can read/write their workspace data
CREATE POLICY "owner read deltas" ON pulse_deltas
    FOR SELECT USING (workspace_id = auth.uid());
CREATE POLICY "owner write deltas" ON pulse_deltas
    FOR ALL USING (workspace_id = auth.uid()) WITH CHECK (workspace_id = auth.uid());

-- pulse_profiles: only owner can read/update; insert via trigger on auth.users
CREATE POLICY "owner read profile" ON pulse_profiles
    FOR SELECT USING (user_id = auth.uid());
CREATE POLICY "owner update profile" ON pulse_profiles
    FOR UPDATE USING (user_id = auth.uid()) WITH CHECK (user_id = auth.uid());

-- leaderboard_entries:
-- - User can read/write their own
-- - Friends can read each other's friends-scoped entries
-- - Anyone can read public entries
CREATE POLICY "leaderboard self" ON leaderboard_entries
    FOR ALL USING (user_id = auth.uid()) WITH CHECK (user_id = auth.uid());
CREATE POLICY "leaderboard friends" ON leaderboard_entries
    FOR SELECT USING (
        visibility = 'friends'
        AND (
            EXISTS (SELECT 1 FROM friendships f
                    WHERE (f.user_a = auth.uid() AND f.user_b = user_id)
                       OR (f.user_b = auth.uid() AND f.user_a = user_id))
        )
    );
CREATE POLICY "leaderboard public" ON leaderboard_entries
    FOR SELECT USING (visibility = 'public');

-- friendships: both parties can see + delete
CREATE POLICY "friendship read" ON friendships
    FOR SELECT USING (user_a = auth.uid() OR user_b = auth.uid());
CREATE POLICY "friendship delete" ON friendships
    FOR DELETE USING (user_a = auth.uid() OR user_b = auth.uid());
-- friendship insert happens via accept_friend_invite RPC, not directly

-- teams: members can read; only admins can update
CREATE POLICY "team member read" ON teams
    FOR SELECT USING (
        EXISTS (SELECT 1 FROM team_members tm
                WHERE tm.team_id = id AND tm.user_id = auth.uid())
    );
CREATE POLICY "team admin update" ON teams
    FOR UPDATE USING (
        EXISTS (SELECT 1 FROM team_members tm
                WHERE tm.team_id = id AND tm.user_id = auth.uid() AND tm.role = 'admin')
    );

-- team_members: members can read; admins can write
CREATE POLICY "team_members read" ON team_members
    FOR SELECT USING (
        EXISTS (SELECT 1 FROM team_members tm2
                WHERE tm2.team_id = team_id AND tm2.user_id = auth.uid())
    );
CREATE POLICY "team_members admin write" ON team_members
    FOR ALL USING (
        EXISTS (SELECT 1 FROM team_members tm2
                WHERE tm2.team_id = team_id AND tm2.user_id = auth.uid() AND tm2.role = 'admin')
    ) WITH CHECK (
        EXISTS (SELECT 1 FROM team_members tm2
                WHERE tm2.team_id = team_id AND tm2.user_id = auth.uid() AND tm2.role = 'admin')
    );

-- team_invites: admins read/write all; invited email can read their own
CREATE POLICY "team_invites admin" ON team_invites
    FOR ALL USING (
        EXISTS (SELECT 1 FROM team_members tm
                WHERE tm.team_id = team_id AND tm.user_id = auth.uid() AND tm.role = 'admin')
    );
CREATE POLICY "team_invites invited" ON team_invites
    FOR SELECT USING (email = auth.jwt() ->> 'email');

-- audit_log: read-only by owner
CREATE POLICY "audit owner read" ON audit_log
    FOR SELECT USING (user_id = auth.uid());


-- ────────────────── 3. RPC FUNCTIONS ──────────────────

-- pulse_push_deltas(workspace_id, deltas) — bulk upsert of encrypted changes
CREATE OR REPLACE FUNCTION pulse_push_deltas(
    workspace_id UUID,
    deltas JSONB
)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    accepted INT := 0;
    rejected INT := 0;
    delta JSONB;
BEGIN
    IF auth.uid() != workspace_id THEN
        RAISE EXCEPTION 'unauthorized: workspace does not match auth.uid()';
    END IF;
    FOR delta IN SELECT jsonb_array_elements(deltas) LOOP
        BEGIN
            INSERT INTO pulse_deltas (
                workspace_id, table_name, row_id,
                ciphertext, nonce, searchable_index, updated_at, deleted
            ) VALUES (
                workspace_id,
                delta->>'table',
                delta->>'row_id',
                decode(delta->>'ciphertext', 'hex'),
                decode(delta->>'nonce', 'hex'),
                COALESCE(delta->'searchable_index', '{}'::jsonb),
                COALESCE((delta->>'updated_at')::timestamptz, now()),
                COALESCE((delta->>'deleted')::boolean, false)
            )
            ON CONFLICT (workspace_id, table_name, row_id) DO UPDATE
            SET ciphertext       = EXCLUDED.ciphertext,
                nonce            = EXCLUDED.nonce,
                searchable_index = EXCLUDED.searchable_index,
                updated_at       = EXCLUDED.updated_at,
                deleted          = EXCLUDED.deleted
            WHERE pulse_deltas.updated_at < EXCLUDED.updated_at;
            accepted := accepted + 1;
        EXCEPTION WHEN OTHERS THEN
            rejected := rejected + 1;
        END;
    END LOOP;
    RETURN jsonb_build_object('accepted', accepted, 'rejected', rejected);
END;
$$;

-- pulse_pull_deltas(workspace_id, since) — fetch newer-than-since changes
CREATE OR REPLACE FUNCTION pulse_pull_deltas(
    workspace_id UUID,
    since TIMESTAMPTZ
)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    result JSONB;
BEGIN
    IF auth.uid() != workspace_id THEN
        RAISE EXCEPTION 'unauthorized: workspace does not match auth.uid()';
    END IF;
    SELECT COALESCE(jsonb_agg(jsonb_build_object(
        'table',            table_name,
        'row_id',           row_id,
        'ciphertext',       encode(ciphertext, 'hex'),
        'nonce',            encode(nonce, 'hex'),
        'searchable_index', searchable_index,
        'updated_at',       updated_at,
        'deleted',          deleted
    )), '[]'::jsonb)
    INTO result
    FROM pulse_deltas
    WHERE pulse_deltas.workspace_id = pulse_pull_deltas.workspace_id
      AND updated_at > since
    LIMIT 5000;
    RETURN result;
END;
$$;

-- pulse_leaderboard(category, window, scope, limit)
CREATE OR REPLACE FUNCTION pulse_leaderboard(
    p_user_id UUID,
    p_category TEXT,
    p_window TEXT DEFAULT 'monthly',
    p_scope TEXT DEFAULT 'friends',
    p_limit INT DEFAULT 10
)
RETURNS TABLE(user_id UUID, display_name TEXT, value NUMERIC, unit TEXT, rank INT)
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    unit_label TEXT;
BEGIN
    IF auth.uid() != p_user_id THEN
        RAISE EXCEPTION 'unauthorized';
    END IF;
    unit_label := CASE p_category
        WHEN 'best_roi'        THEN 'x'
        WHEN 'longest_streak'  THEN 'days'
        WHEN 'token_wizard'    THEN 'ratio'
        WHEN 'power_day'       THEN 'USD'
        WHEN 'project_depth'   THEN 'projects'
        ELSE ''
    END;
    RETURN QUERY
    SELECT
        le.user_id,
        le.display_name,
        (le.metrics ->> p_category)::numeric AS value,
        unit_label AS unit,
        ROW_NUMBER() OVER (ORDER BY (le.metrics ->> p_category)::numeric DESC)::int AS rank
    FROM leaderboard_entries le
    WHERE le.window = p_window
      AND (
        (p_scope = 'public' AND le.visibility = 'public')
        OR
        (p_scope = 'friends' AND le.visibility IN ('friends', 'public')
          AND (le.user_id = p_user_id
               OR EXISTS (SELECT 1 FROM friendships f
                          WHERE (f.user_a = p_user_id AND f.user_b = le.user_id)
                             OR (f.user_b = p_user_id AND f.user_a = le.user_id))))
      )
    ORDER BY value DESC NULLS LAST
    LIMIT p_limit;
END;
$$;

-- pulse_my_teams(user_id) — list teams the user is a member of
CREATE OR REPLACE FUNCTION pulse_my_teams(p_user_id UUID)
RETURNS TABLE(id UUID, name TEXT, owner_id UUID, plan TEXT, seat_count INT)
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
    IF auth.uid() != p_user_id THEN
        RAISE EXCEPTION 'unauthorized';
    END IF;
    RETURN QUERY
    SELECT t.id, t.name, t.owner_id, t.plan, t.seat_count
    FROM teams t
    INNER JOIN team_members tm ON tm.team_id = t.id
    WHERE tm.user_id = p_user_id
    ORDER BY t.name;
END;
$$;

-- pulse_team_dashboard(team_id, window) — aggregate team metrics
CREATE OR REPLACE FUNCTION pulse_team_dashboard(p_team_id UUID, p_window TEXT)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    is_member BOOLEAN;
    result JSONB;
BEGIN
    SELECT EXISTS (
        SELECT 1 FROM team_members tm
        WHERE tm.team_id = p_team_id AND tm.user_id = auth.uid()
    ) INTO is_member;
    IF NOT is_member THEN
        RAISE EXCEPTION 'not a team member';
    END IF;
    SELECT jsonb_build_object(
        'team_id',    p_team_id,
        'window',     p_window,
        'member_count', (SELECT COUNT(*) FROM team_members WHERE team_id = p_team_id),
        'members',    (
            SELECT jsonb_agg(jsonb_build_object(
                'user_id', tm.user_id,
                'role',    tm.role,
                'display_name', COALESCE(pp.display_name, 'member')
            ))
            FROM team_members tm
            LEFT JOIN pulse_profiles pp ON pp.user_id = tm.user_id
            WHERE tm.team_id = p_team_id
        )
    ) INTO result;
    RETURN result;
END;
$$;

-- pulse_accept_team_invite(code, user_id) — redeem invite + add as member
CREATE OR REPLACE FUNCTION pulse_accept_team_invite(p_code TEXT, p_user_id UUID)
RETURNS UUID
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    invite team_invites%ROWTYPE;
BEGIN
    IF auth.uid() != p_user_id THEN
        RAISE EXCEPTION 'unauthorized';
    END IF;
    SELECT * INTO invite FROM team_invites
    WHERE code = p_code AND used_by IS NULL AND expires_at > now();
    IF NOT FOUND THEN
        RAISE EXCEPTION 'invite not found or expired';
    END IF;
    INSERT INTO team_members (team_id, user_id, role)
    VALUES (invite.team_id, p_user_id, invite.role)
    ON CONFLICT DO NOTHING;
    UPDATE team_invites SET used_by = p_user_id, used_at = now()
    WHERE id = invite.id;
    RETURN invite.team_id;
END;
$$;


-- ────────────────── 4. TRIGGERS ──────────────────

-- Auto-update updated_at on relevant tables
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    NEW.updated_at := now();
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_pulse_profiles_updated_at
    BEFORE UPDATE ON pulse_profiles
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_teams_updated_at
    BEFORE UPDATE ON teams
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_leaderboard_updated_at
    BEFORE UPDATE ON leaderboard_entries
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- Auto-create pulse_profile when a new auth.user signs up
CREATE OR REPLACE FUNCTION on_auth_user_created()
RETURNS TRIGGER LANGUAGE plpgsql SECURITY DEFINER AS $$
BEGIN
    INSERT INTO pulse_profiles (user_id, referral_code)
    VALUES (NEW.id, encode(gen_random_bytes(6), 'hex'))
    ON CONFLICT DO NOTHING;
    RETURN NEW;
END;
$$;

-- Note: trigger on auth.users must be installed manually in Supabase Dashboard
-- with admin rights:
--   CREATE TRIGGER trg_on_auth_user_created
--     AFTER INSERT ON auth.users
--     FOR EACH ROW EXECUTE FUNCTION on_auth_user_created();


-- ────────────────── 5. GRANTS ──────────────────

GRANT EXECUTE ON FUNCTION pulse_push_deltas         TO authenticated;
GRANT EXECUTE ON FUNCTION pulse_pull_deltas         TO authenticated;
GRANT EXECUTE ON FUNCTION pulse_leaderboard         TO authenticated;
GRANT EXECUTE ON FUNCTION pulse_my_teams            TO authenticated;
GRANT EXECUTE ON FUNCTION pulse_team_dashboard      TO authenticated;
GRANT EXECUTE ON FUNCTION pulse_accept_team_invite  TO authenticated;

-- Done. Verify with:
--   SELECT proname FROM pg_proc WHERE proname LIKE 'pulse_%';
--   SELECT tablename FROM pg_tables WHERE tablename LIKE 'pulse_%' OR tablename IN
--     ('teams', 'team_members', 'team_invites', 'leaderboard_entries', 'friendships', 'audit_log');
