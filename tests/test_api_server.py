"""Smoke tests for the Pulse REST API.

These exercise the server in dev-mode (PULSE_API_DEV_MODE=1) so the JWT
verification is bypassed — production deployments must run without that flag
and provide SUPABASE_JWT_SECRET.
"""
import os
import pytest

# Force dev mode before the server module imports.
os.environ["PULSE_API_DEV_MODE"] = "1"

try:
    from fastapi.testclient import TestClient
    from api.server import app
    HAVE_FASTAPI = True
except ImportError:
    HAVE_FASTAPI = False

pytestmark = pytest.mark.skipif(not HAVE_FASTAPI, reason="fastapi not installed")


@pytest.fixture
def client():
    return TestClient(app)


def test_health_endpoint(client):
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["service"] == "pulse-api"


def test_healthz_reports_dev_mode(client):
    r = client.get("/healthz")
    assert r.status_code == 200
    body = r.json()
    assert body["dev_mode"] is True
    assert body["supabase_configured"] is False


def test_unauthenticated_request_rejected(client):
    r = client.get("/v1/me")
    assert r.status_code == 401
    assert r.json()["detail"] == "missing_bearer_token"


def test_dev_mode_accepts_any_bearer(client):
    r = client.get("/v1/me", headers={"Authorization": "Bearer hack-token-anything"})
    # Either 200 (settings exist) or some legit error from downstream — but NOT 401.
    assert r.status_code != 401


def test_subscriptions_list_returns_array(client):
    r = client.get("/v1/subscriptions", headers={"Authorization": "Bearer dev"})
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_token_usage_returns_array(client):
    r = client.get("/v1/token_usage?limit=10", headers={"Authorization": "Bearer dev"})
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_monthly_stats_returns_months(client):
    r = client.get("/v1/stats/monthly", headers={"Authorization": "Bearer dev"})
    assert r.status_code == 200
    assert "months" in r.json()


def test_invalid_leaderboard_category(client):
    r = client.get("/v1/leaderboard/not_a_category", headers={"Authorization": "Bearer dev"})
    assert r.status_code == 400


def test_valid_leaderboard_category(client):
    # `best_roi` is in the whitelist — should return [] (no friends seeded) but not error
    r = client.get("/v1/leaderboard/best_roi", headers={"Authorization": "Bearer dev"})
    assert r.status_code == 200
    assert isinstance(r.json(), list)
