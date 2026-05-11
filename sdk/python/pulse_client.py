"""Pulse Python SDK — query your own Pulse data programmatically.

Install:
    pip install requests

Usage:
    from pulse_client import PulseClient
    c = PulseClient(api_key="...")
    me = c.me()
    subs = c.subscriptions(active_only=True)
    leaders = c.leaderboard("best_roi")
"""
from __future__ import annotations

from typing import Optional
from urllib.parse import urlencode

try:
    import requests
except ImportError:
    raise SystemExit("Install requests: pip install requests")


class PulseError(Exception):
    pass


class PulseClient:
    DEFAULT_BASE_URL = "https://api.pulse.app"

    def __init__(self, api_key: str, base_url: Optional[str] = None, timeout: int = 10):
        if not api_key:
            raise ValueError("api_key required")
        self.api_key = api_key
        self.base_url = (base_url or self.DEFAULT_BASE_URL).rstrip("/")
        self.timeout = timeout
        self._session = requests.Session()
        self._session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "User-Agent": "pulse-sdk-python/1.0",
        })

    # ────────────────── Core ──────────────────

    def _get(self, path: str, params: Optional[dict] = None) -> dict | list:
        url = f"{self.base_url}{path}"
        resp = self._session.get(url, params=params, timeout=self.timeout)
        if not resp.ok:
            raise PulseError(f"{resp.status_code}: {resp.text[:200]}")
        return resp.json()

    def _post(self, path: str, data: Optional[dict] = None) -> dict | list | bytes:
        url = f"{self.base_url}{path}"
        resp = self._session.post(url, json=data, timeout=self.timeout)
        if not resp.ok:
            raise PulseError(f"{resp.status_code}: {resp.text[:200]}")
        if resp.headers.get("Content-Type", "").startswith("application/"):
            if "json" in resp.headers["Content-Type"]:
                return resp.json()
            return resp.content
        return resp.content

    # ────────────────── Endpoints ──────────────────

    def me(self) -> dict:
        return self._get("/v1/me")  # type: ignore

    def subscriptions(self, active_only: bool = False) -> list[dict]:
        return self._get("/v1/subscriptions",
                          params={"active_only": str(active_only).lower()})  # type: ignore

    def token_usage(self, since: Optional[str] = None, limit: int = 1000) -> list[dict]:
        params: dict = {"limit": limit}
        if since:
            params["since"] = since
        return self._get("/v1/token_usage", params=params)  # type: ignore

    def monthly_stats(self) -> dict:
        return self._get("/v1/stats/monthly")  # type: ignore

    def leaderboard(self, category: str, window: str = "monthly",
                     scope: str = "friends") -> list[dict]:
        return self._get(
            f"/v1/leaderboard/{category}",
            params={"window": window, "scope": scope},
        )  # type: ignore

    def export(self, format: str = "csv") -> bytes:
        url = f"{self.base_url}/v1/export?{urlencode({'format': format})}"
        resp = self._session.post(url, timeout=self.timeout * 3)
        if not resp.ok:
            raise PulseError(f"{resp.status_code}: {resp.text[:200]}")
        return resp.content
