"""FX rate fetcher with disk cache and hardcoded fallback.

Uses https://api.frankfurter.dev (free, no API key, ECB-sourced rates).
Cached on disk for 24h to avoid hammering the API.
"""
from __future__ import annotations

import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

CACHE_PATH = Path(__file__).parent / "data" / "fx_cache.json"
CACHE_TTL_HOURS = 24

# Used if the API is unreachable. Approximate rates (USD base) — update if drifted.
FALLBACK_RATES = {
    "USD": 1.0,
    "THB": 36.0,
    "EUR": 0.92,
    "GBP": 0.79,
    "JPY": 156.0,
    "SGD": 1.35,
    "MYR": 4.70,
    "CNY": 7.20,
    "KRW": 1380.0,
    "AUD": 1.50,
    "CAD": 1.36,
    "CHF": 0.90,
    "INR": 83.0,
    "PHP": 56.0,
    "IDR": 16000.0,
    "HKD": 7.80,
    "SEK": 10.5,
    "NOK": 10.6,
    "DKK": 6.85,
    "PLN": 4.05,
    "MXN": 17.0,
    "TRY": 32.0,
    "BRL": 5.10,
    "NZD": 1.65,
    "ZAR": 18.5,
    "CZK": 23.0,
    "HUF": 360.0,
    "ILS": 3.70,
}


def _fetch_online(base: str) -> dict | None:
    url = f"https://api.frankfurter.dev/v1/latest?base={base}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "life-tracker/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
    except Exception:
        return None
    rates = dict(data.get("rates", {}))
    rates[base] = 1.0  # base implicit
    return {
        "base": base,
        "rates": rates,
        "date": data.get("date"),
        "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": "frankfurter.dev (ECB)",
    }


def _load_cache() -> dict | None:
    if not CACHE_PATH.exists():
        return None
    try:
        return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return None


def _save_cache(data: dict) -> None:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")


def _is_fresh(cache: dict, base: str) -> bool:
    if cache.get("base") != base:
        return False
    try:
        fetched = datetime.fromisoformat(cache["fetched_at"])
        age_h = (datetime.now(timezone.utc) - fetched).total_seconds() / 3600
        return age_h < CACHE_TTL_HOURS
    except Exception:
        return False


def get_rates(base: str = "USD", refresh: bool = False) -> dict:
    """Returns dict with keys: base, rates, date, fetched_at, source.

    `rates` maps currency codes to "units per 1 base unit" (e.g. THB per 1 USD).
    Always includes the base itself at 1.0. Falls back to FALLBACK_RATES if both
    cache and online fetch fail.
    """
    if not refresh:
        cache = _load_cache()
        if cache and _is_fresh(cache, base):
            return cache

    fresh = _fetch_online(base)
    if fresh:
        _save_cache(fresh)
        return fresh

    # Try stale cache before falling back to hardcoded
    stale = _load_cache()
    if stale and stale.get("base") == base:
        stale["source"] = (stale.get("source") or "") + " (stale, API unreachable)"
        return stale

    return {
        "base": "USD",
        "rates": dict(FALLBACK_RATES),
        "date": "fallback",
        "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": "hardcoded fallback (API unreachable)",
    }


def convert(amount: float, from_cur: str, to_cur: str, rates_data: dict | None = None) -> float:
    """Convert `amount` from `from_cur` to `to_cur`."""
    if from_cur == to_cur:
        return amount
    if rates_data is None:
        rates_data = get_rates()
    rates = rates_data.get("rates", {})
    base = rates_data.get("base", "USD")

    # Step 1: amount -> base
    if from_cur == base:
        in_base = amount
    else:
        rate_from = rates.get(from_cur)
        if not rate_from:
            return amount
        in_base = amount / rate_from  # rates are "units per 1 base"

    # Step 2: base -> to
    if to_cur == base:
        return in_base
    rate_to = rates.get(to_cur)
    if not rate_to:
        return in_base
    return in_base * rate_to


def list_currencies(rates_data: dict | None = None) -> list[str]:
    if rates_data is None:
        rates_data = get_rates()
    return sorted(rates_data.get("rates", {}).keys())


CURRENCY_SYMBOLS: dict[str, str] = {
    "USD": "$", "THB": "฿", "EUR": "€", "GBP": "£",
    "JPY": "¥", "CNY": "¥", "SGD": "S$", "MYR": "RM",
    "KRW": "₩", "AUD": "A$", "CAD": "C$", "CHF": "CHF ",
    "INR": "₹", "PHP": "₱", "IDR": "Rp", "HKD": "HK$",
    "SEK": "kr", "NOK": "kr", "DKK": "kr", "PLN": "zł",
    "MXN": "Mex$", "TRY": "₺", "BRL": "R$", "NZD": "NZ$",
    "ZAR": "R", "CZK": "Kč", "HUF": "Ft", "ILS": "₪",
}

NO_DECIMAL = {"JPY", "KRW", "IDR", "VND", "HUF", "TWD"}


def symbol(code: str) -> str:
    return CURRENCY_SYMBOLS.get(code.upper(), code.upper() + " ")


def default_decimals(code: str) -> int:
    return 0 if code.upper() in NO_DECIMAL else 0  # default 0 for KPI density


if __name__ == "__main__":
    import pprint
    pprint.pprint(get_rates(refresh=True))
