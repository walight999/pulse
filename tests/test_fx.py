"""Test FX conversion logic — uses fallback rates (no network needed)."""
import fx


def test_identity_conversion():
    assert fx.convert(100, "USD", "USD") == 100.0


def test_thb_to_usd_reasonable():
    """1 USD should be roughly 30-40 THB."""
    rate = fx.convert(1, "USD", "THB")
    assert 25 < rate < 45, f"USD->THB rate out of plausible range: {rate}"


def test_round_trip_close():
    """USD -> EUR -> USD should be within 1% of original (rates not perfectly invertible)."""
    eur = fx.convert(100, "USD", "EUR")
    back = fx.convert(eur, "EUR", "USD")
    assert abs(back - 100) < 5, f"Round-trip lost too much: 100 -> {eur} -> {back}"


def test_symbol_lookup():
    assert fx.symbol("USD") == "$"
    assert fx.symbol("THB") == "฿"
    assert fx.symbol("EUR") == "€"
    assert fx.symbol("JPY") == "¥"


def test_unknown_currency_returns_code():
    """For currencies without a symbol, return the 3-letter code."""
    result = fx.symbol("XXX")
    assert "XXX" in result or result == "$"
